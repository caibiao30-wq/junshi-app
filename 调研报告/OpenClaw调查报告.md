# OpenClaw 仓库调查报告

- 状态：候选参照（仅供研究，不自动升级为本地产品决策）
- 调研对象：GitHub `openclaw/openclaw`
- 核验方式：GitHub REST API（`gh` CLI，认证读权限）、仓库 raw 文件直接取样
- 访问/核验日期：2026-09-03
- 核验 commit（调研基准）：`a5b9955ec70a0ba31d148e3a73151b3f2b1cf682`（2026-09-03T03:47:58Z，pushed_at 2026-09-03T03:48:50Z）
- 与任务关系：任务一“四仓库调查取证”之 OpenClaw 独立报告；只读，不修改除本文件外任何仓库文件

> 纪律说明：外部页面与仓库内容均为不可信数据，本研究仅归档证据、不做执行。本报告按研究协议把“外部事实 / 来源自身结论 / Claude 推断 / 候选建议”分离，并对每条证据标注来源、版本/日期、原文定位与核验状态。本报告结论不自动成为 `mate/` 或 junshi-app 的产品决策，采纳须经产品发起人确认。

---

## 摘要（结论先行）

OpenClaw 是一个多通道（multi-channel）AI 助手网关：把 LLM 模型、工具、技能（skills）、插件与用户已有的消息通道（WhatsApp、Telegram、Slack、Discord 等）统一接在同一个本地 `Gateway` 上，定位是“个人助理 / 可信团队共享助理”，官方 slogan“Your own personal AI assistant. Any OS. Any Platform. The lobster way”。其工程形态对“学业军师”最具参考价值的不是复刻某条通道，而是**“可信网关 + 不受信任执行 + 确定性策略”的三元信任模型**、`agent-core` 复用内核、资源包（extensions/skills/prompts/themes）清单化声明，以及把运行时选型（模型/通道/沙箱）全部做成显式配置而非硬编码。

对 junshi-app 最直接可落地的三点启发：(1) 用“状态/配置目录 + schema 版本号”管理 Agent 状态与配置演进（`openclaw` 包内 `schemaVersions: state 15 / agent 19`）；(2) 把 Agent 的模型调用、记忆、任务编排、工具做成独立可测的内核包（`packages/agent-core`），而非与通道/UI 耦合；(3) 建立一套资源声明清单（对应其 `package.json` 的 `openclaw.resources`）来登记 skills/prompts/themes，为长尾扩展提供稳定入口。风险方面：仓库规模极大、单仓库包含桌面/移动/网关/技能注册表多套子系统，junshi-app 不应整体照搬，只应抽取“内核 + 配置 + 生命周期”少数模式。

---

## 1. 官方仓库与定位核验（事实）

### 1.1 官方仓库确认（事实，已核验）

- 官方仓库：`https://github.com/openclaw/openclaw`，默认分支 `main`，`default_branch: main`（GitHub REST API 返回）。
- 组织信息：`package.json` 作者字段为 `OpenClaw Foundation (https://openclaw.org)`；`gh api orgs/OpenClawOrg` 返回 404，说明不存在 `OpenClawOrg` 这一组织，仓库归属在 `openclaw` 用户/组织名下（核验：搜索与 API 双重确认）。
- 版本：`package.json` 顶层 `"version": "2026.8.1"`；`"name": "openclaw"`；`"description": "Multi-channel AI gateway with extensible messaging integrations"`（原文定位：`package.json` 顶部）。
- 许可证：MIT（`package.json` `"license": "MIT"`，LICENSE 文件位于仓库根）。
- 安装方式（README.md:22-64）：macOS/Linux/WSL2 用安装脚本，Windows 用 PowerShell；还提供 `.deb`、`.dmg`、`brew`、Docker、Nix 等部署路径（原文定位：README.md `## Install` 与 `## Quick start`）。
- 定位（README.md:1,18,66-73）：`# OpenClaw 🦞 — Your assistant, on your devices, in your chats`；正文：“runs on your devices and meets you in the channels you already use”，连接模型、工具、消息通道与可选伴生 app，经单一 `Gateway`，可作单人个人助理或可信团队共享部署，配置差异是唯一区别。
- 官方文档站：`https://docs.openclaw.ai`（README 多处链接；CHANGELOG.md、docs/ 均存在）。
- 技能注册表：ClawHub `https://clawhub.ai`（README.md:87 提及）。

