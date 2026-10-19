# Ordinal milestone field exports and independent source columns

## Table of contents

- [Evidence status](#evidence-status)
- [Choose the selection unit](#choose-the-selection-unit)
- [Keep sources independent](#keep-sources-independent)
- [Require the actual serialized shape](#require-the-actual-serialized-shape)
- [Build a guarded ordinal projection](#build-a-guarded-ordinal-projection)
- [Provisional complete examples](#provisional-complete-examples)
- [Expected checks](#expected-checks)
- [Local regression and runtime validation](#local-regression-and-runtime-validation)

## Evidence status

Treat the email-specific formulas below as **provisional, static-lint-clean design examples with local fixture-model checks**, not user-verified Element451 results. No raw milestone-root sample or user-reported Evaluate/Preview Export output accompanied the request that motivated this addition. A request to add lessons does not confirm that the prior formulas worked. Do not promote inherited assistant test claims into observed evidence.

Retain the existing, separately scoped evidence for canonical-type enumeration, missing-occurrence guards, compact-object reconstruction, and label membership in `root-field-parsing.md`, `root-field-occurrence-guards.md`, and `formula-patterns.md`. Those observations do not prove this new email projection works with another serializer or export configuration. Read `official-docs.md` and verify current official documentation when making current product claims.

## Choose the selection unit

Identify what is being counted before writing the formula:

| Requested output | Selection rule |
|---|---|
| Field from the nth milestone of a type | Select the nth type-matching object, then project the field; preserve a blank field. |
| Nth nonblank field value | Filter objects by type and nonblank field, then select the nth remaining value. |
| Nth unique value | Establish normalization and duplicate rules, deduplicate, and then select. |
| Field from the oldest/newest milestone | Rank eligible objects by numeric date and keep the field paired with the winner. |

For ordinal milestone columns, interpret "first" and "second" as serialized order only when no chronological order was requested, and state that assumption. Do not assert that root order equals creation order, event-date order, or the UI display order. Do not assume a column's First/Last setting sorts the serialized root.

A missing email still consumes its milestone slot. If milestone 2 lacks email and milestone 3 has it, column 2 must stay blank when the rule targets milestone 2. If milestone 1 lacks email but milestone 2 has it, retain blank/email across the two columns. Do not silently compact the list.

State capacity: two ordinal milestone columns cover only the first two type matches, not all matching milestones or all distinct email addresses. Unrelated milestone types do not consume those slots. Preserve duplicates unless the current request explicitly asks to remove them.

## Keep sources independent

When a request defines one label-derived profile column and separate milestone-derived columns, implement each condition independently. Do not gate milestone columns on label presence, and do not require a milestone before returning the label-derived value unless an explicit AND rule was requested.

For the label column, use the exact current-task label identifier and the verified primary-email field token from the current field picker or source. Reuse the label-membership guidance in `formula-patterns.md`; do not invent a label, copy a tenant identifier from memory, or assume a broad substring regex is exact-boundary membership. The membership pattern already has separate historical evidence; this task did not add a new live label test.

For a milestone column, return that milestone's `email`, not the current primary email. Never fill a missing milestone email with the primary email, another profile email, or a neighboring milestone unless the user requests that fallback. The event's associated value and the current profile value are distinct sources and can differ. A label-derived value may duplicate a milestone-derived value; do not suppress that duplicate without a requested deduplication rule.

Treat these as data-extraction rules, not a proof of current email-suppression behavior. Do not infer that a label alone changes sending permissions, that a blank-email milestone applies to every address, or that historical unsubscribe milestones settle current eligibility after later subscription changes. Investigate current sending/subscription semantics separately when asked.

## Require the actual serialized shape

Obtain a redacted `[user-milestones-root]` value before calling any exact-string parser production-ready. A user saying "object of email" establishes a requested property name, not whether the value is a string, null, nested object, or array. Distinguish those shapes explicitly.

The examples below assume all of the following:

- Compact, single-line JSON-like root text with exact markers such as `"type":"UNSUBSCRIBE_EMAIL"`; no spaces around these separators.
- Every milestone starts with `"name":`, and the boundary between adjacent milestone objects is `},{"name":`.
- The requested `email` is a top-level string property, absent, or null. Blank and surrounding ASCII whitespace are handled under the modeled text behavior.
- Relevant marker names are not repeated inside nested objects in ways that confuse the prefix or email lookup. Each object has a single canonical `type`.
- Ordinary email strings need no JSON escape decoding. These split expressions are not a general JSON parser: escaped quotes, backslashes, Unicode escapes, nested values, and arrays require a shape-specific solution.

The email can be before or after `type` **within that assumed name-first shape**. Do not call the parser universally property-order-independent: moving `name`, adding nested `name`/`email` properties, pretty-printing the root, or changing object boundaries can invalidate it.

If the current sample is unavailable, supply only a clearly labeled assumption-based draft/diagnostic, or request the minimal redacted root sample. Never manufacture serializer evidence. A changed shape requires re-deriving the parser, not merely rerunning its linter.

## Build a guarded ordinal projection

Use the bounded-object architecture in `root-field-parsing.md`:

1. Enumerate by the exact canonical type marker, not the display/source name.
2. For ordinal n, inspect `SPLIT_INDEX(root, marker, n + 1)` first. If it is blank, return `""` before reconstructing any object.
3. Recover the current object's prefix from segment n using its actual object-start marker. Bound the suffix from segment n + 1 before the next milestone.
4. Concatenate the prefix, type marker, and bounded suffix into a property slice for the same occurrence. The slice need not itself be valid standalone JSON; use it only for the defined extraction.
5. Extract `email` from that slice. Under the assumed compact scalar shape and modeled missing-split behavior, an absent property, null, or empty string yields `""`; apply `TRIM` to a string result.
6. Return the projection without searching another object when it is blank.

Keep all linked indexes aligned: ordinal 1 uses prefix 1 and guarded suffix 2; ordinal 2 uses prefix 2 and guarded suffix 3. Change every linked index together when adding a column.

Do not use `REGEXP_EXTRACT_NTH(..., n)` as though n selected the nth milestone or nth regex match. The bundled training describes n as a **capture-group index**. Enumerate actual occurrences using a supported, verified method such as the guarded splits above.

## Provisional complete examples

These examples contain no institution-specific identifiers. Confirm the root token and all serialization assumptions before use. Do not broaden them to nth nonblank/unique output without changing and testing the selection rule.

### First type-matching milestone's email

<!-- formula-lint: export -->
```text
IF(
    SPLIT_INDEX(
        [user-milestones-root],
        """type"":""UNSUBSCRIBE_EMAIL""",
        2
    ) = "",
    "",
    TRIM(
        SPLIT_INDEX(
            SPLIT_INDEX(
                CONCAT(
                    REGEXP_EXTRACT(
                        SPLIT_INDEX(
                            [user-milestones-root],
                            """type"":""UNSUBSCRIBE_EMAIL""",
                            1
                        ),
                        ".*(""name"":.*)$"
                    ),
                    """type"":""UNSUBSCRIBE_EMAIL""",
                    SPLIT_INDEX(
                        SPLIT_INDEX(
                            [user-milestones-root],
                            """type"":""UNSUBSCRIBE_EMAIL""",
                            2
                        ),
                        "},{""name"":",
                        1
                    )
                ),
                """email"":""",
                2
            ),
            """",
            1
        )
    )
)
```

### Second type-matching milestone's email

<!-- formula-lint: export -->
```text
IF(
    SPLIT_INDEX(
        [user-milestones-root],
        """type"":""UNSUBSCRIBE_EMAIL""",
        3
    ) = "",
    "",
    TRIM(
        SPLIT_INDEX(
            SPLIT_INDEX(
                CONCAT(
                    REGEXP_EXTRACT(
                        SPLIT_INDEX(
                            [user-milestones-root],
                            """type"":""UNSUBSCRIBE_EMAIL""",
                            2
                        ),
                        ".*(""name"":.*)$"
                    ),
                    """type"":""UNSUBSCRIBE_EMAIL""",
                    SPLIT_INDEX(
                        SPLIT_INDEX(
                            [user-milestones-root],
                            """type"":""UNSUBSCRIBE_EMAIL""",
                            3
                        ),
                        "},{""name"":",
                        1
                    )
                ),
                """email"":""",
                2
            ),
            """",
            1
        )
    )
)
```

## Expected checks

Use fictional addresses such as `first@example.test` and `second@example.test` in local fixtures; use minimal redacted records for tenant diagnostics.

| Case | First column | Second column |
|---|---|---|
| No target type, even with other milestones containing emails | Blank | Blank |
| One target with email | Its email | Blank |
| Two targets with emails | First target's email | Second target's email |
| First target's email omitted/null/blank | Blank | Second target's email, if present |
| Second target's email omitted/null/blank; third has email | First target's email | Blank |
| Other milestone types between targets | First target's email | Second target's email |
| Alternate source/display names with the same target type | Same results | Same results |
| Email before type on one target and after type on the other | Same results | Same results |
| Identical emails on both targets | Same email | Same email |
| Event dates disagree with serialized order | Serialized first | Serialized second |
| Label absent but milestone email present | Milestone output unaffected | Milestone output unaffected |
| Label present but no target milestones | Blank milestone output | Blank milestone output |

Also check zero/one target with plausible neighboring emails, unrelated property names such as `backup_email`, raw blank root input, whitespace-only email, and exactly two versus three targets. A record beyond capacity must demonstrate the declared limit rather than suggest all emails were captured.

## Local regression and runtime validation

Run:

```bash
python3 scripts/test_ordinal_email_exports.py
python3 scripts/lint_reference_formulas.py references/root-field-ordinal-exports.md
```

Also run each complete example through `formula_lint.py --strict-functions --export` and `format_formula.py` before delivery. The Python fixture test models only the documented string-operation architecture and selection semantics; it does not execute the Element formula language, validate live field tokens, emulate label membership, or call Element451. Its JSON oracle is a local test aid, not a function offered to formula authors.

Treat pretty-printed JSON, changed object-start order, nested `email` values, repeated nested markers, and JSON-escaped email characters as outside the fixture contract. Obtain real samples and adapt/retest rather than treating a local success on compact fixtures as portability evidence.

In Element, evaluate the raw root, guarded occurrence suffix, bounded property slice, and extracted email on known records. Then test the full expressions in both Evaluate and Preview Export, including missing-slot and nonmatching-neighbor cases. Record exact results and execution surfaces before promoting this email-specific pattern to user-verified status.
