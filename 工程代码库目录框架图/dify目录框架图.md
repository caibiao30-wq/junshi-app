# dify 工程代码库目录框架图

> 状态：**候选归纳**（仅作为目录布局参考，不升级为产品决策或通用模板）
> 来源：`/Users/caibiao/Downloads/dify-main`（本地已解压仓库，仅读取目录结构，未读代码正文）
> 深度：两层。标注「待核验」的项因职责无法从目录名、文件名直接确认，未断言。

## dify 工程代码库目录框架图

### 顶层结构

工程师职责分域：一个 `api`（Python 后端）+ 一个 `web`（前端）+ 多个子工程/SDK + 运维与文档。

```
├── api/                          → 职责：Python 后端服务（Dify 的核心 API 服务端，含业务、路由、模型、扩展）
├── web/                          → 职责：前端应用（Next.js/React 用户界面，Web 控制台与交互层）
├── packages/                     → 职责：前端共享包（可复用的界面库、契约、工具，供多工程复用）
├── cli/                          → 职责：命令行工具（开发者/运维用的 CLI 应用）
├── dify-agent/                   → 职责：Agent 子工程（Python 实现的独立 Agent 框架，侧重 agent 能力）
├── dify-agent-runtime/           → 职责：Agent 运行器（Go 实现的轻量运行层，与 dify-agent 对应）
├── sdks/                         → 职责：面向外部开发者的 SDK（多语言客户端，供集成 dify 使用）
├── docker/                       → 职责：部署与中间件（Docker 编排、各中间件镜像、启动脚本）
├── scripts/                      → 职责：工程脚本（lint/代码守卫/压测等构建与质量工具）
├── dev/                          → 职责：本地开发命令（start-api/start-web/ty-check 等开发便捷脚本）
├── docs/                         → 职责：文档（含多语言本地化文档）
├── e2e/                          → 职责：端到端测试（Cucumber 行为测试）
├── images/                       → 职责：仓库用图片资源（文档/展示用）
├── Makefile / package.json / pnpm-workspace.yaml / vite.config.ts / eslint.config.mjs 等
│                                 → 职责：工程构建、依赖与代码质量配置（JS 工程与 monorepo 配置）
├── .github/                      → 职责：CI/CD 与 GitHub 流程（Actions、模板等）
├── .devcontainer/                → 职责：开发容器配置（VS Code 远程开发环境）
├── .vscode/ .env* .vite-hooks/   → 职责：编辑器与本地开发环境插件/钩子配置
└── README.md / CONTRIBUTING.md / SECURITY.md / LICENSE / AGENTS.md(CLAUDE.md→软链)
                                  → 职责：仓库说明、贡献规范、安全策略、许可与智能体协作说明
```

### 第二层（职责相关的主要子目录）

