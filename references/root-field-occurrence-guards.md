# Guarding missing root-field occurrences before reconstruction

## Table of contents

- [Why this matters](#why-this-matters)
- [Verified failure pattern](#verified-failure-pattern)
- [Required guard pattern](#required-guard-pattern)
- [Why the guard works](#why-the-guard-works)
- [Reconstruction-specific guidance](#reconstruction-specific-guidance)
- [Candidate architecture](#candidate-architecture)
- [Debugging sequence](#debugging-sequence)
- [Regression tests](#regression-tests)

## Why this matters

When a root-field formula scans for the nth occurrence of a marker that appears **inside** an object, such as a milestone `"type":"WITHDRAW"` or `"type":"DEPOSIT"`, the formula may need to reconstruct the full object because fields such as `name`, `application_guid`, `term`, `major`, or other properties can occur before the marker. When the business rule is defined by milestone `type`, use that canonical type marker for occurrence counting instead of a mutable milestone `name`.

Never reconstruct or inspect an nth matching object until the formula first proves that the nth raw occurrence actually exists.

This is especially important when the formula scans a fixed number of possible matches, such as the first five Withdraw milestones. Later slots will be absent for many records.

## Verified failure pattern

In an anonymized August 2026 `[user-milestones-root]` export case, the formula split on the marker:

```text
"""type"":""WITHDRAW"""
```

It then reconstructed each matching milestone by combining text before the marker, the marker itself, and text after the marker. The formula worked for real Withdraw occurrences, but later candidate slots could still execute the reconstruction even when that nth Withdraw occurrence did not exist.

The observed result was a serious false positive: users with no qualifying Withdraw milestone could receive a date from a neighboring Application or Admit milestone.

The successful fix was to add a short-circuiting existence guard around every candidate **before** any reconstruction or property extraction.

## Required guard pattern

For occurrence index `i`, use this outer shape:

```text
IF(
    SPLIT_INDEX(
        [root-field],
        "<exact target marker>",
        <occurrence index>
    ) = "",
    0,
    <reconstruct, isolate, validate, and extract this occurrence>
)
```

For example, when scanning Withdraw milestones:

```text
IF(
    SPLIT_INDEX(
        [user-milestones-root],
        """type"":""WITHDRAW""",
        2
    ) = "",
    0,
    <candidate for first Withdraw occurrence>
)
```

Use indexes `2`, `3`, `4`, and so on according to the documented one-based `SPLIT_INDEX` behavior. Index `2` is the first content segment after the marker, so it corresponds to the first matching occurrence.

In a September 2026 controlled milestone-root evaluation, a nonexistent second target occurrence returned `""`, and a zero-target record also returned `""` for index `2`. An `IF(SPLIT_INDEX(...) = "", "ABSENT", "EXISTS")` probe returned `ABSENT` in both cases. This directly supports the blank-comparison guard for the tested formula-evaluation context; still verify Preview Export separately when the final formula is an export.

## Why the guard works

The bundled function training documents `IF` as short-circuiting: only the selected branch is evaluated. Therefore, when the nth target occurrence is absent and the `SPLIT_INDEX(...)` existence check is blank, the candidate returns numeric `0` immediately.

The reconstruction branch does not run, so it cannot accidentally combine neighboring root-field text with an inserted target marker and then extract another object's date, application, term, major, or other property.

This guard is stronger than merely checking whether the reconstructed segment is nonblank, because the reconstruction itself can create nonblank synthetic text.

## Reconstruction-specific guidance

Do not pick a `name` marker simply to avoid reconstruction. A manually/import-created milestone can keep the required canonical `type` while using a different name such as `Client Import`. If `type` defines eligibility, keep the type marker and reconstruct around it safely.

A common reconstruction pattern is conceptually:

```text
CONCAT(
    <prefix belonging to the target object>,
    "<target marker>",
    <suffix after the target marker>
)
```

This can be necessary when the marker occurs in the middle of an object. However, it is unsafe to execute unconditionally for every planned candidate slot.

Use this order:

1. Check whether the raw nth marker occurrence exists.
2. Only if it exists, reconstruct the object.
3. Bound the reconstructed text to that same object.
4. Apply application, term, major, status, or other conditions only to that bounded object.
5. Extract the timestamp only from that bounded object.
6. Return numeric `0` when any required condition fails.

Do **not** use this order:

1. Reconstruct the nth object.
2. Assume the reconstruction proves the nth occurrence existed.
3. Search the reconstructed text for a date or other properties.

The reconstruction can synthesize plausible text even when the nth marker was absent.

## Candidate architecture

Use this conceptual candidate shape for latest-date selection:

```text
IF(
    <raw nth target occurrence is absent>,
    0,
    IF(
        <same reconstructed/bounded object satisfies every business rule>,
        IF(
            <timestamp is blank>,
            0,
            VAL(<timestamp>)
        ),
        0
    )
)
```

Then compare the candidates with nested binary `MAX` calls.

The existence guard is separate from the business-rule checks. A candidate should have to pass both layers:

- **Structural validity:** the nth target occurrence really exists.
- **Business validity:** that exact object has the required application/term/type/etc. and does not have excluded values.

## Debugging sequence

When a user reports that a root-field formula returns a date from the wrong object even though the target object is absent:

1. Evaluate the raw root field on the failing record.
2. Confirm the target marker truly occurs zero times or fewer times than the candidate slot that is returning data.
3. Evaluate `SPLIT_INDEX([root-field], <marker>, <index>)` by itself for each candidate index.
4. If an absent index is blank but the full candidate still returns a timestamp, inspect for reconstruction that runs before existence validation.
5. Wrap that candidate in the existence guard.
6. Repeat the guard for every candidate slot, not only the first failing slot.
7. Re-test the user with no target objects and a user with fewer target objects than the formula's maximum coverage.
8. Then re-test valid multi-match users to ensure the `MAX` logic still selects the latest date.

## Regression tests

Always include these cases for reconstruction-based root-field formulas:

| Case | Expected result |
|---|---|
| Zero target-marker occurrences, but neighboring objects contain valid-looking dates | Blank / no candidate |
| One real target occurrence while formula scans five | Only candidate 1 can qualify; candidates 2-5 must be `0` |
| Two real target occurrences while formula scans five | Candidates 3-5 must be `0` |
| Target object exists under an alternate/manual/imported name but has the required canonical `type` | It is still scanned and can qualify |
| Target object exists but application/term/status rule fails | That candidate is `0` |
| Target object has exact excluded optional value | That candidate is `0` |
| Target object omits an optional value that is allowed to be missing | Candidate can still qualify |
| Multiple valid target objects in nonchronological serialized order | Numeric `MAX` returns the newest timestamp |
| No valid candidates at all | Final output is an empty string, never another object's date |

Treat the zero-target case as mandatory. It specifically catches neighboring-object leakage that ordinary valid-record testing can miss.
