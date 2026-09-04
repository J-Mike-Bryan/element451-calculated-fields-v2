#!/usr/bin/env python3
"""Build a balanced nested MAX or MIN expression from candidate expressions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_expressions(path: str | None, positional: list[str]) -> list[str]:
    expressions = [item.strip() for item in positional if item.strip()]
    if path is None:
        return expressions

    raw = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8-sig")
    stripped = raw.strip()
    if not stripped:
        return expressions

    if stripped.startswith("["):
        parsed = json.loads(stripped)
        if not isinstance(parsed, list) or not all(isinstance(item, str) for item in parsed):
            raise ValueError("JSON input must be an array of strings")
        expressions.extend(item.strip() for item in parsed if item.strip())
    else:
        expressions.extend(
            line.strip()
            for line in raw.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )
    return expressions


def build_tree(expressions: list[str], function_name: str) -> str:
    if not expressions:
        raise ValueError("provide at least one candidate expression")
    current = expressions[:]
    while len(current) > 1:
        next_level: list[str] = []
        for index in range(0, len(current), 2):
            if index + 1 >= len(current):
                next_level.append(current[index])
            else:
                next_level.append(
                    f"{function_name}({current[index]}, {current[index + 1]})"
                )
        current = next_level
    return current[0]


def pretty(expression: str, indent_width: int = 4) -> str:
    out: list[str] = []
    indent = 0
    token = ""
    in_string = False
    i = 0

    def flush_token() -> None:
        nonlocal token
        if token.strip():
            out.append(" " * (indent * indent_width) + token.strip())
        token = ""

    while i < len(expression):
        ch = expression[i]
        if in_string:
            token += ch
            if ch == '"':
                if i + 1 < len(expression) and expression[i + 1] == '"':
                    token += expression[i + 1]
                    i += 2
                    continue
                in_string = False
            i += 1
            continue

        if ch == '"':
            token += ch
            in_string = True
        elif ch == "(":
            token += ch
            flush_token()
            indent += 1
        elif ch == ",":
            token += ch
            flush_token()
        elif ch == ")":
            flush_token()
            indent = max(0, indent - 1)
            token += ch
        else:
            token += ch
        i += 1

    flush_token()
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expressions", nargs="*", help="Candidate expressions")
    parser.add_argument("--file", help="Text file, JSON array file, or - for stdin")
    parser.add_argument(
        "--function",
        choices=("MAX", "MIN"),
        default="MAX",
        help="Binary function to nest",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print the result")
    args = parser.parse_args()

    try:
        expressions = load_expressions(args.file, args.expressions)
        result = build_tree(expressions, args.function)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"Unable to build expression: {exc}", file=sys.stderr)
        return 2

    print(pretty(result) if args.pretty else result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
