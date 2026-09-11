#!/usr/bin/env python3
"""frontier_gate.py — 决策树/前沿状态契约校验。

用法:
    python3 frontier_gate.py <nodes.json>

输入: 一个 JSON，含 "nodes"（节点数组）与可选 "current_scope"（当前范围版本的整数）。
节点必含字段见 references/decision-tree-contract.md：
    node_id, status, depends_on(list), scope_version(int),
    completion_evidence(str), source_location(str)

检查（对应决策树契约与升级报告 §18 负例）:
  1) 依赖闭合: 命中 -> 依赖未满足即提出下游问题
     进入 ready/active 的节点，depends_on 必须全部为 done。
  2) 范围一致: 命中 -> 用户改目标后继续用旧 frontier
     ready/active/done 节点必须与 current_scope 一致；旧版本节点须为 stale/superseded。
  3) 引用闭合: 命中 -> depends_on 引用了不存在的节点
  4) 证据完整: 命中 -> 空定位/空状态/占位符被视为合格证据
     done 节点必须有非空 completion_evidence 与 source_location，且不等于占位符。
非零退出码 = 发现问题；任一问题都列在报告中，不静默跳过。
"""

import json
import sys
from pathlib import Path

PLACEHOLDERS = {"", "None", "null", "TBD", "待填", "占位", "TODO"}


def _evidenced(v: str) -> bool:
    return (v or "").strip() not in PLACEHOLDERS


def check_nodes(nodes: list[dict], current_scope: int | None = None) -> list[str]:
    problems: list[str] = []
    by_id = {n.get("node_id"): n for n in nodes}

    for n in nodes:
        nid = n.get("node_id")
        status = n.get("status")
        deps = n.get("depends_on") or []
        scope = n.get("scope_version")

        # 2) 范围一致：状态推进不落于旧版本（负例 4）。
        if current_scope is not None and status in ("ready", "active", "done"):
            if scope != current_scope:
                problems.append(
                    f"[范围] {nid} 用旧 scope_version={scope}（当前={current_scope}）仍为 {status}"
                )

        # 1)+3) 依赖闭合与引用闭合（负例 3、7）。
        for dep in deps:
            if dep not in by_id:
                problems.append(f"[引用] {nid} depends_on 引用不存在的节点 {dep}")
                continue
            if status in ("ready", "active") and by_id[dep].get("status") != "done":
                problems.append(f"[依赖] {nid} 依赖 {dep}({by_id[dep].get('status')}) 未完成")

        # 4) 证据完整（负例 9）。
        if status == "done" and not (
            _evidenced(n.get("completion_evidence")) and _evidenced(n.get("source_location"))
        ):
            problems.append(
                f"[证据] {nid} done 但 completion_evidence/source_location 为空或占位"
            )

    # 依赖双向一致：被 supersedes 引用的节点应整体存在（引用闭合）。
    for n in nodes:
        sup = n.get("supersedes")
        if sup and sup not in by_id:
            problems.append(f"[引用] {n.get('node_id')} supersedes 引用不存在的节点 {sup}")

    return problems


def main() -> None:
    if sys.argv[1:]:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    else:
        data = {"nodes": [], "current_scope": 1}

    problems = check_nodes(data.get("nodes", []), data.get("current_scope"))
    if problems:
        print("frontier_gate 发现问题:", *problems, sep="\n  ")
        sys.exit(1)
    print("frontier_gate 通过：依赖闭合、范围一致、引用闭合、证据完整。")


if __name__ == "__main__":
    # 自带最小自检：改动门逻辑后运行本文件即回归（不依赖外部 fixture）。
    _ok = not check_nodes(
        [
            # 范围旧版本仍 ready → 应报
            {"node_id": "n1", "status": "ready", "depends_on": [], "scope_version": 0},
            # 依赖未完成 → 应报
            {"node_id": "n2", "status": "active", "depends_on": ["n3"], "scope_version": 1},
            {"node_id": "n3", "status": "blocked", "depends_on": [], "scope_version": 1},
            # 正常 done → 不报
            {"node_id": "n4", "status": "done", "depends_on": [],
             "scope_version": 1, "completion_evidence": "消息-051", "source_location": "02#消息-051"},
        ],
        current_scope=1,
    )
    assert _ok, "expect: n1(范围) + n2(依赖缺失) 报出，n4 不报"
    print("frontier_gate 自检通过。")