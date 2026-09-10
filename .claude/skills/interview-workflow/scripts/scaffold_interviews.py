#!/usr/bin/env python3
"""scaffold_interviews.py — 为一次访谈创建标准目录与四个产物脚手架。

用法:
    python3 scaffold_interviews.py <本次访谈名> [目标根目录]

缺省根目录: 当前目录下的 `访谈资料`（有则复用，无则创建）。
产物按 interview-workflow 契约从 assets/templates 复制:
    00_访谈约定.md 01_调查取证.md 02_访谈记录.md 03_访谈报告.md
"""

import argparse
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "assets" / "templates"
ARTIFACTS = ["00_访谈约定.md", "01_调查取证.md", "02_访谈记录.md", "03_访谈报告.md"]
FALLBACK = "（创建于 scaffold，模板缺失，由 interview-workflow 填充）\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("name", help="本次访谈名（用作目录名）")
    ap.add_argument("root", nargs="?", default=None, help="访谈资料根目录（缺省取 cwd/访谈资料）")
    args = ap.parse_args()

    root = Path(args.root) if args.root else Path.cwd() / "访谈资料"
    root.mkdir(exist_ok=True)

    project = root / args.name
    if project.exists():
        print(f"已存在，复用目录: {project}")
    else:
        project.mkdir()

    created, reused = [], []
    for a in ARTIFACTS:
        f = project / a
        if f.exists():
            reused.append(a)
            continue
        tpl = TEMPLATE_DIR / a
        f.write_text(tpl.read_text(encoding="utf-8") if tpl.exists() else f"# {a}\n\n{FALLBACK}",
                     encoding="utf-8")
        created.append(a)

    if created:
        print("新建:", ", ".join(created))
    if reused:
        print("复用:", ", ".join(reused))
    print("产物目录:", project)


if __name__ == "__main__":
    main()