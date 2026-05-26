# 题面还原 OJ 项目工作流提示词

下面这份提示词用于以后把“一份完整题面”快速还原成类似本项目的本地 OJ、数据包、题解、可靠性报告、EXE 和 GitHub Release。使用时，把花括号中的内容替换为实际信息即可。

## 可直接复制的完整提示词

```text
你是一个资深算法竞赛工程化助手。现在我会给你一份 OJ 题面，请你根据题面反推并生成一个完整的本地 OJ 项目。项目目标不是只写题解，而是要交付一套能运行、能评测、能复现、能打包发布的完整工程。

输入信息：
- 项目名称：{项目名称}
- 原始题面文件或题面内容：{题面路径或直接粘贴题面}
- 目标仓库地址：{可选，GitHub 仓库地址}
- 默认随机种子：{例如 20260526}
- 目标系统：Windows 优先，同时尽量兼容 Linux/macOS 的 Python 运行方式
- 编译环境：C++17，默认使用 g++

总要求：
1. 从原始题面中拆分出每一道题，保留原始题面，并生成每题独立 Markdown 文件。
2. 对每道题反推出题意、约束、输入输出格式、题型、标准解、暴力解、必要的 checker/validator/interactor。
3. 为每道题生成完整测试数据，每题固定 25 组，分为 10 组 regular、8 组 stress、7 组 edge。
4. 所有数据必须可复现，核心生成脚本必须支持固定随机种子。
5. `.ans` 答案由标准解自动生成；构造题、多解题、实数误差题、交互题必须使用对应 checker/validator/interactor，不允许只靠字符串强行比较。
6. 生成一个可本地运行的 Web OJ，题面用 Markdown 渲染，数学公式用 MathJax 正确渲染，题面和提交框在同一页。
7. 评测结果页面必须显示每一个数据点的状态、运行时间、实际输出；WA 时显示必要 diff。
8. 封装为 Windows 单文件 EXE，并把 EXE 输出到项目根目录。
9. 生成完整编译脚本，后续修改代码、题面、数据或 Web 后可以一键重新打包 EXE。
10. 生成 release 压缩包，压缩包内包含运行所需数据、题面、Web 静态资源、EXE、脚本和文档，但排除 build/dist/runtime/cache/submission 等构建产物。
11. 生成 README、数据可靠性报告、完整题解报告、子代理或独立验证汇总报告。
12. 写好 `.gitignore`，合理排除 EXE、zip、build、dist、runtime、pid、缓存、临时提交、编辑器竞赛插件缓存等文件。
13. 如果提供了 GitHub 仓库地址，请规范化初始化 Git，提交并推送到 main；如果已有 Release 要求，请发布 zip 到 Release。

建议的项目结构：

```text
{项目根目录}/
  OJ题目.md
  README.md
  DATA_RELIABILITY_REPORT.md
  SOLUTION_REPORT.md
  WORKFLOW_PROMPT.md
  subagent_report.md
  problem_list.md
  manifest.json
  requirements.txt
  launcher.py
  build_exe.ps1
  build_exe.bat
  run.sh
  .gitignore
  problems/
    A.md
    B.md
    ...
  data/
    A/
      01_regular.in
      01_regular.ans
      ...
      25_edge.in
      25_edge.ans
  solutions/
    A/
      std.cpp
      brute.cpp
    ...
  checker/
    {problem}/checker.cpp
    {problem}/validator.cpp
    {problem}/interactor.cpp
  scripts/
    build_core.py
    stress_test.py
    evaluate_subagents.py
    summarize_subagents.py
    build_release_package.ps1
  web/
    app.py
    templates/
    static/
      app.css
      mathjax/
  subagents/
    agent1/
    agent2/
    ...
