# junshi-app 代码库目录布局重构研讨报告

> **定位：** 本报告是计划书「任务 2 — 报告二」的交付物，以 `STRUCTURE.md`（v2.4，目录真源）描述的当前布局为基准，结合 Hermes、OpenClaw、DeepTutor、OpenMAIC 四份调查取证报告的目录层证据，对 junshi-app 代码库目录做深度重构分析。
>
> **结论先行：** junshi-app 现有「四区/双区」大方向（`.claude/` 开发侧 A、`apps/` B1、`runtime/` B2、`docs/` 法）与四份成熟仓库的共性一致，**方向不推翻，但缺三个关键件**：(1) 缺一处可复用的 `agent-core` 内核包（四报告均以「内核包与通道/UI 解耦」为第一共性）；(2) 配置与 schema 未版本化，`runtime/config/` 仍是占位；(3) 异步长任务与工具注册、记忆/知识分离、测试/部署/运维资产分层均为 `.gitkeep` 占位。当前最大的风险不是「目录不对」，而是「目录存在 ≠ 已实现」——大量占位把「规划」写成了「结构事实」。重构应以「让占位闭环真实化」为优先，而非另起一套目录。

---
## 目录
1. 方法与证据
2. 当前布局事实核验
3. 四份报告的顶层目录共性（外部基准）
4. 现有目录问题定位
5. 未来目录职责、依赖与边界
6. 代码与元文档的边界
7. 支撑持续迭代的机制建议
8. 可检查的改造清单
9. 局限与待确认

---

## 1. 方法与证据

- 四份调查报告（`调研报告/`）的顶层目录章节与「不适合照搬」节，证据定位到官方 commit/源码/配置。
- `STRUCTURE.md` v2.4 与当前磁盘（2026-09-03 核验：`runtime/`、`apps/` 下除 `.DS_Store` 外无真实代码文件，全为 `.gitkeep` 占位）。
- 判断分级：事实 / 来源结论 / 推断 / 候选建议；对目录的改动均为候选，实施前须确认。

---

## 2. 当前布局事实核验

核验时点 2026-09-03：

- 四区：`docs/`（法）、`mate/`（M 唯一法源）、`.claude/`（A 开发侧）、`apps/`（B1 mobile+api）+ `runtime/`（B2 engine/domain/knowledge）+ `scripts/` + `draft/`。
- B1↔B2 仅经 HTTP API；A/B1/B2 加载根唯一、禁止互读。
- **事实缺口：** `runtime/engine/*`、`runtime/domain/*`、`apps/api/*`、`runtime/config/`、`runtime/ops/` 等核心实现目录当前**均仅含 `.gitkeep`**（占位）。`apps/` 下仅 `.DS_Store`。即：整个代码库在调查时点无真实运行代码。
- `STRUCTURE.md` 已正确标注「占位目录 ≠ 已实现」，并保留 `docs/governance/CAPABILITY_ROADMAP.md` 不存在、不得引用的警示。

---

## 3. 四份报告的顶层目录共性（外部基准）

| 仓库 | 组织方式 | 内核包/解耦点 |
|---|---|---|
| Hermes | 单包：agent/ + tools/ + providers/ + gateway/ + skills/ + apps/ + tests/ + evals/ + scripts/ | 窄腰核心、边缘扩展；状态/配置真源分离 |
| OpenClaw | pnpm monorepo：src/ + packages/(agent-core, llm-core, memory-host-sdk) + apps/ + skills/ + deploy/ + qa/ + config/ | 内核包 + schemaVersions(state/agent) + 资源包清单化 |
| DeepTutor | 单包：agents/ + core/ + runtime/ + services/(memory/rag/knowledge) + api/ + web/ + tools/ + tests/ | 领域能力—共享协议—运行时—API—前端分层 |
| OpenMAIC | Next.js 单体 app/ + lib/(generation/orchestration/ai/action/store) + packages/@openmaic/ + render-service/ + skills/ + e2e/tests/eval/ | 单体+子包；durable session + 独立 worker |

