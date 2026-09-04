# Formula contexts in Element451

## Table of contents

- [Why context matters](#why-context-matters)
- [Import calculated fields](#import-calculated-fields)
- [Export calculated fields](#export-calculated-fields)
- [Workflow and Rule Formula Fields](#workflow-and-rule-formula-fields)
- [Calculated payments](#calculated-payments)
- [Context selection checklist](#context-selection-checklist)
- [Cross-context portability rules](#cross-context-portability-rules)

## Why context matters

Element451 exposes the formula language in more than Imports and Exports. The function vocabulary may be shared, but available input tokens, target validation, preview layers, scoping, output types, and failure modes differ. Always identify the context before writing syntax.

## Import calculated fields

Typical inputs are source columns such as `[C1]`, `[C2]`, and `[C3]`. Establish:

- the incoming text shape;
- the destination field and its type;
- whether the calculated column is mapped before or after related scoped fields;
- whether blank means omit, clear, preserve, or import an empty string;
- whether a map should return GUID, code, value, name, or another database key; and
- whether validations or transformations outside the formula alter the result.

Import formulas may use regex forms that are unsafe in Export Preview, but still require actual import evaluation because parser behavior can differ.

## Export calculated fields

Typical inputs are Element field tokens such as `[user-dob]` or a scoped application/milestone field. Establish:

- person-level versus repeatable-object scope;
- any First/Last and Order By settings applied before formula evaluation;
- date-only versus datetime output and timezone behavior;
- target output format and downstream blank/null rules; and
- whether serialized root-field parsing is truly required.

Run both formula Evaluate/Test and actual Preview Export. Preview Export can reject bracket-like text inside quoted regex strings even when Evaluate succeeds.

## Workflow and Rule Formula Fields

The Formula Field appears on supported user-property actions, including setting system, custom, and custom-date properties. The formula language is described as the same syntax used by Imports/Exports, but the destination write adds a second validation layer.

Always identify:

- the triggering context and which scoped fields are available;
- whether the action writes text, number, date, checkbox/radio/dropdown, taxonomy, or another data-source-backed field;
- the exact representation the destination accepts; and
- whether a successful Test Formula result was actually persisted to the person's profile.

A formula can evaluate successfully yet fail to save when its output is not a valid option in the destination field's backing data source. Debug evaluation and persistence as separate stages.

## Calculated payments

Calculated payment formulas can use person-record data and/or submitted form fields. The final output must be a numeric amount.

Define explicitly:

- blank input behavior;
- zero and negative quantities;
- integer versus decimal quantities;
- minimum/maximum amount policy;
- discount thresholds and boundary inclusivity;
- unexpected option values; and
- whether rounding is required and supported by the chosen functions.

Test with a person who has values in every referenced field. A text label such as `"45.00"` is not a substitute for numeric `45` when a payment amount is required.

## Context selection checklist

| Question | Import | Export | Workflow/Rule | Calculated payment |
|---|---|---|---|---|
| Primary input form | `[C#]` | Element fields/scoped fields | Element fields available to action context | Person/form fields |
| Primary output | Mapped import column | Export cell | Persisted field value | Numeric charge |
| Main extra validation | Destination mapping/import settings | Preview Export and downstream format | Destination field accepts value and write persists | Numeric amount and pricing policy |
| Repeatable data concern | Import scope/order | Scope, First/Last, root parsing | Trigger/action scope | Usually form/person inputs; verify event context |
| Blank decision | Skip/clear/import empty | Blank/null/export policy | Preserve/clear/write empty | Usually zero or explicit fallback |

## Cross-context portability rules

1. Do not assume a token visible in one context is available in another.
2. Do not assume Evaluate proves the final operation succeeded.
3. Keep return types consistent with the destination.
4. Preserve exact tenant slugs and identifiers supplied for the current task.
5. Re-test boolean-returning helpers in the target context.
6. For maps, verify both the source match key and destination representation.
7. For dates, distinguish a date-only calendar value from a timezone-sensitive datetime.
8. For root fields, derive markers from an evaluated sample in the same context.
