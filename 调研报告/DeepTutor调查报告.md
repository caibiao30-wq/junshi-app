# DeepTutor Agent 调查取证报告

- **报告状态**：已核验（外部仓库静态取证）；适配建议为候选，未构成本仓库产品决策
- **实际访问日期**：2026-09-03
- **调查对象**：官方 GitHub 仓库 [HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor)
- **核验版本**：默认分支 `main`，提交 `93df3d48b70586c36b20ebf82c613a67ed20677`，提交信息 `release: v1.6.4`，提交时间 2026-09-02 17:38:54 UTC；README 发布条目标为 v1.6.4、2026-09-03。许可证 API 元数据为 Apache-2.0。
- **范围**：只读 GitHub API（由 agent-reach 路由的 `gh` CLI）获取仓库元数据、目录树、README、源码、配置和部署文档；未克隆、未执行 DeepTutor、未安装依赖。

## 一、结论摘要

DeepTutor 不是只有一个聊天提示词的演示，而是一个以学习场景为中心、把 Agent 循环、工具注册、能力编排、知识库/RAG、三层记忆、会话恢复、Web/API、CLI、容器部署和安全诊断放进同一产品的工程型系统。官方 README 标题为 “DeepTutor: Lifelong Personalized Tutoring”，定位是长期个性化辅导；README 的版本历史显示 v1.4.0 已将 Auto Mode、三层 Memory、agentic Deep Research/Solve/Question、LlamaIndex RAG 和 restart-safe turn runtime 汇合，v1.6.4 又加入隔离运行时、Books、Mastery、Reading/session 等能力。

最值得借鉴的不是某个模型或前端页面，而是四个结构性原则。第一，把通用 Agent loop 与具体能力解耦：`deeptutor/runtime/agentic/loop.py` 以 `LabelProtocol` 和 `LoopHost` 把标签协议、工具轮次、暂停、终止、上下文预算、重试和强制收敛抽象出来。第二，把工具作为有注册表、参数防护、并行调度和可追踪结果的运行时组件，而不是散落在 prompt 中：`runtime/agentic/tool_dispatch.py` 设置 `MAX_PARALLEL_TOOL_CALLS = 8`，每个调用产生子 trace，并处理未知工具、缺参、暂停和终止。第三，把记忆设计成可定位的分层持久化：`services/memory/paths.py` 明确 L1 trace、L2 per-surface summary、L3 cross-surface 文件及 backup。第四，把“能回答”与“能长期运营”同时纳入工程：FastAPI/Next.js、CLI、测试、容器、用户隔离、密钥边界、迁移和安全检查清单均有对应文件。

对学业军师的直接启示是：mate 应明确记录能力契约、工具权限、上下文和记忆边界、恢复协议、来源引用和验证门槛；junshi-app 应把 Agent 核心、工具/外部服务、知识与记忆、API、前端、配置、测试、部署、运行时数据分层，避免把产品定义、实现细节和运行数据混成一个目录。DeepTutor 不应被直接复制：依赖规模很大，模型/解析/RAG/IM/沙箱耦合成本高；其 Apache-2.0 只覆盖仓库许可，不自动覆盖全部第三方依赖、外部模型条款或用户数据处理义务。

## 二、官方身份与来源证据

### 2.1 仓库识别

**外部事实（已核验）**：GitHub 仓库搜索中，`HKUDS/DeepTutor` 是名称与定位都匹配的最高关注官方候选，描述为 “DeepTutor: Lifelong Personalized Tutoring. https://deeptutor.info/”。仓库 API 返回 `full_name=HKUDS/DeepTutor`、默认分支 `main`、许可证 `Apache-2.0`、创建时间 2025-12-28、最新推送 2026-09-02。README 顶部标题、文档入口 `https://deeptutor.info`、版本徽章和 Apache 2.0 徽章与上述元数据一致。

**版本定位（已核验）**：本报告源码证据均以提交 `93df3d48b70586c36b20ebf82c613a67ed20677` 的 GitHub 内容 API 为准，稳定链接格式为 `https://github.com/HKUDS/DeepTutor/blob/93df3d48b70586c36b20ebf82c613a67ed20677/<path>`。README 的 v1.6.4 发布条目写明 “Faster isolated runtimes, richer Books and Mastery flows, Reading/session polish, and explicit model API capabilities”。仓库 README 还挂有 arXiv `2604.26962` 徽章，但本次环境中直接访问 arXiv 的 Bash 请求被权限阻断，因此论文题名、章节和结论均不作为已核验依据；论文证据状态为**阻塞/待复核**，不能由徽章推断产品效果。

