# claude-code 工程代码库目录框架图

> 状态：**候选归纳**（非产品决策、非通用模板）
> 一手来源：`/Users/caibiao/Downloads/claude-code-main`（本地解压仓库）
> 深度限制：两层；职责依据目录/文件名归纳，未确认处标注"待核验"

## 顶层结构

├── `packages/`     → 职责：平台/工具子系统（编译型 native、MCP、工作流等）的包集合
├── `src/`          → 职责：CLI 主程序与交互逻辑的主源码目录
├── `docs/`         → 职责：开发/设计/特性/测试等内部文档
├── `tests/`        → 职责：集成测试与 mock
├── `scripts/`      → 职责：构建、调试、发布辅助脚本
├── `spec/`         → 职责：功能特性规格（feature spec）
├── `vendor/`       → 职责：外部引入的第三方源码/依赖副本
├── `teach-me/`     → 职责：学习/教学材料（learner-profile、vllm）
├── `.claude/`      → 职责：本仓库自身的 Claude 配置（agents、skills）
├── `.github/`      → 职责：GitHub 集成（issue 模板、workflows）
├── `.vscode/`      → 职责：VS Code 编辑器配置（launch、tasks、extensions）
├── `.husky/`       → 职责：git hooks（pre-commit）
├── `build.ts`      → 职责：顶层构建入口脚本
├── `vite.config.ts`→ 职责：vite 构建/打包配置
├── `package.json`  → 职责：依赖与包元数据
├── `bun.lock`      → 职责：bun 依赖锁文件
├── `bunfig.toml`   → 职责：bun 运行配置
├── `tsconfig.json` → 职责：TypeScript 编译配置
├── `tsconfig.base.json` → 职责：TS 基础配置（被各包引用）
├── `biome.json`    → 职责：biome 格式化/检查配置
├── `knip.json`     → 职责：未使用依赖/导出检查配置
├── `mint.json`     → 职责：文档站（mintlify）导航配置
├── `docs.json`     → 职责：文档站点配置
├── `codecov.yml`   → 职责：代码覆盖率服务配置
├── `README.md`     → 职责：项目总说明
├── `README_EN.md`  → 职责：英文版项目说明
├── `AGENTS.md`     → 职责：面向代码代理的工作指引
├── `CLAUDE.md`     → 职责：面向 Claude 的工作指引
├── `SECURITY.md`   → 职责：安全披露说明
├── `DEV-LOG.md`    → 职责：开发日志
├── `Friends.md`    → 职责：致谢/伙伴名单
├── `contributors.svg` → 职责：贡献者徽章图
├── `progress.md`   → 职责：进度记录
└── 隐藏工具配置（`.editorconfig`、`.gitignore`、`.dockerignore`、`.npmrc`、`.tool-versions`、`.mintignore`、`.impeccable.md`）→ 职责：各自环境/工具约束

## 第二层（职责相关的主要子目录）

### `src/` — 主源码
├── `cli/`          → 职责：命令行入口与参数解析
├── `commands/`     → 职责：各斜杠命令实现
├── `commands.ts`   → 职责：命令注册
├── `entrypoints/`  → 职责：程序各入口点（main/repl 等）
├── `main.tsx`      → 职责：TUI 主入口
├── `screens/`      → 职责：TUI 界面屏
├── `components/`   → 职责：TUI 界面组件
├── `hooks/`        → 职责：React hooks（界面状态逻辑）
├── `keybindings/`  → 职责：键盘绑定
├── `vim/`          → 职责：vim 模式支持
├── `outputStyles/` → 职责：输出样式
├── `dialogLaunchers.tsx` / `interactiveHelpers.tsx` / `replLauncher.tsx` → 职责：交互式弹窗/帮助/REPL 启动
├── `assistant/`    → 职责：助手会话逻辑
├── `buddy/`        → 职责：Buddy 协同模式
├── `coordinator/`  → 职责：任务协调
├── `tasks/` + `tasks.ts` + `Task.ts` → 职责：任务模型与调度
├── `jobs/`         → 职责：后台作业
├── `proactive/`    → 职责：主动行为
├── `moreright/`    → 职责：moreright 相关（待核验）
├── `agent`(docs)   → （docs 侧）
├── `context.ts` + `context/` → 职责：上下文管理
├── `memdir/`       → 职责：内存/记忆目录
├── `migrations/`   → 职责：数据/状态迁移
├── `state/`        → 职责：状态管理
├── `history.ts`    → 职责：历史会话记录
├── `query/` + `query.ts` + `QueryEngine.ts` → 职责：查询引擎
├── `schemas/`      → 职责：数据结构 schema
├── `types/`        → 职责：类型定义
├── `constants/`    → 职责：常量
├── `tools.ts` + `Tool.ts` → 职责：工具定义
├── `skills/`       → 职责：技能系统
├── `plugins/`      → 职责：插件系统
├── `services/`     → 职责：通用服务
├── `server/`       → 职责：服务端逻辑
├── `daemon/`       → 职责：后台守护进程
├── `remote/`       → 职责：远程执行
├── `ssh/`          → 职责：SSH 相关
├── `bridge/`       → 职责：桥接层
├── `upstreamproxy/`→ 职责：上游代理
├── `native-ts/`    → 职责：native 绑定（TS）
├── `bootstrap/`    → 职责：引导启动
├── `setup.ts`      → 职责：环境初始化
├── `cost-tracker.ts` + `costHook.ts` → 职责：成本追踪
├── `modes/`        → 职责：模式系统
├── `voice/`        → 职责：语音
├── `utils/`        → 职责：通用工具函数
├── `__tests__/`    → 职责：单元测试
└── 顶层各 `.ts`（`commands.ts`、`tools.ts` 等）→ 职责：对应域注册入口

