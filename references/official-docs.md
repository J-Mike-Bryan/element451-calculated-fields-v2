# Official Element451 formula documentation routes

## Table of contents

- [Source hierarchy](#source-hierarchy)
- [Primary formula-function pages](#primary-formula-function-pages)
- [Import context](#import-context)
- [Export context](#export-context)
- [Workflow and Rule Formula Field context](#workflow-and-rule-formula-field-context)
- [Calculated payment context](#calculated-payment-context)
- [Verification rules](#verification-rules)
- [What the live pages currently establish](#what-the-live-pages-currently-establish)

## Source hierarchy

Use the narrowest current official source that supports the claim:

1. Exact Element451 Help Center article for UI, configuration, preview, scoping, destination behavior, or payments.
2. Exact Element451 Integration Guide page for the formula/function reference.
3. Current import/export column-setting articles for field types, date handling, empty values, transformations, validations, and scope.
4. User-provided training and generalized runtime observations for details not fully described in public articles.
5. Element451 Evaluate/Test Formula, Preview Export, an actual Workflow/Rule write, or calculated-payment result for runtime confirmation in the user's tenant.

The bundled sources are not a frozen substitute for the live product. Open the best live page before claiming a function, token, menu, format, or behavior is currently supported.

## Primary formula-function pages

### Calculated Fields - Help Center

- Canonical current URL: https://help.element451.io/en/articles/9007704-calculated-fields
- Legacy/redirect URL: https://help.element451.com/en/articles/9007704-calculated-fields
- Purpose: common Import and Export formulas, label imports, mappings, dates, checkbox handling, and export Evaluate preview.
- Verified live: 2026-08-31.
- Article date shown at verification: 2026-03-27.

### Calculated Fields - Integration Guide

- URL: https://integrations.element451.com/calculated-fields-37
- Purpose: full calculated-field function documentation referenced by the Help Center.
- The site requires JavaScript in some retrieval environments. If the page cannot be read, do not invent missing details; use the bundled training source and mark the limitation.

## Import context

### Column Setting Options for Imports

- Canonical current URL: https://help.element451.io/en/articles/9006325-column-setting-options-for-imports
- Legacy/redirect URL: https://help.element451.com/en/articles/9006325-column-setting-options-for-imports
- Verified live: 2026-08-31.
- Use for transformations, system mapping, PHP-style date format, empty-value behavior, validation, and repeatable-object scoping.

### Creating Imports

- Canonical current URL: https://help.element451.io/en/articles/9001231-creating-imports
- Legacy/redirect URL: https://help.element451.com/en/articles/9001231-creating-imports
- Use for current navigation and mapping context.

### Integration Guide importing data

- URL: https://integrations.element451.com/importing-data-103

## Export context

### Column Setting Options for Exports

- Canonical current URL: https://help.element451.io/en/articles/9007047-column-setting-options-for-exports
- Legacy/redirect URL: https://help.element451.com/en/articles/9007047-column-setting-options-for-exports
- Verified live: 2026-08-31.
- Article date shown at verification: 2026-07-09.
- Use for transformations, system mapping, date formatting, empty values, scope, and First/Last plus Order By settings.

### Creating Exports

- Canonical current URL: https://help.element451.io/en/articles/9007317-creating-exports
- Legacy/redirect URL: https://help.element451.com/en/articles/9007317-creating-exports
- Use for current navigation and mapping context.

### Integration Guide exporting data

- URL: https://integrations.element451.com/exporting-data-102

## Workflow and Rule Formula Field context

### Formula Field

- Canonical current URL: https://help.element451.io/en/articles/8857623-formula-field
- Legacy/redirect URL: https://help.element451.com/en/articles/8857623-formula-field
- Verified live: 2026-08-31.
- Article date shown at verification: 2026-07-16.
- Purpose: formulas on supported Workflows + Rules user-property actions, Formula Test/Evaluate, examples, and destination data-source validation.

The current article states that supported Formula Fields use the same formula language as Import/Export functions. It also warns that a formula can evaluate successfully but fail to save when the returned value is not accepted by the destination field's backing data source. Verify the actual write, not only the evaluator output.

## Calculated payment context

### Payment Types

- Canonical current URL: https://help.element451.io/en/articles/9071731-payment-types
- Legacy/redirect URL: https://help.element451.com/en/articles/9071731-payment-types
- Verified live: 2026-08-31.
- Article date shown at verification: 2024-04-03.
- Purpose: Fixed, Conditional, Calculated, and User-defined payment types.

The Calculated payment type accepts a formula using person-record data and/or submitted form fields, provides Test Formula/Evaluate, and should produce a numeric amount.

## Verification rules

- Prefer the canonical `.io` Help Center URL after redirects, but accept the official `.com` URL when the user supplies it.
- Do not infer a function signature from another language or spreadsheet product.
- Do not infer a field slug, available trigger token, taxonomy GUID, data-source ID, application GUID, major GUID, or destination representation.
- When official examples contain smart quotes, missing punctuation, or client placeholders, normalize them before use and validate the result.
- Distinguish documented behavior from a formula merely observed in a user-provided example.
- When current docs and a bundled example differ, explain the conflict and use focused runtime testing rather than guessing.
- Do not ask for API keys, passwords, or unredacted student data. Root-field samples should be redacted while preserving structure and relevant marker values.
- Do not recommend a different technical method when the user explicitly requires a formula. Mention other product settings only when they directly affect formula context or the user asks for alternatives.

## What the live pages currently establish

As verified on 2026-08-31:

- Calculated fields manipulate incoming Import data and outgoing Export data.
- Import examples use column references such as `[C#]`.
- The Help Center links to the Integration Guide's fuller formula-function list and demonstrates functions including date, map, text, regex, checkbox, and conditional helpers.
- Export calculated columns can be previewed against a selected contact with Evaluate, but actual Preview Export remains a separate validation layer.
- Import and Export column settings include transformations, validations, empty values, and scope.
- Export datetime settings can use the configured client timezone; date-only fields avoid timezone conversion because it can shift the calendar date.
- Export settings can select First or Last after ordering repeatable items, but those settings do not replace a requested formula when the required cross-object rule cannot be expressed by scope alone.
- Supported Workflows + Rules user-property actions expose a Formula Field using the Import/Export formula language and a Test Formula evaluator.
- A successful Workflow/Rule formula evaluation does not guarantee persistence to a data-source-backed destination field.
- Calculated payments can use formulas over person/form fields and provide Test Formula/Evaluate; their result is the payment amount.
