#!/usr/bin/env python3
"""全量健康检查 02_访谈记录.md 的问题单元与版本边界。

用法：
    python3 record_gate.py <02_访谈记录.md>          # 结构/字段/七态检查
    python3 record_gate.py --full <02_访谈记录.md>    # + 章节、版本边界、重复定位、修正链检查

非零退出表示存在确定性问题；高置信结构错误会报错，保真类问题以警告+人工语义核验提示。
"""

import argparse
import re
import sys
from pathlib import Path

STATES = {
    "用户明确判断",
    "确认采纳",
    "专业建议·代拟",
    "已被修正",
    "待确认",
    "待验证",
    "拒绝",
}
ALLOWED_TRANSITIONS = {
    ("专业建议·代拟", "待确认"),
    ("待确认", "确认采纳"),
    ("待确认", "已被修正"),
    ("待确认", "拒绝"),
    ("用户明确判断", "已被修正"),
    ("待验证", "用户明确判断"),
    ("待验证", "确认采纳"),
}
FIELD_RE = re.compile(r"^\*\*(问题|回应|长篇回应|确认状态|原始定位|记录授权)\*\*\s*[：:]\s*(.*)$", re.M)
UNIT_RE = re.compile(r"^###\s+问题\s+[^\n]+\n(.*?)(?=^###\s+问题\s+|\Z)", re.M | re.S)
SECTION_RE = re.compile(r"^##\s+([^\n]+)", re.M)
TRANSITION_RE = re.compile(r"\[([^\]]+)\]\s*(?:→|->|➡)\s*\[([^\]]+)\]")