### 2.2 证据字段与状态

下表把仓库事实、来源自述、分析和本报告建议分开。G1-G5 为本次计划书要求的缺口映射：G1 产品/用户定位，G2 Agent 运行机制，G3 工具/模型/知识/记忆，G4 工程生命周期与部署，G5 对 mate/junshi-app 的结构启示。若某条不适用，明确标注。

| 编号 | 事实与原文定位 | 来源自身结论 | Claude 分析/建议 | 缺口、状态 |
|---|---|---|---|---|
| E1 | `README.md` 顶部标题及 Features/Get Started/CLI/Ecosystem 链接 | 项目自称长期个性化辅导平台 | 可作为学习 Agent 的产品范围入口，不代表学习效果已证明 | G1；已核验；候选参照 |
| E2 | `SKILL.md` “Prerequisites”和 Commands：Python 3.11+、`deeptutor init`、`chat/run/kb/partner/memory/session/notebook/serve/start` | 官方将 CLI 作为 agent-native interface | CLI 命令契约可降低 UI 外能力难以复现的问题 | G2/G4；已核验；候选参照 |
| E3 | `deeptutor/runtime/agentic/loop.py` 的 `LabelProtocol`、`LoopHost`、`run_agentic_loop` | 循环对能力无关，能力差异由 host 提供 | 适合将通用生命周期与学业能力分离 | G2；已核验；候选参照 |
| E4 | `deeptutor/runtime/agentic/tool_dispatch.py` 的 `MAX_PARALLEL_TOOL_CALLS=8`、`DispatchOutcome`、`PAUSE_LAST_TOOLS={"ask_user"}` | 工具调用并行且带子 trace；ask_user 最后处理 | 并行上限、暂停语义和调用级审计应成为运行时契约 | G2/G3/G5；已核验；候选参照 |
| E5 | `deeptutor/services/memory/paths.py` 注释及函数：`trace/<surface>/<date>.jsonl`、`L2/<surface>.md`、`L3/<slot>.md`、`backup/<timestamp>` | 官方明确三层记忆布局并支持 partner owner override | 记忆必须有层级、所有者和恢复/备份边界 | G3/G5；已核验；候选参照 |
| E6 | `pyproject.toml` `[project]`：`requires-python >=3.11,<3.15`；FastAPI、uvicorn、openai、anthropic、LlamaIndex、FAISS、MCP、Pydantic 等依赖及可选 fallback 注释 | 核心安装包含完整 Web/RAG 能力 | 功能丰富伴随供应链、编译包和版本矩阵风险 | G4；已核验；候选风险参照 |
| E7 | `CONTAINERIZATION.md` Overview：单容器 FastAPI `:8001` + Next.js `:3782`，`/app/data` 持久化；Podman rootless/read-only/tmpfs 方案 | 官方推荐前端同源代理，应用进程降权 | “单公开端口+内部 API”与读写数据树边界可借鉴 | G4/G5；已核验；候选参照 |
| E8 | `REASONING_SAFETY_CHECKLIST.md`：Lost constraints、Retrieval drift、Weak-evidence overconfidence、citation/locator mismatch 等 | 官方把不可靠回答诊断为 prompt/retrieval/context/product bug 的可区分问题 | 学业产品应把证据链和失败诊断纳入验收，而非只测文本流畅度 | G1/G3/G5；已核验；候选参照 |

## 三、产品定位、用户与场景

### 3.1 定位与能力边界

**事实**：README 以 “Lifelong Personalized Tutoring” 命名；`SKILL.md` 的可执行能力列表包括 `chat`、`deep_solve`、`deep_question`、`deep_research`、`visualize`、`math_animator`、`mastery_path`。同一文件将 Knowledge Bases、Partners、Skills、Books、Memory、Sessions、Notebooks、Providers 和 System 管理列为 CLI 一级对象。由此可确认其产品对象不止问答，而是“学习材料—辅导对话—练习/掌握—长期记忆—外部伙伴”的组合。

**来源自身结论与限制**：README 的发布说明是项目方自述功能变更，不是独立评测。比如“personalized”“lifelong”描述目标和产品方向，不能直接推导个性化准确率、学习成绩提升、可用性或规模指标。本报告将其标为产品定位事实，不写成效果事实。

