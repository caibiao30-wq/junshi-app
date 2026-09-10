# claude-code-infrastructure-showcase 目录框架图

> 只读调研产物 · 候选归纳（非本仓库决策，不自动升级）
> 源：`/Users/caibiao/Downloads/claude-code-infrastructure-showcase-main`（多余作演示的 Claude Code 基础设施展示仓库）
> 原则：仅检查目录/文件名称与必要元信息，深度两层，未读取任何代码正文。
> 职责描述为基于名称的模式归纳，非源码阅读结论；职责不确定项标「待核验」。

源元信息（调研日期 2026-09-04）：类型为目录，顶层 6 个目录 + 6 个文件，修改时间 2026-07-12 10:12:34。

## 顶层项（depth 0）

| 项 | 类型 | 候选归纳职责 | 状态 |
|---|---|---|---|
| `.agents/` | 目录 | 智能体定义区（通用 agent 规范） | 候选归纳 |
| `.claude/` | 目录 | Claude Code 本地配置区（agent/命令/hook/脚本/skill/settings） | 候选归纳 |
| `.codex/` | 目录 | Codex（多智能体）配置区（agent/hook） | 候选归纳 |
| `.env.example` | 文件 | 环境变量模板示例 | 候选归纳 |
| `.gitignore` | 文件 | 仓库忽略规则 | 候选归纳 |
| `CLAUDE_INTEGRATION_GUIDE.md` | 文件 | Claude 集成指引文档 | 候选归纳 |
| `dev/` | 目录 | 开发目录（Dev 子模块，含 README） | 候选归纳 |
| `editor-config/` | 目录 | 编辑器配置（vim/lua 配置与说明） | 候选归纳 |
| `LICENSE` | 文件 | 开源许可 | 候选归纳 |
| `README.md` | 文件 | 仓库说明 | 候选归纳 |
| `setup.ts` | 文件 | TypeScript 设置/初始化脚本 | 候选归纳；具体作用待核验 |

## 二级项（depth 1）

### `.agents/`

| 项 | 类型 | 候选归纳职责 | 状态 |
|---|---|---|---|
| `skills/` | 目录 | 智能体技能包目录 | 候选归纳；内部 skill 未在此层列示 |

### `.claude/`

| 项 | 类型 | 候选归纳职责 | 状态 |
|---|---|---|---|
| `agents/` | 目录 | 子智能体定义 | 候选归纳 |
| `commands/` | 目录 | 斜杠命令/skill 命令 | 候选归纳 |
| `hooks/` | 目录 | hook 脚本目录 | 候选归纳 |
| `scripts/` | 目录 | 辅助脚本目录 | 候选归纳 |
| `settings.json` | 文件 | 会话/权限等本地配置 | 候选归纳 |
| `skills/` | 目录 | 内置技能包目录 | 候选归纳；内部 skill 未在此层列示 |

### `.codex/`

| 项 | 类型 | 候选归纳职责 | 状态 |
|---|---|---|---|
| `agents/` | 目录 | Codex 智能体定义 | 候选归纳 |
| `hooks/` | 目录 | Codex hooks 脚本目录 | 候选归纳 |
| `hooks.json` | 文件 | hooks 配置清单 | 候选归纳 |

### `dev/`

| 项 | 类型 | 候选归纳职责 | 状态 |
|---|---|---|---|
| `README.md` | 文件 | 开发模块说明 | 候选归纳 |

### `editor-config/`

| 项 | 类型 | 候选归纳职责 | 状态 |
|---|---|---|---|
| `init.lua` | 文件 | Neovim 初始化配置（.lua） | 候选归纳 |
| `README.md` | 文件 | 编辑器配置说明 | 候选归纳 |
| `vimrc` | 文件 | Vim 配置 | 候选归纳 |

## 说明与边界

- 本调研仅到两层（depth 0-1）。`.claude/skills/`、`.claude/agents/`、`.agents/skills/`、`.codex/agents/` 等目录的内部项未展开，均标「待核验」或未列示。
- 「候选归纳」表示职责为按命名模式推断，未读代码/文件正文验证；如需用于本仓库（junshi-app）需另行深度核验并走 `mate/` 决议。
- 未修改源仓库任何内容；仅生成本框架图文件。
- 无阻塞：目录可读、源与目标路径均可访问。

## Skill 使用记录

- 阶段：只读本地目录调研（两层）
- 任务类型：写入 Markdown 框架图（非产品正文）
- 能力发现：`md-writing` 为通用 Markdown 撰写专项；本任务产出为结构化只读归类表，非论证性文档
- 选择理由：未调用 `md-writing`，仅以目录列示 + Write 完成最小产出，避免引入冗余流程。此为记录用途，非运行强制。
- 实际调用：Bash（`find -maxdepth 2`）、`stat`；结果如上述各层清单
- 输入：`/Users/caibiao/Downloads/claude-code-infrastructure-showcase-main`
- 输出：`/Users/caibiao/orca/projects/junshi-app/工程代码库目录框架图/claude-code-infrastructure-showcase目录框架图.md`
- 未调用项：`agent-reach`/`research`（本任务明确禁止联网）；`md-writing`（只读结构化产出，理由如上）
- 阻塞：无
- 验证：源目录可读、目标文件已写入（此前不存在）

## 回报

顶层项（depth-0）：`.agents/`、`.claude/`、`.codex/`、`.env.example`、`.gitignore`、`CLAUDE_INTEGRATION_GUIDE.md`、`dev/`、`editor-config/`、`LICENSE`、`README.md`、`setup.ts`（6 目录 + 6 文件）。
阻塞：无。全部为只读目录/文件名核验，未读任何代码正文、未联网、未改源仓库与 context.md/mate/STRUCTURE。