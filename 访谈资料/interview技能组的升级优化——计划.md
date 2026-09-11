# interview 技能组升级优化——派工与审查计划

> 状态：执行中
> 依据：[`interview技能组的优化升级报告.md`](./interview技能组的优化升级报告.md)
> 目的：将报告中的升级建议拆成可独立派遣、可合并、可审查的工作包。

## 1. 范围与硬约束

### 1.1 本轮范围

本轮执行 P0-1、P0-2、P0-3、P1-1 至 P1-8、P2-1，以及报告第 17 节列出的高性价比改进；不执行报告第 17 节第 3 步的 `interview eval runner`、`evals/fixtures`、`assertions` 或其他测试基础设施工作。

### 1.2 不测试

全程不运行测试、eval、runner、gate 脚本或黑盒访谈。本轮对运行行为仅做静态覆盖，运行期未验证。验收只做静态核对：路径与文件清单、引用闭合、契约字段存在、权威源与镜像差异、执行记录和审查报告是否齐全。任何未运行项目均标为“未测试”，不得写成“已通过”，也不得称本轮为“可验证升级完成”或“负例已实测阻塞”。

### 1.3 技能源与副本

- 权威编辑源：`.claude/skills/interview-*`。
- 镜像：`.agents/skills/interview-*`，由集成代理在权威源收口后同步。
- 执行代理不得绕过文件所有权矩阵修改他人负责文件。
- 每个优化升级代理（E1–E8、I）**第一调用必须实际调用 `skill-creator`**，随后才可按需调用 `md-writing`、`compare-docs`、`documentation-audit` 或基础文件工具。
- 审查代理（R1–R3）与执行代理分离，不自证、不改稿、不替用户作产品决策。

## 2. 执行工作包

| 编号 | 责任 | 工作内容 | 主文件所有权 | 依赖 |
|---|---|---|---|---|
| E1 | 决策树/前沿代理 | 建立节点生命周期、依赖、frontier、范围版本和重算契约；补前沿静态门 | `interview-workflow/references/decision-tree-contract.md`、`state-rubric.md`、`scripts/frontier_gate.py`、`examples/02_访谈记录.example.md` | 无 |
| E2 | 调查授权/来源代理 | 建立取证前 stop-and-ask 授权门、范围快照、来源登记 schema 和失败来源记录规则 | `interview-due-diligence/scripts/evidence_scope_gate.py`、`references/source-schema.md`、`examples/01_调查取证.example.md` | 无 |
| E3 | brief/语言代理 | 强化六大前置要素、调查授权字段、对象—用户—问题—约束—目标和术语账本；建立术语安全环 | `interview-brief/SKILL.md`、`scripts/brief_validate.py`、所有 `00_访谈约定.example.md`、`interview-workflow/references/non-expert-language.md` | E2 提供授权字段清单 |
| E4 | 异步路由代理 | 建立 fork 非阻塞、快照、版本、迟到、冲突、失败、降级、合并和 frontier 影响协议 | `interview-workflow/references/routing-contract.md`（或独立 async contract） | E1 提供节点依赖接口 |
| E5 | 证据/门禁代理 | 将来源、问题、节点、状态、定位、授权和证据引用结构化校验；修命名误判、非法状态迁移和保真脚本重复 | `evidence_gate.py`、`record_gate.py`、`report_gate.py`、`qc_run.py`、`qc_fidelity.py` | E2 的来源 schema；E7 的状态迁移规则 |
| E6 | 阶段/报告代理 | 将固定阶段改为会话级动态阶段；定义内容级阶段完成证据和无空章报告规则 | `interview-workflow/references/stage-acceptance.md`、`interview-reporter/SKILL.md`、`references/reporting-rules.md` | E1 的 frontier 契约 |
| E7 | 批判代拟代理 | 建立批判卡片、事实冲突先行、代拟与用户判断分离及确认/修正/拒绝状态迁移 | `interview-transcriber/SKILL.md`、`references/recording-rules.md` | E1 的状态域；E5 接收校验规则 |
| E8 | 责任/治理代理 | 建立辅技能输入输出责任协议、失败与冲突格式、版本与有效期；提出单一权威源和路由分级、fork 选型、单元索引、结构一致性规则 | `interview-workflow/references/runtime-responsibility.md` 及治理说明 | 各 E 提供责任边界 |

### 2.1 执行代理统一交接格式

每个 E 代理必须回传：

```text
worker_id / work_package
首调 skill-creator 的实际调用证据
输入快照与版本
修改文件清单
新增或改变的契约/字段
与其他工作包的接口和冲突
未完成项、失败项、需人工确认项
未测试声明
worker_done
```

执行代理不得把测试、eval 或 runner 作为本轮“顺手补充项”。

## 3. 并行、串行与集成

