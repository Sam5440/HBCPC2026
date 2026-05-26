# HBCPC Local Judge

这是一个由 AI 基于 `OJ题目.md` 中的题面反向推导并生成的本地 OJ 评测与验证系统。项目内容包括题面拆分、测试数据、标准解、暴力解、checker/validator/interactor、Subagent 验证报告、Flask Web 评测平台，以及 Windows 单文件 EXE 打包产物。

重要说明：本项目不是官方题库或官方数据包。题解、数据和校验器均由 AI 根据题面理解推导生成，适合用于本地练习、演示、教学和系统验证；若用于正式比赛或严肃评测，请人工复核题意、数据强度、标准答案和 checker。

## 快速使用

### 方式一：直接运行 EXE

双击根目录下的：

```text
HBCPC-OJ.exe
```

程序会启动本地 Web 服务，并自动打开浏览器。若默认端口 `5000` 被占用，会自动尝试 `5001` 至 `5049`。

评测 C++ 提交时，本机仍需要能在命令行访问 `g++`，因为 Web 平台会调用本地 `g++ -std=c++17` 编译用户提交。

### 方式二：使用 Python 启动

在项目根目录运行：

```powershell
python -m pip install -r requirements.txt
$env:FLASK_APP="web.app"
python -m flask run --host 127.0.0.1 --port 5000
```

然后访问：

```text
http://127.0.0.1:5000/
```

Linux/macOS 或 Git Bash 可使用：

```bash
./run.sh
```

### 方式三：重新编译 EXE

修改代码、题面、数据或静态资源后，可重新打包：

```powershell
.\build_exe.ps1
```

也可以双击或运行：

```bat
build_exe.bat
```

脚本会：

1. 安装 `requirements.txt` 中的依赖；
2. 检查并补齐本地 MathJax 静态资源；
3. 停止正在运行的 `HBCPC-OJ.exe`；
4. 使用 PyInstaller 生成单文件 EXE；
5. 将结果复制到根目录 `HBCPC-OJ.exe`。

## Web 平台功能

- 题目列表页：展示 A-M 全部题目、类型和数据组数。
- 题面与提交同页：每道题页面左侧渲染 Markdown 题面，右侧提交 C++17 代码。
- 数学公式渲染：使用本地 MathJax，支持 `$...$`、`$$...$$`、`\(...\)`、`\[...\]`。
- 提交方式：支持上传 `.cpp/.cc/.cxx/.txt` 文件，也支持在线粘贴代码。
- 本地评测：使用 `subprocess` 调用本机 `g++` 编译并逐组运行。
- 限制检测：支持时间限制和基于进程 RSS 的内存限制检测。
- 结果展示：每个数据点显示 AC/WA/TLE/RE/CE、运行时间、实际输出；WA 时显示 diff。

## 根目录文件说明

| 路径 | 说明 |
| --- | --- |
| `OJ题目.md` | 原始题面文件，AI 以此作为输入进行拆题、推导和生成。 |
| `README.md` | 当前说明文件。 |
| `HBCPC-OJ.exe` | 已打包好的 Windows 单文件本地 OJ，可直接双击运行。 |
| `HBCPC-OJ.pid` | 最近一次 EXE 冒烟测试或运行时记录的进程 ID，属于运行状态文件。 |
| `HBCPC-OJ.spec` | PyInstaller 生成的打包规格文件。重新运行 `build_exe.ps1` 时会自动重建。 |
| `build_exe.ps1` | Windows PowerShell 打包脚本，用于重新生成根目录 EXE。 |
| `build_exe.bat` | 对 `build_exe.ps1` 的批处理封装，便于双击或在 cmd 中运行。 |
| `launcher.py` | EXE 的启动入口：选择可用端口、启动 Flask 服务、自动打开浏览器。 |
| `manifest.json` | 题目元信息清单，包括题名、类型、时间限制、内存限制及 checker 路径。 |
| `problem_list.md` | 阶段一产物：题目清单、题目类型和关键约束。 |
| `requirements.txt` | Python 依赖列表，包括 Flask、psutil、Markdown、PyInstaller。 |
| `run.sh` | Bash 一键启动脚本，会创建虚拟环境、安装依赖并启动 Flask。 |
| `subagent_report.md` | 5 个独立 Subagent 的验证汇总报告，包含通过率、失败分类和独立解法路径。 |

## 文件夹说明

### `problems/`

题面目录。

- `problems/OJ题目.md`：原始题面副本。
- `problems/A.md` 至 `problems/M.md`：按题号拆分后的单题 Markdown 题面。

Web 页面会读取这里的 Markdown 并渲染为 HTML，同时由 MathJax 渲染数学公式。

### `data/`

评测数据目录。每题一个子目录：

```text
data/A/
data/B/
...
data/M/
```

每道题包含 25 组数据：

