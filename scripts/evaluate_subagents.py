#!/usr/bin/env python3
import csv
import json
import math
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LETTERS = list("ABCDEFGHIJKLM")
AGENTS = [f"agent{i}" for i in range(1, 6)]
TIMEOUT = 3.0


def compile_cpp(src: Path, exe: Path):
    exe.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["g++", "-std=c++17", "-O2", str(src), "-o", str(exe)]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    if p.returncode:
        return False, p.stderr.decode(errors="replace")
    return True, ""


def normalize(s: bytes) -> str:
    return "\n".join(s.decode(errors="replace").strip().splitlines()).strip()


def compare_float(out: str, ans: str) -> bool:
    a = ans.split()
    b = out.split()
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        try:
            ex = float(x)
            got = float(y)
        except ValueError:
            return False
        tol = 1e-9 * max(1.0, abs(ex))
        if math.isnan(got) or abs(ex - got) > tol:
            return False
    return True


def run_exe(exe: Path, inp: Path, out_path: Path):
    try:
        p = subprocess.run([str(exe)], input=inp.read_bytes(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return "TLE", "timeout"
    out_path.write_bytes(p.stdout)
    if p.returncode != 0:
        return "RE", p.stderr.decode(errors="replace")[:300]
    return "DONE", ""


def run_checker(letter: str, inp: Path, out: Path, ans: Path | None = None):
    if letter == "E":
        cmd = [str(ROOT / "build" / "checker" / "E_validator.exe"), str(inp), str(out)]
    elif letter == "K":
        cmd = [str(ROOT / "build" / "checker" / "K_validator.exe"), str(inp), str(out)]
    elif letter == "M":
        cmd = [str(ROOT / "build" / "checker" / "M_checker.exe"), str(inp), str(out)]
    else:
        raise ValueError(letter)
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    return p.returncode == 0


def judge(letter: str, inp: Path, out_path: Path):
    ans_path = inp.with_suffix(".ans")
    if letter in {"E", "K", "M"}:
        return "AC" if run_checker(letter, inp, out_path, ans_path) else "WA"
    got = normalize(out_path.read_bytes())
    exp = normalize(ans_path.read_bytes())
    if letter == "L":
        return "AC" if compare_float(got, exp) else "WA"
    return "AC" if got == exp else "WA"


def ensure_checkers():
    checker_dir = ROOT / "build" / "checker"
    checker_dir.mkdir(parents=True, exist_ok=True)
    for rel, name in [
        ("checker/E/validator.cpp", "E_validator.exe"),
        ("checker/K/validator.cpp", "K_validator.exe"),
        ("checker/M/checker.cpp", "M_checker.exe"),
    ]:
        exe = checker_dir / name
        if not exe.exists():
            ok, err = compile_cpp(ROOT / rel, exe)
            if not ok:
                raise RuntimeError(err)


def evaluate():
    ensure_checkers()
    results = {}
    for agent in AGENTS:
        agent_dir = ROOT / "subagents" / agent
        results[agent] = {}
        for letter in LETTERS:
            src = agent_dir / f"{letter}.cpp"
            exe = ROOT / "build" / "subagents" / agent / f"{letter}.exe"
            if not src.exists():
                results[agent][letter] = [{"case": f.name, "status": "CE", "reason": "missing source"} for f in sorted((ROOT / "data" / letter).glob("*.in"))]
                continue
            ok, err = compile_cpp(src, exe)
            if not ok:
                results[agent][letter] = [{"case": f.name, "status": "CE", "reason": err[:300]} for f in sorted((ROOT / "data" / letter).glob("*.in"))]
                continue
            cases = []
            for inp in sorted((ROOT / "data" / letter).glob("*.in")):
                out = ROOT / "build" / "subagent_outputs" / agent / letter / (inp.stem + ".out")
                out.parent.mkdir(parents=True, exist_ok=True)
                status, reason = run_exe(exe, inp, out)
                if status == "DONE":
                    status = judge(letter, inp, out)
                    reason = "" if status == "AC" else "output mismatch or invalid construction"
                cases.append({"case": inp.name, "status": status, "reason": reason})
            results[agent][letter] = cases
    return results


def write_report(results):
    rows = []
    lines = ["# 5 个 Subagent 独立验证汇总报告", ""]
    lines.append("评测口径：重新编译 `subagents/agent{1..5}/{A..M}.cpp`；普通题逐字比较 `.ans`；L 使用 `1e-9` 误差；E/K/M 使用本仓库 validator/checker 判定多解合法性；单测试点运行超时阈值为 3 秒。")
    lines.append("")
    lines.append("| 题目 | Agent1 | Agent2 | Agent3 | Agent4 | Agent5 | 失败分类 | 疑似数据错误 |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |")
    all_suspicious = []
    for letter in LETTERS:
        by_agent = []
        fail_counts = defaultdict(int)
        all_failed = []
        case_names = [x["case"] for x in results["agent1"][letter]]
        for agent in AGENTS:
            cases = results[agent][letter]
            ac = sum(1 for c in cases if c["status"] == "AC")
            by_agent.append(f"{ac}/25")
            for c in cases:
                if c["status"] != "AC":
                    fail_counts[c["status"]] += 1
        for idx, case in enumerate(case_names):
            statuses = [results[a][letter][idx]["status"] for a in AGENTS]
            if all(s != "AC" for s in statuses):
                all_failed.append(case)
        if all_failed:
            all_suspicious.extend((letter, x) for x in all_failed)
        cls = ", ".join(f"{k}:{v}" for k, v in sorted(fail_counts.items())) or "-"
        suspicious = ", ".join(all_failed) if all_failed else "-"
        lines.append(f"| {letter} | {' | '.join(by_agent)} | {cls} | {suspicious} |")
    lines.append("")
    lines.append("## 每题失败明细")
    for letter in LETTERS:
        lines.append(f"\n### {letter}")
        for agent in AGENTS:
            fails = [c for c in results[agent][letter] if c["status"] != "AC"]
            if not fails:
                lines.append(f"- {agent}: 25/25 AC")
            else:
                compact = ", ".join(f"{c['case']}:{c['status']}" for c in fails[:30])
                if len(fails) > 30:
                    compact += f", ... 共 {len(fails)} 个失败"
                lines.append(f"- {agent}: {25-len(fails)}/25 AC；失败：{compact}")
    lines.append("")
    if all_suspicious:
        lines.append("## 疑似数据错误处理")
        lines.append("存在所有 Subagent 均失败的数据组，需人工复核。")
        for letter, case in all_suspicious:
            lines.append(f"- {letter}/{case}")
    else:
        lines.append("## 疑似数据错误处理")
        lines.append("未发现所有 5 个 Subagent 均失败的数据组；无需修复阶段二数据。")
    report = "\n".join(lines) + "\n"
    (ROOT / "subagent_report.md").write_text(report, encoding="utf-8")
    with (ROOT / "subagent_results.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["agent", "problem", "case", "status", "reason"])
        for agent in AGENTS:
            for letter in LETTERS:
                for c in results[agent][letter]:
                    w.writerow([agent, letter, c["case"], c["status"], c["reason"]])


def main():
    results = evaluate()
    write_report(results)
    print("subagent_report.md generated")


if __name__ == "__main__":
    main()
