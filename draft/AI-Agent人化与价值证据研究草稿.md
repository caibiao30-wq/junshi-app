# AI Agent 人化与价值证据研究草稿

> **研究草稿／不构成产品决策**
>
> 研究状态：**已按用户要求暂停**。本文只合并暂停前已获得并做过基本来源核对的结果；没有把尚未读完全文的论文摘要、搜索结果或作者主张写成确定结论。
>
> 截止：2026-08-20

## 0. 先给结论

### 对两个待验证命题的判断

1. **“越趋向于人，产品越优秀”——不成立为一般规律；目前只能得到条件性、局部支持。**
   - 在低风险、短时、服务型聊天场景中，人化线索（人名、语言风格、社会性表达、外观等）经常提高**感知社会临场感**，并可能提高情感连接、主观信任、满意度或使用意向。
   - 这类研究大多测的是自报告感知和态度，不等于事实正确率、学习效果、长期留存或最终用户价值。
   - 已核对的 Araujo 研究中，人化线索对公司态度和满意度并非普遍显著；对情感连接的作用主要经由社会临场感出现。由此不能推出“所有维度一起变好”。
   - 信任研究还显示：让人更愿意相信系统，不等于让人更会识别系统何时错误。过度依赖可能上升，主观喜欢与客观协作表现可能相反。

2. **“20% 人化撬动 80% 价值”——没有找到可验证的定量证据；应视为产品比喻或待验证假设，不能写成事实。**
   - “20%”没有明确分母：是界面线索、对话风格、记忆能力、社会临场感，还是研发投入？
   - “80% 价值”也没有明确指标：满意度、信任、学习迁移、成绩、留存、家长感知，还是商业收入？
   - 截止暂停时，没有找到对 AI Agent“人化程度—价值产出”做剂量反应、边际收益或 80/20 分解的原始实验。

### 对《学业军师产品元文档》的最克制启示

可转化的不是“做得更像人”，而是：**在不伪装成人的前提下，提供适度的社会临场感、连续理解和有边界的主动指导；同时把校准信任、学生主体性和可观察的学习结果放在比拟人化更高的位置。**

这句话是**产品设计判断**，不是某一篇论文的直接结论。

---

## 1. 证据纪律与检索范围

### 1.1 本文使用的标签

- **事实证据**：原始论文、作者/大学页面、顶会论文页面或研究机构报告中明确报告的研究对象、方法和结果。
- **作者观点/解释**：论文作者对机制、外推或设计意义的解释；不等同于跨场景事实。
- **产品设计判断**：结合本项目目标提出的取舍，不冒充研究结论。
- **[待核验]**：只拿到标题、摘要或搜索片段，尚未读完方法与结果，不能据此下强结论。
- **[未找到证据]**：本轮检索没有找到足够原始证据，不表示该命题已经被证明为假。

### 1.2 检索与限制

本轮使用了 agent-reach 的后端体检与 Exa 技术/网页搜索，并尝试 Firecrawl。Firecrawl Search/Scrape 返回 402/额度不足；随后使用公开的 arXiv、大学存档、NBER、Science、DOI 页面和 Exa 返回的原始论文摘要/片段交叉核对。部分出版商页面受 403 或网络超时影响，因此下面明确标注“摘要级”或“待核验”。

本轮没有使用 X/Twitter 作为核心证据，也没有把产品宣传、博客或社交媒体观点当作研究结果。

---

## 2. 已完成核验的核心来源

### 2.1 Araujo (2018)：聊天机器人人化线索、社会临场感与公司感知

**来源**

