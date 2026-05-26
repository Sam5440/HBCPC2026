#!/usr/bin/env python3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LETTERS = list("ABCDEFGHIJKLM")


SUMMARY = {
    "agent1": {
        "A": ("25/25", "-"), "B": ("25/25", "-"), "C": ("0/25", "01-25:INCOMPLETE/TLE"),
        "D": ("25/25", "-"), "E": ("1/25", "01-18,20-25:WA"), "F": ("25/25", "-"),
        "G": ("0/25", "01-25:INCOMPLETE/TLE"), "H": ("0/25", "01-25:INCOMPLETE/TLE"),
        "I": ("25/25", "-"), "J": ("25/25", "-"), "K": ("0/25", "01-25:INCOMPLETE/TLE"),
        "L": ("18/25", "12-18:TLE"), "M": ("0/25", "01-25:INCOMPLETE/TLE"),
    },
    "agent2": {x: ("25/25", "-") for x in LETTERS},
    "agent3": {
        "A": ("25/25", "-"), "B": ("25/25", "-"), "C": ("17/25", "11-18:TLE"),
        "D": ("25/25", "-"), "E": ("25/25", "-"), "F": ("25/25", "-"),
        "G": ("24/25", "11:TLE"), "H": ("25/25", "-"), "I": ("25/25", "-"),
        "J": ("25/25", "-"), "K": ("25/25", "-"), "L": ("25/25", "-"), "M": ("25/25", "-"),
    },
    "agent4": {
        "A": ("25/25", "-"), "B": ("25/25", "-"), "C": ("17/25", "11-18:TLE"),
        "D": ("25/25", "-"), "E": ("1/25", "01-18,20-25:WA"), "F": ("25/25", "-"),
        "G": ("25/25", "-"), "H": ("25/25", "-"), "I": ("25/25", "-"),
        "J": ("25/25", "-"), "K": ("25/25", "-"), "L": ("25/25", "-"), "M": ("25/25", "-"),
    },
    "agent5": {
        "A": ("25/25", "-"), "B": ("25/25", "-"), "C": ("17/25", "11-18:TLE"),
        "D": ("25/25", "-"), "E": ("1/25", "01-18,20-25:WA"), "F": ("25/25", "-"),
        "G": ("17/25", "11:WA,12-18:TLE"), "H": ("25/25", "-"), "I": ("25/25", "-"),
        "J": ("25/25", "-"), "K": ("3/25", "01-06,08-20,23-25:WA-by-exact-compare"),
        "L": ("25/25", "-"), "M": ("25/25", "-"),
    },
}


NOTES = {
    "E": "构造题。agent2/agent3 的输出经合法性判定通过；agent4/agent5/agent1 的失败为构造未满足最小电梯数或仅逐字比较失败。",
    "K": "构造题。agent2/agent3/agent4 输出经合法性判定通过；agent5 报告仅做逐字比较，未完成合法性判定。",
    "L": "SPJ 题。通过结果按 1e-9 绝对/相对误差判定。",
    "M": "SPJ/多解题。通过结果按 checker 判定合法性。",
}


def main():
    lines = [
        "# 5 个 Subagent 独立验证汇总报告",
        "",
        "本报告汇总 `subagents/agent1` 至 `subagents/agent5` 的独立实现与评测结果。5 个 agent 均只被要求基于题面原文实现解法；生成的源码位于各自目录下。",
        "",
        "判定口径：普通题按 `.ans` 比较；L 按 `1e-9` 误差；E/K/M 属于构造或多解题，优先按合法性 checker/validator 结论解释。agent1 在中断后保守标记未跑完项目为 `INCOMPLETE/TLE`。",
        "",
        "| 题目 | Agent1 | Agent2 | Agent3 | Agent4 | Agent5 | 主要失败原因 | 疑似数据错误 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for letter in LETTERS:
        passes = [SUMMARY[a][letter][0] for a in SUMMARY]
        failures = [SUMMARY[a][letter][1] for a in SUMMARY if SUMMARY[a][letter][1] != "-"]
        reason = "; ".join(f"{a}:{SUMMARY[a][letter][1]}" for a in SUMMARY if SUMMARY[a][letter][1] != "-") or "-"
        suspicious = "否"
        lines.append(f"| {letter} | {' | '.join(passes)} | {reason} | {suspicious} |")
    lines += [
        "",
        "## 失败原因分类",
        "",
        "- `TLE/INCOMPLETE`: 独立解复杂度不足或在停止请求后未继续跑超大压力点，不作为数据错误处理。",
        "- `WA`: 独立解算法错误、构造未满足最小性，或多解题仅做逐字比较导致的假阴性。",
        "- `CE/RE`: 本轮汇总未发现最终报告中的 CE/RE。",
        "",
        "## 题目备注",
    ]
    for letter in LETTERS:
        if letter in NOTES:
            lines.append(f"- {letter}: {NOTES[letter]}")
    lines += [
        "",
        "## 疑似数据错误处理",
        "",
        "未发现任何数据组导致 5 个 Subagent 全部失败：agent2 对 A-M 每题 25/25 通过，因此不存在“所有 Subagent 均失败”的数据组。本轮无需修复阶段二数据。",
    ]
    lines += [
        "",
        "## 每题独立解法路径",
        "",
        "| 题目 | 5 份独立 C++ 解法 |",
        "| --- | --- |",
    ]
    for letter in LETTERS:
        paths = ", ".join(f"`subagents/agent{i}/{letter}.cpp`" for i in range(1, 6))
        lines.append(f"| {letter} | {paths} |")
    lines += [
        "",
        "## 原始报告位置",
        "",
    ]
    for i in range(1, 6):
        lines.append(f"- `subagents/agent{i}/report.md`")
    (ROOT / "subagent_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("subagent_report.md generated")


if __name__ == "__main__":
    main()
