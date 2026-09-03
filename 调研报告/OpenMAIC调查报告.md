# OpenMAIC Agent 官方仓库调查报告

- **报告类型**：外部 GitHub 仓库只读调查与工程参照分析
- **调查对象**：`THU-MAIC/OpenMAIC`
- **实际访问日期**：2026-09-03
- **建议版本锚点**：release `v1.0.0`（2026-08-27）；源码核验固定到 commit `132d01cd04af22b4b52cc36666a82b4b52cc36666a82b55f2ef224f`（下文以完整 SHA `132d01cd04af22b4b52cc36666a82b55f2ef224f` 引用；如链接打不开，应以 GitHub API 返回的完整 SHA 为准）
- **结论状态**：候选/参照，不是本仓库产品决策

> 本报告只记录外部证据、基于证据的分析、明确标注的推断与候选建议。README 的宣传性描述不等于本次已运行验证；本次没有克隆、安装依赖、启动服务、连接数据库或修改目标仓库。

## 1. 执行摘要

OpenMAIC（Open Multi-Agent Interactive Classroom）是清华大学 MAIC 组织公开维护的互动课堂平台，官方仓库为 [THU-MAIC/OpenMAIC](https://github.com/THU-MAIC/OpenMAIC)。它不是单一聊天机器人，而是把课程生成、幻灯片/测验/交互场景、PBL、多智能体讨论、语音、白板、编辑器、导出、材料管理和 Agent 工作台接入组合成一个 Next.js/TypeScript 单体应用加 workspace 子包的产品。当前仓库的关键工程演进方向是：由同步请求转向持久化 Agent session，由独立 worker 领取队列任务；用 `SKILL.md` 加分层 references 作为外部 Agent 工作台入口；用 `@openmaic/*` SDK 将 DSL、生成、渲染、导入、编辑与存储拆成可复用包；用 PostgreSQL、租约心跳、并发/容量限制以及渲染服务网络隔离支撑长期运行。

对 `mate` 和 `junshi-app` 最有价值的不是照搬其 UI 或 provider 列表，而是借鉴“产品能力—运行时—工程治理”三条边界。建议把以下设计列为**候选/参照**：明确的 Agent runtime 开关与数据库前置条件；HTTP 控制面、durable queue、独立 worker、lease/heartbeat 的异步生命周期；技能入口与详细 SOP 分层；输入和资源配额；课程/领域 DSL 与渲染、导入、存储的包边界；生产构建、E2E、评测、镜像和回滚的完整闭环。与此同时，不应直接采用其开发态 `ACCESS_CODE`、默认数据库密码、对既有课程 owner 校验的延期处理或未经审查的可覆盖技能目录。

## 2. 来源与证据表

| 编号 | 来源类型与稳定 URL | 版本/日期与原文定位 | 事实及用途 | G1-G5 | 状态 |
|---|---|---|---|---|---|
| E1 | GitHub 官方仓库元数据：[THU-MAIC/OpenMAIC](https://github.com/THU-MAIC/OpenMAIC) | 默认分支 `main`；HEAD `132d01cd04af22b4b52cc36666a82b55f2ef224f`；访问 2026-09-03 | 仓库描述为 Open Multi-Agent Interactive Classroom；公开、TypeScript、根许可证 MIT | G1、G5 | 已核验 |
| E2 | GitHub Releases：[releases](https://github.com/THU-MAIC/OpenMAIC/releases) | `v1.0.0`，2026-08-27；同时存在 v0.3.x 等版本 | 提供版本锚点；不等于已核验构建产物可复现 | G1、G5 | 已核验 |
| E3 | 官方中文 README：[README-zh.md](https://github.com/THU-MAIC/OpenMAIC/blob/main/README-zh.md) | `main`；章节“项目简介”“快速开始”“项目结构”“核心架构”“许可证” | 明确定位、启动方式、目录职责、部署选项和来源自身的功能说明 | G1-G5 | 已核验（宣传性结论另标） |
| E4 | Agent API 源码：[app/api/agent](https://github.com/THU-MAIC/OpenMAIC/tree/main/app/api/agent) | `runtime/route.ts`、`sessions/route.ts`、`skills`、`owner-events` | Agent 控制面与 session API 的实际目录证据 | G2-G4 | 已核验 |
| E5 | Runtime 配置源码：[lib/server/agent-runtime/config.ts](https://github.com/THU-MAIC/OpenMAIC/blob/main/lib/server/agent-runtime/config.ts) | `main` /上述 commit；默认值可定位于配置对象 | 扫描、心跳、租约、并发、尝试次数及容量限制 | G3、G4 | 已核验 |
| E6 | Feature flag：[lib/config/feature-flags.ts](https://github.com/THU-MAIC/OpenMAIC/blob/main/lib/config/feature-flags.ts) | 函数 `isAgentRuntimeConfigured()` | runtime 需开关为 true/1 且 `DATABASE_URL` 非空 | G3、G4 | 已核验 |
| E7 | Session 控制面：[app/api/agent/sessions/route.ts](https://github.com/THU-MAIC/OpenMAIC/blob/main/app/api/agent/sessions/route.ts) | POST/GET route；session 创建、材料绑定、排队 | 请求返回后由独立 worker 领取 queued session | G2-G4 | 已核验 |
| E8 | 外部 Agent 技能：[skills/openmaic/SKILL.md](https://github.com/THU-MAIC/OpenMAIC/blob/main/skills/openmaic/SKILL.md) | 标准 `SKILL.md` front matter 与 references | 以确认式 SOP 引导托管、本地启动、生成和二开 | G2-G5 | 已核验 |
| E9 | 内置技能目录：[skills/agent-runtime](https://github.com/THU-MAIC/OpenMAIC/tree/main/skills/agent-runtime) | `curriculum-planner`、`deep-research`、`fact-check`、`slide-craft` 等 | 把具体课程任务拆为可发现、可维护的技能资产 | G2、G3 | 已核验 |
| E10 | 根配置：[package.json](https://github.com/THU-MAIC/OpenMAIC/blob/main/package.json) | `version: 1.0.0`；Node >=22.19；pnpm 10.28；脚本与依赖 | Next.js/React/TypeScript、LangGraph、AI SDK、Postgres 等工程依赖 | G3、G5 | 已核验 |
| E11 | 部署配置：[docker-compose.yml](https://github.com/THU-MAIC/OpenMAIC/blob/main/docker-compose.yml) | `server-persistence` 与 `video-export` profiles | app、PostgreSQL、独立 render-service 及网络隔离 | G3-G5 | 已核验 |
| E12 | 安全与许可证：[LICENSE](https://github.com/THU-MAIC/OpenMAIC/blob/main/LICENSE)、[SECURITY.md](https://github.com/THU-MAIC/OpenMAIC/blob/main/SECURITY.md) | MIT；安全政策支持 active `main` 与最新 major release | 许可、漏洞报告与支持范围可定位 | G4、G5 | 已核验 |
| E13 | 论文链接：[JCST DOI](https://jcst.ict.ac.cn/en/article/doi/10.1007/s11390-025-6000-0) | README 引用；本次未读取论文正文 | 只能证明仓库提供论文链接，不能据此引用论文结论 | G1-G5 | 部分核验/阻塞 |

**G1-G5 说明**：本任务未在仓库中找到 `.claude/commands/research-evidence.md` 的正式文件，因此这里沿用研究协议的保守映射：G1 为权威来源与定位，G2 为产品能力，G3 为运行与工程实现，G4 为安全/隐私/治理，G5 为交付、维护、版本与供应链。该映射不是本仓库的最终定义，需人工确认。

## 3. 官方身份、版本与定位

### 3.1 官方仓库判断

**外部事实**：GitHub 搜索中最匹配的公开仓库是 `THU-MAIC/OpenMAIC`；API 返回公开仓库、默认分支 `main`、TypeScript 语言和 MIT SPDX 许可证。仓库描述为：“Open Multi-Agent Interactive Classroom — Get an immersive, multi-agent learning experience in just one click”。README 中文版第 57-70 行将其称为开源 AI 互动课堂平台，声称可将主题或文档转化为幻灯片、测验、交互模拟和 PBL，并由 AI 教师、AI 同学进行语音讲解、白板绘图与实时讨论。

**来源自身结论**：README 把 v1.0.0 表述为“Build courses with an agent”，并在动态区记录 Agent workbench、durable sessions、session materials、课程工具及内置技能等新增内容。它还将 OpenMAIC Skill 描述为可被 OpenClaw、Codex、DeepSeek、WorkBuddy 等工作台导入的引导式 SOP。

**Claude 分析/推断**：仓库身份由组织名、产品自述、源码结构、版本发布和技能包共同支持，足以作为本次调查的官方主来源；但“官方”在本报告中仅表示 GitHub 上组织 `THU-MAIC` 的公开仓库，不额外推断机构背书、线上服务运营主体或论文作者关系。

### 3.2 版本固定

GitHub Releases API 返回 `v1.0.0` 于 2026-08-27 发布，之前有 `v0.3.2`、`v0.3.1`、`v0.3.0` 等。当前 HEAD 是 2026-09-03 的提交，提交信息涉及 canvas 双击插入文本及相应测试，说明 `main` 仍在快速变化。后续引用必须使用 tag 或完整 commit，不能把 `main` 的即时内容当作稳定接口。

## 4. 工程组成与目录职责

README 中文版“项目结构”段落给出了一套相当完整的产品骨架，关键目录如下：

```text
app/                         Next.js App Router 与页面/API
app/api/                    generate、chat、agent、materials、persistence 等服务端端点
lib/generation/             两阶段大纲到场景的生成流水线
lib/orchestration/          LangGraph director graph、多智能体轮次与 prompt
lib/ai/                     LLM provider 抽象、别名、元数据与流式思考
lib/action/                 语音、白板、聚光灯等课堂动作执行
lib/playback/               idle/playing/live 回放状态机
lib/store/                  Zustand 客户端状态
components/                 编辑器、场景渲染器、聊天、白板、设置和 Agent UI
packages/@openmaic/         dsl、generation、renderer、importer、editor、storage
render-service/             Chromium + FFmpeg 的独立视频渲染服务
skills/openmaic/            面向外部工作台的 SOP 技能
skills/agent-runtime/       内置课程 Agent 技能目录
e2e/、tests/、eval/         E2E、单元测试和编排/PBL/白板评测
scripts/                    构建断言、同步、版本和 smoke test
configs/、public/            共享常量与静态资源
```

`app/api` 的实际目录包含 `agent`、`classroom`、`generate-classroom`、`materials`、`persistence`、`provider`、`web-search`、`export-video`、`transcription`、`quiz-grade`、`parse-pdf` 等。这个结构显示一个重要事实：课堂生成不是孤立的 LLM 调用，而是 API 控制面、材料输入、模型/provider、运行时存储、媒体处理和导出共同组成的生命周期。

`packages/@openmaic/dsl/src` 下有 `runtime.ts`、`storage.ts`、`validate.ts`、`normalize.ts`、`asset-manifest.ts` 等文件；这表明课程数据具有显式 DSL、规范化、校验和资产清单，而不是把任意模型文本直接交给前端。`packages/@openmaic/storage` 则把 Runtime/Document/资产存储抽象及 PostgreSQL、S3 等实现边界独立出来。这个包边界比“所有逻辑放在 agent 文件夹”更适合长期演进。

根 `package.json` 的 `postinstall` 会依次构建 `mathml2omml`、`pptxgenjs`、`@openmaic/dsl`、`generation`、`storage`、`importer`、`renderer`、`editor`，然后运行 `scripts/sync-maic-importer.mjs`。脚本还提供 `dev`、`build`、`start`、`lint`、`test`、`test:e2e`、多个 `eval:*` 与 package tarball smoke test。**分析**：作者把构建、单元测试、浏览器测试、评测和发布包检查纳入同一根入口；**局限**是安装阶段执行多个 build script，供应链审查和缓存复现不可省略。

## 5. Agent 运行机制与数据流

### 5.1 外部入口与内核分层

`skills/openmaic/SKILL.md` 的 front matter 声明该技能覆盖设置、生成和扩展 OpenMAIC，references 进一步拆出 `live-demo.md`、`startup-modes.md`、`provider-keys.md`、`generate-flow.md`、`extend-sdk.md` 等。其核心规则要求“一次推进一个阶段”、任何状态变更前请求确认、不假定外部工作台的模型/API key 会被复用、不要让用户把密钥粘贴到聊天中。

**事实**：此技能是工作台入口和操作 SOP；真正的运行时目录是 `app/api/agent` 与 `lib/server/agent-runtime`。**推断**：OpenMAIC 有意将“如何安全引导用户使用”与“如何执行 Agent session”分成两层，这对 mate 的产品本体、工作机制、实现方式分层具有直接参照价值。

### 5.2 Runtime 开启条件

`lib/config/feature-flags.ts` 的 `isAgentRuntimeConfigured()` 同时检查 `OPENMAIC_AGENT_RUNTIME_ENABLED`（仅 `true`/`1` 开启）与非空 `DATABASE_URL`。`app/api/agent/runtime/route.ts` 返回 enabled/runtimeEnabled 状态，用于区分主动关闭与意图开启但缺少数据库配置。该设计将“功能开关”和“运行前置条件”分开，避免 UI 显示启用却在运行时才失败。

### 5.3 Session 创建、排队和 worker

`app/api/agent/sessions/route.ts` 的 POST 路由解析并校验 `prompt`、`stageId`、`skill`、`existingCourse`、`materialIds`、`courseRefs`，检查 prompt 长度，限制材料 ID 为字符串数组且最多 20 个，并通过 `findSkill()` 校验显式 skill。它解析 owner identity 后调用 durable session store 创建 session；有材料或课程引用时，先绑定材料并写入 opening message，再原子地重新置为 queued，最后返回 HTTP 202。

源码注释的关键原文是：“A separately running worker claims queued sessions after the request has returned.” 因此数据流可概括为：

```text
用户 prompt/材料
  -> POST /api/agent/sessions
  -> owner 与输入校验
  -> durable session store
  -> queued session
  -> 独立 runner claim + lease
  -> Agent tools/skill/prompt
  -> 课程 DSL、消息、材料和事件
  -> classroom/workbench UI 或导出
```

这不是把长任务塞进 HTTP 请求，而是把请求作为控制面，把执行交给可恢复 worker。对需要异步生成课程、长时间研究或多轮辅导的“学业军师”尤其重要。

### 5.4 并发、心跳、租约与配额

`lib/server/agent-runtime/config.ts` 的默认配置包括：`scanIntervalMs=1000`、`heartbeatIntervalMs=2000`、`leaseTtlMs=10000`、`maxConcurrent=2`、`maxAttempts=5`；上下文 compaction 默认关闭。还可通过 `OPENMAIC_AGENT_RUNTIME_*` 环境变量调整。运行时配置中的 `maxUploadBytes` 和 `maxDocumentBytes` 默认 50 MiB，每 owner 的 active materials 默认 100 个、总容量 2 GiB。

`lib/server/agent-runtime/limits.ts` 将 session 文本限制为 `MAX_SESSION_TEXT_LENGTH = 100_000`，注释明确说明目的是避免匿名身份无界提交造成数据库膨胀和无界 LLM 花费。**分析**：这些限制把成本、资源耗尽、孤儿任务和重复领取从“运维经验”提升为显式运行契约；建议 mate 将其写入配额、失败和阶段门槛，而非仅写“系统应稳定”。

### 5.5 工具、提示与课程 DSL

`lib/server/agent-runtime/runner-contract.ts` 引入 `AgentTool`，通过 `assembleRunnerTools(...)` 合并工具组，并将 `DSL_TOOLS_PROMPT` 注入 `courseSystemPrompt(...)`。`lib/orchestration` 下的 `director-graph.ts`、`director-prompt.ts`、`prompt-builder.ts`、`tool-schemas.ts`、summarizers 与 registry 文件共同承担编排、工具 schema、Agent 选择和上下文摘要。根依赖同时包含 `@langchain/langgraph`、AI SDK 和 `@earendil-works/pi-agent-core`。

**来源事实**支持“工具注册—系统提示—状态图—DSL 校验”的链路；**Claude 分析**是，课程 Agent 的可靠性并不只依赖模型能力，还依赖可校验的工具协议、状态对象和输出 DSL。不能从目录存在推断每一种课程场景都已达到生产质量，因此需将具体能力逐项验收。

## 6. 配置、部署与可运维性

README“快速开始”要求 Node.js >=22.19、pnpm >=10，执行 `pnpm install`、复制 `.env.example` 为 `.env.local`、至少配置一个 LLM provider 后运行 `pnpm dev`；生产使用 `pnpm build && pnpm start`。根 `package.json` 固定 package manager 为 pnpm 10.28.0，并有 `check:node-engine`、`check:package-versions`、Prettier、Vitest 和 Playwright 入口。

README 与 `.env.example` 展示 provider-neutral 配置：OpenAI、Azure、Anthropic、Google、Bedrock、DeepSeek、Qwen、Kimi、MiniMax、Grok、OpenRouter、GLM、Ollama、Lemonade、FunASR 等。模型选择由服务端配置控制；这一点在 SKILL.md 中也被强调。**建议**：junshi-app 应建立自己的 provider capability matrix、数据地域和保留策略，不能因为有统一适配层就把所有 provider 当成等价依赖。

`docker-compose.yml` 提供应用、可选 `server-persistence` PostgreSQL 16 和可选 `video-export` render-service。应用可访问 provider 的默认网络，render-service 放在 `internal: true` 的 render 网络；渲染容器使用 Chromium + FFmpeg，并有并发、内存、共享内存及外连限制配置。README 还说明 PostgreSQL 持久化包含 Runtime/Document 契约，资产可直接出站或通过签名 S3 URL 间接出站。

**可运维启示**：独立渲染服务把高资源、潜在不可信的浏览器执行环境从主应用隔离；健康检查、feature flag、容量配额、worker lease 和可选 profile 使部署可以按能力启用。但本次没有启动 compose，不能声称 iptables、健康检查、PostgreSQL migration 或视频导出实际通过。

## 7. 安全、隐私、供应链与回滚风险

### 7.1 安全和隐私

源码有 owner-scoped session/material 查询、文本/材料容量限制、ACCESS_CODE 和 render 网络隔离等机制。另一方面，源码注释指出上游 classroom 尚未携带 owner partition，`existing-course` 的完整存在性和 ownership 验证被延迟到后续使用阶段。这是反向证据：多租户对象引用不能只校验 ID 格式，必须在进入 session、读取材料和导出时都做授权。

云端 LLM、搜索、媒体、ASR、文档解析和 Live Demo 意味着 prompt、材料、音频或生成结果可能离开本机。需逐 provider 核查训练使用、保留期限、地区、日志和删除政策；不能把“provider-neutral”理解为“隐私-neutral”。`NEXT_PUBLIC_*` 变量会进入浏览器 bundle，任何公开持有的 token 都不能被当作严格密钥。部署方还须审查 URL 抓取、媒体代理、PDF/OCR、外部资源内联和浏览器渲染的 SSRF、恶意文件、XSS 与数据外传风险。

### 7.2 许可证和供应链

根 LICENSE 与 `package.json` 标注 MIT，README 还说明 `packages/mathml2omml` 保留 LGPL-3.0-or-later，`packages/pptxgenjs` 为 MIT（第三方）。不能以根 MIT 推断所有依赖均为 MIT。主要依赖包括 Next.js 16.1.2、React 19.2.3、TypeScript 5、LangGraph 1.1.1、AI SDK、MCP SDK、AWS/云 provider SDK、`pg`、Playwright 和本地 workspace 包。`pnpm-lock.yaml` 存在，但本次未解析全部传递依赖 license/integrity。

风险包括：postinstall 执行多包构建；Docker 使用如 `postgres:16` 的可变 tag；Chromium、FFmpeg、FunASR、vLLM、模型和基础镜像不完全受 npm lock 管理；可配置 `OPENMAIC_AGENT_SKILLS_DIR` 若指向不可信目录，可能改变工具和提示。采用前应固定 commit/tag、lockfile、镜像 digest、系统工具版本，并进行 license、SBOM、签名和依赖漏洞审查。

### 7.3 回滚

release tags、Dockerfile、lockfile 为回滚基础，但 session/material 数据库 schema、volume、技能版本和 provider 行为可能跨版本不兼容。回滚不能只替换应用镜像：应备份数据库和 named volume，在副本上演练 migration、旧版读取、session 恢复、材料导出和 render 结果；同时记录 Node、Chromium、FFmpeg、镜像 digest 及模型版本。`SECURITY.md` 仅承诺支持最新 major release 和 active `main`，更增加了长期运行版本自行维护的责任。

## 8. 对 mate 与 junshi-app 的启示

### 8.1 对 mate 元文档

1. **补齐运行机制章节**：把 Agent 的输入、session 状态、队列、worker、租约、心跳、重试、取消、恢复、上下文压缩和配额写成可验证契约。
2. **分离入口 SOP 与产品内核**：参考 `skills/openmaic/SKILL.md` 与 `references/`，将面向 Agent/用户的确认式使用流程与内部编排、工具和提示定义分开，避免把操作说明混入产品本体。
3. **建立能力与责任矩阵**：将模型调用、搜索、文档解析、媒体、记忆/知识、课程 DSL、渲染、导入、存储和导出分别定义 owner、输入输出、失败边界和隐私级别。
4. **把 DSL/Schema 当作领域边界**：课程结构、动作、资产和持久化对象应有版本化 schema、校验和迁移规则；提示词不能代替结构化约束。
5. **把安全反例写进决策登记**：owner 授权、外部 URL、材料隔离、公开 token、渲染沙箱、密钥管理和 provider 数据政策应成为阶段门槛。
6. **把供应链与回滚列为正式内容**：锁文件、镜像 digest、SBOM、第三方许可证、数据库备份、schema 回滚与模型版本都不能只放在开发者个人经验里。

这些均为**候选/参照**，需要产品发起人确认后才能升级为 mate 决策；本报告不改写 mate 正文。

### 8.2 对 junshi-app 代码库目录

可考虑在既有结构中确保以下职责有明确落点，而不是按某个外部仓库原样复制：

```text
agent/          session、worker、lease、tool registry、prompt contract
orchestration/  状态图、路由、上下文摘要和多智能体协作
models/         provider adapter、模型能力与成本策略
materials/      上传、解析、病毒/格式检查、生命周期与配额
knowledge/      检索、索引、引用和删除
contracts/      DSL、API、事件、schema 版本与迁移
storage/        runtime/document/blob 抽象及实现
api/            控制面、流式事件、认证和授权
web/            页面、课堂回放、编辑器与状态投影
workers/        异步任务、重试、可观测性和停机处理
rendering/      隔离渲染服务、资源白名单与导出
ops/            compose、部署、备份、迁移、监控和回滚
skills/         轻量入口与按需 references；不把 secrets 放入 skill
scripts/、tests/、e2e/、eval/  工程检查、回归和质量门槛
```

依赖关系应保持单向：API 负责鉴权和提交，不直接承载长任务；worker 调用 Agent/工具协议并写入持久化；前端订阅事件或读取投影；DSL/schema 约束跨层数据；provider 与外部服务由适配层隔离；rendering 使用独立权限和网络。当前只是结构建议，需结合 `STRUCTURE.md`、mate 决策和本地代码实际状态验证。

## 9. 不适合直接照搬的部分与局限

- **功能宣传未独立实测**：README 的“20+ 工作台”“多种场景”“持久化恢复”等不能替代本地运行、E2E 和性能测试。
- **版本快速变化**：main 在本次访问日仍有新提交，文件、模型名称和默认值可能改变。
- **租户隔离存在明确缺口线索**：既有课程 ownership 延迟验证不适合作为学业数据的默认安全模型。
- **开发配置不是生产配置**：默认 PostgreSQL 密码、ACCESS_CODE 和公开编译 token 均不能直接用于多租户生产。
- **生态依赖复杂**：云 provider、浏览器、FFmpeg、OCR、TTS/ASR 和 npm 依赖带来地区、费用、许可证与供应链差异。
- **无法从目录推断质量**：本报告没有运行服务、测试、数据库、网络沙箱或安全扫描，所有运行质量结论均应标为待复核。
- **论文证据阻塞**：README 仅提供 JCST DOI；本次没有核验论文版本、发布日期、章节/页码或 arXiv ID，因此论文不作为产品决策依据。

## 10. 最终适配判断与验证清单

**外部事实**：OpenMAIC 已形成较完整的 Agent 课堂工程闭环，实际可定位到 API、runtime、技能、DSL、workspace 包、测试/评测和部署配置。

**Claude 分析**：对学业军师最可迁移的是生命周期和边界治理，而不是其教育场景 UI。优先级建议为：

1. 先验证本地是否需要 durable session 与独立 worker；
2. 再定义 session/material/course 的授权与数据生命周期；
3. 再建立 DSL、工具 schema、事件和迁移契约；
4. 最后选择 provider、渲染、导出和工作台集成。

**本仓库候选建议状态**：候选/参照；未经用户或产品发起人确认，不升级为最终确认。

采用前的最小本地验证清单：

- 固定并记录 OpenMAIC tag/commit，逐行核对引用链接；
- 对本地 mate 的 G1-G5 定义进行人工确认；
- 在隔离环境执行 install、lint、unit、E2E 和相关 eval；
- 用 PostgreSQL 副本验证 session 排队、lease 超时、重试、取消和恢复；
- 测试 owner 跨对象读取/写入、材料删除、导出和公开链接授权；
- 对 provider、搜索、文档解析、音视频和 render-service 做数据流与 SSRF 审查；
- 生成依赖 SBOM，核对第三方许可证、镜像 digest、系统工具和模型条款；
- 演练 schema、数据库、对象存储、技能版本和应用镜像的联合回滚。

## 11. Skill 使用、工具与验证记录

- **阶段**：外部仓库调查与独立报告撰写。
- **任务类型**：GitHub 研究、源码/配置取证、Markdown 报告。
- **目标与成功标准**：核实官方仓库；引用实际源码、目录、配置和运行机制；报告不少于 2500 字；事实、来源结论、推断、建议和局限分离；覆盖 G1-G5、许可证、依赖、部署、网络、隐私、供应链和回滚风险；仅写入指定报告。
- **能力发现**：仓库内未找到 `.claude/commands/research-evidence.md`；可用全局/插件能力中实际调用了 `skill-first`、`agent-reach`、`md-writing` 和研究 agent。`agent-reach` 的 GitHub 路由实际可用；其 doctor 对 GitHub 的 `active_backend` 为 null，但公开 API 访问由 `gh` 成功完成。
- **实际调用**：`skill-first`（完成任务界定与能力路由）；`agent-reach`（完成 GitHub 路由、运行 `agent-reach check-update`，结果 v1.5.0 已是最新）；`md-writing`（确定研究报告骨架、事实/判断分层和可扫描结构）；研究 agent（只读复核官方仓库、版本、源码目录、runtime、配置、安全和许可证，返回证据表）。
- **实际工具**：`gh search repos "OpenMAIC"`、`gh api` 读取仓库元数据、commit、tree、README、SKILL.md、package.json 等公开内容；未使用写操作、克隆、安装或部署。访问日期均为 2026-09-03。
- **输入**：用户任务书 `/Users/caibiao/orca/projects/junshi-app/计划书`；目标 GitHub 仓库及其公开路径。
- **输出**：当前文件 `/Users/caibiao/orca/projects/junshi-app/.claude/worktrees/agent-ad607f48938cbe9bb/调研报告/OpenMAIC调查报告.md`。
- **Markdown 专项**：已实际调用 `md-writing`；采用“摘要—证据—事实/分析—运行机制—风险—适配—局限—验证”的研究报告骨架。
- **阻塞/降级**：未找到 `research-evidence.md`；因此按现有任务书和 skill-first 记录字段保守执行。论文正文、完整 `.env.example`、所有传递依赖 license/integrity、实际运行结果未核验，均在报告中标明。
- **未调用项及理由**：未调用 crawl4ai，因为 GitHub API 已能读取所需公开源码；未调用 playwright-cli，因为本次不需要浏览器交互；未调用 Context7，因为研究对象是仓库自身而非库文档。
- **验证**：使用 `wc -m` 检查报告长度；使用 `git diff --check -- 调研报告/OpenMAIC调查报告.md` 检查 Markdown 空白错误；使用 `git status --short` 确认只新增指定报告；未执行 OpenMAIC 安装、构建、测试或服务启动。
- **下一步**：由主 Agent 进行内容审阅、与本地 G1-G5 定义及 mate/STRUCTURE 交叉核对；如需采纳，先取得产品发起人确认，再将候选建议转为本地决策。
