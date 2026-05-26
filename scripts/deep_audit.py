#!/usr/bin/env python3
import argparse
import json
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "deep_audit"
BIN = BUILD / "bin"
TMP = BUILD / "tmp"
LETTERS = list("ABCDEFGHIJKLM")
NORMAL_EXACT = set("ABCDGHIJ")

PROFILES = {
    "quick": {
        "A": 60, "C": 80, "D": 60, "E": 30, "F": 20, "G": 80,
        "H": 60, "I": 60, "J": 80, "K": 80, "L": 60, "M": 50,
    },
    "strong": {
        "A": 180, "C": 220, "D": 180, "E": 100, "F": 60, "G": 260,
        "H": 180, "I": 180, "J": 240, "K": 260, "L": 180, "M": 160,
    },
}


class AuditError(RuntimeError):
    pass


def note(msg):
    print(msg, flush=True)


def norm_bytes(data):
    text = data.decode("utf-8-sig", errors="replace")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(line.rstrip() for line in text.strip().split("\n"))
    return text + ("\n" if text else "")


def run_cmd(cmd, *, timeout=60, input_bytes=None):
    p = subprocess.run(
        [str(x) for x in cmd],
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    if p.returncode != 0:
        raise AuditError(
            f"command failed: {' '.join(map(str, cmd))}\n"
            f"return code: {p.returncode}\n"
            f"stderr:\n{p.stderr.decode(errors='replace')}"
        )
    return p.stdout


def compile_cpp(src, out):
    out.parent.mkdir(parents=True, exist_ok=True)
    run_cmd(["g++", "-std=c++17", "-O2", str(src), "-o", str(out)], timeout=120)
    return out


def run_exe(exe, inp, timeout=20):
    if isinstance(inp, str):
        inp = inp.encode("utf-8")
    return run_cmd([exe], input_bytes=inp, timeout=timeout)


def compile_all():
    note("[1/7] compiling solutions and checkers")
    BIN.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    exes = {"std": {}, "brute": {}, "checker": {}}
    for letter in LETTERS:
        exes["std"][letter] = compile_cpp(ROOT / "solutions" / letter / "std.cpp", BIN / f"{letter}_std.exe")
        exes["brute"][letter] = compile_cpp(ROOT / "solutions" / letter / "brute.cpp", BIN / f"{letter}_brute.exe")
    checker_sources = {
        "E_validator": ROOT / "checker" / "E" / "validator.cpp",
        "F_interactor": ROOT / "checker" / "F" / "interactor.cpp",
        "K_validator": ROOT / "checker" / "K" / "validator.cpp",
        "L_checker": ROOT / "checker" / "L" / "checker.cpp",
        "M_checker": ROOT / "checker" / "M" / "checker.cpp",
    }
    for name, src in checker_sources.items():
        exes["checker"][name] = compile_cpp(src, BIN / f"{name}.exe")
    return exes


def assert_layout():
    note("[2/7] checking data layout")
    expected = [f"{i:02d}_regular" for i in range(1, 11)]
    expected += [f"{i:02d}_stress" for i in range(11, 19)]
    expected += [f"{i:02d}_edge" for i in range(19, 26)]
    for letter in LETTERS:
        d = ROOT / "data" / letter
        if not d.is_dir():
            raise AuditError(f"missing data directory: {d}")
        stems_in = sorted(p.stem for p in d.glob("*.in"))
        stems_ans = sorted(p.stem for p in d.glob("*.ans"))
        if stems_in != expected:
            raise AuditError(f"{letter}: input files do not match expected 25-case layout")
        if stems_ans != expected:
            raise AuditError(f"{letter}: answer files do not match expected 25-case layout")


def run_validator(exe, inp, out, timeout=20):
    run_cmd([exe, inp, out], timeout=timeout)


def run_checker_l(exe, inp, out, ans, timeout=20):
    run_cmd([exe, inp, out, ans], timeout=timeout)


def run_checker_m(exe, inp, out, timeout=20):
    run_cmd([exe, inp, out], timeout=timeout)


def parse_k_cases(text):
    toks = text.split()
    pos = 0
    t = int(toks[pos])
    pos += 1
    cases = []
    for _ in range(t):
        n = int(toks[pos]); m = int(toks[pos + 1])
        counts = [int(toks[pos + 2]), int(toks[pos + 3]), int(toks[pos + 4])]
        pos += 5
        segs = []
        for _ in range(m):
            l = int(toks[pos]); r = int(toks[pos + 1]); pos += 2
            segs.append((l - 1, r - 1))
        cases.append((n, m, counts, segs))
    return cases


def k_valid_line(n, counts, segs, line):
    line = line.strip()
    if line == "-1":
        return None
    if len(line) != n:
        return False
    if any(c not in "RGB" for c in line):
        return False
    if [line.count("R"), line.count("G"), line.count("B")] != counts:
        return False
    for l, r in segs:
        if len(set(line[l:r + 1])) > 2:
            return False
    return True


def k_exists_bruteforce(n, counts, segs):
    if n > 11:
        return None
    ans = ["?"] * n
    colors = "RGB"
    rem0 = counts[:]

    def dfs(i, rem):
        if i == n:
            for l, r in segs:
                if len(set(ans[l:r + 1])) > 2:
                    return False
            return True
        for c in range(3):
            if rem[c] == 0:
                continue
            ans[i] = colors[c]
            rem[c] -= 1
            if dfs(i + 1, rem):
                return True
            rem[c] += 1
            ans[i] = "?"
        return False

    return dfs(0, rem0)


def audit_existing_answers(exes):
    note("[3/7] verifying all existing .ans files")
    for letter in LETTERS:
        data_dir = ROOT / "data" / letter
        for inp_path in sorted(data_dir.glob("*.in")):
            ans_path = inp_path.with_suffix(".ans")
            inp = inp_path.read_bytes()

            if letter in NORMAL_EXACT:
                out = run_exe(exes["std"][letter], inp, timeout=120)
                if norm_bytes(out) != norm_bytes(ans_path.read_bytes()):
                    raise AuditError(f"{letter}/{inp_path.name}: std output differs from .ans")
            elif letter == "E":
                run_validator(exes["checker"]["E_validator"], inp_path, ans_path)
                out_path = TMP / f"E_{inp_path.stem}.out"
                out_path.write_bytes(run_exe(exes["std"]["E"], inp, timeout=120))
                run_validator(exes["checker"]["E_validator"], inp_path, out_path)
            elif letter == "F":
                toks = inp.decode("utf-8-sig").split()
                hidden = toks[1] if len(toks) > 1 else ""
                expected = f"{hidden.count('1')}\n"
                if norm_bytes(expected.encode()) != norm_bytes(ans_path.read_bytes()):
                    raise AuditError(f"F/{inp_path.name}: answer is not hidden-string one count")
            elif letter == "K":
                run_validator(exes["checker"]["K_validator"], inp_path, ans_path)
                out_path = TMP / f"K_{inp_path.stem}.out"
                out_path.write_bytes(run_exe(exes["std"]["K"], inp, timeout=120))
                run_validator(exes["checker"]["K_validator"], inp_path, out_path)
                for (n, _m, counts, segs), line in zip(parse_k_cases(inp.decode("utf-8-sig")), ans_path.read_text(encoding="utf-8-sig").splitlines()):
                    exists = k_exists_bruteforce(n, counts, segs)
                    if exists is not None and line.strip() == "-1" and exists:
                        raise AuditError(f"K/{inp_path.name}: .ans says -1 but brute found a construction")
            elif letter == "L":
                out_path = TMP / f"L_{inp_path.stem}.out"
                out_path.write_bytes(run_exe(exes["std"]["L"], inp, timeout=120))
                run_checker_l(exes["checker"]["L_checker"], inp_path, out_path, ans_path)
            elif letter == "M":
                run_checker_m(exes["checker"]["M_checker"], inp_path, ans_path)
                out_path = TMP / f"M_{inp_path.stem}.out"
                out_path.write_bytes(run_exe(exes["std"]["M"], inp, timeout=120))
                run_checker_m(exes["checker"]["M_checker"], inp_path, out_path)
            else:
                raise AuditError(f"unhandled letter {letter}")


def compare_stdout(letter, exes, inp, timeout=20):
    a = run_exe(exes["std"][letter], inp, timeout=timeout)
    b = run_exe(exes["brute"][letter], inp, timeout=timeout)
    if letter == "L":
        av = [float(x) for x in norm_bytes(a).split()]
        bv = [float(x) for x in norm_bytes(b).split()]
        if len(av) != len(bv) or any(abs(x - y) > 1e-8 * max(1.0, abs(y)) for x, y in zip(av, bv)):
            raise AuditError(f"{letter}: std/brute floating mismatch\ninput:\n{inp}\nstd:\n{a.decode()}\nbrute:\n{b.decode()}")
    elif norm_bytes(a) != norm_bytes(b):
        raise AuditError(f"{letter}: std/brute mismatch\ninput:\n{inp}\nstd:\n{a.decode(errors='replace')}\nbrute:\n{b.decode(errors='replace')}")


def gen_tree(rng, n, wlo=-20, whi=20):
    edges = []
    for v in range(2, n + 1):
        u = rng.randint(1, v - 1)
        w = rng.randint(wlo, whi)
        edges.append((u, v, w))
    return edges


def audit_a_c_d_h_i_j(exes, rng, cfg):
    note("[4/7] running independent exact/brute tests for A,C,D,H,I,J")
    for _ in range(cfg["A"]):
        n = rng.randint(1, 16)
        arr = [rng.randint(1, 5) for _ in range(n)]
        compare_stdout("A", exes, f"{n}\n{' '.join(map(str, arr))}\n", timeout=30)

    for _ in range(cfg["C"]):
        n = rng.randint(2, 35)
        q = rng.randint(1, 50)
        edges = gen_tree(rng, n)
        qs = [(rng.randint(1, n), rng.randint(1, n)) for _ in range(q)]
        inp = f"{n} {q}\n"
        inp += "\n".join(f"{u} {v} {w}" for u, v, w in edges) + "\n"
        inp += "\n".join(f"{x} {y}" for x, y in qs) + "\n"
        compare_stdout("C", exes, inp, timeout=30)
    for n in (2301, 2500):
        q = 25
        edges = [(i, i + 1, rng.randint(-100, 100)) for i in range(1, n)]
        qs = [(rng.randint(1, n), rng.randint(1, n)) for _ in range(q)]
        inp = f"{n} {q}\n" + "\n".join(f"{u} {v} {w}" for u, v, w in edges) + "\n"
        inp += "\n".join(f"{x} {y}" for x, y in qs) + "\n"
        compare_stdout("C", exes, inp, timeout=60)
    n = 2303
    q = 25
    edges = [(1, i, rng.randint(-100, 100)) for i in range(2, n + 1)]
    qs = [(rng.randint(1, n), rng.randint(1, n)) for _ in range(q)]
    inp = f"{n} {q}\n" + "\n".join(f"{u} {v} {w}" for u, v, w in edges) + "\n"
    inp += "\n".join(f"{x} {y}" for x, y in qs) + "\n"
    compare_stdout("C", exes, inp, timeout=60)
    n = 2305
    q = 6
    edges = gen_tree(rng, n)
    qs = [(rng.randint(1, n), rng.randint(1, n)) for _ in range(q)]
    inp = f"{n} {q}\n" + "\n".join(f"{u} {v} {w}" for u, v, w in edges) + "\n"
    inp += "\n".join(f"{x} {y}" for x, y in qs) + "\n"
    compare_stdout("C", exes, inp, timeout=60)

    for _ in range(cfg["D"]):
        n = rng.randint(2, 15)
        k = rng.randint(0, n - 2)
        s = "".join(rng.choice("abc") for _ in range(n))
        compare_stdout("D", exes, f"{n} {k} {s}\n", timeout=30)

    for _ in range(cfg["H"]):
        n = rng.randint(1, 14)
        q = rng.randint(1, 30)
        s = "".join(rng.choice("abc") for _ in range(n))
        queries = []
        expected = []
        for _ in range(q):
            l = rng.randint(1, n)
            r = rng.randint(l, n)
            queries.append((l, r))
            sub = s[l - 1:r]
            best = 0
            for i in range(len(sub)):
                for j in range(i + 1, len(sub) + 1):
                    pat = sub[i:j]
                    cnt = sum(1 for st in range(len(sub) - len(pat) + 1) if sub[st:st + len(pat)] == pat)
                    best = max(best, cnt)
            expected.append(str(best))
        inp = f"{n} {q}\n{s}\n" + "\n".join(f"{l} {r}" for l, r in queries) + "\n"
        out = norm_bytes(run_exe(exes["std"]["H"], inp)).split()
        if out != expected:
            raise AuditError(f"H: substring brute mismatch\ninput:\n{inp}\nstd:{out}\nexpected:{expected}")

    for _ in range(cfg["I"]):
        n = rng.randint(1, 8)
        m = rng.randint(1, 200)
        t = [rng.randint(1, 20) for _ in range(n)]
        ans = 0
        while sum(ans // x for x in t) < m:
            ans += 1
        inp = f"{n} {m}\n{' '.join(map(str, t))}\n"
        out = int(norm_bytes(run_exe(exes["std"]["I"], inp)).strip())
        if out != ans:
            raise AuditError(f"I: brute mismatch input={inp} std={out} expected={ans}")

    for _ in range(cfg["J"]):
        n = rng.randint(1, 15)
        m = rng.randint(1, 300)
        rows = [(rng.randint(1, 40), rng.randint(1, 300)) for _ in range(n)]
        best_cnt = -1
        best_id = 1
        for idx, (a, b) in enumerate(rows, 1):
            cur = 0
            for d in range(m // b + 1):
                cur = max(cur, 12 * d + (m - d * b) // a)
            if cur > best_cnt:
                best_cnt = cur
                best_id = idx
        inp = f"{n} {m}\n" + "\n".join(f"{a} {b}" for a, b in rows) + "\n"
        out = norm_bytes(run_exe(exes["std"]["J"], inp)).split()
        if out != [str(best_cnt), str(best_id)]:
            raise AuditError(f"J: brute mismatch input={inp} std={out} expected={[best_cnt, best_id]}")


def validate_e_random(exes, rng, count):
    note("[5/7] validating E constructive outputs")
    validator = exes["checker"]["E_validator"]
    for i in range(count):
        n = rng.choice([2, 3, 4, 5, 6, 7, 8, 999, 1000, rng.randint(2, 1000)])
        inp_path = TMP / f"E_rand_{i}.in"
        out_path = TMP / f"E_rand_{i}.out"
        inp_path.write_text(f"{n}\n", encoding="utf-8")
        out_path.write_bytes(run_exe(exes["std"]["E"], f"{n}\n", timeout=120))
        run_validator(validator, inp_path, out_path, timeout=60)


def simulate_f(exe, n, bits):
    p = subprocess.Popen(
        [str(exe)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    assert p.stdin is not None and p.stdout is not None
    p.stdin.write(f"{n}\n")
    p.stdin.flush()
    total = bits.count("1")
    queries = 0
    try:
        while True:
            line = p.stdout.readline()
            if not line:
                break
            parts = line.strip().split()
            if not parts:
                continue
            if parts[0] == "?":
                queries += 1
                if queries > 17:
                    raise AuditError("F: more than 17 queries")
                k = int(parts[1])
                pos = [int(x) for x in parts[2:]]
                if len(pos) != k or len(set(pos)) != k or any(x < 1 or x > n for x in pos):
                    raise AuditError(f"F: invalid query line: {line}")
                inside = sum(1 for x in pos if bits[x - 1] == "1")
                p.stdin.write(f"{inside * (total - inside)}\n")
                p.stdin.flush()
            elif parts[0] == "!":
                ans = int(parts[1])
                p.stdin.close()
                p.wait(timeout=5)
                if ans != total:
                    raise AuditError(f"F: wrong final answer n={n} expected={total} got={ans}")
                return
            else:
                raise AuditError(f"F: invalid output line: {line}")
    finally:
        if p.poll() is None:
            p.kill()
    raise AuditError("F: contestant terminated without final answer")


def audit_f(exes, rng, count):
    note("[6/7] simulating F interactive protocol")
    cases = [(1, "1"), (2, "10"), (2, "11"), (17, "1" + "0" * 16), (128, "1" * 128)]
    for _ in range(count):
        n = rng.randint(1, 220)
        bits = ["1" if rng.random() < 0.35 else "0" for _ in range(n)]
        if "1" not in bits:
            bits[rng.randrange(n)] = "1"
        cases.append((n, "".join(bits)))
    for n, bits in cases:
        simulate_f(exes["std"]["F"], n, bits)


def g_expected(inp):
    toks = inp.split()
    pos = 0
    n = int(toks[pos]); m = int(toks[pos + 1]); q = int(toks[pos + 2]); pos += 3
    a = [0] + [int(toks[pos + i]) for i in range(n)]
    pos += n
    edges = []
    for _ in range(m):
        u = int(toks[pos]); v = int(toks[pos + 1]); d = int(toks[pos + 2]); pos += 3
        edges.append((d, u, v))
    edges.sort()

    def find(p, x):
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    out = []
    for _ in range(q):
        op = int(toks[pos]); pos += 1
        if op == 1:
            c = int(toks[pos]); t = int(toks[pos + 1]); pos += 2
            a[c] = t
        else:
            k = int(toks[pos]); pos += 1
            top = sorted(range(1, n + 1), key=lambda x: (-a[x], x))[:k]
            if k <= 1:
                out.append("0")
                continue
            selected = [0] * (n + 1)
            for x in top:
                selected[x] = 1
            p = list(range(n + 1))
            sz = [1] * (n + 1)
            cnt = selected[:]
            ans = 0
            for d, u, v in edges:
                ru = find(p, u); rv = find(p, v)
                if ru != rv:
                    if sz[ru] < sz[rv]:
                        ru, rv = rv, ru
                    p[rv] = ru
                    sz[ru] += sz[rv]
                    cnt[ru] += cnt[rv]
                if cnt[find(p, u)] == k:
                    ans = d
                    break
            out.append(str(ans))
    return out


def audit_g(exes, rng, count):
    note("[7/7] running independent simulations for G,K,L,M")
    for case_id in range(count):
        n = rng.randint(2, 11)
        possible = [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]
        rng.shuffle(possible)
        used = set()
        edges = []
        for v in range(2, n + 1):
            u = rng.randint(1, v - 1)
            d = rng.randint(1, 50)
            edges.append((u, v, d))
            used.add((min(u, v), max(u, v)))
        for u, v in possible:
            if (u, v) in used:
                continue
            if rng.random() < 0.35:
                edges.append((u, v, rng.randint(1, 50)))
        m = len(edges)
        q = rng.randint(5, 35)
        a = [rng.randint(1, 40) for _ in range(n)]
        ops = []
        for i in range(q):
            if i % 7 == 0:
                ops.append(f"2 {n}")
            elif rng.random() < 0.4:
                ops.append(f"1 {rng.randint(1, n)} {rng.randint(1, 40)}")
            else:
                ops.append(f"2 {rng.randint(1, n)}")
        inp = f"{n} {m} {q}\n{' '.join(map(str, a))}\n"
        inp += "\n".join(f"{u} {v} {d}" for u, v, d in edges) + "\n"
        inp += "\n".join(ops) + "\n"
        expected = g_expected(inp)
        got = norm_bytes(run_exe(exes["std"]["G"], inp, timeout=30)).split()
        if got != expected:
            raise AuditError(f"G: independent mismatch case={case_id}\ninput:\n{inp}\nstd:{got}\nexpected:{expected}")


def audit_k(exes, rng, count):
    cases = []
    for _ in range(count):
        n = rng.randint(3, 11)
        r = rng.randint(0, n)
        g = rng.randint(0, n - r)
        b = n - r - g
        starts = list(range(0, n - 1))
        rng.shuffle(starts)
        segs = []
        occupied = [False] * n
        for l in starts:
            if occupied[l]:
                continue
            rr = rng.randint(l + 1, n - 1)
            if any(occupied[i] for i in range(l, rr + 1)):
                continue
            if rng.random() < 0.45:
                for i in range(l, rr + 1):
                    occupied[i] = True
                segs.append((l, rr))
            if len(segs) >= 3:
                break
        if not segs:
            l = rng.randint(0, n - 2)
            segs = [(l, rng.randint(l + 1, n - 1))]
        segs.sort()
        cases.append((n, [r, g, b], segs))
    inp = str(len(cases)) + "\n"
    for n, counts, segs in cases:
        inp += f"{n} {len(segs)} {counts[0]} {counts[1]} {counts[2]}\n"
        inp += "\n".join(f"{l + 1} {r + 1}" for l, r in segs) + "\n"
    out_lines = norm_bytes(run_exe(exes["std"]["K"], inp, timeout=60)).splitlines()
    if len(out_lines) != len(cases):
        raise AuditError("K: wrong number of output lines")
    for idx, ((n, counts, segs), line) in enumerate(zip(cases, out_lines)):
        valid = k_valid_line(n, counts, segs, line)
        exists = k_exists_bruteforce(n, counts, segs)
        if valid is False:
            raise AuditError(f"K: invalid construction at case {idx}: {line}")
        if valid is None and exists:
            raise AuditError(f"K: false -1 at case {idx}: n={n} counts={counts} segs={segs}")
        if valid is True and exists is False:
            raise AuditError(f"K: construction exists but brute says impossible at case {idx}")


def l_expected_case(points, k):
    if k == 1:
        return 0.0
    pi = math.pi
    arr = []
    for x, y in points:
        ang = math.atan2(y, x)
        if ang < 0:
            ang += 2 * pi
        arr.append((ang, x * x + y * y))
    arr.sort()
    n = len(arr)
    best = float("inf")
    for i in range(n):
        for step in range(n):
            j = i + step
            width = (arr[j % n][0] + (2 * pi if j >= n else 0.0)) - arr[i][0]
            inside = []
            for ang, r2 in arr:
                rel = ang - arr[i][0]
                if rel < -1e-14:
                    rel += 2 * pi
                if rel <= width + 1e-14:
                    inside.append(r2)
            if len(inside) >= k:
                best = min(best, 0.5 * width * max(inside))
    return best


def audit_l(exes, rng, count):
    cases = []
    for _ in range(count):
        n = rng.randint(1, 12)
        k = rng.randint(1, n)
        pts = []
        for _ in range(n):
            if rng.random() < 0.25:
                base = rng.choice([(1, 0), (0, 1), (-1, 0), (1, 1)])
                mul = rng.randint(1, 20)
                pts.append((base[0] * mul, base[1] * mul))
            else:
                x = y = 0
                while x == 0 and y == 0:
                    x = rng.randint(-10, 10)
                    y = rng.randint(-10, 10)
                pts.append((x, y))
        cases.append((n, k, pts))
    inp = str(len(cases)) + "\n"
    for n, k, pts in cases:
        inp += f"{n} {k}\n" + "\n".join(f"{x} {y}" for x, y in pts) + "\n"
    got = [float(x) for x in norm_bytes(run_exe(exes["std"]["L"], inp, timeout=60)).split()]
    if len(got) != len(cases):
        raise AuditError("L: wrong number of outputs")
    for i, ((n, k, pts), val) in enumerate(zip(cases, got)):
        exp = l_expected_case(pts, k)
        if abs(val - exp) > 1e-8 * max(1.0, abs(exp)):
            raise AuditError(f"L: independent mismatch case={i} got={val} expected={exp} n={n} k={k} pts={pts}")


DOGS = "UDLR"


def m_dog(c):
    return c in DOGS


def m_dir(c):
    return {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}[c]


def m_can(grid, sleep_idx):
    n = len(grid)
    m = len(grid[0])
    dogs = []
    s = e = None
    for i in range(n):
        for j in range(m):
            if m_dog(grid[i][j]):
                dogs.append((i, j))
            elif grid[i][j] == "S":
                s = (i, j)
            elif grid[i][j] == "E":
                e = (i, j)
    seen = [[False] * m for _ in range(n)]
    for idx, (r, c) in enumerate(dogs):
        if idx == sleep_idx:
            continue
        dr, dc = m_dir(grid[r][c])
        nr, nc = r + dr, c + dc
        while 0 <= nr < n and 0 <= nc < m and grid[nr][nc] != "#" and not m_dog(grid[nr][nc]):
            seen[nr][nc] = True
            nr += dr
            nc += dc

    def free(r, c):
        return 0 <= r < n and 0 <= c < m and grid[r][c] != "#" and not m_dog(grid[r][c]) and not seen[r][c]

    if s is None or e is None or not free(*s) or not free(*e):
        return False
    q = deque([s])
    vis = {s}
    while q:
        r, c = q.popleft()
        if (r, c) == e:
            return True
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if free(nr, nc) and (nr, nc) not in vis:
                vis.add((nr, nc))
                q.append((nr, nc))
    return False


def m_expected(grid):
    dogs = [(i, j) for i, row in enumerate(grid) for j, c in enumerate(row) if m_dog(c)]
    if m_can(grid, -1):
        return f"{dogs[0][0] + 1} {dogs[0][1] + 1}"
    for idx, (r, c) in enumerate(dogs):
        if m_can(grid, idx):
            return f"{r + 1} {c + 1}"
    return "-1 -1"


def gen_m_grid(rng):
    for _ in range(500):
        n = rng.randint(2, 7)
        m = rng.randint(2, 7)
        cells = [["." for _ in range(m)] for _ in range(n)]
        s = (rng.randrange(n), rng.randrange(m))
        e = (rng.randrange(n), rng.randrange(m))
        if e == s:
            continue
        cells[s[0]][s[1]] = "S"
        cells[e[0]][e[1]] = "E"
        dog_count = rng.randint(1, min(5, n * m - 2))
        empties = [(i, j) for i in range(n) for j in range(m) if cells[i][j] == "."]
        rng.shuffle(empties)
        for i, j in empties[:dog_count]:
            cells[i][j] = rng.choice(DOGS)
        for i, j in empties[dog_count:]:
            if rng.random() < 0.18:
                cells[i][j] = "#"
        grid = ["".join(row) for row in cells]
        if m_can(grid, -2) or True:
            # Keep only inputs satisfying the statement guarantee for S/E.
            if m_can_start_end_not_seen(grid):
                return grid
    return ["S.", "RE"]


def m_can_start_end_not_seen(grid):
    n = len(grid)
    m = len(grid[0])
    dogs = []
    s = e = None
    for i in range(n):
        for j in range(m):
            if m_dog(grid[i][j]):
                dogs.append((i, j))
            elif grid[i][j] == "S":
                s = (i, j)
            elif grid[i][j] == "E":
                e = (i, j)
    seen = [[False] * m for _ in range(n)]
    for r, c in dogs:
        dr, dc = m_dir(grid[r][c])
        nr, nc = r + dr, c + dc
        while 0 <= nr < n and 0 <= nc < m and grid[nr][nc] != "#" and not m_dog(grid[nr][nc]):
            seen[nr][nc] = True
            nr += dr
            nc += dc
    return s is not None and e is not None and not seen[s[0]][s[1]] and not seen[e[0]][e[1]]


def audit_m(exes, rng, count):
    cases = [gen_m_grid(rng) for _ in range(count)]
    inp = str(len(cases)) + "\n"
    for grid in cases:
        inp += f"{len(grid)} {len(grid[0])}\n" + "\n".join(grid) + "\n"
    got = norm_bytes(run_exe(exes["std"]["M"], inp, timeout=60)).splitlines()
    expected = [m_expected(grid) for grid in cases]
    if got != expected:
        for i, (g, e) in enumerate(zip(got, expected)):
            if g != e:
                raise AuditError(f"M: mismatch case={i} got={g} expected={e}\ngrid:\n" + "\n".join(cases[i]))
        raise AuditError("M: output count mismatch")


def run_constructive_and_simulation_tests(exes, rng, cfg):
    validate_e_random(exes, rng, cfg["E"])
    audit_f(exes, rng, cfg["F"])
    audit_g(exes, rng, cfg["G"])
    audit_k(exes, rng, cfg["K"])
    audit_l(exes, rng, cfg["L"])
    audit_m(exes, rng, cfg["M"])


def write_result_report(profile, seed, cfg):
    result = {
        "profile": profile,
        "seed": seed,
        "random_cases": cfg,
        "checked_letters": LETTERS,
        "status": "passed",
    }
    BUILD.mkdir(parents=True, exist_ok=True)
    (BUILD / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", choices=sorted(PROFILES), default="strong")
    ap.add_argument("--seed", type=int, default=20260526)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    cfg = PROFILES[args.profile]

    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True, exist_ok=True)

    exes = compile_all()
    assert_layout()
    audit_existing_answers(exes)
    audit_a_c_d_h_i_j(exes, rng, cfg)
    run_constructive_and_simulation_tests(exes, rng, cfg)
    write_result_report(args.profile, args.seed, cfg)
    note("deep audit passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AuditError as e:
        print(f"DEEP AUDIT FAILED:\n{e}", file=sys.stderr)
        raise SystemExit(1)
