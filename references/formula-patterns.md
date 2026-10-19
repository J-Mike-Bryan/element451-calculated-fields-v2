# Reusable Element451 formula patterns

## Table of contents

- [Pattern selection](#pattern-selection)
- [Simple conditionals](#simple-conditionals)
- [Range and precedence logic](#range-and-precedence-logic)
- [Safe blank handling](#safe-blank-handling)
- [Import column transformations](#import-column-transformations)
- [Taxonomy and data-source mapping](#taxonomy-and-data-source-mapping)
- [Labels](#labels)
- [Checkbox and list fields](#checkbox-and-list-fields)
- [Dates and elapsed time](#dates-and-elapsed-time)
- [Text cleanup and capitalization](#text-cleanup-and-capitalization)
- [Appending values without stray separators](#appending-values-without-stray-separators)
- [Any qualifying object in a root field](#any-qualifying-object-in-a-root-field)
- [Latest matching object in a root field](#latest-matching-object-in-a-root-field)
- [Linked value from the winning root object](#linked-value-from-the-winning-root-object)
- [Editing an existing formula](#editing-an-existing-formula)

## Pattern selection

Before selecting a pattern, identify:

1. **Environment:** Import, Export, Workflow/Rule Formula Field, or calculated payment. Read `formula-contexts.md` when output persistence, scoping, or numeric payment behavior matters.
2. **Input form:** import column, Element field slug, checkbox JSON, taxonomy GUID, data-source value, date string, or serialized root field.
3. **Output type:** text, number, date, GUID, taxonomy list, or blank.
4. **Empty behavior:** empty string, existing value, fallback literal, or zero.
5. **Selection rule:** first, last/latest, earliest, highest-priority, all matching, or exact occurrence.
6. **Tenant values:** field slugs, taxonomy GUIDs, data-source IDs, application GUIDs, term/major GUIDs.

Do not reuse client-specific identifiers from the bundled examples unless the user supplied them for the current task.

## Simple conditionals

### One condition

```text
IF([field] = "expected", "result when true", "result when false")
```

### All conditions must match

```text
IF(
    ([field-a] = "Yes") & ([field-b] = "Yes"),
    [field-c],
    ""
)
```

### Any condition may match

```text
IF(
    ([field-a] = "Yes") | ([field-b] = "Yes"),
    [field-c],
    ""
)
```

Use explicit parentheses around each condition in long formulas. This prevents ambiguity when AND and OR are mixed.

## Range and precedence logic

Order nested `IF` branches from highest priority to lowest priority or from most restrictive range to broadest range.

```text
IF(
    [score] >= 27,
    "1",
    IF(
        ([score] >= 24) & ([score] < 27),
        "2",
        IF(
            ([score] >= 21) & ([score] < 24),
            "3",
            "4"
        )
    )
)
```

For status precedence, test the furthest-along status first. A simpler priority chain is usually safer than checking every lower-status absence, unless the business rule explicitly requires exclusivity.

## Safe blank handling

### Preserve an existing value when the new input is blank

```text
IF([new-value] = "", [existing-value], [new-value])
```

### Parse only when input exists

```text
IF(
    [date-text] = "",
    "",
    DATE_READ([date-text], "m/d/Y")
)
```

The training source states that `IF` short-circuits, so the date parser is not evaluated for a blank value.

### Avoid a zero-epoch fallback date

Do not convert a missing timestamp represented as `0` and then try to explain `12/31/1969` after the fact. Prefer a guard:

```text
IF(
    [epoch-seconds] = 0,
    "",
    DATE_FORMAT(DATE_READ(CONCAT("", [epoch-seconds]), "U"), "m/d/Y")
)
```

When the computed timestamp expression is too long to repeat, the sentinel-removal pattern from the user examples may be used, but document why it works and test the exact formatted output and timezone.

## Import column transformations

### Use today's date

```text
DATE_DEFAULT("Y-m-d")
```

### Convert a year to a full date

```text
DATE_READ(CONCAT("06/01/", [C2]), "m/d/Y")
```

### Add a leading zero before parsing an eight-digit date

```text
DATE_READ(PAD([C2], "0", 8), "mdY")
```

### Split a combined name

```text
TITLECASE(SPLIT_INDEX([C1], " ", 1))
```

### Remove literal double quotes

```text
REGEXP_REPLACE([C1], """", "")
```

### Keep a five-digit ZIP code

```text
SUBSTR(
    IF(
        STRLEN([C13]) = 4,
        PAD([C13], "0", 5),
        IF(
            STRLEN([C13]) = 8,
            PAD([C13], "0", 9),
            [C13]
        )
    ),
    0,
    5
)
```

Confirm whether an eight-character source means a missing leading zero in a nine-digit ZIP or whether it contains punctuation. Do not assume.

### Exact lookup in an embedded delimiter table

Use this pattern when an Import calculated field contains a literal fixed-width `key -> value` crosswalk and the incoming identifier may be displayed without its leading zeros in Import Preview. Separate normalization from lookup: first restore the fixed-width text key, then match on an exact delimiter boundary.

A user-verified Import case had six-character identifiers in the CSV, while Import Preview displayed the same values without leading zeros. The formula restored the key with:

```text
RIGHT(CONCAT("000000", TRIM([C1])), 6)
```

That normalization means an incoming `123` becomes `000123` before matching. Use `RIGHT(..., 6)` only when the identifier is defined to be exactly six characters; otherwise choose the correct fixed width and do not silently truncate legitimately longer identifiers.

For a table shaped like `|000123=ABCD|001234=EFGH|`, nested `SPLIT_INDEX` provides an exact lookup without regex escaping:

```text
IF(
    TRIM([C1]) = "",
    "",
    SPLIT_INDEX(
        SPLIT_INDEX(
            CONCAT(
                "|000123=ABCD|001234=EFGH|",
                RIGHT(CONCAT("000000", TRIM([C1])), 6),
                "=",
                RIGHT(CONCAT("000000", TRIM([C1])), 6),
                "|"
            ),
            CONCAT(
                "|",
                RIGHT(CONCAT("000000", TRIM([C1])), 6),
                "="
            ),
            2
        ),
        "|",
        1
    )
)
```

Execution order:

1. Blank input returns `""`.
2. `RIGHT(CONCAT(...), width)` rebuilds the fixed-width text key even if Preview omitted leading zeros.
3. The outer `CONCAT` appends a synthetic `normalized-key=normalized-key|` entry. This is the fallback; if the real table contains the key, its earlier entry is selected. If the key is unknown, the appended entry returns the normalized input itself.
4. The inner `SPLIT_INDEX(..., CONCAT("|", normalized-key, "="), 2)` jumps to the text after the exact key boundary.
5. The outer `SPLIT_INDEX(..., "|", 1)` returns only that key's mapped value.

This architecture was user-reported working in the Element451 Import context after a syntactically valid `REGEXP_EXTRACT` version with escaped pipe boundaries returned blank for all tested codes. Treat that as evidence for this delimiter-table lookup shape, not a general claim that `REGEXP_EXTRACT` is broken. Before rewriting a lookup, echo the normalized key alone so source coercion and lookup behavior are diagnosed separately.

If unknown keys should return blank or another diagnostic rather than the normalized input, change the appended synthetic fallback accordingly instead of changing the exact-match delimiter strategy.

## Taxonomy and data-source mapping

### Name to taxonomy GUID

```text
TAXONOMY_MAP([C2], "name", "guid", "")
```

### GUID to taxonomy name

```text
TAXONOMY_MAP([user-labels-one], "guid", "name", "")
```

### Term name to term GUID

```text
DB_MAP("term", CONCAT("Fall ", [C2]), "name", "guid", "")
```

### Major CIP code to major GUID

```text
DB_MAP("major", [C2], "cip", "guid", "")
```

### Major GUID to associated degree, including inactive majors

A September 2026 user-reported runtime test showed that the database-backed major lookup continued to resolve inactive majors, while the comparable majors data-source lookup returned blank for an inactive major. Use this pattern when historical/inactive majors must still map to their associated degree value:

```text
FIRST(
    DB_MAP(
        "major",
        <major-guid>,
        "guid",
        "degrees",
        ""
    )
)
```

Treat `<major-guid>` as request-scoped tenant data. The exact runtime context was not separately recorded, so re-verify if context-specific behavior matters.

Regression checks for this pattern:
- active major GUID -> associated degree value,
- inactive major GUID -> associated degree value,
- unknown major GUID -> configured default/blank,
- optional diagnostic comparison: the same inactive major through the majors data source may return blank even though `DB_MAP("major", ...)` resolves it.

### Regular data source mapping

```text
DS_MAP(
    [C2],
    "client.data_source.12345",
    "column_2",
    "column_1",
    ""
)
```

Verify all five values:

- input value,
- exact data-source identifier,
- source column/key used to match,
- output column/key,
- default when no match exists.

Do not silently swap the match and output directions.

## Labels

### One label

Map the calculated field to `user-labels-import` and return the label GUID:

```text
"client.taxonomy.12345"
```

### Multiple fixed labels

Return one comma-separated string with no spaces:

```text
"client.taxonomy.12345,client.taxonomy.67890"
```

### Labels from multiple import columns

```text
CONCAT(
    TAXONOMY_MAP([C2], "name", "guid", ""),
    ",",
    TAXONOMY_MAP([C3], "name", "guid", ""),
    ",",
    TAXONOMY_MAP([C4], "name", "guid", "")
)
```

This can create duplicate or leading/trailing commas when some columns are blank. For sparse data, use conditional separator logic rather than copying this pattern blindly.

### Test whether a user has one label GUID

For `[user-labels-all]`, prefer the runtime-verified `REGEXP_MATCH` membership pattern rather than assuming the field is a simple comma-delimited string:

```text
IF(
    REGEXP_MATCH(
        [user-labels-all],
        ".*school.taxonomy.70001.*"
    ) = TRUE,
    "Transfer",
    "Freshman"
)
```

This pattern is based on user-verified label tests where `REGEXP_MATCH` correctly distinguished label presence while two `CONTAINS` approaches did not. Replace the fictional GUID. Because this is a substring-style regex, confirm that the full supplied GUID cannot be a substring of another identifier in the current data. If exact token boundaries matter, first inspect the raw `[user-labels-all]` serialization and derive a boundary-aware regex from that actual shape. A name-to-GUID `TAXONOMY_MAP` may be useful while diagnosing a known label name, but a production formula should not repeatedly map a name when the exact current-task GUID has already been supplied.

## Checkbox and list fields

### Return all checked text

```text
CHECKBOX_CHECKED([user-race-categories], ",")
```

### Put checked values into separate export columns

Column 1:

```text
SPLIT_INDEX(CHECKBOX_CHECKED([user-race-categories], ","), ",", 1)
```

Column 2:

```text
SPLIT_INDEX(CHECKBOX_CHECKED([user-race-categories], ","), ",", 2)
```

Continue for the maximum number of values needed. Missing positions should be tested in Evaluate and normally return blank in the bundled examples.

### Test for a selected text value

```text
IF(CONTAINS([checkbox-text], "White") = TRUE, "White", "")
```

Do not assume `CONTAINS` is token-aware. For values that can be substrings of other values, use delimiters or a regex boundary pattern.

## Dates and elapsed time

### Reformat a date

```text
DATE_FORMAT([date-field], "m/d/Y")
```

### Parse, then format

```text
DATE_FORMAT(
    DATE_READ([C2], "Y-m-d"),
    "m/d/Y"
)
```

### Difference in days

```text
DATE_DIFF("day", [start-date], [end-date])
```

### Days, hours, minutes, and seconds

```text
CONCAT(
    FLOOR(DATE_DIFF("second", [start-date], [end-date]) / 86400),
    " days, ",
    FLOOR(MOD(DATE_DIFF("second", [start-date], [end-date]), 86400) / 3600),
    " hours, ",
    FLOOR(MOD(DATE_DIFF("second", [start-date], [end-date]), 3600) / 60),
    " min, ",
    MOD(DATE_DIFF("second", [start-date], [end-date]), 60),
    " seconds"
)
```

### Mongo-style epoch milliseconds

A root field may contain a 13-digit `$numberLong` millisecond timestamp. Convert to seconds before parsing. Two observed approaches are:

```text
FLOOR(VAL([milliseconds-text]) / 1000)
```

or, when the value is known to be a positive 13-digit integer:

```text
VAL(LEFT(CONCAT("", [milliseconds-value]), 10))
```

The division approach is clearer. The `LEFT(..., 10)` approach should not be used for negative, short, decimal, or nonstandard timestamps.

## Text cleanup and capitalization

### Capitalize a simple single-part value

```text
CONCAT(
    UPPER(LEFT(TRIM([name-field]), 1)),
    LOWER(
        RIGHT(
            TRIM([name-field]),
            STRLEN(TRIM([name-field])) - 1
        )
    )
)
```

Guard blanks before subtracting one from the length.

### Compound names

Before normalizing names, decide whether the requirement includes:

- more than two words,
- apostrophes,
- prefixes such as Mc/Mac/O',
- suffixes,
- mixed separators,
- already intentional capitalization.

A user-verified Import test of `TITLECASE(LOWER(...))` produced these results:

| Input | Output |
|---|---|
| `O'CONNOR` or `o'connor` | `O'connor` |
| `SMITH-JONES` or `smith-jones` | `Smith-jones` |
| `MCDONALD` or `mcdonald` | `Mcdonald` |
| `DE LA CRUZ` or `de la cruz` | `De La Cruz` |

This establishes that the pattern capitalizes ordinary space-separated words, but does not automatically restore capitalization after apostrophes or hyphens and does not infer internal capitalization such as `McDonald`. For conservative name cleanup, preserve already mixed-case values and only apply `TITLECASE(LOWER(...))` when the source value is clearly all-uppercase or all-lowercase. Do not claim this handles every personal name. The exact Import preview/evaluation surface for this user test was not separately specified.

### Remove a URL query string

```text
SPLIT_INDEX([C2], "?", 1)
```

### Extract a search query and replace plus signs

```text
IF(
    REGEXP_MATCH([C2], ".*\\?s=.*") = TRUE,
    REGEXP_REPLACE(
        REGEXP_EXTRACT([C2], ".*\\?s=(.*)"),
        "\\+",
        " "
    ),
    ""
)
```

Test percent-encoded characters separately; replacing `+` does not fully URL-decode text.

## Appending values without stray separators

### Append a new value to an existing value

```text
IF(
    ([existing] <> "") & ([new] = ""),
    [existing],
    IF(
        ([existing] <> "") & ([new] <> ""),
        CONCAT([existing], ", ", [new]),
        IF(
            ([existing] = "") & ([new] <> ""),
            [new],
            [existing]
        )
    )
)
```

This preserves the existing value, appends with a separator only when both exist, and copies the new value when the existing field is blank.

## Any qualifying object in a root field

Use this pattern when the output depends only on whether **at least one** repeatable/root object satisfies the rule. Examples include a status flag, eligibility indicator, or highest-priority classification branch where the date itself is irrelevant.

For each planned occurrence of the canonical marker:

```text
IF(
    raw_nth_occurrence_is_absent,
    0,
    IF(
        same_bounded_object_meets_every_rule,
        1,
        0
    )
)
```

Then combine the candidates with `SUM` and test for any positive result:

```text
SUM(candidate_1, candidate_2, candidate_3, candidate_4, candidate_5) > 0
```

This is simpler than extracting timestamps and building `MAX` when only existence matters. Preserve the same root-field safety rules:

- enumerate by the canonical discriminator such as `"type":"DEPOSIT"`, not a mutable display/source name;
- guard every planned nth raw occurrence before reconstruction;
- validate against the same full bounded object;
- do not assume required-property order unless verified;
- reject null/missing required metadata on that occurrence without stopping the scan;
- scan enough occurrences that a later valid object is not missed because an earlier same-type object is invalid.

For multiple same-type objects, each candidate is independent. An object with `application_guid:null` or `term:null` returns `0`; a later qualifying object can still return `1`, making the final `SUM(...) > 0` true.

## Latest matching object in a root field

Use `references/root-field-parsing.md` for the full workflow. The reusable architecture is:

1. Isolate each possible matching object occurrence.
2. Reject only objects that fail the business rule.
3. Extract the timestamp or return numeric `0`.
4. Combine all candidates with nested binary `MAX`.
5. Return blank when the maximum is `0`.
6. Convert milliseconds to epoch seconds.
7. Apply the explicitly requested timezone rule.
8. Format the final date.

### Candidate rule: exclude one exact major but include missing major

The correct logical shape is:

```text
IF(
    object_contains_exact_excluded_major,
    0,
    IF(timestamp_is_blank, 0, VAL(timestamp_text))
)
```

Do not write a positive requirement such as `major <> excluded` if missing majors must be included and the extraction returns blank or malformed text for missing properties. Detect the exact excluded marker and reject only that case.

### Latest value

`MAX` is binary in the bundled training signature. Use a balanced tree:

```text
MAX(
    MAX(candidate_1, candidate_2),
    MAX(candidate_3, candidate_4)
)
```

Use `scripts/build_binary_tree.py` for many candidates.

## Linked value from the winning root object

When the output is a term, major, status, or other property attached to the latest/earliest object, a scalar `MAX` or `MIN` is not enough. Treat the task as argmax/argmin:

1. Build a valid numeric sort-key candidate for each bounded object.
2. Extract the associated output from that same object.
3. Compare sort keys pairwise.
4. Return the associated output for the winning key.
5. Define equal-key tie behavior.
6. Guard the all-invalid case.

Read `references/root-field-selection.md` for the linked-value architecture. Do not select a date first and then search the entire root field for a matching term; that can pair fields from different objects. No unfinished application argmax frontier formula is bundled as though it were validated; build the key/value pairing from the current tenant's bounded application objects and test it incrementally in Element.

## Editing an existing formula

When the user asks for one change:

1. Preserve unrelated working logic.
2. Identify the smallest semantic change.
3. Re-run structural checks across the complete formula.
4. Re-test all prior edge cases plus the new one.
5. Return the **entire updated formula**, not a partial replacement, unless the user explicitly asks for a patch only.
6. State the changed rule in one sentence and avoid proposing another method when the user requested a calculated field.
