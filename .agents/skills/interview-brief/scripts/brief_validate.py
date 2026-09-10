#!/usr/bin/env python3
"""brief_validate.py — 校验访谈约定文件(00_访谈约定.md)是否具备完整门控。

用法:
    python3 brief_validate.py <00_访谈约定.md>

检查:
  1) 六个对齐维度的必填小节都存在
  2) 门控勾选项全部勾选( [x] )或全部未决被显式列出
非零退出码 = 发现缺项。
"""

import argparse
import re
import sys
from pathlib import Path

# 每个对齐维度需要的标题关键词（顺序无关，至少匹配一个）
REQUIRED = {
    "对象与权限": ["访谈对象", "受访者", "采访者", "权限"],
    "目标与产出": ["目标", "产出", "读者", "用途"],
    "方法与阶段": ["方法", "阶段", "追问", "收敛"],
    "范围内外": ["范围", "不谈", "不讨论"],
    "记录与保密": ["记录", "保密", "不记录"],
    "代拟授权": ["代拟", "授权"],
}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file", help="00_访谈约定.md 路径")
    args = ap.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    problems = []

    # 1) 必填维度检查（按标题行近似）
    for dim, keys in REQUIRED.items():
        if not any(k in text for k in keys):
            problems.append(f"[缺维度] 未找到与「{dim}」相关的内容")

    # 2) 门控检查
    gates = re.findall(r"\[([ xX])\]\s*(.+)", text)
    checked = [g for g in gates if g[0].lower() == "x"]
    unchecked = [g for g in gates if g[0].lower() != "x"]
    if not gates:
        problems.append("[门控] 未发现任何门控勾选项")
    elif unchecked:
        problems.append(f"[未决] 仍有 {len(unchecked)} 项未确认: "
                        + "; ".join(g[1][:20] for g in unchecked))

    # 3) 明确不谈边界
    if not any(k in text for k in ("不谈", "不讨论", "不进入")):
        problems.append("[边界] 未写明「明确不谈什么」")

    if problems:
        print("校验发现问题:", *problems, sep="\n  ")
        sys.exit(1)
    print(f"校验通过：{len(checked)} 项门控已确认，六维度齐备。")


if __name__ == "__main__":
    main()