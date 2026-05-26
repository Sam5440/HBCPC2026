# Agent1 Independent Validation Report

工作范围：仅创建/修改 `subagents/agent1/` 下文件。  
编译环境：`g++ -std=c++17 -O2 -pipe`。  
编译结果：A-M 全部编译通过，无 CE。

评测说明：
- 已完成的评测采用 `data/{A..M}` 中 `.in/.ans` 离线运行。
- 普通题按 token 精确比较。
- L 按绝对/相对误差 `1e-9` 比较。
- E/K/M 为构造题；已运行部分先按 `.ans` 精确比较记录。
- 用户中断后停止继续跑超大压力点，未跑完部分按未完成原因记录。

| 题目 | 通过组数 | 失败/未完成组编号 | 类型 | 简短原因 |
| --- | ---: | --- | --- | --- |
| A | 25/25 | 无 | AC | 全部通过。 |
| B | 25/25 | 无 | AC | 全部通过。 |
| C | 未完成 | 01-25 | timeout/未完成 | 曾尝试整题评测，评测进程总超时；未继续跑压力点。源码已编译通过，但未形成完整逐组结果。 |
| D | 25/25 | 无 | AC | 全部通过。 |
| E | 1/25 | 01_regular, 02_regular, 03_regular, 04_regular, 05_regular, 06_regular, 07_regular, 08_regular, 09_regular, 10_regular, 11_stress, 12_stress, 13_stress, 14_stress, 15_stress, 16_stress, 17_stress, 18_stress, 20_edge, 21_edge, 22_edge, 23_edge, 24_edge, 25_edge | WA | 构造输出的电梯数量不是最小值；仅 19_edge 精确匹配。 |
| F | 25/25 | 无 | AC | 按离线格式读取 `n + 隐藏串` 并输出 1 的个数，全部通过。 |
| G | 未完成 | 01-25 | interrupted/未完成 | 开始评测后被用户中断；源码为朴素动态重算，预期大数据可能 TLE。 |
| H | 未完成 | 01-25 | 未运行 | 用户要求停止继续跑超大压力点；源码为朴素枚举子串，预期大数据 TLE。 |
| I | 25/25 | 无 | AC | 全部通过。 |
| J | 25/25 | 无 | AC | 全部通过。 |
| K | 未完成 | 01-25 | 未运行 | 用户要求停止继续跑超大压力点；当前源码仅按库存顺序输出，未验证区间合法性。 |
| L | 18/25 | 12_stress, 13_stress, 14_stress, 15_stress, 16_stress, 17_stress, 18_stress | TLE | 已完成组精度通过；压力点因朴素窗口内取最大半径导致超时。 |
| M | 未完成 | 01-25 | 未运行 | 用户要求停止继续跑超大压力点；当前源码逐只狗重建视线+BFS，预期大数据 TLE。 |

已创建/修改文件：
- `subagents/agent1/A.cpp`
- `subagents/agent1/B.cpp`
- `subagents/agent1/C.cpp`
- `subagents/agent1/D.cpp`
- `subagents/agent1/E.cpp`
- `subagents/agent1/F.cpp`
- `subagents/agent1/G.cpp`
- `subagents/agent1/H.cpp`
- `subagents/agent1/I.cpp`
- `subagents/agent1/J.cpp`
- `subagents/agent1/K.cpp`
- `subagents/agent1/L.cpp`
- `subagents/agent1/M.cpp`
- `subagents/agent1/eval_one.py`
- `subagents/agent1/report.md`

