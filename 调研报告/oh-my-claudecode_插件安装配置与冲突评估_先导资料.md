# oh-my-claudecode（OMC）插件：安装配置先导资料与现有环境冲突评估

> 用途：交给另一个 Claude 窗口在本机执行安装与配置。本文先说明 OMC 是什么、怎么装、会动哪些文件，**再逐项评估与当前 Claude Code 现有配置的冲突**，最后给出安全安装的运行清单与回滚方法。
> 版本依据：GitHub `v5.4.0`（2026-09-11 发布）；npm 包名 `oh-my-claude-sisyphus`；plugin 名 `oh-my-claudecode`，marketplace 名 `omc`。
> 来源：仓库 README、`.claude-plugin/plugin.json`、`hooks/hooks.json`、`.mcp.json`、`skills/omc-setup/SKILL.md`、`scripts/plugin-setup.mjs`、`uninstall.sh`、`SECURITY.md`、`docs/MIGRATION.md`、`agents/`、`commands/`；以及本机 `~/.claude/settings.json`、`~/.claude/plugins/installed_plugins.json` 实测。

> **三份独立只读审计（config-audit / omc-research / omc-manifest）交叉验证过本文件**，关键冲突多为实证而非推测（如 statusLine 无条件覆写）。omc.vibetip.help/docs 站点访问受限，结论未依赖它，均取自 GitHub 官方源与本地实测。

---

## 一、OMC 是什么（不是普通 MCP）

OMC 不是单个 MCP server，而是 **Claude Code 的原生 marketplace 插件（Plugin）+ 一个 npm CLI 运行时（runtime）** 的「多智能体编排框架」。两条安装路线：

| 路线 | 机制 | 安装对象 |
| --- | --- | --- |
| **A. Marketplace/Plugin**（官方推荐，对多数用户） | 拉取 GitHub 仓库作为 marketplace，作为 plugin 安装 | 装进 `~/.claude/plugins/cache/`，注册 ~40 个 skills、~22 个 commands、19 个 agents、1 个 MCP server、一组 hooks |
| **B. npm CLI/runtime** | `npm i -g oh-my-claude-sisyphus` | 全局二进制 `omc` / `oh-my-claudecode`，供终端 `omc ...` 使用 |

**plugin.json 注册内容**（`.claude-plugin/plugin.json`）：
- **skills**（38 个）：`ai-slop-cleaner`、`ask`、`autopilot`、`autoresearch`、`cancel`、`debug`、`deep-interview`、`deepinit`、`drydock`、`execute`、`graph`、`harbor`、`hud`、`launch`、`loft`、`minimal-code-discipline`、`omc-doctor`、`omc-setup`、`plan`、`ralph`、`ralplan`、`release`、`remember`、`research`、`review`、`self-improve`、`skill`、`skillify`、`team`、`trace`、`ultragoal`、`verify`、`visual-verdict`、`wiki` 等。
- **commands**（~22 个，`commands/`）：`ask`、`autoresearch`、`compact`、`configure-notifications`、`debug`、`deepinit`、`external-context`、`hud`、`omc-doctor`、`omc-setup`、`project-session-manager`、`psm`、`release`、`remember`、`self-improve`、`skill`、`skillify`、`trace`、`verify`、`visual-verdict`、`wiki`。
- **agents**（19 个，`agents/`）：`analyst`、`architect`、`code-reviewer`、`code-simplifier`、`critic`、`debugger`、`designer`、`document-specialist`、`executor`、`explore`、`git-master`、`planner`、`qa-tester`、`scientist`、`security-reviewer`、`test-engineer`、`tracer`、`verifier`、`writer`。
- **MCP servers**（`.mcp.json`）：1 个名为 **`t`** 的 server，`node ${CLAUDE_PLUGIN_ROOT}/bridge/mcp-server.cjs`（OMC 状态 MCP 工具）。
- **hooks**（`hooks/hooks.json`）：一组编排 hook（见下文冲突第 4 条）。

**两条路线可独立使用**：只走 A（插件/skills）不需要装 npm；只走 B（`omc` CLI）不装插件。`omc team` 还需 **tmux**。

---

## 二、安装与配置步骤（标准流程）

### 路线 A：Marketplace/Plugin（推荐先走这条）

