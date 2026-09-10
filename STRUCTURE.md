# 学业军师 目录结构


| 项   | 值                                     |
| --- | ------------------------------------- |
| 版本  | 2.3                                   |
| 日期  | 2026-08-28                            |
| 地位  | 目录真源                                  |
| 服从  | 本文只约束目录组织；产品全局判断以《学业军师产品元文档》及其正式派生链为准 |


> **权威边界：** `STRUCTURE.md` 不决定产品是什么、做什么或产品原则。当前元文档仍处于草稿／未生效阶段；在正式权威路径确认前，不得把不存在的 `docs/constitution/PRODUCT_FORM.md` 当作实际上游文件。正式文档层级和状态以元文档治理章节及后续决策登记为准。

> **目录事实说明：** `✅ V1`、`V2 规划项`、`V3 规划项` 仅表示目录层规划或磁盘状态，不表示对应产品能力已经实现或已经确认。仅含 `.gitkeep` 的目录是占位目录；目录存在、占位文件和能力实现必须分别核验。`docs/governance/CAPABILITY_ROADMAP.md` 当前不存在，不能作为现存权威文件引用。

---

## 四区


| 路径         | 侧   | 含义                                   |
| ---------- | --- | ------------------------------------ |
| `docs/`    | 法   | 由元文档派生的正式执行性规范库                      |
| `mate/`    | M   | 全量元文档（Meta）与顶层战备部署区（唯一产品法源，含 5编+附编） |
| `.claude/` | A   | Claude Code 开发侧（仅开发加载）               |
| `apps/`    | B1  | 可交付应用根（mobile + api）                 |
| `runtime/` | B2  | 产品逻辑根（engine / domain / knowledge …） |


**加载**：Claude → 仅 `.claude/`；产品 → `apps/` + `runtime/engine/` + `runtime/config/`。  
禁止互读、禁止共享路径；B1 与 B2 仅通过 HTTP API 通信。`mate/` 为全量元文档与顶层战备部署区（唯一产品法源），`docs/` 为派生规范，`draft/` 为过程草稿区。

> **mate/ 状态说明：** `mate/` 为 2026-09-01 更名的全量元文档与顶层战备部署区（由 `book/` 更名而来，含 5编+附编，`mate v1.0` 全新基线），为唯一产品法源。内容为 5编正式定义（Ⅰ本体/Ⅱ机制/Ⅲ实现与运行/Ⅳ验证与治理/Ⅴ实施路径与工程抉择）与附编，不含过程痕迹。`draft/元文档——第一阶段/` 仅保留调研报告，其余过程草稿区待清库。

---

## 根目录

```text
xuexi-junshi/
├── README.md                 # 规划项；当前未创建
├── CLAUDE.md
├── STRUCTURE.md              # 目录真源（本文）
├── package.json              # monorepo 根（pnpm workspaces）；规划项，当前未创建
├── pnpm-workspace.yaml       # 规划项；当前未创建
├── turbo.json                # Turborepo 构建编排；规划项，当前未创建
├── tsconfig.base.json        # 全局 TS 基准；规划项，当前未创建
├── docker-compose.yml        # 本地开发环境；规划项，当前未创建
├── .env.example              # 规划项；当前未创建
├── .gitignore                # 规划项；当前未创建
├── .mcp.json                 # 规划项；当前未创建
├── mate/                     # 全量元文档与顶层战备部署区（5编+附编，mate v1.0 全新基线）
├── docs/
├── .claude/
├── apps/
├── runtime/
├── scripts/
└── draft/
```

---

## docs/（法）

`docs/` 承载由产品元文档派生的正式执行性规范；它不能反向决定产品本体。正式规范必须记录上游元文档版本、继承的决策编号、自身状态和验证方式。

效力顺序：`constitution` ＞ `agent-runtime` / `safety-compliance` / `governance` ＞ `engineering` / `quality` ＞ `strategy` ＞ `operations` / `observability` ＞ `process` ＞ `archive`

