# Anonymized application-root export case study and Preview Export pitfalls

## Table of contents

- [Why this reference exists](#why-this-reference-exists)
- [Anonymized business rule](#anonymized-business-rule)
- [What worked](#what-worked)
- [Milestone-derived safeguards that also apply to application roots](#milestone-derived-safeguards-that-also-apply-to-application-roots)
- [What failed and why](#what-failed-and-why)
- [Reusable construction pattern](#reusable-construction-pattern)
- [Preview-safe allow-list guidance](#preview-safe-allow-list-guidance)
- [Timestamp and date lessons](#timestamp-and-date-lessons)
- [Complete five-slot count parity evidence](#complete-five-slot-count-parity-evidence)
- [No-match and regex-delimiter lessons](#no-match-and-regex-delimiter-lessons)
- [Debugging sequence](#debugging-sequence)
- [Superseding full-formula guidance](#superseding-full-formula-guidance)

## Why this reference exists

This reference is derived from a user-verified Element451 export formula case from August 2026. It is valuable because it exposed differences between **Test Formula/Evaluate** and the actual **Preview Export** compiler that were not obvious from the general formula documentation.

All institution-specific values have been replaced with fictional `school.*` identifiers and generalized descriptions. The runtime findings and formula architecture were reported as working before anonymization; the rewritten identifiers are teaching data and are not valid tenant configuration.

Use the behavior and architecture as reusable evidence. Replace every fictional field, GUID, allow-list value, and offset with values supplied or verified for the current tenant, then run both Evaluate and Preview Export.

## Anonymized business rule

The export repeats by person, not application, because non-applicants must remain in the export. The formula therefore parses `[user-applications-root]` as serialized text.

A qualifying application must:

- have application GUID `school.applications.48217`,
- **not** have major `school.major.73104`,
- still qualify when the `major` property is missing,
- have a term equal to one of:
  - `school.terms.59321`
  - `school.terms.59322`
  - `school.terms.61501`
  - `school.terms.61502`
  - `school.terms.60491`
- have `submitted_time`,
- compete with up to nine other occurrences of the same application GUID, with the newest numeric `submitted_time` winning.

The result must:

- return the winning submitted date as `m/d/Y`,
- use the fixed `-18000` second offset that matched the reporting tenant's observed Element time in the original case,
- return blank when no qualifying application exists.

The fixed `-18000` offset is **EST**, not DST-aware year-round Eastern Time.

## What worked

### 1. Search by the target application GUID, not by overall application position

Use occurrence indexes `2` through `11` after splitting on the exact target marker:

```text
"{""guid"":""school.applications.48217"""
```

This covers ten occurrences of that specific application GUID. Unrelated applications do not consume the ten slots.

### 2. Isolate each matching application before testing its properties

After moving to an occurrence, cut it off at the next application object:

```text
SPLIT_INDEX(
    SPLIT_INDEX(
        [user-applications-root],
        "{""guid"":""school.applications.48217""",
        <occurrence-index>
    ),
    "},{""guid"":""",
    1
)
```

Run the term, major, and `submitted_time` checks only against that isolated segment.

### 3. Exclude only the exact disallowed major marker

The rule is "major is not X," and a missing major is valid. Therefore, reject only when this exact marker occurs in the isolated application:

```text
"""major"":""school.major.73104"""
```

Do not extract a generic major and require it to be nonblank; that would incorrectly reject applications with no major.

### 4. Use numeric zero for invalid candidates and nested binary `MAX`

Each occurrence returns either its numeric 13-digit millisecond timestamp or `0`. Compare all candidates with nested two-argument `MAX` calls.

### 5. Convert only the winning millisecond timestamp to integer epoch seconds

Keep millisecond precision through `MAX`, then use the first ten digits of the winner before `DATE_READ(..., "U")`.

## Milestone-derived safeguards that also apply to application roots

The later verified milestone-root reconstruction/count work reinforced several rules already implicit in this application case study:

- prove the raw nth target occurrence exists before deeper parsing;
- bound one complete application object before checking its properties;
- keep all eligibility checks on that same object;
- treat exact optional-value exclusion separately from required-value presence;
- continue after an invalid occurrence because a later matching application can qualify; and
- state a fixed occurrence ceiling rather than implying an unbounded scan.

If a current `[user-applications-root]` sample no longer begins each object with `guid`, do not force the historical `},{"guid":"` delimiter. Reconstruct or bound the full object from markers derived from the current sample, following the same structural discipline that was runtime-verified for milestones. This is a transfer of parsing safeguards, not a claim that the milestone serializer and application serializer are identical.

## What failed and why

### Regex `[.]` worked in Test Formula but failed Preview Export

This term regex originally worked in Test Formula:

```text
"^school[.]terms[.](59321|59322|61501|61502|60491)$"
```

But Preview Export returned an undefined-token error. Element support explained that the export compiler interpreted `[.]` as a field token because bracket syntax is how Element represents fields such as `[user-email-address]`.

**Lesson:** In export formulas, square-bracket regex character classes can be tokenized even when they are inside quoted strings.

### Replacing `[.]` with `\.` removed the preview error but then matched nothing

The obvious regex rewrite passed token validation but caused all candidates to be rejected in this case.

**Lesson:** Do not assume familiar regex escaping survives Element's formula-string parser exactly as expected. Test the rewritten regex alone and then in Preview Export.

### A `CONTAINS` allow-list caused every term to qualify

A compact membership pattern using `CONTAINS` returned a date for applications regardless of term when used directly as the `IF` condition.

This is consistent with the broader Element caveat that boolean-returning helpers can behave differently depending on whether the runtime exposes a real boolean or a text-like boolean value. A nonempty false-like string may be truthy in a conditional context.

**Lesson:** Do not use a boolean helper directly inside `IF` unless its return form has been separately verified. For exact short allow-lists, explicit equality/OR logic is the safest general pattern.

### Fractional Unix seconds produced corrupted dates

Converting a 13-digit millisecond timestamp with:

```text
VAL(timestamp) / 1000
```

produced a decimal Unix value such as `1753128101.067`. Passing that to `DATE_READ(..., "U")` resulted in implausible years and a repeatedly incorrect July month.

**Lesson:** `DATE_READ(..., "U")` should receive integer epoch seconds. Use `FLOOR(ms / 1000)` or truncate the winning positive 13-digit timestamp to its first ten digits.

### Regex containing `/` produced `preg_replace(): Unknown modifier '3'`

Trying to remove the no-match sentinel with:

```text
"^12/31/1969$"
```

caused PHP regex delimiter parsing to treat the slash as syntax and later report modifier `3`.

**Lesson:** Prefer a zero guard before date conversion. If sentinel removal is necessary, avoid unescaped slash characters in the regex pattern and verify the exact pattern in Element.

## Reusable construction pattern

For each target-object occurrence:

```text
segment = isolate occurrence

if required allow-list value is invalid:
    candidate = 0
else if exact excluded optional value is present:
    candidate = 0
else if timestamp is missing:
    candidate = 0
else:
    candidate = numeric millisecond timestamp
```

Then:

```text
latest_ms = MAX(all candidates)
latest_seconds = integer seconds from latest_ms
local_seconds = latest_seconds + configured offset
formatted = DATE_FORMAT(DATE_READ(CONCAT("", local_seconds), "U"), "m/d/Y")
```

If there is no valid candidate, return blank before date conversion when practical.

## Preview-safe allow-list guidance

For small exact lists, the preferred general pattern is explicit equality:

```text
(
    (<term-expression> = "client.terms.100") |
    (<term-expression> = "client.terms.200") |
    (<term-expression> = "client.terms.300")
)
```

This is longer because Element does not provide variable binding, but it avoids:

- bracket-token collisions,
- regex escape ambiguity,
- substring membership errors,
- boolean coercion surprises from a membership helper.

In the original tenant formula, a compact anchored pattern of this shape also worked in both Test Formula and Preview Export. The identifiers shown here are fictional:

```text
"^school.terms.(59321|59322|61501|61502|60491)$"
```

The periods are regex wildcards in that pattern, not literal-dot escapes. It is acceptable here only because the fixed prefix and enumerated numeric suffixes make accidental matches unlikely enough for this known data shape. Do not generalize this as the universal way to match literal periods.

## Timestamp and date lessons

A Mongo-style timestamp looks like:

```json
"submitted_time":{"$date":{"$numberLong":"1753128101067"}}
```

Extract the 13-digit text, convert it to numeric for `MAX`, and keep milliseconds through selection.

After the winner is known:

```text
VAL(
    LEFT(
        CONCAT("", <winning-milliseconds>),
        10
    )
)
```

returns integer epoch seconds for positive 13-digit millisecond timestamps.

Then apply the verified offset and parse:

```text
DATE_FORMAT(
    DATE_READ(
        CONCAT("", <epoch-seconds> - 18000),
        "U"
    ),
    "m/d/Y"
)
```

Again, `-18000` is fixed EST and is not a correct year-round Eastern Time solution when dates can cross daylight-saving seasons.

## No-match and regex-delimiter lessons

The best architecture is:

```text
IF(
    <latest-ms> = 0,
    "",
    <date conversion>
)
```

When the `MAX` expression is so large that repeating it is impractical, the verified formula used a sentinel-removal fallback after date formatting. That is less elegant but avoided duplicating a huge expression.

Because `/` caused a `preg_replace` delimiter error, the verified cleanup pattern was:

```text
"^12.31.1969$"
```

where the dots act as regex wildcards matching the slashes in the formatted sentinel. This is an observed workaround, not a preferred general pattern.

## Complete five-slot count parity evidence

A September 2026 user-verified milestone-root export test established that a long reconstruction-based count formula can behave identically in Test Formula/Evaluate and actual Preview Export when its string patterns avoid Preview's bracket-tokenization trap. The tested architecture:

- enumerated the first five occurrences of a canonical milestone `type`;
- guarded absent raw occurrences before reconstruction;
- reconstructed each compact object from a bounded prefix and suffix;
- applied exact application, term allow-list, exact-major exclusion, and date-presence checks to the same object; and
- summed numeric `1`/`0` candidates.

The complete assembled formula returned `0`, `1`, `0`, `0`, `1`, `2`, `5`, and `5` across controlled zero-valid, one-valid, excluded-major, null-term, mixed-two, two-valid, five-valid, and six-valid cases. The user reported the same results in Evaluate and Preview Export. Treat this as **user-verified parity for the tested compact serializer shape**, not as proof that every root serializer or object-start marker is identical across tenants or contexts.

## Debugging sequence

For a formula like this, debug in this exact order:

1. Return `[user-applications-root]` itself.
2. Isolate one target GUID occurrence.
3. Return only its extracted term.
4. Test one allowed term by exact equality.
5. Test the full allow-list.
6. Test the excluded-major check on that same isolated object.
7. Return raw `submitted_time` text.
8. Return `VAL(submitted_time)`.
9. Combine two candidates with `MAX`.
10. Expand to all covered occurrences.
11. Return the winning 13-digit timestamp.
12. Convert the winner to integer epoch seconds.
13. Apply timezone offset and `m/d/Y` formatting.
14. Test a no-match user.
15. Run **actual Preview Export**, not only Test Formula.
16. If Preview alone fails with undefined tokens, inspect every square-bracket sequence inside quoted strings.

## Superseding full-formula guidance

The original historical formula is intentionally no longer embedded here as a copyable production example. It predated the skill's stronger requirement to guard every planned raw nth occurrence before deeper extraction, and its term-filter workaround was tied to one verified serialization/compiler case.

Use the observations in this case study as evidence, then construct a current formula from:

- `references/root-field-parsing.md` for object markers and boundaries;
- `references/root-field-occurrence-guards.md` for missing-occurrence safety;
- `references/root-field-selection.md` for count/latest/earliest/argmax architecture; and
- `references/root-field-example-latest-application.md` for a complete guarded, static-lint-clean application example.

If a supplied tenant rule also needs a term allow-list, add exact term checks to **every independently bounded candidate**, using user-supplied GUIDs, and test both Evaluate and Preview Export. Do not resurrect the historical wildcard-dot regex merely because it worked in one case.
