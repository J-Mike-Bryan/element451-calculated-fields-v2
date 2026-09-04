# Element451 calculated-field function catalog

## Table of contents

- [How to use this catalog](#how-to-use-this-catalog)
- [Core syntax and operators](#core-syntax-and-operators)
- [Logic](#logic)
- [Regular expressions](#regular-expressions)
- [Maps, data sources, taxonomies, and lists](#maps-data-sources-taxonomies-and-lists)
- [Date and time](#date-and-time)
- [Text](#text)
- [Math and numeric conversion](#math-and-numeric-conversion)
- [Known source discrepancies](#known-source-discrepancies)

## How to use this catalog

Use this catalog to select functions and check signatures. It combines three evidence levels:

- **Official**: currently shown in the Element451 Help Center calculated-fields article.
- **Training**: explicitly described in the user-provided function training source.
- **Observed**: used in the user-provided working examples or current official examples, but not fully specified in the bundled training source.

Do not claim an undocumented function is supported merely because its name seems plausible. For current or disputed behavior, open the official pages in `official-docs.md` and use Element451's Evaluate preview.

## Core syntax and operators

### Field and column references

| Context | Form | Example | Notes |
|---|---|---|---|
| Import source column | `[C#]` | `[C2]` | Replace `#` with the actual one-based import column number. |
| Export or record field | `[field-slug]` | `[user-dob]` | Preserve Element's exact slug, including any historical misspelling. |
| Root/serialized field | `[user-...-root]` | `[user-applications-root]` | Treat as serialized text unless current documentation proves a structured parser exists. |
| Literal string | `"text"` | `"Submitted"` | Use straight ASCII double quotes. |
| Literal number | `123` | `65.00` | Do not quote when numeric behavior is required. |

### Comparison and logical operators

| Operator | Meaning |
|---|---|
| `=` | equal |
| `<>` or `!=` | not equal |
| `<`, `<=`, `>`, `>=` | ordered comparison |
| `&` | logical AND |
| `|` | logical OR |
| `!` | logical NOT |

Use parentheses around compound conditions when precedence could be unclear. The training source states that `IF` short-circuits: only the selected branch is evaluated. Use that behavior to guard division, date parsing, and conversions that would fail on blanks.

### Strings and embedded quotes

Inside an Element formula string, represent a literal double quote by doubling it. For example, a string that searches for JSON text like `"major":"x"` uses a formula literal similar to:

```text
"""major"":""x"""
```

Always lint formulas containing serialized JSON because quote counts are easy to break.

## Logic

### `IF(condition, value_if_true, value_if_false)`

- **Evidence:** Official and Training.
- Return the true branch when the condition is nonzero/true; otherwise return the false branch.
- Exactly three arguments.
- Nest `IF` calls for precedence rules or multiple bands.
- Guard risky expressions in the branch that should run only when data exists.

```text
IF([C1] = "Y" & [C2] = "Y", [C3], "")
```

### Boolean handling

The bundled sources are inconsistent about whether a boolean-returning function should be compared with `TRUE` or with the string `"TRUE"`. The function training describes real booleans; some institution examples compare text. Do not silently merge these behaviors.

Use this order:

1. Prefer the real boolean form when the current official function description says the return type is boolean:
   ```text
   REGEXP_MATCH([C1], ".*value.*") = TRUE
   ```
2. Preserve `"TRUE"` only when the user's known working context returns text or the Evaluate preview proves it.
3. If the result is uncertain, show the expected primary formula and state the exact Evaluate check to run.

## Regular expressions

### Export-preview warning for regex brackets

For **export formulas**, avoid regex character classes written with square brackets inside pattern strings, such as `[.]`, `[a-z]`, and `[0-9]`. Element support confirmed that Preview Export can interpret bracketed text inside a quoted regex as a field token and fail with `Expression have undefined tokens`, even when Test Formula succeeds. Use `scripts/formula_lint.py ... --export` to catch this.

Do not assume `\.` is a universally safe replacement for `[.]`. In a verified 2026 application-root export, that rewrite removed the token error but failed to match as expected. Prefer explicit equality/OR logic for small exact allow-lists, or a regex form that has been verified in both Test Formula and Preview Export.

### `REGEXP_MATCH(text, pattern)`

- **Evidence:** Training; used in examples.
- Returns true/false when the text matches the PHP-style pattern.
- The training source describes whole-string matching. Use `.*` around a substring pattern when needed.
- Do not add slash delimiters unless the current Element environment explicitly requires them; bundled official examples pass a bare pattern string.

```text
REGEXP_MATCH("Hello World", "H[a-z]{4}\\s.*")
```

### `REGEXP_EXTRACT(text, pattern)`

- **Evidence:** Training.
- Returns the first parenthetical capture group, not necessarily the entire match.
- Include a capture group around the desired output.

```text
REGEXP_EXTRACT("Hello World", "Hello\\s(.*)")
```

### `REGEXP_EXTRACT_NTH(text, pattern, n)`

- **Evidence:** Training.
- Returns the `n`th parenthetical capture group.
- Confirm whether the target environment treats the first capture group as 1; the training examples do.

### `REGEXP_REPLACE(text, pattern, replacement)`

- **Evidence:** Official and Training/Observed.
- Replaces matching text.
- The correct name in formulas is `REGEXP_REPLACE`, even though one user-provided heading says `REGEX_REPLACE`.

```text
REGEXP_REPLACE([C1], """", "")
```

The pattern above targets a literal double quote. The four quote characters in the formula are intentional.

## Maps, data sources, taxonomies, and lists

### `DB_MAP(type, input, match_key, output_key, default)`

- **Evidence:** Official and Training.
- Maps among internal database records such as terms, majors, and taxonomies.
- Common direction: human-readable name/code to GUID, or GUID to code/name.
- Use the exact entity type and keys supported by the target collection.
- The training source says input is trimmed and normalized before matching; verify if punctuation-sensitive matching matters.

```text
DB_MAP("term", CONCAT("Fall ", [C2]), "name", "guid", "")
```

### `DS_MAP(input, data_source, match_key, output_key, default)`

- **Evidence:** Official and Training.
- Finds an option in a regular data source and returns another column from that option.
- The data source identifier and column names are client-specific.
- For regular data sources, database columns may be named `column_1`, `column_2`, and so on even when the UI has friendly labels.

```text
DS_MAP([C1], "data_source.major", "code", "guid", "")
```

### `TAXONOMY_MAP(input, match_key, output_key, default)`

- **Evidence:** Official and Training.
- Converts among taxonomy `guid`, `name`, and `value` when those keys exist.
- Preserve the direction explicitly. Do not assume a field stores a name when it stores a GUID.

```text
TAXONOMY_MAP([user-labels-one], "guid", "name", "")
```

### `CEEB_MAP(input, match_key, output_key, default)`

- **Evidence:** Training.
- Specialized map over the CEEB collection.

### `SC_MAP_IMPORT(input, default)`

- **Evidence:** Training.
- Training alias for mapping a source-code taxonomy value to a GUID during import.
- Intended for source and source-segment fields in the supplied reference.

### `SC_MAP_EXPORT(input, default)`

- **Evidence:** Training.
- Training alias for mapping a source taxonomy GUID to its value during export.

### `CHECKBOX_CHECKED(json_input, delimiter)`

- **Evidence:** Official and Training.
- Returns the text of all checked options joined by the delimiter.
- An all-unchecked input returns an empty string in the training examples.

```text
CHECKBOX_CHECKED([user-race-categories], ",")
```

### `CHECKBOX_FIRST(json_input)`

- **Evidence:** Training.
- Returns the first checked option's text, or an empty result when none are checked.

### `HAS_ONE_TRUE(json_input, attribute)`

- **Evidence:** Training.
- Returns true when at least one object has the named attribute set to true.

### `FIRST(value)`

- **Evidence:** Official example.
- Used by the official calculated-fields article to return the first item from a mapped list, such as a major's associated degree.
- The bundled sources do not fully specify ordering or behavior for empty/non-list input. Verify with Evaluate before relying on those details.

### Importing labels

The current official Help Center pattern maps the calculated column to `user-labels-import` and returns one GUID or a comma-separated list of GUIDs with no spaces.

```text
"client.taxonomy.12345,client.taxonomy.67890"
```

When labels arrive by name from multiple columns, map each name to a GUID and concatenate with literal commas.

## Date and time

Element date functions commonly use PHP-style format strings. The training source says standard date inputs use `Y-m-d H:i:s`. Do not assume the record value, import value, or epoch string is already in that format.

### `DATE_ADD(date_part, interval, date)`

- **Evidence:** Training and Observed.
- Supported date parts in the training source: `second`, `minute`, `hour`, `day`, `month`, `year`.
- Returns the adjusted date.

### `DATE_DIFF(date_part, start_date, end_date)`

- **Evidence:** Official and Training.
- Returns an integer difference in the requested unit.
- Confirm how partial years/months are handled when exact age logic matters.

### `DATE_COMPARE(date_1, operator, date_2)`

- **Evidence:** Official and Training.
- Returns true/false for operators such as `<`, `<=`, `=`, `!=`, `<>`, `>=`, and `>`.

### `DATE_FORMAT(input_date, format)`

- **Evidence:** Official and Training.
- Converts a parsed date to a requested PHP-style output format.

Common output formats:

| Desired output | Format |
|---|---|
| `10/13/2026` | `m/d/Y` |
| `2026-10-13` | `Y-m-d` |
| Four-digit year | `Y` |
| Two-digit year | `y` |

The docs describe PHP-style formats, but do not assume every PHP token has been runtime-proven in every Element context. `N` is user-verified in Import Preview for a complete Sunday-through-Saturday test week to follow ISO/PHP numbering: Monday=`1` through Sunday=`7`. `U` is observed in working user examples for epoch parsing/formatting. Re-test uncommon tokens in other formula contexts when the distinction materially affects production behavior.

### `DATE_DEFAULT(format)`

- **Evidence:** Official and Training.
- Returns the current date/time formatted as requested.
- Do not assume the server timezone. If the calendar day matters, prove the timezone with Evaluate.

### `DATE_READ(date_string, format)`

- **Evidence:** Official and Training.
- Parses a string according to the specified PHP-style format and returns a standard date value.
- `U` is user-verified in Import Preview for Unix epoch seconds. After integer conversion from epoch milliseconds, focused boundary tests preserved `06:59:59`, `07:00:00`, `07:00:01`, `05:59:59`, `06:00:00`, and `06:00:01` exactly.
- **Import Preview source-column caution:** a user-verified probe supplied `Y-m-d H:i:s` text through `[C1]`. `DATE_READ(TRIM([C1]), "Y-m-d H:i:s")` followed by `DATE_FORMAT(..., "Y-m-d H:i:s")` returned the correct calendar date but `00:00:00` for every tested source time. In the same probe, `DATE_COMPARE(TRIM([C1]), ...)` behaved as though `[C1]` were also date-only/midnight, while direct literal-to-literal `DATE_COMPARE` preserved second-level behavior. Treat this as Import Preview source-value coercion behavior unless another context is separately verified.
- Mongo-style `$numberLong` timestamps are commonly milliseconds; convert to **integer** seconds before `DATE_READ(..., "U")`. Do not pass fractional seconds such as `1753128101.067`; a verified root-field formula produced implausible years and an incorrect July month until the timestamp was truncated to integer epoch seconds. In Import Preview, `FLOOR(VAL([C1]) / 1000)` followed by `DATE_READ(..., "U")` preserved exact seconds across tested DST transition boundaries.

### Eastern Time warning

A fixed offset is not equivalent to year-round Eastern Time:

- `-18000` seconds is UTC-5 (EST).
- `-14400` seconds is UTC-4 (EDT).

For historical timestamps spanning both seasons, do not describe either fixed offset as fully DST-aware. State the limitation or build and test explicit DST logic only when the available functions and requirements support it.

## Text

### `CONCAT(value_1, value_2, ...)`

- **Evidence:** Official and Observed.
- Joins values without an automatic separator.
- Supply literal spaces, commas, hyphens, or other separators as arguments.

### `SPLIT_INDEX(text, delimiter, index)`

- **Evidence:** Training and Official examples.
- Splits text and returns the indexed segment.
- Bundled examples use one-based indexing.
- When splitting on a marker, index `1` is the text before the first marker and index `2` is the first matching segment after it.

### `CONTAINS(text, substring)`

- **Evidence:** Training and examples.
- Returns true/false when the substring occurs.
- **Boolean-coercion caution:** In some Element contexts, boolean-returning helpers have required an explicit comparison before use inside `IF`. A verified root-field export used a `CONTAINS` allow-list directly as the `IF` condition and incorrectly allowed every term. Evaluate `CONTAINS(...)` by itself and compare explicitly to the observed `TRUE`/`"TRUE"` representation if needed. For a short exact allow-list, explicit equality joined with `|` is safer.

### `STARTS_WITH(text, substring)` and `ENDS_WITH(text, substring)`

- **Evidence:** Training.
- Return true/false for prefix or suffix checks.

### `SUBSTR(text, start, length)`

- **Evidence:** Observed in user examples.
- Returns a substring. The user examples use start `0` for the beginning.
- Verify boundary behavior for short input.

### `STRLEN(text)`

- **Evidence:** Observed in user examples.
- Returns string length.

### `LEFT(text, length)` and `RIGHT(text, length)`

- **Evidence:** Observed in user examples.
- Return characters from the beginning or end.

### `TRIM(text)`

- **Evidence:** Observed in user examples.
- Removes surrounding whitespace.

### `UPPER(text)`, `LOWER(text)`, and `TITLECASE(text)`

- **Evidence:** `TITLECASE` is Official; `UPPER` and `LOWER` are Observed.
- Apply case conversion after handling blanks and compound names.
- Do not assume a simple title-case rule handles apostrophes, hyphens, prefixes, or more than two name parts.

### `PAD(value, pad_character, total_length)`

- **Evidence:** Official and Observed.
- Pads to a target width. Examples use it for dates, ZIP codes, and two-digit term years.
- Preserve leading zeros by returning text where necessary.

## Math and numeric conversion

| Function | Signature | Bundled behavior |
|---|---|---|
| `SQR` | `SQR(x)` | Square of `x`. |
| `SIN` | `SIN(x)` | Sine in radians. |
| `ATAN` | `ATAN(x)` | Inverse tangent. |
| `COSH` | `COSH(x)` | Hyperbolic cosine. |
| `COTAN` | `COTAN(x)` | Cotangent. |
| `EXP` | `EXP(x)` | `e` raised to `x`. |
| `LN` | `LN(x)` | Natural logarithm. |
| `LOG` | `LOG(x)` | Base-10 logarithm. |
| `SQRT` | `SQRT(x)` | Principal square root. |
| `ABS` | `ABS(x)` | Absolute value. |
| `SIGN` | `SIGN(x)` | `-1`, `0`, or `1`. |
| `TRUNC` | `TRUNC(x)` | Drop fractional part. |
| `CEIL` | `CEIL(x)` | Smallest integer greater than or equal to `x`. |
| `FLOOR` | `FLOOR(x)` | Largest integer less than or equal to `x`. |
| `RND` | `RND()` | Pseudorandom value from 0 inclusive to 1 exclusive. |
| `VAL` | `VAL(text)` | Convert leading numeric text to a number; training says a nonnumeric suffix is ignored. |
| `NUM` | `NUM(text)` | Attempt numeric conversion, including currency-like strings. |
| `POW` | `POW(base, exponent)` | Raise base to exponent. |
| `MIN` | `MIN(a, b)` | Smaller of exactly two arguments in the training signature. |
| `MAX` | `MAX(a, b)` | Larger of exactly two arguments in the training signature. |
| `MOD` | `MOD(m, n)` | Remainder. |
| `SUM` | `SUM(x1, x2, ..., xN)` | Sum one or more values. |

For more than two candidates, nest `MAX` or `MIN` or use `scripts/build_binary_tree.py` to create a balanced tree.

```text
MAX(MAX(candidate_1, candidate_2), MAX(candidate_3, candidate_4))
```

## Known source discrepancies

Do not hide these differences:

1. The training source documents functions more broadly than the current Help Center article. Verify uncommon functions live before making a strong current-support claim.
2. The training source repeats `DATE_FORMAT`, `DATE_ADD`, `DB_MAP`, `DS_MAP`, `IF`, and `TAXONOMY_MAP` in later use-case sections.
3. One heading says `REGEX_REPLACE`, while formulas and official documentation use `REGEXP_REPLACE`.
4. Boolean examples alternate among raw `TRUE`, title-case `True`, and quoted `"TRUE"`. Test the actual return type.
5. Some official and user examples contain typographical or client-specific details. Normalize straight quotes, check commas and arity, preserve exact field slugs, and run the linter.
6. Data source IDs, taxonomy GUIDs, application GUIDs, major GUIDs, and field slugs are tenant-specific unless explicitly documented as global.
