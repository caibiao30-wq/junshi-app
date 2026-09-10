#!/usr/bin/env python3
"""qc_run.py — 访谈质检综合校验脚本（确定性、启发式）。

服务 interview-workflow 的 Phase 4 定稿前后质检与集成岗位：
核对 00_访谈约定 / 01_调查取证 / 02_访谈记录 / 03_访谈报告 之间的
结构、证据源、状态与可回溯关系；只输出分级结论与修复建议，
不修改任何产物、不替用户改变产品判断。

用法:
    python3 qc_run.py <访谈目录>         # 目录内须含 00/01/02/03
    python3 qc_run.py <02记录.md> <03报告.md>

检查层级（每一项标记严重度）:
  - 结构: 关键文件存在
  - 证据: 03 的证据源是否为 02（拒绝自证）
  - 状态: 待确认/待验证是否被明显升级或抹除
  - 保真: 长答案保留率（启发式，不能替代语义审查）
  - 长论证: 前提/条件/限定/反例/证据等级/修正链/未决项的缺失信号（仅提示，语义核对交人工）
  - 定位: 记录的原始定位非空；报告可回溯到记录
  - 权限/集成: 报告是否含待确认/待验证清单；集成前后一致性提示

严重度与退出码:
  [阻塞]  结构缺失、证据源断裂 —— 定稿必须停止。发现任一阻塞 → 退出码 1。
  [严重]  状态升级、定位缺失 —— 需修复后再定稿。
  [一般]  弱信号、建议 —— 供参考。
  [需人工复核] 超出脚本能力、需主技能/用户语义判定。

注意: 本脚本只能做确定性启发式检查，不能替代主技能的人工语义核验。
"""

import argparse
import difflib
import re
import sys
from pathlib import Path

MIN_KEEP = 0.6  # 每段长答案至少保留比例，低于视为疑似压缩
# 主方法学保真零件关键词（信号级，缺失仅提示，不冒充语义通过）
FIDELITY_TERMS = [
    "前提", "条件", "限定", "反例", "例外", "证据", "修正",
    "未决", "待验证", "待确认", "边界", "局限",
]
DRAFT_TERMS = ["代拟", "专业建议", "草稿"]
STATES = [
    "[用户明确判断]",
    "[确认采纳]",
    "[专业建议·代拟]",
    "[已被修正]",
    "[待确认]",
    "[待验证]",
]
ARTIFACTS = ["00_访谈约定.md", "01_调查取证.md", "02_访谈记录.md", "03_访谈报告.md"]


class Finding:
    """单条质检发现：严重度 + 层级 + 定位 + 说明。"""

    def __init__(self, sev: str, level: str, loc: str, msg: str):
        self.sev = sev      # 阻塞 / 严重 / 一般 / 需人工复核
        self.level = level  # 结构 / 证据 / 状态 / 保真 / 定位 / 权限
        self.loc = loc
        self.msg = msg


def _normalize(s: str) -> str:
    return re.sub(r"[^\w一-鿿]", "", s)


def _long_answers(text: str) -> list[str]:
    """抽出独立成段、长度>=80 字的正文段落（跳过标题/引用/清单）。"""
    paras = [p.strip() for p in re.split(r"\n{2,}", text)]
    return [p for p in paras if len(p) >= 80 and not p.startswith(("#", ">", "-", "*"))]


def _count(text: str, marker: str) -> int:
    return text.count(marker)


def check_structure(artifacts: dict) -> list[Finding]:
    """结构：关键文件是否存在。"""
    out = []
    for key in ARTIFACTS:
        p = artifacts[key]
        if p is None:
            continue  # 两文件模式只提供 02/03，不扩大校验范围
        if not p.exists():
            out.append(Finding("阻塞", "结构", str(p), f"关键文件不存在: {key}"))
    return out


def check_evidence(report_text: str, record_file: str) -> list[Finding]:
    """证据：03 的证据源是否为 02（拒绝自证）。"""
    out = []
    # 报告必须引用记录文件（含 02_访谈记录 或 02 文件名）
    has_src = "02_访谈记录" in report_text or ("02" in report_text and "访谈记录" in report_text)
    if not has_src:
        out.append(Finding("阻塞", "证据", record_file, "报告未声明证据源为 02_访谈记录.md（拒绝自证：报告不能以自身为证据源）"))
    return out


