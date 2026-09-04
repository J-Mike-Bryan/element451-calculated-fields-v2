#!/usr/bin/env python3
"""Inspect a serialized Element451 milestone-root JSON sample.

This is a design-time diagnostic. It verifies assumptions about milestone type,
application, term, major, and timestamp before a calculated-field formula is
built. It does not emulate Element451's formula runtime.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_term_map(items: list[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise argparse.ArgumentTypeError(
                f"Invalid --term-map value {item!r}; expected GUID=LABEL"
            )
        guid, label = item.split("=", 1)
        guid = guid.strip()
        label = label.strip()
        if not guid or not label:
            raise argparse.ArgumentTypeError(
                f"Invalid --term-map value {item!r}; expected GUID=LABEL"
            )
        mapping[guid] = label
    return mapping


def get_date_ms(item: dict[str, Any]) -> str | None:
    value = item.get("date")
    if not isinstance(value, dict):
        return None
    value = value.get("$date")
    if not isinstance(value, dict):
        return None
    raw = value.get("$numberLong")
    if raw is None:
        return None
    return str(raw)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect Element451 milestone-root JSON by canonical milestone type."
    )
    parser.add_argument("json_file", help="Path to a file containing the raw JSON array")
    parser.add_argument("--type", required=True, dest="milestone_type")
    parser.add_argument("--application-guid")
    parser.add_argument("--exclude-major")
    parser.add_argument(
        "--term-guid",
        action="append",
        default=[],
        help="Allowed term GUID; repeat for multiple values",
    )
    parser.add_argument(
        "--term-map",
        action="append",
        default=[],
        metavar="GUID=LABEL",
        help="Optional verified GUID mapping for display; repeat as needed",
    )
    args = parser.parse_args()

    path = Path(args.json_file)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("Root sample must be a JSON array of milestone objects")

    term_map = parse_term_map(args.term_map)
    allowed_terms = set(args.term_guid)
    targets = [x for x in data if isinstance(x, dict) and x.get("type") == args.milestone_type]

    eligible_count = 0
    print(f"target_type={args.milestone_type} total={len(targets)}")
    for idx, item in enumerate(targets, start=1):
        reasons: list[str] = []
        app = item.get("application_guid")
        term = item.get("term")
        major = item.get("major")
        date_ms = get_date_ms(item)

        if args.application_guid and app != args.application_guid:
            reasons.append("application_guid")
        if allowed_terms and term not in allowed_terms:
            reasons.append("term")
        if args.exclude_major and major == args.exclude_major:
            reasons.append("excluded_major")
        if not date_ms:
            reasons.append("date")

        eligible = not reasons
        eligible_count += int(eligible)
        mapped = term_map.get(term, "") if isinstance(term, str) else ""
        mapped_text = f" mapped={mapped!r}" if mapped else ""
        reason_text = ",".join(reasons) if reasons else "-"
        print(
            f"{idx}: name={item.get('name')!r} app={app!r} term={term!r}{mapped_text} "
            f"major={major!r} date_ms={date_ms!r} eligible={'yes' if eligible else 'no'} "
            f"reasons={reason_text}"
        )

    print(f"eligible={eligible_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
