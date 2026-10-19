#!/usr/bin/env python3
"""Report source-size indicators, not Element execution time or official limits."""
from __future__ import annotations
import argparse
import collections
import json
import re
from pathlib import Path
from formula_lint import mask_strings


def report(path: Path, warn_characters: int) -> dict:
    text = path.read_text(encoding='utf-8-sig')
    expression = text.rstrip('\r\n')
    masked = mask_strings(expression)
    functions = collections.Counter(re.findall(r'\b([A-Z][A-Z_0-9]*)\s*\(', masked))
    fields = collections.Counter(re.findall(r'\[[^\[\]]+\]', masked))
    depth = deepest = 0
    for char in masked:
        if char == '(':
            depth += 1
            deepest = max(depth, deepest)
        elif char == ')':
            depth -= 1
    return {
        'file': str(path),
        'characters_excluding_trailing_newlines': len(expression),
        'file_characters': len(text),
        'file_bytes': path.stat().st_size,
        'function_call_sites': dict(sorted(functions.items())),
        'field_token_occurrences': dict(sorted(fields.items())),
        'max_parenthesis_depth': deepest,
        'approximate_user_reported_warning': warn_characters,
        'at_or_above_warning': len(expression) >= warn_characters,
        'warning_is_official_limit': False,
        'note': 'Approximate user testing observation only. Smaller is not guaranteed safe. Counts are not runtime benchmarks.',
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('files', nargs='+', type=Path)
    ap.add_argument('--warn-characters', type=int, default=500000,
                    help='Approximate user-reported warning; NOT an official Element451 limit.')
    args = ap.parse_args()
    if args.warn_characters < 1:
        ap.error('--warn-characters must be positive')
    try:
        print(json.dumps([report(p, args.warn_characters) for p in args.files], indent=2))
    except (OSError, UnicodeError) as exc:
        ap.error(str(exc))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
