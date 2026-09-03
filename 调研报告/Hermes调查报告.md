# Hermes Agent 调查报告

- **调查对象**：NousResearch/hermes-agent（官方仓库）
- **报告状态**：已核验（基于公开 GitHub API 与官方 README；运行安装、真实部署和性能未在本地执行）
- **实际访问日期**：2026-09-03
- **取证版本**：`main` 在访问时提交 `97f3229dfdc06779f348ab8e7bee043262c3aaa7`，提交时间 2026-09-03T03:17:48Z；同时核验最新公开标签 `v2026.8.31`。报告引用优先绑定上述 commit；标签仅作为发布线索，不把它等同于 HEAD。
- **稳定来源**：[官方仓库](https://github.com/NousResearch/hermes-agent)、[官方文档](https://hermes-agent.nousresearch.com/docs/)、[架构文档入口](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)
- **目标读者**：mate 元文档维护者、junshi-app Agent 工程设计者。

## 1. 执行范围、方法与成功标准

本次任务来自《计划书》“四个 Agent 仓库的外部调查与取证”。范围限定为官方仓库身份核验、README/目录/关键源码和配置的只读调查，重点回答产品定位、核心组件、依赖关系、生命周期、工程目录、风险以及对 mate 和 junshi-app 的启示。成功标准是：报告不少于 2500 字；每个关键判断都能回到稳定 URL、commit/tag、文件路径或可定位摘录；事实、来源自身结论、Claude 分析/推断、候选建议和局限分开；不修改代码和既有仓库文件。

实际调用了 `skill-first`（先界定多阶段外部研究和 Markdown 写入范围）、`agent-reach`（GitHub 路由；运行 `agent-reach doctor --json`，GitHub 的 `gh` 已安装且存在显式认证，但 doctor 将其标为 warn、active_backend 为 null，因此使用可审计的 `gh api` 读取公开端点；运行 `agent-reach check-update`，结果为 v1.5.0 最新）和 `md-writing`（按研究报告骨架写作）。实际外部工具为 `gh search repos`、`gh api` 和官方文档 URL 的网络读取尝试；未调用 playwright-cli，因为本任务的官方 GitHub API 已能返回原始源码、目录和提交元数据，浏览器自动化不能增加必要证据。官方架构页面的 curl 读取在宿主权限策略下被阻塞，故不引用其未取得的正文。临时目录创建在当前 worktree 内仅为目标报告目录；没有安装依赖、运行代码或克隆仓库。

## 2. 官方身份核验与项目定位

### 2.1 身份证据表

| 字段 | 已核验事实 | 来源与定位 | 状态/对应缺口 |
|---|---|---|---|
| 仓库身份 | `NousResearch/hermes-agent`，描述为 “The agent that grows with you”，所有者 Nous Research，默认分支 main | GitHub REST `GET /repos/NousResearch/hermes-agent`，访问 2026-09-03；[URL](https://api.github.com/repos/NousResearch/hermes-agent) | 已核验；G1 |
| 许可证 | MIT | 仓库元数据 license=`MIT`；根目录 `LICENSE`；[URL](https://github.com/NousResearch/hermes-agent/blob/main/LICENSE) | 已核验；G5 |
| 版本 | `pyproject.toml` 项目版本 `0.21.0`；公开标签含 `v2026.8.31` | `pyproject.toml` 顶部；GitHub tags API；[tags](https://github.com/NousResearch/hermes-agent/tags) | 部分核验：包版本、标签命名未证明完全一一对应；G1/G5 |
| 当前提交 | `97f3229dfdc06779f348ab8e7bee043262c3aaa7`，提交消息为 JS 格式化合并 | GitHub commits API；[commit](https://github.com/NousResearch/hermes-agent/commit/97f3229dfdc06779f348ab8e7bee043262c3aaa7) | 已核验；G5 |
| 官方入口 | README 链向 `hermes-agent.nousresearch.com` 及 `/docs/` | `README.md` 顶部和 Documentation 表 | 已核验；G1 |

### 2.2 定位与场景

**外部事实**：`README.md` 将 Hermes 定义为 Nous Research 构建的“self-improving AI agent”，宣称可从经验创建和改进 skills、持久化知识、搜索历史会话，并跨会话形成用户模型。README 的能力表列出真实终端 TUI、多消息平台 gateway（Telegram、Discord、Slack、WhatsApp、Signal 等）、语音备忘录转录、定时自动化、隔离子 Agent、Python RPC 工具脚本，以及七类终端后端（local、Docker、SSH、Singularity、Modal、Daytona、Vercel Sandbox）。其用户入口不是单一 Web 聊天，而是 CLI 和一个可把同一核心连接到多平台的 gateway；README 明确说可从 Telegram 与云 VM 对话。

**来源自身结论**：README 以“闭环学习”“runs anywhere”“research-ready”等产品主张组织叙事，并将 CLI、gateway、TUI、Electron desktop 视为同一 Agent core 的不同入口。`AGENTS.md`（仓库根目录）进一步说明 Hermes 的核心在 CLI、messaging gateway、TUI 和 Electron desktop 间复用，学习能力由 memory + skills 支撑，扩展首选 plugins 和 skills 而非继续膨胀 core。

**Claude 分析**：这不是一个只展示模型调用的样例，而是把“会话运行时 + 多入口适配 + 工具执行隔离 + 状态/记忆 + 可扩展分发 + 运维入口”组合成产品。它适合拿来审查学业军师的工程闭环，不适合把自我改进、全平台接入或云端终端数量直接当作学业场景需求。

## 3. 工程组成和依赖关系

### 3.1 分层组件

从目录和文件名可复核地拆成以下层次：

1. **启动与用户入口**：根目录 `hermes`（可执行入口）、`cli.py`、`run_agent.py`、`hermes_bootstrap.py`、`hermes_startup_watchdog.py`；`hermes_cli/`承载命令 mixin、配置、交互等拆分模块。README 的 Getting Started 给出 `hermes`、`hermes model`、`hermes tools`、`hermes config set/get`、`hermes gateway`、`hermes setup`、`hermes doctor`、`hermes update` 等运维和交互命令。
2. **Agent 核心循环**：`agent/conversation_loop.py` 是从 `run_agent.AIAgent` 拆出的单轮驱动函数。源码模块说明原文指出，一次用户 turn 经过 model call、tool dispatch、retries、fallbacks、compression、post-turn hooks 和 background memory/skill review nudges；`agent/context_engine.py`、`context_compressor.py`、`turn_context.py`、`turn_retry_state.py` 等负责上下文和重试。
3. **模型/供应商适配**：`agent/anthropic_adapter.py`、`bedrock_adapter.py`、`gemini_native_adapter.py`、`vertex_adapter.py`、`codex_responses_adapter.py`、`openrouter_client.py`、`agent/model_metadata.py`、`providers/`组成适配边界。README 明确支持 Nous Portal、OpenRouter、OpenAI、自有 endpoint 等，并可用 `hermes model` 切换而不改代码。
4. **工具层**：`tools/`包含 `registry.py`（注册/发现）、`tool_executor.py` 相关配合模块、文件操作、shell/terminal、browser、computer use、code execution、delegate、memory、cron、MCP、媒体和平台工具。可定位的文件包括 `tools/delegate_tool.py`、`tools/memory_tool.py`、`tools/mcp_tool.py`、`tools/cronjob_tools.py`、`tools/path_security.py`、`tools/approval.py`、`tools/lazy_deps.py`。工具不是循环内部硬编码的一团函数，而是可注册、可门控、可按 toolset 分发的边缘能力。
5. **终端执行环境**：根目录 `toolsets.py`、`toolset_distributions.py`以及 `tools/environments/`；README 列出的 local/Docker/SSH/Singularity/Modal/Daytona/Vercel Sandbox 表明 shell 执行和 Agent 推理被分开，运行环境可替换。
6. **持久状态与记忆**：`hermes_state.py`声明 SQLite State Store，支持 WAL、并发读/单写、FTS5 会话全文搜索、压缩触发的 session splitting 和 `parent_session_id` 链，并以 source 标记 CLI/Telegram/Discord 等会话。`agent/memory_manager.py`是 provider 的单一集成点，源码注释明确流程为 system prompt 注入、pre-turn prefetch、post-turn sync、后台 queue prefetch；且只允许一个外部 provider，以避免 schema 膨胀和后端冲突。
7. **多平台 gateway**：`gateway/`包含 `config.py`、`session.py`、`delivery.py`、`pairing.py`、`authz_mixin.py`、`platform_registry.py`、`platforms/`、`readiness.py`、`restart.py`、`shutdown_*`、`scale_to_zero.py`等。`gateway/platform_registry.py`说明插件平台可通过 `PluginContext.register_platform()`注册，gateway 优先查 registry，找不到再回退 legacy instantiate 路径，成功 adapter 再绑定 runner。这是平台扩展与核心运行器之间的明确边界。
8. **技能、插件与研究工程**：`skills/`按 `research`、`software-development`、`devops`、`web`、`productivity` 等分类；`plugins/`、`optional-skills/`、`optional-mcps/`负责扩展；`evals/`、`tests/`、`tests-js/`、`batch_runner.py`、`trajectory_compressor.py`支撑评测、轨迹生成和训练资料。
9. **桌面和 Web 资产**：`apps/bootstrap-installer`、`apps/desktop`、`apps/shared`，另有 `native/`、`web/`、`website/`、`ui-tui/`。这些不是 Agent 核心依赖，而是发行、界面、共享前端/桌面边缘。

### 3.2 调用与数据流

**事实**可由 `conversation_loop.py` 的模块说明和导入项定位：输入 user message 后，循环构造 turn context，准备/压缩历史，调用 provider adapter；模型返回 tool call 时交给工具注册/执行层，执行结果追加回消息，再继续模型调用；API 错误进入分类、重试和 failover；一轮结束执行 memory/skill review 等 post-turn hook。`hermes_state.py`把消息历史和会话元数据持久化到 SQLite/FTS5；`memory_manager.py`在 pre-turn 预取外部记忆、系统提示构建时加入规则、post-turn 同步新信息。多平台消息先由 gateway adapter 归一化到会话，再复用同一循环，结果经 `delivery.py` 回传平台。定时任务由 `cron/scheduler.py`、`cron/jobs.py`、`cron/executions.py`驱动，工具或 delivery 负责投递。

**Claude 推断**：该流可抽象为 `入口适配 -> 会话身份/授权 -> 上下文组装 -> 模型路由 -> 工具策略/执行 -> 结果回填 -> 持久化与记忆同步 -> 渠道投递`。关键是持久化和安全并非循环之后的附属脚本，而是每轮生命周期的约束点。

## 4. 启动方式与生命周期

README 的官方快速路径是安装脚本（Linux/macOS/WSL2：`curl -fsSL .../install.sh | bash`；Windows PowerShell：`iex (irm .../install.ps1)`），随后 `source ~/.bashrc` 或 zsh，再运行 `hermes`。安装器负责 uv、Python 3.11、Node.js、ripgrep、ffmpeg；Windows 还准备隔离的 portable Git Bash。开发者路径是进入 `$HERMES_HOME/hermes-agent`，执行 `uv pip install -e ".[all,dev]"` 和 `scripts/run_tests.sh`；README 特别警告不要把 venv 放在 Agent 操作目录内，避免相对路径命令误删运行时。

一次 CLI 生命周期是：bootstrap 设置平台兼容性 -> CLI 解析命令/载入配置和历史 -> 建立 Agent 与 provider/toolset -> 进入交互式 turn 循环 -> 可中断、重试、压缩或切模型 -> 将会话和记忆写入状态库 -> 退出时清理。gateway 生命周期是：`hermes gateway setup`配置平台和授权 -> `hermes gateway start`启动单一 gateway -> 各 platform adapter 接收消息并按会话路由到核心 -> delivery 回传；目录中的 readiness、lifecycle ledger、shutdown watchdog、restart 和 scale-to-zero 表明启动、排空、重启和停机都被当作一等运维状态。Cron 则在后台按 job/execution 运行，可将结果投递到平台。

**局限**：我未执行安装脚本、未启动 gateway、未调用真实模型或平台，因此上述启动链是源码/README 设计证据而非本地运行验证；官方架构网页读取被宿主策略阻塞，不能据此确认网页中的额外细节。

## 5. 配置、提示词、工具、记忆与编排组织

### 配置。**事实**：根 `.env.example`把 provider 密钥作为环境变量示例，并明确默认模型在 `~/.hermes/config.yaml`，可用 `hermes model` 或 `hermes setup`修改；`cli-config.yaml.example`说明配置可复制到该路径或用 `hermes config set`更新，且数据库 `journal_mode`支持 `wal`/`delete`，对容器 bind mount、NFS、SMB 等非 WAL crash-safe 文件系统给出显式 DELETE 选择。`pyproject.toml`把 Python 版本限制为 `>=3.11,<3.14`，并说明 uv 解析和 Rust-backed transitive wheel 的兼容性原因。

### 提示词和上下文。**事实**：根 `SOUL.md`是默认人格/行为约束文件；`AGENTS.md`是开发和 Agent coding instructions；`agent/system_prompt.py`、`prompt_builder.py`、`prompt_caching.py`、`prompt_cache_boundary.py`、`context_files`文档入口共同构成提示词层。`AGENTS.md`将“每对话 prompt caching”列为 sacred，指出过去上下文、toolset 或 system prompt 的任意变更会使缓存失效，唯一例外是 context compression。

### 工具。**事实**：`tools/registry.py`支持注册，`toolsets.py`和 `toolset_distributions.py`负责选择/分发；`approval.py`、`path_security.py`、`plugin_guard.py`、`schema_sanitizer.py`显示工具调用有审批、路径、插件和 schema 安全面。能力按核心工具、服务 gated 工具、插件和 skills 分层，减少每次 API 请求的 schema 负担。

### 记忆。**事实**：SQLite 会话状态、FTS5 搜索和外部 MemoryProvider 是两个层次；`MemoryManager`要求最多一个外部 provider，并提供 checkpoint API 兼容逻辑。README 还把 skill 创建、skill 使用中的自我改进、会话搜索、Honcho 用户建模列为功能。这里应区分：仓库代码确实有 manager/state/provider 接口；“deepening model of who you are”是 README 的产品表述，不等同于已在所有安装模式开启的效果。

### 任务编排。**事实**：`tools/delegate_tool.py`、`tools/async_delegation.py`、`agent/subagent_lifecycle.py`、`agent/delegation_context.py`共同支持隔离子 Agent 与并行工作流；`cron/`提供 unattended schedule；`batch_runner.py`和 trajectory 相关文件面向研究/数据生成，而不是普通会话。**分析**：Hermes 将在线交互编排、定时编排、研究批处理分开，避免把所有异步工作都塞进单一 conversation loop。

## 6. 开发、调试、测试、部署和维护

仓库根目录同时存在 `tests/`（Python）、`tests-js/`（JavaScript）、`evals/`（行为/模型评测）、`scripts/`（工程脚本）和 `Dockerfile`、`docker-compose.yml`、`docker-compose.windows.yml`、`nix/`、`flake.nix`。这说明测试并非仅做单元测试：至少有语言级测试、评测、容器化、Nix/跨平台安装和运行脚本多条验证路径。`hermes doctor`是用户侧诊断入口，`hermes update`是更新入口；gateway 下的 readiness、session_db_recovery、shutdown_forensics、restart_loop_guard 等文件显示维护覆盖数据库恢复、优雅停机、重启回路和运行态观测。

`pyproject.toml`核心依赖采用精确 `==` pin；其注释明确指出范围依赖会让 PyPI 新传递版本未经代码审查进入用户环境，更新要求同步 `uv.lock`。同时按 provider-specific 和“所有会话必需”区分 core dependencies 与 extras，并以 `tools/lazy_deps.py`按需安装。该策略不能消除供应链风险，却让变更可审查、爆炸半径可控。README 还给出 Windows 对 uv 的签名/attestation 验证方法，体现发行物来源验证意识。

**风险事实与分析**：

- **供应链**：安装脚本是远程 `curl | bash`，依赖多个包和外部 provider；即使精确 pin 也需保护 lockfile、发布物和安装域名。建议学业军师生产环境采用已审计 artifact、hash/签名校验和可回滚版本，而不是照搬一键脚本。
- **网络与隐私**：Telegram/Discord 等消息平台、模型 provider、搜索/浏览器/MCP、语音和 Honcho 会把用户消息、文件或元数据交给外部服务。Hermes README 宣称多平台便利，但没有在我取得的 README 片段中给出学业数据最小化、家长授权或中国境内合规保证。学业军师必须明确数据分类、出境开关、保留期、删除和审计。
- **执行安全**：shell、browser、computer use、代码执行和插件扩展的能力面很大；`approval.py`、`path_security.py`等是有利证据，但我没有运行安全测试，不能证明默认策略足够。不能把目录名当成安全保证。
- **运行可靠性**：WAL 在某些挂载文件系统不安全，项目提供 DELETE fallback；多平台并发、重启、scale-to-zero、远程环境休眠会引入消息重复、迟到、丢失和状态一致性问题，需本地压测和故障演练。
- **维护成本**：Hermes 功能面极宽，七种终端 backend、约二十平台、多个模型适配器和桌面/Web 发行会扩大测试矩阵；小团队直接复制会得到高耦合运维负担。

许可证为 MIT，允许参照和再使用，但必须保留版权/许可声明；依赖许可证、外部服务条款和模型授权仍需逐项复核，不能仅由 MIT 推导整个系统可商用。

## 7. 对 mate 元文档的启示（G1-G5 映射）

以下是**候选/参照建议，不是当前产品决策**：

- **G1 产品定位与入口边界（候选）**：mate 应明确 Agent core、CLI/Web/API、家长/学生入口及消息渠道是否同一会话模型；Hermes 的多入口复用可作为边界参照，但学业军师优先保留少量受控入口。
- **G2 运行机制与领域模型（候选）**：为“单轮 turn”建立可审计状态机：接收、授权、上下文、模型、工具、回填、持久化、总结/记忆、投递、失败恢复。Hermes `conversation_loop.py`、`turn_context.py`和`hermes_state.py`提供章节拆分参照。
- **G3 工具/记忆/编排责任（候选）**：mate 需要分别定义工具契约、审批/沙箱、短期会话、长期记忆、知识检索、子 Agent 和定时任务，明确哪些是核心必需、哪些是插件/可选增强。Hermes 的“窄腰核心、边缘扩展”原则以及 MemoryManager 单一 provider 约束值得参照。
- **G4 验证与治理（候选）**：建立 provider contract tests、工具安全测试、会话恢复/幂等测试、提示词缓存不变量、评测集、部署 smoke test 和回滚门槛；不能只验 UI 或模型回答。
- **G5 运行、隐私和供应链（候选）**：mate 应记录配置真源、密钥边界、外部数据流、留存/删除、审计日志、锁文件、发布签名、迁移/回滚和网络故障策略。Hermes 的 exact pin、uv.lock、doctor、WAL 选择可作工程参照，但不代表已满足学业数据治理。

## 8. 对 junshi-app 代码库布局的启示

**Claude 分析**：从 Hermes 可以抽出一个最小但完整的可持续闭环，而不是复制其目录数量：

```text
入口层（CLI/API/异步任务）
  -> 会话与身份层（学生/家长/设备/授权/审计）
  -> Agent runtime（turn、上下文、模型路由、重试、压缩）
  -> 工具与外部服务（注册、策略、审批、适配器）
  -> 数据层（会话、记忆、知识、事件、迁移）
  -> 观测与治理（日志、指标、trace、评测、告警、回滚）
```

建议在 mate 确认后映射到 junshi-app 的清晰边界：`apps/`只放可部署入口；`agent/`只放运行时和领域编排；`providers/`只放模型/外部 API 适配；`tools/`只放工具契约及执行器；`memory/`与`knowledge/`分开；`gateway/`或`api/`负责协议、身份、投递；`config/`集中非秘密配置和 schema；`tests/`分层覆盖单元、契约、集成、评测、安全和恢复；`deploy/`、`ops/`、`migrations/`和`docs/`承载交付生命周期。代码与 mate 的边界应是：mate 定义责任、接口、状态、风险和验收；代码实现这些契约，不能让目录存在反向生成产品决策。

Hermes 最值得借鉴的不是“有很多平台”，而是三个结构性原则：第一，核心循环承担稳定的窄腰职责，能力通过 registry/plugin/skill 向边缘扩展；第二，会话状态、记忆同步、上下文压缩和失败恢复被放进生命周期而非事后脚本；第三，开发/部署/评测/运维资产与运行代码同仓但职责分层。对于学业军师，应增加 Hermes README 未能证明的领域专属层：学习目标与证据模型、家长授权、未成年人隐私、建议可解释性、人工复核和教育安全策略。

**不适合直接照搬**：七种终端 backend、多平台 gateway、开放式 shell/browser/computer-use、自我生成 skills、Honcho 用户建模、远程服务和 `curl|bash`安装都应先通过 mate 的风险门槛。尤其不能因为 Hermes 具备“self-improving”宣传就默认允许学业 Agent 修改自身提示词、工具权限或教育策略；这些变化必须版本化、评测、审批和可回滚。

## 9. 结论、局限与本地验证清单

### 结论

**外部证据结论**：Hermes 是一个 MIT 许可、以 NousResearch/hermes-agent 为官方源、以共享 Agent core 为窄腰、向 CLI/TUI/桌面/多平台 gateway/定时任务/远程终端扩展的完整 Agent 产品工程。`conversation_loop.py`给出模型调用—工具派发—重试/回退—上下文压缩—后置记忆/技能审查的生命周期骨架；`hermes_state.py`给出 SQLite/WAL/FTS5/会话链；`memory_manager.py`给出 provider 集成边界；`gateway/platform_registry.py`给出平台插件注册模式；`pyproject.toml`和配置示例给出 Python 约束、依赖 pin、lazy extras 与数据库部署选择。

**本仓库候选建议**：将上述证据用于补齐 mate 的运行机制、工具安全、状态持久化、评测治理和部署回滚章节，并将 junshi-app 代码布局设计成“入口—runtime—provider—tools—memory/knowledge—data—ops”的闭环；候选内容仍需产品发起人确认，不自动升级为决策。

### 局限与待复核

1. GitHub API 访问到了源码文本和目录，但没有本地 checkout，因此未运行测试、类型检查、静态安全扫描或实际启动。
2. `main` 是快速变化分支；commit `97f3229`和标签 `v2026.8.31`之间的精确发布差异尚未逐项比较，后续引用应继续绑定 commit。
3. 官方架构网页读取受宿主权限阻塞；本报告不把未读取页面内容当证据。
4. README 的能力描述是来源自身产品结论，不能替代可用性、成本、延迟、隐私和安全测试。
5. 未核验所有 `providers/`、平台 adapter、插件源码及完整依赖许可证；供应链和部署风险结论需另行审计。

### 本地验证清单

- [ ] 以 commit `97f3229...` 做只读 checkout，运行官方 `scripts/run_tests.sh`并记录结果。
- [ ] 检查默认 tool approval、sandbox、MCP 和 plugin trust 的实际配置，而不是只依据文件名。
- [ ] 在隔离环境验证 WAL/DELETE、session split、FTS5 搜索、重启恢复和多平台幂等。
- [ ] 对模型 provider、语音、搜索、浏览器、Honcho 等外部数据流做隐私/出境/留存评估。
- [ ] 对 exact pins、`uv.lock`、安装脚本、容器镜像和 release artifact 做 SBOM、签名与回滚演练。
- [ ] 由产品发起人确认 G1-G5 候选映射后，才写入 mate 正式决策或 junshi-app 实现计划。

## 10. 来源与证据索引

1. [NousResearch/hermes-agent README.md（commit 97f3229）](https://github.com/NousResearch/hermes-agent/blob/97f3229dfdc06779f348ab8e7bee043262c3aaa7/README.md)：定位、入口、安装、能力表、文档入口、贡献和迁移说明。
2. [AGENTS.md（commit 97f3229）](https://github.com/NousResearch/hermes-agent/blob/97f3229dfdc06779f348ab8e7bee043262c3aaa7/AGENTS.md)：共享核心、prompt caching、窄腰核心、插件/技能扩展原则。
3. [pyproject.toml（commit 97f3229）](https://github.com/NousResearch/hermes-agent/blob/97f3229dfdc06779f348ab8e7bee043262c3aaa7/pyproject.toml)：项目版本、Python 范围、精确依赖、extras/lazy dependency 和供应链注释。
4. [cli.py（commit 97f3229）](https://github.com/NousResearch/hermes-agent/blob/97f3229dfdc06779f348ab8e7bee043262c3aaa7/cli.py)：CLI/TUI 入口说明、bootstrap、toolset/skills 参数和交互依赖。
5. [agent/conversation_loop.py（commit 97f3229）](https://github.com/NousResearch/hermes-agent/blob/97f3229dfdc06779f348ab8e7bee043262c3aaa7/agent/conversation_loop.py)：单轮生命周期模块说明和上下文/重试/压缩导入。
6. [agent/memory_manager.py（commit 97f3229）](https://github.com/NousResearch/hermes-agent/blob/97f3229dfdc06779f348ab8e7bee043262c3aaa7/agent/memory_manager.py)：MemoryProvider 单一集成点、pre-turn/post-turn/checkpoint 机制。
7. [hermes_state.py（commit 97f3229）](https://github.com/NousResearch/hermes-agent/blob/97f3229dfdc06779f348ab8e7bee043262c3aaa7/hermes_state.py)：SQLite、WAL、FTS5、session split 和 source tagging。
8. [gateway/platform_registry.py（commit 97f3229）](https://github.com/NousResearch/hermes-agent/blob/97f3229dfdc06779f348ab8e7bee043262c3aaa7/gateway/platform_registry.py)：插件平台注册和 legacy fallback。
9. [cli-config.yaml.example（commit 97f3229）](https://github.com/NousResearch/hermes-agent/blob/97f3229dfdc06779f348ab8e7bee043262c3aaa7/cli-config.yaml.example)：配置真源提示、数据库 journal_mode。
10. [SOUL.md（commit 97f3229）](https://github.com/NousResearch/hermes-agent/blob/97f3229dfdc06779f348ab8e7bee043262c3aaa7/SOUL.md)：默认行为/人格文件。
11. [官方架构文档入口](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)：已确认为 README 链接目标，但正文在本次宿主网络读取中阻塞，状态为阻塞，不据其未取得内容作结论。
