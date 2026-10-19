#!/usr/bin/env python3
"""Test a fictional abstract term-source model, NOT Element451 execution.

These tests validate source precedence, rank bounds, projection alignment, and
raw per-definition coverage. They do not parse roots, execute the delivered
formulas, or verify real mappings. All policy values below are test fixtures.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from collections import defaultdict
from typing import Iterable
import unittest

PERIOD_BASE = 10
TYPE_BASE = 10
MAX_YEAR_INDEX = 99
SOURCE_BASE = 100_000
SOURCE_TIERS = {"secondary": 1, "primary": 2}
ALLOWED_DEFINITIONS = frozenset({"definition-alpha", "definition-beta"})
PERIOD_LABELS = {1: "Period One", 2: "Period Two", 3: "Period Three"}


@dataclass(frozen=True)
class Candidate:
    source: str
    definition: str = "definition-alpha"
    present: bool = True
    eligible: bool = True
    year_index: int | None = 10
    period: int | None = 1
    type_rank: int = 0


def score(candidate: Candidate) -> int:
    if candidate.source not in SOURCE_TIERS:
        raise ValueError("Unknown source")
    if not candidate.present or not candidate.eligible:
        return 0
    if candidate.definition not in ALLOWED_DEFINITIONS:
        return 0
    if not 0 <= candidate.type_rank < TYPE_BASE:
        raise ValueError("Type rank must fit its encoding base")
    if candidate.period is not None and not 0 <= candidate.period < PERIOD_BASE:
        raise ValueError("Period must fit its encoding base")
    if candidate.year_index is None:
        detail = candidate.type_rank
    else:
        if not 0 <= candidate.year_index <= MAX_YEAR_INDEX:
            raise ValueError("Year index is outside the fixture domain")
        # Plus one keeps a real first-year value distinct from an unknown year.
        term = (candidate.year_index + 1) * PERIOD_BASE + (candidate.period or 0)
        detail = term * TYPE_BASE + candidate.type_rank
    if not 0 <= detail < SOURCE_BASE:
        raise ValueError("Detail score crosses a source-priority boundary")
    return SOURCE_TIERS[candidate.source] * SOURCE_BASE + detail


def select(candidates: Iterable[Candidate], ceiling: int = 3) -> Candidate | None:
    if ceiling < 1:
        raise ValueError("Coverage must be positive")
    seen: dict[tuple[str, str], int] = defaultdict(int)
    winner = None
    best = 0
    for candidate in candidates:
        if not candidate.present or candidate.definition not in ALLOWED_DEFINITIONS:
            continue
        key = (candidate.source, candidate.definition)
        seen[key] += 1
        if seen[key] > ceiling:
            continue
        value = score(candidate)
        if value > best:  # Earliest equal score is this fixture's tie policy.
            winner, best = candidate, value
    return winner


def project(candidate: Candidate | None) -> tuple[str, str]:
    """Return (period label, year-index text) from the very same winner."""
    if candidate is None or candidate.year_index is None:
        return "", ""
    return PERIOD_LABELS.get(candidate.period, ""), str(candidate.year_index)


def decoded_year_index(value: int) -> int | None:
    if value == 0:
        return None
    term = (value % SOURCE_BASE) // TYPE_BASE
    ordinal = term // PERIOD_BASE
    return None if ordinal == 0 else ordinal - 1


def decode_period(code: str, name: str) -> str:
    """Model caller-supplied fictional prefixes; never a tenant lookup."""
    prefixes = {"PX": "Period One", "QX": "Period Two", "RX": "Period Three"}
    label = prefixes.get(code.strip().upper()[:2])
    if label:
        return label
    normalized_name = name.strip().upper()
    for expected in PERIOD_LABELS.values():
        text = expected.upper()
        if normalized_name == text or normalized_name.startswith(text + " "):
            return expected
    return ""


class TermFallbackTests(unittest.TestCase):
    def test_no_candidate(self):
        self.assertEqual(project(select([])), ("", ""))

    def test_primary_only(self):
        self.assertEqual(project(select([Candidate("primary")])), ("Period One", "10"))

    def test_secondary_only(self):
        app = Candidate("secondary", year_index=12, period=2)
        self.assertEqual(project(select([app])), ("Period Two", "12"))

    def test_oldest_primary_beats_newest_secondary(self):
        primary = Candidate("primary", year_index=0, period=1)
        app = Candidate("secondary", year_index=MAX_YEAR_INDEX, period=9, type_rank=9)
        self.assertIs(select([app, primary]), primary)

    def test_ineligible_primary_allows_fallback(self):
        app = Candidate("secondary")
        self.assertIs(select([Candidate("primary", eligible=False), app]), app)

    def test_newest_secondary_term_wins(self):
        older = Candidate("secondary", year_index=11, period=3)
        newer = Candidate("secondary", year_index=12, period=1)
        self.assertIs(select([newer, older]), newer)

    def test_period_orders_equal_years(self):
        first = Candidate("primary", period=1)
        last = replace(first, period=3)
        self.assertIs(select([last, first]), last)

    def test_type_cannot_overrule_newer_term(self):
        older = Candidate("primary", period=1, type_rank=9)
        newer = Candidate("primary", period=2, type_rank=0)
        self.assertIs(select([older, newer]), newer)

    def test_type_breaks_same_term_tie(self):
        low = Candidate("primary", type_rank=1)
        high = replace(low, type_rank=5)
        self.assertIs(select([low, high]), high)
        self.assertEqual(project(low), project(high))

    def test_unknown_primary_period_does_not_enable_fallback(self):
        primary = Candidate("primary", period=None)
        app = Candidate("secondary", year_index=20)
        self.assertEqual(project(select([app, primary])), ("", "10"))

    def test_eligible_unknown_term_still_has_source_priority(self):
        primary = Candidate("primary", year_index=None, period=None)
        app = Candidate("secondary", year_index=20)
        self.assertIs(select([app, primary]), primary)
        self.assertEqual(project(primary), ("", ""))
        self.assertGreater(score(primary), 0)

    def test_projections_share_the_winner(self):
        early = Candidate("secondary", year_index=10, period=3)
        late = Candidate("secondary", year_index=11, period=2)
        self.assertEqual(project(select([early, late])), ("Period Two", "11"))

    def test_sparse_absent_slots_do_not_create_candidates(self):
        absent = Candidate("primary", present=False)
        app = Candidate("secondary")
        self.assertIs(select([absent] * 5 + [app]), app)

    def test_invalid_earlier_record_does_not_stop_scan(self):
        valid = Candidate("primary")
        self.assertIs(select([replace(valid, eligible=False), valid]), valid)

    def test_invalid_raw_occurrences_consume_coverage(self):
        invalid = Candidate("primary", eligible=False)
        beyond = Candidate("primary", year_index=20)
        app = Candidate("secondary")
        self.assertIs(select([invalid] * 3 + [beyond, app]), app)
        self.assertIs(select([invalid] * 3 + [beyond, app], ceiling=4), beyond)

    def test_other_allowed_definition_has_its_own_coverage(self):
        invalid = Candidate("primary", eligible=False)
        other = Candidate("primary", definition="definition-beta")
        self.assertIs(select([invalid] * 4 + [other]), other)

    def test_disallowed_definition_does_not_consume_allowed_slots(self):
        unrelated = Candidate("primary", definition="definition-other")
        valid = Candidate("primary")
        self.assertIs(select([unrelated] * 8 + [valid]), valid)

    def test_score_domain_and_decoding_boundaries(self):
        max_detail = ((MAX_YEAR_INDEX + 1) * PERIOD_BASE + PERIOD_BASE - 1) * TYPE_BASE + TYPE_BASE - 1
        self.assertLess(max_detail, SOURCE_BASE)
        for source in SOURCE_TIERS:
            for year in (0, 1, MAX_YEAR_INDEX):
                for period in (None, 1, 3, PERIOD_BASE - 1):
                    candidate = Candidate(source, year_index=year, period=period)
                    self.assertEqual(decoded_year_index(score(candidate)), year)
        self.assertIsNone(decoded_year_index(0))
        self.assertIsNone(decoded_year_index(score(Candidate("primary", year_index=None))))

    def test_real_zero_year_index_is_not_no_match(self):
        candidate = Candidate("primary", year_index=0)
        self.assertEqual(project(candidate), ("Period One", "0"))
        self.assertEqual(decoded_year_index(score(candidate)), 0)

    def test_rank_limits_are_checked(self):
        for change in ({"type_rank": 10}, {"period": 10}, {"year_index": 100}):
            with self.assertRaises(ValueError):
                score(replace(Candidate("primary"), **change))

    def test_prefix_normalization(self):
        self.assertEqual(decode_period(" qx-31 ", ""), "Period Two")

    def test_approved_numbered_variant_has_same_prefix(self):
        self.assertEqual(decode_period("QX-31", ""), decode_period("QX1-31", ""))

    def test_name_fallback_uses_explicit_name_patterns(self):
        self.assertEqual(decode_period("ZZ-31", "Period Two 2131"), "Period Two")
        self.assertEqual(decode_period("ZZ-31", "Period Twoish"), "")
        self.assertEqual(decode_period("ZZ-31", "Unmapped"), "")

    def test_name_decoding_does_not_change_inherited_code_eligibility(self):
        # Eligibility is a distinct policy, not the output decoder's decision.
        code = ""
        candidate = Candidate("primary", eligible=bool(code.strip()))
        self.assertEqual(decode_period(code, "Period Two"), "Period Two")
        self.assertEqual(score(candidate), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