**四份一致的共性（候选依据）：**
1. **Agent 核心与通道/UI 解耦成独立内核包**（OpenClaw agent-core、Hermes agent/、DeepTutor runtime、OpenMAIC lib/server/agent-runtime）——这是最重要的一条。
2. 工具做注册表/契约而非散进 prompt（Hermes tools/registry、DeepTutor tool_registry、OpenMAIC runner-contract）。
3. 记忆与知识分开、且与运行时解耦（Hermes memory_manager、DeepTutor services/memory、OpenClaw memory-host-sdk、OpenMAIC storage/knowledge）。
4. 测试/评测/部署/运维资产与运行代码同仓但分层（tests/、qa/、deploy/、evals/、e2e/）。
5. 异步长任务与同步会话分离（OpenMAIC durable session+worker；Hermes cron/batch_runner）。

---

## 4. 现有目录问题定位（压力测试）

对照 §3 共性，逐项定位 `STRUCTURE.md` 现状：

| # | 工程环节 | 现状 | 问题定位（对照外部基准） |
|---|---|---|---|
| 1 | Agent 核心逻辑 | `runtime/engine/duty_loop` 等**占位** | 无「内核包/共享 runtime」形态；loop 与能力边界未落目录 |
| 2 | 模型调用 | `apps/api/src/llm/` 占位 | provider 适配与回退、配置快照化无落点 |
| 3 | 工具与外部服务 | `runtime/engine/means/` 占位 | 缺工具注册表/契约/安全审批落点 |
| 4 | 记忆与知识 | `runtime/engine/memory/` + `runtime/knowledge/` 占位 | 两者分离方向对，但无真实实现；memory 归属/owner 未定 |
| 5 | 数据处理 | `runtime/domain/` 占位 | 缺 DSL/schema 校验与迁移机制落点 |
| 6 | API 与前后端边界 | `apps/api/` 占位 | 长任务（如复习生成）若塞 HTTP 会踩反模式 |
| 7 | 配置管理 | `runtime/config/` 占位 | **无 schema 版本化**；配置与代码边界未定 |
| 8 | 测试与质量 | `runtime/tests/`、`apps/*/tests/` 占位 | 缺 eval/qa/契约测试分层 |
| 9 | 构建与部署 | 无独立 `deploy/` | 缺容器/持久化/健康检查真实化 |
| 10 | 运维/监控/日志 | `runtime/ops/` 占位 | 缺 OTEL/日志/监控落点 |
| 11 | 运行时资源 | `runtime/student_data/local`（gitignore） | 方向对（不入 Git），但无数据树持久化方案 |
| 12 | 文档/脚本/辅助 | `scripts/`、`.claude/` | 尚可；与产品核（runtime skills）分离原则正确 |

**核心结论（推断）：** 现有目录骨架在「顶层划分」上不需要推翻；真正的问题是把大量应真实化的实现目录长期停在 `.gitkeep` 占位，同时 `runtime/config`、工具注册、异步 worker、eval/qa、deploy/ops 这些四份报告都点名的工程件在目录上缺失或空置。重构应「填空、补层」，而非「改名、重排」。

---

## 5. 未来目录职责、依赖与边界（候选方案）

保持四区/双区主体，作最小增量（均标注 V2 需确认）：

```text
runtime/                              # B2 产品逻辑根
├── engine/                           # Agent 内核（窄腰核心）
│   ├── core/                         # 【新增】共享 runtime/loop 抽象（对标 agent-core）
│   ├── duty_loop/  identity/  prompt/  safety/
│   ├── memory/                       # 三层记忆（事件/认知/方法），含 owner/保留/删除
│   ├── evidence/                     # 证据驱动 + locator/version/citation
│   ├── tools/                        # 【新建】工具注册表 + schema + 审批 + 沙箱策略
│   ├── subagents/  workflows/  skills/  hooks/  means/
│   └── runtime_config/               # 【强化】显式 schema 版本化 runtime 配置（对标 schemaVersions）
├── domain/                           # 领域模型 + DSL/schema 校验与迁移
├── knowledge/                        # 军师侧资源（与 memory 分开）
├── worker/                           # 【新增】异步/长任务独立 worker（学业闭环后台）
├── tests/  evals/                    # 【新增 evals】契约/恢复/隔离/E2E + 行为评测
├── config/                           # schema 版本化配置真源（非占位）
└── ops/                              # OTEL/日志/监控/回滚演练

apps/
├── api/                              # B1 控制面：鉴权、会话、agent 调度；长任务交 worker
│   ├── src/llm/  modules/  vector/  config/
└── mobile/                           # 多入口复用同一 B2 内核
```

