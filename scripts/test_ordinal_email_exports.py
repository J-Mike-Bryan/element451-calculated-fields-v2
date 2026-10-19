#!/usr/bin/env python3
"""Check a provisional ordinal-email design on fictional compact JSON fixtures.

This models string operations in Python; it does NOT execute Element451 formulas,
verify live serializer shape, or establish Evaluate/Preview Export behavior.
"""
from __future__ import annotations

import itertools
import json
import re
import unittest
from typing import Any

TYPE = "UNSUBSCRIBE_EMAIL"
MARKER = '"type":"UNSUBSCRIBE_EMAIL"'
MISSING = object()
FIRST = "first@example.test"
SECOND = "second@example.test"
THIRD = "third@example.test"
OTHER = "unrelated@example.test"


def split_index(text: str, marker: str, index: int) -> str:
    """Model one-based splits with a blank missing segment, not engine behavior."""
    if index < 1:
        raise ValueError("Split indexes must be positive")
    parts = text.split(marker)
    return parts[index - 1] if index <= len(parts) else ""


def modeled_email(root: str, ordinal: int) -> str:
    if ordinal < 1:
        raise ValueError("Ordinals must be positive")
    after = split_index(root, MARKER, ordinal + 1)
    if after == "":
        return ""
    before = split_index(root, MARKER, ordinal)
    match = re.search(r'.*("name":.*)$', before)
    prefix = match.group(1) if match else ""
    bounded = prefix + MARKER + split_index(after, '},{"name":', 1)
    return split_index(split_index(bounded, '"email":"', 2), '"', 1).strip()


def record(email: Any = MISSING, *, kind: str = TYPE, before: bool = False,
           name: str = "Fictional event", **extra: Any) -> dict[str, Any]:
    item: dict[str, Any] = {"name": name}
    if before and email is not MISSING:
        item["email"] = email
    item["type"] = kind
    if not before and email is not MISSING:
        item["email"] = email
    item.update(extra)
    return item


def oracle_email(records: list[dict[str, Any]], ordinal: int) -> str:
    targets = [r for r in records if r.get("type") == TYPE]
    if ordinal > len(targets):
        return ""
    value = targets[ordinal - 1].get("email")
    return value.strip() if isinstance(value, str) else ""


def require_fixture_contract(records: list[dict[str, Any]]) -> None:
    """Protect only local fixture scope; this guard is NOT in the formulas."""
    def inspect_nested(value: Any) -> None:
        if isinstance(value, dict):
            if {"name", "type", "email"} & set(value):
                raise ValueError("Nested marker fields are outside fixture scope")
            for child in value.values():
                inspect_nested(child)
        elif isinstance(value, list):
            for child in value:
                inspect_nested(child)

    for item in records:
        if next(iter(item), None) != "name":
            raise ValueError("Fixtures require name-first milestone objects")
        value = item.get("email")
        if value is not None and not isinstance(value, str):
            raise ValueError("Email must be scalar text, omitted, or null")
        if isinstance(value, str) and any(
            ch in '\\"' or ord(ch) < 32 for ch in value
        ):
            raise ValueError("JSON-escaped email characters are outside fixture scope")
        for child in item.values():
            inspect_nested(child)


def compare(records: list[dict[str, Any]], expected: tuple[str, str] | None = None
            ) -> tuple[str, str]:
    require_fixture_contract(records)
    root = json.dumps(records, ensure_ascii=False, separators=(",", ":"))
    actual = tuple(modeled_email(root, n) for n in (1, 2))
    oracle = tuple(oracle_email(records, n) for n in (1, 2))
    if actual != oracle or (expected is not None and actual != expected):
        raise AssertionError((root, actual, oracle, expected))
    return actual


