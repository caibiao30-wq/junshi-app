# hermes-agent 工程代码库目录框架图

> **候选归纳**：本文为对本地仓库 `/Users/caibiao/Downloads/hermes-agent-main`（只读）的两层目录布局归纳，属于候选归纳，不升级为产品决策或通用模板。
> **范围与深度**：第一层 = 顶层目录/文件；第二层 = 第一层下与职责相关的主要子目录/文件。不深入第三层，不读代码正文，不研究框架 API。
> **来源**：`ls` 顶层与第二层目录清单（未读任何代码正文）。结构与职责仅由目录/文件命名推断，若无法确认职责标"待核验"。
> **性质**：hermes-agent 为大型单仓（monorepo），大量顶层模块平铺于根目录；根目录同时混有配置、文档与运行模块，未按子系统分组。

## 顶层结构

### 核心运行模块（顶层文件，平铺）
├── `cli.py`            → 主 CLI 命令行入口（体量巨大，约 1MB）→ 职责：命令分发与用户交互
├── `run_agent.py`      → 运行 Agent 主循环 → 职责：会话执行编排
├── `batch_runner.py`   → 批处理运行器 → 职责：批量/后台任务执行
├── `mini_swe_runner.py`→ 小型 SWE（软件工程）评测运行器 → 职责：代码任务评测执行
├── `mcp_serve.py`      → MCP 服务入口 → 职责：以 MCP 协议对外提供工具服务
├── `hermes`            → 可执行启动脚本 → 职责：入口引导
├── `hermes_bootstrap.py`→ 启动引导 → 职责：环境初始化与引导
├── `hermes_startup_watchdog.py` → 启动看门狗 → 职责：启动期健康守护
├── `hermes_state.py`   → 状态主模块（体量巨大）→ 职责：会话/状态存储与读写
├── `hermes_state_common.py` / `_holders.py` / `_portability.py` / `_registry.py` / `_schema.py` / `_search.py` → 状态子系统各域 → 职责：状态通用、持有者、可移植、注册、Schema、搜索
├── `hermes_constants.py` → 全局常量 → 职责：常量定义
├── `hermes_logging.py`   → 日志模块 → 职责：日志基础设施
├── `hermes_time.py`      → 时间模块 → 职责：时间处理
├── `trajectory_compressor.py` → 轨迹压缩 → 职责：对话/轨迹上下文压缩
├── `toolset_distributions.py` / `toolsets.py` → 工具集定义/分发 → 职责：工具集组织
├── `model_tools.py`      → 模型相关工具 → 职责：模型辅助能力
├── `registration_lifecycle.py` → 注册生命周期 → 职责：注册流程管理
├── `utils.py`            → 通用工具函数 → 职责：通用辅助
├── `setup.py` / `pyproject.toml` / `package.json` / `setup-hermes.sh` → 构建/打包/依赖与安装脚本 → 职责：工程构建与安装

### 配置与仓库级文件
├── `.env.example`       → 环境变量示例 → 职责：配置样例
├── `.envrc` / `.nvmrc` / `.python-version` / `.npmrc` / `.gitignore` / `.gitattributes` / `.prettier*` / `.hadolint.yaml` / `.coderabbit.yaml` → 工具/语言/CI 配置 → 职责：开发工具链配置
├── `cli-config.yaml.example` → CLI 配置示例 → 职责：CLI 配置样例
├── `Dockerfile` / `docker-compose.yml` / `docker-compose.windows.yml` / `.dockerignore` → 容器化配置 → 职责：Docker 构建与编排
├── `flake.nix` / `flake.lock` → Nix 打包 → 职责：Nix 构建定义
├── `uv.lock` / `package-lock.json` → 依赖锁文件 → 职责：依赖锁定
├── `LICENSE`            → 许可证 → 职责：许可声明
├── `SOUL.md`            → 人格/灵魂定义（待核验）→ 职责：产品人格设定
├── `AGENTS.md`          → 智能体协作指引 → 职责：多智能体开发约定
├── `README.md` / `README.es.md` / `README.zh-CN.md` / `README.ur-pk.md` → 多语言说明 → 职责：文档入口
├── `CONTRIBUTING.md` / `CONTRIBUTING.es.md` → 贡献指南 → 职责：贡献规范
├── `SECURITY.md` / `SECURITY.es.md` → 安全说明 → 职责：安全披露与策略

