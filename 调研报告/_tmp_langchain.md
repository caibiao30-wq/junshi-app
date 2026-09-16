# LangChain / LangGraph Agent 开发官方指导摘录

- **研究范围**：仅使用 LangChain 官方文档、官方 GitHub 仓库和官方博客；重点是状态化 agent、持久化、checkpoint、状态管理、人机交互与多代理。
- **获取时间**：2026-09-14（本次抓取）。
- **证据等级**：下文标为“官方一手确认”的内容来自页面正文、官方仓库 README 或页面元数据；未能从页面直接确认的字段明确标注。

## 结论先行

LangGraph 的核心定位不是一套抽象的 agent 方法论，而是一个**可安装、可 import 的低层编排框架**：用图、节点、边和显式状态承载长时运行 agent；用 checkpointer 保存线程级 checkpoint，用 store 保存跨线程长期记忆，用 `interrupt` 暂停并通过恢复命令接入人工，用 LangSmith 做追踪/评估/部署配套。官方材料把“状态持久化、故障后恢复、人审、可观测性”视为生产 agent 的基础设施，而不是只依赖一次 LLM 调用的提示词技巧。

## 来源一：LangGraph Persistence 官方文档

### 来源信息

- **标题**：Persistence
- **组织**：LangChain（LangGraph 官方文档）
- **日期**：页面未标注发布日期；本次抓取日期为 2026-09-14
- **URL**：[docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- **关联官方源码/编辑入口**：页面指向 [langchain-ai/docs 的 persistence.mdx](https://github.com/langchain-ai/docs/edit/main/src/oss/langgraph/persistence.mdx)
- **状态**：官方一手确认（页面可访问并返回正文）

### 核心主张

1. 持久化使应用能超越单次 graph run 保存有用信息，适用于继续对话、被打断后恢复、故障恢复以及跨交互记忆。
2. 官方明确区分两个互补系统：
   - **checkpointer**：把 graph state 保存为 checkpoint；用于短期、线程范围的记忆，包括对话连续性、人机交互、time travel 和容错。
   - **store**：把应用定义的数据保存在 graph state 之外；用于长期、跨线程记忆，如用户偏好、事实和共享知识。
3. 常见应用同时使用两者：checkpointer 跟踪当前 thread，store 跟踪跨 thread 的持久信息。

### 定义/实现的 agent 要素

- **显式状态**：graph 的运行状态是可保存、可读取的对象，而不是隐含在模型上下文中的临时变量。
- **线程身份**：以 thread 维度组织连续运行；调用时配置 thread 标识以关联已有状态。
- **checkpoint**：在图执行过程中保存状态快照，支持中断后继续、失败恢复和历史检查。
- **checkpointer 注入**：构建 graph 后以 checkpointer 编译；官方 quickstart 展示 `InMemorySaver`，生产环境可换持久化实现。
- **store 注入**：以 store 保存跨线程的应用数据；与线程 checkpoint 的职责分离。
- **状态检查与时间旅行**：官方导航将“检查 thread state”和“time travel”列为 checkpointer 的用途；可在历史状态基础上检查、回放或分叉执行（具体 API 以 checkpointers 页面版本为准）。
- **子图边界**：子图有自己的 checkpoint namespace；父图未必立即看到子图的状态更新。跨图共享数据时，官方建议使用 Store，或配置子图写入父 checkpoint。

### 覆盖维度

| 维度 | 官方文档覆盖情况 |
|---|---|
| 多代理编排 | **未在本页展开**；只说明子图/跨图状态边界，不给出完整多代理策略 |
| 状态机/图编排 | **间接覆盖**：持久化对象是 graph state/checkpoint；图的节点编排不在本页系统说明 |
| 人工确认 | **覆盖为用途**：checkpointer 支持 human-in-the-loop；具体 `interrupt` API 应看专页 |
| 可回滚/可恢复 | **覆盖**：故障恢复、从保存状态继续、time travel；“回滚”的业务语义和副作用补偿不等同于自动数据库回滚 |
| 评估 | **本页未覆盖**；官方 README 将 LangSmith 指向 agent evals/observability |
| 数据本地化 | **未承诺**；只描述 persistence 抽象与内存示例，部署位置、加密、数据驻留需另查具体 saver/store/部署方案 |
| 确定性 | **未承诺**；保存状态不等于 LLM 输出确定或重放结果必然相同 |
| 商业推广 | **本页基本不涉及**；属于实现文档，不是商业宣传报告 |

### 适用对象与局限

- **适用对象**：需要跨请求/会话保存状态、长时运行、故障恢复、人审暂停或时间旅行调试的开发者。
- **局限**：这是可落地的框架文档，不是纯方法论；它告诉开发者如何组织 checkpoint/store，但不替开发者决定业务状态模型、权限策略、数据保留、幂等与副作用补偿。页面仅展示 `InMemorySaver`/`InMemoryStore` 级别的快速示例，生产持久化的数据库、运维、合规和成本需另行核验。

## 来源二：LangGraph 官方仓库 README

### 来源信息

- **标题**：LangGraph README（副标题：Low-level orchestration framework for building stateful agents）
- **组织**：LangChain Inc. / `langchain-ai/langgraph`
- **日期**：README 当前版本未标注文档发布日期；本次抓取日期为 2026-09-14
- **URL**：[github.com/langchain-ai/langgraph/blob/main/README.md](https://github.com/langchain-ai/langgraph/blob/main/README.md)
- **状态**：官方一手确认（官方仓库 `main` README 可访问）

### 核心主张

README 将 LangGraph 定义为“构建、管理和部署长时运行、状态化 agent 的低层编排框架”，并列出：

- **Durable execution**：可跨越故障并运行较长时间，自动从离开处恢复。
- **Human-in-the-loop**：执行任意时点检查和修改 agent state。
- **Comprehensive memory**：短期工作记忆与跨会话长期持久记忆。
- **LangSmith debugging**：追踪执行路径、状态转换和运行时指标。
- **Production-ready deployment**：面向长时、状态化 workflow 的部署基础设施。

README 还明确：LangGraph 可独立使用，也可与 LangChain 集成；更高层的 Deep Agents 建立在 LangGraph 之上；LangGraph 本身可不依赖 LangChain 使用。

### 定义/实现的 agent 要素

1. **低层 graph orchestration**：把 agent/workflow 表达为可组合的图式执行单元。
2. **状态化运行**：状态是长时运行和恢复的核心载体。
3. **持久化与恢复**：durable execution + checkpoint/persistence 体系。
4. **人机交互**：在执行中暂停、检查和修改状态。
5. **记忆分层**：短期工作记忆和跨 session 长期记忆。
6. **可观测性**：通过 LangSmith 查看轨迹、状态转换和指标，并进行 agent evals。
7. **生产部署**：与 LangSmith Deployment 等产品组合完成部署和扩展。
8. **生态分层**：LangGraph 是低层基础；LangChain 提供集成/可组合组件；Deep Agents 提供更高层 agent 能力。

### 覆盖维度

| 维度 | README 覆盖情况 |
|---|---|
| 多代理编排 | **未给出具体协议**；提到 Deep Agents 可使用 subagents，不能据此推导 README 已定义多代理算法 |
| 状态机/图编排 | **覆盖定位**：低层 orchestration framework；未展开完整状态机语义 |
| 人工确认 | **覆盖主张**：可在任意时点检查/修改状态；实现细节在 interrupts 文档 |
| 可回滚/可恢复 | **覆盖恢复**：durable execution 自动从离开处恢复；README 未把它承诺为事务式回滚 |
| 评估 | **覆盖入口**：LangSmith 用于 agent evals/observability；评估指标、数据集和门槛未在 README 定义 |
| 数据本地化 | **未覆盖** |
| 确定性 | **未覆盖/未承诺** |
| 商业推广 | **有**：列举生产部署、LangSmith Deployment、企业采用者；这些是生态/产品定位陈述，不是独立效果验证 |

### 适用对象与局限

- **适用对象**：希望自己控制 agent 状态、流程分支、恢复、人审与部署的工程团队。
- **局限**：README 是项目定位和入口，不是完整实现规范；“production-ready”是官方定位陈述，不能单独证明特定系统的可靠性、合规性或成本。它与纯方法论文件的差异最明显：需要安装 `langgraph` 并编写/编译 graph 才能使用，具体行为依赖版本、checkpointer/store 实现和部署环境。

## 可选补强：LangGraph Multi-Agent Workflows 官方博客

### 来源信息

- **标题**：LangGraph: Multi-Agent Workflows
- **组织**：LangChain 官方博客
- **发布日期**：2024-01-23（页面结构化元数据 `datePublished`）
- **最近修改**：页面结构化元数据显示 2026-04-17；该日期晚于本次研究日期（2026-09-14）并可由页面元数据确认
- **URL**：[www.langchain.com/blog/langgraph-multi-agent-workflows](https://www.langchain.com/blog/langgraph-multi-agent-workflows)（旧链接 [blog.langchain.com/langgraph-multi-agent-workflows](https://blog.langchain.com/langgraph-multi-agent-workflows/) 会规范化到该地址）
- **状态**：官方一手确认（官方页面可访问，标题/发布日期元数据可取到）；正文部分依赖页面渲染，个别段落未逐字核验

### 核心主张与实现要素

该文以 LangGraph 为载体，主张将复杂任务拆成具有独立 prompt、工具和职责的专门 agent，再用图连接它们。其重点是**显式控制 agent 间的信息流与执行顺序**，而不是让一个通用 agent 无边界地调用所有工具。文章展示的工作流思路包括：

- 专门化 agent：每个 agent 有独立角色、prompt 和工具。
- 图式连接：通过有向流程把 agent 串联、路由或循环。
- supervisor/路由式协调：由协调节点决定调用哪个专门 agent。
- agent 间协作：通过共享或转交上下文传递中间结果。
- 可扩展分解：把复杂任务拆成更小的可观测步骤。

### 覆盖维度

| 维度 | 官方博客覆盖情况 |
|---|---|
| 多代理编排 | **覆盖**：专门 agent + 图连接/路由/协调是文章主题 |
| 状态机 | **覆盖为图式工作流思路**；未等同于完整形式化状态机规范 |
| 人工确认 | **未在本次可核验正文范围确认** |
| 可回滚 | **未在本次可核验正文范围确认**；图可重跑不等于业务回滚 |
| 评估 | **未在本次可核验正文范围确认** |
| 数据本地化 | **未覆盖** |
| 确定性 | **未承诺**；显式流程提高可控性，但 agent/LLM 节点仍可能非确定 |
| 商业推广 | **低到中**：主要是技术架构介绍，不作为独立商业效果证据 |

### 适用对象与局限

- **适用对象**：需要把复杂任务拆成多个专门角色，并希望显式控制路由、上下文和流程的 LangGraph 开发者。
- **局限**：博客是架构示例/指导，不是完整 API 参考，也不是跨场景的性能或可靠性基准；不能据此补齐人工审批、事务回滚、评估门槛或数据驻留承诺。

## 未取到与未核验项

- **LangChain “State of AI Agents” 报告**：本次未纳入。未在限定的官方 docs/GitHub/blog 范围内快速取得可直接核验的正文或 PDF；按任务约束跳过，未继续死磕。
- **`interrupts` 专页完整正文**：直连页面抓取返回的可用正文不足以逐条核验具体 API 代码；因此本文只采用 Persistence 页和 README 对 human-in-the-loop 的明确主张，不把 `interrupt` 的具体参数、恢复命令、重复执行语义写成已确认事实。URL：[docs.langchain.com/oss/python/langgraph/interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)。
- **`checkpointers` 专页完整 API**：Persistence 页确认了 checkpointer 的职责，但本次未逐条核验 saver 的具体类、配置字段和版本差异；相关 API 不应脱离当前安装版本直接照抄。URL：[docs.langchain.com/oss/python/langgraph/checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers)。
- **多代理博客部分正文**：页面可访问且元数据可取，但本次抓取受页面 HTML/渲染影响，正文细节未全部逐字确认；上述“专门 agent + 图连接/路由/协调”只保留为高层主张，不扩展成未核验的架构清单。

## Skill 使用记录

- **阶段**：官方资料快速取证与报告写入
- **任务类型**：外部研究 + Markdown 写入
- **目标与成功标准**：取得一至两份 LangChain/LangGraph 官方一手来源，提取状态化 agent、持久化、checkpoint、人机交互、多代理及边界，并写入指定文件；失败来源按约束标注。
- **能力发现**：仓库项目 skill 以 `graphify` 为主；当前会话可调用全局/插件 skill 包含 `skill-first`、`agent-reach`、`research`、`md-writing`；context-mode MCP 实际可调用。未调用仓库 agent，因无需协作编码。
- **选择理由**：`agent-reach` 负责官方网页/GitHub 获取；`md-writing` 负责研究 Markdown 的证据分层与格式；context-mode 用于批量抓取并避免把大段 HTML 原文带入上下文。
- **实际调用**：`skill-first`（已调用，完成路由）；`agent-reach`（已调用，按官方 URL 范围取证）；`md-writing`（已调用，按研究文档骨架写入）。
- **协作 agent/工具/MCP**：使用 `mcp__plugin_context-mode_context-mode__ctx_batch_execute` 批量访问 5 个官方 URL 并索引结果；使用 `ctx_search` 提取 Persistence/README/博客要点；一次进一步批量抓取因安全策略阻止 `curl` 命令而未执行。
- **输入**：上述 docs.langchain.com、github.com/langchain-ai/langgraph、www.langchain.com/blog 官方 URL。
- **输出**：`/Users/caibiao/orca/workspaces/junshi-app/docs/调研报告/_tmp_langchain.md`
- **Markdown 专项**：已实际调用 `md-writing`；采用“结论 → 来源 → 要素 → 覆盖矩阵 → 适用对象/局限 → 未取到 → 记录”的结构。
- **阻塞/降级**：`interrupts`/`checkpointers`完整正文和 State of AI Agents 未快速取得足够可核验内容；未死磕，改为只写已确认的高层主张并明确未核验项。一次 `ctx_batch_execute` 的 `curl` 方案被安全策略拒绝，未绕过。
- **未调用项及理由**：`research` 未另行调用；已用用户明确要求的 `agent-reach` 完成同职责取证，避免重复。`crawl4ai` 未调用；目标页面无需建立爬虫管线，且已有官方页面直取路径。
- **验证**：已检查目标文件内容结构、来源 URL、日期与状态标注；未运行 `check_markdown.py`（当前执行窗口未再调用 shell 校验脚本）。
- **下一步**：如需逐条复制 `interrupt()`、`Command(resume=...)` 或具体 checkpointer API，应在指定 LangGraph 版本下重新取得并做版本化核验。
