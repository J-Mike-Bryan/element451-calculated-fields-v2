#!/usr/bin/env python3
"""Expand an Element451 occurrence-candidate template and optionally combine it.

The template may contain:
  {index}          current SPLIT_INDEX occurrence index
  {previous_index} index immediately before the current one
  {ordinal}        zero-based generated candidate number

Example:
  build_occurrence_scan.py candidate.txt --start-index 2 --count 5 --combine MAX

Only the three exact placeholder tokens are replaced, so literal JSON braces may be
used without escaping. This is a text generator; it does not validate object
boundaries or prove that an occurrence marker is correct for a tenant's root field.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from format_formula import pretty_formula  # noqa: E402


def balanced(function: str, expressions: list[str]) -> str:
    if not expressions:
        raise ValueError("At least one expression is required.")
    current = expressions
    while len(current) > 1:
        next_level: list[str] = []
        for offset in range(0, len(current), 2):
            pair = current[offset : offset + 2]
            if len(pair) == 1:
                next_level.append(pair[0])
            else:
                next_level.append(f"{function}({pair[0]},{pair[1]})")
        current = next_level
    return current[0]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template", help="Text file containing the candidate template")
    parser.add_argument("--start-index", type=int, default=2)
    parser.add_argument("--count", type=int, required=True)
    parser.add_argument(
        "--combine",
        choices=("NONE", "MAX", "MIN", "SUM", "CONCAT"),
        default="NONE",
    )
    parser.add_argument("-o", "--output", help="Write output to this file")
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()

    if args.count < 1:
        parser.error("--count must be at least 1")

    try:
        template = Path(args.template).read_text(encoding="utf-8-sig").strip()
    except (OSError, UnicodeError) as exc:
        print(f"Unable to read template: {exc}", file=sys.stderr)
        return 2

    expressions: list[str] = []
    for ordinal in range(args.count):
        index = args.start_index + ordinal
        expression = template
        expression = expression.replace("{index}", str(index))
        expression = expression.replace("{previous_index}", str(index - 1))
        expression = expression.replace("{ordinal}", str(ordinal))
        expressions.append(expression)

    if args.combine == "NONE":
        result = "\n\n".join(expressions)
    elif args.combine in {"MAX", "MIN"}:
        result = balanced(args.combine, expressions)
    else:
        result = f"{args.combine}({','.join(expressions)})"

    if not args.compact and args.combine != "NONE":
        result = pretty_formula(result, 4)

    if args.output:
        Path(args.output).write_text(result.rstrip() + "\n", encoding="utf-8")
    else:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