- T. Araujo, *Living up to the chatbot hype: The influence of anthropomorphic design cues and communicative agency framing on conversational agent and company perceptions*, *Computers in Human Behavior* 85 (2018), 183–189。
- [UvA-DARE 作者/大学存档](https://dare.uva.nl/id/c2ecbc88-290d-44bf-8f63-6f7832abe802)
- [全文 PDF（阿姆斯特丹大学存档）](https://pure.uva.nl/ws/files/25443263/Living_up_to_the_chatbot_hype.pdf)
- [DOI / 出版来源](https://doi.org/10.1016/j.chb.2018.03.051)

**研究对象与方法（事实证据）**

- 使用当时技术可运行的实际聊天机器人，而非只给被试看静态概念图。
- 采用 `2（人化/非人化代理）× 2（智能框架/中性框架）` 的组间实验。
- 被试被要求仿佛在 Facebook Messenger 中与代理交互，完成一个虚构鲜花订单的地址修改；论文片段报告问题解决率约为 91%，并将问题是否解决作为协变量。
- 比较了人化感知（mindful / mindless anthropomorphism）、社会临场感，以及对公司的态度、满意度和情感连接。

**主要发现（事实证据）**

- 人化线索提高了被试对代理的 mindful 和 mindless anthropomorphism 感知。
- 人化代理与“智能”介绍框架的组合，社会临场感更高。
- 人化线索对“对公司的情感连接”有显著作用；社会临场感是其中的重要中介。
- 对公司态度和满意度，论文报告的总效应/中介效应并不普遍显著；至少不能概括为所有下游指标都提升。

**局限**

- 任务是一次性的、低风险的客户服务场景，结果主要是即时感知和态度，不能直接外推到长期学习、规划或高风险建议。
- 研究操纵的是外显线索与介绍框架，不是一个可连续测量的“人化百分比”；无法支持 20/80 或单调递增规律。
- 研究结果更接近“社会临场感影响服务体验”，不是“系统能力变强”。

**对命题的意义**

- **支持的较弱命题**：人化线索可以改变用户如何感知代理，并在特定服务场景中增加社会临场感和情感连接。
- **不支持的强命题**：人化越多，产品客观上越优秀；人化必然提高满意度、正确率或长期价值。

---

### 2.2 “Someone out there?”：人化语言、社会临场感与信任/满意度（摘要级核验）

**来源**

- *Someone out there? A study on the social presence of anthropomorphized chatbots*, *Computers in Human Behavior*。
- [DOI](https://doi.org/10.1016/j.chb.2022.107513)

**研究对象与方法（摘要级事实证据）**

- 摘要报告了三个实验。
- 通过人化的语言线索诱发不同程度的聊天机器人拟人化，并考察客户—聊天机器人互动。
- 结果变量包括信任、购买意向、口碑意向和购物体验满意度；社会临场感被作为潜在中介。

**主要发现（摘要级事实证据）**

- 摘要报告人化对信任、购买意向、口碑和满意度有正向影响。
- 摘要报告社会临场感是这些效应的中介机制。
- 摘要称这些效应在享乐型/功利型购物情境以及是否披露敏感信息的条件下仍较稳健。

**局限**

- 本轮只核对到出版物摘要级信息，尚未核对完整样本、操纵检查、效应量、统计模型和实验材料。
- 仍是购物/服务情境，不能外推到学业军师，也不能区分短期好感和长期信任校准。

**状态**：**已纳入“摘要级证据”，不是全文级完成核验**。

---

### 2.3 Buçinca、Malaya、Gajos (2021)：信任不是越高越好，关键是减少过度依赖

**来源**

- Z. Buçinca, M. B. Malaya, K. Z. Gajos, *To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI in AI-assisted Decision-making*, CSCW 2021。
- [arXiv 全文/摘要](https://arxiv.org/abs/2102.09692)
- [Harvard 作者/研究页面](https://eecs.harvard.edu/~kgajos/papers/2021/bucinca2021trust.shtml)
- [ACM DOI](https://doi.org/10.1145/3449287)
- [作者 PDF](https://zbucinca.github.io/assets/pdf/publications/bucinca2021trust.pdf)

**研究对象与方法（事实证据）**

- 199 名参与者的实验；论文摘要及全文说明参与者来自 Amazon Mechanical Turk。
- 比较三种认知强制干预、两种简单可解释 AI 方案和无 AI 基线。
- 任务要求参与者在 AI 建议可能正确或错误时做选择，研究“是否盲目接受错误建议”以及最终客观表现。

**主要发现（事实证据）**

- 认知强制干预相较简单解释方案显著减少了对错误 AI 建议的过度依赖。
- 最能减少过度依赖的设计，主观上更难、更不受偏好、也更不被信任；论文明确报告了有效性与可接受性之间的权衡。
- 干预没有完全消除过度依赖；某些情况下人机团队仍不如单独的 AI。
- 高 Need for Cognition（更愿意投入认知努力）的参与者平均受益更多，提示交互设计可能造成群体差异。

**局限**

- 这是模拟的 AI 辅助决策任务，不是长期真实工作或教育现场。
- 研究操纵解释与认知过程，不是拟人化；它不能直接证明“人化会导致过度信任”，但能证明“更喜欢/更信任的界面不必然带来更好的协作表现”。
- 用户主观信任、正确依赖和客观结果是不同指标，不能混为一个“信任分”。

**对命题的意义**

- 对“越人化越优秀”的反证性提醒：如果人化提高了未经校准的信任，可能反而扩大错误建议的影响。
- 对产品方向的直接启示是：目标应为**适当依赖/信任校准**，而非把信任分数做高。

---

### 2.4 Noy、Zhang (2023)：通用聊天工具带来生产力收益，但没有证明人化是原因

**来源**

- S. Noy, W. Zhang, *Experimental evidence on the productivity effects of generative artificial intelligence*, *Science* 381 (2023), 187–192。
- [Science DOI 页面](https://doi.org/10.1126/science.adh2586)
- [MIT 作者工作论文 PDF](https://economics.mit.edu/sites/default/files/inline-files/Noy_Zhang_1.pdf)
- [OSF 数据与代码记录](https://osf.io/xd7qw/?view_only=b8dac58dd6f44b979bf81069022fa392)
- [PubMed 摘要](https://pubmed.ncbi.nlm.nih.gov/37440646/)

**研究对象与方法（事实证据）**

- 预注册在线实验，把职业相关、带激励的中等复杂度写作任务随机分配给是否可使用 ChatGPT 的组。
- Science/PubMed 摘要报告 453 名受过大学教育的专业人士；MIT 早期工作论文版本报告 444 人。本报告保留这一版本差异，不擅自合并成一个数字。
- 主要指标是完成时间和外部评价的输出质量。

**主要发现（事实证据）**

- Science/PubMed 摘要报告：平均完成时间减少约 40%，输出质量提高约 18%。
- MIT 工作论文报告：时间约下降 0.8 个标准差、质量约提高 0.4 个标准差；低能力参与者收益更大，生产力差距缩小。
- 工作论文进一步报告，参与者往往直接提交 ChatGPT 初始输出，实验中观察到的收益主要像是替代部分劳动投入，而不是充分的人机互补。
- 参与者的任务满意度提高；这仍不能解释为“因为更像人”。

**局限**

- 任务集中在中等复杂度职业写作，不能直接外推到学业规划、学习迁移、成绩或青少年。
- 比较的是“可用/不可用 ChatGPT”，没有独立操纵人化线索、社会临场感、记忆或自主性；因此只能证明工具可用性在该任务中的效果，不能归因于人化。
- 短期实验和后续自报使用意向，不等于长期教育收益。

**对命题的意义**

- 有较强的“工具能力/可用性可以创造用户价值”的证据。
- 没有“拟人化导致生产力收益”的证据，不能把 ChatGPT 的收益记在人化账上。

---

### 2.5 Brynjolfsson、Li、Raymond (2023)：现场部署的生成式 AI 提升生产力，但增益异质

**来源**

- E. Brynjolfsson, D. Li, L. R. Raymond, *Generative AI at Work*, NBER Working Paper 31161。
- [NBER 研究页面](https://www.nber.org/papers/w31161)
- [NBER PDF](https://www.nber.org/system/files/working_papers/w31161/w31161.pdf)
- [Stanford Digital Economy Lab / Stanford 工作论文页面](https://www.gsb.stanford.edu/faculty-research/working-papers/generative-ai-work)

**研究对象与方法（事实证据）**

- 研究某大型软件公司的客户支持工作，分析生成式 AI 对话助手分阶段引入后的数据。
- NBER 摘要报告 5,179 名客服人员；核心指标是每小时解决的客户问题数量。
- 这是现场部署的分阶段引入研究，不应描述成对所有使用者随机分配的实验。

**主要发现（事实证据）**

- 平均生产率提高约 14%。
- 新手/低技能员工提升约 34%，经验丰富/高技能员工影响很小。
- 论文提供“AI 传播高能力员工最佳实践、帮助新员工沿经验曲线学习”的提示性证据；还报告客户情绪改善、员工留任改善，并提出可能存在员工学习。

**局限**

- 单一企业、单一职业、单一工作流；外推到教育产品需谨慎。
- 工具是辅助员工的对话建议系统，员工仍负责对话并可忽略建议；没有操纵人化程度。
- “可能导致学习”是作者的证据解释，不能当作已证明的长期学习迁移。

**对命题的意义**

- 支持“恰当的人机协作机制与任务匹配能产生真实价值”，不支持“人化是主要原因”。
- 增益具有显著异质性；不存在不考虑用户能力、任务和错误率的统一收益百分比。

---

## 3. 已定位但本轮没有完成核验的主题

下面的来源是真实可定位的研究入口，但因用户要求暂停，**本轮不把它们的摘要或标题当成已核实结论**。

### 3.1 人化、健康场景与信任

- *The Influence of Anthropomorphic Cues on Patients’ Perceived Anthropomorphism, Social Presence, Trust Building, and Acceptance of Health Care Conversational Agents: Within-Subject Web-Based Experiment*。
  - [JMIR DOI](https://doi.org/10.2196/44479)
  - 已确认：标题与摘要描述的是不同人化水平的健康指导会话代理、被试内网页实验，结果变量包含拟人化感知、社会临场感、信任与接受。
  - **未完成**：样本、具体操纵、效应量、统计显著性、健康情境外推和全文局限。

- *How to leverage anthropomorphism for chatbot service interfaces: The interplay of communication style and personification*。
  - [DOI](https://doi.org/10.1016/j.chb.2023.107630)
  - 已获得摘要级线索：研究人化外观/人格化与社会性沟通风格，摘要称二者影响社会临场感，社会临场感与信任、同理心和满意度相关。
  - **未完成**：实验样本、任务、操纵强度、效应量和是否存在边际递减。

- Go & Sundar (2019), *Humanizing chatbots: The effects of visual, identity and conversational cues on humanness perceptions*。
  - [DOI（由后续论文引用的原始出版物入口）](https://doi.org/10.1016/j.chb.2019.03.020)
  - **未完成**：本轮未读取原文，不能在本文中断言其具体实验结果。

### 3.2 信任校准的其他原始研究

- Buçinca 等论文已经完成核验，作为本轮信任校准核心证据。
- 另已定位但未完成全文核验：
  - *Explanations Can Reduce Overreliance on AI Systems During Decision-Making*，[arXiv](https://arxiv.org/abs/2212.06823)，[ACM DOI](https://doi.org/10.1145/3579605)。
  - *Who Should I Trust: AI or Myself? Leveraging Human and AI Correctness Likelihood to Promote Appropriate Trust in AI-Assisted Decision-Making*，[arXiv](https://arxiv.org/abs/2301.05809)，[ACM DOI](https://doi.org/10.1145/3544548.3581058)。
  - *Trust and reliance on AI — An experimental study on the extent and costs of overreliance on AI*，[DOI](https://doi.org/10.1016/j.chb.2024.108352)。
- **未完成**：尚未比较这些研究的样本、任务、依赖定义和是否能外推到长期 Agent。

### 3.3 记忆与个性化

本轮已定位以下原始论文入口，但没有完成“记忆/个性化是否改善真实用户长期价值”的全文核验：

- *MemoryBank: Enhancing Large Language Models with Long-Term Memory*，[arXiv](https://arxiv.org/abs/2305.10250)，[AAAI DOI](https://doi.org/10.1609/aaai.v38i17.29946)。
- *Generative Agents: Interactive Simulacra of Human Behavior*，[arXiv](https://arxiv.org/abs/2304.03442)，[ACM DOI](https://doi.org/10.1145/3586183.3606763)。
- 相关综述入口：*A survey on large language model based autonomous agents*，[DOI](https://doi.org/10.1007/s11704-024-40231-1)。

**本轮不能得出的结论**

- 没有足够证据说“记忆越多越有价值”。
- 没有足够证据说“个性化一定提高信任”；记忆错误、过时或越权使用可能反而损害信任，但这一句在本轮只是合理风险假设，不是本文已核验的实证结论。
- 没有找到以学业长期结果为终点、并把记忆/个性化与无记忆对照的充分现场实验。

### 3.4 Reflection / self-improvement

- *Reflexion: Language Agents with Verbal Reinforcement Learning*，[arXiv](https://arxiv.org/abs/2303.11366)，[DOI](https://doi.org/10.48550/arXiv.2303.11366)。
- 该方向已定位为“语言反馈/反思记忆驱动的 Agent 性能改进”研究入口。
- **未完成**：本轮没有核对其任务、基线、提升幅度、失败案例、成本和是否有真实用户研究。因此不能把 benchmark 提升写成“产品自我改进会给学生带来价值”。

### 3.5 Agent autonomy / agency

- 本轮没有完成足够的原始证据，证明自主程度与用户价值、信任或教育结果之间存在单调关系。
- 目前可确认的最低判断是：自主性、主动性、代表用户行动和学生主体性是不同变量；不能用“更自主”替代“更有用”。
- **缺少的关键研究**：不同自主等级的随机对照；用户可撤销、可解释、可拒绝与不可逆行动的比较；错误行动成本；长期依赖和责任分配；未成年人/家长场景。

### 3.6 Human-agent collaboration

已完成的 Noy–Zhang 和 Brynjolfsson–Li–Raymond 证明了部分生成式 AI 辅助任务的生产率价值，但没有操纵人化。仍缺少本轮针对以下问题的完整核验：

- 人化线索是否改变人类何时接受、质疑或复核 Agent 建议；
- 人化是否提高协作的客观决策质量，而不仅是满意度；
- Agent 主动性、记忆、反思和人化之间是否存在交互效应；
- 学业规划、学习方法和复盘等长期教育任务中的人机协作结果。

---

## 4. 主题化综合：当前证据到底支持什么

### 4.1 Anthropomorphism / social presence

**事实证据**：多个服务/购物/健康聊天研究入口和 Araujo 的完整实验表明，人化线索能够提高人化感知和社会临场感；在部分短期服务情境中，还能提高情感连接、主观信任、满意度或行为意向。

**作者观点**：社会临场感可能是人化线索影响服务评价的中介机制。

**不能推出的结论**：社会临场感不是能力、正确性或学习迁移的同义词；人化不是一个越高越好的单维旋钮。

### 4.2 Human-AI trust calibration

**事实证据**：Buçinca 等研究显示，减少过度依赖的设计可以降低主观偏好和信任；即使这样仍不能完全消除错误依赖。

**产品设计判断**：学业军师应追求“在有依据时相信、在不确定时复核、在高风险时升级”的校准信任，而不是让学生形成“它像一个很懂我的人，所以总是对的”的印象。

### 4.3 Memory / personalization

**当前状态**：来源已定位，用户价值证据尚未完成。不能把“记得更多”写成价值公理。

**产品设计判断**：若未来纳入元文档，只能先写成待验证原则，例如“记忆应服务于连续理解和学生可修正的规划，而不是为了制造亲密感”；需要用长期任务完成率、复盘质量、错误记忆率、用户控制感和退出/纠正行为验证。

### 4.4 Reflection / self-improvement

**当前状态**：已有 Agent benchmark 方向的原始论文入口，但本轮没有完成用户价值核验。

**不能写成事实**：Agent 在 benchmark 上通过反思获得更高分，不等于它能帮助学生形成更好的学习方法，也不等于自主反思永远可靠。

### 4.5 Autonomy / agency

**当前状态**：证据不足以支持“越自主越有价值”。

**产品设计判断**：学业军师可以有主动判断和行动建议，但学生应拥有理解、质疑、拒绝、调整和复盘的权利；这与项目既有会话交接中的用户决策一致，但仍属于本项目产品决策，不是本轮外部研究证明的事实。

### 4.6 Human-agent collaboration

**事实证据**：生成式 AI 在特定写作和客服工作流中能提高生产率，收益依任务和用户能力而异；这两项研究没有把收益归因于人化。

**产品设计判断**：评估学业军师时应直接测学生是否更能理解处境、制定计划、采取行动、提交证据和完成复盘，而不是只测“像不像一个人”“喜不喜欢聊天”。

---

## 5. 哪些可以转入《学业军师产品元文档》

以下是**可作为候选原则/工作假设**的内容；写入元文档前仍需用户确认，并标注证据范围与状态。

### 5.1 可以转化（但应写克制版本）

1. **人化的目的不是伪装成人，而是降低交互距离、提高理解感和表达意愿。**
   - 依据：Araujo 等关于社会临场感的实验结果。
   - 限制：主要来自短期服务/购物场景；“表达意愿”在本轮没有直接充分测量，宜写成待验证假设。

2. **产品评价必须把主观体验与客观结果分开。**
   - 依据：人化研究常提高感知指标；Noy/Zhang、Brynjolfsson 等则显示能力/任务匹配影响客观生产率；Buçinca 显示信任/偏好可能与适当依赖相反。

3. **目标是校准信任，不是最大化信任。**
   - 依据：Buçinca 等关于过度依赖、认知强制和主观可接受性权衡的实验。

4. **主动指导不能取消学生主体性。**
   - 这是本项目的产品设计判断，与信任校准和责任边界相容；本轮没有找到足以替产品直接决定该边界的单篇外部研究。

5. **所有“人化”能力都应通过真实任务结果验证。**
   - 推荐指标：计划是否被理解和执行、证据提交率、复盘完成率、学生能否解释并质疑建议、错误建议识别率、长期迁移，而非只看满意度/拟人化评分。

6. **记忆、个性化、反思和自主行动应分别验证，不应打包成“更像人”。**
   - 这是避免混淆变量的产品/研究方法原则；本轮尚未完成这些能力各自的教育长期证据。

### 5.2 不能直接转化为元文档事实

1. “越像人，产品越优秀。”
2. “20% 人化带来 80% 价值。”
3. “社会临场感越高，学习效果越好。”
4. “更高信任代表更好产品。”
5. “记住更多个人信息就会更懂学生。”
6. “Agent 能反思就会持续自我改进并可靠地帮助学生。”
7. “Agent 越自主，学生收益越高。”
8. “聊天机器人研究中的购买意向/服务满意度可直接代表学业价值。”
9. “生成式 AI 生产率提升来自人化设计。”
10. “一次实验或 benchmark 的提升可以证明长期成绩提升。”

这些表述若要保留，只能放在**候选假设、开发者判断或待验证问题**中，不能标为客观事实。

---

## 6. 建议保留的待研究清单

1. **剂量关系**：把人化拆成语言风格、命名/身份、外观、社会性回应、情绪表达、记忆连续性、主动性，逐项做消融或阶梯实验。
2. **校准信任**：同时测“信任”“正确依赖”“错误拒绝”“复核行为”和最终任务结果。
3. **长期记忆**：有记忆/无记忆/错误记忆/用户可纠正记忆的长期对照，终点包含复盘质量和学生独立能力。
4. **反思与自主性**：比较无反思、内部反思、可见反思、学生确认后行动、自动行动；记录成本、错误和可撤销性。
5. **教育场景**：青少年、家长观察者、学生主体、隐私和安全边界，不能用电商客服研究直接代替。
6. **“20%/80%”命题**：除非先定义投入、价值和时间窗口并获得数据，否则不要使用百分比；最小可行验证是对具体设计元素做随机 A/B 和长期任务指标比较。

---

## 7. 来源索引（按本轮状态）

### 已完成或基本完成

- [Araujo 2018 — UvA-DARE](https://dare.uva.nl/id/c2ecbc88-290d-44bf-8f63-6f7832abe802)
- [Araujo 2018 — 全文 PDF](https://pure.uva.nl/ws/files/25443263/Living_up_to_the_chatbot_hype.pdf)
- [Araujo 2018 — DOI](https://doi.org/10.1016/j.chb.2018.03.051)
- [Someone out there? — DOI（摘要级）](https://doi.org/10.1016/j.chb.2022.107513)
- [Buçinca et al. 2021 — arXiv](https://arxiv.org/abs/2102.09692)
- [Buçinca et al. 2021 — Harvard 页面](https://eecs.harvard.edu/~kgajos/papers/2021/bucinca2021trust.shtml)
- [Buçinca et al. 2021 — ACM DOI](https://doi.org/10.1145/3449287)
- [Noy & Zhang — Science DOI](https://doi.org/10.1126/science.adh2586)
- [Noy & Zhang — MIT 工作论文](https://economics.mit.edu/sites/default/files/inline-files/Noy_Zhang_1.pdf)
- [Noy & Zhang — OSF 数据/代码](https://osf.io/xd7qw/?view_only=b8dac58dd6f44b979bf81069022fa392)
- [Brynjolfsson, Li & Raymond — NBER](https://www.nber.org/papers/w31161)
- [Brynjolfsson, Li & Raymond — NBER PDF](https://www.nber.org/system/files/working_papers/w31161/w31161.pdf)

### 已定位、待全文核验

- [健康聊天代理人化实验 — JMIR DOI](https://doi.org/10.2196/44479)
- [Anthropomorphism 与 chatbot service interface — DOI](https://doi.org/10.1016/j.chb.2023.107630)
- [Go & Sundar 2019 — DOI](https://doi.org/10.1016/j.chb.2019.03.020)
- [Explanations Can Reduce Overreliance — arXiv](https://arxiv.org/abs/2212.06823)
- [Who Should I Trust — arXiv](https://arxiv.org/abs/2301.05809)
- [Trust and reliance on AI — DOI](https://doi.org/10.1016/j.chb.2024.108352)
- [MemoryBank — arXiv](https://arxiv.org/abs/2305.10250)
- [MemoryBank — AAAI DOI](https://doi.org/10.1609/aaai.v38i17.29946)
- [Generative Agents — arXiv](https://arxiv.org/abs/2304.03442)
- [Generative Agents — ACM DOI](https://doi.org/10.1145/3586183.3606763)
- [Reflexion — arXiv](https://arxiv.org/abs/2303.11366)

---

## 8. 最终状态

- **本轮已完成**：人化/社会临场感的局部实验事实；信任校准与过度依赖的一项核心实验；两项生成式 AI 真实任务/现场价值研究；两个强命题的初步证伪边界；可进入元文档的克制原则与不可写成事实的句子。
- **本轮未完成**：记忆/个性化的长期用户价值；reflection/self-improvement 的用户结果；自主性/agency 的因果证据；教育/青少年场景；人化“剂量—价值”关系；“20%/80%”定量命题；已定位的若干论文全文核验。
- **因此本文不是完整综述，也不是产品决策书。**