**分析**：目标用户至少包括需要阅读资料、解题、生成问题、研究、可视化和掌握路径的学习者；管理员/部署者还要配置模型、搜索、存储和账户。对学业军师而言，最重要的场景切分是：即时答疑、基于指定材料的有据讲解、阶段练习、掌握状态更新、跨会话偏好记忆和家长/教师可审计的进展，而非盲目引入全部能力。

### 3.2 从功能到工程组件

DeepTutor 的目录树显示 `deeptutor/agents/` 下按能力组织 `chat`、`question`、`research`、`visualize`、`math_animator`、`notebook` 等；每个能力通常有 `capability.py`、`pipeline.py`、`request_config.py`、`prompts/` 或子 agent。`deeptutor/core/`（目录树中可见 `context`、`tool_protocol`、`trace` 相关导入）提供跨能力的上下文/工具/追踪协议；`deeptutor/runtime/` 负责运行时；`deeptutor/api/routers/` 提供 auth、attachments、book、capabilities、courses、memory 等路由；`web/app/` 按 workspace、utility、auth、admin 切分前端页面。这形成“领域能力—共享协议—运行时—API—前端”的分层，而非把所有逻辑放在一个 agent 文件中。

## 四、Agent 运行机制与数据流

### 4.1 通用循环

**源码事实**：`deeptutor/runtime/agentic/loop.py` 文件头注释规定每次迭代调用 `run_labeled_step`，随后校验协议；工具标签会追加 assistant/tool 消息并由 host dispatch；中间标签把文本保存为 assistant 上下文；协议违规会生成 retry notice 和 repair message；超过最大迭代数可 `force_finalize`。`LabelProtocol` 字段包括 `allowed`、`terminal`、`intermediate`、`final`、`tool_label`。`LoopHost` 则要求/允许能力提供 `guard_context_window`、`build_iteration_trace_meta`、`dispatch_tools`、`resolve_pause`、`emit_terminator`、`emit_final`、`validate_terminal`、`force_finalize`、`before_iteration`、`on_intermediate`。

**分析**：该机制把模型输出当作受协议约束的事件，而非任意字符串。能力可以共用“调用模型—解析标签—调用工具—继续/暂停/收敛”的骨架，同时在 host 中注入上下文预算、能力状态和 UI trace。对学业军师的价值是让 `答疑/诊断/练习/复习` 共享生命周期，但拥有不同的终止条件和证据要求。

### 4.2 工具调度与暂停

**源码事实**：`deeptutor/runtime/agentic/tool_dispatch.py` 导入 `asyncio`，定义 `MAX_PARALLEL_TOOL_CALLS = 8`；`DispatchOutcome` 包含 sources、tool messages、metadata、terminate/pause 状态。注释说明工具调用并行执行、每个调用产生独立子 trace；`PAUSE_LAST_TOOLS` 把 `ask_user` 延后，以便其问题卡绑定到已提交的状态。`tool_arg_guard` 提供缺失参数和不满足必需参数的提示，注册表来自 `runtime/registry/tool_registry.py`。

**分析**：这里有三条可复用边界：模型只提出调用，注册表决定可调用对象；服务端 augment context 负责补入 `source_index` 等不应由模型伪造的参数；调度器负责并行上限、错误和可观测性。不可直接照搬“8”这一数字，它依赖模型延迟、资源和工具副作用；junshi-app 应把并发上限作为配置和测试对象，并将写记忆、提交练习等有副作用工具与只读检索工具分级。

### 4.3 学习数据流

依据 `SKILL.md`，一次 CLI `run deep_research` 可指定 `--kb`、`--tool rag`、`--config mode=report`；`kb create/add/search` 管理资料；`memory show/clear` 管理长期上下文；`session` 可 list/show/open；`notebook add-md` 可保存结果。结合源码目录 `deeptutor/tools/rag_tool.py`、`web_search.py`、`paper_search_tool.py`、`read_source` 提示词和 `deeptutor/agents/research/utils/citation_manager.py`，可还原出候选数据流：用户请求进入 capability → loop 选择工具 → RAG/搜索/附件等产生 sources → 工具结果回到消息上下文和 trace → 能力输出带引用的答案/报告 → session/notebook/memory 持久化。此处调用顺序是架构推断，未运行端到端流程，标为**部分核验**。