在 Claude Code 会话里**逐条**执行（README 明确提示两条一起粘贴会失败）：

```bash
/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
/plugin install oh-my-claudecode
```

然后**关键一步——setup**（会改配置，见冲突）：
```bash
/oh-my-claudecode:omc-setup          # 全量向导（会写 CLAUDE.md + HUD + 状态）
/oh-my-claudecode:omc-setup --local  # 只配当前项目
/oh-my-claudecode:omc-setup --global # 只配全局（默认会改写 ~/.claude/CLAUDE.md）
/oh-my-claudecode:omc-setup --force  # 强制重跑全量
/oh-my-claudecode:omc-setup --help   # 查看帮助
```

### 路线 B：npm CLI（可选，装 `omc` 终端命令）

```bash
npm i -g oh-my-claude-sisyphus@latest   # 已知会打 better-sqlite3 原生编译警告（#2913，无害）
omc setup                                # 终端版 setup
```

### 更新
- 插件：`/plugin marketplace update omc` → 重跑 `omc-setup`；缓存异常用 `/oh-my-claudecode:omc-doctor`。
- npm：`npm i -g oh-my-claude-sisyphus@latest`。

### 硬性前置
- Claude Code CLI + Claude Max/Pro 订阅 **或** Anthropic API key。
- `omc team` / `omc wait`：需 **tmux**（macOS `brew install tmux`）。
- 可选外部 CLI（非必需）：`codex`、`gemini`、`agy`(antigravity)、`grok`、`cursor-agent`。

---

## 三、★ 与本机现有配置的冲突评估（核心）

本机现状要点（来自 `~/.claude/settings.json` 实测）：
- **模型走第三方中转**：`ANTHROPIC_BASE_URL=https://llm.goaichat.top`，且 `ANTHROPIC_DEFAULT_SONNET_MODEL=qwen3.8-max-0902`、`DEFAULT_OPUS_MODEL=kimi-k3`、`DEFAULT_HAIKU_MODEL=glm-5.3`、`ANTHROPIC_MODEL=qwen3.8-max-0902`、`CLAUDE_CODE_SUBAGENT_MODEL=glm-5.3`。
- **statusLine 已被 claude-hud 占用**：`~/.claude/plugins/claude-hud/statusline-wrapper.sh`。
- **已启用 8 个插件**：claude-hud、typescript-lsp、hookify、claude-md-management、security-guidance、commit-commands、claude-code-setup、context-mode（另有项目级 ponytail）。
- **已注册密集 hooks**：Orca agent-hooks（SessionStart/UserPromptSubmit/Stop/StopFailure/SubagentStart/SubagentStop/TeammateIdle/PreToolUse/PostToolUse/PostToolUseFailure/PermissionRequest/PostCompact）+ context-mode-cache-heal(SessionStart) + ponytail(项目 SessionStart/SubagentStart/UserPromptSubmit)。
- **权限**：`defaultMode=acceptEdits`；`deny` 含 `Bash(curl *)`、`Bash(wget *)`；`enableAllProjectMcpServers=false`；`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`。

### 冲突 1 — `setup` 会改写 CLAUDE.md（高风险，最需防护）
`omc-setup` 通过 `scripts/setup-claude-md.sh` 把 OMC 配置写入 `.claude/CLAUDE.md`（local）或 `~/.claude/CLAUDE.md`（global）。**`--global` 默认「显式覆盖 `~/.claude/CLAUDE.md`」**，另有 `preserve` 模式可保留原 CLAUDE.md、把 OMC 装进 `CLAUDE-omc.md`。
> 你当前项目的 `docs/CLAUDE.md` 是经过精心维护的学业军师工程规范，`~/.claude/CLAUDE.md` 是全局行为准则。**必须**：执行 setup 前先备份两个 CLAUDE.md；全局用 `preserve` 模式；项目尽量跳过 `--local` 或用 `--force` 前的完整备份兜底。

### 冲突 2 — statusLine / HUD 撞车 claude-hud（★已确认，高风险）
`scripts/plugin-setup.mjs`（post-install 必跑）会**无条件覆写 `settings.json` 的 `statusLine`，清掉任何已有 statusline**，并写 `~/.claude/hud/`（lib、omc-hud.mjs 等）。而你的 statusLine 当前被 **claude-hud** 占用。装 OMC 后 claude-hud 的 HUD 会被 OMC 顶掉，二者只能留一个，需安装后二选一并手动重建 claude-hud 的 statusline。

