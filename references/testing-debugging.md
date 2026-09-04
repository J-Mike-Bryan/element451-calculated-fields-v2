# Testing and debugging Element451 formulas

## Table of contents

- [Validation layers](#validation-layers)
- [Static checks](#static-checks)
- [Element451 Evaluate preview](#element451-evaluate-preview)
- [Preview Export compiler differences](#preview-export-compiler-differences)
- [Workflow/Rule persistence validation](#workflowrule-persistence-validation)
- [Calculated-payment validation](#calculated-payment-validation)
- [Reference-formula regression linting](#reference-formula-regression-linting)
- [Incremental debugging workflow](#incremental-debugging-workflow)
- [Syntax checklist](#syntax-checklist)
- [Type checklist](#type-checklist)
- [Date checklist](#date-checklist)
- [Mapping checklist](#mapping-checklist)
- [Regex checklist](#regex-checklist)
- [Root-field checklist](#root-field-checklist)
- [Common symptoms and likely causes](#common-symptoms-and-likely-causes)
- [Test-case template](#test-case-template)

## Validation layers

Use all applicable layers:

1. **Source validation:** Confirm field slugs, column numbers, GUIDs, data-source IDs, sample values, and business rules.
2. **Static structure:** Check quotes, parentheses, brackets, function names, argument counts, and placeholders.
3. **Component evaluation:** Evaluate small extraction or conversion expressions separately.
4. **Integrated evaluation:** Evaluate the complete formula against representative contacts.
5. **Output validation:** Confirm the target field or payment context accepts the returned type and identifier form.
6. **Operation validation:** For Workflow/Rule Formula Fields, confirm the value actually persists; for calculated payments, confirm the numeric amount used by the payment flow; for exports, confirm Preview Export.
7. **Regression validation:** Re-test earlier working cases after every edit.

A formula that parses successfully can still be semantically wrong. A formula that works for one contact can still fail on blanks, missing optional properties, multiple matches, or timezone boundaries.

## Static checks

### Lint

```bash
python3 scripts/formula_lint.py formula.txt
```

Useful options:

```bash
python3 scripts/formula_lint.py formula.txt --strict-functions
python3 scripts/formula_lint.py formula.txt --strict-functions --export
python3 scripts/formula_lint.py formula.txt --json
```

The linter checks:

- balanced parentheses and field brackets,
- closed string literals with doubled-quote handling,
- smart quotes and nonbreaking spaces,
- the `REGEX_REPLACE` typo,
- unresolved placeholders,
- common documented function arities,
- fixed EST/EDT offsets that need review,
- token-like bracket sequences inside quoted strings; with `--export`, these are errors because Preview Export may misread them as field tokens.

The linter does not execute the formula or prove Element451 supports a function in the current release.

### Format

```bash
python3 scripts/format_formula.py formula.txt -o formatted.txt
```

Use `--compact` for one normalized line. The formatter preserves characters inside strings, which is essential for regex and serialized JSON markers.

### Build nested MAX or MIN

```bash
python3 scripts/build_binary_tree.py --function MAX --file candidates.txt --pretty
```

Use this when the source signature permits only two arguments.

## Element451 Evaluate preview

The current official calculated-fields article describes an Evaluate preview for export formulas. After adding a formula, select a contact and use the blue **Evaluate** button; Element displays the evaluated formula in the preview area.

Treat Evaluate as the runtime source of truth for formula evaluation details such as:

- boolean return form,
- blank/null handling,
- date timezone behavior,
- split indexing,
- regex behavior,
- map results,
- checkbox ordering,
- unsupported or changed functions.

For exports, do **not** treat Evaluate/Test Formula as proof that Preview Export will accept the formula. Preview Export has a separate token-validation/compiler layer. Always run both. Do not test only with the contact that originally motivated the formula.

## Preview Export compiler differences

Element support confirmed in August 2026 that Preview Export may interpret bracketed text inside quoted strings as field tokens. This means a formula can work perfectly in Test Formula and still fail Preview Export with an error such as:

```text
Expression have undefined tokens
```

A concrete failure pattern is a regex character class inside a string:

```text
"^client[.]terms[.](100|200)$"
```

Although `[.]` is regex syntax, Preview Export can treat it as a field-token candidate. Apply these rules to export formulas:

1. Scan the **entire formula**, including quoted strings, for `[...]`.
2. Keep only legitimate Element field references in brackets.
3. Rewrite regex character classes without square brackets where possible.
4. Do not automatically substitute `\.` for `[.]`; verify the rewritten regex separately because Element's string/regex transport can differ between contexts.
5. Re-run Preview Export after every regex/token rewrite.
6. Run `scripts/formula_lint.py ... --export` so bracketed text inside quoted strings is flagged before paste.

If Test Formula succeeds and Preview Export alone fails, investigate tokenization before changing otherwise-correct application logic.

## Workflow/Rule persistence validation

Treat formula evaluation and field persistence as separate stages:

1. Test the formula on a representative person and record the evaluated output.
2. Confirm the destination field's type and backing data source.
3. Confirm the returned representation is one the field accepts: GUID, value, code, text, number, or date as applicable.
4. Run the Rule/Workflow action in a controlled test.
5. Re-open or re-read the person's profile and verify the value was actually saved.
6. If Evaluate is correct but the profile remains blank, debug destination compatibility before rewriting working formula logic.

A fixed system field may accept only its locked options even when Field Management appears to show another source. Use a custom field backed by an appropriate custom data source when the required output is outside a system field's accepted domain.

## Calculated-payment validation

Test pricing formulas with a matrix that includes:

- blank input;
- zero and negative input;
- smallest ordinary value;
- exact discount threshold and one unit on either side;
- fractional quantity if the form permits it;
- maximum expected value;
- unexpected option text; and
- a person missing one referenced field.

Every branch should return a number. Confirm the evaluated numeric output is the amount actually presented/charged in the controlled payment flow.

## Reference-formula regression linting

When editing bundled examples, annotate each complete formula fence with:

```text
<!-- formula-lint: standard -->
```

or:

```text
<!-- formula-lint: export -->
```

Then run:

```bash
python3 scripts/lint_reference_formulas.py references/source-formula-examples.md
```

This prevents a documentation edit from silently introducing unbalanced syntax, unknown functions, arity problems, or export-preview bracket tokens. Warnings still require judgment; static linting never substitutes for Element runtime testing.

## Incremental debugging workflow

For a long formula, avoid changing the whole expression at once.

1. **Return the raw source field.** Confirm the expected data is present.
2. **Return one isolated segment.** Confirm object or delimiter boundaries.
3. **Return the exact property text.** Confirm quote escaping and property spelling.
4. **Return the extracted raw value.** Do not parse or format yet.
5. **Return the numeric conversion.** Confirm milliseconds versus seconds.
6. **Return one candidate expression.** Test valid, excluded, missing, and blank cases.
7. **Combine two candidates.** Confirm `MAX`/`MIN` selection.
8. **Expand to all occurrences.** Generate or count the binary tree.
9. **Convert the selected value to a date.** Test epoch behavior.
10. **Apply timezone and final format.** Test boundary records.
11. **Add no-match cleanup.** Confirm blank rather than a sentinel date.
12. **Run actual Preview Export.** If only Preview fails, inspect token-like bracket syntax inside strings before changing working logic.

When debugging a production formula, save the last known working version before each step.

## Syntax checklist

- Use straight ASCII double quotes, not typographic quotes.
- Double embedded double quotes inside a string.
- Match every `(` with `)` and every `[` with `]`.
- Separate every function argument with a comma.
- Do not pass more than two arguments to `MAX` or `MIN` when following the bundled training signature.
- Use `REGEXP_REPLACE`, not `REGEX_REPLACE`.
- Replace `[C#]`, `[Column#]`, `<placeholder>`, and template GUIDs.
- Preserve exact field slugs even when their spelling looks unusual.
- Remove copied labels such as `Formula:` from the code fence.
- Ensure regex backslashes survive the transport into Element.

## Type checklist

- Compare text to quoted text and numbers to unquoted numbers.
- Convert timestamp strings with `VAL` or `NUM` before numeric `MAX`.
- Return numeric `0`, not string `"0"`, for invalid numeric candidates.
- Return GUIDs to fields that expect GUIDs; return names/codes only when the target expects them.
- Confirm whether booleans are real `TRUE`/`FALSE` or text in the current context.
- Keep all branches of a conditional compatible with the target field type.
- For calculated payments, keep every branch numeric.
- For Workflow/Rule writes, verify both evaluated output and persisted destination value.
- Do not use a boolean-returning helper directly as an `IF` condition unless its return type has been proven in that context. If Evaluate shows a boolean/text discrepancy, compare explicitly to `TRUE` or `"TRUE"`.
- Preserve leading zeros as text when they are identifiers rather than quantities.

## Date checklist

- Identify the exact input format before `DATE_READ`.
- In Import Preview, do not assume a `[C#]` value that visibly contains `Y-m-d H:i:s` will retain the time portion inside date functions. A user-verified probe returned midnight after `DATE_READ` and showed midnight-like behavior even when the raw `[C1]` was passed directly to `DATE_COMPARE`. If second-level precision matters, first echo the raw value, round-trip it through the intended date path, and compare against exact boundaries. Prefer an epoch-based harness when the production input is epoch-based.
- Do **not** treat successful `DATE_READ` output as proof that the source date was valid. User-verified Import Preview behavior shows rollover normalization: `02/29/2025` parsed as March 1, 2025, and an input reconstructed as year 2026/month 13/day 40 parsed into February 2027. When strict validity matters, canonicalize the source components, parse them, format the parsed date back to the same canonical representation, and require an exact round-trip match.
- Determine whether epoch values are milliseconds or seconds.
- Use `FLOOR(milliseconds / 1000)` or another explicit conversion. Never pass fractional epoch seconds to `DATE_READ(..., "U")`; this has produced implausible years and incorrect months in a verified root-field case. User-verified Import Preview boundary tests show that integer epoch seconds parsed with `DATE_READ(..., "U")` can preserve exact second-level time across DST transition instants.
- Confirm the timezone of the raw timestamp and Element's parser.
- Do not call a fixed UTC-5 offset year-round Eastern Time.
- Test timestamps near midnight.
- Guard missing timestamps before conversion.
- Confirm `m/d/Y` versus `Y-m-d` and four-digit `Y` versus two-digit `y`.
- If a result is always July or has implausible years, inspect the raw numeric value before any date function.

## Mapping checklist

For every `DB_MAP`, `DS_MAP`, or `TAXONOMY_MAP`, write down:

| Item | Value |
|---|---|
| Input value | What the formula receives |
| Collection/data source | Exact type or ID |
| Match key | Key that contains the input |
| Output key | Key to return |
| Default | Blank or explicit diagnostic value |

During debugging, use a visible default such as `"NO_MATCH"` rather than `""`. Restore the intended blank/default after the map is proven.

Treat tenant GUIDs as opaque. If a formula turns a selected term GUID into a semester/year/date, verify the exact GUID -> code/name mapping before hard-coding the output. Do not infer mappings from GUID order, suffixes, or another formula. Local simulations must use the verified mapping fixture; otherwise they can falsely "pass" with the wrong semester/year.

Do not assume a dropdown's displayed label is the stored value. Data-source UI labels may map to database columns such as `column_1` and `column_3`.

## Regex checklist

- Confirm whether the function matches the entire string.
- For export formulas, avoid square-bracket character classes such as `[.]`, `[a-z]`, and `[0-9]` inside regex strings; Preview Export may tokenize them as fields.
- Do not assume `\.` is a safe replacement for `[.]`; test the new pattern by itself and then in Preview Export.
- Add `.*` only when substring matching is intended.
- Put the desired output in a capture group for `REGEXP_EXTRACT`.
- Escape `?`, `.`, `+`, slash, and backslash only as verified by the formula string and regex engine. A syntactically familiar escape can behave differently after Element parses the formula string.
- Do not copy slash delimiters from another language without verifying Element's syntax. Unescaped `/` inside a `REGEXP_REPLACE` pattern can produce errors such as `preg_replace(): Unknown modifier '3'`.
- Anchor exact sentinel matches with `^` and `$`.
- Test strings containing delimiters, empty strings, and near-matches.
- Remember that `CONTAINS` is simpler than regex but is not token-aware.

## Root-field checklist

- Obtain a real redacted sample.
- Choose the occurrence marker from the canonical discriminator that defines the business rule. For milestone rules defined by `type`, enumerate exact `type` occurrences rather than display/source `name` values that may change for manual/import creation paths.
- Test the same canonical type under at least one alternate/manual/imported name when such creation paths exist.
- Confirm compact versus spaced JSON serialization.
- Isolate one object before applying all conditions.
- When the canonical marker sits inside the object, reconstruct or bound the full current object before eligibility checks unless property locations are proven invariant.
- Test required properties independently when practical; do not make eligibility depend on `application.*term` or another property sequence unless that order is verified.
- When scanning nth occurrences that may be absent, prove each raw nth occurrence exists **before** reconstruction or property extraction; return `0` immediately when absent.
- Test zero target occurrences and fewer target occurrences than the formula's maximum candidate slots so neighboring objects cannot leak into synthetic reconstructed candidates.
- Test the same qualifying object with required properties reordered, and test multiple same-type objects where one has null/missing metadata and another qualifies.
- Confirm occurrence indexes start at `2` after splitting on a marker.
- Cover enough occurrences for real records.
- Reject only the exact excluded value when missing values should remain valid.
- Convert every valid timestamp to a number; return `0` for invalid candidates.
- Use a balanced binary `MAX` tree for latest.
- Test a record where the first match is newer than the last match.
- Document property-order or delimiter assumptions.
- Guard the all-zero no-match result.
- For small exact allow-lists, prefer explicit equality/OR checks. If using `CONTAINS` or another boolean helper, verify and explicitly handle its boolean representation before trusting it inside `IF`.
- For exports, verify both Test Formula and Preview Export.

## Common symptoms and likely causes

| Symptom | Likely causes | First diagnostic step |
|---|---|---|
| Formula parser error | Smart quote, missing comma, unbalanced parenthesis, broken embedded quote | Run linter; inspect the first reported location and nearby nested call |
| Blank for every record | Wrong field slug, marker mismatch, mutable name used instead of canonical type, map direction, quoted/unquoted mismatch | Return the raw field; count the canonical type marker; expose a visible map default |
| Correct for one record only | Missing blank handling, optional property, occurrence limit, order assumption | Build a test matrix across edge cases |
| Automatic milestones match but manual/imported milestones do not | Mutable name marker, prefix-only validation, ordered property regex, or source-specific null/extra metadata | Reconstruct one manual/import object; test type/application/term/major independently |
| Returns an Application/Admit/other-object date when the target milestone/object is absent | Reconstruction runs for a nonexistent nth target occurrence and borrows neighboring-object text | Evaluate `SPLIT_INDEX([root], marker, index)` alone; add an outer existence guard before reconstruction for every candidate slot |
| Returns first matching date | Only first occurrence inspected or no numeric `MAX` | Evaluate each candidate and the final `MAX` separately |
| Returns `12/31/1969` | Zero epoch plus timezone offset | Guard zero before date conversion |
| Random year or fixed July | Wrong substring or milliseconds parsed as seconds | Return the extracted numeric timestamp |
| Wrong local date | Fixed offset, double offset, server timezone assumption | Compare raw UTC and Evaluate result for a boundary record |
| Missing-major match excluded | Formula requires a major instead of rejecting only one exact major | Test exact excluded marker presence |
| `MAX` parser error | More than two arguments or mismatched tree parentheses | Generate balanced tree with script |
| Test Formula works but Preview Export says undefined tokens | Regex/string contains token-like brackets such as `[.]`; preview compiler differs from evaluator | Run linter with `--export`; remove bracket classes inside strings |
| Allowed-term filter accepts every term | Boolean membership helper coerced unexpectedly, term extraction not scoped, or substring membership too broad | Return one raw term; test exact equality; expand to OR list |
| Escaped-dot regex makes every match blank | `\.` rewrite not interpreted as expected in Element's formula/regex pipeline | Test regex alone; use explicit equality or a preview-safe verified pattern |
| Correct milestone selected but term-derived date/name is wrong | Tenant GUID mapping was guessed or stale | Return the raw selected GUID; verify GUID -> code/name before formatting |
| Map returns default | Wrong match/output direction or wrong data-source column | Expose input and use `"NO_MATCH"` |
| Label import partially works | Spaces, blank components, names not mapped to GUIDs | Evaluate the exact comma-separated output |
| Name capitalization damages values | Formula handles only one/two parts or ignores apostrophes/hyphens | Define supported name shapes before expanding logic |

## Test-case template

Use a small table in the response for complex formulas:

| Case | Input characteristics | Expected output |
|---|---|---|
| Baseline | One valid value | Exact transformed value |
| Alternate milestone name | Same required canonical `type`, different manual/imported `name` | Same eligibility/result as equivalent named milestone |
| Verified GUID mapping | Selected tenant GUID with known code/name | Correct semantic/date output |
| Blank | Source missing | `""` or stated fallback |
| Excluded | Exact excluded GUID/value | Ignored or alternate result |
| Missing optional property | Property omitted | Included or excluded according to rule |
| Multiple | Older and newer valid values | Latest/earliest according to rule |
| Boundary | Date near midnight or threshold | Correct side of rule |

For each case, distinguish a logically expected result from a result actually verified in Element. Do not claim runtime verification unless Evaluate or user feedback confirms it.