## 五、记忆、知识与证据治理

### 5.1 三层记忆

`deeptutor/services/memory/paths.py` 的模块 docstring 是最直接证据：每个用户 memory root 下，L1 是 `trace/<surface>/<YYYY-MM-DD>.jsonl` 追加记录，L2 是 `L2/<surface>.md` 的按 surface 摘要，L3 是 `L3/<recent|profile|scope|preferences>.md` 的跨 surface 摘要，另有 `backup/<timestamp>/` 迁移归档。`Surface` 明列 chat、notebook、quiz、kb、book、partner、cowriter；`memory_path_service_override` 说明 partner turn 可临时读 owner 的 memory，同时其他服务仍保持 partner scope。

**分析**：L1 适合可追溯事件，L2 适合某个产品表面的工作上下文，L3 适合稳定偏好/画像；三者不能混写。owner override 是多租户系统中极易出错的权限点，必须有测试验证“可读哪些、不可读哪些、写入归属谁”。学业军师可借鉴层级和 surface 划分，但不应未经家长/学生同意把成绩、健康、家庭信息自动升级到 L3。

### 5.2 RAG 与证据

目录中有 `deeptutor/services/rag/pipelines/graphrag/`（config、engine、ingestion、storage、provider 等）、`services/rag` 其他 pipeline、`knowledge/manifest.py`、`tools/rag_tool.py` 以及 `agents/research/utils/citation_manager.py`。README 版本历史还明确提到 LlamaIndex RAG、FAISS、PageIndex、LightRAG、MinerU 等。**外部事实**是这些路径和依赖存在；**来源自身结论**是发布说明宣称相关能力；**本报告推断**是系统允许多种解析/检索后端并把引用作为研究输出的一部分，尚未验证每种 pipeline 的运行质量。

`REASONING_SAFETY_CHECKLIST.md` 对 Retrieval drift、stale source、chunk boundary split、over-broad top-k、missing rerank、conflicting sources、citation mismatch、locator mismatch、hallucinated evidence 逐项列出检查方式，并要求收集能力、模型、KB、工具参数、结果摘要和 citation IDs。该文档是很强的治理参照：学业军师应将“指定教材是否被使用”“引用位置是否支持陈述”“来源冲突是否显式呈现”写成测试与活动记录字段。

## 六、配置、模型、提示词与扩展

`SKILL.md` 规定 `deeptutor init` 以向导写入 `data/user/settings`，包括 ports、LLM、embedding、search 和 review；`config show` 查看解析后配置，`plugin list/info` 查看工具/能力。`pyproject.toml` 的依赖同时覆盖 OpenAI、Anthropic、DashScope、Perplexity、OAuth、LlamaIndex、FAISS、MCP、FastAPI、PocketBase、Redis 等，且对 BM25、FAISS、psutil 等注明条件安装或软依赖 fallback。`deeptutor/agents/*/prompts/en|zh/` 说明提示词按能力和语言放置，不把多语言规则全塞进 Python；`pyproject.toml` entry points 还注册 `deeptutor.reading_extensions` 的 read_aloud、guided_learning、vocabulary、quiz、translation。

**分析**：能力注册、工具注册、提示词资源和 provider 配置形成可扩展面；但扩展面越大，版本兼容、权限和供应链验证越重要。`skill install clawhub:...` 支持 `--allow-unverified`，这意味着“社区技能”必须独立审核，不能因为能安装就视为可信。对 junshi-app，建议把自有工具与第三方插件分层、默认拒绝高风险能力，并在 mate 记录每个扩展的输入、输出、网络、数据和回滚契约。

## 七、部署、生命周期与工程保障

### 7.1 启动与持久化

`SKILL.md` 提供三条入口：`deeptutor serve [--host --port --reload]` 启动 API，`deeptutor start [--home]` 启动后端和前端，`deeptutor init` 初始化 workspace。`CONTAINERIZATION.md` 说明发布镜像 `ghcr.io/hkuds/deeptutor` 在单容器内运行 FastAPI 8001 和 Next.js 3782，`supervisord` 管理进程，`/app/data` 保存 settings、workspaces、memory、knowledge bases、logs；浏览器只需访问前端端口，Next.js `/api/*` 和 `/ws/*` 在运行时代理至后端。硬化 Podman 方案使用 `userns_mode: keep-id`、read-only rootfs、tmpfs 和 `./data` bind mount；应用进程通过 supervisord 的 per-program `user=` 降为 `deeptutor`。