```
├── api/（Python 后端 · 职责可分域）
│   ├── controllers/   → 职责：HTTP 路由/接口层（console/web/service_api 等入口）
│   ├── services/      → 职责：业务服务逻辑层（account/dataset/workflow 等业务服务）
│   ├── models/        → 职责：数据模型与 ORM 实体（account/dataset/workflow/task…）
│   ├── core/          → 职责：领域核心逻辑（agent/rag/mcp/prompt/memory/llm_generator…）
│   ├── migrations/    → 职责：数据库迁移脚本（schema 演进，顶层无二级子目录时为迁移脚本目录——待核验）
│   ├── configs/       → 职责：配置定义（应用配置与模型配置）
│   ├── extensions/    → 职责：运行时扩展接入（db/redis/celery/sentry 等第三方集成初始化）
│   ├── providers/     → 职责：供应商接入（模型供应商、向量数据库供应商）
│   ├── events/        → 职责：事件定义与分发
│   ├── tasks/         → 职责：异步任务（celery 任务）
│   ├── factories/     → 职责：对象工厂（应用/模型等工厂）
│   ├── context/ context/contexts/
│                       → 职责：上下文对象与请求上下文管理
│   ├── repositories/  → 职责：数据访问仓库层（数据查询封装）
│   ├── commands/      → 职责：命令行入口（管理类命令）
│   ├── fields/        → 职责：Pydantic 字段/序列化定义
│   ├── enums/ / constants/ → 职责：枚举与常量定义
│   ├── libs/          → 职责：内部工具库
│   ├── machinery/     → 职责：后台/框架运行机制（实证语义待核验）
│   ├── openapi/       → 职责：OpenAPI 规范生成/注册
│   ├── tests/         → 职责：后端测试
│   ├── enterprise/    → 职责：企业版相关扩展逻辑（待核验）
│   └── app.py / app_factory.py / dify_app.py → 职责：应用入口与工厂构建

├── web/（前端 · 职责可分域）
│   ├── app/           → 职责：应用路由页面与布局（各路由页/布局/登录注册/安装等）
│   ├── features/      → 职责：按业务功能划分的前端模块（如 agent-v2/new-rag/skills/account-profile…）
│   ├── components/    → 职责：通用 UI 组件（可复用组件库）
│   ├── hooks/         → 职责：自定义 React Hooks
│   ├── service/       → 职责：前端 API 调用层（服务层封装）
│   ├── constant/ / constants/ → 职责：前端常量
│   ├── context/       → 职责：前端上下文/Provider
│   ├── i18n/ / i18n-config/ → 职责：国际化文案与配置（多语言）
│   ├── models/        → 职责：前端数据模型/类型
│   ├── types/         → 职责：TypeScript 类型定义
│   ├── utils/         → 职责：前端工具函数
│   ├── themes/        → 职责：主题样式
│   ├── assets/ / public/ → 职责：静态资源
│   ├── plugins/       → 职责：前端插件（待核验）
│   ├── config/        → 职责：前端构建/运行配置
│   ├── test/ / tests/ / __tests__/ → 职责：前端测试
│   ├── next/          → 职责：Next.js 框架相关代码（待核验）
│   └── i18n-config/ / next.config.ts / vite.config.ts → 职责：构建与框架配置

├── packages/（前端共享包）
│   ├── contracts/     → 职责：前后端契约定义（OpenAPI/zod 契约与生成）
│   ├── dify-ui/       → 职责：共享 UI 组件库（跨工程复用）
│   ├── dev-proxy/     → 职责：本地开发代理工具
│   ├── iconify-collections/ → 职责：图标集合（iconify 图标资源）
│   ├── jotai-tanstack-form/ → 职责：jotai + tanstack-form 集成封装
│   ├── migrate-no-unchecked-indexed-access/ → 职责：TS 迁移辅助工具（待核验）
│   └── tsconfig/      → 职责：共享 TypeScript 配置

├── cli/（命令行工具）
│   ├── src/           → 职责：CLI 源码
│   ├── bin/           → 职责：CLI 可执行入口
│   ├── test/          → 职责：CLI 测试
│   └── scripts/       → 职责：CLI 配套脚本（待核验）

├── dify-agent/（Agent 框架，Python）
│   ├── src/           → 职责：Agent 框架源码
│   ├── tests/         → 职责：Agent 测试
│   ├── examples/      → 职责：使用示例
│   └── docs/          → 职责：Agent 文档

├── dify-agent-runtime/（Agent 运行器，Go）
│   ├── cmd/           → 职责：可执行程序入口（main 命令）
│   ├── internal/      → 职责：内部实现包（不对外暴露）
│   ├── benchmarks/    → 职责：基准测试/性能
│   ├── tests/         → 职责：运行器测试
│   └── docker/        → 职责：运行器容器化配置（待核验）

├── sdks/（多语言 SDK）
│   ├── nodejs-client/  → 职责：Node.js 客户端 SDK
│   └── php-client/     → 职责：PHP 客户端 SDK

├── docker/（部署与中间件）
│   ├── nginx/          → 职责：Nginx 反向代理配置
│   ├── certbot/        → 职责：证书自动续期（HTTPS 证书）
│   ├── ssrf_proxy/     → 职责：SSRF 防护代理
│   ├── envs/           → 职责：环境变量模板示例
│   ├── volumes/        → 职责：数据卷/挂载目录（待核验）
│   ├── startupscripts/ → 职责：启动初始化脚本
│   ├── elasticsearch/ tidb/ pgvector/ couchbase-server/ iris/（各中间件目录）
│                       → 职责：对应中间件的镜像/配置：向量索引、数据库、向量库等
│   └── docker-compose*.yaml / generate_docker_compose / dify-env-sync*
│                       → 职责：编排文件与生成/同步脚本
```

### 备注 / 阻塞

- **未确认项（待核验）**：`api/machinery/`、`api/migrations/`（顶层无二级子目录细项时的职责）、`web/next/`、`web/plugins/`、`packages/migrate-no-unchecked-indexed-access/`、`cli/scripts/`、`docker/volumes/`、`enterprise/`。以上仅能从目录名推断大致方向，未读代码正文，故不背书为既定职责。
- **口径**：`dify-agent` 用 Python、`dify-agent-runtime` 用 Go，二者为独立子工程；`dify` 主工程为 `api` + `web` + `packages` 的 monorepo（`pnpm-workspace.yaml`）。