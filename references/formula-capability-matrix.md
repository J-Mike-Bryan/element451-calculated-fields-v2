# Formula capability and uncertainty matrix

## Table of contents

- [Purpose](#purpose)
- [Coverage matrix](#coverage-matrix)
- [Confidence labels](#confidence-labels)
- [Known knowledge frontiers](#known-knowledge-frontiers)
- [How to record test feedback](#how-to-record-test-feedback)

## Purpose

Use this matrix to decide whether the skill already has a stable pattern, needs tenant data, or should propose an isolated test formula before producing a production formula. “All-encompassing” means covering every source-supported construction category while making uncertainty visible; it does not mean pretending undocumented runtime behavior is known.

## Coverage matrix

| Area | Covered patterns | Main uncertainty |
|---|---|---|
| Logic | nested `IF`, AND/OR, precedence, blank branches | boolean helper representation and coercion |
| Numeric | conversion, arithmetic, thresholds, bands, caps, `SUM`, binary `MIN`/`MAX` | invalid numeric text, rounding policy, negative-value domains |
| Text | trim, case, split, substring, padding, exact list membership | Unicode, punctuation, regex-string escaping |
| Regex | match, extract, nth extract, replace | Export Preview bracket tokenization and backslash handling |
| Core maps | taxonomy, term, major, CEEB, source code | tenant keys, map contents, target representation |
| Regular data sources | `DS_MAP` across database columns | data-source ID and real `column_N` names |
| Checkbox/list | checked text, first value, exact membership, separate columns | returned text versus codes and delimiter shape |
| Dates | parse, format, compare, add, difference, current date; Import Preview invalid-component rollover, strict round-trip validation, and deterministic birthday/leap-year branching verified | timezone, date-only semantics, cross-context parity |
| Imports | `[C#]` transformations, labels, maps, cleanup | column order, import scope, blank action |
| Exports | calculated columns, scope, root parsing, output formatting | Preview compiler and downstream file expectations |
| Workflow/Rule Formula Field | scoring, cleanup, property assignment | token availability and destination write validation |
| Calculated payments | quantity, option, threshold pricing | numeric enforcement, decimals, unexpected input |
| Root fields | occurrence guards; compact milestone object isolation/reconstruction, independent exact application/term/major checks, same-object epoch-millisecond extraction, combined single-candidate `&` eligibility returning numeric `1`/`0`, explicit `major:null` inclusion under exact-major exclusion, explicit `term:null` rejection under exact allowed-term matching, guarded numeric `SUM` aggregation, two-occurrence business-eligibility counting with all valid/invalid arrangements, manually created Deposit compatibility under canonical `type` enumeration, five-slot coverage ceiling, and a complete five-slot qualifying-Deposit count formula user-verified across an eight-case matrix with matching Evaluate/Preview Export results; these guard/bound/same-object/coverage lessons are explicitly transferred to application-root guidance without assuming the same serializer | application serializer/runtime parity for each assembled formula, serializer-shape portability, entirely omitted major/term shapes, maximum practical formula length |
| Linked root selection | argmax/argmin returning associated value | tie policy and repeated-expression complexity |
| Dynamic Eastern time | end-to-end modern US DST conversion from positive UTC epoch milliseconds verified in Import Preview, including `N` weekday mapping, transition construction, epoch-`U` exact-second parsing, dynamic EST/EDT classification, offset application, and local datetime formatting | Export-context parity still needs runtime verification; Import Preview `Y-m-d H:i:s` source columns can lose time-of-day inside date functions |

## Confidence labels

Use one of these labels when documenting a formula:

- **Officially documented:** exact behavior appears in current official Element451 documentation.
- **User-verified:** observed in Element451 Evaluate, Preview Export, or a completed action/export; preserve only generalized behavior.
- **Static-lint clean:** syntax/arity/common-risk checks pass locally, but runtime is not proven.
- **Design target:** logically constructed to test a gap; requires isolated runtime evaluation before production use.
- **Unsupported/unknown:** no source-supported way has been established; do not invent a function.

## Known knowledge frontiers

Prioritize controlled tests for:

1. Boolean return types across Import, Export, Workflow/Rule, and Payment contexts.
2. Backslash and literal-character handling in regex strings across contexts.
3. Strict date-validation round trips across contexts. Import Preview testing established both invalid-component rollover and the canonical parse-format-compare validation technique.
4. Cross-context parity for deterministic birthday/leap-year logic. Import Preview verified ordinary before/after/today cases plus February 29 handling in leap and non-leap years, but the exact Export/Workflow construction using `DATE_DEFAULT` remains unverified.
5. PHP date-format token coverage beyond commonly demonstrated tokens. `N` weekday numbering and `U` epoch parsing with exact seconds are user-verified in Import Preview, but cross-context parity remains open.
6. Exact Formula Field token availability under different workflow/application/event trigger scopes.
7. Maximum practical formula length/depth in Evaluate and Preview Export.
8. Serializer stability for application and milestone root fields across creation paths and contexts. One compact milestone shape now has user-verified `name`-anchored prefix recovery, next-object suffix bounding, blank missing-occurrence guards, and complete single-object reconstruction, but portability is still open.
9. Cross-context parity for end-to-end DST-aware conversion. Exact spring/fall transition classification and final local datetime conversion are user-verified in Import Preview for positive UTC epoch milliseconds; Export Evaluate and actual Preview Export remain open.
10. Argmax/argmin formulas that return a field from the winning object.
11. Earliest-selection sentinel behavior and numeric comparison at large millisecond values.

The current date/time frontier suite is in `references/formula-frontier-tests.md`. `references/formula-frontier-root-tests.md` retains the completed, user-verified milestone reconstruction/count test. General application latest/earliest/linked-value architecture remains documented in the normal root-field references and must be tested against the current application serializer.

## How to record test feedback

When a user tests a design target, capture only reusable evidence:

1. Formula context: Import, Export Evaluate, Preview Export, Workflow/Rule Test Formula, actual persisted write, or Calculated Payment.
2. Exact minimal test expression, anonymized before bundling.
3. Input shape and expected output, with personal data removed.
4. Actual output or exact error text.
5. Whether the result reproduces on more than one record.
6. The smallest change that fixes or disproves the hypothesis.
7. Confidence label after testing.
8. Regression cases that must remain in the skill.

Do not store tenant GUIDs, custom slugs, data-source mappings, domains, or institutional business policy unless they are fictionalized first.
