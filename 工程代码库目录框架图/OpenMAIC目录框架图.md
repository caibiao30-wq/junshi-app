# OpenMAIC 工程代码库目录框架图

> 状态：**候选归纳**。本图为对 `/Users/caibiao/Downloads/OpenMAIC-main`（已解压仓库）只读目录勘察的两层框架归纳，基于路径与文件名层面的职责推断，未读取代码正文。不构成产品决策或通用模板。凡无法从命名确认职责者均标注「待核验」。

## 顶层结构

### 顶层目录
- `app/` → 职责：Next.js 应用路由与页面入口
- `assets/` → 职责：项目展示素材、演示动画、二维码与品牌资源
- `components/` → 职责：前端 UI 与业务组件
- `configs/` → 职责：前端或应用配置模块
- `community/` → 职责：社区相关文档或集成说明（待核验）
- `e2e/` → 职责：端到端测试
- `eval/` → 职责：评测场景、评测数据或评测脚本
- `lib/` → 职责：应用核心库、业务逻辑与基础设施模块
- `packages/` → 职责：Monorepo 内部可复用包
- `public/` → 职责：Web 静态资源
- `render-service/` → 职责：独立渲染服务
- `scripts/` → 职责：构建、检查、同步、冒烟测试等辅助脚本
- `skills/` → 职责：项目内 Agent skill 目录
- `tests/` → 职责：单元、集成及领域测试
- `types/` → 职责：TypeScript 类型声明
- `.codegraph/` → 职责：代码图或代码分析相关配置/产物（待核验）
- `.github/` → 职责：GitHub 协作模板、脚本与 CI 工作流

### 顶层文件
- `package.json` → 职责：Node.js 项目脚本与依赖清单
- `pnpm-lock.yaml` → 职责：pnpm 依赖锁定文件
- `pnpm-workspace.yaml` → 职责：pnpm workspace 配置
- `next.config.ts` → 职责：Next.js 配置
- `middleware.ts` → 职责：Next.js 中间件入口
- `instrumentation.ts` → 职责：应用运行时 instrumentation 入口
- `tsconfig.json` / `tsconfig.build.json` → 职责：TypeScript 主配置 / 构建配置
- `eslint.config.mjs` → 职责：ESLint 配置
- `postcss.config.mjs` → 职责：PostCSS 配置
- `vitest.config.ts` / `vitest.eval.config.ts` → 职责：Vitest 测试配置 / 评测专用配置
- `playwright.config.ts` → 职责：Playwright 测试配置
- `components.json` → 职责：UI 组件工具或组件生成配置（待核验）
- `Dockerfile` / `docker-compose.yml` → 职责：主应用容器构建配置 / 多服务编排配置
- `.dockerignore` / `.gitignore` / `.gitattributes` / `.prettierignore` / `.prettierrc` → 职责：Docker / Git / Prettier 各自忽略与属性规则
- `.env.example` → 职责：环境变量示例
- `.nvmrc` → 职责：Node.js 版本约束
- `vercel.json` → 职责：Vercel 部署配置
- `README.md` / `README-zh.md` → 职责：项目主说明 / 中文说明文档
- `CHANGELOG.md` → 职责：版本变更记录
- `CONTRIBUTING.md` / `SECURITY.md` / `LICENSE` → 职责：贡献指南 / 安全策略 / 开源许可
- `comfyui-setup-instructions.md` → 职责：ComfyUI 配置/部署说明

## 第二层（职责相关的主要子目录）

### `app/`
- `api/` → 职责：API 路由目录
- `classroom/` → 职责：课堂/教室功能页面
- `eval/` → 职责：评测页面或入口
- `generation-preview/` → 职责：生成结果预览页面
- `workbench/` → 职责：工作台页面
- `workspace/` → 职责：工作空间页面
- `layout.tsx` / `page.tsx` → 职责：应用布局入口 / 根页面入口
- `globals.css` → 职责：全局样式
- `editor-fonts.ts` → 职责：编辑器字体配置或字体注册（待核验）
- `apple-icon.png` / `favicon.ico` → 职责：应用图标资源

