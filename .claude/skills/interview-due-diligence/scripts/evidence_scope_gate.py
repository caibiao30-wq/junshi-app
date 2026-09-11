#!/usr/bin/env python3
"""evidence_scope_gate.py — 校验调查范围授权与来源登记结构（§5、§10）。

用法:
    python3 evidence_scope_gate.py <01_调查取证.md>

检查:
  1) 「调查范围」区块含 §5 关键字段；缺任一关键项 → 先提问、不开始外部取证
  2) 「来源登记」表可解析，含来源ID/类型/定位/获取时间/版本/访问状态/材料状态/证据等级
  3) 每个来源区块含必填 来源ID/类型/定位/获取时间/版本/权限/访问状态/材料状态/证据等级（source-schema 来源区块字段）；访问状态=不可访问的来源含失败原因并按失败处理、转入待核验
  4) question_id → evidence_ref 映射非空且逐问题有引用

规则:
  - 本脚本是启发式结构校验，无法判断语义时输出「需人工复核」，不视为通过。
  - 通过不构成定稿放行；定稿仍需方法学语义审查与主技能判断。
非零退出码 = 缺必填项/发现阻塞。本脚本只读，不修改文件。
"""

import argparse
import re
import sys
from pathlib import Path

# §5 调查范围必填字段 → 在「调查范围」区块内匹配的关键词
SCOPE_LABELS = [
    "调查目标与核心问题",
    "产出用途",
    "时间窗口",
    "版本锚点",
    "允许的来源类型",
    "平台授权",
    "联网",
    "排除范围",
    "失败来源处理方式",
    "验收条件",
]

# §10 来源登记表必填列
TABLE_COLUMNS = ["来源ID", "来源类型", "定位", "获取时间", "版本", "访问状态", "材料状态", "证据等级"]

# 每个来源区块必填标签（source-schema §二来源区块字段；权限为该区块字段，不在登记表列中）
SOURCE_BLOCK_REQUIRED = ["来源ID", "来源类型", "定位", "获取时间", "版本", "权限", "访问状态", "材料状态", "证据等级"]


def _section(text, title):
    """返回「title」区块（到下一个二级标题前的文本），无则返回空串。"""
    m = re.search(rf"^##\s+{re.escape(title)}.*?$(?=\n## |\Z)", text, flags=re.M | re.S)
    return m.group(0) if m else ""


def check_scope(text, problems):
    block = _section(text, "调查范围")
    if not block:
        problems.append("[范围] 未找到「调查范围」区块")
        return
    missing = [lab for lab in SCOPE_LABELS if lab not in block]
    if missing:
        problems.append("[范围] 缺关键字段：" + "、".join(missing))
        problems.append("[范围] 缺任一关键字段 → 应先提问、不开始外部取证")


def check_source_table(text, problems):
    block = _section(text, "来源登记")
    if not block:
        problems.append("[登记] 未找到「来源登记」区块")
        return
    header_line = next((ln for ln in block.splitlines() if "来源ID" in ln), None)
    if not header_line:
        problems.append("[登记] 来源登记表缺「来源ID」表头")
        return
    table = [ln.strip() for ln in block.splitlines() if ln.strip().startswith("|")
             and "---" not in ln and "来源ID" not in ln]
    if not table:
        problems.append("[登记] 来源登记表为空")
        return
    header_cols = [c.strip() for c in header_line.strip("|").split("|")]
    for col in TABLE_COLUMNS:
        if col not in header_cols:
            problems.append(f"[登记] 缺失列「{col}」")
            break
    for row in table:
        cells = [c.strip() for c in row.strip("|").split("|")]
        if len(cells) < len(header_cols):
            problems.append(f"[登记] 行字段数不足（缺列）：{cells}")

    # 不可访问来源必须记为失败并转入待核验
    if any("失败" in c or "不可访问" in c for row in table for c in row.split("|")):
        if "待核验" not in text:
            problems.append("[失败来源] 存在不可访问来源但未见待核验清单")


def check_source_blocks(text, problems):
    blocks = re.split(r"^###\s+来源", text, flags=re.M)[1:]
    if not blocks:
        problems.append("[来源] 未发现「### 来源」区块")
        return
    for b in blocks:
        for lab in SOURCE_BLOCK_REQUIRED:
            if not re.search(rf"{lab}[:：]", b):
                problems.append("[来源] 区块缺字段：" + lab)
                break
        if re.search(r"访问状态[:：]\s*失败", b) or re.search(r"不可访问", b):
            if not re.search(r"失败原因[:：]", b):
                problems.append("[来源] 不可访问来源须记录「失败原因」")


def check_question_map(text, problems):
    if "question_id → evidence_ref" not in text and "question_id → evidence_ref[]" not in text:
        problems.append("[映射] 未找到「question_id → evidence_ref」映射")
        return
    block = _section(text, "question_id")
    rows = [ln for ln in block.splitlines() if ln.strip().startswith("|") and "Q-" in ln]
    if not rows:
        problems.append("[映射] 映射为空（无 Q- 行）")
        return
    for row in rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        refs = [c for c in cells if re.fullmatch(r"SRC-\d+", c) or "SRC-" in c or "待核验" in c]
        if not refs:
            problems.append(f"[映射] 无证据引用：{row}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file")
    args = ap.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    problems = []
    check_scope(text, problems)
    check_source_table(text, problems)
    check_source_blocks(text, problems)
    check_question_map(text, problems)

    if problems:
        print("校验发现问题：", *problems, sep="\n  ")
        sys.exit(1)
    # 结构可解析；语义仍需人工复核，脚本不单独放行定稿
    print("校验通过（启发式）：调查范围、来源登记、不可访问来源处理、问题映射结构齐备。")
    print("注意：脚本不判语义，定稿前请进行方法学语义审查与主技能人工复核。")


if __name__ == "__main__":
    main()