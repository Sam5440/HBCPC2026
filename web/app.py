from __future__ import annotations

import difflib
import json
import math
import os
import subprocess
import sys
import threading
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

import markdown
from flask import Flask, flash, redirect, render_template, request, url_for
from markupsafe import Markup

try:
    import psutil
except ImportError:  # pragma: no cover
    psutil = None


def resource_root() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[1]


def runtime_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return resource_root()


ROOT = resource_root()
RUNTIME_ROOT = runtime_root()
WEB = ROOT / "web"
RUNTIME_WEB = RUNTIME_ROOT / "web_runtime"
SUBMISSIONS = RUNTIME_WEB / "submissions"
BUILD = RUNTIME_WEB / "build"
LETTERS = list("ABCDEFGHIJKLM")
MAX_CODE_SIZE = 512 * 1024


app = Flask(
    __name__,
    template_folder=str(WEB / "templates"),
    static_folder=str(WEB / "static"),
)
app.secret_key = "local-hbcpc-judge"


def load_manifest() -> dict:
    with (ROOT / "manifest.json").open("r", encoding="utf-8") as f:
        return json.load(f)


MANIFEST = load_manifest()


def problem_cases(letter: str) -> list[Path]:
    return sorted((ROOT / "data" / letter).glob("*.in"))


def count_cases(letter: str) -> int:
    return len(problem_cases(letter))


def sample_code(letter: str) -> str:
    return f"""#include <bits/stdc++.h>
using namespace std;

int main() {{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // paste your solution for problem {letter}
    return 0;
}}
"""


def render_statement_markdown(letter: str) -> Markup:
    text = (ROOT / "problems" / f"{letter}.md").read_text(encoding="utf-8", errors="replace")
    html = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "nl2br"],
        output_format="html5",
    )
    return Markup(html)


def read_submission_code() -> str:
    code = request.form.get("code", "")
    file = request.files.get("source")
    if file and file.filename:
        code = file.read().decode("utf-8", errors="replace")
    return code


def normalize(text: str) -> str:
    return "\n".join(text.strip().splitlines()).strip()


def compare_float(out: str, ans: str) -> bool:
    got = out.split()
    exp = ans.split()
    if len(got) != len(exp):
        return False
    for a, b in zip(got, exp):
        try:
            x = float(a)
            y = float(b)
        except ValueError:
            return False
        if math.isnan(x):
            return False
        tol = 1e-9 * max(1.0, abs(y))
        if abs(x - y) > tol:
            return False
    return True


def text_diff(expected: str, actual: str) -> str:
    return "\n".join(
        difflib.unified_diff(
            expected.splitlines(),
            actual.splitlines(),
            fromfile="expected",
            tofile="actual",
            lineterm="",
        )
    )


def ensure_tool(source: Path, exe: Path) -> tuple[bool, str]:
    if exe.exists() and exe.stat().st_mtime >= source.stat().st_mtime:
        return True, ""
    exe.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["g++", "-std=c++17", "-O2", str(source), "-o", str(exe)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=60,
    )
    return proc.returncode == 0, proc.stderr


