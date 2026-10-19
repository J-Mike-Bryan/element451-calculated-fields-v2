# Root-field selection strategies

## Table of contents

- [Separate filtering from selection](#separate-filtering-from-selection)
- [Ordinal projections and missing values](#ordinal-projections-and-missing-values)
- [Existence and counts](#existence-and-counts)
- [Mapped attribute eligibility inside any-match scans](#mapped-attribute-eligibility-inside-any-match-scans)
- [Latest and earliest scalar values](#latest-and-earliest-scalar-values)
- [Argmax and argmin: return a field from the winning object](#argmax-and-argmin-return-a-field-from-the-winning-object)
- [Companion application exports](#companion-application-exports)
- [Primary-source fallback for term outputs](#primary-source-fallback-for-term-outputs)
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

## Ordinal projections and missing values

For "email from the first/second matching milestone," filter by the requested milestone type, select its ordinal in serialized order, and then extract its email. An object with a missing email still consumes its ordinal slot unless the user explicitly requests the first/second **nonblank** value. Do not reuse a filter-before-selection rule that removes blank outputs when the intended selection unit is the object. This differs from any-match scans, latest-date selection, and deduplicated value lists.

See `root-field-ordinal-exports.md` for complete provisional examples, same-object extraction before/after the type marker, independent label/profile outputs, serializer assumptions, and local fixture checks. Preserve source independence and the requested coverage; do not substitute current profile data for a missing event-level value.

## Existence and counts

For an any-match decision, return `1` for each qualifying object and `0` otherwise, then test the sum:

```text
IF(SUM(candidate_1, candidate_2, candidate_3) > 0, "Y", "N")
```

For a count, return the `SUM(...)` directly. The outer raw-occurrence guard remains mandatory for reconstructed milestone objects. In a user-verified compact milestone-root formula evaluation, one reconstructed Deposit candidate combining exact application, exact term, exact-major exclusion, and timestamp-presence checks with `&` returned numeric `1` when all checks passed and `0` when any one tested rule failed. A separate five-slot occurrence-guard probe returned `0`, `1`, and `2` for records containing zero, one, and two Deposit occurrences respectively. A two-Deposit business-eligibility probe then returned `1`, `1`, `2`, and `0` for invalid/valid, valid/invalid, valid/valid, and invalid/invalid arrangements. Together, these tests verify that guarded numeric candidates aggregate independently through `SUM` and that each reconstructed occurrence can be filtered without borrowing another occurrence's eligibility metadata in that tested context. A separate five-slot coverage probe returned `5` for both exactly five and exactly six Deposit occurrences, user-verifying that the scan includes only the first five target occurrences and intentionally ignores a sixth. A separate reconstructed-object probe with explicit `"term":null` confirmed that exact quoted-term allow-list matching rejects a null required term. The complete five-slot count formula was then user-verified as one assembled expression across eight controlled cases, producing `0`, `1`, `0`, `0`, `1`, `2`, `5`, and `5`, with the user reporting matching results in formula evaluation and actual Preview Export. This promotes that tested count architecture from a design target to user-verified Export behavior for the observed compact serializer shape.

## Mapped attribute eligibility inside any-match scans

A user-reported working Export formula in September 2026 verified another reusable candidate shape on a compact milestone root: enumerate the canonical application-submit milestone type, guard each raw nth occurrence, reconstruct and bound that same milestone object, require one of several exact application identifiers, extract that object's major identifier, map the major through `FIRST(DS_MAP(...))` to a scalar classification attribute, compare the mapped result against a small exact allow-list, and emit numeric `1` or `0`. Aggregating those candidates and testing whether the total is greater than zero produced the requested text boolean. A follow-up version changed only the exact classification allow-list while preserving the reconstruction, mapping, aggregation, and output logic, and was also reported working.

**Inactive-major caveat:** a later September 2026 user-reported runtime test found that a majors data-source lookup could return blank for an inactive major, while `FIRST(DB_MAP("major", <major-guid>, "guid", "degrees", ""))` returned the associated degree code for both active and inactive majors. Therefore, when the scalar classification is a core major attribute such as `degrees` and inactive majors must remain eligible, prefer the database-backed `DB_MAP("major", ...)` pattern. Keep `DS_MAP` for ordinary data-source lookups or when its active-only behavior is acceptable.

Treat the application identifiers, data-source identifier, output column, and allowed classification codes as tenant-specific inputs. The reusable architecture is:

```text
raw occurrence guard
-> bounded current milestone
-> exact application allow-list on that milestone
-> extract that milestone's major GUID
-> map that major GUID to the needed classification:
   - core major attribute such as `degrees`, with inactive majors in scope: `FIRST(DB_MAP("major", major_guid, "guid", "degrees", ""))`
   - ordinary tenant data-source attribute: `FIRST(DS_MAP(major_guid, <major-data-source>, "guid", <classification-column>, ""))`
-> exact mapped-value allow-list
-> 1 or 0
-> SUM(all candidates) > 0
-> requested boolean/text output
```

Do not use the mapped attribute from the whole root field after isolating only the milestone type. The major GUID and the mapped classification must originate from the same bounded occurrence whose application/type conditions are being tested. For a small allow-list, prefer explicit equality joined with `|`; if a compact regex is used, keep it free of Export Preview square-bracket character classes and verify both Evaluate and Preview Export.

### When recency is semantically unnecessary

If the final result is only an existence boolean and **every already-qualifying occurrence leads to the same TRUE result**, choosing the newest term/date among those qualifying occurrences cannot change the answer. In that case, filter each occurrence and perform an any-match aggregation; do not add argmax/latest-term machinery merely because the request mentions which qualifying occurrence is newest.

This is different from **latest-first eligibility**: if the business rule means "find the newest occurrence first, then decide whether that one qualifies," recency can change the boolean and an argmax-style selection is required. Clarify the rule from the requested semantics rather than assuming these two operations are equivalent.

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

### Rank by record index and return an associated name

The user-confirmed school-root Export example is a concrete argmax variant: check a bounded object's canonical `type`, compare nonnegative numeric `index_weight`, attach the **serialized slot ordinal** as a compact-table payload, then extract `name` only from the winning object. This specifically avoids confusing upload order with array order or borrowing a neighboring school's name. The reported sample includes a college with `entry_type=home_schooled` yet `type=college`, so the working discriminator is `type` in that supplied shape. See `references/school-root-index-weight.md` for limits, tie behavior, exact generation commands, and the matching user-confirmed formula architecture; the generator is `scripts/build_linked_index_weight_export.py`. Do not claim the related generic generator variations have been confirmed in Element451.

## Companion application exports

When multiple output columns must describe one application, use `references/application-root-linked-exports.md`. It extends this argmax guidance with a shared selector across columns, no fallback for a missing selected field, term-rank policies, global ties across separately scanned GUIDs, per-GUID coverage, and an optional packed-score/aligned-slot design. These application-specific additions have local abstract tests and static diagnostic checks, not confirmed Element451 runtime results.

## Primary-source fallback for term outputs

For milestone-first application fallback and companion season/year projections, read `references/term-root-fallback.md`. Use source precedence before term recency when that policy is requested, preserve eligible-but-undecodable primary records, and keep both projections on one selector. A bounded scan can establish only that no **scanned** primary candidate qualified.

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
11. Same-object mapped attribute returns one allowed code -> candidate qualifies.
12. Same-object mapped attribute returns a disallowed code or blank map result -> candidate does not qualify.
13. Earlier invalid mapped candidate followed by a later valid candidate -> any-match result still qualifies.
14. If only the mapped-value allow-list changes, re-test at least one newly allowed and one newly disallowed value while preserving all other candidate logic.

## Compact-record alternative for large selectors

When repeated root reconstruction, maps, or blocker scans make a selector very large, read `references/compact-root-pipelines.md`. It documents a user-confirmed assembled export optimization: emit guarded eligible records into a short string, remove invalidated candidates before ranking, then check existence or reduce adjacent pairs while carrying the linked payload. Use current-task policy, mappings, fixed widths, and capacity. Do not replace a ten-raw-slot scan with three raw slots and call that three valid matches. The generalized helper's broader options are locally tested, not independently Element-verified.