### 顶层目录
├── `agent/`             → 核心 Agent 运行时 → 职责：会话循环、模型适配、上下文管理（含大量适配器：anthropic/bedrock/azure/codex 等）
├── `hermes_cli/`        → CLI 命令实现 → 职责：CLI 子命令、认证、会话、备份等命令模块
├── `gateway/`           → 网关服务 → 职责：多通道/平台接入、托管房间、消息路由
├── `tui_gateway/`       → TUI 网关 → 职责：终端 UI 与网关间的协议/传输服务
├── `tools/`             → 工具实现库 → 职责：文件、浏览器、代码执行、MCP、图像生成等各类工具
├── `skills/`            → 内置技能集 → 职责：内建 skill 目录
├── `optional-skills/`   → 可选技能集 → 职责：可选/可插拔 skill
├── `optional-mcps/`     → 可选 MCP 集成 → 职责：第三方平台 MCP 适配器（数十家 SaaS）
├── `plugins/`           → 插件体系 → 职责：插件注册、运行时与各类业务插件
├── `providers/`         → 提供者基类 → 职责：第三方能力提供者的抽象基类
├── `acp_adapter/`       → ACP 适配器 → 职责：外部 Agent 客户端协议适配
├── `cron/`              → 定时任务系统 → 职责：调度器、任务、执行、通知
├── `apps/`              → 应用层（桌面/安装器/共享）→ 职责：桌面端 UI 与应用
├── `web/`               → Web 前端 → 职责：Web UI（React/Vite）
├── `website/`           → 官网站点 → 职责：产品官网（Docusaurus）
├── `ui-tui/`            → TUI 前端 → 职责：终端 UI 应用（含 hermes-ink 包）
├── `docker/`            → 容器运行层 → 职责：Docker 入口、s6 进程管理、SOUL 注入
├── `nix/`               → Nix 模块 → 职责：NixOS/home-manager 模块与打包
├── `scripts/`           → 运维/构建/CI 脚本 → 职责：安装、发布、诊断、评测等脚本
├── `docs/`              → 文档 → 职责：设计、RFC、安全、观测等文档
├── `evals/`             → 评测 → 职责：能力评测与基准
├── `tests/`             → Python 测试 → 职责：单元/集成/e2e/安全测试
├── `tests-js/`          → JS/TS 测试 → 职责：前端/工具链测试
├── `locales/`           → 多语言翻译 → 职责：i18n 语言包
├── `mcp-research-data/` → MCP 调研数据 → 职责：调研基准数据文件
├── `assets/`            → 静态资源 → 职责：图片等资源
├── `contributors/`      → 贡献者信息 → 职责：贡献者名单
├── `native/`            → 原生扩展 → 职责：原生模块（如 FTS5 中文分词）
├── `datagen-config-examples/` → 数据生成配置示例 → 职责：数据生成配置样例
├── `.github/`           → GitHub 工作流 → 职责：CI/CD、Issue/PR 模板、actionlint

## 第二层（职责相关的主要子目录）

├── `agent/`
│   ├── `anthropic_adapter.py` / `bedrock_adapter.py` / `azure_identity_adapter.py` / `codex_runtime.py` → 各模型后端适配 → 职责：多模型提供方接入
│   ├── `conversation_loop.py` / `conversation_compression.py` / `context_engine.py` / `context_compressor.py` → 对话/上下文 → 职责：会话循环与上下文治理
│   ├── `browser_provider.py` / `browser_registry.py` → 浏览器能力 → 职责：浏览器提供方管理
│   ├── `credential_pool.py` / `credential_persistence.py` / `credential_sources.py` / `anthropic_credentials.py` → 凭据 → 职责：密钥凭据池与管理
│   ├── `account_usage.py` / `billing_usage.py` / `billing_view.py` / `billing_links.py` / `aux_accounting.py` → 计费/用量 → 职责：账户额度与计费
│   ├── `background_review.py` / `coding_context.py` / `command_token_source.py` → 辅助能力 → 职责：后台评审、编码上下文、命令令牌源（待核验）

