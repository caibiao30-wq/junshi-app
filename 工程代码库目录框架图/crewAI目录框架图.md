# crewAI 工程代码库目录框架图（候选归纳）

> 状态：候选归纳，仅供产品设计参照，不升级为产品决策或通用模板。
> 来源：本地 /Users/caibiao/Downloads/crewAI-main（只读，未读取代码正文）。
> 深度：两层。第一层=顶层项；第二层=职责相关的主要子目录。未深入第三层。
> 凡职责依据目录名/命名推断、未读代码核实处，标注「待核验」。

## 顶层结构

├── lib/              → 职责：产品核心源码库（monorepo 组织，含 cli / crewai / crewai-core / crewai-files / crewai-tools / devtools 多个子包）
├── docs/             → 职责：文档站（Mintlify 风格 MDX，含各版本快照）
├── scripts/          → 职责：工程脚本（文档生成、测试辅助等）
├── .github/          → 职责：GitHub 协作与 CI/CD 配置（issue 模板、workflows、codeql）
├── AGENTS.md         → 职责：面向 AI/Agent 协作者的仓库说明与指引
├── DOCS_TRANSLATIONS.md → 职责：文档多语言翻译（ar/ko/pt-BR）协作说明
├── README.md         → 职责：项目概述与上手入口
├── LICENSE           → 职责：开源许可证
├── pyproject.toml    → 职责：Python 项目打包/依赖/工具配置
├── uv.lock           → 职责：uv 锁定的依赖版本清单
├── conftest.py       → 职责：pytest 根级测试配置/夹具
├── .pre-commit-config.yaml → 职责：pre-commit 钩子配置
├── .env.test         → 职责：测试环境变量示例
├── .python-version   → 职责：Python 版本声明
├── .gitignore        → 职责：Git 忽略规则
└── .editorconfig     → 职责：跨编辑器格式约定

## 第二层（职责相关的主要子目录）

├── lib/
│   ├── cli/          → 职责：命令行工具包（CrewAI CLI）
│   ├── crewai/       → 职责：主 Agent 框架库（核心 API）
│   ├── crewai-core/  → 职责：核心逻辑独立包【与 crewai 的边界关系待核验】
│   ├── crewai-files/ → 职责：文件处理/加载能力包
│   ├── crewai-tools/ → 职责：工具（tools）集成包
│   └── devtools/     → 职责：文档版本快照（docs/v*/）管理工具【由 AGENTS.md 佐证】

├── docs/
│   ├── edge/         → 职责：未发布的预览/最新文档（编辑入口）
│   ├── images/       → 职责：文档图片素材（被版本快照引用）
│   ├── index.mdx     → 职责：文档站首页
│   ├── docs.json     → 职责：文档站导航/路由配置
│   ├── common-room-tracking.js → 职责：站点埋点脚本（common-room）
│   ├── reo-tracking.js         → 职责：站点埋点脚本（reo）
│   └── v1.10.0 ～ v1.15.18     → 职责：各发布版本的冻结文档快照（按版本号分目录，由 devtools 管理，不可直接修改）

├── scripts/
│   ├── age90_file_input_runner.py → 职责：测试辅助运行脚本（文件名语义待核验）
│   └── docs/           → 职责：文档相关脚本（生成/同步/校验）

├── .github/
│   ├── ISSUE_TEMPLATE/ → 职责：Issue 模板
│   ├── workflows/      → 职责：CI/CD 工作流
│   ├── codeql/         → 职责：CodeQL 安全扫描配置
│   ├── dependabot.yml  → 职责：依赖自动更新配置
│   ├── pull_request_template.md → 职责：PR 模板
│   ├── CONTRIBUTING.md → 职责：贡献指南
│   └── security.md     → 职责：安全漏洞上报说明

## 无法确认 / 待核验清单

1. lib/ 各子包（cli/crewai/crewai-core/crewai-files/crewai-tools）的精确职责边界：仅按包名与 AGENTS.md 推断为 monorepo 多包，未读各包 pyproject 与内部结构核实，标注待核验。
2. crewai-core 与 crewai 之间的拆分关系：无法从目录名确认，待核验。
3. scripts/age90_file_input_runner.py 的具体用途：按文件名推断为测试辅助，语义待核验。
4. docs/ 版本快照 v1.10.0 至 v1.15.18 的覆盖范围与最新版本：仅列出目录名，最高版本是否为当前发布版本待核验。
5. 顶层配置文件（.pre-commit-config.yaml/.python-version/.env.test 等）的具体内容与使用方式：仅按惯例与文件名描述职责，未读内容。
6. 本地目录非 git 仓库（find 显示无 .git），无法提供 commit/tag 版本锚点；目录后缀 -main 提示为源码归档，具体版本待核验。