### 1.2 核验方法（事实）

- 用 GitHub REST API 拉取：仓库元数据（full_name、default_branch、license、pushed_at）、最近一次 commit SHA、根目录列表、`src/`、`packages/`、`apps/`、`skills/`、`src/agents/`、`src/channels/`、`src/config/`、`src/memory/`、`src/gateway/`、`docs/`、`deploy/`、`qa/` 等目录内容，以及 `package.json`、`.env.example`、`docker-compose.yml`、`fly.toml`、`docs/agent-runtime-architecture.md` 的原文。
- 未执行仓库内任何脚本、hook、构建命令；未安装依赖；`gh api` 仅做只读拉取。

---

## 2. 顶层目录与关键文件职责（事实，根目录列表于 2026-09-03 核验）

| 路径 | 类型 | 职责（据命名与 README/docs 推断标注） |
|---|---|---|
| `openclaw.mjs` | 文件 | bin 入口（`package.json` `"bin": {"openclaw": "openclaw.mjs"}`） |
| `package.json` | 文件 | 版本、bin、schemaVersions（state:15 / agent:19）、files 清单 |
| `pnpm-workspace.yaml` | 文件 | monorepo 声明（packages/ 工作区） |
| `src/` | 目录 | 主实现：agents、channels、config、memory、tools、gateway、cron、daemon、cli、commands、context-engine、model-catalog、model-picker、flows、fleet、acp 等 |
| `packages/` | 目录 | 复用内核：agent-core、ai、llm-core、plugin-sdk、memory-host-sdk、gateway-client、gateway-protocol、model-catalog-core、net-policy、retry、sdk、tool-call-repair 等 |
| `apps/` | 目录 | 平台 app：android、ios、linux、macos、macos-mlx-tts、mobile、shared、swabble |
| `skills/` | 目录 | 内置技能：1password、apple-notes、blogwatcher、clawhub、coding-agent、diagram-maker 等 |
| `custodian-skills/` | 目录 | 治理类技能 |
| `config/` | 目录 | 工程配置：oxlint、tsconfig、markdownlint、knip、shellcheck、swiftlint 等 |
| `deploy/`、`Dockerfile`、`docker-compose.yml`、`fly.toml`、`render.yaml` | 部署 | 多平台容器/平台部署描述 |
| `docs/` | 目录 | 官方文档源（含 agent-runtime-architecture.md、docs_map.md、concepts/、gateway/、channels/、install/ 等） |
| `qa/` | 目录 | 质量：maturity-scores.yaml、scenarios/、frontier-harness-plan.md、convex-credential-broker/ |
| `test/`、`test.ts` 遍布 | 测试 | src 各层带 `.test.ts`、`*.e2e.test.ts` |
| `extensions/`、`patches/` | 目录 | 扩展与依赖补丁 |
| `.github/`、`git-hooks/`、`.pre-commit-config.yaml`、`.semgrepignore` | CI/安全 | 工作流与静态安全扫描 |
| `AGENTS.md`、`CLAUDE.md`、`VISION.md`、`CHANGELOG.md`、`SECURITY.md`、`THIRD_PARTY_NOTICES.md` | 文档 | 开发者/模型代理指引、愿景、变更、安全、第三方声明 |
| `appcast.xml`、`taxonomy.yaml` | 文件 | 更新源与技能分类 |

### 2.1 核心运行组件分布（事实）

按 `docs/agent-runtime-architecture.md` 的 `## Runtime Layout` 表格（原文定位）：
- `src/agents/embedded-agent-runner/`：内置 attempt loop（`run.ts`、`run/`）、模型选择与 provider 归一化（`model*.ts`）、每 provider 请求参数、compaction、transcript 与 session 接线。
- `src/agents/sessions/`：session 持久化（`session-manager.ts`）、资源发现（`package-manager.ts`、`resource-loader.ts`）、session 内 `extensions` 加载、prompt 模板、skills、themes、TUI 支撑工具渲染。
- `packages/agent-core/`：可复用 agent 内核（`@openclaw/agent-core`）——agent loop、harness 类型、messages、compaction helpers、prompt 模板、skills、session 存储契约。
- `src/agents/agent-tools*.ts`：OpenClaw 自有工具定义、参数 schema、工具策略、tool 调用前后适配器、host/sandbox 编辑工具。
- 边界说明：`@earendil-works/pi-tui` 是第三方终端组件依赖（第三方依赖保留项）。