**分析**：单公开端口减少跨域与暴露面，数据树整体挂载避免重建丢失 auth secret、账户、workspace 等状态；但单容器仍把前端、后端和可能的代码执行信任边界放在一起。文档特别提醒 `sandbox_allow_subprocess=false` 可避免模型生成代码与 secrets 共享容器信任边界，这应被视为部署配置而非默认安全保证。

### 7.2 测试与维护

仓库树包含 `tests/api`、`tests/runtime/coordination`、`tests/book`、`tests/fixtures`，以及 `.github/workflows/tests.yml`、`docker-release.yml`、`pypi-release.yml`、`repository-hygiene.yml`。这证明项目把 API、运行时协调、Book、解析 fixture 和发布自动化纳入工程结构。`CONTAINERIZATION.md` 还记录数据挂载迁移：旧 Compose 只挂载部分 `data` 子树会导致 system（JWT secret/accounts/audit log）和 users 等在重建时丢失，升级前必须复制出来。

**分析**：可持续 Agent 的生命周期不止“启动成功”：需要 schema/数据迁移、恢复、索引重建、版本回滚和发布流水线。DeepTutor 的文档化迁移提醒尤其适合学业产品：成绩、学习轨迹和家长授权数据不能随容器重建消失；任何 schema 变更都要有备份、迁移前检查和回滚演练。

## 八、许可证、依赖、网络、隐私与供应链风险

1. **许可证**：GitHub API 和 `pyproject.toml` 均标 Apache-2.0，状态已核验；但本报告未逐项审计 `THIRD_PARTY_NOTICES.md` 或每个运行时插件的许可证。采用时必须复核第三方组件、模型服务和社区技能许可，不能把仓库许可证扩展到外部资产。
2. **依赖**：`pyproject.toml` 的依赖数量和范围较大，含编译/向量/文档解析包，且 Python 版本上限 `<3.15`。FAISS、LlamaIndex、MinerU、MCP 等升级可能改变行为；应锁定依赖、生成 SBOM、扫描漏洞并保留可回滚镜像。
3. **网络**：搜索、论文、GitHub、MCP、IM Partner、模型 provider 都可能出网；`CONTAINERIZATION.md` 的反向代理和 OAuth 临时回调说明了网络边界。学业军师要区分教材内检索、受控外部搜索和用户私有数据，默认不把学生资料发送给未知 provider。
4. **隐私与多租户**：记忆路径、workspace、账户、JWT secret、Codex token、audit log 均属于敏感状态。`memory_path_service_override` 体现 owner/partner 边界，但仅凭静态代码不能证明全链路隔离；必须本地验证越权读取、日志脱敏、删除和导出。
5. **工具/代码执行**：`exec_tool.py`、CLI Apps、MCP 和生成媒体扩大攻击面。`REASONING_SAFETY_CHECKLIST.md` 要求报告中去除密钥、路径、用户名和个人内容；`CONTAINERIZATION.md` 也强调 subprocess 信任边界。建议默认 deny、最小权限、超时/资源上限、人工确认和审计。
6. **回滚**：README 发布频率高，容器数据迁移又可能影响认证和索引。采用前应定义版本化 settings/schema、数据备份、索引重建和“应用版本—数据版本”兼容矩阵；不能仅依赖 `latest` 标签。

## 九、对 mate 与 junshi-app 的适配判断

### 9.1 对 mate 的候选启示

**候选建议（待产品发起人确认）**：在 mate 的 Agent 工程元文档中补齐一份“运行时契约”章节，至少定义：回合状态（开始、工具中、等待用户、完成、失败、恢复）、终止条件、最大迭代、上下文预算、协议违规修复和 trace 字段；再以“工具目录”登记每个工具的权限、输入来源、可否并行、副作用、网络、超时和回滚。新增“证据治理”章节，规定引用 locator、来源版本、冲突处理、空检索和过期索引行为；新增“记忆治理”章节，区分事件、表面摘要、稳定偏好，明确学生/家长所有权、保留期限、删除和人工确认。

mate 还应把“能力设计”和“实现方式”分开：`deep_solve` 等名称属于产品能力定义；标签 loop、Python 类、LlamaIndex 等属于实现参照；外部项目的“来源结论”只能进入设计参照/候选，不自动变成最终确认。每项采用建议应附适用前提、验证用例、失败处理和淘汰条件。