### 冲突 3 — 模型路由不匹配（中高）
OMC 核心卖点是「智能模型路由：简单任务走 Haiku、复杂走 Opus」，其模型兼容矩阵/预设（premium/balanced/budget）按**真实 Anthropic Haiku/Sonnet/Opus** 设计。而本机把 Haiku/Sonnet/Opus 全部重映射到第三方中转的 **glm-5.3 / qwen3.8-max-0902 / kimi-k3**。后果：OMC 的按复杂度选模型、以及其 `omc team` 派生的 `claude` 子进程（继承 `ANTHROPIC_BASE_URL` 走中转）行为可能不符合预期；`omc ask codex/gemini/antigravity` 需要额外安装外部 CLI。

### 冲突 4 — hooks 矩阵高度重叠（中，确认会 patch settings.json）
OMC 注册 **21 个脚本 / 11 个事件**的 hooks（`hooks/hooks.json`），且 post-install 会把 OMC hooks **合并/覆写进 `~/.claude/settings.json` 的 hooks 字段**（plugin-setup.mjs patch hooks/hooks.json）。与本机已有 hooks 在同一批高频事件上重叠：

| 事件 | OMC 新增 | 本机已有 |
| --- | --- | --- |
| UserPromptSubmit | keyword-detector(30s)、skill-injector(30s) | Orca、ponytail |
| SessionStart | session-start/project-memory/wiki-session-start、init、maintenance | Orca、context-mode-cache-heal、ponytail |
| PreToolUse | pre-tool-enforcer | Orca |
| PostToolUse | post-tool-verifier、project-memory-posttool、post-tool-rules-injector | Orca |
| PostToolUseFailure | post-tool-use-failure | Orca |
| PermissionRequest(matcher=Bash) | permission-handler | Orca |
| SubagentStart/SubagentStop / PreCompact / Stop / SessionEnd | OMC 编排脚本 | Orca（SubagentStart/Stop、Stop、PostCompact） |

逐条按顺序叠加执行：每个提示/每次工具调用都会多跑数条带 30s 超时的 node 脚本 → **延迟上升**；`UserPromptSubmit` 的 keyword-detector/skill-injector 每次提交都运行、可改写注入上下文；`PermissionRequest matcher=Bash` 处理器可能与 Orca 权限处理及你的 deny 规则交互。**可整体禁用**：设 `DISABLE_OMC=1` 或 `OMC_SKIP_HOOKS` 关闭 OMC hooks（不动系统 hooks）。

### 冲突 5 — MCP `t` server（低风险，有默认保护）
OMC 自带的 `t` MCP 走 `node bridge/mcp-server.cjs`。本机 `enableAllProjectMcpServers=false`，所以**不会自动启用**，需要时再显式允许——这反而是安全的默认。

### 冲突 6 — `deny Bash(curl *)/wget` 削弱部分功能（低-中）
OMC 的 `external-context`、`research` 等技能及部分更新路径可能 shell 调 `curl`/`wget`，会被你的 deny 规则拦截 → 这些功能降级或报错。若想完整可用，需要你在本机权限里对这些命令**临时放行**（属修改权限，需你亲自确认，不要由执行代理代办）。

### 冲突 7 — npm 运行时 / tmux 运维依赖（中）
npm 路线装 `oh-my-claude-sisyphus` 需编译 **better-sqlite3**（原生 addon，可能有编译失败风险）；`omc team`/`omc wait` 需 **tmux**（macOS `brew install tmux`）。两路线都建议先确认 node/npm 版本。

### 冲突 8 — 技能/命令/代理名称重叠（低-中）
插件内 skills/commands 带 `oh-my-claudecode:` 前缀，多数不冲突；但 `omc setup` 会把 skills/agents **复制到用户/项目级目录**，届时可能覆盖/叠加同名项：
- skill：**`research`**（你已有同名 skill）、`hud`（撞 claude-hud）、`compact`、`remember`、`review` 等。
- agent：`explore`（与现有 `Explore` 近似），其余 18 个与现有 12 个全局代理大多不同名。

