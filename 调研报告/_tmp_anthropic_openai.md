# Anthropic 与 OpenAI 官方 Agent 构建指南 — 快速调研报告

> 依据 `.claude/commands/research-evidence.md` 字段协议整理。`已核验`指直接取自官方原文；`部分核验`指原文只覆盖相关侧面；`阻塞`指未从来源取得。获取时间均为 2026-09-14。G1–G5 的精确含义未在当前 worktree 中核验，故不擅自映射；相关项标为“G1–G5：待主 Agent 映射”。

## 来源与证据表

| 状态 | 来源类型 | 标题/组织 | 日期/版本 | 稳定 URL | 实际访问 |
|---|---|---|---|---|---|
| 已核验 | 官方工程文章 | *Building effective agents* / Anthropic | Published Dec 19, 2024 | https://www.anthropic.com/engineering/building-effective-agents | 2026-09-14；agent-reach web/Jina Reader，全文 21 节 |
| 已核验 | 官方 PDF 指南 | *A practical guide to building agents* / OpenAI | PDF 未标明发布日期或版本 | https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf | 2026-09-14；agent-reach web/Jina Reader 取 PDF，pypdf 提取 34 页 |

> 访问失败处理：直接 WebFetch 对两域名均因安全策略无法验证；按用户要求未超过 3 次。随后 agent-reach 的 Jina Reader 成功取得 Anthropic 页面与 OpenAI PDF；OpenAI PDF 初始为二进制，改用隔离 venv 的 `pypdf` 提取成功。因此最终来源不是“未取到”。

## 一、Anthropic：Building effective agents

**组织/日期/URL**：Anthropic；2024-12-19；https://www.anthropic.com/engineering/building-effective-agents。获取时间 2026-09-14。**状态：已核验；候选/参照。**

### 核心主张与原文定义

- 原文建议从最简单方案开始，只在需要时增加复杂度；Summary 的表述是：“Success in the LLM space isn't about building the most sophisticated system. It's about building the right system for your needs.” [Anthropic URL；获取 2026-09-14；已核验]
- **Workflow**：LLM 与工具通过“predefined code paths”编排。
- **Agent**：LLM 动态指挥自己的过程与工具使用，保持完成任务方式的控制。
- **Augmented LLM**：用 retrieval、tools、memory 增强的 LLM；模型可生成搜索查询、选择工具并决定保留哪些信息。
- **Routing**：将输入分类并导向专门的后续任务。
- **Parallelization**：`sectioning`（独立子任务并行）与 `voting`（同一任务多次运行以获得多样输出）。原文示例包括将 guardrail 与主响应分开，以及自动化 eval。
- **Orchestrator-workers**：中央 LLM 动态拆解任务、委派 worker LLM 并综合结果；子任务不预先定义，而由 orchestrator 按输入决定。
- **Evaluator-optimizer**：一次 LLM 生成，另一次提供评估和反馈，循环迭代；适合有清晰评价标准且迭代有可测收益的任务。
- **Agents**：从人的命令或对话开始，独立规划和操作；从环境每一步取得 ground truth（工具结果或代码执行）评估进度；可在检查点或阻塞处暂停等待人工反馈；应设置最大迭代等停止条件。

### 目标维度覆盖

| 维度 | 结论、原文定位与状态 | G1–G5 |
|---|---|---|
| 多代理编排 | **已核验/部分覆盖**：明确 Orchestrator-workers；未见平级 handoff 的定义。原文标题“Workflow: Orchestrator-workers”。 | 待主 Agent 映射 |
| 状态机 | **未覆盖/阻塞**：没有“state machine”实现或术语；只有预定义路径、循环与停止条件。 | 待主 Agent 映射 |
| 人工确认 | **已核验**：agent 可在 checkpoints 或 blockers 处暂停以获得 human feedback。 | 待主 Agent 映射 |
| 可回滚 | **未覆盖/阻塞**：没有 rollback、恢复快照或事务补偿机制；沙盒测试不是回滚实现。 | 待主 Agent 映射 |
| 评估 eval | **已核验**：强调 comprehensive evaluation；parallelization 示例包含 automated evals；Evaluator-optimizer 要求清晰评价标准。 | 待主 Agent 映射 |
| 数据本地化 | **未覆盖/阻塞**：提 retrieval/tools/memory 与 MCP，但未规定驻留区域或本地部署。 | 待主 Agent 映射 |
| 确定性 | **未覆盖/阻塞**：未给确定性保证；明确提醒自主性带来更高成本与 compounding errors。 | 待主 Agent 映射 |
| 商业推广 | **已核验/部分覆盖**：客户支持与 coding agent 实践；客服案例提按 successful resolution 收费的 usage-based pricing。不是完整商业推广方案。 | 待主 Agent 映射 |

