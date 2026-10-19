# Application-root selection shared across export columns

## Table of contents

- [Evidence and scope](#evidence-and-scope)
- [Select one application, then project its fields](#select-one-application-then-project-its-fields)
- [Map eligibility and output separately](#map-eligibility-and-output-separately)
- [Rank mapped terms without importing institutional policy](#rank-mapped-terms-without-importing-institutional-policy)
- [Preserve global order across separate occurrence scans](#preserve-global-order-across-separate-occurrence-scans)
- [Optional packed-score selector](#optional-packed-score-selector)
- [Small runtime diagnostics](#small-runtime-diagnostics)
- [Coverage and serializer limits](#coverage-and-serializer-limits)
- [Regression and runtime checks](#regression-and-runtime-checks)

## Evidence and scope

Use this reference when several calculated export columns must describe the same winning application, especially when ranking by mapped term rather than an application timestamp. Read `references/root-field-parsing.md` and `references/root-field-selection.md` for the existing occurrence guards, same-object isolation, and mapping guidance; do not duplicate those rules here.

**Status:** reusable design guidance with locally tested abstract selection invariants and static-lint-clean diagnostic formulas. No user-reported Element451 Evaluate or Preview Export results have established this complete multi-column application selector. The included Python tests are not an Element formula interpreter and do not verify serialization or live maps. Do not promote prior simulation totals or successful file generation into runtime evidence.

For the separate user-reported successful scalar term-season solution with milestone-first application fallback, see `references/term-root-fallback.md`. Its source/rank arithmetic does not verify the output-slot-list design below, and the subsequent year projection still needs separate runtime confirmation.

Keep application allow-lists, academic classifications, field overrides, term conventions, scan ceilings, and tie rules request-scoped. Do not bundle real root payloads, exported formulas containing tenant identifiers, or institutional lookup tables.

## Select one application, then project its fields

Construct one conceptual selector per eligibility group. Generate the same candidate inventory, eligibility conditions, ranking expression, scan ceiling, and tie policy for every output in that group. Change only the final field extraction or output mapping. Standalone formulas must fully expand that shared selector; do not introduce helper-column dependencies unless requested.

Distinguish two operations:

- **Eligibility:** decide whether the application may participate at all. Missing metadata required to classify it makes it ineligible.
- **Projection:** return a field from the already selected application. A missing output value returns the requested blank without selecting a different application.

When the winning application lacks a requested field, do not fill it from an older application merely because that older record has a nonblank value. Otherwise the exported row can combine unrelated application records. Never add submitted-only, status, timestamp, or completeness preferences unless requested.

Use the current root sample to verify property names. A registration identifier, an application configuration GUID, a raw student-type code, a major GUID, a mapped major name, and a degree code are different outputs. Do not assume a configuration GUID uniquely identifies an individual registration. Use a registration identifier as a diagnostic when it is present and distinguishes the candidate records; otherwise show the occurrence position and relevant fields together.

## Map eligibility and output separately

When requested, derive classification from the bounded application's major rather than its stored application-degree property. Do not claim this is universally more accurate; the authoritative source is a task-specific choice.

Reuse the existing database-backed major-degree guidance in `references/formula-functions.md` and `references/root-field-selection.md` when inactive majors must remain resolvable. Do not extend the recorded inactive-major degree observation into proof that major-name, term-code, or every other map behaves identically. Test those lookups independently.

`FIRST` selects one associated degree; it is not an any-associated-degree test. State whether the requirement is first, any, all, or a particular classification. If multiple associated degrees can qualify, define which one to output and keep the eligibility and output rules consistent. Never invent an ordering guarantee for an association list.

Clarify whether the final output should be a raw code, GUID, stored value, or display name. Do not translate raw student-type values or expand degree codes into labels without a supplied or verified mapping.

## Rank mapped terms without importing institutional policy

Map the term GUID to a configured code/name before deriving a numeric rank. Do not sort opaque GUID suffixes, assume lexical code order is chronological, or use registration/update/submission timestamps as substitutes for term recency.

Obtain the period ordering, year convention, supported code forms, and optional-session equivalence from the current request or a verified mapping. For a calendar-year-first rule, a conceptual rank is `year * K + period_rank`, where `K` exceeds every allowed period rank. Academic-year conventions can require a different ordering.

Only remove a numbered or other session suffix when the user establishes that it has no meaning for this task. Do not globally remove digits, collapse genuinely distinct sessions, or silently treat all numbered terms as equivalent. Normalize case/spacing only when appropriate; validate the complete supported code shape before converting its year. State the century/window when expanding two-digit years.

Choose an explicit policy for missing, unmapped, or malformed terms: exclude them, keep them below known terms, or apply another user-defined rule. When unknown terms remain eligible, keep their score distinct from the invalid/no-candidate sentinel; if all terms are unknown, apply the stated tie rule rather than claiming their recency is known. Do not automatically make a nonblank term a new eligibility condition.

## Preserve global order across separate occurrence scans

Scanning each allowed application GUID separately can accidentally favor the GUID whose candidates are generated first. Candidate-slot order is not necessarily original root order.

If the chosen tie policy is earliest original occurrence, compare the candidates' absolute positions in the same root string (or a verified equivalent global ordinal), not their per-GUID occurrence numbers or generated slots. Apply the same rule even when equal-ranked applications have different allowed GUIDs. State this policy as an assumption when the user has not specified one; do not claim the first serialized application is inherently more accurate.

For a verified literal marker, the position of its nth occurrence can be recovered conceptually by summing the lengths of the n preceding split segments and adding `(n - 1) * marker_length`. Derive lengths from the actual marker rather than copying a tenant-specific numeric length. Guard occurrence existence first, and do not confuse one-based split indexes with zero-based character positions.

## Optional packed-score selector

A numeric sort key can carry the winning candidate's slot, reducing repeated value-selection branches. Use only source-supported functions and verify the assembled formula's numeric and splitting behavior in the target context.

The following is design notation, **not a paste-ready Element formula**:

```text
N = fixed candidate count, including absent and ineligible slots
B = N + 1
L = length of the current root string
P = L + 1
slot_i = unique integer in 1..N
position_i = verified zero-based marker position in 0..L-1
position_preference_i = L - position_i
rank_i = nonnegative integer term rank; zero may mean eligible/unknown

score_i = 0 when absent or ineligible
score_i = ((rank_i * P + position_preference_i) * B) + slot_i otherwise

winner_slot = MOD(MAX_of_all_scores, B)
output = SPLIT_INDEX(aligned_output_string, reserved_separator, winner_slot + 1)
```

Keep these invariants:

1. Set `B` above every slot number, so `MOD` recovers only the slot. Recalculate it when coverage changes.
2. Set `P` above every position-preference value, so position cannot outweigh a one-unit rank difference. Preserve exact integer comparisons; very large scores can lose precision. Do not assume Element's numeric representation. A conservative exact-integer budget for common binary floating-point implementations is at most `2**53 - 1`, but verify the target runtime separately.
3. Give each eligible application a positive score, even with an unknown term. Reserve zero exclusively for absent/ineligible candidates.
4. Begin the aligned output list with an empty slot. A zero maximum must select this explicit no-match slot, never the first real or unscanned application.
5. Retain one output slot per candidate, including empty and absent candidates, in exactly the same order as the score inventory. Never drop blank slots.
6. Choose a separator that cannot appear in any output, including mapped names. Detect collisions and change the separator or use pairwise selection; do not silently strip characters from real values.
7. Verify that the actual `SPLIT_INDEX` implementation preserves leading, internal, and trailing empty segments. Static linting and Python string splitting do not establish this behavior in Element451.

Keep a simpler pairwise selector available when packing would exceed a numeric bound or require unproven delimiter behavior. Do not assert a performance improvement without measuring an actual export.

## Small runtime diagnostics

These literal-only probes are static-lint clean, not user-verified. They deliberately use fictional values and no tenant configuration. Run them in Evaluate and Preview Export before relying on packed-slot selection.

**Associated slot:** expected `second`; the lower base-10 digit of the winning score is 2, and the output list begins with an empty slot.

<!-- formula-lint: export -->
```text
SPLIT_INDEX(
    CONCAT("", "~SLOT_BOUNDARY~", "first", "~SLOT_BOUNDARY~", "second"),
    "~SLOT_BOUNDARY~",
    MOD(MAX(301, 502), 10) + 1
)
```

**No match:** expected an empty string, even though real output slots exist.

<!-- formula-lint: export -->
```text
SPLIT_INDEX(
    CONCAT("", "~SLOT_BOUNDARY~", "first", "~SLOT_BOUNDARY~", "second"),
    "~SLOT_BOUNDARY~",
    MOD(MAX(0, 0), 10) + 1
)
```

**Selected missing field:** expected an empty string at the second candidate's slot, not `first` or `third`.

<!-- formula-lint: export -->
```text
SPLIT_INDEX(
    CONCAT("", "~SLOT_BOUNDARY~", "first", "~SLOT_BOUNDARY~", "", "~SLOT_BOUNDARY~", "third"),
    "~SLOT_BOUNDARY~",
    MOD(MAX(MAX(301, 502), 103), 10) + 1
)
```

**Trailing missing field:** expected an empty string at the final candidate's slot.

<!-- formula-lint: export -->
```text
SPLIT_INDEX(
    CONCAT("", "~SLOT_BOUNDARY~", "first", "~SLOT_BOUNDARY~", ""),
    "~SLOT_BOUNDARY~",
    MOD(MAX(301, 502), 10) + 1
)
```

## Coverage and serializer limits

Specify whether the ceiling counts all applications, each allowed GUID's raw occurrences, or only qualifying records. In a per-GUID raw scan, an ineligible occurrence still consumes a slot; unrelated GUIDs do not. A total count below the combined ceiling does not guarantee coverage if one GUID exceeds its individual limit. Make ceiling changes in scores, output slots, bases, and all companion formulas together.

Compact `guid`-first object boundaries are sample-specific, not a universal schema. Bounding one application prevents neighboring-object leakage, but does **not** guarantee top-level-property extraction: nested form data can duplicate `major`, `term`, or another key. Inspect duplicate nested keys, imitated object-start markers, spacing, property order, null/omitted values, and escaped quotes before adopting a string-split extractor.

## Regression and runtime checks

Run the bundled abstract invariant tests after changing the selector design:

```bash
python3 scripts/test_application_selection_invariants.py
```

These tests use fictional candidate records and precomputed numeric term ranks. They check packed-score order against an independent tuple-key selector, blank-slot alignment, and per-GUID coverage. They do not parse application JSON, execute the delivered export formulas, resolve maps, or demonstrate Element runtime behavior.

For actual runtime acceptance, preview at least: no eligible candidates; an invalid first and valid later occurrence; missing classification; equal terms across allowed GUIDs; differing years; documented equivalent term variants; a missing selected output with an older nonblank value; unknown terms under the chosen policy; inactive majors; multi-degree majors; exact coverage and one occurrence beyond it; delimiter/empty-slot behavior; and the current serializer's nested-key risks.

Start with a registration-identity diagnostic when available, then compare all companion columns for the same application. Test the mapping functions and the packed-slot diagnostics separately before evaluating the complete formulas. Preserve the distinction between syntax checks, local abstract tests, Element Evaluate, and actual Preview Export.
