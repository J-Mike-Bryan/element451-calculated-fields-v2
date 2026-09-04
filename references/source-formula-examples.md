# Generalized Element451 formula examples

## Table of contents

- [How to use this reference](#how-to-use-this-reference)
- [Audit findings applied](#audit-findings-applied)
- [Conditionals and numeric output](#conditionals-and-numeric-output)
- [Terms, grades, and mappings](#terms-grades-and-mappings)
- [Labels and prioritized status](#labels-and-prioritized-status)
- [Dates and elapsed time](#dates-and-elapsed-time)
- [URLs and source attribution](#urls-and-source-attribution)
- [Text, address, and list cleanup](#text-address-and-list-cleanup)
- [Demographic and name output](#demographic-and-name-output)
- [Root-field selection](#root-field-selection)
- [Maintenance rules](#maintenance-rules)

## How to use this reference

These are **generalized teaching examples**, not tenant configuration. Identifiers beginning with `school.*`, fields such as `[user-custom-field-example]`, domains such as `example.edu`, prices, thresholds, status names, and policy dates are fictional. Rebuild each formula with values supplied for the current tenant.

Every marked formula in this file passes the bundled static linter. Static linting does not prove that a formula runs in Element451, that a field exists, that a map contains a requested value, or that the output can be saved to the target field. Formulas described as **test targets** still require Element451 Evaluate; export formulas also require actual Preview Export.

Use the formula context explicitly:

- **Import:** source values normally use `[C#]` references.
- **Export:** person or scoped object fields use Element field tokens; run Preview Export.
- **Workflow or Rule Formula Field:** use the same formula language, but validate that the returned value is accepted by the destination field.
- **Calculated payment:** return a numeric amount and define blank, zero, negative, and unexpected-option behavior.

## Audit findings applied

| Weakness in the prior example set | Improvement now used |
|---|---|
| Redundant range upper bounds | Order descending thresholds so each later branch inherits the upper bound. |
| Blank text compared numerically | Guard blanks and use `VAL` when numeric text is expected. |
| Lowest-to-highest status checks with many negative tests | Check the highest-priority label first and stop at the first match. |
| Regex or substring label matching | Wrap comma-delimited GUID lists with commas and search for an exact delimited token. |
| `DS_MAP` used for core term records | Use `DB_MAP("term", ...)` for Element term data; reserve `DS_MAP` for a supplied regular data source. |
| First-three-character address comparison | Remove Address 2 only when normalized full values are equal; do not delete plausible unit data from a weak prefix match. |
| Hard-coded `20` before a two-digit term year | Prefer the term's mapped `start_date` when the full year is needed. |
| Hispanic plus one race categorized as two or more races | Apply the requested ethnicity policy first, then count race selections separately. |
| Manual capitalization described as robust | Prefer `TITLECASE` and state its punctuation/particle limitations; retain a simple single-token fallback only. |
| Root scanning without a raw nth-occurrence guard | Guard every planned occurrence before isolation, validation, or reconstruction. |
| Milliseconds divided into fractional epoch seconds | Keep milliseconds through selection and use `FLOOR(ms / 1000)` before `DATE_READ(..., "U")`. |
| Examples presented without evidence level | State whether a formula is merely static-lint clean or actually runtime verified. |

## Conditionals and numeric output


### Multi-condition eligibility tier

**Context:** Export or Workflow/Rule Formula Field

Return `Tier A` when any supplied eligibility condition is true; otherwise return `Other`.

<!-- formula-lint: export -->
```text
IF(
    (
        [user-education-schools-transcript_type] = "EXAMPLE_CODE"
    )
    |(
        VAL(
            [user-education-highschools-gpa]
        )
        >= 3.8
    )
    |(
        VAL(
            [user-official-tests-act-composite-superscore]
        )
        >= 27
    )
    |(
        VAL(
            [user-official-tests-nsat-composite-superscore]
        )
        >= 1250
    )
    |(
        VAL(
            [user-official-tests-clt-composite-superscore]
        )
        >= 70
    )
    |(
        VAL(
            [user-education-college-gpa]
        )
        >= 3.8
    ),
    "Tier A",
    "Other"
)
```

**Why this is stronger**
- Parentheses make each OR condition auditable.
- The formula does not infer which blank scores should be treated as zero; high thresholds naturally leave them false in this example.

**Assumptions and limits**
- Confirm that every numeric field evaluates as a number in the target context.
- Replace the transcript code, thresholds, and output labels with the current policy.

**Evaluate checks**
- One qualifying condition, no qualifying conditions, all score fields blank, and a value exactly on each threshold.

### Calculated ticket payment with quantity discount

**Context:** Calculated payment

Return zero for a blank or nonpositive quantity; otherwise apply a fictional bulk rate at eight or more tickets.

<!-- formula-lint: standard -->
```text
IF(
    [user-custom-field-ticket-quantity] = "",
    0,
    IF(
        VAL([user-custom-field-ticket-quantity]) <= 0,
        0,
        IF(
            VAL([user-custom-field-ticket-quantity]) >= 8,
            VAL([user-custom-field-ticket-quantity]) * 12,
            VAL([user-custom-field-ticket-quantity]) * 18
        )
    )
)
```

**Why this is stronger**
- Returns numeric values in every branch.
- Uses `VAL` consistently for quantity text.
- Defines blank, zero, negative, threshold, and ordinary-quantity behavior.

**Assumptions and limits**
- Replace the threshold and rates; decide whether fractional quantities should be rejected or rounded.

**Evaluate checks**
- Blank, `0`, `-1`, `1`, `7`, `8`, and a decimal quantity.

### Calculated payment by selected option

**Context:** Calculated payment

Return zero when no plan is selected, the fictional annual price for `Annual Plan`, and the fictional alternate price for every other nonblank option.

<!-- formula-lint: standard -->
```text
IF(
    [user-custom-field-service-plan] = "",
    0,
    IF(
        [user-custom-field-service-plan] = "Annual Plan",
        80,
        45
    )
)
```

**Why this is stronger**
- The blank branch prevents an unanswered field from producing a charge.
- All outputs are numeric rather than numeric-looking strings.

**Assumptions and limits**
- If more than two options exist, replace the final catch-all with explicit branches so an unknown option cannot be charged accidentally.

**Evaluate checks**
- Blank, exact annual option, expected alternate option, unexpected text, and capitalization mismatch.

### Descending score bands

**Context:** Export or Workflow/Rule Formula Field

Map a fictional score to bands 1 through 4.

<!-- formula-lint: export -->
```text
IF(
    [user-custom-field-highest-evaluation-score] = "",
    "",
    IF(
        VAL([user-custom-field-highest-evaluation-score]) >= 26,
        "1",
        IF(
            VAL([user-custom-field-highest-evaluation-score]) >= 23,
            "2",
            IF(
                VAL([user-custom-field-highest-evaluation-score]) >= 20,
                "3",
                "4"
            )
        )
    )
)
```

**Why this is stronger**
- A blank score returns blank instead of silently entering the lowest band.
- Descending thresholds remove redundant upper-bound comparisons.
- `VAL` makes the numeric conversion explicit.

**Assumptions and limits**
- The band values are text. Return unquoted numbers if the destination field is numeric.

**Evaluate checks**
- Blank, values immediately below/on/above 20, 23, and 26, plus a negative score.

### Compare two evaluation scores

**Context:** Export or Workflow/Rule Formula Field

Return `Y` only when both scores exist and the first is greater; return blank when either score is missing.

<!-- formula-lint: export -->
```text
IF(
    ([user-official-tests-act-composite-superscore] = "") |
    ([user-custom-field-highest-evaluation-score] = ""),
    "",
    IF(
        VAL([user-official-tests-act-composite-superscore]) > VAL([user-custom-field-highest-evaluation-score]),
        "Y",
        "N"
    )
)
```

**Why this is stronger**
- Prevents a missing value from being coerced into a misleading numeric comparison.
- Converts both values with `VAL` before comparison.

**Assumptions and limits**
- Change the blank policy to `N` only when the business rule explicitly treats missing data as a failed comparison.

**Evaluate checks**
- First higher, equal, first lower, first blank, second blank, and both blank.


## Terms, grades, and mappings


### Grade level plus annual cutoff to intended Fall term

**Context:** Workflow/Rule Formula Field or Export

Calculate a fictional Fall term code from grade level and an August 1 school-cycle cutoff, then map the code to a term GUID.

<!-- formula-lint: export -->
```text
IF(
    (
        [user-custom-field-grade-level] = ""
    )
    |(
        VAL(
            [user-custom-field-grade-level]
        )
        < 1
    )
    |(
        VAL(
            [user-custom-field-grade-level]
        )
        > 12
    ),
    "",
    DB_MAP(
        "term",
        CONCAT(
            "FA-",
            PAD(
                MOD(
                    VAL(
                        DATE_DEFAULT(
                            "Y"
                        )
                    )
                    +(
                        12 - VAL(
                            [user-custom-field-grade-level]
                        )
                    )
                    + IF(
                        DATE_COMPARE(
                            DATE_DEFAULT(
                                "Y-m-d"
                            ),
                            ">=",
                            CONCAT(
                                DATE_DEFAULT(
                                    "Y"
                                ),
                                "-08-01"
                            )
                        )
                        = TRUE,
                        1,
                        0
                    ),
                    100
                ),
                "0",
                2
            )
        ),
        "code",
        "guid",
        ""
    )
)
```

**Why this is stronger**
- The cutoff branches now match the stated policy: before August 1, use the just-completed grade; on/after August 1, add one school-cycle year.
- The map default is blank instead of an arbitrary tenant value.

**Assumptions and limits**
- The field must contain a directly numeric grade such as `11`; adapt extraction for text such as `11th Grade`.
- This is a policy example, not a universal graduation calculation.
- Confirm the tenant uses codes such as `FA-27` and contains the computed term.

**Evaluate checks**
- Grade 12 and 11 immediately before and after August 1, blank grade, out-of-range grade, and a missing term map.

### Graduation year to term GUID by full name

**Context:** Import, Export, or Workflow/Rule Formula Field

Normalize a two- or four-digit graduation year into a fictional term name such as `Fall 2027`, then map it through the core term collection.

<!-- formula-lint: standard -->
```text
IF(
    (
        [user-custom-field-graduation-year] = ""
    )
    |(
        VAL(
            [user-custom-field-graduation-year]
        )
        <= 0
    ),
    "",
    DB_MAP(
        "term",
        CONCAT(
            "Fall ",
            IF(
                VAL(
                    [user-custom-field-graduation-year]
                )
                < 100,
                CONCAT(
                    "20",
                    PAD(
                        VAL(
                            [user-custom-field-graduation-year]
                        ),
                        "0",
                        2
                    )
                ),
                CONCAT(
                    "",
                    VAL(
                        [user-custom-field-graduation-year]
                    )
                )
            )
        ),
        "name",
        "guid",
        ""
    )
)
```

**Why this is stronger**
- Uses `DB_MAP("term", ...)` rather than treating the core term collection as an arbitrary regular data source.
- Handles `27` and `2027` explicitly.
- Returns blank when the source or map is blank.

**Assumptions and limits**
- Two-digit values are assumed to be in the 2000s; use a pivot-year rule when historical years are possible.

**Evaluate checks**
- Blank, `27`, `2027`, `7`, an invalid text value, and a year with no mapped term.

### Graduation year to term GUID by code

**Context:** Import, Export, or Workflow/Rule Formula Field

Build a fictional `FA-YY` code and map it to a term GUID.

<!-- formula-lint: standard -->
```text
IF(
    (
        [user-custom-field-graduation-year] = ""
    )
    |(
        VAL(
            [user-custom-field-graduation-year]
        )
        <= 0
    ),
    "",
    DB_MAP(
        "term",
        CONCAT(
            "FA-",
            PAD(
                MOD(
                    VAL(
                        [user-custom-field-graduation-year]
                    ),
                    100
                ),
                "0",
                2
            )
        ),
        "code",
        "guid",
        ""
    )
)
```

**Why this is stronger**
- Keeps the two-digit code calculation separate from full-year display logic.
- Uses a blank default for unmapped values.

**Assumptions and limits**
- The tenant must confirm the exact term code convention and century policy.

**Evaluate checks**
- Blank, two-digit year, four-digit year, and a code absent from the term map.

### Major GUID to CIP

**Context:** Export

Map an intended-major GUID to its CIP value.

<!-- formula-lint: export -->
```text
IF(
    [user-education-prefered-major] = "",
    "",
    DB_MAP(
        "major",
        [user-education-prefered-major],
        "guid",
        "cip",
        ""
    )
)
```

**Why this is stronger**
- Guards a blank major before mapping.
- Preserves the historical `prefered` field slug exactly.

**Assumptions and limits**
- Confirm the major data source contains and exposes the requested `cip` key.

**Evaluate checks**
- Blank major, mapped major, and major without a CIP value.

### CIP to major GUID

**Context:** Import

Map a trimmed CIP value from column 3 to a major GUID.

<!-- formula-lint: standard -->
```text
IF(
    TRIM([C3]) = "",
    "",
    DB_MAP(
        "major",
        TRIM([C3]),
        "cip",
        "guid",
        ""
    )
)
```

**Why this is stronger**
- Uses a real `[C3]` example rather than an unresolved `[Column#]` placeholder.
- Returns blank for blank or unmapped input.

**Assumptions and limits**
- Confirm whether CIP values contain punctuation or leading zeros that must be preserved.

**Evaluate checks**
- Blank, exact match, whitespace-padded match, and unmapped CIP.

### Term name to term GUID

**Context:** Import

Map the full trimmed term name in column 2 directly to a term GUID.

<!-- formula-lint: standard -->
```text
IF(
    TRIM([C2]) = "",
    "",
    DB_MAP(
        "term",
        TRIM([C2]),
        "name",
        "guid",
        ""
    )
)
```

**Why this is stronger**
- Avoids extracting only the last two digits and accidentally discarding a valid four-digit year.
- Leaves naming-convention decisions to the supplied source value and term map.

**Assumptions and limits**
- If the incoming value is abbreviated, normalize it first and document the exact input forms.

**Evaluate checks**
- Blank, exact full name, extra surrounding whitespace, abbreviated name, and unmapped name.

### Term GUID to full year from start date

**Context:** Export or Workflow/Rule Formula Field

Map the term GUID to its `start_date`, parse the mapped date, and return the four-digit year.

<!-- formula-lint: export -->
```text
IF(
    [user-education-term] = "",
    "",
    IF(
        DB_MAP(
            "term",
            [user-education-term],
            "guid",
            "start_date",
            ""
        )
        = "",
        "",
        DATE_FORMAT(
            DATE_READ(
                DB_MAP(
                    "term",
                    [user-education-term],
                    "guid",
                    "start_date",
                    ""
                ),
                "D M d H:i:s O Y"
            ),
            "Y"
        )
    )
)
```

**Why this is stronger**
- Uses term metadata instead of assuming every two-digit term code belongs to the 2000s.
- Avoids coupling the result to one code prefix.

**Assumptions and limits**
- Confirm the mapped `start_date` text matches `D M d H:i:s O Y`; inspect a raw mapped value before changing the parser format.

**Evaluate checks**
- Blank term, mapped term, missing start date, and a start date near a timezone boundary.

### Fall term display with four-digit year

**Context:** Export

Return a display value such as `Fall 2027` by using the mapped term start year.

<!-- formula-lint: export -->
```text
IF(
    [user-education-term] = "",
    "",
    IF(
        DB_MAP(
            "term",
            [user-education-term],
            "guid",
            "start_date",
            ""
        )
        = "",
        "",
        CONCAT(
            "Fall ",
            DATE_FORMAT(
                DATE_READ(
                    DB_MAP(
                        "term",
                        [user-education-term],
                        "guid",
                        "start_date",
                        ""
                    ),
                    "D M d H:i:s O Y"
                ),
                "Y"
            )
        )
    )
)
```

**Why this is stronger**
- Derives the year from term metadata rather than prepending `20` to a suffix.
- Returns blank for a blank term.

**Assumptions and limits**
- This example intentionally hard-codes `Fall`; do not use it for Spring or Summer terms without adding a verified season mapping.

**Evaluate checks**
- Blank, Fall term, non-Fall term to expose the assumption, and term with no start date.

### Regular data-source column mapping

**Context:** Export or Workflow/Rule Formula Field

Translate one fictional regular data-source column into another.

<!-- formula-lint: export -->
```text
IF(
    [user-custom-field-example-status] = "",
    "",
    DS_MAP(
        [user-custom-field-example-status],
        "school.data_source.58231",
        "column_2",
        "column_1",
        ""
    )
)
```

**Why this is stronger**
- Keeps `DS_MAP` for a user-supplied regular data source, where it belongs.
- Guards blank input and uses a blank fallback.

**Assumptions and limits**
- Replace the data-source ID and confirm downloaded database column names such as `column_1` and `column_2`.

**Evaluate checks**
- Blank, mapped value, unmapped value, and an output that the destination field rejects.


## Labels and prioritized status


### Highest-priority active status from exact label GUIDs

**Context:** Workflow/Rule Formula Field or Export

Choose the furthest-progressed fictional status from six exact label GUIDs; preserve the current value if none is present.

<!-- formula-lint: export -->
```text
IF(
    CONTAINS(
        CONCAT(
            ",",
            REGEXP_REPLACE(
                [user-labels-all],
                " ",
                ""
            ),
            ","
        ),
        ",school.taxonomy.60006,"
    )
    = TRUE,
    "Enrolled",
    IF(
        CONTAINS(
            CONCAT(
                ",",
                REGEXP_REPLACE(
                    [user-labels-all],
                    " ",
                    ""
                ),
                ","
            ),
            ",school.taxonomy.60005,"
        )
        = TRUE,
        "Deposited",
        IF(
            CONTAINS(
                CONCAT(
                    ",",
                    REGEXP_REPLACE(
                        [user-labels-all],
                        " ",
                        ""
                    ),
                    ","
                ),
                ",school.taxonomy.60004,"
            )
            = TRUE,
            "Admitted",
            IF(
                CONTAINS(
                    CONCAT(
                        ",",
                        REGEXP_REPLACE(
                            [user-labels-all],
                            " ",
                            ""
                        ),
                        ","
                    ),
                    ",school.taxonomy.60003,"
                )
                = TRUE,
                "Applicant",
                IF(
                    CONTAINS(
                        CONCAT(
                            ",",
                            REGEXP_REPLACE(
                                [user-labels-all],
                                " ",
                                ""
                            ),
                            ","
                        ),
                        ",school.taxonomy.60002,"
                    )
                    = TRUE,
                    "Application Started",
                    IF(
                        CONTAINS(
                            CONCAT(
                                ",",
                                REGEXP_REPLACE(
                                    [user-labels-all],
                                    " ",
                                    ""
                                ),
                                ","
                            ),
                            ",school.taxonomy.60001,"
                        )
                        = TRUE,
                        "Inquiry",
                        [user-custom-field-active-status]
                    )
                )
            )
        )
    )
)
```

**Why this is stronger**
- Checks highest priority first, so no branch needs to prove every later status is absent.
- Uses comma-bounded exact GUID membership instead of regex or partial substring matching.
- Normalizes spaces in the comma-delimited GUID list.
- Removes redundant checks against the current status; returning the same value is already safe.

**Assumptions and limits**
- Replace every GUID and status value with current-tenant values.
- Verify whether `CONTAINS` returns boolean `TRUE` or text `"TRUE"` in this context and adjust the explicit comparison if needed.
- A formula that writes to a data-source-backed status field must return an accepted destination value.

**Evaluate checks**
- No labels, each label alone, all labels together, two nonadjacent labels, a GUID that merely contains another GUID, and spaces after commas.

### Exact export label check

**Context:** Export

Return `Transfer` when one exact fictional label GUID exists; otherwise return `Freshman`.

<!-- formula-lint: export -->
```text
IF(
    CONTAINS(
        CONCAT(
            ",",
            REGEXP_REPLACE(
                [user-labels-all],
                " ",
                ""
            ),
            ","
        ),
        ",school.taxonomy.70001,"
    )
    = TRUE,
    "Transfer",
    "Freshman"
)
```

**Why this is stronger**
- Avoids treating the GUID as a regex pattern.
- Prevents partial GUID matches by adding delimiter boundaries.

**Assumptions and limits**
- Confirm the default classification is really `Freshman`; many policies should return blank when neither category is proven.

**Evaluate checks**
- Exact label, absent label, neighboring GUID, partial GUID, blank label list, and multiple labels.


## Dates and elapsed time


### Application completion duration

**Context:** Export

Return elapsed days, hours, minutes, and seconds between start and completion.

<!-- formula-lint: export -->
```text
IF(
    ([user-milestones-application-start-date] = "") |
    ([user-milestones-application-complete-date] = ""),
    "",
    IF(
        DATE_COMPARE(
            [user-milestones-application-complete-date],
            "<",
            [user-milestones-application-start-date]
        ) = TRUE,
        "",
        CONCAT(
            FLOOR(
                DATE_DIFF(
                    "second",
                    [user-milestones-application-start-date],
                    [user-milestones-application-complete-date]
                ) / 86400
            ),
            " days, ",
            FLOOR(
                MOD(
                    DATE_DIFF(
                        "second",
                        [user-milestones-application-start-date],
                        [user-milestones-application-complete-date]
                    ),
                    86400
                ) / 3600
            ),
            " hours, ",
            FLOOR(
                MOD(
                    DATE_DIFF(
                        "second",
                        [user-milestones-application-start-date],
                        [user-milestones-application-complete-date]
                    ),
                    3600
                ) / 60
            ),
            " min, ",
            MOD(
                DATE_DIFF(
                    "second",
                    [user-milestones-application-start-date],
                    [user-milestones-application-complete-date]
                ),
                60
            ),
            " seconds"
        )
    )
)
```

**Why this is stronger**
- Returns blank when either endpoint is blank.
- Returns blank when completion precedes start instead of displaying a negative decomposition.
- Uses remainder arithmetic consistently.

**Assumptions and limits**
- Confirm both fields resolve to compatible datetimes and whether seconds-level precision is needed.

**Evaluate checks**
- Same timestamp, one second, 59/60 seconds, 23:59:59, exactly one day, blank endpoint, and completion before start.


## URLs and source attribution


### Website-search source segment or URL taxonomy lookup

**Context:** Import

Return a supplied source-segment GUID for URLs containing `?s=`; otherwise remove the query string and map the base URL to a taxonomy GUID.

<!-- formula-lint: standard -->
```text
IF(
    TRIM([C2]) = "",
    "",
    IF(
        CONTAINS([C2], "?s=") = TRUE,
        "school.taxonomy.845210",
        TAXONOMY_MAP(
            TRIM(SPLIT_INDEX([C2], "?", 1)),
            "name",
            "guid",
            ""
        )
    )
)
```

**Why this is stronger**
- Uses an exact `CONTAINS(...)=TRUE` check instead of a broad regex.
- Trims the base URL before mapping.
- Returns blank for blank input.

**Assumptions and limits**
- Replace the fictional taxonomy GUID and verify whether search parameters can appear as `&s=` rather than only `?s=`.

**Evaluate checks**
- Blank, plain URL, UTM query, `?s=` query, additional parameters, uppercase parameter, and unmapped URL.

### Extract website search query

**Context:** Import

Extract the value after `?s=`, stop at the next `&`, replace plus signs with spaces, and trim the result.

<!-- formula-lint: standard -->
```text
IF(
    CONTAINS(
        [C2],
        "?s="
    )
    = TRUE,
    TRIM(
        REGEXP_REPLACE(
            SPLIT_INDEX(
                SPLIT_INDEX(
                    [C2],
                    "?s=",
                    2
                ),
                "&",
                1
            ),
            "\+",
            " "
        )
    ),
    ""
)
```

**Why this is stronger**
- Stops before later query parameters instead of consuming the rest of the URL.
- Returns blank when no search parameter is present.

**Assumptions and limits**
- The literal-plus regex escape is parser-sensitive; test this small formula directly in the import formula evaluator.
- This does not percent-decode values such as `%20` unless a supported decoding pattern is added and verified.

**Evaluate checks**
- One word, multiple plus-separated words, a later `&` parameter, `%20`, blank, and no `?s=`.

### Return an unmapped source name

**Context:** Import

Strip the query string, test whether the base URL maps to a taxonomy GUID, and return the original base URL only when no match exists.

<!-- formula-lint: standard -->
```text
IF(
    TRIM(SPLIT_INDEX([C2], "?", 1)) = "",
    "",
    IF(
        TAXONOMY_MAP(
            TRIM(SPLIT_INDEX([C2], "?", 1)),
            "name",
            "guid",
            "NO_MATCH"
        ) = "NO_MATCH",
        TRIM(SPLIT_INDEX([C2], "?", 1)),
        ""
    )
)
```

**Why this is stronger**
- Uses a conspicuous sentinel only inside the map test.
- Avoids repeating untrimmed source text in the result.

**Assumptions and limits**
- Choose a sentinel that cannot be a real taxonomy output in the target map.

**Evaluate checks**
- Blank, mapped base URL, unmapped base URL, URL with query, and literal text equal to the sentinel.

### Exact URL match

**Context:** Import or Export

Return `Y` only for one exact normalized URL.

<!-- formula-lint: export -->
```text
IF(
    TRIM([C1]) = "https://apply.example.edu/dashboard/",
    "Y",
    "N"
)
```

**Why this is stronger**
- Uses equality instead of a slash-delimited regex that could be interpreted as pattern delimiters.
- Trims surrounding whitespace.

**Assumptions and limits**
- Decide whether protocol, host case, trailing slash, fragments, or query strings should be normalized.

**Evaluate checks**
- Exact URL, missing trailing slash, HTTP instead of HTTPS, query string, surrounding whitespace, and blank.


## Text, address, and list cleanup


### Append two fields without stray separators

**Context:** Workflow/Rule Formula Field or Export

Preserve the first value when the second is blank, use the second when the first is blank, and join both with `, ` when both exist.

<!-- formula-lint: export -->
```text
IF(
    TRIM([user-custom-field-website-searches-2]) = "",
    TRIM([user-custom-field-web-searches]),
    IF(
        TRIM([user-custom-field-web-searches]) = "",
        TRIM([user-custom-field-website-searches-2]),
        CONCAT(
            TRIM([user-custom-field-web-searches]),
            ", ",
            TRIM([user-custom-field-website-searches-2])
        )
    )
)
```

**Why this is stronger**
- Reduces four branches to two nested decisions.
- Trims each source before blank checks and concatenation.

**Assumptions and limits**
- This does not de-duplicate equal values; add an exact normalized equality branch when duplicates are possible.

**Evaluate checks**
- Both blank, first only, second only, both, whitespace-only values, and equal values.

### Conservative Address 2 duplicate removal

**Context:** Export

Return blank only when normalized Address 2 is blank or exactly equals Address 1; otherwise preserve Address 2.

<!-- formula-lint: export -->
```text
IF(
    TRIM([user-addresses-home-street2]) = "",
    "",
    IF(
        LOWER(TRIM([user-addresses-home-street1])) = LOWER(TRIM([user-addresses-home-street2])),
        "",
        TRIM([user-addresses-home-street2])
    )
)
```

**Why this is stronger**
- Eliminates the dangerous first-three-character heuristic, which can delete legitimate unit or building information.
- Normalizes case and surrounding whitespace for full-value equality.

**Assumptions and limits**
- This is duplicate detection, not a complete Address 2 validator.
- Do not attempt aggressive address classification without a supplied policy and representative bad/good examples.

**Evaluate checks**
- Exact duplicate, case-only duplicate, surrounding spaces, `Apt 2`, another full address, blank Address 2, and similar first three characters.

### Five-digit ZIP normalization

**Context:** Export

Remove spaces and hyphens, pad a missing leading zero for four- or eight-character inputs, and return the first five characters for valid five- or nine-character forms.

<!-- formula-lint: export -->
```text
IF(
    REGEXP_REPLACE(
        REGEXP_REPLACE(TRIM([user-addresses-home-zip]), "-", ""),
        " ",
        ""
    ) = "",
    "",
    IF(
        STRLEN(
            REGEXP_REPLACE(
                REGEXP_REPLACE(TRIM([user-addresses-home-zip]), "-", ""),
                " ",
                ""
            )
        ) = 4,
        PAD(
            REGEXP_REPLACE(
                REGEXP_REPLACE(TRIM([user-addresses-home-zip]), "-", ""),
                " ",
                ""
            ),
            "0",
            5
        ),
        IF(
            STRLEN(
                REGEXP_REPLACE(
                    REGEXP_REPLACE(TRIM([user-addresses-home-zip]), "-", ""),
                    " ",
                    ""
                )
            ) = 5,
            REGEXP_REPLACE(
                REGEXP_REPLACE(TRIM([user-addresses-home-zip]), "-", ""),
                " ",
                ""
            ),
            IF(
                STRLEN(
                    REGEXP_REPLACE(
                        REGEXP_REPLACE(TRIM([user-addresses-home-zip]), "-", ""),
                        " ",
                        ""
                    )
                ) = 8,
                SUBSTR(
                    PAD(
                        REGEXP_REPLACE(
                            REGEXP_REPLACE(TRIM([user-addresses-home-zip]), "-", ""),
                            " ",
                            ""
                        ),
                        "0",
                        9
                    ),
                    0,
                    5
                ),
                IF(
                    STRLEN(
                        REGEXP_REPLACE(
                            REGEXP_REPLACE(TRIM([user-addresses-home-zip]), "-", ""),
                            " ",
                            ""
                        )
                    ) = 9,
                    SUBSTR(
                        REGEXP_REPLACE(
                            REGEXP_REPLACE(TRIM([user-addresses-home-zip]), "-", ""),
                            " ",
                            ""
                        ),
                        0,
                        5
                    ),
                    ""
                )
            )
        )
    )
)
```

**Why this is stronger**
- Uses text `"0"` as the pad character.
- Defines behavior for 4, 5, 8, and 9 cleaned characters and rejects other lengths.
- Does not silently truncate arbitrary long input.

**Assumptions and limits**
- This length-based formula does not prove that every character is numeric. Export-safe digit validation would need a Preview-compatible tested pattern.

**Evaluate checks**
- Blank, 4/5/8/9 digits, ZIP+4 with hyphen, spaces, letters, 3 digits, and 10 digits.

### Build a clean list from exact delimited selections

**Context:** Import

Return a comma-separated subset of seven fictional allowed values without leading, trailing, or empty commas.

<!-- formula-lint: standard -->
```text
REGEXP_REPLACE(
    CONCAT(
        IF(
            CONTAINS(CONCAT(",", [C29], ","), ",White,") = TRUE,
            ",White",
            ""
        ),
        IF(
            CONTAINS(CONCAT(",", [C29], ","), ",Black/African American,") = TRUE,
            ",Black/African American",
            ""
        ),
        IF(
            CONTAINS(CONCAT(",", [C29], ","), ",Hispanic/Latino,") = TRUE,
            ",Hispanic/Latino",
            ""
        ),
        IF(
            CONTAINS(CONCAT(",", [C29], ","), ",Asian,") = TRUE,
            ",Asian",
            ""
        ),
        IF(
            CONTAINS(CONCAT(",", [C29], ","), ",American Indian/Alaska Native,") = TRUE,
            ",American Indian/Alaska Native",
            ""
        ),
        IF(
            CONTAINS(CONCAT(",", [C29], ","), ",Not Specified,") = TRUE,
            ",Not Specified",
            ""
        ),
        IF(
            CONTAINS(CONCAT(",", [C29], ","), ",Native Hawaiian/Oth Pac Island,") = TRUE,
            ",Native Hawaiian/Oth Pac Island",
            ""
        )
    ),
    "^,",
    ""
)
```

**Why this is stronger**
- Each output item includes its own leading comma; one final replacement removes only the first comma.
- Uses comma boundaries to avoid matching a selected value merely as a substring of another value.
- Every boolean helper is compared explicitly to `TRUE`.

**Assumptions and limits**
- The source must be a comma-delimited text list with no unexpected spaces around delimiters; normalize its delimiter format when necessary.
- Change `TRUE` to the observed boolean representation if Evaluate shows text booleans.

**Evaluate checks**
- No values, one value, several nonadjacent values, all values, substring collision, duplicates, and spaces after commas.


## Demographic and name output


### Race and ethnicity display with explicit precedence

**Context:** Export

Return `Hispanic of any race` first when the supplied ethnicity flag is true; otherwise return unspecified, two-or-more-races, or the single selected race text.

<!-- formula-lint: export -->
```text
IF(
    [user-race-hispanic] = "TRUE",
    "Hispanic of any race",
    IF(
        CHECKBOX_CHECKED([user-race-categories], ",") = "",
        "Unspecified",
        IF(
            SPLIT_INDEX(
                CHECKBOX_CHECKED([user-race-categories], ","),
                ",",
                2
            ) <> "",
            "Two or More Races",
            CHECKBOX_CHECKED([user-race-categories], ",")
        )
    )
)
```

**Why this is stronger**
- Does not incorrectly classify Hispanic plus one race as two or more races.
- Detects multiple race selections by checking for a second comma-delimited value.
- Returns the selected race text rather than assuming numeric option codes.

**Assumptions and limits**
- This is one reporting policy; some downstream systems require race and ethnicity in separate columns.
- Verify whether the Hispanic field returns `"TRUE"`, raw `TRUE`, `Y`, or another value.
- Verify the exact text returned by `CHECKBOX_CHECKED`.

**Evaluate checks**
- Hispanic with no race, Hispanic with one/multiple races, non-Hispanic with none/one/multiple races, and blank ethnicity.

### Preferred general title casing

**Context:** Import, Export, or Workflow/Rule Formula Field

Trim and title-case a general text value.

<!-- formula-lint: export -->
```text
IF(
    TRIM([user-custom-field-example-text]) = "",
    "",
    TITLECASE(TRIM([user-custom-field-example-text]))
)
```

**Why this is stronger**
- Uses the documented `TITLECASE` function rather than a hand-written two-part-name tree.
- Handles an arbitrary number of space-separated words more compactly.

**Assumptions and limits**
- Test apostrophes, hyphens, particles such as `de` or `van`, suffixes, all-caps abbreviations, and non-English names; title case is not a full name-normalization policy.

**Evaluate checks**
- Blank, one word, multiple words, hyphen, apostrophe, suffix, and all-caps input.

### Simple single-token capitalization fallback

**Context:** Import, Export, or Workflow/Rule Formula Field

Uppercase the first character and lowercase the remainder.

<!-- formula-lint: export -->
```text
IF(
    TRIM(
        [user-custom-field-example-text]
    )
    = "",
    "",
    IF(
        STRLEN(
            TRIM(
                [user-custom-field-example-text]
            )
        )
        = 1,
        UPPER(
            TRIM(
                [user-custom-field-example-text]
            )
        ),
        CONCAT(
            UPPER(
                LEFT(
                    TRIM(
                        [user-custom-field-example-text]
                    ),
                    1
                )
            ),
            LOWER(
                RIGHT(
                    TRIM(
                        [user-custom-field-example-text]
                    ),
                    STRLEN(
                        TRIM(
                            [user-custom-field-example-text]
                        )
                    )
                    - 1
                )
            )
        )
    )
)
```

**Why this is stronger**
- The old example failed to lowercase the remainder; this version does.
- Blank input is guarded.

**Assumptions and limits**
- Use only for a single token or when the destructive lowercasing policy is explicitly desired. Prefer `TITLECASE` for general text.

**Evaluate checks**
- Blank, one character, lowercase, uppercase, mixed case, space-separated, hyphenated, and apostrophe-containing input.


## Root-field selection

The previous example embedded one enormous application-root formula without consistently proving that each planned occurrence existed. It has been replaced by a separately maintained, statically linted example that:

- scans ten occurrences of one supplied application GUID;
- guards each raw nth occurrence before inspecting it;
- isolates the same application object before checking the excluded major and timestamp;
- includes applications whose optional major is missing;
- selects the newest numeric millisecond timestamp;
- converts the winner to **integer** epoch seconds;
- returns blank for the common zero-epoch sentinel; and
- avoids square-bracket regex classes in an export formula.

Read `references/root-field-example-latest-application.md` before adapting it. For milestone `type` scans that require prefix/suffix reconstruction, also read `references/root-field-occurrence-guards.md`.

## Maintenance rules

When adding or revising an example:

1. Remove tenant identifiers, custom slugs, domains, business thresholds, and named institutional policies.
2. State the formula context and destination type.
3. Define blank, invalid, threshold, no-match, and tie behavior.
4. Add `<!-- formula-lint: standard -->` or `<!-- formula-lint: export -->` immediately before the formula fence.
5. Run `scripts/lint_reference_formulas.py` on the edited reference.
6. Do not call a formula verified unless Element451 Evaluate or user-reported runtime output proves it.
7. For exports, require Preview Export in addition to Test Formula.
8. Record generalized runtime lessons in the relevant parsing/testing reference, not institution-specific values.