### `packages/` — 独立包
├── `@ant/`              → 职责：组织内共享包（ant 命名空间）
├── `acp-link/`          → 职责：ACP（Agent Client Protocol）连接
├── `agent-tools/`       → 职责：代理工具集
├── `audio-capture-napi/`→ 职责：音频采集 native 模块（待核验编译产物）
├── `builtin-tools/`     → 职责：内置工具
├── `cloud-artifacts/`   → 职责：云端产物
├── `color-diff-napi/`   → 职责：颜色差异计算 native 模块
├── `image-processor-napi/` → 职责：图像处理 native 模块
├── `mcp-client/`        → 职责：MCP 客户端
├── `modifiers-napi/`    → 职责：修饰键 native 模块（待核验）
├── `remote-control-server/` → 职责：远程控制服务端
├── `url-handler-napi/`  → 职责：URL 协议处理 native 模块
├── `weixin/`            → 职责：微信集成
├── `workflow-engine/`   → 职责：工作流引擎
└── `tsconfig.json`      → 职责：包级 TS 配置

### `docs/` — 文档
├── `introduction/`  → 职责：入门文档
├── `features/`      → 职责：功能特性文档
├── `design/`        → 职责：设计文档
├── `internals/`     → 职责：内部实现文档
├── `context/`       → 职责：上下文机制文档
├── `conversation/`  → 职责：会话机制文档
├── `tools/`         → 职责：工具文档
├── `task/`          → 职责：任务机制文档
├── `safety/`        → 职责：安全文档
├── `testing/` + `test-plans/` → 职责：测试与测试计划
├── `extensibility/` → 职责：扩展性文档
├── `diagrams/`      → 职责：架构图
├── `images/` / `logo/` → 职责：图片素材
├── `agent/`         → 职责：代理相关文档
├── `superpowers/`   → 职责：superpowers 主题（待核验）
├── 各审计文档（`acp-compliance-audit.md`、`ink-tui-deep-audit.md`、`memory-leak-audit.md`、`memory-peak-analysis.md`、`telemetry-remote-config-audit.md`、`performance-reporter.md`、`lsp-integration.md`、`external-dependencies.md`、`auto-updater.md`）→ 职责：专项审计/机制说明
└── `favicon.svg`    → 职责：站点图标

### `tests/` — 测试
├── `integration/`  → 职责：集成测试
└── `mocks/`        → 职责：测试 mock

### `scripts/` — 辅助脚本
├── `dev.ts` + `dev-debug.ts`        → 职责：开发调试
├── `build.ts`(顶层)                 → 见顶层
├── `post-build.ts`                  → 职责：构建后处理
├── `check-bundle-integrity.ts`      → 职责：产物完整性校验
├── `defines.ts`                     → 职责：构建宏定义
├── `dump-prompt.ts`                 → 职责：导出 prompt
├── `postinstall.cjs`                → 职责：安装后处理
├── `rcs.ts` + `rcs-ccb.sh`          → 职责：RCS 相关（待核验）
├── `run-parallel.mjs`               → 职责：并行执行
├── `setup-chrome-mcp.mjs`           → 职责：Chrome MCP 安装
├── `vite-plugin-feature-flags.ts`   → 职责：特性开关 vite 插件
└── `vite-plugin-import-meta-require.ts` → 职责：import.meta.require vite 插件

### `spec/` — 规格
├── `feature_20260502_F001_fork-agent-redesign/` → 职责：fork 代理重设计特性规格
└── `feature_20260508_F001_tool-search/`         → 职责：工具搜索特性规格

### `vendor/` — 第三方源码
├── `audio-capture/`     → 职责：音频采集第三方源码副本
└── `audio-capture-src/` → 职责：音频采集源码（待核验与上者关系）

### `teach-me/` — 教学材料
├── `learner-profile.md` → 职责：学习者画像
└── `vllm/`              → 职责：vLLM 相关材料（待核验）

### `.claude/` — 本仓库 Claude 配置
├── `agents/`   → 职责：自定义子代理定义
└── `skills/`   → 职责：自定义技能定义

### `.github/` — GitHub 集成
├── `ISSUE_TEMPLATE/` → 职责：issue 模板
└── `workflows/`      → 职责：CI/CD 工作流

### `.vscode/` — 编辑器配置
├── `launch.json`     → 职责：调试启动配置
├── `tasks.json`      → 职责：构建任务
└── `extensions.json` → 职责：推荐扩展

## 待核验/未确认项
- `src/moreright/`、`src/buddy/`、`src/coordinator/` 的具体职责边界
- `packages/audio-capture-napi/`、`modifiers-napi/` 是否为编译型 native 产物
- `vendor/audio-capture/` 与 `vendor/audio-capture-src/` 的关系
- `docs/superpowers/`、`teach-me/vllm/`、`scripts/rcs*.ts` 的确切职责
- `docs/agent/` 与 `src/` 中 agent 相关目录的关系（docs 侧）