### `components/`
- `agent/` → 职责：Agent UI 组件（待核验）
- `ai-elements/` → 职责：AI 相关通用 UI 元素（待核验）
- `audio/` → 职责：音频组件（待核验）
- `canvas/` → 职责：画布组件（待核验）
- `chat/` → 职责：聊天组件（待核验）
- `classroom/` → 职责：课堂组件（待核验）
- `discovery/` → 职责：发现/探索组件（待核验）
- `edit/` → 职责：编辑组件（待核验）
- `generation/` → 职责：生成流程组件（待核验）
- `roundtable/` → 职责：圆桌/多方讨论组件（待核验）
- `scene-renderers/` → 职责：场景渲染组件（待核验）
- `settings/` → 职责：设置组件（待核验）
- `site-header/` → 职责：站点头部组件（待核验）
- `slide-renderer/` → 职责：幻灯片渲染组件（待核验）
- `stage/` → 职责：舞台/阶段展示组件（待核验）
- `ui/` → 职责：通用 UI 组件（待核验）
- `whiteboard/` → 职责：白板组件（待核验）
- `workbench/` → 职责：工作台组件（待核验）
- 顶层组件文件（`header.tsx`、`stage.tsx`、`user-profile.tsx`、`access-code-guard.tsx`、`access-code-modal.tsx`、`language-switcher.tsx`、`server-providers-init.tsx`、`storage-health-notice.tsx`）→ 职责：各对应通用/入口组件（待核验）

### `configs/`
- `animation.ts` / `chart.ts` / `element.ts` / `font.ts` / `hotkey.ts` / `image-clip.ts` / `latex.ts` / `lines.ts` / `mime.ts` / `shapes.ts` / `storage.ts` / `symbol.ts` / `theme.ts` → 职责：对应领域配置模块（动画/图表/元素/字体/快捷键/图片裁剪/LaTeX/线条/MIME/形状/存储/符号/主题，待核验）

### `lib/`
- `action/` → 职责：动作或服务端 action（待核验）
- `agent/` / `agent-runtime/` → 职责：Agent 逻辑 / Agent 运行时（待核验）
- `ai/` / `api/` → 职责：AI 能力封装 / API 逻辑（待核验）
- `audio/` / `media/` / `media-parse/` / `pdf/` → 职责：音频 / 媒体处理 / 媒体解析 / PDF 处理（待核验）
- `choreography/` / `orchestration/` → 职责：流程编排 / Agent 或任务编排（待核验）
- `classroom/` / `pbl/` / `quiz/` → 职责：课堂 / 项目式学习 / 测验领域逻辑（待核验）
- `document/` / `document-store/` / `persistence/` / `storage/` → 职责：文档模型 / 文档存储 / 持久化 / 存储（待核验）
- `edit/` / `import/` / `export/` / `video-export/` / `video-export-app/` → 职责：编辑 / 导入 / 导出 / 视频导出 / 视频导出应用逻辑（待核验）
- `chat/` / `interactive/` / `live/` / `playback/` / `web-search/` → 职责：聊天 / 交互模式 / 实时 / 回放 / 网页搜索逻辑（待核验）
- `rag/` / `prompts/` → 职责：检索增强生成 / 提示词（待核验）
- `prosemirror/` / `whiteboard/` / `workbench/` → 职责：ProseMirror 编辑器 / 白板 / 工作台逻辑（待核验）
- `config/` / `constants/` / `contexts/` / `hooks/` / `i18n/` / `runtime/` / `server/` / `store/` / `types/` / `usage/` / `utils/` / `brand/` / `buffer/` → 职责：对应基础设施与横切模块（配置/常量/上下文/Hooks/国际化/运行时/服务端/状态存储/类型/用量/工具/品牌/缓冲区，待核验）
- 顶层文件 `logger.ts` → 职责：日志工具或日志入口（待核验）

### `packages/`
- `@openmaic/` → 职责：OpenMAIC 命名空间内部包（待核验）
- `docs/` → 职责：文档包（待核验）
- `mathml2omml/` → 职责：MathML 到 OMML 转换包（待核验）
- `pptxgenjs/` → 职责：PPTX 生成相关内部包或封装（待核验）

### `render-service/`
- `src/` → 职责：渲染服务源代码（待核验）
- `scripts/` → 职责：渲染服务脚本（待核验）
- `test/` → 职责：渲染服务测试
- `Dockerfile` / `docker-entrypoint.sh` → 职责：渲染服务容器构建 / 启动脚本（待核验）
- `package.json` / `package-lock.json` / `tsconfig.json` / `vitest.config.ts` / `.dockerignore` / `.gitignore` / `README.md` → 职责：渲染服务依赖、配置、忽略规则与说明

