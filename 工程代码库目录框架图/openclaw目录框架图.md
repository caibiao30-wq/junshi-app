# openclaw-main 目录框架图

- 定位：OpenClaw（TypeScript）多智能体运行时源码仓库，顶层为主源码/包/插件/技能/测试的一体化 monorepo。
- 状态：候选归纳（仅两层目录布局，未读代码正文，未联网，未修改源仓库）。
- 来源：本机 `/Users/caibiao/Downloads/openclaw-main`，实际访问日期 2026-09-04。
- 范围：顶层目录 + 主要职责相关子目录一层；`src/*` 深层仅抽样 `src/agents` 以辅助职责判断，不构成源码研究。

> 说明：本次为本地只读目录调研，字段协议参考 `.claude/commands/research-evidence.md`（该命令文件在仓库中未找到，见文末阻塞项）。每条职责为「候选归纳」，不确定项标「待核验」。

## 顶层布局

| 顶层项 | 类型 | 职责（候选归纳） |
|---|---|---|
| `src/` | 目录 | 主源码：agent 运行时、多渠道收发、CLI、网关、LLM 层等核心实现 |
| `packages/` | 目录 | 共享包库（agent-core、gateway-protocol、plugin-sdk、sdk 等），被核心与插件引用 |
| `apps/` | 目录 | 多平台客户端：android/ios/linux/macos/mobile/shared/swabble |
| `extensions/` | 目录 | 插件集成（模型供应商、渠道、工具等），数量最多 |
| `skills/` | 目录 | 技能/工具定义集合（1password、github、notion、whisper 等） |
| `scripts/` | 目录 | 开发/构建/发布/基准测试脚本 |
| `test/` | 目录 | 测试套件（单元/e2e/integration） |
| `docs/` | 目录 | 文档集（架构、渠道、插件、供应商、安全等） |
| `config/` | 目录 | 构建/CI/lint 配置（oxlint、tsconfig、knip 等） |
| `ui/` | 目录 | 前端界面（Vite 应用 + 独立 package 结构） |
| `qa/` | 目录 | 质量评估（maturity 评分、scenarios） |
| `security/` | 目录 | 安全扫描配置（opengrep） |
| `deploy/` | 目录 | 部署配置（fly.private.toml） |
| `examples/` | 目录 | 示例（ai-chat） |
| `custodian-skills/` | 目录 | 维护类技能（职责待核验） |
| `.github/` | 目录 | CI/工作流 |
| `.agents/`、`.claude/`、`.vscode/` | 目录 | 编辑器/agent 配置 |
| 根文件 | 文件 | `openclaw.mjs`（入口）、`AGENTS.md`/`CLAUDE.md`、`package.json`、`pnpm-workspace.yaml`、`Dockerfile`、`docker-compose.yml`、`README.md`、`CHANGELOG.md`、`appcast.xml`、`taxonomy.yaml` 等 |
| `.crabbox.yaml`、`fly.toml`、`render.yaml` | 文件 | 部署/配置 |

## 核心子目录：src/

| 子项 | 职责（候选归纳） |
|---|---|
| `agents/` | agent 运行时、认证、MCP 捆绑与生命周期（抽样确认） |
| `channels/` | 多渠道收发（WhatsApp/Telegram 等） |
| `cli/`、`commands/`、`tui/` | 命令行与终端交互 |
| `gateway/` | 网关/会话管理 |
| `llm/`、`provider-runtime/` | LLM 调用与供应商运行时 |
| `fleet/`、`worker/` | 多 worker/fleet 编排 |
| `flows/`、`tasks/`、`cron/` | 工作流、任务、定时任务 |
| `sessions/`、`state/`、`secrets/`、`security/` | 会话、状态、密钥、安全 |
| `context-engine/`、`memory`（待核验） | 上下文/记忆引擎 |
| `web/`、`web-fetch/`、`web-search/` | 网络能力 |
| `skills/`、`tools/` | 技能与工具运行时 |
| `tts/`、`image-generation/`、`video-generation/` | 媒体生成 |
| `daemon/`、`bootstrap/`、`infra/` | 守护进程/启动/基础设施 |
| `acp/`、`compat/`、`projects/`、`system-agent/` | ACP 协议、兼容、项目、系统 agent（职责部分待核验） |
| `shared/`、`types/`、`utils/`、`logger*` | 公共类型/工具/日志 |

