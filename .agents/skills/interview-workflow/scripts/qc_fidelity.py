#!/usr/bin/env python3
"""qc_fidelity.py — 质检：核对访谈加工未压缩长答案、状态未升级、可回溯。

用法:
    python3 qc_fidelity.py <02_访谈记录.md> <03_访谈报告.md>

检查:
  1) 保真: 报告对记录中每段"长答案"保留足够比例（默认 >=60%，低于报错）
  2) 状态: 报告未把待确认/待验证整体抹除（提示人工核对是否被升级）
  3) 回溯: 记录中的"原始定位"行非空
非零退出码 = 发现问题。

说明: 本脚本与 interview-qc 的 qc_run 在保真/状态/回溯上逻辑相近（有意镜像），
但分属 interview-workflow / interview-qc 两个独立职责域、各自独立调用。
为不破坏各自职责与调用契约，保持独立实现、不做跨目录 import 合并（ponytail: 见 §10）。
"""

import argparse
import difflib
import re
import sys
from pathlib import Path

MIN_KEEP = 0.6  # 每段长答案至少保留比例；低于视为疑似压缩


def _long_answers(record: str) -> list[str]:
    """抽出记录中独立成段的、长度>=80 字的正文段落（跳过标题/引用/清单）。"""
    paras = [p.strip() for p in re.split(r"\n{2,}", record)]
    return [p for p in paras if len(p) >= 80 and not p.startswith(("#", ">", "-", "*"))]


def _normalize(s: str) -> str:
    return re.sub(r"[^\w一-鿿]", "", s)


def _keep_ratio(para_norm: str, report_norm: str) -> float:
    sm = difflib.SequenceMatcher(None, para_norm, report_norm)
    matched = sum(b.size for b in sm.get_matching_blocks())
    return matched / max(len(para_norm), 1)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("record")
    ap.add_argument("report")
    args = ap.parse_args()

    record = Path(args.record).read_text(encoding="utf-8")
    report = Path(args.report).read_text(encoding="utf-8")
    report_norm = _normalize(report)

    problems = []
    for p in _long_answers(record):
        r = _keep_ratio(_normalize(p), report_norm)
        if r < MIN_KEEP:
            problems.append(f"[压缩] 保留率 {r:.0%} < {MIN_KEEP:.0%}: {p[:36]}…")

    # 状态升级启发式：报告完全没有 [待确认]/[待验证] 状态标记时提示人工核对。
    # 仅见“待确认/待验证”字样而无状态标记（无关文字）同样不认可（§10）。
    if "[待确认]" not in report and "[待验证]" not in report:
        problems.append("[状态] 报告未见 [待确认]/[待验证] 状态标记——请人工核对是否被升级，或仅有无关待确认/待验证文字")

    # 回溯检查：记录中"原始定位"行非空非占位。
    for ln in record.splitlines():
        if ln.strip().startswith("原始定位") and len(ln.strip()) <= len("原始定位："):
            problems.append(f"[回溯] 空的原始定位行: {ln.strip()}")

    if problems:
        print("QC 发现问题:", *problems, sep="\n  ")
        sys.exit(1)
    print("QC 通过：长答案保留率达标、状态未抹除、原始定位齐全。")


if __name__ == "__main__":
    main()