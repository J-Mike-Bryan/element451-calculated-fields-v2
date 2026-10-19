#!/usr/bin/env python3
"""Test abstract linked-application selection, not the Element451 runtime.

Fixtures are fictional; ranks are already numeric and no CRM maps or JSON
extractors are exercised. Python split behavior is not evidence about Element.
"""
from __future__ import annotations

import random
import unittest
from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    slot: int
    position: int
    rank: int
    eligible: bool = True
    value: str = ""


def pack_scores(candidates: list[Candidate], root_length: int) -> list[int]:
    """Encode rank, global position, and aligned slot using bounded integers."""
    if root_length <= 0:
        raise ValueError("Root length must be positive.")
    n = len(candidates)
    if [c.slot for c in candidates] != list(range(1, n + 1)):
        raise ValueError("Slots must be contiguous, unique, and in output order.")
    eligible_positions: set[int] = set()
    scores = []
    base = n + 1
    position_base = root_length + 1
    for c in candidates:
        if not c.eligible:
            scores.append(0)
            continue
        if c.rank < 0 or not 0 <= c.position < root_length:
            raise ValueError("Eligible ranks and positions must be in range.")
        if c.position in eligible_positions:
            raise ValueError("Eligible candidates must have distinct root positions.")
        eligible_positions.add(c.position)
        preference = root_length - c.position
        score = (c.rank * position_base + preference) * base + c.slot
        if score > 2**53 - 1:
            raise ValueError("Score exceeds the conservative exact-integer budget.")
        scores.append(score)
    return scores


def packed_winner(candidates: list[Candidate], root_length: int) -> int:
    return max(pack_scores(candidates, root_length), default=0) % (len(candidates) + 1)


def reference_winner(candidates: list[Candidate]) -> int:
    """Independent lexicographic selector: rank, then earliest root position."""
    eligible = [c for c in candidates if c.eligible]
    return max(eligible, key=lambda c: (c.rank, -c.position)).slot if eligible else 0


def project(candidates: list[Candidate], winner: int, separator: str = "~SLOT~") -> str:
    """Model aligned slots locally; do not infer Element SPLIT_INDEX behavior."""
    if not separator or any(separator in c.value for c in candidates):
        raise ValueError("Separator must be nonempty and absent from all outputs.")
    values = [""] + [c.value for c in candidates]
    if not 0 <= winner < len(values):
        raise ValueError("Selected slot is outside the aligned value list.")
    return separator.join(values).split(separator)[winner]


def covered_positions(root_groups: list[str], allowed: list[str], limit: int) -> list[int]:
    """Enumerate raw occurrences per fictional GUID/group, not eligible count."""
    if limit < 1 or len(allowed) != len(set(allowed)):
        raise ValueError("Use a positive per-group limit and unique allowed groups.")
    return [pos for group in allowed
            for pos in [i for i, current in enumerate(root_groups) if current == group][:limit]]


class LinkedSelectionTests(unittest.TestCase):
    def test_no_candidates(self):
        self.assertEqual(packed_winner([], 1), 0)
        self.assertEqual(project([], 0), "")

    def test_no_match_cannot_select_real_output(self):
        c = [Candidate(1, 0, 4, False, "not-selected")]
        self.assertEqual(packed_winner(c, 10), 0)
        self.assertEqual(project(c, 0), "")

    def test_rank_dominates_every_position(self):
        c = [Candidate(1, 0, 3), Candidate(2, 999, 4)]
        self.assertEqual(packed_winner(c, 1000), 2)

    def test_global_order_not_generated_group_order(self):
        c = [Candidate(1, 90, 4), Candidate(2, 3, 4)]
        self.assertEqual(packed_winner(c, 100), 2)

    def test_invalid_early_candidate_does_not_block_later(self):
        c = [Candidate(1, 0, 999, False), Candidate(2, 30, 1)]
        self.assertEqual(packed_winner(c, 100), 2)

    def test_eligible_unknown_rank_remains_positive(self):
        c = [Candidate(1, 4, 0)]
        self.assertGreater(pack_scores(c, 10)[0], 0)
        self.assertEqual(packed_winner(c, 10), 1)

    def test_known_term_beats_unknown_term(self):
        c = [Candidate(1, 0, 0), Candidate(2, 9, 1)]
        self.assertEqual(packed_winner(c, 10), 2)

    def test_all_unknowns_use_global_tie_rule(self):
        c = [Candidate(1, 8, 0), Candidate(2, 2, 0)]
        self.assertEqual(packed_winner(c, 10), 2)

    def test_missing_selected_field_does_not_fall_back(self):
        c = [Candidate(1, 0, 1, value="older"), Candidate(2, 5, 2),
             Candidate(3, 9, 1, value="another")]
        self.assertEqual(project(c, packed_winner(c, 10)), "")

    def test_trailing_empty_slot_stays_aligned(self):
        c = [Candidate(1, 0, 1, value="older"), Candidate(2, 5, 2)]
        self.assertEqual(project(c, packed_winner(c, 10)), "")

    def test_companion_projection_keeps_same_winner(self):
        c = [Candidate(1, 0, 1, value="old-id"), Candidate(2, 5, 2, value="new-id")]
        winner = packed_winner(c, 10)
        other_field = [Candidate(1, 0, 1, value="old-type"), Candidate(2, 5, 2)]
        self.assertEqual(packed_winner(other_field, 10), winner)
        self.assertEqual(project(c, winner), "new-id")
        self.assertEqual(project(other_field, winner), "")

    def test_reserved_separator_collision_is_rejected(self):
        with self.assertRaises(ValueError):
            project([Candidate(1, 0, 1, value="a~SLOT~b")], 1)

    def test_coverage_counts_raw_occurrences_per_group(self):
        root = ["other", "form-x", "form-y", "form-x", "form-x", "form-y"]
        self.assertEqual(covered_positions(root, ["form-x", "form-y"], 2), [1, 3, 2, 5])
        # The third form-x is excluded regardless of its eligibility or recency.
        self.assertNotIn(4, covered_positions(root, ["form-x", "form-y"], 2))

    def test_missing_output_does_not_shift_candidate_slot(self):
        c = [Candidate(1, 0, 9, False), Candidate(2, 3, 0, False),
             Candidate(3, 5, 1, value="third")]
        self.assertEqual(packed_winner(c, 10), 3)
        self.assertEqual(project(c, 3), "third")

    def test_invalid_bounds_are_rejected(self):
        invalid_cases = [([Candidate(2, 0, 1)], 10),
                         ([Candidate(1, 10, 1)], 10),
                         ([Candidate(1, 0, -1)], 10),
                         ([Candidate(1, 0, 1), Candidate(2, 0, 1)], 10),
                         ([Candidate(1, 0, 2**53)], 10)]
        for candidates, length in invalid_cases:
            with self.subTest(candidates=candidates), self.assertRaises(ValueError):
                pack_scores(candidates, length)

    def test_randomized_against_independent_tuple_selector(self):
        rng = random.Random(7403)
        for case in range(400):
            n = rng.randrange(0, 80)
            length = max(2, n * 31)
            positions = rng.sample(range(length), n)
            c = [Candidate(i + 1, pos, rng.randrange(0, 6000),
                           rng.random() > 0.3, "" if rng.random() < 0.3 else f"value-{i}")
                 for i, pos in enumerate(positions)]
            with self.subTest(case=case):
                slot = packed_winner(c, length)
                self.assertEqual(slot, reference_winner(c))
                expected = "" if slot == 0 else c[slot - 1].value
                self.assertEqual(project(c, slot), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