### 适用对象与局限

- **适用对象（已核验）**：构建生产级 LLM 应用/agent 的工程与产品团队；尤其需要在简单 prompt、workflow、自主 agent 间做复杂度权衡者。
- **局限（已核验）**：文章是模式与经验指南，不提供状态持久化、回滚、数据驻留、确定性 SLA 的工程规范。原文建议自主 agent 在 sandbox 中广泛测试并配 guardrails。
- **许可、依赖、部署、网络、隐私、供应链、回滚风险（来源事实与未核验分开）**：文章页面未在所取正文中给出软件许可证、完整依赖清单、部署拓扑、网络隔离、数据处理条款或供应链审计要求（**未核验/阻塞**）。文中提 MCP 作为工具接入方式，属于依赖/网络边界提示，不等于本地部署保证（**已核验事实；适配推断待复核**）。

## 二、OpenAI：A practical guide to building agents

**组织/日期/URL**：OpenAI；日期/版本未标；https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf。获取时间 2026-09-14。**状态：已核验；候选/参照。**

### 核心主张与原文定义（页码为 PDF 页码）

- Agent 是“systems that independently accomplish tasks on your behalf”（p.4）；workflow 是满足用户目标必须执行的步骤序列（p.4）。不控制 workflow 执行的简单 chatbot、单轮 LLM、sentiment classifier 不属于 agent（p.4）。
- Agent 用 LLM 管理 workflow 与决策，识别完成、需要时纠正；失败时可停止并把控制权交回用户（p.4）。Agent 通过工具与外部系统交互，并按当前 workflow state 动态选择工具、在 guardrails 内运行（p.4）。
- **Single-agent systems**：单一模型配工具和指令，在 loop 中执行 workflow（p.13–15）。run 的常见退出条件是工具调用、结构化输出、错误或最大轮数（p.14）。
- **Multi-agent systems**：workflow 执行分布到多个协调 agent（p.13）。两类：**Manager / agents as tools**（中央 manager 通过 tool calls 协调专门 agent）与 **Decentralized / agents handing off**（对等 agent 依据专长 handoff）（p.17–18）。文中将 agent 建模为图节点；manager 的边是 tool calls，decentralized 的边是 handoffs（p.17）。
- **工具**：Data、Action、Orchestration 三类（p.9–10）；工具应标准化、文档充分、经过测试并可复用（p.9）。
- **Guardrails**：分层防御，包括 relevance/safety classifier、PII filter、moderation、tool safeguards、规则保护（正则/黑名单/输入长度）与 output validation（p.24–27）。工具按只读/可逆性/权限/财务影响评估风险，高风险可暂停检查或升级人工（p.26）。
- **Human intervention**：早期部署尤其重要；两类触发为超过失败/重试阈值，或高风险、敏感、不可逆动作（如取消订单、大额退款、付款）（p.31）。
- **模型与 eval**：先用最强模型建立性能基线，再以 eval 判断较小模型能否达到准确率目标并优化成本/延迟（p.8）。

### 目标维度覆盖

| 维度 | 结论、原文定位与状态 | G1–G5 |
|---|---|---|
| 多代理编排 | **已核验/强覆盖**：single-agent、manager、decentralized；含图、tool call、handoff 与 SDK 示例（p.13–19）。 | 待主 Agent 映射 |
| 状态机 | **部分核验**：未使用“状态机”术语；run loop、退出条件及 handoff 时传递 latest conversation state（p.14–15、p.20 左右）提供状态控制的相关概念。 | 待主 Agent 映射 |
| 人工确认 | **已核验/强覆盖**：失败阈值与高风险动作两类人工介入（p.31）。 | 待主 Agent 映射 |
| 可回滚 | **未覆盖/阻塞**：工具风险中提 reversibility，但未规定快照、事务回滚或补偿流程（p.26）。 | 待主 Agent 映射 |
| 评估 eval | **已核验**：p.8 明确“Set up evals to establish a performance baseline”；单 agent 的好处包含简化 evaluation（p.14）。 | 待主 Agent 映射 |
| 数据本地化/隐私 | **部分核验**：guardrails 覆盖 data privacy risks、system prompt leak 与 PII filter（p.24、26）；未规定数据驻留、区域或本地部署。 | 待主 Agent 映射 |
| 确定性 | **部分核验**：规则型保护被定义为 simple deterministic measures（p.27）；这不是整体 agent 行为确定性保证。 | 待主 Agent 映射 |
| 商业推广 | **已核验/部分覆盖**：面向 product and engineering teams，提 customer deployments 与 production；结论强调 real business value（p.3、32）。未提供定价、销售或市场进入方案。 | 待主 Agent 映射 |

