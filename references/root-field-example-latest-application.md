# Latest matching application date: guarded root-field example

## Table of contents

- [Purpose](#purpose)
- [Business rule](#business-rule)
- [Formula](#formula)
- [Why the construction is safer](#why-the-construction-is-safer)
- [Transferable safeguards from the verified milestone-root work](#transferable-safeguards-from-the-verified-milestone-root-work)
- [Serializer assumptions](#serializer-assumptions)
- [Required replacements](#required-replacements)
- [Evaluate and Preview Export matrix](#evaluate-and-preview-export-matrix)
- [Evidence level](#evidence-level)

## Purpose

This is the complete replacement for the former long formula in `source-formula-examples.md`. It demonstrates a guarded latest-date scan over serialized `[user-applications-root]` data. The identifiers are fictional teaching values.

## Business rule

Among up to ten occurrences of application GUID `school.applications.48217`:

- reject only the exact major `school.major.73104`;
- allow an application whose `major` property is missing;
- require a `submitted_time` Mongo-style millisecond timestamp;
- select the newest numeric timestamp regardless of serialized order;
- return the date in UTC as `m/d/Y`; and
- return blank when no candidate qualifies.

## Formula

<!-- formula-lint: export -->
```text
REGEXP_REPLACE(
    REGEXP_REPLACE(
        DATE_FORMAT(
            DATE_READ(
                CONCAT(
                    "",
                    FLOOR(
                        MAX(
                            MAX(
                                MAX(
                                    IF(
                                        SPLIT_INDEX(
                                            [user-applications-root],
                                            "{""guid"":""school.applications.48217""",
                                            2
                                        ) = "",
                                        0,
                                        IF(
                                            SPLIT_INDEX(
                                                SPLIT_INDEX(
                                                    SPLIT_INDEX(
                                                        [user-applications-root],
                                                        "{""guid"":""school.applications.48217""",
                                                        2
                                                    ),
                                                    "},{""guid"":""",
                                                    1
                                                ),
                                                """major"":""school.major.73104""",
                                                2
                                            ) <> "",
                                            0,
                                            IF(
                                                SPLIT_INDEX(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                [user-applications-root],
                                                                "{""guid"":""school.applications.48217""",
                                                                2
                                                            ),
                                                            "},{""guid"":""",
                                                            1
                                                        ),
                                                        """submitted_time"":{""$date"":{""$numberLong"":""",
                                                        2
                                                    ),
                                                    """",
                                                    1
                                                ) = "",
                                                0,
                                                VAL(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                SPLIT_INDEX(
                                                                    [user-applications-root],
                                                                    "{""guid"":""school.applications.48217""",
                                                                    2
                                                                ),
                                                                "},{""guid"":""",
                                                                1
                                                            ),
                                                            """submitted_time"":{""$date"":{""$numberLong"":""",
                                                            2
                                                        ),
                                                        """",
                                                        1
                                                    )
                                                )
                                            )
                                        )
                                    ),
                                    IF(
                                        SPLIT_INDEX(
                                            [user-applications-root],
                                            "{""guid"":""school.applications.48217""",
                                            3
                                        ) = "",
                                        0,
                                        IF(
                                            SPLIT_INDEX(
                                                SPLIT_INDEX(
                                                    SPLIT_INDEX(
                                                        [user-applications-root],
                                                        "{""guid"":""school.applications.48217""",
                                                        3
                                                    ),
                                                    "},{""guid"":""",
                                                    1
                                                ),
                                                """major"":""school.major.73104""",
                                                2
                                            ) <> "",
                                            0,
                                            IF(
                                                SPLIT_INDEX(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                [user-applications-root],
                                                                "{""guid"":""school.applications.48217""",
                                                                3
                                                            ),
                                                            "},{""guid"":""",
                                                            1
                                                        ),
                                                        """submitted_time"":{""$date"":{""$numberLong"":""",
                                                        2
                                                    ),
                                                    """",
                                                    1
                                                ) = "",
                                                0,
                                                VAL(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                SPLIT_INDEX(
                                                                    [user-applications-root],
                                                                    "{""guid"":""school.applications.48217""",
                                                                    3
                                                                ),
                                                                "},{""guid"":""",
                                                                1
                                                            ),
                                                            """submitted_time"":{""$date"":{""$numberLong"":""",
                                                            2
                                                        ),
                                                        """",
                                                        1
                                                    )
                                                )
                                            )
                                        )
                                    )
                                ),
                                MAX(
                                    IF(
                                        SPLIT_INDEX(
                                            [user-applications-root],
                                            "{""guid"":""school.applications.48217""",
                                            4
                                        ) = "",
                                        0,
                                        IF(
                                            SPLIT_INDEX(
                                                SPLIT_INDEX(
                                                    SPLIT_INDEX(
                                                        [user-applications-root],
                                                        "{""guid"":""school.applications.48217""",
                                                        4
                                                    ),
                                                    "},{""guid"":""",
                                                    1
                                                ),
                                                """major"":""school.major.73104""",
                                                2
                                            ) <> "",
                                            0,
                                            IF(
                                                SPLIT_INDEX(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                [user-applications-root],
                                                                "{""guid"":""school.applications.48217""",
                                                                4
                                                            ),
                                                            "},{""guid"":""",
                                                            1
                                                        ),
                                                        """submitted_time"":{""$date"":{""$numberLong"":""",
                                                        2
                                                    ),
                                                    """",
                                                    1
                                                ) = "",
                                                0,
                                                VAL(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                SPLIT_INDEX(
                                                                    [user-applications-root],
                                                                    "{""guid"":""school.applications.48217""",
                                                                    4
                                                                ),
                                                                "},{""guid"":""",
                                                                1
                                                            ),
                                                            """submitted_time"":{""$date"":{""$numberLong"":""",
                                                            2
                                                        ),
                                                        """",
                                                        1
                                                    )
                                                )
                                            )
                                        )
                                    ),
                                    MAX(
                                        IF(
                                            SPLIT_INDEX(
                                                [user-applications-root],
                                                "{""guid"":""school.applications.48217""",
                                                5
                                            ) = "",
                                            0,
                                            IF(
                                                SPLIT_INDEX(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            [user-applications-root],
                                                            "{""guid"":""school.applications.48217""",
                                                            5
                                                        ),
                                                        "},{""guid"":""",
                                                        1
                                                    ),
                                                    """major"":""school.major.73104""",
                                                    2
                                                ) <> "",
                                                0,
                                                IF(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                SPLIT_INDEX(
                                                                    [user-applications-root],
                                                                    "{""guid"":""school.applications.48217""",
                                                                    5
                                                                ),
                                                                "},{""guid"":""",
                                                                1
                                                            ),
                                                            """submitted_time"":{""$date"":{""$numberLong"":""",
                                                            2
                                                        ),
                                                        """",
                                                        1
                                                    ) = "",
                                                    0,
                                                    VAL(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                SPLIT_INDEX(
                                                                    SPLIT_INDEX(
                                                                        [user-applications-root],
                                                                        "{""guid"":""school.applications.48217""",
                                                                        5
                                                                    ),
                                                                    "},{""guid"":""",
                                                                    1
                                                                ),
                                                                """submitted_time"":{""$date"":{""$numberLong"":""",
                                                                2
                                                            ),
                                                            """",
                                                            1
                                                        )
                                                    )
                                                )
                                            )
                                        ),
                                        IF(
                                            SPLIT_INDEX(
                                                [user-applications-root],
                                                "{""guid"":""school.applications.48217""",
                                                6
                                            ) = "",
                                            0,
                                            IF(
                                                SPLIT_INDEX(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            [user-applications-root],
                                                            "{""guid"":""school.applications.48217""",
                                                            6
                                                        ),
                                                        "},{""guid"":""",
                                                        1
                                                    ),
                                                    """major"":""school.major.73104""",
                                                    2
                                                ) <> "",
                                                0,
                                                IF(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                SPLIT_INDEX(
                                                                    [user-applications-root],
                                                                    "{""guid"":""school.applications.48217""",
                                                                    6
                                                                ),
                                                                "},{""guid"":""",
                                                                1
                                                            ),
                                                            """submitted_time"":{""$date"":{""$numberLong"":""",
                                                            2
                                                        ),
                                                        """",
                                                        1
                                                    ) = "",
                                                    0,
                                                    VAL(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                SPLIT_INDEX(
                                                                    SPLIT_INDEX(
                                                                        [user-applications-root],
                                                                        "{""guid"":""school.applications.48217""",
                                                                        6
                                                                    ),
                                                                    "},{""guid"":""",
                                                                    1
                                                                ),
                                                                """submitted_time"":{""$date"":{""$numberLong"":""",
                                                                2
                                                            ),
                                                            """",
                                                            1
                                                        )
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            ),
                            MAX(
                                MAX(
                                    IF(
                                        SPLIT_INDEX(
                                            [user-applications-root],
                                            "{""guid"":""school.applications.48217""",
                                            7
                                        ) = "",
                                        0,
                                        IF(
                                            SPLIT_INDEX(
                                                SPLIT_INDEX(
                                                    SPLIT_INDEX(
                                                        [user-applications-root],
                                                        "{""guid"":""school.applications.48217""",
                                                        7
                                                    ),
                                                    "},{""guid"":""",
                                                    1
                                                ),
                                                """major"":""school.major.73104""",
                                                2
                                            ) <> "",
                                            0,
                                            IF(
                                                SPLIT_INDEX(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                [user-applications-root],
                                                                "{""guid"":""school.applications.48217""",
                                                                7
                                                            ),
                                                            "},{""guid"":""",
                                                            1
                                                        ),
                                                        """submitted_time"":{""$date"":{""$numberLong"":""",
                                                        2
                                                    ),
                                                    """",
                                                    1
                                                ) = "",
                                                0,
                                                VAL(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                SPLIT_INDEX(
                                                                    [user-applications-root],
                                                                    "{""guid"":""school.applications.48217""",
                                                                    7
                                                                ),
                                                                "},{""guid"":""",
                                                                1
                                                            ),
                                                            """submitted_time"":{""$date"":{""$numberLong"":""",
                                                            2
                                                        ),
                                                        """",
                                                        1
                                                    )
                                                )
                                            )
                                        )
                                    ),
                                    IF(
                                        SPLIT_INDEX(
                                            [user-applications-root],
                                            "{""guid"":""school.applications.48217""",
                                            8
                                        ) = "",
                                        0,
                                        IF(
                                            SPLIT_INDEX(
                                                SPLIT_INDEX(
                                                    SPLIT_INDEX(
                                                        [user-applications-root],
                                                        "{""guid"":""school.applications.48217""",
                                                        8
                                                    ),
                                                    "},{""guid"":""",
                                                    1
                                                ),
                                                """major"":""school.major.73104""",
                                                2
                                            ) <> "",
                                            0,
                                            IF(
                                                SPLIT_INDEX(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                [user-applications-root],
                                                                "{""guid"":""school.applications.48217""",
                                                                8
                                                            ),
                                                            "},{""guid"":""",
                                                            1
                                                        ),
                                                        """submitted_time"":{""$date"":{""$numberLong"":""",
                                                        2
                                                    ),
                                                    """",
                                                    1
                                                ) = "",
                                                0,
                                                VAL(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                SPLIT_INDEX(
                                                                    [user-applications-root],
                                                                    "{""guid"":""school.applications.48217""",
                                                                    8
                                                                ),
                                                                "},{""guid"":""",
                                                                1
                                                            ),
                                                            """submitted_time"":{""$date"":{""$numberLong"":""",
                                                            2
                                                        ),
                                                        """",
                                                        1
                                                    )
                                                )
                                            )
                                        )
                                    )
                                ),
                                MAX(
                                    IF(
                                        SPLIT_INDEX(
                                            [user-applications-root],
                                            "{""guid"":""school.applications.48217""",
                                            9
                                        ) = "",
                                        0,
                                        IF(
                                            SPLIT_INDEX(
                                                SPLIT_INDEX(
                                                    SPLIT_INDEX(
                                                        [user-applications-root],
                                                        "{""guid"":""school.applications.48217""",
                                                        9
                                                    ),
                                                    "},{""guid"":""",
                                                    1
                                                ),
                                                """major"":""school.major.73104""",
                                                2
                                            ) <> "",
                                            0,
                                            IF(
                                                SPLIT_INDEX(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                [user-applications-root],
                                                                "{""guid"":""school.applications.48217""",
                                                                9
                                                            ),
                                                            "},{""guid"":""",
                                                            1
                                                        ),
                                                        """submitted_time"":{""$date"":{""$numberLong"":""",
                                                        2
                                                    ),
                                                    """",
                                                    1
                                                ) = "",
                                                0,
                                                VAL(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                SPLIT_INDEX(
                                                                    [user-applications-root],
                                                                    "{""guid"":""school.applications.48217""",
                                                                    9
                                                                ),
                                                                "},{""guid"":""",
                                                                1
                                                            ),
                                                            """submitted_time"":{""$date"":{""$numberLong"":""",
                                                            2
                                                        ),
                                                        """",
                                                        1
                                                    )
                                                )
                                            )
                                        )
                                    ),
                                    MAX(
                                        IF(
                                            SPLIT_INDEX(
                                                [user-applications-root],
                                                "{""guid"":""school.applications.48217""",
                                                10
                                            ) = "",
                                            0,
                                            IF(
                                                SPLIT_INDEX(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            [user-applications-root],
                                                            "{""guid"":""school.applications.48217""",
                                                            10
                                                        ),
                                                        "},{""guid"":""",
                                                        1
                                                    ),
                                                    """major"":""school.major.73104""",
                                                    2
                                                ) <> "",
                                                0,
                                                IF(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                SPLIT_INDEX(
                                                                    [user-applications-root],
                                                                    "{""guid"":""school.applications.48217""",
                                                                    10
                                                                ),
                                                                "},{""guid"":""",
                                                                1
                                                            ),
                                                            """submitted_time"":{""$date"":{""$numberLong"":""",
                                                            2
                                                        ),
                                                        """",
                                                        1
                                                    ) = "",
                                                    0,
                                                    VAL(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                SPLIT_INDEX(
                                                                    SPLIT_INDEX(
                                                                        [user-applications-root],
                                                                        "{""guid"":""school.applications.48217""",
                                                                        10
                                                                    ),
                                                                    "},{""guid"":""",
                                                                    1
                                                                ),
                                                                """submitted_time"":{""$date"":{""$numberLong"":""",
                                                                2
                                                            ),
                                                            """",
                                                            1
                                                        )
                                                    )
                                                )
                                            )
                                        ),
                                        IF(
                                            SPLIT_INDEX(
                                                [user-applications-root],
                                                "{""guid"":""school.applications.48217""",
                                                11
                                            ) = "",
                                            0,
                                            IF(
                                                SPLIT_INDEX(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            [user-applications-root],
                                                            "{""guid"":""school.applications.48217""",
                                                            11
                                                        ),
                                                        "},{""guid"":""",
                                                        1
                                                    ),
                                                    """major"":""school.major.73104""",
                                                    2
                                                ) <> "",
                                                0,
                                                IF(
                                                    SPLIT_INDEX(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                SPLIT_INDEX(
                                                                    [user-applications-root],
                                                                    "{""guid"":""school.applications.48217""",
                                                                    11
                                                                ),
                                                                "},{""guid"":""",
                                                                1
                                                            ),
                                                            """submitted_time"":{""$date"":{""$numberLong"":""",
                                                            2
                                                        ),
                                                        """",
                                                        1
                                                    ) = "",
                                                    0,
                                                    VAL(
                                                        SPLIT_INDEX(
                                                            SPLIT_INDEX(
                                                                SPLIT_INDEX(
                                                                    SPLIT_INDEX(
                                                                        [user-applications-root],
                                                                        "{""guid"":""school.applications.48217""",
                                                                        11
                                                                    ),
                                                                    "},{""guid"":""",
                                                                    1
                                                                ),
                                                                """submitted_time"":{""$date"":{""$numberLong"":""",
                                                                2
                                                            ),
                                                            """",
                                                            1
                                                        )
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        ) / 1000
                    )
                ),
                "U"
            ),
            "m-d-Y"
        ),
        "^(01-01-1970|12-31-1969)$",
        ""
    ),
    "-",
    "/"
)
```

## Why the construction is safer

- Every index from `2` through `11` first checks `SPLIT_INDEX([user-applications-root], <application marker>, index) = ""` and short-circuits to numeric `0` when absent.
- Each candidate is bounded before major or timestamp checks, preventing a later application from lending metadata to the current candidate.
- Only the exact excluded-major marker is rejected, so missing major remains valid.
- Invalid candidates are numeric `0`; valid candidates are numeric milliseconds.
- Nested binary `MAX` selects by time, not by textual order.
- `FLOOR(winning_ms / 1000)` prevents fractional Unix seconds from reaching `DATE_READ(..., "U")`.
- The no-match cleanup formats to `m-d-Y` before regex removal, avoiding slash-delimiter errors.
- The export formula contains no bracketed regex character classes such as `[.]` or `[0-9]`.

## Transferable safeguards from the verified milestone-root work

Although this application example itself remains application-context evidence as described below, the completed milestone-root test suite strengthens several parts of its architecture:

- **Raw occurrence guard first.** Do not isolate or inspect a planned nth application slot until the raw nth target-guid split is proven nonblank.
- **Same-object bounding.** Apply major, term, status, and timestamp checks only to the current bounded application object. Neighboring applications must not supply missing metadata.
- **Independent checks.** Do not depend on `major`, `term`, and timestamps appearing in a particular order unless the current application serializer proves that order.
- **Exact optional-value exclusion.** If only one exact major is excluded, reject that exact quoted marker; a different major and an allowed missing/null major shape should not fail merely because the property is blank.
- **Required-value null rejection.** If term or timestamp is required, an explicit null/blank/absent required marker invalidates that candidate without terminating the scan.
- **Later matches remain eligible.** An invalid first occurrence of the target application GUID must not prevent a later valid occurrence from winning.
- **Coverage is explicit.** Ten written target-guid slots cover ten matching occurrences, not an unlimited number.

The milestone tests do **not** prove that applications begin with `guid`, that the next-object delimiter is identical across contexts, or that this complete application formula has Preview parity. Re-derive those application-specific details from the current `[user-applications-root]` sample and verify the assembled formula in its target context.

## Serializer assumptions

This formula is not a universal JSON parser. It assumes the evaluated root text is compact and has these properties:

1. Each application object begins with `{"guid":"..."`.
2. The next application boundary is `},{"guid":"`.
3. `major` and `submitted_time` occur after `guid` in the same object.
4. The timestamp shape is `"submitted_time":{"$date":{"$numberLong":"<milliseconds>"}}`.
5. Positive timestamps are used.
6. Ten occurrences are sufficient for the requested application GUID.

Obtain a redacted real root-field sample and rebuild markers when whitespace, key order, null representation, or object boundaries differ.

## Required replacements

- `school.applications.48217` -> supplied application GUID.
- `school.major.73104` -> supplied excluded major GUID.
- Occurrence indexes `2` through `11` -> the requested maximum coverage.
- `m/d/Y` -> requested output format.
- UTC behavior -> requested and tested timezone policy.

Do not copy a term allow-list or semantic date mapping from another tenant. Add supplied term markers to every candidate only after verifying the real serialized term shape.

## Evaluate and Preview Export matrix

| Case | Expected result |
|---|---|
| No target application occurrence | Blank |
| One target application and nine absent planned slots | Its submitted date |
| Exact excluded major | Blank for that candidate |
| Different major | Candidate can qualify |
| Missing major property | Candidate can qualify |
| Missing submitted time | Candidate is ignored |
| Multiple valid applications in nonchronological serialized order | Newest timestamp |
| Ten valid occurrences | Newest of all ten |
| Eleven valid occurrences | The eleventh is outside coverage; increase the formula if required |
| Timestamp near UTC midnight | UTC calendar date unless a different tested timezone rule is added |
| Formula Test succeeds | Still run actual Preview Export |

## Evidence level

The generalized formula is **static-lint clean**. Its architecture incorporates user-verified lessons about occurrence guards, integer epoch seconds, preview tokenization, and sentinel cleanup, but the anonymized formula has not been claimed as runtime verified in another tenant. Treat the test matrix as expected behavior until Element451 confirms it.