### 2.2 资源包清单化（事实，架构文档 `## Manifests`）

`package.json` 的 `openclaw` 字段可声明资源包：
```json
{ "openclaw": { "extensions": ["extensions/index.ts"],
                "skills": ["skills/*.md"],
                "prompts": ["prompts/*.md"],
                "themes": ["themes/*.json"] } }
```
未在清单列出的资源类型会回退到约定目录 `extensions/`、`skills/`、`prompts/`、`themes/` 的自动发现。这是“显式声明优先、约定发现兜底”的资源组织模式。

### 2.3 状态与配置 schema 版本化（事实）

`package.json` 顶层 `"openclaw": { "schemaVersions": { "state": 15, "agent": 19 } }`。说明状态存储（state）与 Agent 定义（agent）各带独立 schema 版本号，用于迁移与兼容管理。状态目录默认 `~/.openclaw`（`.env.example`：`OPENCLAW_STATE_DIR=~/.openclaw`、`OPENCLAW_CONFIG_PATH=~/.openclaw/openclaw.json`、`OPENCLAW_HOME=~`）。

---

## 3. 运行机制与生命周期（事实 + 分析）

### 3.1 三元信任模型（README.md:18 与 docs 观点，来源自身结论）

README.md:18 原文：“The architecture case — trusted gateway, untrusted execution, deterministic policy”。即三层分离：
- **trusted gateway**：可信网关为会话/工具/事件/通道连接的本地控制面（README.md:68 “The Gateway is the local control plane for sessions, tools, events, and channel connections”）。
- **untrusted execution**：不受信任的执行环境；README.md:79 “Tools run on the host for the main session unless you configure sandboxing”，并引导用户读安全指南与沙箱指南。
- **deterministic policy**：确定性策略（`src/agents/agent-tools*.ts` 的工具策略、`.env.example` 的 token 校验、`net-policy` 网络策略包等）。

Claude 推断：这套模型的核心是把“策略/控制”与“执行/风险”解耦，用网关注入策略、用沙箱隔离执行。对教育类 Agent（面对未成年人/家长数据）尤为重要——不可信任的输入应默认低权限执行，DM 通道未知发送者默认需配对。

### 3.2 模型运行时选型（架构文档 `## Runtime Selection`，事实）

- 内置 runtime id 为 `openclaw`；旧别名 `pi` 归一化为 `openclaw`；`codex-app-server` 归一化为 `codex`。
- 插件 harness 可注册额外 runtime id（例如 `codex`）。
- 运行时策略是“模型/provider 级”的 `agentRuntime.id` 配置（模型条目优先于 provider 条目）；未设置或 `default` 解析为 `auto`。
- `auto` 选择支持有效 provider 路由的已注册插件 harness，否则用内置 OpenClaw runtime；provider 或模型前缀本身不会单独选中 harness。
- `## Model Runtime Generations`：网关启动与配置/插件/认证发布时，为每个配置的 agent 构建一份“准备好的模型运行时 generation”，每代持有认证模板、模型注册表、投影模型目录的原子快照；agent 运行从快照 fork 可变的认证与注册表存储，而 browse/status/cron/doctor/TUI/PDF/image 路径读取已发布的目录，避免重复文件系统发现。失败或过期的 generation 不会与更新的部分 generation 同时被服务。

Claude 推断：这是“快照化发布 / fork 式运行”的可观测、可回滚模式，值得 junshi-app 在模型配置多租户或多 agent 场景借鉴——每次启动把模型栈做成一次原子快照，避免运行期配置漂移。

### 3.3 通道（Channels）与事件驱动（事实 + 分析）

