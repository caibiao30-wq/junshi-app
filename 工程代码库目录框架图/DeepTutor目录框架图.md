# DeepTutor 工程代码库目录框架图

> **状态：候选归纳（非产品决策、非通用模板）**
> 仅根据 /Users/caibiao/Downloads/DeepTutor-main 本地目录布局归纳，未读代码正文、未联网核验。目录名反映职责，职责为推断；凡无法从命名确认的均标注「待核验」。

## 顶层结构

```
├── deeptutor/          → 职责：后端核心 Python 包（业务逻辑/领域分层主域）
├── deeptutor_cli/      → 职责：命令行客户端（Chat/Book/Memory/KB/Skill/Plugin 等子命令）
├── deeptutor_web/      → 职责：Web 侧 Python 包（后端与前端之间的桥接/入口，容器仅 __init__，待核验）
├── web/                → 职责：前端 Web 应用（Next.js/TypeScript 主域）
├── tests/              → 职责：测试套件（按 deeptutor 同名域镜像存放）
├── scripts/            → 职责：工程/运维脚本（启动、检查、导出、安装等）
├── requirements/       → 职责：分环境的 Python 依赖清单（server/cli/dev/matrix/partners 等）
├── packaging/          → 职责：打包发布相关（deeptutor-cli 打包元数据）
├── assets/             → 职责：静态资源（图文、发布、角色清单）
├── docs/               → 职责：设计与架构文档（ADR、计划）
├── .github/            → 职责：GitHub 工作流与 Issue/PR 模板
├── deeptutor          【dir 上方已列，占位勿计】
```

### 顶层文件（根目录）

```
├── pyproject.toml                  → 职责：Python 包构建/元数据/依赖声明（现代打包规范）
├── requirements.txt                → 职责：汇总依赖入口
├── Dockerfile                      → 职责：主容器镜像构建
├── Dockerfile.runner               → 职责：执行器（runner）镜像构建
├── compose.yaml / docker-compose*.yml  → 职责：多服务编排（容器化部署拓扑）
├── README.md                       → 职责：项目总说明与使用指南
├── AGENTS.md                       → 职责：面向 Agent 的开发协作约定
├── SKILL.md                        → 职责：DeepTutor 对外呈现的技能类接口说明（待核验）
├── CONTAINERIZATION.md             → 职责：容器化方案说明
├── CONTRIBUTING.md                 → 职责：贡献指南
├── KNOWLEDGE_MIGRATION.md          → 职责：旧知识迁移说明
├── READING_EXTENSIONS.md           → 职责：阅读能力扩展说明
├── REASONING_SAFETY_CHECKLIST.md   → 职责：推理安全核对清单
├── THIRD_PARTY_NOTICES.md          → 职责：第三方组件声明
├── CITATION.cff / Communication.md / LICENSE / MANIFEST.in  → 职责：项目元数据、交流说明、许可、打包清单
├── .env.example / .gitignore / .dockerignore / .gitattributes → 职责：配置样例与仓库/构建忽略规则
├── .secrets.baseline / .pre-commit-config.yaml / .importlinter / pyproject.toml → 职责：静态安全/提交钩子/导入边界检查
├── .ToolsMCP 相关：.importlinter  → 职责：（上层已并入，略）
```

## 第二层（职责相关的主要子目录）

### deeptutor/（后端核心包，按职责分域）

```
├── agents/         → 职责：多智能体编排层
├── api/            → 职责：对外接口/API 层
├── app/            → 职责：应用生命周期/装配层
├── book/           → 职责：书籍/教材知识域
├── capabilities/   → 职责：能力模块（扩展能力集）
├── co_writer/      → 职责：协同写作域
├── config/         → 职责：配置管理与加载
├── core/           → 职责：核心机制（引擎级基础设施）
├── events/         → 职责：事件定义与分发
├── i18n/           → 职责：国际化
├── knowledge/      → 职责：知识库/知识管理域
├── learning/       → 职责：学习域（学习方法论/教学逻辑）
├── logging/        → 职责：日志
├── multi_user/     → 职责：多用户/多账号域
├── partners/       → 职责：第三方合作方集成
├── plugins/        → 职责：插件机制
├── reading/        → 职责：阅读理解域
├── runtime/        → 职责：运行时执行环境
├── services/       → 职责：业务服务层
├── skills/         → 职责：技能注册与编排
├── tools/          → 职责：工具集合（工具调用）
├── utils/          → 职责：通用工具函数
├── video_learning/ → 职责：视频学习域
└── visualizers/    → 职责：可视化呈现
```

### web/（前端 Next.js/TS 应用）