### 冲突 9 — 供应链/自动更新/外部 worker auto-approve（中-高，与安全相关）
- **在缓存里自动跑 `npm install --omit=dev`**，并有**静默自动更新**（`disableAutoUpdate`/`OMC_SECURITY=strict` 才关）→ 供应链面大，建议手动安装并锁版本。
- **外部 LLM worker 以 auto-approve 启动**：Codex `--dangerously-bypass-approvals-and-sandbox`、Gemini `--approval-mode yolo`、Grok `--always-approve`，等同 `--dangerously-skip-permissions`。**必须** `export OMC_SECURITY=strict`（禁远程 MCP、禁 Codex/Gemini/Grok、禁自动更新、工具路径限制到项目根、Python REPL 沙箱），或干脆不装任何外部 worker CLI。
- OMC 信任的二进制路径前缀白名单 `/usr/local/bin /usr/bin /opt/homebrew ...`，可用 `OMC_TRUSTED_CLI_DIRS` 扩展；无 OS 级进程沙箱、agent 间无安全边界。
- 你的 deny 含 `Bash(curl *)`/`wget`，结合 OMC 的远程 MCP / 自动下载面，**建议保持 `strict` 并把外部 MCP/LLM 全关**。

### 冲突 10 — 状态目录落盘到工作区（低-中，工程仓库需注意）
OMC 默认在 `{worktree}/.omc/` 写 state/notepad/plans/research/logs/team 等（唯一可提交项 `.omc/skills/**`），并**向 git exclude（非 .gitignore）追加 `.omc/.omx`**。若在 junshi-app 工程仓库试用，`.omc/` 会持续落盘运行时状态，建议用 `OMC_STATE_DIR` 指到 `~/.claude/omc/{project}/` 集中存放，避免污染仓库。

---

## 四、★ 安全安装运行清单（交给执行窗口）

> 执行方务必遵守：**先备份，再动手；每一步验证；不改权限与 CLAUDE.md 本体除非先备份。**

1. **备份**（先做）：
   ```bash
   cp ~/.claude/settings.json ~/.claude/settings.json.omc.bak
   cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.omc.bak
   cp docs/CLAUDE.md docs/CLAUDE.md.omc.bak        # 项目规范，务必保护
   cp -r ~/.claude/plugins ~/.claude/plugins.omc.bak
   ```
2. **（推荐路线 A）装插件**：逐条跑 `/plugin marketplace add ...` 与 `/plugin install oh-my-claudecode`；用 `/oh-my-claudecode:omc-setup --help` 确认模式。
3. **跑 setup 用安全姿态**：优先只做全局且用 preserve 模式（保 CLAUDE.md）；项目级宁可跳过，避免污染 `docs/CLAUDE.md`。
4. **处理 statusLine 二选一**：OMC post-install 会无条件覆写 statusLine，决定保留 OMC HUD 还是 claude-hud；若保留 claude-hud，装后手动重建其 statusline。
5. **设安全项**：`export OMC_SECURITY=strict`（禁远程 MCP/外部 LLM/自动更新）；不装任何外部 worker CLI；必要时 `export OMC_STATE_DIR=$HOME/.claude/omc/{工程}/` 集中状态，避免污染仓库。
6. **验证**：开新会话，确认 skill/agent/command 已可见、hook 正常、`t` MCP 是否按需启用；观察首轮工具调用延迟是否可接受。
6. **冲突若被放大则回滚**（官方提供卸载与回滚入口）：
   - 卸载插件：`/plugin uninstall oh-my-claudecode@oh-my-claudecode`；再手动清旧残留
     `rm ~/.claude/agents/{architect,executor,planner,critic,...}.md`、`rm ~/.claude/commands/{analyze,autopilot,deepsearch}.md`
   - 命令级回滚：`omc checkpoint rollback <id> --force`（git shadow 提交，存 `refs/omc/checkpoints/`，restore 后 `git clean -fd`）；
     多仓库回退 `export OMC_DISABLE_MULTIREPO=1` 或 `unset`
   - 恢复备份文件：
     ```bash
     cp ~/.claude/settings.json.omc.bak ~/.claude/settings.json
     cp ~/.claude/CLAUDE.md.omc.bak ~/.claude/CLAUDE.md
     cp docs/CLAUDE.md.omc.bak docs/CLAUDE.md
     ```
   - npm 路线：`npm uninstall -g oh-my-claude-sisyphus`

