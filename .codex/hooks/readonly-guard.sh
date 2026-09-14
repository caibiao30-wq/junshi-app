#!/bin/bash
# 只读审查门：当 CLAUDE_READONLY=1 时，阻止 Edit/Write 操作
# 退出码：0=放行, 2=阻止(stderr→Claude), 其他=非阻塞警告

# 读取 Claude Code 传入的 JSON（包含 tool_name, tool_input 等）
INPUT=$(cat)

# 提取 tool_name，兼容合法 JSON 中的空格
TOOL_NAME=$(printf '%s' "$INPUT" | sed -nE 's/.*"tool_name"[[:space:]]*:[[:space:]]*"([^"]*)".*/\1/p')

# 如果不是 Edit/Write，直接放行
if [[ "$TOOL_NAME" != "Edit" && "$TOOL_NAME" != "Write" ]]; then
  exit 0
fi

# 检查只读模式
if [[ "$CLAUDE_READONLY" == "1" ]]; then
  echo "🚫 当前处于只读模式，禁止文件修改操作。请先退出只读模式。" >&2
  exit 2
fi

# 默认放行
exit 0