### 适用对象与局限

- **适用对象（已核验）**：探索构建第一个 agent 的产品与工程团队（p.3）；已有 OpenAI Agents SDK 的团队可直接参照示例。
- **局限（已核验）**：与 OpenAI Agents SDK 的 `Runner.run()`、guardrail、handoff 等概念绑定；不是跨供应商标准。未提供完整状态机、持久化、回滚、数据驻留或确定性工程保证。
- **许可、依赖、部署、网络、隐私、供应链、回滚风险**：PDF 未在所取正文中给出许可证、完整依赖清单、部署拓扑、网络隔离、数据驻留或供应链审计条款（**未核验/阻塞**）。明确要求 guardrails 与 authentication/authorization、access controls、安全措施配合（p.24），可作为安全控制建议，但不等于完成安全审计（**已核验事实；适配推断待复核**）。

## 三、适配判断与风险（Claude 推断；候选建议，待本地验证和用户确认）

1. 若本仓库缺口涉及**多代理编排、人工确认、eval**，两份官方资料均可作**候选/参照**；OpenAI 对 manager、decentralized、风险评级与人工升级写得更可执行，Anthropic 对简单性、ground truth、检查点和复合错误风险的边界提醒更明确。
2. 若缺口涉及**状态机、可回滚、数据本地化、确定性**，两份资料都不足，不能据此做产品决策；状态机/回滚/驻留/确定性需要另行查找规范或实现级一手资料。
3. 两份资料都是厂商官方指导，存在供应商绑定、模型行为变化、API/SDK 版本变化和外部工具网络依赖风险；在本仓库采用前，需本地验证许可证、依赖锁定、部署网络、隐私边界、失败恢复、成本/延迟和 eval 基线。
4. **不适用/淘汰条件**：若需求必须提供可证明确定性、强数据驻留或事务级回滚，本报告不能作为充分证据，应标为**待复核**而非采用。

## 证据、状态与调用记录

- **外部事实**：上文标“已核验”的定义、模式、页码与引文，均来自两份官方 URL，访问日 2026-09-14。
- **来源自身结论**：Anthropic 的“简单优先/透明/工具文档测试”、OpenAI 的“先单 agent、按需多 agent、分层 guardrails、生产中人工介入”均明确标为来源结论。
- **Claude 推断**：第三节适配判断、风险和 G1–G5 待映射声明均不是来源结论。
- **本地验证与用户确认**：尚未验证本仓库 G1–G5 的定义、现有实现、许可证兼容性、部署网络、数据处理、回滚可行性或性能 eval；均需主 Agent/用户确认。
- **工具调用**：`agent-reach` skill；`agent-reach doctor --json`（确认 web active_backend=Jina Reader）；`ctx_fetch_and_index`（两 URL）；`ctx_search`（Anthropic 定向检索）；`pypdf`（OpenAI PDF 34 页文本提取）；`Bash` 的 `grep/sed`（只读定位）。未执行来源页面中的任何嵌入指令，未披露密钥/个人数据。
- **文件写入状态**：已写入当前隔离 worktree 的 `/Users/caibiao/orca/projects/junshi-app/.claude/worktrees/agent-aa36fb8a8cd4e954f/调研报告/_tmp_anthropic_openai.md`。因当前 agent 的 worktree 隔离策略，无法直接写入用户指定的共享路径 `/Users/caibiao/orca/workspaces/junshi-app/docs/调研报告/_tmp_anthropic_openai.md`；这是环境阻塞，未提交任何 commit。
