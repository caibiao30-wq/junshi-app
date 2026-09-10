# agno 工程代码库目录框架图（候选归纳）

> 状态：候选归纳，仅供产品设计参照，不升级为产品决策或通用模板。
> 来源：本地 /Users/caibiao/Downloads/agno-main（只读，未读取代码正文）。
> 深度：两层。第一层=顶层项；第二层=职责相关的主要子目录。未深入第三层。
> 凡职责依据目录名推断、未读代码核实处，标注「待核验」。

## 顶层结构

├── libs/              → 职责：产品核心代码库（monorepo 源，含 agno / agno_infra / agnoctl 三个子库）
├── cookbook/          → 职责：面向用户的示例/教程/用例集（按主题分目编排的用法示例）
├── scripts/           → 职责：开发、测试、格式化、环境搭建等工程脚本（sh/bat 双平台）
├── .github/           → 职责：GitHub 协作与 CI/CD 配置（issue 模板、工作流）
├── AGENTS.md          → 职责：面向 AI/Agent 协作者的仓库说明与指引
├── CLAUDE.md          → 职责：面向 Claude 等 AI 助手的仓库项目说明（约定与工作上下文）
├── README.md          → 职责：项目概述与上手入口
├── CONTRIBUTING.md    → 职责：贡献指南
├── CODE_OF_CONDUCT.md → 职责：社区行为准则
├── CODEOWNERS         → 职责：代码所有权与评审人归属配置
├── LICENSE            → 职责：开源许可证
├── .gitignore         → 职责：Git 忽略规则
├── .editorconfig      → 职责：跨编辑器格式约定
└── .cursorrules       → 职责：面向 Cursor 编辑器的 AI 辅助规则

## 第二层（职责相关的主要子目录）

├── libs/
│   ├── agno/       → 职责：主 Agent 框架库（核心包、数据库迁移、测试、打包配置）
│   ├── agno_infra/ → 职责：基础设施相关库（部署/运行依赖，独立打包与测试）
│   └── agnoctl/    → 职责：命令行工具（agnoctl CLI）库，独立打包与测试

├── cookbook/
│   ├── 00_quickstart   → 职责：快速上手示例（按编号 00 起步）
│   ├── 01_demo ～ 13_filesystem → 职责：按能力分域的示例（agents/teams/workflows/storage/knowledge/learning/evals/reasoning/memory/context/filesystem 等）【编号语义为职责推断，待核验】
│   ├── 90_models        → 职责：各模型接入示例
│   ├── 91_tools         → 职责：各工具集成示例
│   ├── 93_components    → 职责：组件化用法示例
│   ├── 99_docs          → 职责：文档相关示例
│   ├── frameworks       → 职责：与外部框架集成示例
│   ├── integrations     → 职责：第三方/平台集成示例
│   ├── environments     → 职责：运行环境相关示例
│   ├── observability    → 职责：可观测性示例
│   ├── performance      → 职责：性能调优示例
│   ├── data_labeling    → 职责：数据标注相关示例
│   ├── gemini_3         → 职责：Gemini 3 模型相关示例
│   ├── code             → 职责：代码类示例
│   ├── examples         → 职责：综合/额外示例集
│   └── scripts          → 职责：cookbook 配套脚本

├── scripts/
│   ├── *_setup.sh / *.bat / *.ps1 → 职责：各环境搭建脚本（dev/test/perf/demo/cookbook）【跨平台对应关系待核验】
│   ├── test.sh / test.bat         → 职责：测试运行入口
│   ├── format.sh / format.bat     → 职责：代码格式化入口
│   ├── validate.sh / validate.bat → 职责：校验入口
│   ├── run_model_tests.sh         → 职责：模型测试运行脚本
│   └── _utils.sh / _utils.bat     → 职责：脚本共享工具函数

├── .github/
│   ├── ISSUE_TEMPLATE/ → 职责：Issue 模板（bug-report / feature-request / config）
│   ├── workflows/      → 职责：CI/CD 工作流（test / release / performance / pr-lint / pr-triage / claude / test_on_release）
│   └── pull_request_template.md → 职责：PR 模板

## 无法确认 / 待核验清单

1. cookbook 各编号目录（01_demo～13_filesystem）的具体内容映射：仅按目录名推断为分域能力示例，未读内容核实，标注待核验。
2. libs/agno/agno 内部子包结构（model/tool/agent 等）：属第三层，未展开，职责需进一步分层才能确认。
3. scripts/ 中各 setup 脚本与开发/测试/性能环境的精确对应关系：按文件名推断，待核验。
4. 顶层若干文件（.cursorrules/.editorconfig/CODEOWNERS）仅按惯例描述职责，未读内容。