```

执行流程：

第一阶段：解析题面
1. 读取原始题面，识别题号、题名、题意、输入输出、样例、约束、特殊说明。
2. 将题面拆成 `problems/{题号}.md`。
3. 生成 `manifest.json`，记录题号、题名、类型、时限、内存、checker/validator/interactor 路径。
4. 生成 `problem_list.md`，用表格列出每题类型和关键约束。
5. 如果题面存在明显 OCR 或编码问题，保留原文，同时在文档中注明推断依据。

第二阶段：反推解法
1. 每题生成 `solutions/{题号}/std.cpp`。
2. 每题生成 `solutions/{题号}/brute.cpp`，用于小规模对拍或语义验证。
3. 对普通题：标准解输出唯一答案。
4. 对构造题：生成 validator，用于检查用户输出是否合法且满足最优性或题目要求。
5. 对 Special Judge 题：生成 checker，支持误差、多解、合法性判定。
6. 对交互题：生成 interactor，并在本地 OJ 中明确交互题的处理限制。
7. 所有 C++ 源码使用 `g++ -std=c++17 -O2` 编译通过。

第三阶段：生成数据
1. 生成 `scripts/build_core.py`，统一创建题面拆分、解法、checker、数据和答案。
2. 每题生成 25 组数据：
   - `01_regular` 到 `10_regular`：常规数据
   - `11_stress` 到 `18_stress`：压力数据
   - `19_edge` 到 `25_edge`：边界数据
3. 压力数据要尽量覆盖约束上界、退化结构、极值参数、重复值、链/星/稠密/稀疏等风险点。
4. 边界数据要覆盖最小规模、全相等、单点、空边界、极端答案、不可行情况等。
5. 用标准解自动生成 `.ans`。
6. 生成数据时使用固定随机种子 `{随机种子}`。

第四阶段：验证数据可靠性
1. 编译所有 `solutions/*/std.cpp`、`solutions/*/brute.cpp` 和 `checker/**/*.cpp`。
2. 运行 `scripts/stress_test.py`，在随机小数据上对拍标准解和暴力解。
3. 检查每题是否恰好有 25 个 `.in` 和 25 个 `.ans`，分类是否为 10/8/7。
4. 对构造题、SPJ 题、交互题分别运行 validator/checker/interactor 的可用性检查。
5. 可以使用多个独立实现或子代理做交叉验证，生成 `subagent_report.md`。
6. 若任何数据点被多个独立实现共同指出问题，必须回到生成脚本修复，而不是手工改答案。

第五阶段：Web OJ
1. 使用 Flask 或项目内已有轻量 Web 框架实现本地 OJ。
2. 首页列出所有题目、题型、数据组数量。
3. 题目页左侧渲染 Markdown 题面，右侧提供 C++17 提交框和文件上传。
4. 使用本地 MathJax，保证 `$...$`、`$$...$$`、`\(...\)`、`\[...\]` 等数学公式正确渲染。
5. 提交后调用本机 `g++` 编译，逐个数据点运行。
6. 结果页显示每个数据点的 AC/WA/TLE/RE/CE、运行时间、实际输出、期望输出或 diff。
7. 对 checker/validator/interactor 题型调用对应判定程序。
8. 运行时输出写入 `web_runtime/` 或 `web/submissions/`，不要污染源码目录。

第六阶段：EXE 打包
1. 生成 `launcher.py`，负责选择可用端口、启动 Flask、自动打开浏览器。
2. 生成 `build_exe.ps1` 和 `build_exe.bat`。
3. 使用 PyInstaller 打包为单文件 `HBCPC-OJ.exe` 或 `{项目名}-OJ.exe`。
4. EXE 必须输出到项目根目录。
5. 打包时包含题面、数据、checker、web、MathJax、manifest、requirements 等必要资源。
6. 运行 EXE 后应能打开本地 Web OJ；若默认端口被占用，应自动换端口。

第七阶段：文档
1. 生成 `README.md`，说明：
   - 项目由 AI 根据题面反推生成。
   - 不是官方数据或官方题库。
   - 如何直接运行 EXE。
   - 如何用 Python 启动 Web。
   - 如何重新生成数据。
   - 如何重新打包 EXE。
   - 每个文件和文件夹的作用。
2. 生成 `DATA_RELIABILITY_REPORT.md`，说明：
   - 数据为什么比较可靠。
   - 数据如何生成。
   - 用了哪些验证流程。
   - 哪些题使用 checker/validator/interactor。
   - 可靠性边界：AI 反推，不是官方权威数据。
3. 生成 `SOLUTION_REPORT.md`，按从简单到困难的顺序写完整题解：
   - 题意简述
   - 关键观察
   - 做法
   - 复杂度
   - 对特殊题型的说明
4. 生成 `WORKFLOW_PROMPT.md`，保存本提示词，方便后续复用。

第八阶段：发布包
1. 生成 `scripts/build_release_package.ps1`。
2. 压缩包中包含：
   - EXE
   - README
   - 可靠性报告
   - 题解报告
   - 工作流提示词
   - problems
   - data
   - solutions
   - checker
   - scripts
   - web
   - manifest
   - requirements
3. 压缩包中排除：
   - build
   - dist
   - release 中间目录
   - web_runtime
   - web/submissions
   - __pycache__
   - *.pyc
   - *.exe 的重复构建产物
   - *.zip 的旧包
   - *.pid
   - .cph
4. 生成 `release/{项目名}-release.zip`。
5. 验证压缩包确实包含 EXE、数据、MathJax、README、报告，并确认没有 build/dist/runtime。

第九阶段：Git 与 Release
1. 先检查 `git status`，不要误删用户已有改动。
2. 写好 `.gitignore`。
3. 执行规范提交：
   - `git add ...`
   - `git commit -m "Initial AI-generated local judge"`
4. 如果提供远端：
   - `git remote add origin {仓库地址}`
   - `git branch -M main`
   - `git push -u origin main`
5. 如果要求发布 Release：
   - 创建 tag，例如 `v0.1.0`
   - 上传 release zip
   - 最终确认 Release 资产存在且可下载。

验收标准：
1. `python scripts\stress_test.py` 通过可对拍题目。
2. 每题数据数量检查通过：25 `.in` + 25 `.ans`，分类 10/8/7。
3. 所有 C++17 源码编译通过。
4. Web OJ 能启动，题面 Markdown 与数学公式正常渲染。
5. 提交页和题面在同一页。
6. 评测结果能显示每一个数据点的实际输出。
7. EXE 位于根目录并可启动。
8. release zip 包含所有运行所需文件，且排除了构建缓存。
9. README、可靠性报告、题解报告、工作流提示词齐全。
10. Git 工作区最终干净，远端仓库和 Release 状态明确。

重要边界：
1. 不要声称数据是官方数据。
2. 不要把 AI 反推题解包装成官方题解。
3. 对题面含糊、样例疑似错误、OCR 乱码或约束矛盾的地方，要在报告中明确说明推断依据。
4. 不能为了让数据通过而手工硬改答案，必须修正生成器、标准解或 checker。
5. 如果正式比赛使用，必须建议人工复核题意、数据强度、标准解和 checker。

请直接开始执行，不要只给计划。先读取题面和项目目录，再实现、验证、打包、写报告、提交。每个阶段完成后给出简短进度，最终汇总生成的文件、验证命令结果、Release 链接和仍需人工复核的风险点。
```

## 使用方法

1. 新建一个空目录，把完整题面保存成 `OJ题目.md`。
2. 把上面的提示词复制给 AI，并填入项目名、题面路径、随机种子和仓库地址。
3. 等 AI 完成后，重点检查 `DATA_RELIABILITY_REPORT.md`、`SOLUTION_REPORT.md`、`scripts/build_core.py` 和 `checker/`。
4. 若题面来自正式比赛，必须再做人工复核，尤其是构造题、交互题、Special Judge 和大数据上界。

## 推荐复核命令

```powershell
git status --short --branch
python scripts\stress_test.py
.\build_exe.ps1
.\scripts\build_release_package.ps1
```

压缩包复核重点：

- 包含 EXE、题面、数据、Web、MathJax、README、报告。
- 不包含 `build/`、`dist/`、`web_runtime/`、`web/submissions/`、`.cph/`。
- EXE 启动后能打开本地 Web OJ。
- Web 中 Markdown 和数学公式能正确渲染。
- 提交结果能显示每一个数据点的实际输出。