> 版本漂移备注：v5.4.0 tag 下 `docs/REFERENCE.md` 顶部仍自述 "for v5.3.0"。本文件中的 skills/agents/tools/hooks 数目，以**仓库目录级清单**（`plugin.json`/`hooks/hooks.json`/`agents/`/`commands/`）为准，REFERENCE.md 里的具体数字仅供参照、可能滞后。

---

## 五、结论与建议

- OMC 是**功能强大但侵入性强**的编排框架：会加约 40 个 skills、19 个 agents、约 20 条 hooks（11 事件）、1 个 MCP（55 tools），post-install **无条件覆写 statusLine、patch settings.json 的 hooks**，setup 会**改写 CLAUDE.md**，并写状态目录 `.omc/`。
- 与本机环境**最实质的冲突**：① setup 改写 CLAUDE.md（工程规范，高）；② statusLine/HUD 无条件覆写撞 claude-hud（已确认）；③ 模型路由依赖真实 Claude 模型而本机走第三方中转；④ hooks 高频事件重度叠加；⑤ 供应链/自动更新/外部 worker auto-approve；⑥ deny curl/wget 削弱部分技能；⑦ 需要 tmux/原生编译。
- **建议**：若要试用，走**路线 A（插件）**、setup 用全局 `preserve`、装后保留 claude-hud、设 `OMC_SECURITY=strict`、不装外部 worker CLI、`OMC_STATE_DIR` 集中状态、暂不启用 `t` MCP、先备份再装；把「装完-对比-回滚」作为一次可逆实验（官方提供 `/plugin uninstall` 与 `omc checkpoint rollback`），勿一次性全量启用以免覆盖现有工程规范与插件生态。
- 判断为基于仓库 manifest/脚本与本地 settings **实测的推论**；个别 hooks 是否真正冲突需装后实测确认（README 自述 19 agents/39 skills/55 tools 等数字存在 REFERENCE.md 版本漂移，本文件以其目录级清单为准）。

---

## 六、安装前另需处理的既有配置问题（config-audit 跨切面发现，与本插件无关但高优先）

执行窗口在动手前应知会用户，而非代改权限/凭据：
1. **`~/.claude/settings.json` 含明文 `ANTHROPIC_API_KEY`** + 第三方中转 `ANTHROPIC_BASE_URL` 与模型映射 → 最高优先安全项，建议**轮换 key 并移出 JSON**（不要把完整 key 复制进任何报告/日志）。
2. **ponytail projectPath 与当前 worktree 不一致**：项目 settings 启用 `ponytail@ponytail`，但 installed_plugins.json 记录 `projectPath=/Users/caibiao/orca/projects/junshi-app`，当前 worktree 是 `/Users/caibiao/orca/workspaces/junshi-app/docs` → 其 `${CLAUDE_PLUGIN_ROOT}` hooks 可能解析失败/不加载，启用 OMC 前需确认 project scope 是否命中。
3. **`.claude/hooks/readonly-guard.sh` 已存在但未绑定任何 hook 事件**（且用 sed 解析 JSON、stderr 含 emoji）→ 项目的「默认只读」纪律并未被 hook 强制执行，与全局 `acceptEdits` 存在张力。
4. **MCP 作用域**：项目无 `.mcp.json`，server 在用户级 `~/.claude.json`（github/context7/filesystem）；`enableAllProjectMcpServers` 值需核实，避免自动放行未知项目服务。安装 OMC 的 `t` server 前明确作用域与数据边界。

### 附：本次结论的证据定位
- 仓库 README（`gh api .../readme`）：安装命令、组件表、tmux/外部 CLI 要求、HUD。
- `.claude-plugin/plugin.json`：38 skills + commands + `.mcp.json`。
- `hooks/hooks.json`：OMC hooks 事件与 matcher。
- `.mcp.json`：`t` server 命令。
- `skills/omc-setup/SKILL.md`：setup 写入路径、--local/--global/preserve 语义、CLAUDE.md 改写。
- `agents/`：19 个 agent 名。
- `commands/`：22 个命令名。
- 本机 `~/.claude/settings.json`：模型 env、statusLine、enabledPlugins、hooks、permissions、enableAllProjectMcpServers。
