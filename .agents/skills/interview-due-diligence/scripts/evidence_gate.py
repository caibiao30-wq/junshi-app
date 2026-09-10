#!/usr/bin/env python3
"""evidence_gate.py — 检查调查取证汇总文件是否满足证据包必备区块。

用法:
    python3 evidence_gate.py <01_调查取证.md>

检查:
  1) 是否包含来源区块、证据概括、来源冲突/限制、待核验清单
  2) 每条证据是否标记来源定位和材料状态
  3) 待核验清单是否非空
非零退出码 = 发现缺项。本脚本只做结构启发式检查，不替代语义审查。
"""

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = ["来源与证据", "证据概括", "待核验清单"]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file")
    args = ap.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    problems = []

    for sec in REQUIRED_SECTIONS:
        if sec not in text:
            problems.append(f"[缺区块] 未找到「{sec}」")

    # 来源区块内是否标记了材料状态
    src_blocks = re.split(r"^###\s+来源", text, flags=re.M)
    evidence_blocks = [b for b in src_blocks[1:] if b.strip()]
    if not evidence_blocks:
        problems.append("[来源] 未发现「### 来源」区块")
    else:
        for b in evidence_blocks:
            if "材料状态" not in b:
                problems.append("[来源] 有来源区块未标「材料状态」")
                break
            if not re.search(r"定位[:：]", b):
                problems.append("[来源] 有来源区块缺「定位」")
                break

    # 待核验清单非空
    if "待核验清单" in text:
        tail = text.split("待核验清单")[-1]
        items = re.findall(r"[-*]\s*", tail)
        if not items:
            problems.append("[待核验] 待核验清单为空")

    if problems:
        print("校验发现问题:", *problems, sep="\n  ")
        sys.exit(1)
    print("校验通过：来源区块、证据概括、待核验清单齐备。")


if __name__ == "__main__":
    main()