def check_formal_structure(report_text: str) -> list[Finding]:
    """结构：核对正式报告的总目录、结论总览、章/节和文末区块。"""
    out = []
    if not re.search(r"^#{1,4}\s*[^\n]*(总)?目录", report_text, re.M):
        out.append(Finding("阻塞", "结构", "03_访谈报告.md", "正式报告缺少总目录"))
    if not re.search(r"^#{1,4}\s*[^\n]*结论总览", report_text, re.M):
        out.append(Finding("严重", "结构", "03_访谈报告.md", "正式报告缺少正文前的结论总览"))
    if not re.search(r"^#\s*第一章[^\n]*阶段\s*0", report_text, re.M):
        out.append(Finding("严重", "结构", "03_访谈报告.md", "缺少第一章与阶段0的映射声明"))
    if not re.search(r"^#{2,4}\s*[^\n]*问题\s*\d+-\d+", report_text, re.M):
        out.append(Finding("阻塞", "结构", "03_访谈报告.md", "缺少‘节=问题’格式的问题节"))
    if not re.search(r"^#{1,4}\s*[^\n]*结论边界", report_text, re.M):
        out.append(Finding("严重", "结构", "03_访谈报告.md", "缺少文末结论边界"))
    return out


def check_state(record_text: str, report_text: str) -> list[Finding]:
    """状态：待确认/待验证是否被明显升级或抹除。"""
    out = []
    rec_pending = _count(record_text, "[待确认]") + _count(record_text, "[待验证]")
    rep_pending = _count(report_text, "待确认") + _count(report_text, "待验证")
    if rep_pending == 0:
        out.append(Finding("阻塞", "状态", "03_访谈报告.md", "报告完全未见待确认/待验证标记——请人工核对是否被升级（记录中有保留项时尤其可疑）"))
    return out


def check_fidelity(record_text: str, report_text: str) -> list[Finding]:
    """保真：长答案保留率（启发式，不能替代语义审查）。"""
    out = []
    report_norm = _normalize(report_text)
    for p in _long_answers(record_text):
        pn = _normalize(p)
        sm = difflib.SequenceMatcher(None, pn, report_norm)
        matched = sum(b.size for b in sm.get_matching_blocks())
        ratio = matched / max(len(pn), 1)
        # 大批原文块没进报告 → 疑似压缩
        if ratio < MIN_KEEP and len(pn) >= 200:
            out.append(Finding("阻塞", "保真", "02_访谈记录.md→03", f"疑似压缩长答案，保留率 {ratio:.0%} < {MIN_KEEP:.0%}：{p[:36]}…"))
        elif ratio < MIN_KEEP:
            out.append(Finding("严重", "保真", "02_访谈记录.md→03", f"疑似压缩长答案，保留率 {ratio:.0%} < {MIN_KEEP:.0%}：{p[:36]}…"))
    # 原文块在报告中被"重组"（顺序改变）超出脚本能力 → 需人工复核
    if report_text and _long_answers(report_text):
        out.append(Finding("需人工复核", "保真", "03_访谈报告.md", "报告存在长段落——请主技能核对长答案是否逐层保留、未静默截断（脚本只做启发式）"))
    return out


def check_long_argument(record_text: str, report_text: str) -> list[Finding]:
    """长论证：缺失保真零件信号、摘要冒充、代拟隔离（信号级，交人工核对）。"""
    out = []
    rn = _normalize(report_text)
    missing = [t for t in FIDELITY_TERMS if t not in rn and t not in _normalize(record_text)]
    if missing:
        out.append(Finding("需人工复核", "长论证", "02_访谈记录.md→03",
                           f"长论证常用保真零件词在记录/报告中均未见：{'、'.join(missing)}。请核对前提/条件/限定/反例/证据等级/修正链/未决项是否被删或以摘要替代（信号，非结论）"))
    if "代拟" in report_text and "[专业建议·代拟]" not in report_text:
        # 代拟词出现却无标准状态标记——仅信号，需人工看是否与用户判断分隔
        out.append(Finding("需人工复核", "权限", "03_访谈报告.md",
                           "报告含‘代拟’相关词但未见标准 `[专业建议·代拟]` 标记，请核对代拟是否在视觉/语义上与用户原话/判断清楚分隔、未被冒充（信号，非结论）"))
    if "摘要" in rn:
        out.append(Finding("需人工复核", "长论证", "03_访谈报告.md",
                           "报告出现‘摘要’字样，请核对摘要仅作导航、未冒充完整长论证（信号，非结论）"))
    return out


