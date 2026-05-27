# HBCPC 全题强审计报告

审计日期：2026-05-26

本报告记录本轮基于 K 题修复后的全题强检测结果。审计目标是检查 A-M 每一道题的标准程序、已有数据、答案文件、checker/validator/interactor 和关键边界条件，并补充更强的随机暴力/模拟测试。

## 结论

本轮新增并运行了强审计程序：

```powershell
python scripts\deep_audit.py --profile strong --seed 20260526
```

结果：通过。

同时复跑旧轻量对拍：

```powershell
python scripts\stress_test.py
```

结果：通过。

脚本语法检查：

```powershell
python -m py_compile scripts\deep_audit.py scripts\stress_test.py
```

结果：通过。

需要说明：本报告中的“通过”表示现有数据、答案、checker 和新增强随机/暴力检测均未再发现错误；这不是数学形式化证明，也不是官方数据对照证明。

## 本轮新增工具

新增文件：

```text
scripts/deep_audit.py
```

该脚本会执行以下检查：

1. 编译所有 `solutions/{A..M}/std.cpp` 和 `brute.cpp`。
2. 编译所有 checker、validator、interactor。
3. 检查每题数据文件结构是否为 25 组：10 组 regular、8 组 stress、7 组 edge。
4. 复算并验证所有已有 `.ans`。
5. 对普通题进行标准解与独立暴力/模拟结果核对。
6. 对构造题运行 validator，并对小规模数据做可行性暴力检查。
7. 对交互题 F 进行本地交互协议模拟。
8. 对 L、M 这类 Special Judge 题做独立几何/网格模拟。

本轮 strong 配置随机覆盖数量：

| 题号 | 强随机/暴力用例数 |
| --- | ---: |
| A | 180 |
| C | 220，另含链、星形、普通大树分支专项 |
| D | 180 |
| E | 100 |
| F | 60，另含固定边界交互用例 |
| G | 260 |
| H | 180 |
| I | 180 |
| J | 240 |
| K | 260 |
| L | 180 |
| M | 160 |

## 发现并修复的问题

### G 题：`k == n` 的未定义行为

原实现中：

```cpp
nth_element(id.begin(), id.begin()+k, id.end(), cmp);
```

当 `k == n` 时，`id.begin()+k == id.end()`，不满足 `nth_element` 对 `nth` 的参数要求，属于未定义行为。

已修复为：

```cpp
if (k < n) {
    nth_element(id.begin(), id.begin()+k, id.end(), cmp);
}
id.resize(k);
```

同步修改文件：

```text
solutions/G/std.cpp
solutions/G/brute.cpp
scripts/build_core.py
```

### L 题：同一射线与近共线方向的几何边界

强审计构造出同一射线上多个食物的用例，发现旧算法按“连续 k 个点”滑动窗口时，可能错误排除同角度但更远的点。后续补充近共线大坐标用例，覆盖直接用两个极角相减导致的消元误差。

原因：扇形角度区间包含边界；如果某个方向被包含，则该方向上的所有食物都会被包含，不能只选择其中一部分。

修复方式：

1. 先按约分后的方向向量 `(x/g, y/g)` 分组。
2. 每组记录：
   - 极角 `angle`
   - 食物数量 `cnt`
   - 该方向最大距离平方 `max_r2`
3. 在方向组上做双指针滑动窗口。
4. 用单调队列维护窗口中的最大 `max_r2`。
5. 窗口端点夹角用 `atan2(cross, dot)` 计算，避免接近共线时的极角相减精度损失。

同步修改文件：

```text
solutions/L/std.cpp
solutions/L/brute.cpp
scripts/build_core.py
SOLUTION_REPORT.md
```

已有 L 数据答案在修复后仍通过 checker 复核，说明现有 `.ans` 未被该边界影响。

## 每题检测明细

| 题号 | 已有数据验证 | 新增强检测方式 | 结果 |
| --- | --- | --- | --- |
| A | 25 组 `.ans` 由 `std` 复算精确匹配 | 小规模 `n <= 16`，与指数枚举 brute 对拍 180 组 | 通过 |
| B | 25 组固定输出精确匹配 | 固定输出一致性检查 | 通过 |
| C | 25 组 `.ans` 由 `std` 复算精确匹配 | 随机小树 brute；链式大树、星形大树、普通大树分支专项对拍 | 通过 |
| D | 25 组 `.ans` 由 `std` 复算精确匹配 | 小规模字符串与枚举 brute 对拍 180 组 | 通过 |
| E | 25 组 `.ans` 通过 validator | 随机 `n` 构造输出再过 validator 100 组 | 通过 |
| F | 25 组 `.ans` 等于隐藏串中 `1` 的数量 | 本地模拟交互协议，检查查询合法性、17 次限制和最终答案 | 通过 |
| G | 25 组 `.ans` 由修复后 `std` 复算精确匹配 | 独立 Python Kruskal 模拟 260 组，覆盖 `k=1`、`k=n`、更新操作、随机连通图 | 通过 |
| H | 25 组 `.ans` 由 `std` 复算精确匹配 | 小字符串枚举所有子串出现次数，和 `std` 对比 180 组 | 通过 |
| I | 25 组 `.ans` 由 `std` 复算精确匹配 | 小规模按时间从 0 递增暴力模拟 180 组 | 通过 |
| J | 25 组 `.ans` 由 `std` 复算精确匹配 | 小预算枚举购买整打数，验证贪心公式 240 组 | 通过 |
| K | 25 组 `.ans` 通过 validator | 随机小规模暴力枚举存在性，检查 false `-1`；随机构造输出合法性 260 组 | 通过 |
| L | 25 组由 checker 验证 `std` 输出与 `.ans` | 独立几何模拟 180 组，覆盖同角度/同射线边界 | 通过 |
| M | 25 组通过 checker，且 `std` 输出通过 checker | 独立网格视线+BFS+字典序模拟 160 组 | 通过 |

## 数据强度检查

每道题均保留 25 组数据，结构为：

```text
01_regular.in  ~ 10_regular.in
11_stress.in   ~ 18_stress.in
19_edge.in     ~ 25_edge.in
```

本轮脚本验证了所有 `.in` 均有同名 `.ans`，且文件布局完整。

新增检测对边界覆盖包括：

- 空输入/固定输出：B。
- 极小规模：A、E、F、H、I、K、L、M。
- 大数边界：I、J。
- 负权边：C。
- `k=1` 与 `k=n`：G、L。
- 构造题 false `-1` 风险：K。
- 同方向几何退化：L。
- 狗视线阻断、睡狗、多解字典序：M。
- 交互询问次数和询问集合合法性：F。

## 可复现命令

以后修改代码或数据后，建议按以下顺序复查：

```powershell
python -m py_compile scripts\deep_audit.py scripts\stress_test.py
python scripts\deep_audit.py --profile strong --seed 20260526
python scripts\stress_test.py
```

如果只想快速检查，可以运行：

```powershell
python scripts\deep_audit.py --profile quick --seed 20260526
```

## 剩余风险说明

1. 本项目由 AI 根据题面反推生成，并非官方题库，仍建议正式使用前进行人工复核。
2. 强审计包含现有数据复算、checker/validator、随机暴力和独立模拟，但不能替代数学证明。
3. C、G 等题的参考实现仍带有面向本项目生成数据的实现特征。强审计覆盖了当前数据和多种随机边界，但若要作为正式比赛题解，应进一步补充完整复杂度证明或替换为严格通用的最优算法。
4. 本轮未向远端仓库推送，也未发布 Release。
