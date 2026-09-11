# 决策树与前沿状态契约

本文件定义访谈问题的可执行决策树与前沿（frontier）机制：节点生命周期、状态域分离、依赖约束、前沿推进与范围变更重算。它回答"一个问题为什么在此时被提出、依赖是否满足、哪些因范围改变而失效"。

配合读取：`state-rubric.md`（证据与确认状态）、`artifact-schemas.md`（02 记录的节点字段落位）、`routing-contract.md`（派遣门控）。

## 目标与判据

- 每个当前问题都能指向一个节点和一条依赖链（从 `root` 到该节点）。
- 依赖未满足的问题不能进入 `ready`。
- 同一轮只问当前前沿中相互独立且前提已满足的问题。
- 用户改变范围后递增 `scope_version`、沿下游标记 `stale`、记录重算原因。
- 报告引用的问题 ID 必须与记录节点一一对应，不得引用不存在的节点。

## 三种状态域（分离，不混用）

| 域 | 取值 | 归属 | 说明 |
|---|---|---|---|
| 节点生命周期 | `candidate / ready / active / blocked / done / stale / superseded` | 决策树 | 描述问题在树中的推进阶段，不与确认状态互相替代 |
| 证据与确认状态 | 沿用七态：`[用户明确判断] [确认采纳] [专业建议·代拟] [已被修正] [拒绝] [待确认] [待验证]` | 证据 | 贴在具体回应/判断上，定义见 `state-rubric.md` |
| 取证状态 | `unverified / partially_verified / verified / conflicting` | 证据来源 | 描述外部证据的验证程度，不由节点生命周期推断 |

生命周期状态只表达"节点在树中的位置与推进条件"，不表达"是否可写成用户结论"；可写结论与否只由证据与确认状态决定。

## 节点必含字段

每个节点至少包含以下字段：

```text
node_id              # 稳定唯一 ID，供记录/报告回溯
root_id              # 所属树的根节点
parent_id            # 父节点；root 的父节点为空
branch_id            # 分支标识（同 scope_version 下同一脉络）
depends_on           # 前置依赖节点列表；全部 done 才能进 ready
blocked_by           # 阻塞该节点的外部条件（fork、待确认、取证未完成等）
independent_group    # 同轮可并行问出的相互独立问题分组
question_kind        # 问题类型（objective_change / constraint / tradeoff / verify 等）
assumptions / prerequisites  # 前提假设
facts                # 该节点引入的事实
tradeoffs            # 取舍
risks                # 风险
downstream_decisions # 下游依赖本节点结论的决策
completion_evidence  # 该节点完成的可回溯证据
evidence_refs        # 证据来源定位（路径/锚点）
status               # 生命周期状态
supersedes           # 取代的旧节点（被取代者标 superseded）
scope_version        # 该节点生效所依赖的范围版本
recompute_reason     # 因范围改变重算/失效的原因
round                # 提出的轮次
source_location      # 记录中的原始定位
```

## 生命周期状态与迁移

| 状态 | 含义 | 进入条件 | 可推进为 |
|---|---|---|---|
| `candidate` | 已识别但未就绪 | 被记录为候选问题 | `ready`（依赖满足）或保持 `candidate` |
| `ready` | 依赖满足、可被提出 | `depends_on` 全部 `done`，前提已确认 | `active` |
| `active` | 正在本轮被问出 | 属当前前沿且相互独立 | `done` / `blocked` |
| `blocked` | 因依赖、取证或外部条件无法推进 | 依赖未到、证据冲突、待确认 | `active`（解除后）/ `done` |
| `done` | 有合格 completion_evidence，已确认 | 已获确认且证据可回溯 | 范围改变时 → `stale` / `superseded` |
| `stale` | 范围改变后失效，待重算 | `scope_version` 递增 | `superseded` 或重算后重新 `active` |
| `superseded` | 已被新节点取代 | 被 `supersedes` 引用 | 不再使用 |

`depends_on` 未完成的节点不得进入 `ready`（负例 3）。生命周期不能替确认状态下结论。

## 前沿（frontier）推进规则

- 当前前沿 = 所有 `status in (ready, active)` 且属同一 `scope_version` 的节点中，相互独立、前提满足的子集。
- 一轮只推进当前前沿的问题；同一轮问出的节点应相互独立（`independent_group` 内）。
- 节点进入 `active` 前提是依赖链闭合且证据/确认前置已满足。
- 用户改变范围 → 递增 `scope_version` → 沿下游将所有旧版本节点标 `stale` 并记录 `recompute_reason` → 重算 frontier → 旧 frontier 不再使用（负例 4）。

## 范围变更重算

范围（目标/对象/边界）改变时：

1. 主技能递增 `scope_version`。
2. 沿下游标记受影响的节点为 `stale`（保留文本，标 `superseded` 仅当有明确取代者）。
3. 记录每个受影响节点的 `recompute_reason`。
4. 重新计算 frontier，仅从新 `scope_version` 的 `ready/active` 节点取当前问题。
5. 旧下游结论不得被静默沿用；若要复用须显式重算并更新版本。

## 必须阻塞的负例（对齐 §18）

| 负例 | 触发 | 处置 |
|---|---|---|
| 依赖节点未完成即提出下游问题 | 下游节点 `depends_on` 未全部 `done` | 阻塞，待依赖满足 |
| 用户改目标后继续用旧 frontier | 旧 `scope_version` 节点仍被当当前问题 | 阻塞，递增版本并重算 |
| 报告引用不存在的问题或节点 | 报告引用的 `node_id` 不在记录 | 阻塞，修正引用 |
| 空定位/空状态/占位符视为合格证据 | `completion_evidence`/`evidence_refs` 为空或占位 | 阻塞，补证据或改回 `blocked/candidate` |

## 与异步路由的接口（E4 边界，仅记录不实现）

异步支线结果回传按 `dispatch_id + input_version` 去重（见 `routing-contract.md` 与异步契约）。决策树侧只声明两处接口字段、不实现异步协议本身：

- `blocked_by`：允许出现 fork/待到达的异步结果作为阻塞源。
- 依赖支线结果的节点，其 `depends_on` 不得包含尚在跑的结果作为已满足前置；主线可继续的条件由异步契约定义（不依赖该支线结果、不写入其结果工件）。

异步契约的其余字段（`dispatch_id / input_version / conflict_set / frontier_effect` 等）由 E4 负责，本契约不越权实现。
