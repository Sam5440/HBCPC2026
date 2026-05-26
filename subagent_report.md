# 5 个 Subagent 独立验证汇总报告

本报告汇总 `subagents/agent1` 至 `subagents/agent5` 的独立实现与评测结果。5 个 agent 均只被要求基于题面原文实现解法；生成的源码位于各自目录下。

判定口径：普通题按 `.ans` 比较；L 按 `1e-9` 误差；E/K/M 属于构造或多解题，优先按合法性 checker/validator 结论解释。agent1 在中断后保守标记未跑完项目为 `INCOMPLETE/TLE`。

| 题目 | Agent1 | Agent2 | Agent3 | Agent4 | Agent5 | 主要失败原因 | 疑似数据错误 |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| A | 25/25 | 25/25 | 25/25 | 25/25 | 25/25 | - | 否 |
| B | 25/25 | 25/25 | 25/25 | 25/25 | 25/25 | - | 否 |
| C | 0/25 | 25/25 | 17/25 | 17/25 | 17/25 | agent1:01-25:INCOMPLETE/TLE; agent3:11-18:TLE; agent4:11-18:TLE; agent5:11-18:TLE | 否 |
| D | 25/25 | 25/25 | 25/25 | 25/25 | 25/25 | - | 否 |
| E | 1/25 | 25/25 | 25/25 | 1/25 | 1/25 | agent1:01-18,20-25:WA; agent4:01-18,20-25:WA; agent5:01-18,20-25:WA | 否 |
| F | 25/25 | 25/25 | 25/25 | 25/25 | 25/25 | - | 否 |
| G | 0/25 | 25/25 | 24/25 | 25/25 | 17/25 | agent1:01-25:INCOMPLETE/TLE; agent3:11:TLE; agent5:11:WA,12-18:TLE | 否 |
| H | 0/25 | 25/25 | 25/25 | 25/25 | 25/25 | agent1:01-25:INCOMPLETE/TLE | 否 |
| I | 25/25 | 25/25 | 25/25 | 25/25 | 25/25 | - | 否 |
| J | 25/25 | 25/25 | 25/25 | 25/25 | 25/25 | - | 否 |
| K | 0/25 | 25/25 | 25/25 | 25/25 | 3/25 | agent1:01-25:INCOMPLETE/TLE; agent5:01-06,08-20,23-25:WA-by-exact-compare | 否 |
| L | 18/25 | 25/25 | 25/25 | 25/25 | 25/25 | agent1:12-18:TLE | 否 |
| M | 0/25 | 25/25 | 25/25 | 25/25 | 25/25 | agent1:01-25:INCOMPLETE/TLE | 否 |

## 失败原因分类

- `TLE/INCOMPLETE`: 独立解复杂度不足或在停止请求后未继续跑超大压力点，不作为数据错误处理。
- `WA`: 独立解算法错误、构造未满足最小性，或多解题仅做逐字比较导致的假阴性。
- `CE/RE`: 本轮汇总未发现最终报告中的 CE/RE。

## 题目备注
- E: 构造题。agent2/agent3 的输出经合法性判定通过；agent4/agent5/agent1 的失败为构造未满足最小电梯数或仅逐字比较失败。
- K: 构造题。agent2/agent3/agent4 输出经合法性判定通过；agent5 报告仅做逐字比较，未完成合法性判定。
- L: SPJ 题。通过结果按 1e-9 绝对/相对误差判定。
- M: SPJ/多解题。通过结果按 checker 判定合法性。

## 疑似数据错误处理

未发现任何数据组导致 5 个 Subagent 全部失败：agent2 对 A-M 每题 25/25 通过，因此不存在“所有 Subagent 均失败”的数据组。本轮无需修复阶段二数据。

## 每题独立解法路径

| 题目 | 5 份独立 C++ 解法 |
| --- | --- |
| A | `subagents/agent1/A.cpp`, `subagents/agent2/A.cpp`, `subagents/agent3/A.cpp`, `subagents/agent4/A.cpp`, `subagents/agent5/A.cpp` |
| B | `subagents/agent1/B.cpp`, `subagents/agent2/B.cpp`, `subagents/agent3/B.cpp`, `subagents/agent4/B.cpp`, `subagents/agent5/B.cpp` |
| C | `subagents/agent1/C.cpp`, `subagents/agent2/C.cpp`, `subagents/agent3/C.cpp`, `subagents/agent4/C.cpp`, `subagents/agent5/C.cpp` |
| D | `subagents/agent1/D.cpp`, `subagents/agent2/D.cpp`, `subagents/agent3/D.cpp`, `subagents/agent4/D.cpp`, `subagents/agent5/D.cpp` |
| E | `subagents/agent1/E.cpp`, `subagents/agent2/E.cpp`, `subagents/agent3/E.cpp`, `subagents/agent4/E.cpp`, `subagents/agent5/E.cpp` |
| F | `subagents/agent1/F.cpp`, `subagents/agent2/F.cpp`, `subagents/agent3/F.cpp`, `subagents/agent4/F.cpp`, `subagents/agent5/F.cpp` |
| G | `subagents/agent1/G.cpp`, `subagents/agent2/G.cpp`, `subagents/agent3/G.cpp`, `subagents/agent4/G.cpp`, `subagents/agent5/G.cpp` |
| H | `subagents/agent1/H.cpp`, `subagents/agent2/H.cpp`, `subagents/agent3/H.cpp`, `subagents/agent4/H.cpp`, `subagents/agent5/H.cpp` |
| I | `subagents/agent1/I.cpp`, `subagents/agent2/I.cpp`, `subagents/agent3/I.cpp`, `subagents/agent4/I.cpp`, `subagents/agent5/I.cpp` |
| J | `subagents/agent1/J.cpp`, `subagents/agent2/J.cpp`, `subagents/agent3/J.cpp`, `subagents/agent4/J.cpp`, `subagents/agent5/J.cpp` |
| K | `subagents/agent1/K.cpp`, `subagents/agent2/K.cpp`, `subagents/agent3/K.cpp`, `subagents/agent4/K.cpp`, `subagents/agent5/K.cpp` |
| L | `subagents/agent1/L.cpp`, `subagents/agent2/L.cpp`, `subagents/agent3/L.cpp`, `subagents/agent4/L.cpp`, `subagents/agent5/L.cpp` |
| M | `subagents/agent1/M.cpp`, `subagents/agent2/M.cpp`, `subagents/agent3/M.cpp`, `subagents/agent4/M.cpp`, `subagents/agent5/M.cpp` |

## 原始报告位置

- `subagents/agent1/report.md`
- `subagents/agent2/report.md`
- `subagents/agent3/report.md`
- `subagents/agent4/report.md`
- `subagents/agent5/report.md`
