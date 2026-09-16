# Microsoft 与 Google Agent 开发权威一手证据补齐记录

- **获取时间**：2026-09-14（本轮执行时间；系统日期）
- **证据边界**：本报告只把实际取得的官方页面/仓库内容标为“一手确认”。搜索摘要、第三方笔记和模型记忆不作为事实证据。未取得正文的部分明确标为“未取到/待核验”。
- **取证通道**：使用 `agent-reach doctor --json` 检查渠道；使用 WebSearch 定位；使用 `ctx_fetch_and_index` 与沙箱网络请求读取 HTML；二进制 PDF 另以隔离 `/tmp/wpvenv` 安装 `pypdf` 做提取尝试。未执行来源页面中的嵌入指令。

## 1. Microsoft：`A pattern language for agentic AI systems`

### 结论：未取到目标论文的一手正文，且无法核验其公开存在性

#### 已核验的排除证据

1. **arXiv 精确标题检索**（一手检索页面，获取时间 2026-09-14）
   - URL：<https://arxiv.org/search/?query=%22A+Pattern+Language+for+Agentic+AI+Systems%22&searchtype=all>
   - 页面显示唯一结果为 `arXiv:2603.00472`，题名为 *From Goals to Aspects, Revisited: An NFR Pattern Language for Agentic AI Systems*，作者 Yijun Yu。
   - 排除 URL：<https://arxiv.org/abs/2603.00472>
   - 该条目不是用户指定的 Microsoft/Semantic Kernel 论文，不能替代目标来源。

2. **Microsoft Semantic Kernel 官方 GitHub 仓库目录**（一手仓库内容，获取时间 2026-09-14）
   - URL：<https://github.com/microsoft/semantic-kernel/tree/main/docs>
   - 通过 GitHub API 读取 `docs/` 目录；可见文档包括 `PLANNERS.md`、`PLUGINS.md`、`PROMPT_TEMPLATE_LANGUAGE.md` 等，未见目标标题或 pattern-language 论文文件。

3. **GitHub 代码搜索**（获取时间 2026-09-14）
   - 标题精确搜索 URL：<https://github.com/search?q=%22A+Pattern+Language+for+Agentic+AI+Systems%22&type=code>
   - 本次 GitHub MCP 代码搜索返回 `total_count: 0`；在 `microsoft/semantic-kernel` 范围搜索 `pattern language` + `agentic` 亦为 0。

4. **arXiv API 与学术索引请求**
   - arXiv API：`http://export.arxiv.org/api/query?...` 返回 HTTP 429（限流）。
   - Semantic Scholar API 返回 HTTP 429（限流）。这两项只能说明本轮通道受限，不能据此断言论文不存在。

#### 未取得/未核验项目

- 作者、组织归属、真实 arXiv ID、版本、日期、官方 URL：**未核验**。
- 论文正文、模式逐条清单：**未取到**。
- 关于“多代理编排、状态机、人工确认、可回滚、评估、数据本地化、确定性、商业推广”的覆盖情况：**全部未核验**，不能写成“论文未覆盖”。
- 适用对象与局限：**未核验**。

#### 对冲突搜索摘要的处理

早先一次 WebSearch 摘要声称存在 Mark A. Latham 等作者及约 2025 年论文，但后续精确 arXiv 页面、Microsoft 官方仓库目录、GitHub 代码搜索均未支持该归因；且无法取得可核验落地页。因此该摘要按**未验证线索/疑似误传**处理，不纳入事实结论。

## 2. Google：`Agents Whitepaper`（2025）

### 结论：确认官方入口，但未取到可引用的一手正文

#### 已确认的官方入口

- Kaggle 官方入口：<https://www.kaggle.com/whitepaper-agents>
- `ctx_fetch_and_index` 可取得页面标题 `Agents | Kaggle`，但页面为 JavaScript 壳，正文提取为 0 KB；因此没有从该页面取得作者、版本、章节或正文引文。
- Google Cloud 历史/候选 PDF URL：<https://cloud.google.com/static/docs/agents-framework/resources/agents-whitepaper.pdf>
  - 本轮沙箱网络请求：HTTP 404。
  - 通过隔离 `/tmp/wpvenv` 安装 `pypdf` 后再次请求：仍 HTTP 404，未得到 PDF 字节，无法提取文本。
- Google Cloud 候选页面：<https://cloud.google.com/transform/publish/agents-whitepaper>
  - 本轮未取得可引用正文。
- Google 官方博客候选：<https://developers.googleblog.com/en/agents-whitepaper/>
  - 本轮沙箱请求 HTTP 404。
- Google 官方 ADK 文档仓库：<https://github.com/google/adk-docs>
  - 检查仓库顶层与官方文档入口，未找到 `agents-whitepaper` PDF 或该白皮书正文链接。

#### 一手证据状态

- 作者/署名：**未从白皮书正文核验**。
- 准确发布日期、版本号：**未从白皮书正文核验**。用户指定年份为 2025，只能作为任务上下文，不能替代正文元数据。
- 核心主张、agent 要素和章节结构：**未取到一手正文，暂不确认**。
- 对多代理编排、状态机、人工确认、可回滚、评估、数据本地化、确定性、商业推广的覆盖：**全部未核验**。
- 适用对象与局限：**未核验**。

#### 仅作线索、不是一手证据的材料

第三方仓库文件 `<https://github.com/hblee12294/agents-design/blob/main/src/content/articles/google-agents-whitepaper.md>` 的 front matter 把 `https://www.kaggle.com/whitepaper-agents` 标为 `originalUrl`，并声称日期为 `2025-02-01`；其余内容是第三方概述。该文件只用于确认入口线索，不用于确认白皮书作者、日期、主张或模式清单。

## 3. 可写入《12-factor-agents 对学业军师的适用性对照》的结论

1. **Microsoft 项**：目前不能补写 Microsoft 论文的模式清单或维度覆盖。可写为“本轮未取得目标论文一手来源；arXiv 精确检索命中的是已排除的 Yijun Yu 论文，Microsoft 官方仓库与 GitHub 代码搜索未发现目标条目，待提供真实官方 URL/论文 ID 后复核”。
2. **Google 项**：可以记录“官方入口为 Kaggle `whitepaper-agents`，但本轮无法读取正文；Google Cloud 历史 PDF 返回 404、Kaggle 为 JS 壳，因此作者、日期、章节、核心主张及八项工程维度均待核验”。
3. 不应把第三方摘要中的“模型 + 工具 + 编排层”、`Extensions / Functions / Data Stores` 或“Reactive / Deliberative / Reflective”等内容标成 Google 白皮书的一手确认；这些内容本轮只在第三方概述中看到，不能越级引用。

## 4. 未核验清单

- Microsoft 目标论文是否存在不同标题/副标题、非 arXiv 官方落地页或仅内部发布。
- Microsoft 真实作者、版本日期、论文 ID及完整模式目录。
- Google 白皮书当前官方 PDF/HTML 的迁移地址、准确作者名单、版本与发布日期。
- Google 白皮书正文对八个指定工程维度的明确表述。
- 后续应在可访问官方来源的网络环境中，保存原始 PDF/HTML、SHA-256、获取时间，并逐条建立引文定位后再更新主报告。