## 核心子目录：packages/

- 能力分层：`agent-core`、`llm-core`、`ai`、`sdk`、`plugin-sdk`、`plugin-package-contract`、`gateway-protocol`、`gateway-client`、`memory-host-sdk`、`media-*`、`markdown-core`、`normalization-core`、`terminal-core`、`net-policy`、`tool-call-repair`、`retry`、`session-url-contract`、`workboard-contract`、`model-catalog-core`、`mermaid-renderer` 等。
- 职责：被 `src/` 与 `extensions/` 复用的核心/契约/客户端库（候选归纳）。

## 核心子目录：apps/

| 子项 | 职责（候选归纳） |
|---|---|
| `android/`、`ios/` | 移动端应用 |
| `linux/`、`macos/`、`macos-mlx-tts/` | 桌面端应用/语音 |
| `mobile/` | 移动端（与 android/ios 关系待核验） |
| `shared/` | 各平台共享代码 |
| `swabble/` | 独立应用（职责待核验） |

## 核心子目录：extensions/（抽样）

- 模型/供应商：`anthropic`、`anthropic-vertex`、`openai`（待核验）、`deepseek`、`cohere`、`amazon-bedrock`、`google`、`gemini`（待核验）、`fireworks`、`baseten`、`cerebras`、`chutes`、`deepinfra` 等。
- 渠道：`discord`、`googlechat`、`feishu`、`duckduckgo`、`github-copilot` 等。
- 能力：`browser`、`cua-computer`、`canvas`、`document-extract`、`firecrawl`、`deepgram`、`elevenlabs`、`device-pair`、`active-memory` 等。
- 运维：`admin-http-rpc`、`diagnostics-otel`、`diagnostics-prometheus` 等。

## 核心子目录：skills/（抽样）

- 工具类：`1password`、`apple-notes`、`notion`、`obsidian`、`trello`、`things-mac`、`github`、`gh-issues`、`weather`。
- 媒体：`openai-whisper`、`sherpa-onnx-tts`、`spotify-player`、`meme-maker`、`diagram-maker`、`video-frames`。
- 集成/自动化：`coding-agent`、`clawhub`、`control-ui`、`taskflow`、`summarize`、`tmux`、`model-usage`。

## 不确定项（待核验）

1. `custodian-skills/`、`.agents/` 具体职责未确认。
2. `apps/mobile` 与 `apps/android`、`apps/ios` 的从属/共享关系需读代码确认。
3. `extensions/` 完整 165 项清单与各自职责未逐一核对；`openai`、`gemini` 等目录是否存在未在抽样中确认。
4. `src/` 深层（如 `memory`、`acp`、`projects`）职责为推断，未读源码验证。
5. `taxonomy.yaml`、`appcast.xml` 等根文件具体作用未确认。
6. 各包/目录依赖与构建关系（pnpm workspace）未展开。

## 风险与说明

- 本图为「候选归纳」：仅基于目录名与文件类型推断，未读代码正文，不构成产品决策或工程实现判断。
- 不联网、未修改源仓库 `/Users/caibiao/Downloads/openclaw-main`。
- 不执行仓库内任何脚本或配置。

## 阻塞与验证

- 阻塞：`.claude/commands/research-evidence.md` 命令文件在 junshi-app 仓库未找到，G1-G5 字段协议与证据表字段无法按原文引用；本次以本地目录元数据 + 候选归纳 + 待核验标注替代。
- 验证：`ls` 目录列表已完成（顶层 + 各主要子目录一层）；未读取任何代码正文、未联网。
- 下一步：如需更精确职责，需授权后按需抽样 `src/`、`extensions/`、`apps/` 的 README/入口文件；或由用户指定是否将本图纳入工程代码库目录框架的正式参照。
