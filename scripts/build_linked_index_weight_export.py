#!/usr/bin/env python3
"""Generate a compact-JSON Element451 Export formula selecting one object's field
by its largest numeric index_weight (or another configured integer rank).

This generates a formula; it does not evaluate it inside Element451. Refer to
references/school-root-index-weight.md for source-serializer prerequisites.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from compact_record_pipeline import Pipeline, quote

ROOT_TOKEN = re.compile(r"^\[[A-Za-z0-9_-]+\]$")
JSON_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
DIGIT = "(?:0|1|2|3|4|5|6|7|8|9)"


def generate(
    root: str = "[user-education-schools-root]",
    eligible_key: str = "type",
    eligible_value: str = "college",
    rank_key: str = "index_weight",
    output_key: str = "name",
    max_objects: int = 20,
    rank_width: int = 6,
) -> str:
    """Generate the user-confirmed school-export architecture, generalized.

    - Input must be a compact serialized array with object boundary `},{`.
    - Integer ranks must be nonnegative and fit in rank_width decimal digits.
    - Objects are scanned in serialized order. Rank ties choose the later slot.
    - The winning object's output field may be absent: return empty instead of
      borrowing the value from another object.
    """
    if not ROOT_TOKEN.fullmatch(root):
        raise ValueError("root must be an Element field token such as [user-education-schools-root]")
    for key in [eligible_key, rank_key, output_key]:
        if not JSON_KEY.fullmatch(key):
            raise ValueError("JSON property names must be simple letters/digits/underscores")
    if not eligible_value or '"' in eligible_value or "\\" in eligible_value:
        raise ValueError("eligible-value must be a nonempty literal without quotes/backslashes")
    if not 1 <= max_objects <= 99:
        raise ValueError("max-objects must be 1..99; increasing it increases source size")
    if not 1 <= rank_width <= 16:
        raise ValueError("rank-width must be 1..16; verify source-value range")

    slot_width = max(2, len(str(max_objects)))
    matching_type = quote(f'"{eligible_key}":"{eligible_value}"')
    numeric_rank = quote(f'"{rank_key}":{DIGIT}+')
    rank_capture = quote(f'"{rank_key}":({DIGIT}+)')
    producers = []
    for i in range(1, max_objects + 1):
        obj = f'SPLIT_INDEX({root}, "}},{{", {i})'
        slot = str(i).zfill(slot_width)
        producers.append(
            f'IF((REGEXP_MATCH({obj}, {matching_type}) = TRUE)'
            f' & (REGEXP_MATCH({obj}, {numeric_rank}) = TRUE), '
            f'CONCAT("C", RIGHT(CONCAT("{"0" * rank_width}", '
            f'REGEXP_EXTRACT({obj}, {rank_capture})), {rank_width}), '
            f'":", "{slot}", "={slot};"), "")'
        )

    table = 'CONCAT(\n    ' + ',\n    '.join(producers) + '\n)'
    # The second ordering dimension is the original slot, so a weight tie picks
    # the later serialized object. The payload ALSO retains that exact slot.
    winner_slot = Pipeline(rank_width, slot_width, max_objects, "max", "max").formula(
        table, "payload"
    )
    return (
        'REGEXP_EXTRACT(\n'
        '    SPLIT_INDEX(\n'
        f'        CONCAT("{{}}", "}},{{", {root}),\n'
        '        "},{",\n'
        f'        SUM(1, VAL(CONCAT("0", {winner_slot})))\n'
        '    ),\n'
        f'    {quote(f"\"{output_key}\":\"(.*?)\"")}\n'
        ')'
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default="[user-education-schools-root]")
    parser.add_argument("--eligible-key", default="type")
    parser.add_argument("--eligible-value", default="college")
    parser.add_argument("--rank-key", default="index_weight")
    parser.add_argument("--output-key", default="name")
    parser.add_argument("--max-objects", type=int, default=20)
    parser.add_argument("--rank-width", type=int, default=6)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        formula = generate(
            args.root, args.eligible_key, args.eligible_value,
            args.rank_key, args.output_key, args.max_objects, args.rank_width,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(formula + "\n", encoding="utf-8")
        print(json.dumps({
            "output": str(args.output),
            "formula_characters": len(formula),
            "max_raw_objects": args.max_objects,
            "index_weight_decimal_digits": args.rank_width,
            "rank_tie_policy": "later serialized object wins",
            "element_runtime_verified": False,
            "note": "Generated adaptation must be checked in Test Formula and Preview Export."
        }, indent=2))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