### 9.2 对 junshi-app 目录的候选启示

以本仓库现有 `apps/`、`runtime/`、`mate/`、`docs/`、`scripts/` 等为背景，建议只在规划层面评估如下边界（不在本次任务修改代码）：

- `runtime/agent/`：循环、状态机、上下文预算、恢复和 trace；不放学科业务 prompt。
- `runtime/tools/`：工具协议、注册表、权限/并发/超时/副作用策略；外部服务适配器另分层。
- `domain/learning/`：学习目标、练习、掌握状态、课程/材料模型；不把 UI 状态当领域真相。
- `services/knowledge/` 与 `services/memory/`：解析、索引、引用和三层记忆；每个结果保留 source/version/locator。
- `api/`、`web/`：明确请求契约、流式事件和鉴权边界；前端不得持有 provider secret。
- `config/`：schema、默认值、迁移、敏感字段处理；配置变更必须可审计。
- `tests/`：按协议、工具安全、来源引用、租户隔离、恢复、迁移和端到端场景组织，而不是只测页面。
- `deploy/`、`runtime-data/`、`scripts/`：镜像、Compose、备份/迁移/索引维护和本地开发脚本分开；运行数据不进 Git。

以上是与 DeepTutor 对照后的结构建议，不是对当前仓库结构的事实判定，也不授权本报告修改 `mate/` 或代码。

## 十、局限、未核验项与采用门槛

本次证据主要来自 GitHub 官方仓库在固定 commit 的 README、目录树、源码和部署文档。没有执行安装、模型调用、RAG 建库、用户注册、Partner、代码执行、容器启动或压力测试，因此不能确认性能、真实并发、故障恢复是否有效，也不能把目录存在等同于生产能力。GitHub README 的功能描述属于项目方自述；没有独立用户研究或学习效果实验。arXiv `2604.26962` 因网络工具阻塞未能核验，不能引用论文结论。某些目录（如 `core` 的具体实现、全部 auth middleware、所有 pipeline）只做了路径级确认，属于部分核验。

**采用门槛（候选/待复核）**：若 junshi-app 参考 DeepTutor，应先在本地建立最小垂直切片：一个学习能力、一个只读教材检索工具、一个带 locator 的回答、一个可恢复 session 和一条 L1→L2 记忆路径；通过越权、空检索、冲突来源、上下文超限、工具超时、进程重启和数据备份恢复测试后，才评估扩大到多 Agent、社区技能、代码执行、IM Partner 或多种 RAG。产品发起人仍需确认隐私等级、家长授权、模型 provider、部署形态和是否接受 Apache-2.0/第三方许可组合。

## 十一、外部研究与 Skill 使用记录

- 阶段：DeepTutor 外部仓库调查与独立报告
- 任务类型：GitHub 研究、源码取证、Markdown 写入
- 目标与成功标准：确认准确官方仓库；固定版本；覆盖定位、组件、目录、运行机制、配置、工具、记忆、模型、部署、测试、风险和对 mate/junshi-app 的启示；报告不少于 2500 字并只写目标文件。
- 能力发现：实际调用了全局 `agent-reach`、`md-writing`、`skill-first`；本地 `.claude/commands/research-evidence.md` 在当前 worktree 不存在，记录为阻塞，按用户计划书和 agent-reach 研究字段降级执行。
- 选择理由：GitHub 研究必须使用 agent-reach；Markdown 报告必须先调用 md-writing；skill-first 负责记录入口和验证。
- 实际调用：`agent-reach` Skill（返回路由与 GitHub `gh` 用法）；`md-writing` Skill（返回研究报告结构和事实/推断分离规则）；`skill-first` Skill（返回统一执行协议）。
- 协作 agent/工具/MCP：未调用其他 agent；实际工具为 `agent-reach doctor --json`、`gh search repos`、`gh api`、本地 `Read`/`Bash`/`Write`。doctor 显示 GitHub `gh CLI` 可执行但 active_backend 为 null（未实时验证认证）；未使用 Playwright，原因是本次固定 commit 的 API/源码读取已满足静态取证，且用户要求只读。
- 输入：`HKUDS/DeepTutor`、commit `93df3d48b70586c36b20ebf82c613a67ed20677`、README/SKILL/CONTAINERIZATION/REASONING_SAFETY_CHECKLIST、`deeptutor/runtime/agentic/*`、`services/memory/paths.py`、`pyproject.toml`、目录树和本地 `计划书`。
- 输出：`/Users/caibiao/orca/projects/junshi-app/.claude/worktrees/agent-a1a71f8fd06f12a70/调研报告/DeepTutor调查报告.md`。
- 阻塞/降级：`research-evidence.md` 在当前 worktree 未找到；arXiv URL 直接 Bash 请求被权限系统拒绝；未以记忆补写论文信息。降级为 GitHub 固定 commit 的一手仓库资料，并把阻塞显式标注。
- 未调用项及理由：Playwright 未调用（非必要，API 已可定位源码）；Context7 不适用（目标是仓库取证而非库 API 文档）；crawl4ai 不适用（未进行 JS 重页面抓取）。
- 验证：将执行 `wc -m` 确认字数、`git diff --check` 检查 Markdown 空白、`git status --short` 确认仅目标文件、`git diff --stat` 确认提交范围。未执行 DeepTutor 运行测试；外部事实仍以报告中的来源定位为准。

