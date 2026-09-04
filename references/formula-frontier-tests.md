# Advanced formula frontier tests

## Table of contents

- [Purpose and evidence level](#purpose-and-evidence-level)
- [Test 1: normalize two input date formats](#test-1-normalize-two-input-date-formats)
- [Test 1B: strict date validation by round-trip](#test-1b-strict-date-validation-by-round-trip)
- [Test 2: next birthday with a leap-day policy](#test-2-next-birthday-with-a-leap-day-policy)
- [Test 3: DST-aware modern US Eastern conversion](#test-3-dst-aware-modern-us-eastern-conversion)
- [How to report results](#how-to-report-results)

## Purpose and evidence level

These formulas intentionally probe behaviors that are easy to get wrong or not fully established by ordinary examples. They are **design targets**: each is static-lint clean, but none should be promoted to a production pattern until Element451 runtime testing confirms the expected behavior.

Test one layer at a time. Record the exact context and distinguish Test Formula/Evaluate from actual Preview Export or a persisted workflow write.

## Test 1: normalize two input date formats

**Context:** Import

**Evidence level:** **User-verified in Import Preview (August 2026).**

**Verified behavior:** `DATE_READ` is a parser/normalizer, not a strict calendar validator. When the reconstructed date contains overflowing components, Element can roll those components into a later valid date instead of rejecting the input.

The formula accepts either `YYYY-M-D` with hyphens or `M/D/YYYY` with slashes, pads components, and returns a parsed date value. It deliberately rejects inputs with neither delimiter.

<!-- formula-lint: standard -->
```text
IF(
    TRIM([C1]) = "",
    "",
    IF(
        CONTAINS([C1], "-") = TRUE,
        DATE_READ(
            CONCAT(
                PAD(VAL(SPLIT_INDEX(TRIM([C1]), "-", 1)), "0", 4),
                "-",
                PAD(VAL(SPLIT_INDEX(TRIM([C1]), "-", 2)), "0", 2),
                "-",
                PAD(VAL(SPLIT_INDEX(TRIM([C1]), "-", 3)), "0", 2)
            ),
            "Y-m-d"
        ),
        IF(
            CONTAINS([C1], "/") = TRUE,
            DATE_READ(
                CONCAT(
                    PAD(VAL(SPLIT_INDEX(TRIM([C1]), "/", 1)), "0", 2),
                    "/",
                    PAD(VAL(SPLIT_INDEX(TRIM([C1]), "/", 2)), "0", 2),
                    "/",
                    PAD(VAL(SPLIT_INDEX(TRIM([C1]), "/", 3)), "0", 4)
                ),
                "m/d/Y"
            ),
            ""
        )
    )
)
```

**Test matrix**

| Input | Verified Import Preview result |
|---|---|
| `2026-9-3` | `2026-09-03T00:00:00+00:00` |
| `09/03/2026` | `2026-09-03T00:00:00+00:00` |
| `9/3/2026` | `2026-09-03T00:00:00+00:00` |
| blank | `EMPTY` |
| `2026/09/03` | `EMPTY` |
| `02/29/2025` | `2025-03-01T00:00:00+00:00` |
| `2026-13-40` | `2027-02-09T00:00:00+00:00` |
| `September 3, 2026` | `EMPTY` |

**Reusable lesson:** Never use successful `DATE_READ` output alone as proof that an input date was valid. For strict validation, normalize the input to a canonical string, parse it, format the parsed value back to the same canonical format, and compare the two. If they differ, the original date contained an invalid or overflowing component.

These results are verified for **Import Preview**. Re-test if strict behavior in another formula context materially matters.

## Test 1B: strict date validation by round-trip

**Context:** Import

**Purpose:** Turn the Test 1 discovery into a reusable strict validator. Accept `YYYY-M-D` or `M/D/YYYY`, but return blank when `DATE_READ` normalizes the input into a different calendar date.

**Evidence level:** **Round-trip validation technique user-verified in Import Preview (August 2026)** for the focused `M/D/YYYY` probe below. The complete two-format date-returning formula remains partially unverified because the exact runtime test used `VALID`/`INVALID` output and exercised the slash-delimited branch.

<!-- formula-lint: standard -->
```text
IF(
    TRIM([C1]) = "",
    "",
    IF(
        CONTAINS([C1], "-") = TRUE,
        IF(
            DATE_FORMAT(
                DATE_READ(
                    CONCAT(
                        PAD(VAL(SPLIT_INDEX(TRIM([C1]), "-", 1)), "0", 4),
                        "-",
                        PAD(VAL(SPLIT_INDEX(TRIM([C1]), "-", 2)), "0", 2),
                        "-",
                        PAD(VAL(SPLIT_INDEX(TRIM([C1]), "-", 3)), "0", 2)
                    ),
                    "Y-m-d"
                ),
                "Y-m-d"
            )
            =
            CONCAT(
                PAD(VAL(SPLIT_INDEX(TRIM([C1]), "-", 1)), "0", 4),
                "-",
                PAD(VAL(SPLIT_INDEX(TRIM([C1]), "-", 2)), "0", 2),
                "-",
                PAD(VAL(SPLIT_INDEX(TRIM([C1]), "-", 3)), "0", 2)
            ),
            DATE_READ(
                CONCAT(
                    PAD(VAL(SPLIT_INDEX(TRIM([C1]), "-", 1)), "0", 4),
                    "-",
                    PAD(VAL(SPLIT_INDEX(TRIM([C1]), "-", 2)), "0", 2),
                    "-",
                    PAD(VAL(SPLIT_INDEX(TRIM([C1]), "-", 3)), "0", 2)
                ),
                "Y-m-d"
            ),
            ""
        ),
        IF(
            CONTAINS([C1], "/") = TRUE,
            IF(
                DATE_FORMAT(
                    DATE_READ(
                        CONCAT(
                            PAD(VAL(SPLIT_INDEX(TRIM([C1]), "/", 1)), "0", 2),
                            "/",
                            PAD(VAL(SPLIT_INDEX(TRIM([C1]), "/", 2)), "0", 2),
                            "/",
                            PAD(VAL(SPLIT_INDEX(TRIM([C1]), "/", 3)), "0", 4)
                        ),
                        "m/d/Y"
                    ),
                    "m/d/Y"
                )
                =
                CONCAT(
                    PAD(VAL(SPLIT_INDEX(TRIM([C1]), "/", 1)), "0", 2),
                    "/",
                    PAD(VAL(SPLIT_INDEX(TRIM([C1]), "/", 2)), "0", 2),
                    "/",
                    PAD(VAL(SPLIT_INDEX(TRIM([C1]), "/", 3)), "0", 4)
                ),
                DATE_READ(
                    CONCAT(
                        PAD(VAL(SPLIT_INDEX(TRIM([C1]), "/", 1)), "0", 2),
                        "/",
                        PAD(VAL(SPLIT_INDEX(TRIM([C1]), "/", 2)), "0", 2),
                        "/",
                        PAD(VAL(SPLIT_INDEX(TRIM([C1]), "/", 3)), "0", 4)
                    ),
                    "m/d/Y"
                ),
                ""
            ),
            ""
        )
    )
)
```

**Test matrix**

| Input | Expected result |
|---|---|
| `2026-9-3` | 2026-09-03 date value |
| `09/03/2026` | 2026-09-03 date value |
| `9/3/2026` | 2026-09-03 date value |
| `02/29/2025` | blank |
| `2024-02-29` | 2024-02-29 date value |
| `2026-13-40` | blank |
| `2026-04-31` | blank |
| blank | blank |

**Verified focused probe results (Import Preview):**

| Input | Actual result |
|---|---|
| `9/3/2026` | `VALID` |
| `09/03/2026` | `VALID` |
| `2/29/2024` | `VALID` |
| `2/29/2025` | `INVALID` |
| `4/30/2026` | `VALID` |
| `4/31/2026` | `INVALID` |
| `13/40/2026` | `INVALID` |

**Verified conclusion:** In Import Preview, strict calendar validation can be implemented by canonicalizing the source date, parsing it with `DATE_READ`, formatting the parsed result back to the same canonical representation with `DATE_FORMAT`, and requiring exact equality. This catches both non-leap February 29 and overflowing month/day values that `DATE_READ` would otherwise normalize.

The complete two-format formula above should still be runtime-tested before treating both delimiter branches and the date-value return path as fully verified.

## Test 2: next birthday with a leap-day policy

**Context:** Export or Workflow/Rule Formula Field

**Evidence level:** **Core birthday/leap-year logic user-verified in Import Preview (August 2026)** using a deterministic two-column harness (`[C1]` DOB, `[C2]` simulated today). The exact Export/Workflow version below remains context-unverified because it uses `[user-dob]` and `DATE_DEFAULT`.

**Knowledge gap remaining:** Whether the same construction behaves identically in Export and Workflow/Rule Formula Field contexts, including `DATE_DEFAULT` and destination behavior.

Policy in this test: a February 29 birthday is observed on February 28 in a non-leap year; a birthday occurring today returns today rather than next year.

<!-- formula-lint: export -->
```text
IF(
    [user-dob] = "",
    "",
    IF(
        DATE_COMPARE(
            DATE_DEFAULT("Y-m-d"),
            "<=",
            CONCAT(
                DATE_DEFAULT("Y"),
                IF(
                    (DATE_FORMAT([user-dob], "m-d") = "02-29") &
                    (
                        (MOD(VAL(DATE_DEFAULT("Y")), 400) <> 0) &
                        (
                            (MOD(VAL(DATE_DEFAULT("Y")), 4) <> 0) |
                            (MOD(VAL(DATE_DEFAULT("Y")), 100) = 0)
                        )
                    ),
                    "-02-28",
                    DATE_FORMAT([user-dob], "-m-d")
                )
            )
        ) = TRUE,
        DATE_READ(
            CONCAT(
                DATE_DEFAULT("Y"),
                IF(
                    (DATE_FORMAT([user-dob], "m-d") = "02-29") &
                    (
                        (MOD(VAL(DATE_DEFAULT("Y")), 400) <> 0) &
                        (
                            (MOD(VAL(DATE_DEFAULT("Y")), 4) <> 0) |
                            (MOD(VAL(DATE_DEFAULT("Y")), 100) = 0)
                        )
                    ),
                    "-02-28",
                    DATE_FORMAT([user-dob], "-m-d")
                )
            ),
            "Y-m-d"
        ),
        DATE_READ(
            CONCAT(
                VAL(DATE_DEFAULT("Y")) + 1,
                IF(
                    (DATE_FORMAT([user-dob], "m-d") = "02-29") &
                    (
                        (MOD(VAL(DATE_DEFAULT("Y")) + 1, 400) <> 0) &
                        (
                            (MOD(VAL(DATE_DEFAULT("Y")) + 1, 4) <> 0) |
                            (MOD(VAL(DATE_DEFAULT("Y")) + 1, 100) = 0)
                        )
                    ),
                    "-02-28",
                    DATE_FORMAT([user-dob], "-m-d")
                )
            ),
            "Y-m-d"
        )
    )
)
```

**Test matrix**

- Ordinary birthday later this year.
- Ordinary birthday earlier this year.
- Birthday today.
- February 29 DOB evaluated in a non-leap year before, on, and after February 28.
- February 29 DOB evaluated in a leap year before, on, and after February 29.
- Century years 2100 and 2000 if a fixed test clock or equivalent isolated expressions can be used.
- Blank DOB.

The final policy may instead observe leap-day birthdays on March 1; that is a business-rule choice, not formula-engine knowledge.

### Verified deterministic Import harness results

A focused Import test replaced the live current date with a second input column so leap-year and boundary behavior could be tested deterministically. `[C1]` contained the DOB and `[C2]` contained simulated today, both in `Y-m-d` form. The harness used the same leap-year rule and birthday-selection structure as the formula above.

| DOB | Simulated today | Verified Import Preview result |
|---|---|---|
| `2000-10-15` | `2026-08-31` | `2026-10-15T00:00:00+00:00` |
| `2000-07-15` | `2026-08-31` | `2027-07-15T00:00:00+00:00` |
| `2000-08-31` | `2026-08-31` | `2026-08-31T00:00:00+00:00` |
| `2000-02-29` | `2025-02-27` | `2025-02-28T00:00:00+00:00` |
| `2000-02-29` | `2025-02-28` | `2025-02-28T00:00:00+00:00` |
| `2000-02-29` | `2025-03-01` | `2026-02-28T00:00:00+00:00` |
| `2000-02-29` | `2024-02-28` | `2024-02-29T00:00:00+00:00` |
| `2000-02-29` | `2024-02-29` | `2024-02-29T00:00:00+00:00` |
| `2000-02-29` | `2024-03-01` | `2025-02-28T00:00:00+00:00` |

**Verified conclusions in Import Preview:**

- The formula can correctly distinguish birthdays later this year, earlier this year, and exactly today.
- The standard Gregorian leap-year test using `MOD(year, 4)`, `MOD(year, 100)`, and `MOD(year, 400)` works for the exercised modern leap/non-leap cases.
- A February 29 policy can be implemented explicitly; the tested policy observes February 29 on February 28 in non-leap years.
- `DATE_COMPARE`, dynamic year reconstruction, `MOD`, `DATE_READ`, and `DATE_FORMAT` can cooperate correctly for these tested cases.
- Do not generalize this Import evidence to the exact `DATE_DEFAULT`/Export/Workflow formula until those contexts are separately tested.

## Test 3: DST-aware modern US Eastern conversion

**Context:** Export target; core transition logic is also being isolated with deterministic Import probes.

**Evidence level:** **End-to-end dynamic modern-US Eastern conversion user-verified in Import Preview (August 2026); Export-context parity still requires runtime verification.** Transition-day construction, ISO weekday numbering, literal second-level comparisons, epoch-millisecond `U` parsing, dynamic offset classification, offset application, and final local datetime formatting have all been verified at exact 2026 spring/fall transition seconds.

**Knowledge gap:** Does the same end-to-end design behave correctly in the target Export context, including Export Evaluate and actual Preview Export?

Input `[user-custom-field-event-time-ms]` is assumed to be a positive UTC epoch-millisecond value. The formula applies `-14400` only from the second Sunday in March at 07:00 UTC through the first Sunday in November before 06:00 UTC; otherwise it applies `-18000`.

<!-- formula-lint: export -->
```text
IF(
    (
        [user-custom-field-event-time-ms]=""
    )
    |(
        VAL(
            [user-custom-field-event-time-ms]
        )
        <=0
    ),
    "",
    DATE_FORMAT(
        DATE_READ(
            CONCAT(
                "",
                FLOOR(
                    VAL(
                        [user-custom-field-event-time-ms]
                    )
                    /1000
                )
                +IF(
                    (
                        DATE_COMPARE(
                            DATE_FORMAT(
                                DATE_READ(
                                    CONCAT(
                                        "",
                                        FLOOR(
                                            VAL(
                                                [user-custom-field-event-time-ms]
                                            )
                                            /1000
                                        )
                                    ),
                                    "U"
                                ),
                                "Y-m-d H:i:s"
                            ),
                            ">=",
                            CONCAT(
                                DATE_FORMAT(
                                    DATE_READ(
                                        CONCAT(
                                            "",
                                            FLOOR(
                                                VAL(
                                                    [user-custom-field-event-time-ms]
                                                )
                                                /1000
                                            )
                                        ),
                                        "U"
                                    ),
                                    "Y"
                                ),
                                "-03-",
                                PAD(
                                    1+MOD(
                                        7-VAL(
                                            DATE_FORMAT(
                                                DATE_READ(
                                                    CONCAT(
                                                        DATE_FORMAT(
                                                            DATE_READ(
                                                                CONCAT(
                                                                    "",
                                                                    FLOOR(
                                                                        VAL(
                                                                            [user-custom-field-event-time-ms]
                                                                        )
                                                                        /1000
                                                                    )
                                                                ),
                                                                "U"
                                                            ),
                                                            "Y"
                                                        ),
                                                        "-03-01"
                                                    ),
                                                    "Y-m-d"
                                                ),
                                                "N"
                                            )
                                        ),
                                        7
                                    )
                                    +7,
                                    "0",
                                    2
                                ),
                                " 07:00:00"
                            )
                        )
                        =TRUE
                    )
                    &(
                        DATE_COMPARE(
                            DATE_FORMAT(
                                DATE_READ(
                                    CONCAT(
                                        "",
                                        FLOOR(
                                            VAL(
                                                [user-custom-field-event-time-ms]
                                            )
                                            /1000
                                        )
                                    ),
                                    "U"
                                ),
                                "Y-m-d H:i:s"
                            ),
                            "<",
                            CONCAT(
                                DATE_FORMAT(
                                    DATE_READ(
                                        CONCAT(
                                            "",
                                            FLOOR(
                                                VAL(
                                                    [user-custom-field-event-time-ms]
                                                )
                                                /1000
                                            )
                                        ),
                                        "U"
                                    ),
                                    "Y"
                                ),
                                "-11-",
                                PAD(
                                    1+MOD(
                                        7-VAL(
                                            DATE_FORMAT(
                                                DATE_READ(
                                                    CONCAT(
                                                        DATE_FORMAT(
                                                            DATE_READ(
                                                                CONCAT(
                                                                    "",
                                                                    FLOOR(
                                                                        VAL(
                                                                            [user-custom-field-event-time-ms]
                                                                        )
                                                                        /1000
                                                                    )
                                                                ),
                                                                "U"
                                                            ),
                                                            "Y"
                                                        ),
                                                        "-11-01"
                                                    ),
                                                    "Y-m-d"
                                                ),
                                                "N"
                                            )
                                        ),
                                        7
                                    ),
                                    "0",
                                    2
                                ),
                                " 06:00:00"
                            )
                        )
                        =TRUE
                    ),
                    -14400,
                    -18000
                )
            ),
            "U"
        ),
        "Y-m-d H:i:s"
    )
)
```

**Critical transition tests**

For a known year under post-2007 US rules, test one second before, exactly at, and one second after:

- spring transition at 07:00:00 UTC on the second Sunday in March;
- fall transition at 06:00:00 UTC on the first Sunday in November.

Also test January, July, blank, zero, negative input, and a timestamp near local midnight. Confirm the exact expected local output independently before evaluating the formula.

**Limits**

- This implements modern US rules, not historical rules before 2007 and not every jurisdiction called “Eastern.”
- The static linter warns about fixed `-18000` and `-14400` literals even though this formula selects them seasonally; the warning is expected here.
- The `N` token is user-verified in Import Preview to follow standard PHP/ISO weekday numbering for the tested week: Monday=`1` through Sunday=`7`.
- `DATE_READ(..., "U")` is user-verified in Import Preview to preserve exact seconds for tested epoch-millisecond inputs after integer conversion to epoch seconds.
- The complete dynamic offset classifier and final adjusted local datetime are user-verified at exact 2026 DST boundaries in Import Preview. Re-test in Export before treating the Export implementation as user-verified.

### User-verified deterministic Import boundary probe

A focused Import formula used `[C1]` as a simulated UTC datetime in `Y-m-d H:i:s` form and returned only the chosen offset. It reused the same transition-day arithmetic as the larger formula above.

| UTC input | Expected offset | Verified Import Preview result |
|---|---:|---:|
| `2026-01-15 12:00:00` | `-18000` | `-18000` |
| `2026-03-08 06:59:59` | `-18000` | `-18000` |
| `2026-03-08 07:00:00` | `-14400` | `-18000` |
| `2026-03-08 07:00:01` | `-14400` | `-18000` |
| `2026-07-01 12:00:00` | `-14400` | `-14400` |
| `2026-11-01 05:59:59` | `-14400` | `-14400` |
| `2026-11-01 06:00:00` | `-18000` | `-14400` |
| `2026-11-01 06:00:01` | `-18000` | `-14400` |

**Revised conclusion after later diagnostics:** These results do **not** disprove the epoch-millisecond DST design. The deterministic harness itself used a `Y-m-d H:i:s` Import source column, and later user-verified testing showed that Element's Import Preview date path discarded the source time-of-day and treated the value as midnight. That explains why broad winter/summer dates looked correct while exact transition-hour tests failed. Keep the epoch-based DST formula **unverified**, not failed, until an epoch-millisecond boundary harness is tested.

### Test 3A: inspect weekday-token and transition-day construction

Use one Import row with `[C1]` containing any valid 2026 datetime, such as `2026-07-01 12:00:00`. This diagnostic returns the raw `N` token value for March 1 and November 1 plus the day numbers produced by the current transition arithmetic.

<!-- formula-lint: standard -->
```text
CONCAT(
    "MARCH_N=",
    DATE_FORMAT(
        DATE_READ(
            CONCAT(
                DATE_FORMAT(DATE_READ(TRIM([C1]), "Y-m-d H:i:s"), "Y"),
                "-03-01"
            ),
            "Y-m-d"
        ),
        "N"
    ),
    ";MARCH_DAY=",
    PAD(
        1 + MOD(
            7 - VAL(
                DATE_FORMAT(
                    DATE_READ(
                        CONCAT(
                            DATE_FORMAT(DATE_READ(TRIM([C1]), "Y-m-d H:i:s"), "Y"),
                            "-03-01"
                        ),
                        "Y-m-d"
                    ),
                    "N"
                )
            ),
            7
        ) + 7,
        "0",
        2
    ),
    ";NOV_N=",
    DATE_FORMAT(
        DATE_READ(
            CONCAT(
                DATE_FORMAT(DATE_READ(TRIM([C1]), "Y-m-d H:i:s"), "Y"),
                "-11-01"
            ),
            "Y-m-d"
        ),
        "N"
    ),
    ";NOV_DAY=",
    PAD(
        1 + MOD(
            7 - VAL(
                DATE_FORMAT(
                    DATE_READ(
                        CONCAT(
                            DATE_FORMAT(DATE_READ(TRIM([C1]), "Y-m-d H:i:s"), "Y"),
                            "-11-01"
                        ),
                        "Y-m-d"
                    ),
                    "N"
                )
            ),
            7
        ),
        "0",
        2
    )
)
```

**User-verified weekday-token probe (Import Preview, August 2026):**

```text
SUN=7;MON=1;TUE=2;WED=3;THU=4;FRI=5;SAT=6
```

This confirms that `DATE_FORMAT(..., "N")` follows the standard PHP/ISO weekday numbering for the tested dates: Monday=`1` through Sunday=`7`. Therefore the failed DST boundary behavior is **not** caused by a Sunday=`1` interpretation.

### Test 3B: verify constructed transitions and literal boundary comparisons

A second focused Import Preview probe removed `[C1]` entirely and returned the constructed 2026 DST transition datetimes plus direct `DATE_COMPARE` results one second before and exactly at each boundary.

**User-verified result (Import Preview, August 2026):**

```text
START=2026-03-08 07:00:00;END=2026-11-01 06:00:00;SPRING_BEFORE=F;SPRING_AT=T;FALL_BEFORE=T;FALL_AT=F
```

**Verified conclusions:**

- The current second-Sunday-in-March arithmetic correctly constructs `2026-03-08 07:00:00`.
- The current first-Sunday-in-November arithmetic correctly constructs `2026-11-01 06:00:00`.
- `DATE_COMPARE` distinguishes second-level boundaries correctly when both operands are direct `Y-m-d H:i:s` strings: one second before spring is false for `>=`, the exact spring instant is true, one second before fall is true for `<`, and the exact fall instant is false.
- The earlier failed offset-selection probe therefore is **not** explained by weekday numbering, transition-day construction, or basic second-level comparison semantics.
- The remaining investigation must isolate the `[C1]` input path: direct raw string comparison versus `DATE_READ` -> `DATE_FORMAT` round trip, and fixed literal boundary versus dynamically constructed boundary when the left-hand operand comes from the input row.

### Test 3C: source-column datetime coercion

A focused Import Preview probe compared six `Y-m-d H:i:s` source values around the 2026 spring/fall boundaries four ways: raw `[C1]` versus a fixed boundary, raw `[C1]` versus a dynamically constructed boundary, `DATE_READ`/`DATE_FORMAT` round-trip versus fixed, and round-trip versus dynamic.

**User-verified results (Import Preview, August 2026):**

| Source `[C1]` | Round-trip value | Spring `>= 07:00` behavior | Fall `< 06:00` behavior |
|---|---|---|---|
| `2026-03-08 06:59:59` | `2026-03-08 00:00:00` | false in all four comparison variants | true in all four variants |
| `2026-03-08 07:00:00` | `2026-03-08 00:00:00` | false in all four comparison variants | true in all four variants |
| `2026-03-08 07:00:01` | `2026-03-08 00:00:00` | false in all four comparison variants | true in all four variants |
| `2026-11-01 05:59:59` | `2026-11-01 00:00:00` | true in all four comparison variants | true in all four variants |
| `2026-11-01 06:00:00` | `2026-11-01 00:00:00` | true in all four comparison variants | true in all four variants |
| `2026-11-01 06:00:01` | `2026-11-01 00:00:00` | true in all four comparison variants | true in all four variants |

**Verified conclusions:**

- In this Import Preview harness, `DATE_READ(TRIM([C1]), "Y-m-d H:i:s")` did not preserve the source time; formatting the parsed value back always produced `00:00:00`.
- Passing `TRIM([C1])` directly to `DATE_COMPARE` did not rescue the time-of-day. Its results matched midnight semantics for all six tested rows.
- Fixed versus dynamically constructed right-hand boundaries produced identical results, so dynamic boundary construction is not the cause.
- Direct literal-to-literal `DATE_COMPARE` had already been verified to respect seconds, so this behavior is best treated as **Import Preview source-value/date coercion**, not a general `DATE_COMPARE` inability to compare times.
- Do not use a `Y-m-d H:i:s` Import source-column harness to validate exact-hour DST logic. Match the harness to the production representation. For an epoch-millisecond production formula, test epoch milliseconds.

### Test 3D: epoch-millisecond exact-boundary harness

**Context:** Import

**Purpose:** Test the same representation used by the production-oriented DST formula and determine whether `DATE_READ(..., "U")` preserves exact seconds when the source is numeric epoch milliseconds.

Use `[C1]` as UTC epoch milliseconds.

<!-- formula-lint: standard -->
```text
CONCAT(
    "UTC=",
    DATE_FORMAT(
        DATE_READ(
            CONCAT("", FLOOR(VAL([C1]) / 1000)),
            "U"
        ),
        "Y-m-d H:i:s"
    ),
    ";SPRING=",
    IF(
        DATE_COMPARE(
            DATE_FORMAT(
                DATE_READ(CONCAT("", FLOOR(VAL([C1]) / 1000)), "U"),
                "Y-m-d H:i:s"
            ),
            ">=",
            "2026-03-08 07:00:00"
        ) = TRUE,
        "T",
        "F"
    ),
    ";FALL=",
    IF(
        DATE_COMPARE(
            DATE_FORMAT(
                DATE_READ(CONCAT("", FLOOR(VAL([C1]) / 1000)), "U"),
                "Y-m-d H:i:s"
            ),
            "<",
            "2026-11-01 06:00:00"
        ) = TRUE,
        "T",
        "F"
    )
)
```

Test rows:

| Epoch ms | Expected UTC | Expected SPRING | Expected FALL |
|---:|---|---|---|
| `1772953199000` | `2026-03-08 06:59:59` | `F` | `T` |
| `1772953200000` | `2026-03-08 07:00:00` | `T` | `T` |
| `1772953201000` | `2026-03-08 07:00:01` | `T` | `T` |
| `1793512799000` | `2026-11-01 05:59:59` | `T` | `T` |
| `1793512800000` | `2026-11-01 06:00:00` | `T` | `F` |
| `1793512801000` | `2026-11-01 06:00:01` | `T` | `F` |

**User-verified results (Import Preview, August 2026):**

| Epoch ms | Verified UTC | Verified SPRING | Verified FALL |
|---:|---|---|---|
| `1772953199000` | `2026-03-08 06:59:59` | `F` | `T` |
| `1772953200000` | `2026-03-08 07:00:00` | `T` | `T` |
| `1772953201000` | `2026-03-08 07:00:01` | `T` | `T` |
| `1793512799000` | `2026-11-01 05:59:59` | `T` | `T` |
| `1793512800000` | `2026-11-01 06:00:00` | `T` | `F` |
| `1793512801000` | `2026-11-01 06:00:01` | `T` | `F` |

**Verified conclusions:**

- Converting epoch milliseconds with `FLOOR(VAL([C1]) / 1000)`, then parsing with `DATE_READ(..., "U")`, preserves second-level precision for the tested boundary values in Import Preview.
- The exact spring and fall boundary comparisons behave correctly when the left-hand datetime originates from epoch parsing.
- This is a materially safer test harness for sub-day calculations than passing `Y-m-d H:i:s` text through an Import source column, which was verified to coerce to midnight in the earlier probe.
- The next remaining layer is to combine the epoch-derived UTC datetime with the dynamically constructed transition boundaries in one offset-selection expression.

### Test 3E: combine epoch parsing with dynamic DST boundaries

**Context:** Import diagnostic for the Export-oriented design.

**Purpose:** Combine the individually verified pieces without yet applying the chosen offset to the epoch. A passing result establishes that the epoch-derived UTC datetime can be classified against dynamically constructed modern-US Eastern DST boundaries.

Use `[C1]` as positive UTC epoch milliseconds.

<!-- formula-lint: standard -->
```text
IF(
    ([C1] = "") | (VAL([C1]) <= 0),
    "",
    IF(
        (
            DATE_COMPARE(
                DATE_FORMAT(
                    DATE_READ(CONCAT("", FLOOR(VAL([C1]) / 1000)), "U"),
                    "Y-m-d H:i:s"
                ),
                ">=",
                CONCAT(
                    DATE_FORMAT(
                        DATE_READ(CONCAT("", FLOOR(VAL([C1]) / 1000)), "U"),
                        "Y"
                    ),
                    "-03-",
                    PAD(
                        1 + MOD(
                            7 - VAL(
                                DATE_FORMAT(
                                    DATE_READ(
                                        CONCAT(
                                            DATE_FORMAT(
                                                DATE_READ(CONCAT("", FLOOR(VAL([C1]) / 1000)), "U"),
                                                "Y"
                                            ),
                                            "-03-01"
                                        ),
                                        "Y-m-d"
                                    ),
                                    "N"
                                )
                            ),
                            7
                        ) + 7,
                        "0",
                        2
                    ),
                    " 07:00:00"
                )
            ) = TRUE
        )
        &
        (
            DATE_COMPARE(
                DATE_FORMAT(
                    DATE_READ(CONCAT("", FLOOR(VAL([C1]) / 1000)), "U"),
                    "Y-m-d H:i:s"
                ),
                "<",
                CONCAT(
                    DATE_FORMAT(
                        DATE_READ(CONCAT("", FLOOR(VAL([C1]) / 1000)), "U"),
                        "Y"
                    ),
                    "-11-",
                    PAD(
                        1 + MOD(
                            7 - VAL(
                                DATE_FORMAT(
                                    DATE_READ(
                                        CONCAT(
                                            DATE_FORMAT(
                                                DATE_READ(CONCAT("", FLOOR(VAL([C1]) / 1000)), "U"),
                                                "Y"
                                            ),
                                            "-11-01"
                                        ),
                                        "Y-m-d"
                                    ),
                                    "N"
                                )
                            ),
                            7
                        ),
                        "0",
                        2
                    ),
                    " 06:00:00"
                )
            ) = TRUE
        ),
        -14400,
        -18000
    )
)
```

Use the same six epoch-millisecond boundary rows from Test 3D. Expected offsets, in order: `-18000`, `-14400`, `-14400`, `-14400`, `-18000`, `-18000`.

**User-verified results (Import Preview, August 2026):**

| Epoch ms | Expected offset | Verified offset |
|---:|---:|---:|
| `1772953199000` | `-18000` | `-18000` |
| `1772953200000` | `-14400` | `-14400` |
| `1772953201000` | `-14400` | `-14400` |
| `1793512799000` | `-14400` | `-14400` |
| `1793512800000` | `-18000` | `-18000` |
| `1793512801000` | `-18000` | `-18000` |

**Verified conclusions:**

- The complete dynamic modern-US Eastern DST classifier works for all six tested exact-boundary epoch-millisecond values in Import Preview.
- The classifier switches from `-18000` to `-14400` exactly at `2026-03-08 07:00:00` UTC and back to `-18000` exactly at `2026-11-01 06:00:00` UTC.
- This verifies the combined use of epoch-millisecond conversion, `DATE_READ(..., "U")`, `DATE_FORMAT(..., "N")`, dynamic transition construction, `DATE_COMPARE`, compound `&`, and offset selection in this Import Preview harness.
- Do not yet generalize this result to the final local-datetime conversion or to Export. Those remain separate runtime layers.

### Test 3F: apply the selected Eastern offset and format the local datetime

**Context:** Import diagnostic for the Export-oriented design.

**Purpose:** Verify the final remaining runtime layer: add the dynamically selected EST/EDT offset to epoch seconds, parse the adjusted epoch with `DATE_READ(..., "U")`, and format the resulting Eastern local datetime.

Use `[C1]` as positive UTC epoch milliseconds.

<!-- formula-lint: standard -->
```text
IF(
    ([C1] = "") | (VAL([C1]) <= 0),
    "",
    DATE_FORMAT(
        DATE_READ(
            CONCAT(
                "",
                FLOOR(VAL([C1]) / 1000)
                + IF(
                    (
                        DATE_COMPARE(
                            DATE_FORMAT(
                                DATE_READ(CONCAT("", FLOOR(VAL([C1]) / 1000)), "U"),
                                "Y-m-d H:i:s"
                            ),
                            ">=",
                            CONCAT(
                                DATE_FORMAT(
                                    DATE_READ(CONCAT("", FLOOR(VAL([C1]) / 1000)), "U"),
                                    "Y"
                                ),
                                "-03-",
                                PAD(
                                    1 + MOD(
                                        7 - VAL(
                                            DATE_FORMAT(
                                                DATE_READ(
                                                    CONCAT(
                                                        DATE_FORMAT(
                                                            DATE_READ(CONCAT("", FLOOR(VAL([C1]) / 1000)), "U"),
                                                            "Y"
                                                        ),
                                                        "-03-01"
                                                    ),
                                                    "Y-m-d"
                                                ),
                                                "N"
                                            )
                                        ),
                                        7
                                    ) + 7,
                                    "0",
                                    2
                                ),
                                " 07:00:00"
                            )
                        ) = TRUE
                    )
                    &
                    (
                        DATE_COMPARE(
                            DATE_FORMAT(
                                DATE_READ(CONCAT("", FLOOR(VAL([C1]) / 1000)), "U"),
                                "Y-m-d H:i:s"
                            ),
                            "<",
                            CONCAT(
                                DATE_FORMAT(
                                    DATE_READ(CONCAT("", FLOOR(VAL([C1]) / 1000)), "U"),
                                    "Y"
                                ),
                                "-11-",
                                PAD(
                                    1 + MOD(
                                        7 - VAL(
                                            DATE_FORMAT(
                                                DATE_READ(
                                                    CONCAT(
                                                        DATE_FORMAT(
                                                            DATE_READ(CONCAT("", FLOOR(VAL([C1]) / 1000)), "U"),
                                                            "Y"
                                                        ),
                                                        "-11-01"
                                                    ),
                                                    "Y-m-d"
                                                ),
                                                "N"
                                            )
                                        ),
                                        7
                                    ),
                                    "0",
                                    2
                                ),
                                " 06:00:00"
                            )
                        ) = TRUE
                    ),
                    -14400,
                    -18000
                )
            ),
            "U"
        ),
        "Y-m-d H:i:s"
    )
)
```

Use the same six boundary rows. Expected Eastern local datetimes:

| UTC epoch ms | Expected Eastern local datetime |
|---:|---|
| `1772953199000` | `2026-03-08 01:59:59` |
| `1772953200000` | `2026-03-08 03:00:00` |
| `1772953201000` | `2026-03-08 03:00:01` |
| `1793512799000` | `2026-11-01 01:59:59` |
| `1793512800000` | `2026-11-01 01:00:00` |
| `1793512801000` | `2026-11-01 01:00:01` |

**User-verified results (Import Preview, August 2026):**

| UTC epoch ms | Expected Eastern local datetime | Verified Eastern local datetime |
|---:|---|---|
| `1772953199000` | `2026-03-08 01:59:59` | `2026-03-08 01:59:59` |
| `1772953200000` | `2026-03-08 03:00:00` | `2026-03-08 03:00:00` |
| `1772953201000` | `2026-03-08 03:00:01` | `2026-03-08 03:00:01` |
| `1793512799000` | `2026-11-01 01:59:59` | `2026-11-01 01:59:59` |
| `1793512800000` | `2026-11-01 01:00:00` | `2026-11-01 01:00:00` |
| `1793512801000` | `2026-11-01 01:00:01` | `2026-11-01 01:00:01` |

**Verified conclusions:**

- The complete modern-US Eastern conversion works end to end for all six tested exact-boundary epoch-millisecond values in Import Preview.
- The spring transition correctly jumps from `01:59:59` EST to `03:00:00` EDT at `2026-03-08 07:00:00` UTC.
- The fall transition correctly moves from `01:59:59` EDT back to `01:00:00` EST at `2026-11-01 06:00:00` UTC.
- Adding the dynamically selected `-14400` or `-18000` offset to integer epoch seconds, then reparsing with `DATE_READ(..., "U")` and formatting with `DATE_FORMAT`, preserves the intended local wall-clock time for the tested boundaries.
- This establishes an end-to-end DST-aware Import Preview pattern for post-2007 US Eastern rules when the source is positive UTC epoch milliseconds. It does not establish historical pre-2007 rules or non-US jurisdictions.
- Export Evaluate and actual Preview Export still require separate verification before calling the Export implementation user-verified.

## How to report results

For each formula, provide:

- formula context;
- exact input value;
- expected output;
- actual evaluated output or exact error;
- whether Preview Export or an actual write/payment was also tested; and
- whether the same result occurred on another record.

The completed advanced milestone-root reconstruction/count evidence is separated into `references/formula-frontier-root-tests.md` because the verified formula is long and should be loaded only for comparable root-field parsing/count work.