def _full_health(text: str, units: list[re.Match[str]], problems: list[str], warnings: list[str]) -> None:
    """Run whole-file checks; semantic fidelity remains a human review."""
    sections = SECTION_RE.findall(text)
    if not any("待确认" in section and "待验证" in section for section in sections):
        problems.append("全量检查缺少「待确认与待验证」章节")
    change_match = re.search(r"^##\s+记录变更\s*$([\s\S]*)", text, re.M)
    if not change_match:
        problems.append("全量检查缺少「记录变更」章节")
    elif not re.search(r"版本\s*[：:]\s*(?!$|<)", change_match.group(1), re.M):
        problems.append("全量检查「记录变更」缺少非空版本")

    locations: dict[str, list[int]] = {}
    for index, match in enumerate(units, 1):
        block = match.group(1)
        location = next((value.strip() for name, value in FIELD_RE.findall(block) if name == "原始定位"), "")
        if location:
            locations.setdefault(location, []).append(index)
    for location, indexes in locations.items():
        if len(indexes) > 1:
            problems.append(f"全量检查发现重复原始定位（问题单元 {', '.join(map(str, indexes))}）：{location}")

    if "[已被修正]" in text and not re.search(r"修正链|早期表述|后续修正", text):
        warnings.append("发现[已被修正]但未见修正链说明：需人工核对早期表述、触发依据与后续状态")
    warnings.extend([
        "人工核对：所有长论证的前提、限定、反例、证据等级、修正链和未决项未被压缩或横向扁平化",
        "人工核对：三态回溯（报告→记录→原始底稿）、授权范围与版本边界均可复核",
    ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file")
    parser.add_argument("--full", action="store_true",
                        help="执行全量健康检查：除字段/状态外，还检查章节、版本边界、重复定位与修正链");
    args = parser.parse_args()
    path = Path(args.file)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"读取失败：{exc}", file=sys.stderr)
        return 2

    units = list(UNIT_RE.finditer(text))
    problems = []
    warnings = []
    if not units:
        problems.append("未发现「### 问题 ...」问题单元")

    for index, match in enumerate(units, 1):
        block = match.group(1)
        fields = {name: value.strip() for name, value in FIELD_RE.findall(block)}
        label = f"问题单元 {index}"
        if "问题" not in fields or not fields["问题"]:
            problems.append(f"{label}缺少非空「问题」")
        response = fields.get("回应", fields.get("长篇回应", ""))
        if not response:
            problems.append(f"{label}缺少非空「回应」或「长篇回应」")
        if "确认状态" not in fields or not fields["确认状态"]:
            problems.append(f"{label}缺少非空「确认状态」")
        else:
            statuses = re.findall(r"\[([^\]]+)\]", fields["确认状态"])
            if not statuses or any(status not in STATES for status in statuses):
                problems.append(f"{label}确认状态不属于七态：{fields['确认状态']}")
        if "原始定位" not in fields or not fields["原始定位"]:
            problems.append(f"{label}缺少非空「原始定位」")
        if "记录授权" not in fields or not fields["记录授权"]:
            problems.append(f"{label}缺少非空「记录授权」")
        status_values = re.findall(r"\[([^\]]+)\]", fields.get("确认状态", ""))
        status_set = set(status_values)
        response_text = fields.get("回应", fields.get("长篇回应", ""))
        full_text = match.group(0)
        if "专业建议·代拟" in status_values and not re.search(r"代拟", response_text + full_text):
            problems.append(f"{label}标为「专业建议·代拟」但回应未显式标注代拟")
        if "确认采纳" in status_values and re.search(r"采访者代拟.*不代表用户已确认|尚未获.*确认|待确认", response_text):
            problems.append(f"{label}回应仍显示代拟/待确认，不得标为「确认采纳」")

        # 迁移冲突校验（§11）：只允许沿 §11 迁移边迁移，禁止跳级（如[专业建议·代拟]→[确认采纳]）。
        for a, b in TRANSITION_RE.findall(full_text):
            if a == b:
                continue
            if (a, b) not in ALLOWED_TRANSITIONS:
                problems.append(f"{label}非法状态迁移 [{a}]→[{b}]（不在 §11 允许迁移边内）")
            elif b == "确认采纳" and not re.search(r"定位|确认范围|覆盖", fields.get("原始定位", "") + fields.get("记录授权", "") + full_text):
                problems.append(f"{label}[待确认]→[确认采纳] 迁移缺少可回溯定位/确认范围")

        # 对象定位校验（§11/c）：[确认采纳]/[已被修正]/[拒绝] 须有可回溯定位与对象范围，缺失即阻塞。
        for st in ("确认采纳", "已被修正", "拒绝"):
            if st in status_set and not re.search(
                r"定位|对象|范围|覆盖|段落|问题\s*\d",
                fields.get("原始定位", "") + fields.get("记录授权", ""),
            ):
                problems.append(f"{label}标为「{st}」但原始定位/记录授权缺少可回溯对象范围")

        # 事实冲突先行校验（§11/d）：代拟段存在冲突证据却未显式列出批判卡片冲突证据段时阻塞。
        if "专业建议·代拟" in status_set and re.search(r"不支持|冲突|矛盾|相反|反例", response_text) \
                and not re.search(r"不支持/冲突的证据", full_text):
            problems.append(f"{label}代拟段存在冲突证据但未显式列出「不支持/冲突的证据」")

        # 非法状态冲突阻塞（§10/§11）：同一单元不得同时处于互斥状态。
        status_set = set(status_values)
        conflicts = (
            ("用户明确判断", "待确认"),
            ("用户明确判断", "待验证"),
            ("确认采纳", "待确认"),
            ("确认采纳", "待验证"),
            ("用户明确判断", "专业建议·代拟"),
            ("专业建议·代拟", "确认采纳"),
        )
        for a, b in conflicts:
            if a in status_set and b in status_set:
                problems.append(
                    f"{label}存在非法状态冲突 [{a}][{b}]（同一单元不能同时处于互斥状态）"
                )

    if args.full:
        _full_health(text, units, problems, warnings)

    if problems:
        print("校验失败：")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    if warnings:
        for warning in warnings:
            print(f"警告：{warning}")
    print(f"校验通过：发现 {len(units)} 个问题单元，字段与确认状态合法。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
