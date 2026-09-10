# Claude Code 项目配置审计报告

**审计对象：** `/Users/caibiao/orca/projects/junshi-app`  
**审计日期：** 2026-08-24  
**审计者：** codex  
**文档性质：** 调研报告（只追加，不改写）

---

## 1. 审计概述

本次审计依据 Claude Code 官方文档（https://code.claude.com/docs/en/claude-directory）对 `junshi-app` 仓库的 `.claude/` 目录进行配置完整性检查，识别缺口并执行补齐。

## 2. 审计前状态

### 2.1 已有配置（健康）

| 配置项 | 文件 | 状态 | 说明 |
|--------|------|------|------|
| 项目指令 | `CLAUDE.md` | ✅ 完整 | ~30 行，引用的文件路径均有效 |
| 智能体指令 | `AGENTS.md` | ✅ 完整 | 正确指向 CLAUDE.md |
| 规则文件 | `.claude/rules/` (4 个) | ✅ 完整 | write-discipline、read-routing、anti-patterns、status-discipline |
| 子代理 | `.claude/agents/` (6 个) | ✅ 完整 | config-auditor、file-updater、grilling、orchestrator、repo-scanner、research |
| 技能 | `.claude/skills/` (2 个) | ✅ 完整 | enter-draft、graphify |

### 2.2 缺失配置（需补齐）

| 配置项 | 文件 | 缺失类型 | 优先级 |
|--------|------|----------|--------|
| 忽略文件 | `.gitignore` | 完全缺失 | P0 |
| 忽略文件 | `.claudeignore` | 完全缺失 | P1 |
| 本地设置 | `.claude/settings.local.json` | 内容不完整 | P0 |
| 钩子脚本 | `.claude/hooks/readonly-guard.sh` | 内容为空壳 | P0 |
| 自定义命令 | `.claude/commands/` | 目录不存在 | P1 |
| 智能体记忆 | `.claude/agent-memory/` | 目录不存在 | P2 |

## 3. 问题详解

### 3.1 P0：`.gitignore` 完全缺失

**问题描述：** 仓库没有 `.gitignore` 文件，导致以下风险：
- `.claude/settings.local.json` 可能被提交到 git（含敏感配置）
- `.claude/agent-memory/` 可能被提交（含会话记忆）
- `.DS_Store`、`node_modules/`、`dist/` 等无关文件可能被提交

**风险等级：** 高  
**修复方案：** 创建 `.gitignore`，排除敏感文件和构建产物

### 3.2 P0：`.claude/settings.local.json` 内容不完整

**问题描述：** 现有配置只有 `enabledPlugins` 和空的 `enabledMcpjsonServers`，缺少：
- `permissions`：没有定义权限规则，所有工具调用都需要逐次确认
- `hooks`：没有注册钩子，`readonly-guard.sh` 即使有逻辑也不会被调用

**风险等级：** 高  
**修复方案：** 添加 `permissions`（allow/deny/defaultMode）和 `hooks`（PreToolUse）

### 3.3 P0：`.claude/hooks/readonly-guard.sh` 是空壳

**问题描述：** 文件只有 3 行（shebang + 2 行注释），没有实际逻辑：
```bash
#!/bin/bash
# 只读审查门：任务声明包含"只读"时，禁止 Edit/Write
# 在 Claude Code settings.json 中配置为 PreToolUse hook
```

**风险等级：** 中（因为没有注册到 hooks，实际上不会执行）  
**修复方案：** 实现完整逻辑：读取 stdin JSON → 检查 `CLAUDE_READONLY` 环境变量 → 退出码 0=放行/2=阻止

### 3.4 P1：`.claudeignore` 完全缺失

**问题描述：** 没有 `.claudeignore` 文件，Claude 会读取所有文件（包括 `node_modules/`、`dist/`、`build/`），浪费 token。

**风险等级：** 低（影响效率，不影响功能）  
**修复方案：** 创建 `.claudeignore`，排除构建产物和依赖目录

### 3.5 P1：`.claude/commands/` 目录不存在

**问题描述：** 没有自定义命令，无法通过 `/command` 快捷操作。

**风险等级：** 低（功能缺失，不影响现有工作）  
**修复方案：** 创建 `commands/` 目录，添加 `audit.md`、`grill.md`、`draft.md`

### 3.6 P2：`.claude/agent-memory/` 目录不存在