├── `hermes_cli/`
│   ├── `auth_commands.py` / `auth.py` / `approval_mode.py` / `approvals_*` → 认证/审批 → 职责：认证与操作审批
│   ├── `cli_billing_mixin.py` / `cli_commands_mixin.py` / `cli_agent_setup_mixin.py` / `commands.py` → 命令组织 → 职责：CLI 命令与 mixin 组合
│   ├── `active_sessions.py` / `agent_plugins.py` / `backup.py` / `checkpoints.py` → 会话/插件/备份 → 职责：会话管理、插件加载、备份与检查点
│   ├── `_parser.py` / `_startup_fast.py` / `_early_recovery.py` / `_scan_venv_blockers.py` / `_subprocess_compat.py` → 启动/解析 → 职责：启动路径与参数解析底层

├── `gateway/`
│   ├── `platforms/` / `platform_registry.py` → 平台接入 → 职责：各平台通道注册
│   ├── `hosted_room_*.py` / `hosted_room_driver.py` → 托管房间 → 职责：托管会话/协作房间
│   ├── `builtin_hooks/` → 内建钩子 → 职责：内建行为钩子（待核验）
│   ├── `delivery.py` / `delivery_ledger.py` / `channel_directory.py` / `profile_routing.py` → 投递/路由 → 职责：消息投递与配置路由
│   ├── `media_policy.py` / `media_repair.py` / `browser_control_*.py` / `memory_monitor.py` → 策略/监控 → 职责：媒体策略、浏览器控制、内存监控

├── `tools/`
│   ├── `file_tools.py` / `file_operations.py` / `path_security.py` → 文件 → 职责：文件读写与路径安全
│   ├── `browser_tool.py` / `browser_cdp_tool.py` / `browser_camofox.py` / `browser_supervisor.py` / `computer_use/` → 浏览器/电脑操作 → 职责：浏览器与电脑自动化工具
│   ├── `code_execution_tool.py` / `code_kernel.py` / `code_kernel_remote.py` / `environments/` → 代码执行 → 职责：代码执行与沙箱环境
│   ├── `mcp_tool.py` / `mcp_oauth_manager.py` / `mcp_schema_cache.py` → MCP → 职责：MCP 工具与 OAuth
│   ├── `image_generation_tool.py` / `video_gen` 相关 / `image_source.py` → 生成 → 职责：图像/视频生成（待核验视频项）
│   ├── `cronjob_tools.py` / `kanban_tools.py` / `memory_tool.py` / `delegate_tool.py` / `async_delegation.py` → 业务工具 → 职责：定时、看板、记忆、委派

├── `optional-mcps/`
│   ├── `airtable/` `asana/` `figma/` `linear/` `notion/` `slack` `stripe/` `vercel/` `wolfram/` 等数十家 → 第三方平台 MCP 适配 → 职责：各 SaaS 平台工具封装（每家一个目录）

├── `optional-skills/`
│   ├── `software-development/` `web-development/` `data-science/` `research/` `security/` `devops/` `email/` `communication/` 等 → 分域技能集 → 职责：按领域组织的可选技能

├── `plugins/`
│   ├── `browser/` `web/` `image_gen/` `kanban/` `memory/` `observability/` `cron_providers/` `platforms/` 等 → 业务插件 → 职责：各领域插件实现
│   ├── `plugin_storage.py` / `plugin_utils.py` → 插件基建 → 职责：插件存储与工具

