# OpenHands 工程代码库目录框架图

> **归纳性质：候选归纳**。本图依据本地目录 `/Users/caibiao/Downloads/OpenHands-main` 的实际布局整理，仅展示两层：顶层及其职责相关的主要直属子目录/文件；未读取代码正文，不将本图升级为产品决策或通用模板。职责说明主要依据目录/文件命名及仓库布局，无法仅凭目录确认的项目语义标注为“待核验”。

## 顶层结构

├── `.agents/` → 职责：存放 Agent/开发协作相关配置或技能资产。
├── `.github/` → 职责：承载 GitHub 协作、自动化工作流、发布和问题模板配置。
├── `.husky/` → 职责：承载 Git hooks 配置，用于提交等阶段的自动检查。
├── `.openhands/` → 职责：提供 OpenHands 项目本地初始化或设置脚本。
├── `__mocks__/` → 职责：存放测试框架或依赖的全局模拟实现。
├── `__tests__/` → 职责：集中存放按 API、组件、路由、Hook 等划分的测试资产。
├── `bin/` → 职责：提供可执行的项目命令入口。
├── `config/` → 职责：提供运行时或应用默认配置数据。
├── `docker/` → 职责：提供 Docker 镜像构建与容器启动配置。
├── `docs/` → 职责：维护架构、开发、自托管、测试及相关项目说明文档。
├── `electron/` → 职责：承载 Electron 桌面端主进程、预加载、构建资源和桌面封装代码。
├── `examples/` → 职责：提供可运行或可参考的部署/集成示例。
├── `helm/` → 职责：提供 Kubernetes Helm 部署编排。
├── `public/` → 职责：提供无需打包处理的 Web 静态资源、图标、清单及 Mock Service Worker。
├── `scripts/` → 职责：承载开发、构建、静态服务、依赖下载、国际化和辅助检查脚本。
├── `specs/` → 职责：记录特定功能或行为的规格说明。
├── `src/` → 职责：承载 Web 应用的主要 TypeScript/React 源代码、资源、状态和路由。
├── `tests/` → 职责：承载独立于集中测试目录的端到端测试入口或资产。
├── `tools/` → 职责：提供面向特定功能的辅助工具脚本。
├── `.dockerignore` → 职责：声明 Docker 构建上下文中应忽略的文件。
├── `.env.sample` → 职责：提供环境变量配置示例。
├── `.gitattributes` → 职责：声明 Git 路径属性和文本处理规则。
├── `.gitignore` → 职责：声明 Git 不纳入版本控制的文件。
├── `.npmignore` → 职责：声明发布 npm 包时应排除的文件。
├── `.prettierrc.json` → 职责：定义 Prettier 代码格式化规则。
├── `.release-please-manifest.json` → 职责：记录 release-please 的版本清单状态。
├── `AGENTS.md` → 职责：提供 Agent/贡献者工作约定；具体适用范围待核验。
├── `CHANGELOG.md` → 职责：记录版本变更历史。
├── `LICENSE` → 职责：声明项目许可条款。
├── `README.md` → 职责：提供项目入口说明、使用和开发概览。
├── `README.windows.md` → 职责：提供 Windows 环境下的项目说明。
├── `electron-builder.config.mjs` → 职责：配置 Electron 应用打包与发布参数。
├── `eslint.config.js` → 职责：配置 ESLint 静态检查规则。
├── `global.d.ts` → 职责：声明全局 TypeScript 类型。
├── `hero.ts` → 职责：提供名为 hero 的独立 TypeScript 入口或功能；具体职责待核验。
├── `package.json` → 职责：声明 JavaScript 项目元数据、依赖和 npm scripts。
├── `package-lock.json` → 职责：锁定 npm 依赖解析结果。
├── `playwright.config.ts` → 职责：配置 Playwright 测试。
├── `playwright.live.config.ts` → 职责：配置面向真实服务/在线环境的 Playwright 测试；具体运行边界待核验。
├── `playwright.mock-llm.config.ts` → 职责：配置 Mock LLM 场景的 Playwright 测试。
├── `playwright.mock-llm-docker.config.ts` → 职责：配置 Docker Mock LLM 场景的 Playwright 测试。
├── `react-router.config.ts` → 职责：配置 React Router 应用构建或路由行为。
├── `release-please-config.json` → 职责：配置 release-please 的版本发布流程。
├── `stryker.config.mjs` → 职责：配置 JavaScript/TypeScript 变异测试。
├── `tailwind.config.js` → 职责：配置 Tailwind CSS 样式生成。
├── `test-utils.tsx` → 职责：提供测试用 React 辅助工具。
├── `tsconfig.json` → 职责：配置主 TypeScript 编译检查。
├── `tsconfig.lib.json` → 职责：配置库构建或库入口相关的 TypeScript 编译选项。
├── `vercel.json` → 职责：配置 Vercel 部署行为。
├── `vite-env.d.ts` → 职责：声明 Vite 环境相关 TypeScript 类型。
├── `vite.config.ts` → 职责：配置 Vite 开发服务器、构建和插件。
└── `vitest.setup.ts` → 职责：配置 Vitest 测试初始化环境。

