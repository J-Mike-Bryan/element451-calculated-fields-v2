# Root-field selection strategies

## Table of contents

- [Separate filtering from selection](#separate-filtering-from-selection)
- [Existence and counts](#existence-and-counts)
- [Latest and earliest scalar values](#latest-and-earliest-scalar-values)
- [Argmax and argmin: return a field from the winning object](#argmax-and-argmin-return-a-field-from-the-winning-object)
- [Threshold windows](#threshold-windows)
- [Tie-breaking](#tie-breaking)
- [Candidate sentinels](#candidate-sentinels)
- [Coverage and complexity](#coverage-and-complexity)
- [Required tests](#required-tests)

## Separate filtering from selection

For every planned occurrence, build one candidate from the same bounded object:

```text
raw occurrence exists
-> isolate or reconstruct this object
-> apply every eligibility rule to this object
-> extract candidate sort key and/or associated output
-> otherwise return the invalid sentinel
```

Only after every candidate is independently valid should the formula combine them.

### Application-root transfer from verified milestone parsing

The milestone-root tests established several safeguards that are also applicable to `[user-applications-root]` whenever applications are scanned by repeated text markers:

- Guard the raw nth target application occurrence before deeper extraction. A fixed scan can have absent later slots just like a milestone scan.
- Bound each target application object before testing `major`, `term`, status, timestamps, or other metadata. Do not let a neighboring application satisfy the current candidate.
- Test independent properties against the same bounded application object rather than relying on fragile property order.
- If the business rule excludes only one exact optional value, reject only that exact marker; explicit `null` or an omitted property should not be rejected merely for being blank unless the rule requires the property.
- If a property such as `term` is required, an explicit `null` or absent exact allowed marker should make that candidate invalid.
- Continue scanning after an invalid earlier occurrence; a later occurrence of the same application GUID can still qualify.
- State the fixed occurrence ceiling and test one record beyond it.

These are **transferable parsing/selection safeguards**, not proof that the application serializer has the same object-start marker or key order as the verified milestone serializer. Derive the application marker and next-object boundary from a current `[user-applications-root]` sample.

## Existence and counts

For an any-match decision, return `1` for each qualifying object and `0` otherwise, then test the sum:

```text
IF(SUM(candidate_1, candidate_2, candidate_3) > 0, "Y", "N")
```

For a count, return the `SUM(...)` directly. The outer raw-occurrence guard remains mandatory for reconstructed milestone objects. In a user-verified compact milestone-root formula evaluation, one reconstructed Deposit candidate combining exact application, exact term, exact-major exclusion, and timestamp-presence checks with `&` returned numeric `1` when all checks passed and `0` when any one tested rule failed. A separate five-slot occurrence-guard probe returned `0`, `1`, and `2` for records containing zero, one, and two Deposit occurrences respectively. A two-Deposit business-eligibility probe then returned `1`, `1`, `2`, and `0` for invalid/valid, valid/invalid, valid/valid, and invalid/invalid arrangements. Together, these tests verify that guarded numeric candidates aggregate independently through `SUM` and that each reconstructed occurrence can be filtered without borrowing another occurrence's eligibility metadata in that tested context. A separate five-slot coverage probe returned `5` for both exactly five and exactly six Deposit occurrences, user-verifying that the scan includes only the first five target occurrences and intentionally ignores a sixth. A separate reconstructed-object probe with explicit `"term":null` confirmed that exact quoted-term allow-list matching rejects a null required term. The complete five-slot count formula was then user-verified as one assembled expression across eight controlled cases, producing `0`, `1`, `0`, `0`, `1`, `2`, `5`, and `5`, with the user reporting matching results in formula evaluation and actual Preview Export. This promotes that tested count architecture from a design target to user-verified Export behavior for the observed compact serializer shape.

## Latest and earliest scalar values

For latest timestamps:

- valid candidate -> numeric millisecond timestamp;
- invalid candidate -> numeric `0`;
- selection -> nested binary `MAX`;
- no match -> selected value equals `0`.

For earliest positive timestamps, zero cannot be the invalid value because it would always win. Use a sentinel larger than every real candidate, such as a verified maximum epoch-millisecond bound, then nested binary `MIN` and an explicit sentinel cleanup.

Keep millisecond precision through `MAX`/`MIN`. Convert only the winning value with `FLOOR(ms / 1000)` before `DATE_READ(..., "U")`.

## Argmax and argmin: return a field from the winning object

Sometimes the request is not “return the latest timestamp” but “return the **term, major, status, or other field attached to the latest matching object**.” This is an argmax/argmin problem.

For each occurrence, define conceptually:

```text
sort_key_i = qualifying timestamp or invalid sentinel
value_i = associated field extracted from the same bounded object
```

Then select the associated value with pairwise comparisons of the sort keys. For three latest candidates with an earliest-occurrence tie policy:

```text
IF(
    MAX(MAX(key_1, key_2), key_3) = 0,
    "",
    IF(
        (key_1 >= key_2) & (key_1 >= key_3),
        value_1,
        IF(key_2 >= key_3, value_2, value_3)
    )
)
```

In real Element syntax, each conceptual key/value expression must be expanded completely because the formula language does not provide local variables. Never extract `value_i` from the whole root after selecting a date; that can return a value from a different object.

Do not treat an untested application argmax formula as established behavior. Build and test the per-application sort keys and associated values incrementally from the current `[user-applications-root]` serializer. The guarded latest-application date example in `references/root-field-example-latest-application.md` demonstrates safe occurrence guards, object bounding, exact exclusion, numeric timestamp selection, and final date conversion; extend the same-object pairing carefully when the desired output is an associated term or other field.

## Threshold windows

Apply thresholds inside each candidate before selection:

- latest on/before cutoff: candidate timestamp must be `<= cutoff`;
- earliest on/after cutoff: candidate timestamp must be `>= cutoff`;
- within range: both comparisons must hold;
- nearest before/after: build separate latest-before and earliest-after selections.

Convert the cutoff into the same numeric unit as the candidate. Do not compare a 13-digit millisecond value to 10-digit epoch seconds.

## Tie-breaking

State the tie rule. Pairwise `>=` comparisons give the earlier serialized occurrence priority; `>` allows a later branch to win equal timestamps. Other possible tie rules include:

- highest or lowest index;
- a second numeric field;
- a status priority;
- nonblank associated value;
- latest secondary timestamp.

A deterministic tie policy is required even when equal timestamps seem unlikely.

## Candidate sentinels

| Selection | Valid candidate | Invalid candidate | No-match test |
|---|---|---|---|
| Any/count | `1` | `0` | `SUM(...) = 0` |
| Latest positive timestamp | milliseconds | `0` | `MAX(...) = 0` |
| Earliest positive timestamp | milliseconds | large upper sentinel | `MIN(...) = sentinel` |
| Highest score where negatives are valid | score | smaller verified lower sentinel | selected equals sentinel |
| Lowest score where negatives are valid | score | larger verified upper sentinel | selected equals sentinel |

Choose sentinels from the true data domain. A sentinel that can be a legitimate value makes no-match detection ambiguous.

## Coverage and complexity

State the maximum number of target occurrences covered. Search by the most specific stable marker so unrelated objects do not consume slots. Use `scripts/build_occurrence_scan.py` to expand an indexed candidate template and `scripts/build_binary_tree.py` to build balanced `MAX`/`MIN` trees.

Generated repetition reduces copy errors but does not prove:

- the marker identifies the right object;
- the delimiter bounds the object;
- key order is stable;
- the target occurrence exists;
- the destination representation is correct; or
- Element supports the resulting formula length.

## Required tests

1. Zero target occurrences with plausible neighboring data.
2. Fewer occurrences than planned slots.
3. One and multiple valid occurrences.
4. Invalid first occurrence followed by a valid later occurrence.
5. Multiple valid objects out of chronological order.
6. Equal sort keys to verify the tie policy.
7. Missing associated value on the winning object.
8. Exact excluded value, different value, and omitted optional value.
9. Threshold equality and one unit on either side.
10. Maximum coverage and one occurrence beyond coverage.
