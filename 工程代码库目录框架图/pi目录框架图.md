# pi 工程代码库目录框架图

> 状态标注：**候选归纳**（基于目录命名与 monorepo 通用惯例归纳，未读取代码正文，未联网核验）。
> 本图仅为只读勘察产物，不升级为产品决策或通用模板。凡职责无法由命名/惯例确认者，均标注 **待核验**。
> 数据来源：`/Users/caibiao/Downloads/pi-main`（本地一手解压仓库，maxdepth=2，排除 .git 内容）。

## 顶层结构

```
pi-main/
├── packages/            → 职责：npm workspaces 核心分包集合（产品功能按职责拆分的主战场）
├── scripts/             → 职责：构建、发布、冒烟测试、发布工程与统计类脚本
├── .github/             → 职责：CI 工作流与社区治理（issue 模板、批准贡献者、ci/pr 门禁）
├── .pi/                 → 职责：本产品自身的运行时配置目录（扩展、提示词、技能、git/npm 忽略）
├── .husky/              → 职责：git 提交钩子（pre-commit）
├── package.json         → 职责：monorepo 工作区定义与顶层依赖/脚本入口
├── package-lock.json    → 职责：依赖锁定文件
├── tsconfig.json        → 职责：TypeScript 顶层编译配置
├── tsconfig.base.json   → 职责：TypeScript 基础共享编译配置
├── vitest.base.ts       → 职责：vitest 顶层共享测试配置
├── biome.json           → 职责：代码格式化与 lint（biome）配置
├── README.md            → 职责：项目说明与使用文档
├── AGENTS.md            → 职责：多智能体协作说明（面向 agent 的项目指引）
├── CONTRIBUTING.md      → 职责：贡献指南
├── SECURITY.md          → 职责：安全策略与报告流程
├── LICENSE              → 职责：许可证
├── tui-plan.md          → 职责：TUI 终端界面规划文档
├── mini-test.sh         → 职责：轻量测试运行脚本
├── test.sh              → 职责：测试运行脚本
├── pi-test.sh           → 职责：跨平台测试脚本（POSIX）
├── pi-test.ps1          → 职责：跨平台测试脚本（PowerShell/Windows）
├── pi-test.bat          → 职责：跨平台测试脚本（Windows 批处理）
├── .gitignore           → 职责：git 忽略规则
├── .gitattributes       → 职责：git 属性（换行/差异等）
└── .npmrc               → 职责：npm 源与 registry 配置
```

## 第二层（职责相关的主要子目录）