**依赖与边界（候选）：**
- `apps/`（入口/UI）→ 只经 HTTP API → `runtime/`（内核）→ `domain/`（数据）→ `knowledge/` + `memory/`；长任务从 API 进 `worker/` 异步执行，不阻塞 HTTP（对齐 OpenMAIC durable session+worker 与 Hermes 异步分离）。
- 工具注册、产品 skills/hooks/workflows/subagents **仅**在 `runtime/engine/` 下；`.claude/` 只放开发侧能力（沿用「同名异质」对照）。
- 配置：`runtime/config/` 为运行时配置真源并版本化；敏感字段走 env，`runtime/student_data/local` 与运行数据不入 Git。

---

## 6. 代码与元文档的边界

- `mate/`（法源）→ 定义「是什么/做什么/运行机制」；`docs/`（派生规范）→ 记录可执行工程规范，须回链上游 mate 版本与决策编号。
- **具体字段、Schema、Prompt、代码、测试与部署配置**属 `docs/`/代码库，不进 `mate/` 正文（`mate/README.md` 已明确）。
- 每条对 junshi-app 目录的改造，应先有 `mate/`（尤其 T9 工程架构）的决议与派生闸门，再改目录与代码——避免「代码先行、法源后补」。
- 目录变更先改 `STRUCTURE.md`，再改磁盘（沿用硬规则 5）。

---

## 7. 支撑持续迭代的机制建议（候选）

1. **占位真实化门槛：** 新增/存续目录须有非 `.gitkeep` 的验收物（README 说明职责、schema、测试或最小实现之一），否则不得标注为「结构事实」。
2. **能力验收矩阵：** 参照 OpenClaw `maturity-scores.yaml`，为 V2/V3 规划能力建立可核验的成熟度登记，杜绝「目录存在=能力实现」。
3. **配置与 schema 版本化：** 引入 state/agent/领域 schema 版本与迁移机制（对齐 OpenClaw schemaVersions、OpenMAIC DSL/schema），并纳入 CI 校验。
4. **依赖与供应链：** 引入 lockfile、SBOM/许可证登记与镜像 digest 固定（对齐四报告供应链建议），回滚演练含 DB/volume/schema/技能/provider 联合回滚。
5. **可观测性第一天：** `runtime/ops/` 默认 OTEL + 健康检查 + 日志指标 trace，不后补（对齐 OpenClaw）。

---

## 8. 可检查的改造清单

| # | 动作（候选） | 验收门槛 |
|---|---|---|
| 1 | 新增 `runtime/engine/core/` 内核包 | 有共享 loop/状态抽象；B1 与 worker 都复用，非各写一套 |
| 2 | `runtime/config/` 从占位转真实 | 配置 schema 有版本号；敏感字段走 env；CI 校验 |
| 3 | 新增 `runtime/worker/` | 长任务（复习生成等）经 worker 异步执行，API 不阻塞 |
| 4 | `runtime/tools/` 注册表 | 工具/技能经注册+审批+沙箱策略，非散进 prompt |
| 5 | 记忆/知识/领域分离落地 | memory 有 owner/保留/删除；domain 有 schema 迁移 |
| 6 | 新增 `runtime/evals/` | 协议/恢复/隔离/迁移/E2E 有测试，非只测 UI |
| 7 | 新增部署与运维真实物 | 有容器/持久卷/健康检查/OTEL；回滚演练含联合回滚 |
| 8 | STRUCTURE.md 同步 | 每次目录变更先改真源再改磁盘，附变更历史 |

---

## 9. 局限与待确认

- 本报告为**候选建议**，未改动任何目录或代码；进入实施前须产品发起人确认范围与优先级，并经 `mate/` 相应编（尤其 T9/T10）决议。
- 四份报告为外部参照，其组织方式不一定直接适用于教育场景（如 OpenClaw 默认不沙箱、OpenMAIC 租户授权延期等反例不可照搬）。
- 占位真实化涉及大量存量目录，工作量与先后序需评估；建议从「最小可运行闭环」（engine core + domain + config + api）起步。
- 悬而未决：`runtime/engine/core/` 是否新增独立内核包，还是沿用 `duty_loop` 内聚——建议先写「最小可运行闭环」验证后再定。

（全文约 3300 字）