**执行顺序依赖 DAG**：逻辑上按接口依赖收敛执行——E1 先冻结决策树/状态接口与 frontier 契约，作为其后各包的下游接口；E4/E6/E7 依赖 E1 接口，收到接口后再执行（E7 另依赖 E1 状态域）；E5 依赖 E1 状态域与 E2 的来源 schema；E8 在收集各 E 的责任边界后收口；所有 E 回传 `worker_done` 后才派遣 I。本批因文件所有权互不相交、接口字段交由集成阶段统一对齐，实际在保证文件不重叠前提下并行执行，逻辑 DAG 边不作为串行闸门。

1. E1、E2、E4、E6、E7、E8 可在文件不相交前提下并行。
2. E3 需接收 E2 的调查授权字段，再修改 00 模板；00 模板的所有副本由 E3 统一负责，其他代理不得并行修改。
3. E5 等待 E2 的来源 schema、E7 的状态迁移规则后执行；E5 独占门禁脚本。
4. 所有 E 代理完成并回传 `worker_done` 后，才派遣集成代理 I。
5. I 是唯一可修改 `interview-workflow/SKILL.md` 的代理：整合新契约路由、六要素、取证技能绑定（`agent-reach` / `research` / `playwright-cli`）、动态阶段、运行时责任和高性价比规则。
6. I 在权威源收口后，按 `compare-docs → documentation-audit` 顺序处理副本与文档集，再同步 `.claude/skills` 到 `.agents/skills`。
7. I 回传整合清单、冲突处理、同步结果和 `worker_done` 后，才进入审查。

## 4. 审查工作包

审查代理在 I 完成后另行派遣，均只读：

| 编号 | 审查重点 | 输出要求 |
|---|---|---|
| R1 | 结构与漂移：双副本、引用、路径、字段、职责、版本 | `通过 / 阻塞 / 需人工复核` + `path:line` + 影响 + 修复建议 |
| R2 | interview 质量：六要素、节点/frontier、授权门、异步协议、阶段验收、证据门禁、批判卡片、语言安全环、责任协议 | 对照报告第 18 节及 12 条负例逐项给出三态结果；不改稿 |
| R3 | 边界压力：不测试约束是否被违反、静态验收是否可核、并发所有权是否产生漂移、是否存在隐性产品决策 | 区分事实、推断、风险和待用户确认项；不替代 R1/R2 |

任一审查代理报告“阻塞”，主编排暂停发布并将定位交回责任代理；审查代理不得自行修复后自证通过。

## 5. 静态验收清单（不是测试）

以下验收仅证明静态覆盖与引用/字段存在，不证明运行正确；全项通过也不构成“已验证”或“可验证升级完成”。

- [ ] E1–E8、I 均有首调 `skill-creator` 的实际调用记录。
- [ ] 所有工作包均有输入、输出、依赖、文件所有权和 `worker_done` 记录。
- [ ] 决策树、frontier、范围版本、异步路由、阶段验收、语言安全、来源 schema、运行时责任契约的关键字段可在相应 reference 中定位。
- [ ] 00/01/02/03 工件职责、六种证据/确认状态、长论证保真原则仍被保留。
- [ ] 报告第 18 节 12 条负例均有对应规则或静态审查项；不执行测试验证。
- [ ] `.claude/skills/interview-*` 与 `.agents/skills/interview-*` 的内容差异已记录；若同步完成，静态 diff 应无差异。
- [ ] R1–R3 均已独立回报；阻塞项、人工复核项和未测试项没有被隐藏。
- [ ] 未执行 `eval`、runner、gate 脚本、黑盒访谈或任何测试命令。

## 6. Skill 使用记录

每个阶段追加以下记录，不以“写了技能名称”替代实际调用证据：

```markdown
### <阶段>/<代理>
- 任务类型：执行 / 集成 / 审查
- 输入：路径、版本、范围
- 首调技能：`skill-creator`（仅 E1–E8、I；记录实际返回）
- 其他技能/工具：实际调用及返回摘要
- 输出：文件、结论或审查报告
- 阻塞/降级：无则写“无”
- 未调用项及理由：尤其记录未调用测试能力
- 验证：仅静态核对；明确写“未测试”
- 状态：`worker_done` / `通过` / `阻塞` / `需人工复核`
```

## 7. 发布门

只有在 E1–E8、I 均收口，R1–R3 均有回报，且所有阻塞与人工确认项已显式列出后，才能把本轮产物的发布身份标为“待用户采纳升级草案”。本计划不把技能升级方案自动视为产品决策，也不把静态覆盖自动视为运行正确；未运行验证的负例不称“已实测阻塞”。

---

## 本轮执行记录

> 由主编排追加；不得删除失败、阻塞、迟到或未测试记录。