def run_external_checker(letter: str, inp: Path, out: Path, ans: Path) -> tuple[bool, str]:
    checker_map = {
        "E": (ROOT / "checker" / "E" / "validator.cpp", BUILD / "tools" / "E_validator.exe", [str(inp), str(out)]),
        "K": (ROOT / "checker" / "K" / "validator.cpp", BUILD / "tools" / "K_validator.exe", [str(inp), str(out)]),
        "M": (ROOT / "checker" / "M" / "checker.cpp", BUILD / "tools" / "M_checker.exe", [str(inp), str(out)]),
    }
    source, exe, args = checker_map[letter]
    ok, err = ensure_tool(source, exe)
    if not ok:
        return False, f"checker compile failed:\n{err}"
    proc = subprocess.run(
        [str(exe), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=30,
    )
    if proc.returncode == 0:
        return True, ""
    return False, proc.stderr or proc.stdout or "checker rejected output"


@dataclass
class CaseResult:
    case: str
    status: str
    time_ms: int
    expected: str = ""
    actual: str = ""
    diff: str = ""
    message: str = ""


def compile_submission(source: Path, exe: Path, limit: float) -> tuple[bool, str]:
    proc = subprocess.run(
        ["g++", "-std=c++17", "-O2", "-pipe", str(source), "-o", str(exe)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=max(10, int(limit * 10)),
    )
    return proc.returncode == 0, proc.stderr


def process_rss_bytes(proc: "psutil.Process") -> int:
    total = 0
    try:
        total += proc.memory_info().rss
        for child in proc.children(recursive=True):
            try:
                total += child.memory_info().rss
            except psutil.Error:
                pass
    except psutil.Error:
        return total
    return total


def run_case(exe: Path, inp: Path, out: Path, tl: float, memory_mb: int) -> tuple[str, int, str]:
    started = time.perf_counter()
    payload = inp.read_bytes()
    proc = subprocess.Popen(
        [str(exe)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    holder: dict[str, bytes | None] = {"stdout": None, "stderr": None}

    def communicate() -> None:
        try:
            stdout, stderr = proc.communicate(input=payload)
            holder["stdout"] = stdout
            holder["stderr"] = stderr
        except Exception as exc:
            holder["stdout"] = b""
            holder["stderr"] = str(exc).encode()

    worker = threading.Thread(target=communicate, daemon=True)
    worker.start()
    ps_proc = psutil.Process(proc.pid) if psutil else None
    limit_bytes = memory_mb * 1024 * 1024

    def save_stdout() -> None:
        out.write_bytes(holder["stdout"] or b"")

    while worker.is_alive():
        elapsed_sec = time.perf_counter() - started
        if elapsed_sec > tl:
            proc.kill()
            worker.join(timeout=1)
            save_stdout()
            elapsed = int((time.perf_counter() - started) * 1000)
            return "TLE", elapsed, "time limit exceeded"
        if ps_proc is not None and process_rss_bytes(ps_proc) > limit_bytes:
            proc.kill()
            worker.join(timeout=1)
            save_stdout()
            elapsed = int((time.perf_counter() - started) * 1000)
            return "RE", elapsed, "memory limit exceeded"
        time.sleep(0.01)
    worker.join()
    elapsed = int((time.perf_counter() - started) * 1000)
    stdout = holder["stdout"] or b""
    stderr = holder["stderr"] or b""
    out.write_bytes(stdout)
    if proc.returncode != 0:
        return "RE", elapsed, stderr.decode(errors="replace")[:2000]
    return "OK", elapsed, ""


def judge_output(letter: str, inp: Path, out: Path) -> tuple[str, str, str, str]:
    ans = inp.with_suffix(".ans")
    actual = out.read_text(encoding="utf-8", errors="replace")
    expected = ans.read_text(encoding="utf-8", errors="replace")
    if letter in {"E", "K", "M"}:
        accepted, message = run_external_checker(letter, inp, out, ans)
        return ("AC" if accepted else "WA", expected, actual, message)
    if letter == "L":
        return ("AC" if compare_float(actual, expected) else "WA", expected, actual, "")
    return ("AC" if normalize(actual) == normalize(expected) else "WA", expected, actual, "")


def judge_submission(letter: str, code: str) -> dict:
    if letter not in MANIFEST:
        raise ValueError("unknown problem")
    if len(code.encode("utf-8")) > MAX_CODE_SIZE:
        raise ValueError("source file is too large")
    problem = MANIFEST[letter]
    run_id = time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8]
    work = SUBMISSIONS / run_id
    work.mkdir(parents=True, exist_ok=True)
    src = work / f"{letter}.cpp"
    exe = work / f"{letter}.exe"
    src.write_text(code, encoding="utf-8")
    ok, cerr = compile_submission(src, exe, float(problem.get("time_limit", 2.0)))
    if not ok:
        return {
            "run_id": run_id,
            "problem": problem,
            "letter": letter,
            "compile_error": cerr,
            "results": [],
            "accepted": 0,
            "total": count_cases(letter),
            "score": 0,
        }
    results: list[CaseResult] = []
    tl = float(problem.get("time_limit", 2.0))
    memory_mb = int(problem.get("memory_limit_mb", 256))
    for inp in problem_cases(letter):
        out = work / (inp.stem + ".out")
        status, elapsed, message = run_case(exe, inp, out, tl, memory_mb)
        if status == "OK":
            status, expected, actual, checker_msg = judge_output(letter, inp, out)
            diff = text_diff(expected, actual) if status == "WA" else ""
            results.append(CaseResult(inp.name, status, elapsed, expected, actual, diff, checker_msg))
        else:
            actual = out.read_text(encoding="utf-8", errors="replace") if out.exists() else ""
            results.append(CaseResult(inp.name, status, elapsed, actual=actual, message=message))
    accepted = sum(1 for r in results if r.status == "AC")
    total = len(results)
    return {
        "run_id": run_id,
        "problem": problem,
        "letter": letter,
        "compile_error": "",
        "results": results,
        "accepted": accepted,
        "total": total,
        "score": round(accepted * 100 / total, 2) if total else 0,
    }


@app.route("/")
def index():
    problems = []
    for letter in LETTERS:
        item = dict(MANIFEST[letter])
        item["letter"] = letter
        item["case_count"] = count_cases(letter)
        problems.append(item)
    return render_template("index.html", problems=problems)


@app.route("/problem/<letter>", methods=["GET", "POST"])
def problem_detail(letter: str):
    if letter not in MANIFEST:
        return redirect(url_for("index"))
    item = dict(MANIFEST[letter])
    item["letter"] = letter
    item["case_count"] = count_cases(letter)
    if request.method == "POST":
        code = read_submission_code()
        if not code.strip():
            flash("请上传 C++ 源码或粘贴代码。")
            return render_template(
                "problem.html",
                problem=item,
                statement_html=render_statement_markdown(letter),
                sample_code="",
            )
        try:
            result = judge_submission(letter, code)
        except Exception as exc:
            flash(str(exc))
            return render_template(
                "problem.html",
                problem=item,
                statement_html=render_statement_markdown(letter),
                sample_code=code,
            )
        return render_template("result.html", result=result)
    return render_template(
        "problem.html",
        problem=item,
        statement_html=render_statement_markdown(letter),
        sample_code=sample_code(letter),
    )


@app.route("/submit/<letter>", methods=["GET", "POST"])
def submit(letter: str):
    if letter not in MANIFEST:
        return redirect(url_for("index"))
    if request.method == "POST":
        code = read_submission_code()
        if not code.strip():
            flash("请上传 C++ 源码或粘贴代码。")
            return redirect(url_for("problem_detail", letter=letter))
        result = judge_submission(letter, code)
        return render_template("result.html", result=result)
    return redirect(url_for("problem_detail", letter=letter))


@app.route("/submissions")
def submissions():
    SUBMISSIONS.mkdir(parents=True, exist_ok=True)
    runs = []
    for path in sorted(SUBMISSIONS.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        if path.is_dir():
            runs.append(
                {
                    "id": path.name,
                    "mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(path.stat().st_mtime)),
                }
            )
    return render_template("submissions.html", runs=runs[:100])


if __name__ == "__main__":
    SUBMISSIONS.mkdir(parents=True, exist_ok=True)
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=True)
