# AutoGPT 工程代码库目录框架图

> **性质：候选归纳**。本图依据 `/Users/caibiao/Downloads/AutoGPT-master` 的目录与文件名进行只读盘点；深度最多两层，不读取实现代码正文。职责是按路径命名和目录位置作出的结构性归纳，无法仅凭目录确认的内容标注为“待核验”。

## 顶层结构

├── `assets/`  → 职责：存放项目使用的静态资源与素材。
├── `autogpt_platform/`  → 职责：承载当前 AutoGPT Platform 的平台化产品、服务、客户端与部署工程。
├── `classic/`  → 职责：承载经典版 AutoGPT、Forge 开发框架及其基准测试等历史/兼容工程。
├── `docs/`  → 职责：按 classic、home、integrations、platform 分域维护项目文档站内容。
├── `.github/`  → 职责：维护 GitHub 协作配置、自动化脚本、Issue/PR 模板与 CI/CD 工作流。
├── `.claude/`  → 职责：提供仓库内 Claude 相关技能配置；具体运行边界待核验。
├── `AGENTS.md`  → 职责：提供仓库级智能体协作说明。
├── `CLAUDE.md`  → 职责：提供仓库级 Claude 工作说明与约束。
├── `CITATION.cff`  → 职责：提供软件引用元数据。
├── `CODE_OF_CONDUCT.md`  → 职责：规定社区行为准则。
├── `CONTRIBUTING.md`  → 职责：说明贡献流程与协作要求。
├── `LICENSE`  → 职责：声明项目许可条款。
├── `SECURITY.md`  → 职责：说明安全问题报告与处理规则。
├── `codecov.yml`  → 职责：配置 Codecov 覆盖率集成；具体门槛待核验。
├── `orca.yaml`  → 职责：提供 Orca 工作区或自动化配置；具体字段职责待核验。
└── `README.md`  → 职责：提供项目总览、入口说明与使用导航。

## 第二层（职责相关的主要子目录）

├── `autogpt_platform/`
│   ├── `analytics/`  → 职责：存放平台分析相关资源与查询；具体分析链路待核验。
│   ├── `autogpt_libs/`  → 职责：提供可复用的 AutoGPT 平台共享 Python 库。
│   ├── `backend/`  → 职责：承载平台后端服务、Agent 资源、数据库迁移、负载测试与后端测试。
│   ├── `db/`  → 职责：提供数据库容器与初始化相关资源。
│   ├── `frontend/`  → 职责：承载平台前端应用、公共资源、脚本与前端测试配置。
│   ├── `graph_templates/`  → 职责：存放可导入或复用的 Agent 图模板 JSON 文件。
│   ├── `installer/`  → 职责：提供平台安装引导脚本（Windows 与 Unix shell）。
│   ├── `single-container/`  → 职责：编排单容器部署所需的入口、服务运行脚本、代理与依赖配置。
│   ├── `docker-compose.yml`  → 职责：定义平台本地/通用多容器编排入口；具体服务集合待核验。
│   ├── `docker-compose.platform.yml`  → 职责：定义平台部署场景的容器编排覆盖配置。
│   ├── `Makefile`  → 职责：提供平台工程常用任务入口。
│   ├── `cloudflare_worker.js`  → 职责：提供 Cloudflare Worker 部署单元；具体请求职责待核验。
│   ├── `README.md`  → 职责：说明平台子工程的启动、使用或开发入口。
│   └── `LICENSE.md`  → 职责：声明平台子工程许可信息。

├── `classic/`
│   ├── `direct_benchmark/`  → 职责：承载直接基准测试、挑战数据、分析脚本与基准测试入口。
│   ├── `forge/`  → 职责：承载经典 AutoGPT 的 Forge 开发框架、配置、镜像与测试。
│   ├── `original_autogpt/`  → 职责：承载原始经典 AutoGPT 应用、插件、数据、脚本、文档与测试。
│   ├── `reports/`  → 职责：存放经典工程生成或汇总的报告；具体报告生产流程待核验。
│   ├── `pyproject.toml`  → 职责：定义 classic 区域 Python 工程元数据与依赖配置。
│   ├── `poetry.lock`  → 职责：锁定 classic 区域 Python 依赖版本。
│   ├── `Dockerfile.autogpt`  → 职责：定义经典 AutoGPT 容器构建方式。
│   ├── `README.md`  → 职责：提供 classic 区域总览与入口说明。
│   ├── `SECURITY.md`  → 职责：提供 classic 区域安全说明。
│   └── `TROUBLESHOOTING.md`  → 职责：提供 classic 区域问题排查说明。

├── `docs/`
│   ├── `content/`  → 职责：维护经典版、挑战、贡献等通用文档内容。
│   ├── `home/`  → 职责：维护文档站首页、导航与目录结构。
│   ├── `integrations/`  → 职责：维护集成说明、集成区导航及区块集成文档。
│   ├── `platform/`  → 职责：维护平台使用、开发、部署、集成和功能说明。
│   ├── `AGENTS.md`  → 职责：提供文档目录的智能体协作说明。
│   └── `CLAUDE.md`  → 职责：提供文档目录的 Claude 工作说明与约束。

└── `.github/`
    ├── `workflows/`  → 职责：定义 CI、测试、发布、部署、依赖维护与仓库治理自动化。
    ├── `scripts/`  → 职责：存放 GitHub Actions 与协作流程使用的辅助脚本。
    ├── `batch-bot/`  → 职责：承载批处理机器人及其说明；具体事件流程待核验。
    ├── `ISSUE_TEMPLATE/`  → 职责：提供 Bug 与 Feature Issue 模板。
    ├── `CODEOWNERS`  → 职责：声明路径到代码所有者的审查责任映射。
    ├── `PULL_REQUEST_TEMPLATE.md`  → 职责：提供 Pull Request 描述模板。
    ├── `dependabot.yml`  → 职责：配置依赖更新机器人。
    ├── `labeler.yml`  → 职责：配置基于变更路径或规则的自动标签；具体规则待核验。
    └── `copilot-instructions.md`  → 职责：提供 GitHub Copilot 协作指引。
