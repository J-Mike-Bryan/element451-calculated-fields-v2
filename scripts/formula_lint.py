#!/usr/bin/env python3
"""Static checks for Element451 calculated-field formulas.

This tool cannot execute Element451 formulas. It catches structural and common
portability problems before the formula is pasted into Element451. The Element
Evaluate preview remains the runtime source of truth.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Diagnostic:
    severity: str
    code: str
    message: str
    line: int
    column: int


EXACT_ARITY = {
    "IF": 3,
    "REGEXP_MATCH": 2,
    "REGEXP_EXTRACT": 2,
    "REGEXP_EXTRACT_NTH": 3,
    "REGEXP_REPLACE": 3,
    "CEEB_MAP": 4,
    "DS_MAP": 5,
    "TAXONOMY_MAP": 4,
    "CHECKBOX_CHECKED": 2,
    "CHECKBOX_FIRST": 1,
    "HAS_ONE_TRUE": 2,
    "DB_MAP": 5,
    "SC_MAP_IMPORT": 2,
    "SC_MAP_EXPORT": 2,
    "DATE_ADD": 3,
    "DATE_DIFF": 3,
    "DATE_COMPARE": 3,
    "DATE_FORMAT": 2,
    "DATE_DEFAULT": 1,
    "DATE_READ": 2,
    "SQR": 1,
    "SIN": 1,
    "ATAN": 1,
    "COSH": 1,
    "COTAN": 1,
    "EXP": 1,
    "LN": 1,
    "LOG": 1,
    "SQRT": 1,
    "ABS": 1,
    "SIGN": 1,
    "TRUNC": 1,
    "CEIL": 1,
    "FLOOR": 1,
    "RND": 0,
    "VAL": 1,
    "POW": 2,
    "MIN": 2,
    "MAX": 2,
    "MOD": 2,
    "NUM": 1,
    "DATE_FORMAT": 2,
    "DATE_ADD": 3,
    "SPLIT_INDEX": 3,
    "SUBSTR": 3,
    "STRLEN": 1,
    "LEFT": 2,
    "RIGHT": 2,
    "UPPER": 1,
    "LOWER": 1,
    "TRIM": 1,
    "PAD": 3,
    "TITLECASE": 1,
    "FIRST": 1,
    "CONTAINS": 2,
    "STARTS_WITH": 2,
    "ENDS_WITH": 2,
}

MIN_ARITY = {
    "CONCAT": 1,
    "SUM": 1,
}

SMART_CHARS = {
    "\u2018": "ASCII apostrophe or quote",
    "\u2019": "ASCII apostrophe or quote",
    "\u201c": "straight double quote",
    "\u201d": "straight double quote",
    "\u00a0": "regular space",
}


def offset_to_line_col(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    last_newline = text.rfind("\n", 0, offset)
    column = offset + 1 if last_newline < 0 else offset - last_newline
    return line, column


def add_diag(
    out: list[Diagnostic], text: str, severity: str, code: str, message: str, offset: int
) -> None:
    line, column = offset_to_line_col(text, max(0, offset))
    out.append(Diagnostic(severity, code, message, line, column))


def mask_strings(text: str) -> str:
    """Replace string contents with spaces while preserving indexes and newlines."""
    chars = list(text)
    in_string = False
    i = 0
    while i < len(chars):
        ch = chars[i]
        if not in_string:
            if ch == '"':
                in_string = True
                chars[i] = " "
            i += 1
            continue

        if ch == '"':
            if i + 1 < len(chars) and chars[i + 1] == '"':
                chars[i] = " "
                chars[i + 1] = " "
                i += 2
                continue
            in_string = False
            chars[i] = " "
            i += 1
            continue

        if ch != "\n":
            chars[i] = " "
        i += 1
    return "".join(chars)


def string_literal_spans(text: str) -> list[tuple[int, int]]:
    """Return (content_start, content_end) spans for formula string literals.

    Element escapes a literal double quote by doubling it. Spans include the raw
    string contents between the outer quotes so diagnostics can point at token-like
    bracket sequences that may be seen by the export preview compiler.
    """
    spans: list[tuple[int, int]] = []
    in_string = False
    start = -1
    i = 0
    while i < len(text):
        ch = text[i]
        if not in_string:
            if ch == '"':
                in_string = True
                start = i + 1
            i += 1
            continue

        if ch == '"':
            if i + 1 < len(text) and text[i + 1] == '"':
                i += 2
                continue
            spans.append((start, i))
            in_string = False
            start = -1
        i += 1
    return spans


def bracket_sequences_inside_strings(text: str) -> list[tuple[int, str]]:
    """Find raw [...]-style sequences that occur inside quoted strings.

    Element support confirmed that Export Preview can interpret bracketed text
    inside a regex/string (for example [.] or [a-z]) as a field token even though
    Test Formula evaluates it as literal string content.
    """
    found: list[tuple[int, str]] = []
    for start, end in string_literal_spans(text):
        raw = text[start:end]
        for match in re.finditer(r"\[[^\]\r\n]+\]", raw):
            found.append((start + match.start(), match.group(0)))
    return found


def structural_checks(text: str) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    stack: list[tuple[str, int]] = []
    in_string = False
    string_start = -1
    i = 0

    while i < len(text):
        ch = text[i]
        if not in_string:
            if ch == '"':
                in_string = True
                string_start = i
            elif ch in "([":
                stack.append((ch, i))
            elif ch in ")]":
                expected = "(" if ch == ")" else "["
                if not stack or stack[-1][0] != expected:
                    add_diag(
                        diagnostics,
                        text,
                        "error",
                        "unmatched-closer",
                        f"Unmatched closing {ch!r}.",
                        i,
                    )
                else:
                    stack.pop()
            i += 1
            continue

        if ch == '"':
            if i + 1 < len(text) and text[i + 1] == '"':
                i += 2
                continue
            in_string = False
        i += 1

    if in_string:
        add_diag(
            diagnostics,
            text,
            "error",
            "unclosed-string",
            "String literal is not closed with a straight double quote.",
            string_start,
        )

    for opener, offset in reversed(stack):
        closer = ")" if opener == "(" else "]"
        add_diag(
            diagnostics,
            text,
            "error",
            "unclosed-delimiter",
            f"Opening {opener!r} is missing closing {closer!r}.",
            offset,
        )

    return diagnostics


@dataclass
class CallFrame:
    name: str | None
    offset: int
    commas: int = 0
    has_content: bool = False


def function_calls(text: str) -> list[tuple[str, int, int]]:
    """Return (function name, argument count, offset) for syntactic calls."""
    calls: list[tuple[str, int, int]] = []
    frames: list[CallFrame] = []
    in_string = False
    field_depth = 0
    i = 0

    while i < len(text):
        ch = text[i]
        if in_string:
            if ch == '"':
                if i + 1 < len(text) and text[i + 1] == '"':
                    i += 2
                    continue
                in_string = False
            i += 1
            continue

        if ch == '"':
            in_string = True
            if frames:
                frames[-1].has_content = True
            i += 1
            continue

        if ch == "[":
            field_depth += 1
            if frames:
                frames[-1].has_content = True
            i += 1
            continue
        if ch == "]" and field_depth:
            field_depth -= 1
            i += 1
            continue
        if field_depth:
            i += 1
            continue

        if ch == "(":
            j = i - 1
            while j >= 0 and text[j].isspace():
                j -= 1
            end = j + 1
            while j >= 0 and (text[j].isalnum() or text[j] == "_"):
                j -= 1
            name = text[j + 1 : end]
            if not name or not (name[0].isalpha() or name[0] == "_"):
                name = None
            if frames:
                frames[-1].has_content = True
            frames.append(CallFrame(name.upper() if name else None, j + 1))
            i += 1
            continue

        if ch == "," and frames:
            frames[-1].commas += 1
            i += 1
            continue

        if ch == ")" and frames:
            frame = frames.pop()
            if frame.name:
                argc = 0 if not frame.has_content else frame.commas + 1
                calls.append((frame.name, argc, frame.offset))
            if frames:
                frames[-1].has_content = True
            i += 1
            continue

        if frames and not ch.isspace():
            frames[-1].has_content = True
        i += 1

    return calls


def semantic_checks(text: str, strict_functions: bool, export_context: bool) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    if text.startswith("\ufeff"):
        add_diag(
            diagnostics,
            text,
            "warning",
            "bom",
            "Remove the UTF-8 byte-order mark before pasting the formula.",
            0,
        )

    for offset, ch in enumerate(text):
        if ch in SMART_CHARS:
            add_diag(
                diagnostics,
                text,
                "error" if ch in "\u201c\u201d" else "warning",
                "non-ascii-punctuation",
                f"Replace {ch!r} with a {SMART_CHARS[ch]}.",
                offset,
            )

    for offset, sequence in bracket_sequences_inside_strings(text):
        severity = "error" if export_context else "warning"
        add_diag(
            diagnostics,
            text,
            severity,
            "bracket-token-in-string",
            (
                f"Bracketed text {sequence!r} appears inside a quoted string. "
                "Element Export Preview may interpret it as a field token even when Test Formula works. "
                "Avoid regex character classes such as [.] or [a-z] in export formulas, or rewrite and verify Preview Export."
            ),
            offset,
        )

    masked = mask_strings(text)

    for match in re.finditer(r"\bREGEX_REPLACE\b", masked, flags=re.IGNORECASE):
        add_diag(
            diagnostics,
            text,
            "error",
            "function-name",
            "Use REGEXP_REPLACE, not REGEX_REPLACE.",
            match.start(),
        )

    for match in re.finditer(r"\[([^\]]*)\]", masked):
        content = match.group(1).strip()
        if not content:
            add_diag(
                diagnostics,
                text,
                "error",
                "empty-field",
                "Field reference brackets are empty.",
                match.start(),
            )
        if content in {"C#", "Column#"} or any(token in content for token in ("<", ">", "{{", "}}")):
            add_diag(
                diagnostics,
                text,
                "warning",
                "placeholder",
                f"Replace unresolved field placeholder [{content}] before use.",
                match.start(),
            )

    for match in re.finditer(r"(?<!\d)-\s*(18000|14400)\b", masked):
        add_diag(
            diagnostics,
            text,
            "warning",
            "fixed-eastern-offset",
            "A fixed Eastern Time offset is seasonal: -18000 is EST and -14400 is EDT. Verify the intended date range.",
            match.start(),
        )

    known = set(EXACT_ARITY) | set(MIN_ARITY)
    for name, argc, offset in function_calls(text):
        if name in EXACT_ARITY and argc != EXACT_ARITY[name]:
            add_diag(
                diagnostics,
                text,
                "warning",
                "arity",
                f"{name} appears to have {argc} argument(s); the bundled reference documents {EXACT_ARITY[name]}.",
                offset,
            )
        elif name in MIN_ARITY and argc < MIN_ARITY[name]:
            add_diag(
                diagnostics,
                text,
                "warning",
                "arity",
                f"{name} appears to have {argc} argument(s); expected at least {MIN_ARITY[name]}.",
                offset,
            )
        elif strict_functions and name not in known:
            add_diag(
                diagnostics,
                text,
                "warning",
                "unknown-function",
                f"{name} is not in the bundled function catalog. Verify it in current official documentation.",
                offset,
            )

    return diagnostics


def deduplicate(items: Iterable[Diagnostic]) -> list[Diagnostic]:
    seen: set[tuple[str, str, str, int, int]] = set()
    result: list[Diagnostic] = []
    for item in items:
        key = (item.severity, item.code, item.message, item.line, item.column)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return sorted(result, key=lambda d: (d.line, d.column, d.severity, d.code))


def load_formula(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8-sig")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("formula", help="Formula file path, or - for standard input")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument(
        "--strict-functions",
        action="store_true",
        help="Warn about calls not present in the bundled function catalog",
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help=(
            "Apply export-preview-specific checks. In particular, token-like bracket "
            "sequences inside quoted strings are errors because Export Preview may "
            "interpret them as field references."
        ),
    )
    args = parser.parse_args()

    try:
        text = load_formula(args.formula)
    except (OSError, UnicodeError) as exc:
        print(f"Unable to read formula: {exc}", file=sys.stderr)
        return 2

    diagnostics = deduplicate(
        structural_checks(text) + semantic_checks(text, args.strict_functions, args.export)
    )
    errors = sum(item.severity == "error" for item in diagnostics)
    warnings = sum(item.severity == "warning" for item in diagnostics)

    if args.json:
        print(
            json.dumps(
                {
                    "errors": errors,
                    "warnings": warnings,
                    "diagnostics": [asdict(item) for item in diagnostics],
                },
                indent=2,
            )
        )
    else:
        for item in diagnostics:
            print(
                f"{item.severity.upper():7} {item.line}:{item.column} "
                f"[{item.code}] {item.message}"
            )
        if not diagnostics:
            print("OK: no static issues found.")
        else:
            print(f"Summary: {errors} error(s), {warnings} warning(s).")
        print("Note: this is a static check; verify runtime behavior with Element451 Evaluate.")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
