# letta 工程代码库目录框架图

> **归纳状态：候选归纳**  
> **主来源：** `/Users/caibiao/Downloads/letta-main` 目录实际内容  
> **范围：** 仅检查本地仓库目录与文件名，并读取少量入口/元数据文件确认职责；未读取框架实现代码正文，未联网。  
> **关键核验结论：** 当前目录不是 Letta 的工程实现代码库，而是项目 landing page 仓库。其 `README.md` 与 `AGENTS.md` 均说明当前实现位于独立的 `letta-ai/letta-code` 仓库；该仓库未出现在本地 primary source 中。因此，Letta 当前工程代码库的目录框架**待核验**，以下先记录本地实际存在的目录框架，不将其臆测为实现代码结构。

## 顶层结构

├── `.github/`   → 职责：承载 GitHub 协作配置，包括 issue 模板、受信贡献者名单和自动化工作流。
├── `AGENTS.md`   → 职责：声明本仓库不是当前 Letta 实现，并规定历史分支与当前开发仓库的使用边界。
├── `AI_POLICY.md`   → 职责：规定项目相关 AI 使用、披露或治理要求。（具体条款未作为目录判断依据展开。）
├── `CITATION.cff`   → 职责：提供软件引用元数据和推荐学术引用信息。
├── `CONTRIBUTING.md`   → 职责：说明本仓库已归档，当前 Letta 开发应转向 `letta-ai/letta-code`。
├── `LICENSE`   → 职责：提供项目许可法律文本。
├── `PRIVACY.md`   → 职责：提供项目隐私政策文本。
├── `README.md`   → 职责：作为 Letta 项目 landing page，提供产品定位、入口和当前代码仓库指引。
├── `SECURITY.md`   → 职责：提供安全问题报告与处理说明。
└── `TERMS.md`   → 职责：提供服务或项目使用条款文本。

## 第二层（职责相关的主要子目录）

├── `.github/`
│   ├── `ISSUE_TEMPLATE/`   → 职责：提供 GitHub issue 提交模板与入口配置。
│   ├── `TRUSTED_CONTRIBUTORS`   → 职责：维护 issue 自动审核时可跳过限制检查的受信贡献者名单。
│   └── `workflows/`   → 职责：存放 GitHub Actions 自动化流程定义。
│       └── `issue-guard.yml`   → 职责：校验新 issue 的仓库归属、披露和反垃圾要求，并对不合规 issue 执行评论、标记、关闭与锁定。

## 工程实现代码目录（待核验）

本地 `/Users/caibiao/Downloads/letta-main` 中未发现可确认的工程实现目录或构建/依赖入口，例如 `src/`、`packages/`、`apps/`、`server/`、`runtime/`、`package.json`、`pyproject.toml` 等。基于本地一手文件可确认的边界如下：

- `README.md` 指出当前 source code 位于 `letta-ai/letta-code`，包含 agent harness、interactive terminal UI、App Server、channels 和 runtime。
- `AGENTS.md` 明确要求不要把本仓库作为 Letta implementation 使用，并将当前行为检查、开发和修改工作指向 `letta-ai/letta-code`。
- 本次未联网，也未读取外部仓库，因此 `letta-ai/letta-code` 的具体目录结构不能从本次 primary source 确认，标注为**待核验**。
- 本地仓库的 `archive` 分支被文件说明为已退休的 Letta V1 server 历史源；它不代表当前 Letta，也未纳入本次目录框架勘察。

## 覆盖范围与限制

- **已覆盖顶层目录：** `.github/`。
- **已覆盖顶层文件：** `AGENTS.md`、`AI_POLICY.md`、`CITATION.cff`、`CONTRIBUTING.md`、`LICENSE`、`PRIVACY.md`、`README.md`、`SECURITY.md`、`TERMS.md`。
- **未确认项：** 当前 Letta 工程实现仓库 `letta-ai/letta-code` 的目录布局。
- **阻塞：** 指定的本地 primary source 不包含当前工程代码；在不联网且不读取其他仓库的约束下，无法继续绘制当前实现的两层目录框架。
