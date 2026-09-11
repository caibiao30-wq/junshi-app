#!/usr/bin/env python3
"""evidence_gate.py — 检查调查取证汇总文件是否满足证据包必备区块。

用法:
    python3 evidence_gate.py <01_调查取证.md>

检查:
  1) 是否包含来源区块、证据概括、来源冲突/限制、待核验清单
  2) 每条证据是否标记来源定位和材料状态
  3) 待核验清单是否非空
  4) 逐来源校验必填字段（来源ID/类型/定位/获取时间/版本/权限/访问状态/材料状态/证据等级），缺失列「需人工复核」
  5) question_id → evidence_ref 映射存在、逐问题有引用、引用指认真实来源ID
非零退出码 = 发现缺项。本脚本只做结构启发式检查，不替代语义审查；无法判语义时输出「需人工复核」，不单独放行。
"""

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = ["来源与证据", "待核验清单"]

# §10 逐来源必填字段（source-schema §二）。「材料状态」可经「来源状态统一说明」统一标注，故单独豁免。
PER_SOURCE_REQUIRED = ["来源ID", "来源类型", "定位", "获取时间", "版本", "权限", "访问状态", "材料状态", "证据等级"]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file")
    args = ap.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    problems = []

    for sec in REQUIRED_SECTIONS:
        if sec not in text:
            problems.append(f"[缺区块] 未找到「{sec}」")
    # 命名统一：兼容「调查概括」/「证据概括」别名（§10）
    if "调查概括" not in text and "证据概括" not in text:
        problems.append("[缺区块] 未找到「调查概括」/「证据概括」（可互为别名）")

    # 来源区块内是否标记了材料状态。
    # 允许「来源状态统一说明」统一标注，不做逐来源强检；该统一说明区块不计入来源列表。
    src_blocks = re.split(r"^###\s+来源", text, flags=re.M)
    evidence_blocks = [b for b in src_blocks[1:] if b.strip() and not b.lstrip().startswith("状态统一")]
    if not evidence_blocks:
        problems.append("[来源] 未发现「### 来源」区块")
    else:
        # E5 兼容：可由「来源状态统一说明」统一标注材料状态；其余字段逐来源必填。
        state_note = "来源状态统一说明" in text or "材料状态" in text
        for b in evidence_blocks:
            for label in PER_SOURCE_REQUIRED:
                if label == "材料状态" and state_note:
                    continue
                if not re.search(rf"{re.escape(label)}[:：]", b):
                    problems.append(f"[来源·需人工复核] 来源区块缺「{label}」")
                    break
            if not re.search(r"SRC-\d+", b):
                problems.append("[来源·需人工复核] 来源区块缺「来源ID」(SRC-xx)")

    # 待核验清单非空
    if "待核验清单" in text:
        tail = text.split("待核验清单")[-1]
        items = re.findall(r"[-*]\s*", tail)
        if not items:
            problems.append("[待核验] 待核验清单为空")

    check_question_map(text, problems)

    if problems:
        print("校验发现问题:", *problems, sep="\n  ")
        sys.exit(1)
    print("校验通过：来源区块、证据概括、待核验清单齐备。")
    print("注意：脚本不判语义，缺判列已标「需人工复核」；定稿前请进行方法学语义审查与主技能人工复核。")


def check_question_map(text: str, problems: list[str]) -> None:
    """校验 question_id → evidence_ref[] 映射：存在、逐问题有引用、引用指认真实来源ID。"""
    marker = "question_id → evidence_ref"
    if marker not in text:
        problems.append("[映射·需人工复核] 未找到「question_id → evidence_ref」映射")
        return
    block = text.split(marker, 1)[1]
    rows = [ln for ln in block.splitlines() if ln.strip().startswith("|") and "Q-" in ln]
    if not rows:
        problems.append("[映射·需人工复核] 映射为空（无 Q- 行）")
        return
    # 已登记来源ID：仅取映射区块之前的来源登记/来源区块，避免把映射自身误当登记。
    registered = set(re.findall(r"SRC-\d+", text.split("question_id", 1)[0]))
    for row in rows:
        refs = re.findall(r"SRC-\d+", row)
        if not refs:
            problems.append(f"[映射·需人工复核] 问题无证据引用：{row}")
            continue
        for ref in refs:
            if ref not in registered:
                problems.append(f"[映射·需人工复核] 证据引用指向未登记来源：{ref}")


if __name__ == "__main__":
    main()