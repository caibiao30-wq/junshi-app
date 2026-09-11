# 异步路由契约（非阻塞派遣）

本契约补充 `routing-contract.md` 的硬路由规则，定义辅技能以异步、非阻塞方式运行时的身份、输入版本、分片、回收和合并边界。**异步不等于放弃专业路由或门控**：主线可在安全范围内继续，但不得把未回收结果当作已完成，也不得绕过原有硬闸门。

## 1. 派遣记录（dispatch envelope）

每次异步派遣必须生成稳定且不可复用的 `dispatch_id`，并在主技能账本或既有交接中记录以下字段：

| 字段 | 要求 |
|---|---|
| `dispatch_id` | 本次派遣的唯一标识；重试、补派、分片各自新建 ID，并保留 `parent_dispatch_id`（如有） |
| `parent_checkpoint` | 派遣时主线的检查点：阶段、问题/章节范围、工件版本及门控状态；结果只能对该检查点负责 |
| `input_snapshot` | 实际交给 worker 的输入快照（文件、消息/段落定位、授权与排除项）；不可只写“最新内容” |
| `input_version` | 快照对应的单调版本或内容指纹；合并前必须比较当前版本 |
| `shard` | 分片范围与边界（如阶段、问题、章节或记录块）；说明是否允许跨片引用、是否完整覆盖目标 |
| `merge_policy` | 结果如何合并、由谁合并、冲突如何处理、是否允许写入；默认 `review_then_merge`，worker 不得直接覆盖主线结论 |
| `frontier_effect` | 该派遣对主线推进边界的声明：`none`、`advisory`、`blocked`；不得将 advisory 结果误作门控完成 |
| `review_due` | 必须回收/复核结果的检查点或条件（至少含阶段、门控、工件版本或用户确认要求） |

推荐的最小账本形态：

```text
dispatch_id: <唯一 ID>
parent_checkpoint: <阶段/问题或章节/工件版本/门控状态>
input_snapshot: <文件 + 定位 + 授权 + 排除项>
input_version: <版本号或内容指纹>
shard: <范围；覆盖边界>
merge_policy: review_then_merge | append_only | reject_stale | manual_conflict
frontier_effect: none | advisory | blocked
review_due: <回收条件与责任>
status: dispatched | running | worker_done | late | failed | cancelled | conflict | degraded
```

## 2. 主线与 worker 的非阻塞规则

- 派遣成功只表示 `dispatched`，不表示专业动作完成；只有收到字段完整的 `worker_done` 才能进入结果审查。
- 主线可以继续的前提是：当前动作不依赖该 shard 的结论、`frontier_effect` 不是 `blocked`、没有跨 shard 写入或决策依赖，且已登记 `review_due`。
- 主线不得越过 `parent_checkpoint` 所声明的门控，也不得把同一工件的后续版本作为该 worker 的输入来解释。
- 到达 `review_due` 时必须回收并审查所有相关 dispatch；若结果尚未可用，主线转为阻塞或按已授权降级处理，不得静默跳过。
- `worker_done` 不是用户确认，也不是质检通过；状态仍按 `state-rubric.md` 判定，用户结论只能在确认门后写入。

## 3. `worker_done` 返回接口

worker 完成、部分完成或无法完成时，必须回报：

```text
worker_done:
  dispatch_id: <对应 ID>
  parent_checkpoint: <原样回显>
  input_version: <实际处理版本>
  shard: <实际覆盖范围；未覆盖范围>
  outcome: complete | partial | failed | cancelled | conflict
  output: <产物/建议/差异；含来源定位>
  state: <每项状态；不得自行升级>
  evidence: <文件、消息、段落或锚点定位>
  missing_or_failed: <缺失证据、错误、未完成项；无则“无”>
  conflict: <与哪个版本/结果冲突及差异；无则“无”>
  merge_recommendation: <按 merge_policy 给出的可合并动作>
  review_due: <仍需谁在何检查点复核>
```

字段缺失、ID 不匹配、版本无法核对或定位不可回溯时，交接为 `failed`/`conflict`，而不是“基本完成”。

## 4. 异常与结果处理

| 情形 | 判定 | 主线动作 | 是否推进门控 |
|---|---|---|---|
| **迟到 `late`** | 超过 `review_due` 仍未返回，或返回时主线已越过其检查点 | 标记迟到；冻结其自动写入资格，按版本重新审查；必要时取消并补派 | 依赖该 shard 则阻塞；不依赖则可继续，但必须保留待回收项 |
| **失败 `failed`** | 工具/权限/执行错误，或返回字段/证据不全 | 保留失败证据；不得伪造输出；判断是否授权降级或补派 | 依赖该结果则不放行；非依赖动作可继续 |
| **取消 `cancelled`** | 主线、用户或调度方明确取消，或输入已失效而主动终止 | 记录取消者、原因、时间与未完成范围；结果不进入合并 | 依赖该结果不放行，除非取得授权降级并复核 |
| **冲突 `conflict`** | 输入版本过旧、分片重叠、结果与现状/其他 worker 不一致 | 隔离冲突结果，列出差异与证据；由主技能或指定复核者裁决 | 未裁决不得合并或放行 |
| **降级 `degraded`** | 辅技能不可用、调用失败或权限/工具阻塞，经明确授权由主技能代执行 | 记录失败证据、授权依据、代执行范围与恢复/复核条件；沿用同一输入输出字段 | 结果只能标“待复核”；原硬闸门仍视为未由辅技能完成，除非流程明确允许该授权替代 |

迟到、失败、取消、冲突和降级均不得被压成普通 `complete`。任何自动重试都须新建 `dispatch_id`，不可覆盖原始审计链。

## 5. 合并策略（`merge_policy`）

默认采用 `review_then_merge`：worker 只返回可定位的候选差异，由主技能按当前工件版本审查后合并。按风险选择：

- `append_only`：仅可追加互不覆盖的新记录单元；仍需检查定位、状态和授权。
- `reject_stale`：`input_version` 非当前版本即拒绝自动合并，要求重派或人工复核。
- `manual_conflict`：任何重叠、修正、状态变化或跨 shard 依赖都必须人工裁决。

合并前至少核对：`dispatch_id`、父检查点、版本、分片边界、来源定位、状态标签、保真要求和用户记录授权。合并后更新工件版本并记录合并者、时间、纳入/拒绝范围及未决项。报告不得以 worker 自己的摘要替代 `02_访谈记录.md` 证据。

## 6. `frontier_effect` 与主线继续条件

- `none`：结果仅供未来审查；主线按原门控继续，不得引用未回收内容。
- `advisory`：结果可能改善问题清单、候选或准备工作；主线可继续非依赖动作，结果回收后再决定是否采用。
- `blocked`：结果是当前门控、写入或安全判断的必要输入；主线只能做不依赖该结果的保全和等待动作。

主线继续必须同时满足：

1. 已有 `dispatch_id` 和完整 `parent_checkpoint`，输入快照/版本及 shard 边界可核对；
2. worker 尚未完成时，继续动作不读取其未确认结论、不覆盖其分片、不跨越依赖门控；
3. `frontier_effect` 非 `blocked`，并已设置具体 `review_due`；
4. 当前阶段的用户确认、记录固化、报告撰写和质检等原硬闸门仍按 `routing-contract.md` 执行；异步状态不能替代辅技能调用或合格交接；
5. 到达 `review_due`、发生版本变化或出现冲突时，先暂停依赖动作，完成回收/重派/授权降级与复核，再更新主线检查点。

因此，“主线继续”只表示安全地处理独立工作，不表示访谈阶段、工件或专业动作已经完成。