```
├── app/        → 职责：Next.js App Router 页面/路由
├── components/ → 职责：UI 组件
├── features/   → 职责：按功能域组织的前端模块
├── hooks/      → 职责：React Hooks
├── context/    → 职责：React Context（全局状态）
├── lib/        → 职责：前端通用库/工具
├── shared/     → 职责：跨前端共享代码
├── contracts/  → 职责：前端与后端契约/类型定义
├── types/      → 职责：TS 类型定义
├── i18n/       → 职责：国际化
├── locales/    → 职责：多语言文案包
├── public/     → 职责：静态公开资源
├── scripts/    → 职责：前端工程脚本
├── tests/      → 职责：前端测试
├── vendor/     → 职责：第三方（vendored）代码
└── eslint/     → 职责：ESLint 相关配置/规则
```

> 排查辅助：`.dependency-cruiser.cjs`、`playwright.config.ts`、`vitest.config.mts`、`next.config.js`、`tailwind.config.js`、`proxy.ts`、`tsconfig*.json`、`package.json` 均为前端工程/测试/构建配置文件，职责见其名。

### deeptutor_cli/（命令行客户端）

```
├── __main__.py / main.py → 职责：CLI 入口/命令主分发
├── chat.py / book.py / notebook.py / memory.py → 职责：对话/书籍/笔记本/记忆 子命令
├── kb.py / skill.py / skill_login.py / skill_prompts.py → 职责：知识库/技能 子命令
├── plugin.py / partner.py / provider_cmd.py → 职责：插件/合作方/模型提供商 子命令
├── config_cmd.py / init_cmd.py / init_wizard.py / session_cmd.py / doctor.py → 职责：配置/初始化/会话/诊断 子命令
├── common.py / _tool_result.py → 职责：CLI 公共工具与工具结果处理
└── README.md → 职责：CLI 使用说明
```

### tests/（测试套件，按后端域镜像）

```
├── agents/、api/、app/、book/、capabilities/、core/、knowledge/、logging/、multi_user/、partners/、plugins/、reading/、runtime/、services/、tools/、utils/、video_learning/、visualizers/
│   → 职责：与 deeptutor 同名域对应的测试
├── cli/       → 职责：CLI 测试
├── scripts/   → 职责：工程脚本测试
├── architecture/ → 职责：架构/导入边界测试
├── fixtures/  → 职责：测试夹具/数据
└── 顶层 *_test.py（test_matrix_requirements / test_packaging_metadata / test_release_workflow_guards）→ 职责：矩阵依赖/打包元数据/发布流程守卫测试
```

### scripts/（工程脚本）

```
├── start_backend.bat / start_frontend.bat / start_web.py / start_tour.py → 职责：后端/前端/Web/导览 启动脚本
├── check_architecture.py / check_branch_policy.py / check_repo_hygiene.py / check_workspace_hygiene.py → 职责：架构/分支策略/仓库/工作区 卫生检查
├── export_discord_history.py / export_frontend_contracts.py → 职责：Discord 历史与前端契约导出
├── pb_setup.py / install_extras.py / update.py / docker_compose.py → 职责：环境搭建/扩展安装/更新/编排辅助
├── prepare_web_package.py → 职责：Web 打包准备
├── _cli_kit.py → 职责：脚本公共脚手架
└── hooks/    → 职责：预提交等 Git 钩子脚本
```

### requirements/（依赖清单）

```
└── server.txt / cli.txt / dev.txt / matrix.txt / matrix-e2e.txt / partners.txt / rag-rerank.txt / video-learning.txt / math-animator.txt → 职责：各运行/开发环境的 Python 依赖拆分
```

### assets/、docs/、packaging/、.github/

```
├── assets/
│   ├── figs/     → 职责：文档配图
│   ├── README/   → 职责：资产目录说明（待核验）
│   ├── releases/ → 职责：发布产物
│   └── roster/   → 职责：成员/名单相关（待核验）
├── docs/
│   ├── adr/   → 职责：架构决策记录（ADR）
│   └── plans/ → 职责：计划文档
├── packaging/deeptutor-cli/ → 职责：deeptutor-cli 打包元数据
└── .github/
    ├── workflows/ → 职责：CI/CD 工作流
    ├── ISSUE_TEMPLATE/ → 职责：Issue 模板
    ├── pull_request_template.md → 职责：PR 模板
    └── pull.yml → 职责：自动同步（PULL）配置
```

---

## 边界与说明

- 深度受限为两层，第三层及代码正文未读取；个别条目（deeptutor_web、assets/README-roster、SKILL.md）职责仅能推断至「待核验」。
- 本图仅描述目录布局与命名推断的职责，不升级为产品决策或通用模板。