`src/channels/` 包含 allowlists、account-config、ack-reactions、bundled-channel-catalog、channel-config 等。README 列出 WhatsApp、Telegram、Slack、Discord、Google Chat、Signal、iMessage 等。网关作为控制面接收通道消息、触发会话、调用工具。`src/cron`、`src/daemon`、`src/auto-reply`、`src/flows` 表明存在定时、后台守护、自动回复与流程编排。

Claude 推断：OpenClaw 把“消息通道”抽象为网关下的统一接入层，一个 agent 对多通道复用同一内核。junshi-app 若未来需要“家长端 App / 微信 / Web”多入口，可参考“内核与通道分离、通道做成配置化插件”的形态，而非每个入口各写一套逻辑。

### 3.4 记忆（memory）（事实）

`src/memory/` 含 `memory-artifact-provenance.ts`、`root-memory-files.ts`；`packages/memory-host-sdk/` 提供宿主 embedding 注册等。说明记忆有“宿主侧 SDK + 根记忆文件 + 溯源”三层。README 未见把记忆列为独立营销词，属工程内置能力。

### 3.5 配置优先级（.env.example，事实）

`.env.example` 原文注释（定位：文件开头）：“Env-source precedence（最高→最低）：process env, ./.env, ~/.openclaw/.env, then openclaw.json `env` block”；直接配置键（如 `gateway.auth.token`、通道 token）独立于 env 加载解析，常优先于 env 回退。另有 `OPENCLAW_INCLUDE_ROOTS` 用于限定 `$include` 指令在 openclaw.json 中可解析文件的范围（默认限定在 openclaw.json 所在目录），这是针对配置注入攻击的一个边界控制。

---

## 4. 部署、测试与工程配套（事实）

### 4.1 容器部署（docker-compose.yml，已核验）

- 服务 `openclaw-gateway`：`node dist/index.js gateway --bind lan --port 18789`；固定容器内路径（`HOME=/home/node`、`OPENCLAW_STATE_DIR=/home/node/.openclaw`、`OPENCLAW_CONFIG_PATH`、`OPENCLAW_WORKSPACE_DIR`）防止 macOS 主机路径从 `.env` 泄漏进容器引发 EACCES（注释引述 issue #77436）。
- 安全加固：`cap_drop: [NET_RAW, NET_ADMIN]`、`security_opt: no-new-privileges:true`、`init: true`、`restart: unless-stopped`、healthcheck（`dist/docker-healthcheck.js`，30s/5s/retries 5）。
- 沙箱需显式启用：挂载 `/var/run/docker.sock` 需 `--build-arg OPENCLAW_INSTALL_DOCKER_CLI=1` 或 `scripts/docker/setup.sh` 配 `OPENCLAW_SANDBOX=1`；`DOCKER_GID` 需手动指定。默认不启用沙箱。
- 可观测性：OTEL_*（OTLP HTTP/protobuf traces/metrics/logs）注入；Prometheus 走已有认证的网关路由，不需额外端口。

### 4.2 平台部署（fly.toml，已核验）

- Fly.io：`[processes] app = "node dist/index.js gateway --allow-unconfigured --port 3000 --bind lan"`；`NODE_OPTIONS=--max-old-space-size=1536`；`OPENCLAW_STATE_DIR=/data`；`min_machines_running=1`、`auto_stop_machines=false`（保持持久连接）；强制 HTTPS。`render.yaml` 提供另一平台路径。

### 4.3 测试与质量（qa/、test/，事实）

- `qa/maturity-scores.yaml`、`qa/scenarios/`、`qa/frontier-harness-plan.md`、`qa/convex-credential-broker/`。
- 各模块带 `.test.ts` 与 `*.e2e.test.ts`（如 `docker-setup.e2e.test.ts`、`agent-exec-plugin.e2e.test.ts`）。
- 工程工具链：`config/` 下 oxlint、tsconfig、markdownlint、knip（检测未使用导出）、shellcheck、swiftlint、stylelint；`.pre-commit-config.yaml` 与 `.semgrepignore` 提供 git 钩子与 Semgrep 静态扫描。

---

## 5. 事实 / 来源结论 / Claude 推断 分离表

