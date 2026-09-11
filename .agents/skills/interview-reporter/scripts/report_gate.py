#!/usr/bin/env python3
"""Deterministic structural gate for interview reports."""
import argparse
import re
import sys
from pathlib import Path

# 区块关键词：允许任意标题层级（#~####），目录允许“总目录/目录”。
KEYWORDS = ("阅读说明", "结论边界", "待确认清单", "待验证清单", "回溯索引")
BAD = ("报告自身为证据", "以本报告为证据", "报告证明报告")

def fail(msg):
    print(f"FAIL: {msg}")
    return 1

def has_heading(text: str, keyword: str) -> bool:
    return re.search(r"^#{1,4}\s*[^\n]*" + re.escape(keyword), text, re.M) is not None

def problem_ids(text: str) -> set:
    """抽取正文中的问题节点 ID（形如 N-M），兼容“问题 2-1”“问题-2-1”两种写法。"""
    return set(re.findall(r"问题[-\s](\d+-\d+)", text))

def cross_check(report_text: str, record_text: str):
    """报告问题 ID ↔ 记录问题节点交叉校验（负例 7）。

    返回 (ok, msg, manual)：ok 为 False 即阻塞；manual 为 True 表示无法判定，需人工复核而非放行。
    """
    rep_ids = problem_ids(report_text)
    rec_ids = problem_ids(record_text)
    if not rep_ids or not rec_ids:
        return False, "报告与记录无法解析出任何问题 ID——交叉校验无法判定", True
    missing = sorted(rep_ids - rec_ids)
    if missing:
        return False, f"报告引用了记录中不存在的问题节点：{', '.join(missing)}", False
    return True, "", False

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("record", nargs="?")
    a=ap.parse_args()
    report=Path(a.report)
    if not report.is_file(): return fail("报告文件不存在")
    text=report.read_text(encoding="utf-8")
    if not re.search(r"^#{1,4}\s*[^\n]*(总)?目录", text, re.M):
        return fail("缺少结构：目录/总目录")
    for key in KEYWORDS:
        if not has_heading(text, key): return fail(f"缺少结构：{key}")
    if not re.search(r"证据源：[^\n]*02_访谈记录", text): return fail("未明确标明证据源为 02_访谈记录")
    if not re.search(r"^#{2,4}\s*[^\n]*问题\s*\d", text, re.M): return fail("缺少问题节")
    if not re.search(r"确认状态\*{0,2}[：:]\s*[^\n]*(?:\[用户明确判断\]|\[确认采纳\]|\[专业建议·代拟\]|\[已被修正\]|\[拒绝\]|\[待确认\]|\[待验证\])", text): return fail("问题节缺少确认状态")
    if not re.search(r"记录定位[：:]\s*`?[^\n]*02_访谈记录", text): return fail("问题单元缺少有效记录定位")
    if not re.search(r"\|\s*报告位置\s*\|\s*记录位置\s*\|\s*原始底稿位置\s*\|", text): return fail("回溯索引表头不完整")
    if re.search(r"\|[^|]+\|\s*(?:待补|暂无|空|无)\s*\|", text): return fail("回溯索引存在空定位")
    if any(x in text for x in BAD): return fail("出现明显报告自证表述")
    if not (re.search(r"\[待确认\]", text) or re.search(r"待确认[^\n]*(?:清单|列表)", text)):
        return fail("未保留待确认清单标识（需 [待确认] 标记或待确认清单结构）")
    if not (re.search(r"\[待验证\]", text) or re.search(r"待验证[^\n]*(?:清单|列表)", text)):
        return fail("未保留待验证清单标识（需 [待验证] 标记或待验证清单结构）")
    if a.record:
        record=Path(a.record)
        if not record.is_file(): return fail("指定记录文件不存在")
        if not re.search(r"02_访谈记录", text): return fail("报告未引用记录")
        ok, msg, manual = cross_check(text, record.read_text(encoding="utf-8"))
        if not ok:
            if manual:
                print(f"NEED-MANUAL-REVIEW: {msg}")
                return 1
            return fail(msg)
    print("PASS: report structure, evidence source, status, and traceability gates passed")
    return 0

if __name__ == "__main__": sys.exit(main())