```text
docs/
├── constitution/              # 目录规划项；当前仅 .gitkeep，占位（不得作为现行产品权威）
├── strategy/                  # 目录规划项；当前仅 .gitkeep，占位
├── process/                   # 目录规划项；当前仅 .gitkeep，占位
├── agents/                    # 当前存在协作规则材料；不决定产品本体
├── archive/
│   ├── raw/                   # 目录规划项；当前仅 .gitkeep，占位
│   └── legacy/                # 目录规划项；当前仅 .gitkeep，占位
├── agent-runtime/             # V2 规划项；当前仅 .gitkeep，占位
├── safety-compliance/         # V2 规划项；当前仅 .gitkeep，占位
├── engineering/               # V2 规划项；当前仅 .gitkeep，占位
├── quality/                   # V2 规划项；当前仅 .gitkeep，占位
├── governance/                # V2 规划项；当前仅 .gitkeep，占位
├── observability/             # V3 规划项；当前仅 .gitkeep，占位
└── operations/                # V3 规划项；当前仅 .gitkeep，占位
```

规范状态：`stub` → `draft` → `review` → `locked`。未 `locked` 不得作唯一验收依据（负责人明示除外）。

---

## .claude/（A · 开发侧）

仅服务开发共创。禁止存放产品 Prompt / 技能正文；禁止 `apps/` 或 `runtime/` 读取本树。

```text
.claude/
├── settings.json
├── PROJECT_GUIDE.md
├── rules/
├── commands/
├── skills/                    # 开发技能
├── agents/                    # 共创子代理
├── hooks/                     # 开发门禁
├── workflows/                 # 共创流程
├── output-styles/
└── agent-memory/
```

---

## apps/（B1 · 可交付应用根）

B1 是可部署应用根。B1 与 B2 禁止互读，仅通过 HTTP API 通信。

```text
apps/
│
├── mobile/                    # React Native + TypeScript（平板优先）
│   ├── src/
│   │   ├── screens/
│   │   │   ├── student/
│   │   │   │   ├── chat/         # 规划项；当前仅 .gitkeep，占位；  核心对话界面
│   │   │   │   ├── cold_start/   # 规划项；当前仅 .gitkeep，占位；  P0–P5 冷启动流程（30min）
│   │   │   │   ├── assets/       # V2 规划项（当前仅 .gitkeep，占位）：  学业资产展示
│   │   │   │   ├── workbench/    # V2 规划项（当前仅 .gitkeep，占位）：  任务工作台
│   │   │   │   └── war_room/     # V2 规划项（当前仅 .gitkeep，占位）：  全局战局可视化
│   │   │   ├── parent/           # V2 规划项（当前仅 .gitkeep，占位）：  家长端学情报告
│   │   │   └── admin/            # V3 规划项；当前仅 .gitkeep，占位；  管理端
│   │   ├── components/           # 规划项；当前仅 .gitkeep，占位；  共用组件
│   │   ├── navigation/           # 规划项；当前仅 .gitkeep，占位；  导航路由
│   │   ├── shell/                # V2 规划项（当前仅 .gitkeep，占位）：  人格壳层（情绪档 × 五维 × 语言包）
│   │   └── voice/                # V2 规划项（当前仅 .gitkeep，占位）：  TTS / STT 界面层
│   └── tests/
│
└── api/                       # NestJS + TypeScript
    ├── prisma/                # V1 规划项；当前 schema.prisma 未创建，migrations 仅占位
    │   ├── schema.prisma
    │   └── migrations/
    ├── src/
    │   ├── agents/
    │   │   └── base/             # 规划项；当前仅 .gitkeep，占位；  BaseAgentService（共享 LLM + 记忆能力）
    │   ├── llm/                  # 规划项；当前仅 .gitkeep，占位；  LLM NestJS 模块（Claude Sonnet + 备用）
    │   ├── modules/
    │   │   ├── auth/             # 规划项；当前仅 .gitkeep，占位；
    │   │   ├── student/          # 规划项；当前仅 .gitkeep，占位；
    │   │   ├── session/          # 规划项；当前仅 .gitkeep，占位；
    │   │   ├── push/             # V2 规划项（当前仅 .gitkeep，占位）：  家长推送通知
    │   │   └── billing/          # V2 规划项（当前仅 .gitkeep，占位）：  激活码 / 计费
    │   ├── vector/               # V2 规划项（当前仅 .gitkeep，占位）：  向量数据库（记忆检索）
    │   └── config/               # 规划项；当前仅 .gitkeep，占位；
    └── tests/
```