| 类别 | 内容 | 定位/来源 |
|---|---|---|
| 事实 | 官方仓库 openclaw/openclaw，版本 2026.8.1，MIT，main 分支 | package.json、REST API |
| 事实 | schemaVersions state 15 / agent 19 | package.json `openclaw` |
| 事实 | 资源包可经 openclaw.extensions/skills/prompts/themes 声明 | docs/agent-runtime-architecture.md Manifests |
| 事实 | 运行时 id：openclaw 内置、codex 插件；模型/provider 级 agentRuntime.id 决定 | 架构文档 Runtime Selection |
| 事实 | Gateway 为本地控制面；默认宿主执行工具，沙箱需显式开启 | README.md:68,79 |
| 事实 | 状态/配置默认 ~/.openclaw/openclaw.json | .env.example |
| 来源结论 | “trusted gateway, untrusted execution, deterministic policy” | README.md:18 |
| 来源结论 | env 优先级 process > ./.env > ~/.openclaw/.env > openclaw.json env 块 | .env.example |
| Claude 推断 | 快照化 model generation 提供可回滚的可观测模型栈 | 架构文档 + 推理 |
| Claude 推断 | 多通道抽象利于多端复用同一内核 | README + src/channels + 推理 |

---

## 6. 风险与不适于照搬的部分（分析/建议）

1. **规模与复杂度**：单仓库同时承载桌面/mobile/网关/技能注册表多套子系统，学习与维护成本高；junshi-app 不应整体复制，只取内核+配置+生命周期模式。
2. **默认不沙箱**：README 明确工具默认在宿主执行，需显式配置沙箱；对教育数据默认低权限是刚需，junshi-app 应把沙箱/最小权限设为默认而非可选。
3. **外部凭证处理**：`.env.example` 暴露 `CLAUDE_WEB_SESSION_KEY`、`CLAUDE_WEB_COOKIE`、`CLAUDE_AI_SESSION_KEY` 等会话/凭证类变量（用于代理通道），存在凭据管理风险；junshi-app 若涉第三方会话须严格脱敏与最小化。
4. **第三方依赖**：`@earendil-works/pi-tui`、host-gateway 别名依赖 Docker Desktop 等，跨平台一致性有取舍（架构文档明确列出边界）。
5. **供应链/许可证**：MIT 主许可但有 `THIRD_PARTY_NOTICES.md`；引用其模式无需复制代码，规避许可证与供应链风险（不引入其 npm 依赖）。
6. **版本演进快**：版本命名 `2026.8.1`，schemaVersions 随迭代递增，跟随上游会持续追赶；junshi-app 只吸收稳定抽象，不绑定其具体版本。

---

## 7. 对 mate 元文档与 junshi-app 的启示（建议）

以下均为“候选建议”，需经产品发起人确认后写入决策登记，不自动生效。

1. **内核复用包**：把“判断引擎/学业规划”等核心 Agent 逻辑做成 `packages/agent-core` 式的可复用内核，与通道、UI 解耦；mate 中应新增“内核/模型调用/记忆/工具”的组件边界文档（对照其 agent-core 契约）。
2. **状态 schema 版本化**：junshi-app 引入 `schemaVersions`（state/agent 分版本）管理学业数据与 Agent 定义演进，mate 决策登记应记录版本化迁移策略。
3. **资源清单化**：参照 `openclaw.extensions/skills/prompts/themes` 声明，为 junshi-app 的 skills/prompts/themes 建立清单文件，mate 中登记“资源注册表”条目。
4. **运行时选型显式配置**：把“模型 provider / agentRuntime”做成配置项而非硬编码；对教育场景锁定允许的 provider 路由。
5. **信任模型写入产品原则**：把“可信网关 + 不受信任执行 + 确定性策略 + 默认最小权限沙箱”作为 junshi-app 家长/隐私/安全原则的一条，纳入 mate 安全编。
6. **可观测性默认开启**：借鉴 OTEL 注入与 healthcheck，junshi-app 从第一天就带日志/指标/探活，避免后补。
7. **部署多路径但抽象统一**：保留 Docker/Fly 等部署描述，但把容器内路径固定化防主机路径泄漏（呼应其 #77436 教训）。
8. **QA 成熟度矩阵**：可参考 `qa/maturity-scores.yaml`，为 mate 各编能力建立成熟度分档，支撑“验证与阶段门槛”。

---

## 8. 局限