- `01_regular.in` 至 `10_regular.in`：常规数据。
- `11_stress.in` 至 `18_stress.in`：大数据/压力数据。
- `19_edge.in` 至 `25_edge.in`：极端/边界数据。
- 同名 `.ans` 文件：对应标准答案。

### `solutions/`

AI 生成的解法目录。每题一个子目录：

```text
solutions/A/std.cpp
solutions/A/brute.cpp
...
solutions/M/std.cpp
solutions/M/brute.cpp
```

- `std.cpp`：标准解，用于生成 `.ans`。
- `brute.cpp`：暴力解或朴素校验解，用于对拍。

所有 C++ 源码按 C++17 编译。

### `checker/`

非普通判题程序目录。

- `checker/E/validator.cpp`：E 构造题输出合法性验证器。
- `checker/F/interactor.cpp`：F 交互题 interactor。
- `checker/K/validator.cpp`：K 构造题输出合法性验证器。
- `checker/L/checker.cpp`：L 实数误差 Special Judge。
- `checker/M/checker.cpp`：M 多解/构造类 Special Judge。

Web 平台在需要时会编译并调用这些程序。

### `scripts/`

自动化脚本目录。

- `scripts/build_core.py`：核心生成脚本，可按随机种子重新生成题面拆分、解法、数据和答案。
- `scripts/stress_test.py`：标准解与暴力解对拍脚本。
- `scripts/evaluate_subagents.py`：统一评测 Subagent 源码的辅助脚本。
- `scripts/summarize_subagents.py`：生成 `subagent_report.md` 的汇总脚本。

### `subagents/`

5 个独立 Subagent 的工作目录。

- `subagents/agent1/` 至 `subagents/agent5/`：每个 agent 独立生成 A-M 的 C++ 解法和报告。
- 每个目录通常包含 `A.cpp` 至 `M.cpp`、`report.md` 和若干本地编译/运行产物。

这些文件用于阶段四的独立验证，不是 Web 平台运行所必需。

### `web/`

Flask Web 平台源码。

- `web/app.py`：主应用，包含题目展示、Markdown 渲染、提交、编译、运行、判题、结果展示。
- `web/__init__.py`：Python 包标记文件。
- `web/templates/`：Jinja2 模板。
  - `base.html`：全站基础布局，并加载本地 MathJax。
  - `index.html`：题目列表页。
  - `problem.html`：题面与提交同页。
  - `result.html`：评测结果页。
  - `submissions.html`：本地提交记录页。
  - `submit.html`：兼容旧路由的模板占位。
- `web/static/app.css`：页面样式。
- `web/static/mathjax/`：本地 MathJax 静态资源，用于离线渲染数学公式。
- `web/flask.pid`：最近一次开发服务器启动时记录的进程 ID，属于运行状态文件。
- `web/build/`：Web 运行时编译 checker 的缓存目录。
- `web/submissions/`：开发模式下的提交源码、编译产物和输出文件。

### `web_runtime/`

EXE 运行时输出目录。

当通过 `HBCPC-OJ.exe` 启动时，提交记录、编译产物、输出文件和 checker 缓存会写入这里，而不是写入 PyInstaller 的临时解包目录。

### `build/`

编译与验证缓存目录。

可能包含：

- 标准解编译产物；
- checker 编译产物；
- stress test 编译产物；
- PyInstaller 中间文件；
- npm 下载的 MathJax 临时包；
- Subagent 评测输出。

这是构建缓存目录，必要时可以删除；删除后重新运行脚本会再生成。

### `dist/`

PyInstaller 默认输出目录。

- `dist/HBCPC-OJ.exe`：最近一次 PyInstaller 生成的 EXE。

根目录的 `HBCPC-OJ.exe` 是从这里复制出来的最终交付文件。

### `__pycache__/`

Python 字节码缓存目录，可删除。

## 常用命令

### 重新生成核心数据与答案

```powershell
python scripts\build_core.py --seed 20260526
```

该脚本会清理并重建 `problems/`、`data/`、`solutions/`、`checker/` 等核心产物。除非明确需要重置数据，否则不要随意运行。

### 运行对拍

```powershell
python scripts\stress_test.py
```

### 重新生成 Subagent 汇总报告

```powershell
python scripts\summarize_subagents.py
```

### 重新打包 EXE

```powershell
.\build_exe.ps1
```

## 使用注意

1. 评测 C++ 代码需要本机安装 `g++` 并加入 `PATH`。
2. EXE 是单文件封装，但不是远程 OJ；所有编译和运行都在本机完成。
3. 本项目的数据、标准解和 checker 是 AI 依据题面反推生成，不代表官方答案。
4. 若修改 `problems/`、`data/`、`checker/`、`web/` 或 `manifest.json` 后希望 EXE 生效，需要重新运行 `build_exe.ps1`。
5. `build/`、`dist/`、`web_runtime/`、`web/submissions/` 多数是缓存或运行输出；清理前请确认不需要保留历史提交结果。