class OrdinalEmailTests(unittest.TestCase):
    def test_named_fixtures(self) -> None:
        cases = [
            ("empty", [], ("", "")),
            ("other type only", [record(OTHER, kind="OTHER")], ("", "")),
            ("one after", [record(FIRST)], (FIRST, "")),
            ("one before", [record(FIRST, before=True)], (FIRST, "")),
            ("two after", [record(FIRST), record(SECOND)], (FIRST, SECOND)),
            ("two before", [record(FIRST, before=True), record(SECOND, before=True)], (FIRST, SECOND)),
            ("mixed order", [record(FIRST), record(SECOND, before=True)], (FIRST, SECOND)),
            ("reverse mixed", [record(FIRST, before=True), record(SECOND)], (FIRST, SECOND)),
            ("first omitted", [record(), record(SECOND)], ("", SECOND)),
            ("first null", [record(None), record(SECOND)], ("", SECOND)),
            ("first empty", [record(""), record(SECOND)], ("", SECOND)),
            ("first spaces", [record("   "), record(SECOND)], ("", SECOND)),
            ("second omitted third present", [record(FIRST), record(), record(THIRD)], (FIRST, "")),
            ("second null third present", [record(FIRST), record(None), record(THIRD)], (FIRST, "")),
            ("second empty third present", [record(FIRST), record(""), record(THIRD)], (FIRST, "")),
            ("no borrow from next type", [record(), record(OTHER, kind="OTHER")], ("", "")),
            ("no borrow from previous type", [record(OTHER, kind="OTHER"), record()], ("", "")),
            ("interleaved types", [record(FIRST), record(OTHER, kind="OTHER"), record(SECOND)], (FIRST, SECOND)),
            ("duplicates", [record(FIRST), record(FIRST)], (FIRST, FIRST)),
            ("alternate names", [record(FIRST, name="Fictional import"), record(SECOND, name="Different source")], (FIRST, SECOND)),
            ("similar type not equal", [record(OTHER, kind=TYPE + "_OTHER"), record(FIRST)], (FIRST, "")),
            ("wrong email key", [record(backup_email=OTHER)], ("", "")),
            ("dates do not reorder", [record(FIRST, date=200), record(SECOND, date=100)], (FIRST, SECOND)),
            ("three limited to two", [record(FIRST), record(SECOND), record(THIRD)], (FIRST, SECOND)),
            ("type last", [{"name": "Fictional event", "email": FIRST, "date": {"$date": {"$numberLong": "1"}}, "type": TYPE}], (FIRST, "")),
            ("trim without case conversion", [record("  Upper@EXAMPLE.test  ")], ("Upper@EXAMPLE.test", "")),
            ("name text not type", [record(OTHER, kind="OTHER", name=TYPE)], ("", "")),
            ("exact quoted type", [record(OTHER, kind="PREFIX_" + TYPE), record(FIRST)], (FIRST, "")),
        ]
        for name, records, expected in cases:
            with self.subTest(case=name):
                compare(records, expected)
        self.assertEqual(len(cases), 28)

    def test_exhaustive_short_sequences(self) -> None:
        variants = [record(), record(None), record(FIRST),
                    record(SECOND, before=True), record(OTHER, kind="OTHER")]
        checked = 0
        for length in range(5):
            for sequence in itertools.product(variants, repeat=length):
                compare(list(sequence))
                checked += 1
        self.assertEqual(checked, 781)

    def test_blank_or_null_root(self) -> None:
        for root in ("", "null", "[]"):
            self.assertEqual((modeled_email(root, 1), modeled_email(root, 2)), ("", ""))

    def test_independent_sources_and_duplicates(self) -> None:
        # Model business source independence, not the label regex or live field.
        for has_label, records in itertools.product((False, True), ([], [record(FIRST)])):
            profile_result = FIRST if has_label else ""
            milestone_results = compare(records)
            combined = (profile_result, *milestone_results)
            self.assertEqual(combined[1:], (FIRST, "") if records else ("", ""))
            self.assertEqual(combined[0], FIRST if has_label else "")
        self.assertEqual((FIRST, *compare([record(FIRST)])), (FIRST, FIRST, ""))

    def test_outside_contract_is_not_certified(self) -> None:
        for records in (
            [{"type": TYPE, "name": "Not name first", "email": FIRST}],
            [record({"address": FIRST})],
            [record(metadata={"email": FIRST})],
            [record(metadata={"name": "Nested marker"})],
            [record('"quoted"@example.test')],
            [record("escaped\\value@example.test")],
        ):
            with self.subTest(records=records), self.assertRaises(ValueError):
                require_fixture_contract(records)

    def test_invalid_ordinal(self) -> None:
        with self.assertRaises(ValueError):
            modeled_email("[]", 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
