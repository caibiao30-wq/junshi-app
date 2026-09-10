# codex 工程代码库目录框架图

> **产出属性：候选归纳**
>
> **范围与方法：** 以 `/Users/caibiao/Downloads/codex-main` 的实际目录项为唯一来源；仅列出顶层与第二层职责相关的主要目录/文件，不读取代码正文，不联网。职责说明依据目录名、文件名及仓库布局作保守归纳；无法从目录布局确认的内容标注为“待核验”。

## 顶层结构

├── `.codex/`   → 职责：仓库本地 Codex 工作区配置与技能资源。
├── `.devcontainer/`   → 职责：开发容器环境配置。
├── `.github/`   → 职责：GitHub 协作、自动化工作流、维护脚本与仓库元配置。
├── `.vscode/`   → 职责：Visual Studio Code 编辑器工作区配置。
├── `bazel/`   → 职责：Bazel 构建系统的扩展、规则、平台、模块与工具链配置。
├── `codex-cli/`   → 职责：Codex 命令行分发包及其启动脚本。
├── `codex-rs/`   → 职责：Codex 核心 Rust 工程及按运行能力拆分的工作区 crate。
├── `docs/`   → 职责：用户、开发者、配置、执行策略与项目贡献文档。
├── `patches/`   → 职责：第三方依赖或构建过程所需的补丁文件。
├── `scripts/`   → 职责：构建、打包、安装、格式检查、测试与本地运行辅助脚本。
├── `sdk/`   → 职责：面向外部集成的 Python、Python runtime 与 TypeScript SDK。
├── `third_party/`   → 职责：第三方组件、平台适配或外部运行时相关资产。
├── `tools/`   → 职责：仓库构建与代码质量辅助工具。
├── `AGENTS.md`   → 职责：Agent 协作与仓库操作说明。
├── `BUILD.bazel`   → 职责：仓库顶层 Bazel 构建声明。
├── `MODULE.bazel` / `MODULE.bazel.lock`   → 职责：Bazel 模块依赖声明与锁定状态。
├── `Cargo.toml`（位于 `codex-rs/`）   → 职责：Rust 工作区依赖与构建元数据；顶层无同名文件，归属见 `codex-rs/`。
├── `package.json`   → 职责：JavaScript/TypeScript 工作区及包级元数据。
├── `pnpm-workspace.yaml` / `pnpm-lock.yaml`   → 职责：pnpm 工作区边界与 JavaScript 依赖锁定。
├── `flake.nix` / `flake.lock`   → 职责：Nix 开发或构建环境声明与锁定状态。
├── `justfile`   → 职责：常用开发、构建和检查命令编排。
├── `README.md`   → 职责：仓库入口说明与使用导航。
├── `CHANGELOG.md`   → 职责：版本变更记录。
├── `LICENSE` / `NOTICE`   → 职责：许可证与第三方声明。
├── `SECURITY.md`   → 职责：安全问题报告与处理说明。
├── `defs.bzl` / `rbe.bzl`   → 职责：Bazel 构建宏、共享定义或远程构建配置；具体职责待核验。
├── `workspace_root_test_launcher.sh.tpl` / `.bat.tpl`   → 职责：工作区根目录测试启动器模板。
└── 其他点文件（`.bazelrc`、`.bazelversion`、`.gitignore`、格式/拼写检查配置等）   → 职责：构建、版本控制与代码风格工具的仓库级配置。

## 第二层（职责相关的主要子目录）