---

## runtime/（B2 · 产品逻辑根）

B2 是纯逻辑根，不含可交付应用。禁止并行 `src/`、`agents/` 实现根，禁止软链两用。

```text
runtime/
│
├── engine/                    # AI Agent 引擎（学业规划壳层核心）
│   ├── identity/              # 规划项；当前仅 .gitkeep，占位；  身份核（六条不可变原则）
│   ├── duty_loop/             # 规划项；当前仅 .gitkeep，占位；  义务环五步 + 九步主循环
│   ├── memory/                # 规划项；当前仅 .gitkeep，占位；  三层记忆（事件 / 认知 / 方法）
│   ├── evidence/              # 规划项；当前仅 .gitkeep，占位；  证据驱动模型
│   ├── prompt/                # 规划项；当前仅 .gitkeep，占位；  Prompt 模板管理
│   ├── safety/                # 规划项；当前仅 .gitkeep，占位；  红线执行 / 边界守护
│   ├── skills/                # V2 规划项（当前仅 .gitkeep，占位）：  产品技能库
│   ├── subagents/             # V2 规划项（当前仅 .gitkeep，占位）：  产品内子代理
│   ├── hooks/                 # V2 规划项（当前仅 .gitkeep，占位）：  产品触发钩子
│   ├── workflows/             # V2 规划项（当前仅 .gitkeep，占位）：  学业闭环工作流
│   ├── means/                 # V2 规划项（当前仅 .gitkeep，占位）：  义务环工具集（从属义务环，非并列）
│   │   ├── qa/
│   │   ├── review_work/
│   │   ├── drill/
│   │   ├── scratchpad/
│   │   └── explain/
│   ├── mirrors/               # V3 规划项；当前仅 .gitkeep，占位；  三面镜子
│   ├── understanding/         # V3 规划项；当前仅 .gitkeep，占位；  了解度百分比
│   └── planning/              # V3 规划项；当前仅 .gitkeep，占位；  动态规划完整体
│
├── domain/                    # 领域数据模型
│   ├── situation/             # 规划项；当前仅 .gitkeep，占位；  当前局势快照
│   ├── assets/                # 规划项；当前仅 .gitkeep，占位；  学业资产
│   ├── action_items/          # 规划项；当前仅 .gitkeep，占位；  行动项
│   ├── evidence_records/      # 规划项；当前仅 .gitkeep，占位；  证据记录
│   ├── liabilities/           # V2 规划项（当前仅 .gitkeep，占位）：  学业负债
│   ├── tracks/                # V2 规划项（当前仅 .gitkeep，占位）：  应试 / 特长双轨
│   │   ├── exam/
│   │   └── specialty/
│   ├── error_chain/           # V3 规划项；当前仅 .gitkeep，占位；  错误链
│   └── thinking_fingerprint/  # V3 规划项；当前仅 .gitkeep，占位；  思维指纹
│
├── knowledge/                 # 知识库（军师侧资源）
│   ├── 00_system/             # 规划项；当前仅 .gitkeep，占位；
│   ├── 01_raw_reference/      # 规划项；当前仅 .gitkeep，占位；
│   ├── 02_staging/            # 规划项；当前仅 .gitkeep，占位；
│   ├── 03_graph/              # V2 规划项（当前仅 .gitkeep，占位）：
│   ├── 04_playbooks/          # V2 规划项（当前仅 .gitkeep，占位）：
│   ├── 05_evals/              # V3 规划项；当前仅 .gitkeep，占位；
│   └── tracks/                # V2 规划项（当前仅 .gitkeep，占位）：
│
├── student_data/
│   ├── fixtures/              # 规划项；当前仅 .gitkeep，占位；
│   └── local/                 # gitignore · 严禁提交
│
├── config/                    # 规划项；当前仅 .gitkeep，占位；
├── tests/                     # 规划项；当前仅 .gitkeep，占位；  集成 / E2E（首个：义务环五步 harness）
└── ops/                       # 规划项；当前仅 .gitkeep，占位；
```