def check_location(record_text: str) -> list[Finding]:
    """定位：记录的原始定位非空非占位；报告保留定位。"""
    out = []
    empty = []
    marker_count = 0
    for ln in record_text.splitlines():
        # 兼容 *原始定位* / **原始定位** / 原始定位：等写法
        if "原始定位" not in ln:
            continue
        marker_count += 1
        val = ln.split("：", 1)[1] if "：" in ln else (ln.split(":", 1)[1] if ":" in ln else "")
        if not val.strip() or val.strip() in ("TODO", "待补", "占位"):
            empty.append(ln.strip())
    if marker_count == 0:
        out.append(Finding("严重", "定位", "02_访谈记录.md", "记录未见任何‘原始定位’行——三态可回溯闭环断裂"))
    if empty:
        out.append(Finding("阻塞", "定位", "02_访谈记录.md", f"存在 {len(empty)} 个空的原始定位行，无法回到底稿：{empty[:3]}"))
    return out


def check_permission(report_text: str) -> list[Finding]:
    """权限/集成：报告是否含待确认/待验证清单（纪律六：保留待确认，不静默补齐）。"""
    out = []
    has_list = ("待确认" in report_text and ("清单" in report_text or "列表" in report_text or "待验证" in report_text))
    if not has_list:
        out.append(Finding("严重", "权限", "03_访谈报告.md", "报告未单列待确认/待验证清单——待确认项不可被阶段摘要遮蔽"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", nargs="+", help="访谈目录，或 <02记录.md> <03报告.md>")
    args = ap.parse_args()

    target = [Path(t) for t in args.target]

    # 输入归一：目录，或两个文件路径
    artifacts: dict = {k: None for k in ARTIFACTS}
    if len(target) == 1 and target[0].is_dir():
        d = target[0]
        for k in ARTIFACTS:
            artifacts[k] = d / k
    elif len(target) == 2:
        rec, rep = target
        artifacts["02_访谈记录.md"] = rec
        artifacts["03_访谈报告.md"] = rep
        # 00/01 保持 None：两文件模式下不校验约定/取证存在性
    else:
        ap.error("需传入一个访谈目录，或 <02记录.md> <03报告.md> 两个路径")

    findings: list[Finding] = []
    findings += check_structure(artifacts)

    rec = artifacts["02_访谈记录.md"]
    rep = artifacts["03_访谈报告.md"]
    if rec and rec.exists():
        rec_text = rec.read_text(encoding="utf-8")
    else:
        rec_text = ""
    if rep and rep.exists():
        rep_text = rep.read_text(encoding="utf-8")
    else:
        rep_text = ""

    # 仅当 02/03 至少其一可读时做内容级检查，避免对空文件堆砌误报
    if rec_text or rep_text:
        findings += check_formal_structure(rep_text)
        findings += check_evidence(rep_text, str(rec) if rec else "?")
        findings += check_state(rec_text, rep_text)
        findings += check_fidelity(rec_text, rep_text)
        findings += check_long_argument(rec_text, rep_text)
        findings += check_location(rec_text)
        findings += check_permission(rep_text)

    # 汇总与排序（阻塞 > 严重 > 一般 > 需人工复核）
    order = {"阻塞": 0, "严重": 1, "一般": 2, "需人工复核": 3}
    findings.sort(key=lambda f: order.get(f.sev, 9))

    n_block = sum(1 for f in findings if f.sev == "阻塞")
    n_sev = sum(1 for f in findings if f.sev == "严重")
    print("=" * 60)
    print(f"interview-qc 质检结果：共 {len(findings)} 项  |  阻塞 {n_block} / 严重 {n_sev}")
    print("=" * 60)
    for i, f in enumerate(findings, 1):
        print(f"[{f.sev} · {f.level}] {f.loc}\n     {f.msg}")
    print("=" * 60)

    if n_block > 0:
        print("结论：存在阻塞项 —— 定稿暂停。请按定位修复后再验。")
        return 1
    if n_sev > 0:
        print("结论：存在严重项 —— 建议修复后再定稿；需人工复核项请主技能确认。")
        return 0
    print("结论：通过（无阻塞/严重/一般项）；需人工复核项请主技能做最终语义核验。")
    return 0


if __name__ == "__main__":
    sys.exit(main())