├── `.codex/`
│   ├── `environments/`   → 职责：仓库本地运行环境定义。
│   └── `skills/`   → 职责：仓库本地 Agent 技能资源。
│
├── `.github/`
│   ├── `actions/`   → 职责：GitHub Actions 可复用动作。
│   ├── `codex/`   → 职责：GitHub 上 Codex 专属协作或自动化配置；具体职责待核验。
│   ├── `ISSUE_TEMPLATE/`   → 职责：Issue 提交模板。
│   ├── `scripts/`   → 职责：GitHub 协作流程辅助脚本。
│   └── `workflows/`   → 职责：持续集成、检查、发布等 GitHub Actions 工作流。
│
├── `bazel/`
│   ├── `extensions/`   → 职责：Bazel 扩展定义。
│   ├── `modules/`   → 职责：Bazel 模块相关配置。
│   ├── `platforms/`   → 职责：构建平台声明。
│   ├── `rules/`   → 职责：仓库自定义构建规则。
│   ├── `schema/`   → 职责：Bazel 构建数据或规则 schema；具体内容待核验。
│   └── `toolchains/`   → 职责：编译与构建工具链配置。
│
├── `codex-cli/`
│   ├── `bin/`   → 职责：命令行入口可执行脚本。
│   ├── `scripts/`   → 职责：CLI 包构建、发布或安装辅助脚本。
│   └── `package.json`   → 职责：CLI npm 包元数据与脚本声明。
│
├── `codex-rs/`
│   ├── `cli/`   → 职责：Rust CLI 交互层与命令行编排。
│   ├── `core/`   → 职责：Codex 核心 Agent 运行逻辑；内部职责边界待核验。
│   ├── `protocol/`   → 职责：核心协议类型或消息定义。
│   ├── `app-server/`、`app-server-client/`、`app-server-daemon/`   → 职责：应用服务端、客户端与守护进程组件。
│   ├── `app-server-protocol/`、`app-server-transport/`   → 职责：应用服务协议与传输层。
│   ├── `backend-client/`、`codex-client/`   → 职责：后端或 Codex 服务客户端连接能力。
│   ├── `codex-api/`、`codex-backend-openapi-models/`   → 职责：API 接口与 OpenAPI 模型。
│   ├── `config/`、`config-schema/`   → 职责：运行配置处理与配置 schema。
│   ├── `exec/`、`exec-server/`、`exec-server-protocol/`   → 职责：命令执行、执行服务及其协议。
│   ├── `sandboxing/`、`bwrap/`、`linux-sandbox/`、`windows-sandbox-rs/`、`windows-sandbox-service/`   → 职责：跨平台沙箱与隔离执行。
│   ├── `execpolicy/`、`shell-command/`、`shell-escalation/`   → 职责：执行策略、Shell 命令及权限升级控制。
│   ├── `apply-patch/`、`file-system/`、`file-search/`、`file-watcher/`、`git-utils/`、`worktree/`   → 职责：代码修改、文件访问、搜索、监视、Git 与工作树操作。
│   ├── `mcp-server/`、`codex-mcp/`、`rmcp-client/`   → 职责：MCP 服务端、MCP 集成与客户端能力。
│   ├── `tools/`、`core-plugins/`、`plugin/`、`skills/`   → 职责：工具、插件与技能扩展机制。
│   ├── `agent-graph-store/`、`agent-identity/`、`agent-roles/`、`collaboration-mode-templates/`   → 职责：Agent 图存储、身份、角色与协作模式资源。
│   ├── `context-fragments/`、`prompts/`、`guardian-context/`   → 职责：上下文片段、提示资源与安全上下文。
│   ├── `history/`、`message-history/`、`rollout/`、`rollout-trace/`、`thread-manager-sample/`、`thread-store/`   → 职责：会话、消息、线程与运行轨迹状态管理。
│   ├── `login/`、`secrets/`、`keyring-store/`、`aws-auth/`、`workload-identity/`   → 职责：登录、密钥、凭据及身份认证集成。
│   ├── `model-provider/`、`model-provider-info/`、`models-manager/`、`cloud-config/`、`cloud-tasks/`   → 职责：模型提供方、模型管理与云端任务配置/客户端。
│   ├── `analytics/`、`diagnostics/`、`feedback/`、`otel/`、`otel-trace-websocket/`、`response-debug-context/`   → 职责：分析、诊断、反馈、可观测性与调试信息。
│   ├── `tui/`、`terminal-detection/`、`ansi-escape/`、`voice-host/`、`realtime-webrtc/`   → 职责：终端用户界面、终端适配及语音/实时交互支持。
│   ├── `connectors/`、`http-client/`、`network-proxy/`、`websocket-client/`   → 职责：外部连接、HTTP/WebSocket 通信与网络代理。
│   ├── `attachments-store/`、`memories/`、`state/`、`install-context/`、`codex-home/`   → 职责：附件、记忆、持久状态、安装上下文与用户目录支持；目录名职责以命名归纳，部分待核验。
│   ├── `async-utils/`、`build-info/`、`http-client/`、`utils/`   → 职责：共享异步、构建信息、HTTP 与通用工具能力。
│   ├── `vendor/`、`ext/`   → 职责：供应商代码及外部扩展；具体纳入边界待核验。
│   └── `Cargo.toml`、`Cargo.lock`、`BUILD.bazel`   → 职责：Rust 工作区依赖锁定与 Bazel 构建入口。
│
├── `sdk/`
│   ├── `python/`   → 职责：Python SDK。
│   ├── `python-runtime/`   → 职责：Python SDK 运行时支持。
│   └── `typescript/`   → 职责：TypeScript SDK。
│
├── `docs/`
│   ├── `getting-started.md`、`install.md`   → 职责：入门与安装说明。
│   ├── `authentication.md`、`config.md`、`example-config.md`   → 职责：认证与配置说明及示例。
│   ├── `exec.md`、`execpolicy.md`、`sandbox.md`、`skills.md`、`slash_commands.md`   → 职责：执行、隔离、技能与命令功能说明。
│   ├── `agents_md.md`、`contributing.md`、`CLA.md`   → 职责：Agent 指引、贡献流程与贡献者协议。
│   └── `license.md`、`open-source-fund.md`   → 职责：许可证与开源基金说明。
│
├── `scripts/`
│   ├── `codex_package/`   → 职责：Codex 包构建或组装流程。
│   ├── `install/`   → 职责：安装流程辅助资源。
│   ├── `mcp_conformance/`   → 职责：MCP 一致性验证辅助资源。
│   ├── `build_codex_package.py`、`stage_npm_packages.py`   → 职责：Codex 与 npm 包构建/暂存。
│   ├── `format.py`、`asciicheck.py`、`check_blob_size.py`   → 职责：格式、字符集与文件大小检查。
│   ├── `list-bazel-*.sh`、`check-module-bazel-lock.sh`   → 职责：Bazel 目标枚举与模块锁定检查。
│   ├── `debug-codex.sh`、`run_tui_with_exec_server.sh`、`start-codex-exec.sh`   → 职责：本地调试与启动执行服务。
│   └── `mock_responses_websocket_server.py`、`test-remote-env.sh`   → 职责：测试用模拟 WebSocket 服务与远程环境验证。
│
├── `third_party/`
│   ├── `powershell/`   → 职责：PowerShell 相关第三方适配资产。
│   ├── `v8/`   → 职责：V8 运行时相关第三方资产。
│   ├── `voice/`   → 职责：语音能力相关第三方资产。
│   ├── `wezterm/`   → 职责：WezTerm 终端相关第三方资产。
│   └── `wine/`   → 职责：Wine 兼容层相关第三方资产。
│
└── `tools/`
    ├── `argument-comment-lint/`   → 职责：参数注释代码质量检查工具。
    └── `buildifier/`   → 职责：Bazel 文件格式化与检查工具。

## 待核验与边界说明

- `codex-rs/` 下包含大量按能力拆分的 Rust crate；上图只纳入可由名称直接判断、且对工程职责划分有代表性的主要项，未逐项罗列全部 crate。
- 目录名无法单独确认内部实现边界的项（例如 `.github/codex/`、`codex-rs/ext/`、`codex-rs/schema/` 等）已明确标注“待核验”。
- 顶层配置文件的具体字段语义未通过代码或配置正文核实，故仅按文件名与标准工程约定作候选归纳。
