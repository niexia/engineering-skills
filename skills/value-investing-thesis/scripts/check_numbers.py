#!/usr/bin/env python3
"""Verify the arithmetic behind an investment thesis.

Usage:
    python check_numbers.py checks.json
    python check_numbers.py checks.json --json

Each check supplies the value used in the analysis (`left`) and the value
recomputed from its formula (`right`). The script does not choose formulas; it
verifies that both sides agree within tolerance and makes the gate explicit.

Exit codes:
    0  PASS
    1  FAIL (a check failed, is missing, or is invalid)
    2  VACUOUS (no checks, all skipped, or invalid input)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def as_number(value: Any) -> float | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        stripped = value.strip().replace(",", "")
        if stripped.endswith("%"):
            stripped = stripped[:-1]
            try:
                return float(stripped) / 100.0
            except ValueError:
                return None
        try:
            return float(stripped)
        except ValueError:
            return None
    return None


def format_number(value: float | None) -> str:
    if value is None:
        return "n/a"
    if abs(value) >= 1000:
        return f"{value:,.2f}"
    if abs(value) >= 1:
        return f"{value:,.3f}"
    return f"{value:.6f}"


def check_one(raw: dict[str, Any], index: int) -> dict[str, Any]:
    name = str(raw.get("name") or f"check {index + 1}")
    left = as_number(raw.get("left"))
    right = as_number(raw.get("right"))
    required = bool(raw.get("required", True))
    mode = str(raw.get("mode", "relative")).lower()
    operator = str(raw.get("operator", "eq")).lower()
    base = {
        "name": name,
        "left": left,
        "right": right,
        "unit": raw.get("unit", ""),
        "note": raw.get("note", ""),
    }
    if mode not in ("relative", "absolute"):
        return {**base, "status": "INVALID", "detail": f"mode must be relative or absolute, got {mode!r}"}
    if operator not in ("eq", "gt", "gte", "lt", "lte"):
        return {**base, "status": "INVALID", "detail": f"operator must be eq, gt, gte, lt or lte, got {operator!r}"}

    tolerance_raw = raw.get("tolerance", 0.01)
    tolerance = as_number(tolerance_raw)
    if tolerance is None or tolerance < 0:
        return {**base, "status": "INVALID", "detail": f"tolerance must be a non-negative number, got {tolerance_raw!r}"}

    if left is None or right is None:
        status = "SKIP" if not required else "MISSING"
        detail = "left or right is missing"
        if not required:
            detail += " (optional check)"
        return {**base, "status": status, "detail": detail}

    if operator != "eq":
        symbols = {"gt": ">", "gte": ">=", "lt": "<", "lte": "<="}
        comparisons = {
            "gt": left > right,
            "gte": left >= right,
            "lt": left < right,
            "lte": left <= right,
        }
        status = "PASS" if comparisons[operator] else "FAIL"
        return {
            **base,
            "status": status,
            "detail": f"{format_number(left)} {symbols[operator]} {format_number(right)}",
            "mode": operator,
        }

    delta = abs(left - right)
    if mode == "relative":
        denominator = max(abs(left), abs(right), 1e-12)
        diff = delta / denominator
        diff_display = f"{diff:.4%}"
        tolerance_display = f"{tolerance:.2%}"
    else:
        diff = delta
        diff_display = format_number(diff)
        tolerance_display = format_number(tolerance)

    status = "PASS" if diff <= tolerance + 1e-12 else "FAIL"
    return {
        **base,
        "status": status,
        "detail": f"diff {diff_display} vs tolerance {tolerance_display} ({mode})",
        "diff": diff,
        "tolerance": tolerance,
        "mode": mode,
    }


def render_table(result: dict[str, Any]) -> str:
    lines = [
        f"Accuracy checks: {result['company']} (as of {result['as_of']})",
        "",
        "| Check | Used | Recomputed | Status | Detail |",
        "|---|---:|---:|---|---|",
    ]
    for check in result["checks"]:
        unit = f" {check['unit']}" if check.get("unit") else ""
        lines.append(
            "| {name} | {left}{unit} | {right}{unit} | {status} | {detail} |".format(
                name=check["name"],
                left=format_number(check.get("left")),
                right=format_number(check.get("right")),
                unit=unit,
                status=check["status"],
                detail=check.get("detail", ""),
            )
        )
    notes = [(check["name"], check["note"]) for check in result["checks"] if check.get("note")]
    if notes:
        lines.extend(["", "Notes:"])
        for name, note in notes:
            lines.append(f"- {name}: {note}")
    lines.extend(
        [
            "",
            f"Summary: {result['passed']} passed, {result['failed']} failed, "
            f"{result['skipped']} skipped, {result['missing']} missing.",
            f"Accuracy gate: {result['gate']}",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify investment-thesis arithmetic.")
    parser.add_argument("input", type=Path, help="Path to checks.json")
    parser.add_argument("--json", action="store_true", help="Print a JSON report")
    args = parser.parse_args()

    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"input not found: {args.input}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")

    if not isinstance(payload, dict):
        fail("input must be a JSON object")

    company = str(payload.get("company") or "Unknown company")
    as_of = str(payload.get("as_of") or "unknown date")
    raw_checks = payload.get("checks")
    if not isinstance(raw_checks, list) or not raw_checks:
        result = {
            "company": company,
            "as_of": as_of,
            "gate": "VACUOUS",
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "missing": 0,
            "checks": [],
        }
        print(render_table(result))
        raise SystemExit(2)

    checks = [check_one(raw, index) for index, raw in enumerate(raw_checks) if isinstance(raw, dict)]
    if len(checks) != len(raw_checks):
        fail("every check must be a JSON object")

    passed = sum(1 for check in checks if check["status"] == "PASS")
    failed = sum(1 for check in checks if check["status"] in ("FAIL", "INVALID"))
    skipped = sum(1 for check in checks if check["status"] == "SKIP")
    missing = sum(1 for check in checks if check["status"] == "MISSING")

    if failed or missing:
        gate = "FAIL"
    elif passed == 0:
        gate = "VACUOUS"
    else:
        gate = "PASS"

    result = {
        "company": company,
        "as_of": as_of,
        "gate": gate,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "missing": missing,
        "checks": checks,
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render_table(result))

    if gate == "PASS":
        raise SystemExit(0)
    if gate == "FAIL":
        raise SystemExit(1)
    raise SystemExit(2)


if __name__ == "__main__":
    main()