**问题描述：** 没有智能体记忆目录，无法跨会话持久化知识。

**风险等级：** 低（功能缺失，不影响现有工作）  
**修复方案：** 创建 `agent-memory/` 目录，添加 `README.md` 说明用途

## 4. 修复方案

### 4.1 变更清单

| 优先级 | 文件 | 操作 | 说明 |
|--------|------|------|------|
| P0 | `.gitignore` | 新建 | 排除敏感文件和构建产物 |
| P0 | `.claude/settings.local.json` | 重写 | 添加 permissions + hooks |
| P0 | `.claude/hooks/readonly-guard.sh` | 重写 | 实现完整逻辑 |
| P1 | `.claudeignore` | 新建 | 排除无关文件，节省 token |
| P1 | `.claude/commands/audit.md` | 新建 | 审计配置一致性 |
| P1 | `.claude/commands/grill.md` | 新建 | 深度追问设计方案 |
| P1 | `.claude/commands/draft.md` | 新建 | 进入草稿模式 |
| P2 | `.claude/agent-memory/` | 新建 | 智能体持久化记忆目录 |

### 4.2 变更架构

```
junshi-app/
├── .gitignore                    ← NEW
├── .claudeignore                 ← NEW
├── CLAUDE.md                     (unchanged)
├── AGENTS.md                     (unchanged)
└── .claude/
    ├── settings.local.json       ← REWRITTEN (permissions + hooks)
    ├── hooks/
    │   └── readonly-guard.sh     ← REWRITTEN (actual logic)
    ├── commands/
    │   ├── audit.md              ← NEW
    │   ├── grill.md              ← NEW
    │   └── draft.md              ← NEW
    ├── agents/                   (unchanged, 6 agents)
    ├── rules/                    (unchanged, 4 rules)
    ├── skills/                   (unchanged)
    └── agent-memory/
        └── README.md             ← NEW
```

## 5. 验证清单

### 5.1 文件完整性

- [x] `.gitignore` 已创建，包含正确的排除模式
- [x] `.claudeignore` 已创建，包含正确的排除模式
- [x] `.claude/settings.local.json` 已重写，包含 permissions + hooks
- [x] `.claude/hooks/readonly-guard.sh` 已重写，有实际逻辑
- [x] `.claude/commands/` 目录已创建，包含 3 个命令文件
- [x] `.claude/agent-memory/` 目录已创建，包含 README.md

### 5.2 内容正确性

- [x] `.gitignore` 排除 `.claude/settings.local.json`（敏感配置）
- [x] `.gitignore` 排除 `.claude/agent-memory/`（会话记忆）
- [x] `.claudeignore` 排除 `node_modules/`、`dist/`、`build/`（节省 token）
- [x] `settings.local.json` 的 `permissions` 包含合理的 allow/deny 规则
- [x] `settings.local.json` 的 `hooks` 正确注册 `readonly-guard.sh`
- [x] `readonly-guard.sh` 读取 stdin JSON，检查 `CLAUDE_READONLY`，返回正确退出码
- [x] 命令文件格式正确，内容清晰

### 5.3 功能验证

- [x] JSON 文件可解析（无语法错误）
- [x] Shell 脚本有执行权限（`chmod +x`）
- [x] `.gitignore` 排除项正确（不会误排除必要文件）
- [x] `.claudeignore` 排除项正确（不会误排除配置文件）

## 6. 后续建议

### 6.1 立即可用

- **只读模式：** `export CLAUDE_READONLY=1` 启用，`readonly-guard.sh` 会阻止 Edit/Write
- **自定义命令：** `/audit`、`/grill`、`/draft` 可直接使用

### 6.2 可选扩展

| 配置项 | 用途 | 优先级 |
|--------|------|--------|
| `.claude/output-styles/` | 自定义输出样式 | P2 |
| 更多自定义命令 | 根据工作流需要添加 | P2 |
| 更多子代理 | 根据任务类型添加 | P2 |

### 6.3 团队协作

如果未来需要多人协作：
1. 将团队共享配置写入 `.claude/settings.json`（提交到 git）
2. 将个人本地配置保留在 `.claude/settings.local.json`（不提交到 git）
3. 两者会自动合并，`settings.local.json` 优先级更高

---

**审计完成日期：** 2026-08-24  
**审计者：** codex