## 十二、来源索引

1. [官方仓库主页](https://github.com/HKUDS/DeepTutor)，访问日期 2026-09-03；仓库身份、许可证、默认分支。
2. [固定版本 README.md](https://github.com/HKUDS/DeepTutor/blob/93df3d48b70586c36b20ebf82c613a67ed20677/README.md)，访问日期 2026-09-03；标题、版本历史、能力入口、arXiv 徽章。
3. [固定版本 SKILL.md](https://github.com/HKUDS/DeepTutor/blob/93df3d48b70586c36b20ebf82c613a67ed20677/SKILL.md)，访问日期 2026-09-03；CLI、初始化、能力、工具、知识库、记忆和服务命令。
4. [固定版本 Agent loop](https://github.com/HKUDS/DeepTutor/blob/93df3d48b70586c36b20ebf82c613a67ed20677/deeptutor/runtime/agentic/loop.py)，访问日期 2026-09-03；`LabelProtocol`、`LoopHost`、迭代/恢复协议。
5. [固定版本 tool dispatch](https://github.com/HKUDS/DeepTutor/blob/93df3d48b70586c36b20ebf82c613a67ed20677/deeptutor/runtime/agentic/tool_dispatch.py)，访问日期 2026-09-03；并行上限、DispatchOutcome、暂停工具、参数防护和 trace。
6. [固定版本 memory paths](https://github.com/HKUDS/DeepTutor/blob/93df3d48b70586c36b20ebf82c613a67ed20677/deeptutor/services/memory/paths.py)，访问日期 2026-09-03；L1/L2/L3、surface、owner override、backup。
7. [固定版本 pyproject.toml](https://github.com/HKUDS/DeepTutor/blob/93df3d48b70586c36b20ebf82c613a67ed20677/pyproject.toml)，访问日期 2026-09-03；Python 版本、依赖、entry points。
8. [固定版本 CONTAINERIZATION.md](https://github.com/HKUDS/DeepTutor/blob/93df3d48b70586c36b20ebf82c613a67ed20677/CONTAINERIZATION.md)，访问日期 2026-09-03；容器、端口、数据持久化、rootless/read-only 和信任边界。
9. [固定版本 REASONING_SAFETY_CHECKLIST.md](https://github.com/HKUDS/DeepTutor/blob/93df3d48b70586c36b20ebf82c613a67ed20677/REASONING_SAFETY_CHECKLIST.md)，访问日期 2026-09-03；长程约束、检索漂移、证据和隐私安全诊断。
10. [仓库许可文件](https://github.com/HKUDS/DeepTutor/blob/93df3d48b70586c36b20ebf82c613a67ed20677/LICENSE)，访问日期 2026-09-03；Apache-2.0 原文（本次仅通过 API 元数据核验许可证，许可全文未逐段摘录）。

> **最终判断**：DeepTutor 是适合作为“完整 Agent 产品工程闭环”参照的候选项目，尤其适合参照循环协议、工具调度、分层记忆、引用治理、CLI/API 双入口和容器持久化；它不是学业军师的产品决策，也不是可无条件复制的技术栈。所有 mate/junshi-app 采用建议均保持“候选/待复核”，需本地实现和用户确认后才能升级状态。