### `scripts/`
- `ci-run-parallel.sh` → 职责：并行 CI 执行脚本
- `assert-pg-contract-suites.mjs` / `assert-vendor-maic-importer.mjs` → 职责：PG 合约测试套件检查 / 供应商 MAIC importer 检查（待核验）
- `check-i18n-keys.mjs` / `check-internal-dependency-ranges.mjs` / `check-node-engine-contract.mjs` / `check-package-version-bumps.mjs` → 职责：i18n 键 / 内部依赖版本范围 / Node 引擎约束 / 包版本变更检查（待核验）
- `generate-video-export-katex.mjs` / `generate-video-export-noto-cjk.mjs` / `generate-video-export-noto-script-fonts.mjs` → 职责：视频导出 KaTeX / Noto CJK / Noto Script 字体资源生成（待核验）
- `generation-node-smoke.mjs` / `generation-node-smoke-server.mjs` / `smoke-test-package-tarballs.mjs` → 职责：生成节点 / 包 tarball 冒烟测试（待核验）
- `probe-mineru-cloud.mjs` → 职责：MinerU 云服务探测（待核验）
- `sync-maic-importer.mjs` / `verify-package-artifacts.mjs` / `openmaic-packages.mjs` → 职责：MAIC importer 同步 / 包构建产物校验 / OpenMAIC 包相关操作（待核验）

### `skills/`
- `agent-runtime/` → 职责：Agent runtime skill（待核验）
- `openmaic/` → 职责：OpenMAIC skill（待核验）

### `tests/`
- 领域测试目录（`action/`、`agent-runtime/`、`ai/`、`api/`、`audio/`、`chat/`、`ci/`、`classroom/`、`components/`、`config/`、`document/`、`document-store/`、`edit/`、`eval/`、`export/`、`fixtures/`、`generation/`、`generation-preview/`、`hooks/`、`i18n/`、`import/`、`lib/`、`media/`、`orchestration/`、`packages/`、`pbl/`、`persistence/`、`playback/`、`prompts/`、`prosemirror/`、`providers/`、`quiz/`、`rag/`、`runtime/`、`scene-renderers/`、`security/`、`server/`、`settings/`、`slide-renderer/`、`store/`、`ui/`、`usage/`、`utils/`、`video-export/`、`web-search/`、`workbench/`、`workflows/`）→ 职责：对应领域的测试（按领域拆分，具体覆盖范围与执行入口待核验）
- 顶层文件 `lint-llm-entry-guard.test.ts`、`setup-env.ts` → 职责：LLM 入口守卫相关测试 / 测试环境初始化（待核验）

### `e2e/`
- `fixtures/` / `pages/` / `tests/` → 职责：端到端测试 fixtures / 页面对象封装 / 用例（组织方式待核验）

### `eval/`
- `orchestration/` / `outline-language/` / `pbl-v2-planner/` / `whiteboard-layout/` → 职责：编排 / 大纲语言 / PBL v2 规划器 / 白板布局评测（评测协议与运行方式待核验）
- `shared/` → 职责：评测共享资源或工具（待核验）

### `public/`
- `avatars/` / `logos/` → 职责：头像 / Logo 资源
- `vendor/` → 职责：第三方或供应商静态资源（待核验）
- `comfyui-workflow.json` → 职责：ComfyUI 工作流定义（待核验）
- `logo-horizontal.png` / `openmaic-mark.png` → 职责：品牌图片

### `assets/`
- `interactive_mode/` / `voxcpm/` → 职责：交互模式 / VoxCPM 相关素材（待核验）
- 演示动画（`avalon.gif`、`deepseek.gif`、`discussion.gif`、`interactive.gif`、`openclaw-feishu-demo.gif`、`pbl.gif`、`python.gif`、`quiz.gif`、`slides.gif`、`zhipu-minimax.gif`）→ 职责：功能或模型演示动画
- `banner.png` / `logo-horizontal.png` / `feishu-qrcode.png` → 职责：品牌/宣传图片、飞书二维码

### `community/`
- `feishu.md` → 职责：飞书相关社区或集成说明（待核验）

### `types/`
- `web-extraction-vendors.d.ts` / `web-speech.d.ts` → 职责：网页提取供应商 / Web Speech 类型声明（待核验）

### `.github/`
- `ISSUE_TEMPLATE/` → 职责：Issue 模板（待核验）
- `pull_request_template.md` → 职责：Pull Request 模板（待核验）
- `scripts/` → 职责：GitHub 自动化脚本（待核验）
- `workflows/` → 职责：GitHub Actions 工作流（待核验）

---

## 勘察说明
- 依据：`find /Users/caibiao/Downloads/OpenMAIC-main -maxdepth 2`（排除 `.git/`）。
- 深度：严格两层，未展开第三层，未读取任何代码/配置/文档正文。
- 纪律：未联网、未修改仓库、未触碰 context.md、mate/、STRUCTURE.md 及仓库外文件。
- 无法从命名确认职责者一律标注「待核验」，未作臆测。