```
packages/                        → npm workspaces 各功能分包
├── agent/                       → 职责：智能体核心实现（src/docs/test/benchmark）
│   ├── src/                     → 职责：核心源码
│   ├── test/                    → 职责：单元/集成测试
│   ├── docs/                    → 职责：文档
│   ├── benchmark/               → 职责：基准测试
│   └── scripts/                 → 职责：分包内脚本
├── ai/                          → 职责：AI/LLM 提供者封装（含 bedrock-provider 声明/实现）
│   ├── src/                     → 职责：核心源码
│   ├── test/                    → 职责：测试
│   └── scripts/                 → 职责：分包内脚本
├── chord/                       → 职责：待核验（命名不明；有 src/test/PLANNING.md）
│   ├── src/                     → 职责：核心源码
│   └── test/                    → 职责：测试
├── client/                      → 职责：客户端库/API
│   ├── src/                     → 职责：核心源码
│   └── test/                    → 职责：测试
├── coding-agent/                → 职责：编码智能体（独立分发/打包，含 install-lock 与 shrinkwrap）
│   ├── src/                     → 职责：核心源码
│   ├── test/                    → 职责：测试
│   ├── docs/                    → 职责：文档
│   ├── examples/                → 职责：示例
│   ├── install-lock/            → 职责：安装锁文件
│   └── scripts/                 → 职责：分包内脚本
├── evals/                       → 职责：评测/评估框架
│   ├── src/                     → 职责：核心源码
│   ├── test/                    → 职责：测试
│   └── scripts/                 → 职责：分包内脚本
├── protocol/                    → 职责：通信协议定义
│   ├── src/                     → 职责：核心源码
│   └── test/                    → 职责：测试
├── server/                      → 职责：服务端实现
│   ├── src/                     → 职责：核心源码
│   └── test/                    → 职责：测试
├── session-backends/            → 职责：会话存储后端
│   └── sqlite-node/             → 职责：SQLite 节点会话存储后端（待核验层级，maxdepth=2 显示）
├── telemetry/                   → 职责：遥测/指标采集
│   ├── src/                     → 职责：核心源码
│   └── test/                    → 职责：测试
└── tui/                         → 职责：终端用户界面（含 native 部分）
    ├── src/                     → 职责：核心源码
    ├── test/                    → 职责：测试
    └── native/                  → 职责：原生模块/绑定（待核验）

scripts/                         → 工程脚本（按职责分组，未逐一展开全部脚本）
├── build-* / release-* / publish-* / sync-versions / local-release / package-workspaces
│                                → 职责：构建、发布、版本同步、工作区打包
├── *-smoke-entry.ts / check-*-smoke.mjs / mini-test / repro-*.mjs
│                                → 职责：冒烟测试与问题复现脚本
├── check-*.mjs（entry-graphs/lockfile-commit/pinned-deps/ts-relative-imports）
│                                → 职责：工程健康与一致性检查
├── generate-*.mjs / diff-model-catalog.mjs / publish-model-catalog.mjs
│                                → 职责：生成类脚本与模型目录发布
├── read/edit-tool-stats.mjs / tool-stats.ts / cost.ts / stats.ts / session-context-stats.mjs
│                                → 职责：工具/成本/会话上下文统计
├── profile-coding-agent-node.mjs / agent-treeshake-smoke-entry.ts
│                                → 职责：编码智能体性能剖析与 tree-shake 冒烟
└── auto-pi.sh / create-source-archive.sh / update-source-imports-to-ts.sh
    → 职责：自动化与源码归档/导入迁移脚本

.github/                        → CI 与社区治理
├── workflows/                  → 职责：CI/CD 工作流（ci、pr-gate、build-binaries、npm-audit、publish-model-catalog、issue-* 等）
├── ISSUE_TEMPLATE/             → 职责：issue 模板（bug/contribution/package-report/config）
└── APPROVED_CONTRIBUTORS       → 职责：已批准贡献者清单

.pi/                            → 本产品运行时配置目录
├── extensions/                 → 职责：运行时扩展（tps、redraws、prompt-url-widget、import-repro）
├── prompts/                    → 职责：命令/提示词文件（cl、pr、sa、wr、is、deslop 等）
├── skills/                     → 职责：技能定义（add-llm-provider.md）
├── git/                        → 职责：git 相关运行时数据（.gitignore，内容未读）
└── npm/                        → 职责：npm 相关运行时数据（.gitignore，内容未读）
```

## 覆盖范围与未决说明

- 已覆盖顶层项：`packages`、`scripts`、`.github`、`.pi`、`.husky`、`package*.json`、`tsconfig*`、`vitest.base.ts`、`biome.json`、`README`、`AGENTS`、`CONTRIBUTING`、`SECURITY`、`LICENSE`、`tui-plan.md`、各类测试脚本（`mini-test.sh`/`test.sh`/`pi-test.*`）、工程配置文件（`.gitignore`/`.gitattributes`/`.npmrc`）。
- 待核验项：
  - `packages/chord`：命名含义不明，职责待核验。
  - `packages/session-backends/sqlite-node`：仅显示为 sqlite-node 一层，未确认其为目录含子层，故按目录列出、职责待核验。
  - `packages/tui/native`：原生模块具体作用待核验。
  - `.pi/git` 与 `.pi/npm`：因规则只读且深度受限，仅见含 `.gitignore`，其具体承载职责待核验。
  - `scripts/` 下全部脚本为按命名归组归纳，未逐一读正文，具体行为以命名推断，个别（如 `repro-5893-wsl-bash`）仅能从文件名推测为问题复现脚本。
- 未深入第三层，未读取任何源码正文，未联网。
