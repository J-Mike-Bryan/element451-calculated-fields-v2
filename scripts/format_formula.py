#!/usr/bin/env python3
"""Format an Element451 calculated-field formula without changing string data."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def load_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8-sig")


def next_nonspace(text: str, start: int) -> tuple[int, str | None]:
    i = start
    while i < len(text) and text[i].isspace():
        i += 1
    return i, text[i] if i < len(text) else None


def compact_formula(text: str) -> str:
    out: list[str] = []
    in_string = False
    pending_space = False
    i = 0
    text = text.lstrip("\ufeff").strip()

    while i < len(text):
        ch = text[i]
        if in_string:
            out.append(ch)
            if ch == '"':
                if i + 1 < len(text) and text[i + 1] == '"':
                    out.append(text[i + 1])
                    i += 2
                    continue
                in_string = False
            i += 1
            continue

        if ch == '"':
            if pending_space and out and out[-1] not in "(, ":
                out.append(" ")
            pending_space = False
            out.append(ch)
            in_string = True
            i += 1
            continue

        if ch.isspace():
            pending_space = True
            i += 1
            continue

        if ch in "(),":
            while out and out[-1] == " ":
                out.pop()
            out.append(ch)
            pending_space = ch == ","
            i += 1
            continue

        if pending_space and out and out[-1] not in "(, ":
            out.append(" ")
        pending_space = False
        out.append(ch)
        i += 1

    return "".join(out).strip()


def pretty_formula(text: str, indent_width: int) -> str:
    text = compact_formula(text)
    lines: list[str] = []
    current: list[str] = []
    indent = 0
    in_string = False
    i = 0

    def flush() -> None:
        nonlocal current
        content = "".join(current).strip()
        if content:
            lines.append(" " * (indent * indent_width) + content)
        current = []

    while i < len(text):
        ch = text[i]
        if in_string:
            current.append(ch)
            if ch == '"':
                if i + 1 < len(text) and text[i + 1] == '"':
                    current.append(text[i + 1])
                    i += 2
                    continue
                in_string = False
            i += 1
            continue

        if ch == '"':
            current.append(ch)
            in_string = True
            i += 1
            continue

        if ch == "(":
            _, upcoming = next_nonspace(text, i + 1)
            current.append(ch)
            if upcoming == ")":
                current.append(")")
                close_index, _ = next_nonspace(text, i + 1)
                i = close_index + 1
                continue
            flush()
            indent += 1
            i += 1
            continue

        if ch == ",":
            current.append(ch)
            flush()
            i += 1
            continue

        if ch == ")":
            flush()
            indent = max(0, indent - 1)
            current.append(ch)
            i += 1
            if i < len(text) and text[i] not in ",)":
                flush()
            continue

        current.append(ch)
        i += 1

    flush()
    return "\n".join(line.rstrip() for line in lines if line.strip())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("formula", help="Formula file path, or - for standard input")
    parser.add_argument("-o", "--output", help="Write to this path instead of standard output")
    parser.add_argument("--compact", action="store_true", help="Emit one normalized line")
    parser.add_argument("--indent", type=int, default=4, help="Spaces per indentation level")
    args = parser.parse_args()

    if args.indent < 1 or args.indent > 12:
        parser.error("--indent must be between 1 and 12")

    try:
        source = load_text(args.formula)
    except (OSError, UnicodeError) as exc:
        print(f"Unable to read formula: {exc}", file=sys.stderr)
        return 2

    result = compact_formula(source) if args.compact else pretty_formula(source, args.indent)
    result += "\n"

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
    else:
        sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