## 第二层（职责相关的主要子目录）

├── `.agents/`
│   └── `skills/` → 职责：存放项目或 Agent 可调用的技能定义。
├── `.github/`
│   ├── `ISSUE_TEMPLATE/` → 职责：提供 GitHub issue 模板。
│   ├── `pr-assets/` → 职责：存放 Pull Request 相关展示资源。
│   ├── `scripts/` → 职责：存放 GitHub 自动化辅助脚本。
│   └── `workflows/` → 职责：定义 GitHub Actions 持续集成、检查或发布流程。
├── `__tests__/`
│   ├── `api/` → 职责：测试 API 层行为。
│   ├── `bin/` → 职责：测试命令入口行为。
│   ├── `components/` → 职责：测试 React 组件。
│   ├── `constants/` → 职责：测试常量相关逻辑。
│   ├── `contexts/` → 职责：测试 React Context 和 Provider 行为。
│   ├── `e2e/` → 职责：存放端到端测试。
│   ├── `fixtures/` → 职责：提供测试夹具和固定测试数据。
│   ├── `github-workflows/` → 职责：测试 GitHub Actions 工作流相关内容。
│   ├── `helpers/` → 职责：提供测试辅助函数。
│   ├── `hooks/` → 职责：测试 React hooks。
│   ├── `i18n/` → 职责：测试国际化相关行为。
│   ├── `manifests/` → 职责：测试 manifest 及其校验/注册相关行为。
│   ├── `mocks/` → 职责：集中提供测试模拟对象和模拟服务。
│   └── `routes/` → 职责：测试应用路由和页面级行为。
├── `electron/`
│   ├── `build-resources/` → 职责：提供桌面应用打包所需的图标等资源。
│   ├── `lib/` → 职责：提供 Electron 主进程使用的桌面端辅助模块。
│   ├── `loading.html` → 职责：提供 Electron 启动期间的加载页面。
│   ├── `main.mjs` → 职责：作为 Electron 主进程入口。
│   ├── `package.json` → 职责：声明 Electron 子项目元数据和依赖。
│   └── `preload.cjs` → 职责：作为 Electron 渲染器与主进程之间的预加载桥接入口。
├── `src/`
│   ├── `api/` → 职责：封装后端、Agent、云端、自动化、文件和画布等 API 访问。
│   ├── `assets/` → 职责：存放需由前端构建处理的静态资源。
│   ├── `components/` → 职责：按浏览器、会话、文件、设置、侧栏、终端等职责组织 React UI 组件。
│   ├── `constants/` → 职责：集中定义应用常量。
│   ├── `context/` → 职责：提供导航、滚动等基础 React Context。
│   ├── `contexts/` → 职责：提供活动后端、会话 WebSocket、设置区等应用级 Context/Provider。
│   ├── `dev/` → 职责：承载开发环境专用代码或调试辅助；具体内容待核验。
│   ├── `extensions/` → 职责：承载画布扩展模块加载能力。
│   ├── `fixtures/` → 职责：提供应用演示和测试用固定会话/自动化数据。
│   ├── `hooks/` → 职责：集中提供 React hooks 及其按查询、变更等场景的组织。
│   ├── `i18n/` → 职责：承载国际化资源和本地化逻辑。
│   ├── `icons/` → 职责：存放应用图标组件或图标资源。
│   ├── `lib/` → 职责：提供可复用的库级入口或基础封装；具体职责待核验。
│   ├── `manifests/` → 职责：定义 manifest 类型、能力、来源、注册、校验和错误映射。
│   ├── `mocks/` → 职责：提供应用运行/测试所需的模拟数据或模拟服务。
│   ├── `routes/` → 职责：实现页面级路由及各功能页面。
│   ├── `services/` → 职责：承载 Agent 状态、聊天、画布、设置、遥测等业务服务。
│   ├── `stores/` → 职责：集中管理 Agent、会话、浏览器、文件、模型等客户端状态。
│   ├── `styles/` → 职责：组织应用样式资源。
│   ├── `themes/` → 职责：组织主题定义和主题切换相关资源。
│   ├── `types/` → 职责：集中定义 TypeScript 类型。
│   ├── `ui/` → 职责：提供通用 UI 基础层；具体组件边界待核验。
│   ├── `utils/` → 职责：提供跨模块通用工具函数。
│   ├── `wrapper/` → 职责：提供应用事件处理等外围包装组件。
│   ├── `entry.client.tsx` → 职责：作为客户端应用启动入口。
│   ├── `index.ts` → 职责：提供源代码公共导出或入口；具体导出范围待核验。
│   ├── `index.css` → 职责：提供全局 CSS 入口样式。
│   ├── `root.tsx` → 职责：定义应用根组件和根级渲染结构。
│   ├── `routes.ts` → 职责：集中声明应用路由配置。
│   ├── `tailwind.css` → 职责：提供 Tailwind CSS 层和应用样式入口。
│   └── `query-client-config.ts` → 职责：配置客户端查询缓存/请求管理。
├── `public/`
│   ├── `mockServiceWorker.js` → 职责：提供 Mock Service Worker 的浏览器端服务 worker。
│   ├── `site.webmanifest` → 职责：声明 Web 应用安装及展示元数据。
│   └── `robots.txt` → 职责：声明爬虫访问规则。
├── `scripts/`
│   ├── `dev-*.mjs` → 职责：提供开发服务器、开发进程和开发环境辅助脚本。
│   ├── `docker-build.mjs` → 职责：自动化 Docker 构建。
│   ├── `download-node.mjs` → 职责：下载或准备 Node.js 运行时。
│   ├── `download-uv.mjs` → 职责：下载或准备 uv 工具链。
│   ├── `generate-icons.mjs` → 职责：生成应用图标。
│   ├── `make-i18n-translations.cjs` → 职责：生成或整理国际化翻译资源。
│   ├── `static-*.mjs` → 职责：构建和启动静态站点服务。
│   └── `check-*.cjs` → 职责：执行版本同步、翻译完整性等自动检查。
├── `docs/`
│   ├── `architecture.md` → 职责：记录系统架构说明。
│   ├── `DEVELOPMENT.md` → 职责：记录开发流程和环境说明。
│   ├── `SELF_HOSTING.md` → 职责：记录自托管部署说明。
│   ├── `TESTING_MATRIX.md` → 职责：记录测试矩阵。
│   └── `README.md` → 职责：提供文档区索引或总览。
├── `specs/`
│   ├── `backend-management.md` → 职责：描述后端管理功能规格。
│   ├── `canvas-extensions.md` → 职责：描述画布扩展功能规格。
│   ├── `llm-defaults.md` → 职责：描述 LLM 默认配置规格。
│   ├── `mcp-settings.md` → 职责：描述 MCP 设置功能规格。
│   └── `workspace-upload-path.md` → 职责：描述工作区上传路径行为规格。
├── `tests/`
│   └── `e2e/` → 职责：承载端到端测试资源。
├── `examples/`
│   └── `acp-docker/` → 职责：提供通过 Docker 运行 ACP 示例的部署文件。
├── `helm/`
│   └── `agent-canvas/` → 职责：提供 Agent Canvas 的 Helm chart 部署单元。
├── `docker/`
│   ├── `Dockerfile` → 职责：定义应用容器镜像构建步骤。
│   └── `entrypoint.sh` → 职责：定义容器启动入口流程。
├── `config/`
│   └── `defaults.json` → 职责：提供应用默认配置值。
├── `bin/`
│   └── `agent-canvas.mjs` → 职责：提供 Agent Canvas 命令行可执行入口。
├── `tools/`
│   └── `canvas_ui_tool.py` → 职责：提供画布 UI 相关辅助工具。

## 范围与待核验项

- 本次只读取并整理目录清单及少量直属子项名称，没有读取 OpenHands-main 的框架实现代码正文。
- `src/dev/`、`src/lib/`、`src/ui/`、顶层 `hero.ts`、`AGENTS.md` 的更细职责不能仅凭本次两层目录扫描完全确认，已标注“待核验”。
- `public/` 中大量图标和站点资源未逐一展开职责，统一归入静态资源域；其具体用途以文件名为准。
