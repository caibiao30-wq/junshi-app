# awesome-claude-code-subagents 工程代码库目录框架图

> **状态标注：候选归纳**（只读勘察产物，非产品决策、非通用模板）。
> 依据：本地一手来源 `/Users/caibiao/Downloads/awesome-claude-code-subagents-main`（`find -maxdepth 2` 实扫 + 仓库自身 README/CONTRIBUTING 标题佐证）。仅覆盖两层目录布局，未读 agent 定义正文、未研究框架 API。

## 顶层结构

```
awesome-claude-code-subagents-main/
├── .claude/              → 职责：Claude 本地运行设置（agent 运行时配置）
├── .claude-plugin/       → 职责：插件元数据（marketplace 市场清单）
├── .github/              → 职责：GitHub 仓库集成（CI 工作流）
├── .gitignore            → 职责：Git 忽略规则
├── categories/           → 职责：Agent 产品主体——按领域分区的全部 subagent 定义目录（核心资产）
├── CLAUDE.md             → 职责：仓库级 Claude Code 指令（agent 使用/开发约定）
├── CONTRIBUTING.md       → 职责：贡献指南（新增 agent、分类归属、版本号同步流程）
├── install-agents.sh     → 职责：交互式安装/卸载脚本（将 agent 从本仓库装入全局或本地 .claude/agents）
├── LICENSE               → 职责：开源许可证
├── README.md             → 职责：总览文档（分类索引、安装方式、subagent 结构、通信协议、工具说明）
└── tools/                → 职责：配套工具目录（增强目录体验的 Claude Code skill）
```

## 第二层（职责相关的主要子目录）

```
├── .claude/
│   └── settings.local.json   → 职责：Claude 本地运行设置（本项目级覆盖配置）
├── .claude-plugin/
│   └── marketplace.json      → 职责：插件市场清单，登记各分类插件及其版本（与分类内 plugin.json 版本同步）
├── .github/
│   └── workflows/
│       └── enforce-plugin-version-bump.yml → 职责：CI 校验插件版本号变更（发布前强制 bump 以支持 claude plugin update）
├── categories/
│   ├── 01-core-development/      → 职责：核心开发 agent（通用编程/语言无关开发角色），12 项
│   ├── 02-language-specialists/  → 职责：特定语言专家 agent（python、go、rust、react 等），31 项
│   ├── 03-infrastructure/        → 职责：基础设施 agent（云/部署/架构运维），17 项
│   ├── 04-quality-security/      → 职责：质量与安全 agent（测试/代码审查/安全），18 项
│   ├── 05-data-ai/              → 职责：数据与 AI agent（数据处理/机器学习/AI 工程），14 项
│   ├── 06-developer-experience/ → 职责：开发者体验 agent（提效工具/工作流），17 项
│   ├── 07-specialized-domains/  → 职责：专业领域 agent（细分行业/垂直场景），17 项
│   ├── 08-business-product/     → 职责：业务与产品 agent（产品/业务/增长），18 项
│   ├── 09-meta-orchestration/   → 职责：元编排 agent（多 agent 协调/管理层），12 项
│   └── 10-research-analysis/    → 职责：研究与分析 agent（调研/信息分析），12 项
│   （注：每个分类目录内均含 1 份 README.md + 若干 agent 定义 .md；agent 定义文件属第三层，不在本图展开）
└── tools/
    └── subagent-catalog/        → 职责：目录浏览管理 skill（列出/检索/搜索 subagent，带 12h 缓存与原子更新）
        ├── README.md            → 职责：工具说明与用法
        ├── config.sh            → 职责：缓存路径与 TTL 等配置
        ├── list.md / search.md / fetch.md / invalidate.md → 职责：目录的列出/搜索/拉取/缓存失效子命令说明（第三层，职责待核验）
```

## 归纳说明

- **职责分域逻辑**：仓库以「categories/ 存 agent 产品本体、tools/ 存配套工具、顶层文档与脚本负责元信息与分发」三层职责划分；categories 内部再按领域（开发/语言/基础设施/安全/数据/体验/领域/业务/编排/研究）进一步分域。
- **贡献约定**（据 CONTRIBUTING.md）：新增 agent 需同时更新主 README、分类 README、agent 定义文件，并同步分类内 plugin.json 与 marketplace.json 版本——印证 categories 与 .claude-plugin 的职责关联。
- **待核验项**：
  1. `tools/subagent-catalog/` 内 `fetch.md`/`invalidate.md` 等单个命令文件的精确职责（仅据文件命名推断）。
  2. `.claude/settings.local.json` 的具体配置内容（未读正文）。
  3. 各分类目录内是否存在分类级 `.claude-plugin/plugin.json`（据 CONTRIBUTING 推断存在，未实扫确认，属第三层）。
