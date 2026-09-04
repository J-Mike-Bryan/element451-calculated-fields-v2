#!/usr/bin/env python3
"""Lint Element451 formulas embedded in Markdown reference files.

Annotate a formula fence with one of these comments immediately before it:

    <!-- formula-lint: standard -->
    <!-- formula-lint: export -->

The following fenced ``text`` block is checked with the bundled formula linter.
This script performs static checks only; Element451 Evaluate remains the runtime
source of truth.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from formula_lint import deduplicate, semantic_checks, structural_checks  # noqa: E402

BLOCK_RE = re.compile(
    r"<!--\s*formula-lint:\s*(standard|export)\s*-->"
    r"[ \t]*\r?\n[ \t]*```text[ \t]*\r?\n"
    r"(.*?)\r?\n[ \t]*```",
    re.IGNORECASE | re.DOTALL,
)


def markdown_files(paths: Iterable[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
        elif path.suffix.lower() == ".md":
            files.append(path)
        else:
            raise ValueError(f"Not a Markdown file or directory: {path}")
    unique: list[Path] = []
    seen: set[Path] = set()
    for item in files:
        resolved = item.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(item)
    return unique


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Markdown file(s) or directories")
    parser.add_argument(
        "--warnings-as-errors",
        action="store_true",
        help="Return a failure code when a marked formula has warnings.",
    )
    args = parser.parse_args()

    try:
        files = markdown_files(args.paths)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2

    if not files:
        print("No Markdown files found.", file=sys.stderr)
        return 2

    total_blocks = 0
    total_errors = 0
    total_warnings = 0

    for path in files:
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            print(f"Unable to read {path}: {exc}", file=sys.stderr)
            return 2

        for number, match in enumerate(BLOCK_RE.finditer(text), start=1):
            total_blocks += 1
            context = match.group(1).lower()
            formula = match.group(2)
            block_line = text.count("\n", 0, match.start(2)) + 1
            diagnostics = deduplicate(
                structural_checks(formula)
                + semantic_checks(
                    formula,
                    strict_functions=True,
                    export_context=(context == "export"),
                )
            )
            errors = sum(item.severity == "error" for item in diagnostics)
            warnings = sum(item.severity == "warning" for item in diagnostics)
            total_errors += errors
            total_warnings += warnings

            label = f"{path}:{block_line} block {number} ({context})"
            if not diagnostics:
                print(f"OK      {label}")
                continue

            print(f"CHECK   {label}")
            for item in diagnostics:
                absolute_line = block_line + item.line - 1
                print(
                    f"  {item.severity.upper():7} {absolute_line}:{item.column} "
                    f"[{item.code}] {item.message}"
                )

    if total_blocks == 0:
        print(
            "No annotated formula blocks found. Add <!-- formula-lint: standard --> "
            "or <!-- formula-lint: export --> before a fenced text block.",
            file=sys.stderr,
        )
        return 2

    print(
        f"Summary: {total_blocks} formula block(s), "
        f"{total_errors} error(s), {total_warnings} warning(s)."
    )
    print("Note: static checks do not prove Element451 runtime behavior.")

    if total_errors:
        return 1
    if args.warnings_as_errors and total_warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