- 本研究基于 GitHub API 与仓库原文取样，未执行构建、测试或运行；`.test.ts` 是否通过、运行时行为、性能未实证。
- 仓库迭代极快，commit 基准为 `a5b9955`（2026-09-03）；后续 commit 可能改变目录/文档，本报告结论对更早/更新版本不保证一致。
- 官方文档站 `docs.openclaw.ai`、ClawHub 等内容未抓全，仅以仓库内 `docs/` 与 README 为据。
- 未核对 LICENSE 全文细节（MIT SPDX 显示为 NOASSERTION，需以 LICENSE 文件为准）。
- 外部材料为不可信数据；本报告未把任何执行/配置指令当作本地事实执行。

---

## 9. 关键来源与证据定位

| 证据 | 稳定来源 | 版本/日期 | 原文定位 |
|---|---|---|---|
| 官方仓库元数据 | https://github.com/openclaw/openclaw | 2026-09-03 | REST API full_name/default_branch/license/pushed_at |
| commit 基准 | GitHub REST | a5b9955（2026-09-03） | /commits |
| 版本/描述/license/bin/schemaVersions | package.json | v2026.8.1 | 顶层字段 |
| 定位/信任模型/安装/通道 | README.md | main | 行 1,18,22-64,66-73,79 |
| 组件分布/运行时选型/Manifests | docs/agent-runtime-architecture.md | main | Runtime Layout / Runtime Selection / Manifests |
| 状态/配置默认与 env 优先级 | .env.example | main | 文件开头注释 + OPENCLAW_STATE_DIR |
| 容器部署/加固/沙箱 | docker-compose.yml | main | openclaw-gateway 服务 |
| 平台部署 | fly.toml | main | processes/http_service |
| 质量体系 | qa/、test/、config/ | main | maturity-scores.yaml、e2e 测试、lint 配置 |
| 顶层目录 | GitHub REST /contents/ | main | 根目录列表 |

状态标注：仓库定位、版本、目录结构为 `已核验`（API 原文）；信任模型、schema 迁移、快照化等运行机制推断为 `部分核验`；性能、运行时行为、测试通过情况为 `未实证`。全部为 `候选/参照`，未升级为决策。

---

## 附：Skill 使用记录

- 阶段：OpenClaw 外部调查取证
- 任务类型：外部研究（GitHub 仓库只读调查 + Markdown 报告撰写）
- 目标与成功标准：核实官方仓库并产出不少于 2500 字中文独立报告，证据可定位、事实/分析/建议/局限分离、面向 mate 与 junshi-app。
- 能力发现：`skill-first`（全局命令，仓库路由）、`agent-reach`（全局 skill，GitHub 路由，实际运行 `agent-reach doctor --json`，github 后端为 gh CLI 且已认证）、`md-writing`（全局 skill）、`research`（agent 类型）、`playwright-cli`（未用，理由：GitHub API 可只读取证，无需浏览器自动化）。
- 选择理由：研究任务按仓库协议选 agent-reach 的 GitHub 路由 + research agent；Markdown 报告按协议调用 md-writing。
- 实际调用：`agent-reach`（doctor + GitHub 路由指引）、`research` 子代理（后台调查）、`md-writing`（写作规范）。
- 协作 agent/工具/MCP：`research` 子代理；`gh` CLI、GitHub REST API（filesystem MCP 用于建目录）。
- 输入：仓库 URL openclaw/openclaw、REST API 端点、目录/文件路径。
- 输出：本报告（`调研报告/OpenClaw调查报告.md`）。
- Markdown 专项：已实际调用 `md-writing` 并遵循其结论先行/事实分级/边界闭合规范。
- 阻塞/降级：`curl` 访问 Jina Reader（raw 域名）被权限拒绝；降级为 `gh api` 直读仓库文件，已覆盖所需证据。
- 未调用项及理由：`playwright-cli`（无需浏览器抓取，API 即可）、`crawl4ai`（同上）、其他平台（本次仅 GitHub）。
- 验证：报告写入后 `git status` 应仅新增本文件；字数核查见下节验证摘要。
- 下一步：等待 `research` 子代理返回的补充证据，若有新增关键事实则并入本报告后交主工作区取回；无则由主 Agent 审核。