- 产品 skills / hooks / workflows / subagents **仅**位于 `runtime/engine/` 下。
- `means/` 从属义务环，非并列产品线。
- V2/V3 仅表示目录规划；当前仅含 `.gitkeep` 的目录为占位，必须单独核验能力实现后才能改变其状态说明。
- `docs/governance/CAPABILITY_ROADMAP.md` 当前不存在；不得以该路径作为现存门控文件或权威引用。
- 空目录 ≠ 已实现；任何能力状态仍以元文档决策登记及后续正式派生链为准。

---

## 同名异质对照


| 概念                 | A（`.claude/`）   | B1（`apps/api/src/`） | B2（`runtime/engine/`） |
| ------------------ | --------------- | ------------------- | --------------------- |
| skills             | 开发技能            | —                   | 产品技能                  |
| hooks              | 开发门禁            | —                   | 产品触发                  |
| workflows          | 共创流程            | —                   | 学业闭环                  |
| agents / subagents | 共创子代理           | `agents/base`（共享服务） | 产品内子代理                |
| memory             | `agent-memory/` | —                   | `engine/memory/`      |
| config             | `settings.json` | `src/config/`       | `runtime/config/`     |


---

## 附属


| 路径         | 含义                   |
| ---------- | -------------------- |
| `scripts/` | 仓级脚本（含 init-dirs.sh） |
| `draft/`   | 无约束力草稿               |


---

## 硬规则

1. 有约束力的规范只住 `docs/`（`archive` 除外且非法）。
2. B1 根为 `apps/`，B2 根为 `runtime/`；禁止并行 `src/`、`agents/` 实现根。
3. A / B1 / B2 加载根唯一；禁止软链两用；禁止互读、禁止共享路径。
4. `student_data/local` 不进 git。
5. 目录变更先改本文，再改磁盘。
6. V2/V3 标注只表示目录规划，不表示能力已实现；仅含 `.gitkeep` 的目录必须标明为占位并单独核验。

---

## 变更历史


| 版本  | 日期         | 主要变更                                                                                                               |
| --- | ---------- | ------------------------------------------------------------------------------------------------------------------ |
| 1.0 | 2026-08-12 | 初版三柱结构（claude-opus-5 提案）                                                                                           |
| 2.0 | 2026-08-12 | 接受 Fable5 最终修订：apps/ 提升到根级；删除 runtime/adapters/ 和 runtime/packages/；增加 V1/V2/V3 版本标注；增加 docker-compose / Prisma 路径 |
| 2.2 | 2026-08-22 | 对齐当前目录事实：区分规划项、占位目录与已实现文件；补录 `docs/agents/`；移除不存在的能力路线图权威引用 |
| 2.3 | 2026-08-28 | 新增 `book/` 为 M 区（产品元文档正式版，书本形态）；四区表新增 book/ 行；根目录列表新增 book/；book/ 状态说明新增 |
| 2.4 | 2026-09-01 | 更名 `book/`→`mate/` 为全量元文档与顶层战备部署区（5编+附编，mate v1.0 全新基线）；四区/加载/根目录/状态说明同步；正文去 D-ID/去 draft 关联，仅留定义陈述，溯源移附录B |