├── `cron/`
│   ├── `scheduler.py` / `scheduler_provider.py` → 调度核心 → 职责：定时调度
│   ├── `jobs.py` / `executions.py` / `delivery_queue.py` / `suggestions.py` / `incidents.py` / `blueprint_catalog.py` → 任务/通知 → 职责：任务、执行、投递、建议、告警
│   ├── `scripts/` → 定时任务脚本 → 职责：可执行的定时任务（待核验）

├── `apps/`
│   ├── `desktop/` → 桌面应用 → 职责：桌面端（Electron + Vite）
│   ├── `bootstrap-installer/` → 安装引导器 → 职责：安装引导（Tauri）
│   ├── `shared/` → 共享代码 → 职责：跨应用共享前端模块

├── `web/src/`
│   ├── `components/` `pages/` `hooks/` `contexts/` `lib/` `plugins/` `i18n/` → Web UI 分域 → 职责：React 组件、页面、状态、国际化

├── `website/`
│   ├── `docs/` `src/` `static/` `sidebars.ts` `i18n/` → 官网内容与代码 → 职责：产品官网站点（Docusaurus）

├── `ui-tui/`
│   ├── `packages/hermes-ink` → TUI 渲染包 → 职责：终端渲染库
│   ├── `src/` `scripts/` → TUI 源码 → 职责：TUI 应用实现

├── `docker/`
│   ├── `entrypoint.sh` / `entrypoint-dispatch.sh` / `main-wrapper.sh` / `s6-rc.d/` / `cont-init.d/` → 容器启动/进程管理 → 职责：容器入口与 s6 监督

├── `nix/`
│   ├── `hermes-agent.nix` / `nixosModules.nix` / `homeManagerModules.nix` / `packages.nix` / `overlays.nix` / `sandbox.nix` / `devShell.nix` → Nix 构建/集成 → 职责：NixOS/home-manager 集成与打包

├── `scripts/`
│   ├── `install.sh` / `install.ps1` / `install.cmd` / `release.py` / `ci/` → 安装与发布 → 职责：跨平台安装与发布
│   ├── `sandbox/` `dev-sandbox.sh` / `hermes-gateway/` / `toolperf_abeval/` / `LIVETEST_README.md` → 沙箱/评测 → 职责：沙箱与活体测试（待核验细项）

├── `docs/`
│   ├── `design/` `rfcs/` `security/` `observability/` `middleware/` `kanban/` → 分域文档 → 职责：设计、RFC、安全、观测等文档

├── `evals/`
│   ├── `browser_use/` `compaction/` `core_tool_deferral/` `readtool/` `session_search_schema/` → 各评测集 → 职责：分能力评测

├── `tests/`
│   ├── `agent/` `cli/` `gateway/` `tools/` `skills/` `cron/` `plugins/` `security/` `conformance/` `e2e/` `integration/` → 分域测试 → 职责：按模块组织的测试套件
│   ├── `fixtures/` `fakes/` `conftest.py` → 测试基建 → 职责：测试夹具与共享配置

├── `locales/`
│   ├── `zh.yaml` / `en.yaml` / `ja.yaml` / `ko.yaml` / `*.yaml`（多语言） → 翻译包 → 职责：i18n 本地化

├── `.github/`
│   ├── `workflows/` `actions/` `ISSUE_TEMPLATE/` `PULL_REQUEST_TEMPLATE.md` `dependabot.yml` → CI/CD → 职责：自动化工作流与模板

## 未能确认/需待核验项

- `SOUL.md`、`contributors/`、`assets/`、`native/`、`mcp-research-data/`、`datagen-config-examples/` 的具体内部职责仅由命名推断，未读正文，标注"待核验"。
- `agent/`、`tools/`、`hermes_cli/`、`gateway/` 内部大量平铺 `.py` 文件，未逐一定位，只归纳了职责相关的主要项。
- 顶层平铺了大量巨型模块（`cli.py`、`hermes_state.py`、`run_agent.py` 等），它们各自承担跨域职责，单一"一句话职责"为粗粒度归纳，精确边界待核验。
- 未深入第三层（如 `tools/computer_use/`、`tools/environments/`、`gateway/platforms/` 内部），第三层以下结构未覆盖。
