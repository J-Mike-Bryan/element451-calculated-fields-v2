# Parsing serialized Element451 root fields

## Table of contents

- [Scope and risk](#scope-and-risk)
- [Required inputs](#required-inputs)
- [Object-selection workflow](#object-selection-workflow)
- [Choose a canonical occurrence marker](#choose-a-canonical-occurrence-marker)
- [Applying the verified milestone lessons to `[user-applications-root]`](#applying-the-verified-milestone-lessons-to-user-applications-root)
- [Occurrence indexing](#occurrence-indexing)
- [Isolating one object](#isolating-one-object)
- [Guard missing nth occurrences before reconstruction](#guard-missing-nth-occurrences-before-reconstruction)
- [Testing inclusion and exclusion rules](#testing-inclusion-and-exclusion-rules)
- [Exact allow-lists and boolean traps](#exact-allow-lists-and-boolean-traps)
- [Export Preview tokenization gotcha](#export-preview-tokenization-gotcha)
- [Extracting timestamps](#extracting-timestamps)
- [Selecting the latest or earliest candidate](#selecting-the-latest-or-earliest-candidate)
- [Converting and formatting epoch values](#converting-and-formatting-epoch-values)
- [Eastern Time and daylight saving](#eastern-time-and-daylight-saving)
- [No-match handling](#no-match-handling)
- [Validation matrix](#validation-matrix)
- [Failure modes](#failure-modes)

## Scope and risk

Fields such as `[user-applications-root]` and `[user-milestones-root]` can expose serialized JSON-like text. The bundled sources do not document a general JSON parser for calculated fields. The working examples therefore use exact text markers, escaped quotes, repeated `SPLIT_INDEX`, numeric candidate values, and nested `MAX`.

This approach is fragile because it depends on the exact serialization:

- property names,
- quote escaping,
- property order when a delimiter assumes order,
- separators between objects,
- timestamp representation,
- whether missing properties are omitted or emitted as blank/null,
- the maximum number of occurrences covered by the formula.

Never write a production root-field formula from a guessed schema. Require a redacted sample of the actual field output or use a sample already supplied in the conversation.

## Required inputs

Before constructing the formula, identify all of the following:

1. Exact root field slug.
2. A representative raw value containing:
   - at least one matching object,
   - one nonmatching object,
   - the excluded value if any,
   - a missing optional property if that case must be included,
   - more than one matching timestamp if latest/earliest matters.
3. Exact object marker. Prefer the canonical discriminator that matches the business rule (for example milestone `type` or application `guid`) over a display/source `name` that can vary.
4. Exact include/exclude conditions.
5. Timestamp property and representation.
6. Whether to return first, last/latest, earliest, or all.
7. Maximum number of occurrences the formula must inspect.
8. Desired output format and timezone rule.
9. What to return when no valid match exists.

Preserve exact GUIDs and field names. Do not replace a user-supplied slug because its spelling looks wrong.

## Object-selection workflow

Use this architecture for a latest matching timestamp:

```text
for each occurrence i:
    segment_i = isolate the i-th matching object
    if segment_i is absent:
        candidate_i = 0
    else if segment_i contains the exact excluded value:
        candidate_i = 0
    else if timestamp is absent:
        candidate_i = 0
    else:
        candidate_i = numeric timestamp

latest = MAX of all candidate_i values

if latest = 0:
    return ""
else:
    convert latest to a date and format it
```

The loop above is design notation, not valid Element formula syntax. Element formulas require each occurrence expression to be written explicitly.

## Choose a canonical occurrence marker

Choose the marker from the field that actually defines eligibility, not from a convenient-looking label in one sample.

For milestone formulas, when the requirement says the milestone must have a specific `type`, enumerate occurrences with that exact type marker. For example, a deposit scan should prefer:

```text
"""type"":""DEPOSIT"""
```

over a name marker such as `Deposit Paid` or `Deposit Page`. Milestone names can differ by creation path. In an anonymized user-verified tenant record, a manually/import-created qualifying deposit was named `Client Import` while its canonical field remained `"type":"DEPOSIT"`. A formula that enumerated only `Deposit Pa...` therefore returned blank even though a valid deposit existed.

Use these rules:

- If the business rule says `type = DEPOSIT`, `ADMIT`, `WITHDRAW`, or another exact type, use that `type` as the occurrence marker.
- Do not use `name` as the primary occurrence marker merely because the first sample uses a familiar name. Use `name` only when the requirement itself is name-based or the user explicitly establishes that it is invariant.
- If multiple creation paths exist (manual entry, client import, landing page, system action), assume display/source names may vary until proven otherwise.
- Test at least one alternate-name object with the same canonical type.
- Derive the exact compact/spaced quoting from the real root sample.

### When the canonical marker is inside the object

A canonical type marker may occur after fields such as `application_guid`, `term`, and `major`, while `date` occurs after the type. In that layout, splitting on `"type":"DEPOSIT"` does not by itself return the full object. Treat the prefix and suffix as two halves of the **same occurrence**.

For the nth target occurrence:

1. Prove the nth type marker exists before doing any reconstruction.
2. Recover the current object's prefix from the segment immediately before that nth type marker, bounded from the last object-start marker in that segment.
3. Recover the current object's suffix from the segment immediately after that nth type marker, bounded before the next object.
4. Prefer reconstructing or logically pairing the **entire bounded object** before applying eligibility conditions when required-property order is not guaranteed.
5. Apply application, term, major, status, and other eligibility checks to that same full object. Extract a post-marker value such as `date` from the bounded suffix only when its location is actually part of the serializer contract.
6. If you concatenate prefix + type marker + suffix, keep the same existence guard around the entire reconstruction.

For milestone JSON where every object begins with `"name":`, a preview-safe prefix recovery pattern used successfully in August 2026 was conceptually:

```text
REGEXP_EXTRACT(
    SPLIT_INDEX([user-milestones-root], """type"":""DEPOSIT""", <segment-before-index>),
    ".*(""name"":.*)$"
)
```

Derive the object-start marker from the supplied sample instead of assuming `name` is always first. The regex above is an architecture example, not a universal serializer contract.

A controlled September 2026 formula evaluation verified this reconstruction sequence for one compact milestone serializer shape:

1. Splitting on the canonical `"type":"DEPOSIT"` marker at index `2` returned the suffix of the first Deposit and then continued through later milestone objects, so the raw post-marker segment was not object-bounded.
2. A nonexistent later Deposit occurrence returned an empty string; a record with zero Deposits also returned an empty string for the first post-marker segment. This supports using the raw split as the structural existence guard before reconstruction.
3. Recovering the pre-marker prefix from the final `"name":` object start, bounding the post-marker suffix at the next `},{"name":"` delimiter, and concatenating `prefix + type marker + suffix` returned exactly one complete Deposit object in the tested data.

Treat this as **user-verified for the observed compact shape**, not as proof that `name` is universally the first property or that the same delimiter is stable in every Element context. Always derive the object-start and next-object markers from the actual evaluated root sample.

### Do not make eligibility depend on property order

A milestone can be structurally valid even when required properties are serialized in a different order than another creation path. Automatic, manual, and import-created milestones may also contain different optional properties. Treat property order as fragile unless repeated real samples prove it invariant.

Avoid validating a full milestone with one ordered pattern such as:

```text
application_guid ... term ... major
```

That silently assumes those properties always appear in that sequence and on the same side of the canonical `type` marker. A formula can therefore recognize one creation path while rejecting another even though the canonical type and metadata are equivalent.

Prefer this sequence:

1. Guard the raw nth canonical type occurrence.
2. Reconstruct or bound the entire current object.
3. Test the required application marker against that object.
4. Test the term independently against that object or extract the term and compare it to the allow-list.
5. Reject only the exact excluded major marker when a missing major is allowed.
6. Return the candidate only when all independent checks pass.

If one regex must assert two required properties, account for both property orders rather than assuming one. Independent tests are easier to debug and are generally safer.

The same anonymized milestone case also contained two `DEPOSIT` objects: one valid `Client Import` deposit with application/term/major metadata and another `DEPOSIT` whose application, term, and major were `null`. The correct formula evaluated each bounded Deposit independently, allowing the valid occurrence to qualify while rejecting the null-metadata occurrence. Do not let the first invalid same-type object terminate the scan or lend metadata to another occurrence.

## Applying the verified milestone lessons to `[user-applications-root]`

The completed milestone-root tests verify general string-parsing safeguards that also apply to application-root formulas, with one important limit: **do not copy milestone-specific markers or assume the application object has the same property order.**

For `[user-applications-root]`:

1. Prefer the exact application `guid` as the occurrence discriminator when the business rule targets one application definition. Do not enumerate by a display label or another mutable descriptive value.
2. Guard every planned nth target-guid occurrence before any deeper isolation, reconstruction, or timestamp extraction. Later planned slots may be absent.
3. Bound the current application object before testing `major`, `term`, `status`, `submitted_time`, or other metadata. The same anti-leakage principle verified on milestones applies: another application object must never lend a property to the current candidate.
4. Test each required/excluded property independently against the same bounded application object unless current samples prove a stable order.
5. For an exclusion such as "major is not X," reject only the exact excluded marker. This naturally allows a different major and, when the business rule permits it, `null`/omitted major shapes because they do not contain the exact excluded quoted value.
6. For required values such as an allowed term or required timestamp, explicit `null` or absence of an allowed marker should invalidate only that application occurrence; continue scanning later occurrences.
7. Keep candidate outputs typed consistently (`0` for invalid numeric candidates, milliseconds for valid date candidates) before `MAX`/`MIN`/`SUM`.
8. State and test the occurrence ceiling. A formula scanning ten matching application GUID occurrences intentionally ignores an eleventh unless expanded.

When the application GUID marker begins each object (for example `{"guid":"..."` in a compact sample), the object may be isolated directly from the post-marker segment to the next application boundary. If a current serializer places the chosen marker inside the object instead, use the same **guard -> recover/bound full object -> independent same-object checks** architecture proven on milestones rather than assuming the historical `guid`-first delimiter still works.

These rules transfer the verified parsing discipline, not the milestone serializer contract. Application-root Evaluate and Preview Export still require their own runtime confirmation for the final assembled formula.

## Occurrence indexing

With the bundled `SPLIT_INDEX` behavior:

```text
SPLIT_INDEX(text, marker, 1)
```

returns text before the first marker. Therefore:

- index `2` is the content after the first occurrence,
- index `3` is after the second occurrence,
- index `N + 1` is after the `N`th occurrence.

The large application example scans indexes `2` through `11`, which covers ten matching application occurrences.

Do not call index `1` the first match. That off-by-one error commonly returns unrelated prefix text.

## Isolating one object

A typical two-stage extraction is:

```text
SPLIT_INDEX(
    SPLIT_INDEX(
        [root-field],
        "<escaped object marker>",
        <occurrence index>
    ),
    "<escaped next-object delimiter>",
    1
)
```

The first split moves to the requested occurrence. The second split cuts off the next object so later checks do not accidentally inspect a different object.

## Guard missing nth occurrences before reconstruction

When the target marker occurs **inside** an object and the formula reconstructs the full object around that marker, add an outer existence check for every planned nth candidate before reconstruction. This is mandatory when the formula scans a fixed maximum number of matches, because later slots are often absent.

Use this architecture:

```text
IF(
    SPLIT_INDEX([root-field], "<exact target marker>", <occurrence index>) = "",
    0,
    <reconstruct, isolate, validate, and extract this occurrence>
)
```

Do not treat a nonblank reconstructed segment as proof that the raw occurrence existed. Reconstruction can synthesize nonblank text from neighboring objects even when the nth marker was absent. In a user-verified 2026 milestone case, that allowed an Application or Admit milestone date to leak into a formula intended to return a Withdraw date. Adding the outer `SPLIT_INDEX(...)= ""` guard to every candidate fixed the false positives.

The guard works because the bundled `IF` behavior is short-circuiting: when the occurrence is absent, the candidate returns numeric `0` and the reconstruction/property-extraction branch is not evaluated.

Read `references/root-field-occurrence-guards.md` for the full verified pattern, debugging sequence, and regression tests.

### Marker rules

- Prefer the canonical discriminator that matches the requirement. For milestone scans defined by `type`, use the exact type marker rather than a mutable `name`.
- Make the marker specific enough to identify the intended object type.
- Include stable property text and exact quoting from the sample.
- Avoid a broad marker that can appear inside another value.
- Confirm whether whitespace is present in the serialized output. A compact JSON marker will not match pretty-printed JSON with spaces, and vice versa.

### Delimiter rules

The user-provided application formula uses a delimiter based on the next object's `guid` property. This assumes the next object begins in that exact way. For milestones or a different serializer, derive the delimiter from the actual sample rather than copying the application delimiter.

## Testing inclusion and exclusion rules

### Exclude one exact value; include missing values

Suppose the rule is:

- exclude the object only when `major` equals one specific GUID,
- include a different major,
- include the object when `major` is missing.

Test for the presence of the exact excluded marker:

```text
SPLIT_INDEX(
    <isolated-object>,
    """major"":""<excluded-major-guid>""",
    2
) <> ""
```

Then reject that object:

```text
IF(
    SPLIT_INDEX(
        <isolated-object>,
        """major"":""<excluded-major-guid>""",
        2
    ) <> "",
    0,
    <timestamp-or-zero>
)
```

This logical shape includes both a different major and no major because neither contains the exact excluded marker.

Do not require the existence of a `major` property if the business rule says missing majors are valid.

In a user-verified compact milestone-root evaluation, these independent exact-marker checks behaved as intended against one reconstructed Deposit object: an exact application marker matched, an exact term marker matched, the object's exact major marker was detectable for exclusion, a deliberately different major marker was absent and therefore allowed, and the nested date extraction returned the exact 13-digit epoch-millisecond value from that same object. A combined `&` candidate using application match, term match, exact-major exclusion, and timestamp presence then returned numeric `1` only when all checks passed; substituting a matching excluded major, nonmatching term, or nonmatching application individually returned `0`. A second runtime probe used a reconstructed Deposit with an explicit `"major":null` property: the null marker was detectable, while the exact quoted excluded-major marker remained absent, so the object was correctly treated as allowed. Keep this evidence scoped to the tested compact serializer shape. A separate raw-occurrence aggregation probe using five guarded Deposit slots returned `0`, `1`, and `2` for records with zero, one, and two Deposit occurrences. A two-Deposit business-eligibility probe then produced `1`, `1`, `2`, and `0` for invalid/valid, valid/invalid, valid/valid, and invalid/invalid arrangements, verifying that each reconstructed Deposit is filtered independently and that `SUM` counts only qualifying occurrences without cross-object metadata leakage. A separate five-slot coverage probe then returned `5` for a record with exactly five Deposit occurrences and also `5` for a record with exactly six Deposit occurrences. This user-verifies the stated coverage ceiling: the first five raw target occurrences are counted and a sixth occurrence is intentionally outside the formula's scan. A reconstructed Deposit with explicit `"term":null` was also user-verified: the null marker was detectable and an exact allowed quoted-term marker was absent, so an exact term allow-list rejected the object as intended. The complete five-slot formula was subsequently evaluated as one assembled expression across eight controlled count cases and returned `0`, `1`, `0`, `0`, `1`, `2`, `5`, and `5`; the user reported the same results in actual Preview Export. This establishes evaluation/Preview parity for that complete formula and tested compact serializer shape. A completely omitted `term` property and an entirely omitted `major` property remain separate serializer shapes requiring their own runtime tests.

### Include one exact value

For an inclusion rule, return the candidate only when the exact marker exists:

```text
IF(
    SPLIT_INDEX(<isolated-object>, "<exact include marker>", 2) = "",
    0,
    <timestamp-or-zero>
)
```

### Multiple conditions

Apply conditions to the same isolated object. Never search the full root field for a major, term, or timestamp after isolating only the object type, because a matching property from another object can leak into the result.

For example:

```text
IF(
    (<same-object has required application GUID>) &
    (<same-object does not have excluded major>) &
    (<same-object has timestamp>),
    VAL(<same-object timestamp>),
    0
)
```

## Exact allow-lists and boolean traps

For a small list of exact allowed values, prefer explicit equality checks joined with `|` when reliability matters more than formula length. This avoids regex escaping and boolean-coercion surprises:

```text
IF(
    (<term-expression> = "client.terms.100") |
    (<term-expression> = "client.terms.200") |
    (<term-expression> = "client.terms.300"),
    <candidate>,
    0
)
```

If a boolean-returning helper such as `CONTAINS` or `REGEXP_MATCH` is used as the allow-list test, do not assume its raw result is safe as an `IF` condition. Element contexts have differed between real booleans and text-like boolean results. First Evaluate the helper by itself, then compare explicitly to the observed representation (`TRUE` or `"TRUE"`) if needed.

A compact membership trick such as:

```text
CONTAINS("|a|b|c|", CONCAT("|", <value>, "|"))
```

looks attractive, but in a verified 2026 tenant application-root case it caused all application terms to pass when used directly as an `IF` condition. Do not use that pattern in a production root-field formula unless the boolean return/coercion behavior has been separately verified in the same export context.

For a constrained GUID allow-list, an anchored regex without square-bracket character classes can be compact:

```text
REGEXP_REPLACE(
    <term-expression>,
    "^client.terms.(100|200|300)$",
    "1"
) = "1"
```

The dots in that pattern are regex wildcards, not literal-dot escapes. Use this only when the surrounding fixed text and enumerated suffixes make the broader match acceptable. If exact literal punctuation is required, prefer explicit equality checks rather than assuming a backslash escape will behave identically across Element runtimes.

## Export Preview tokenization gotcha

**Support-confirmed behavior (August 2026):** Export Preview can scan square-bracket text as Element field tokens even when the brackets occur inside a quoted regex/string literal. For example, this regex can work in Test Formula yet fail Preview Export with `Expression have undefined tokens`:

```text
"^client[.]terms[.](100|200)$"
```

The preview/compiler sees `[.]` as though it were a field token. The same risk applies to other regex character classes such as `[a-z]` or `[0-9]`. Therefore, for export formulas:

- Treat **every** `[...]` sequence as potentially tokenized, even inside quotes.
- Reserve bracket syntax for legitimate field references such as `[user-applications-root]`.
- Prefer regex patterns without square-bracket character classes, or use explicit equality/OR conditions.
- Do not assume replacing `[.]` with `\.` is safe. In the verified tenant case, the escaped-dot rewrite removed the preview error but then failed to match the term at runtime.
- Run both Test Formula/Evaluate and actual Preview Export. Passing Test Formula alone does not prove the export compiler will accept the expression.

When debugging `Expression have undefined tokens`, inspect quoted strings for bracket sequences before blaming valid field slugs. The bundled linter supports `--export` to flag this pattern.

## Extracting timestamps

A Mongo-style timestamp may appear similar to:

```json
"submitted_time":{"$date":{"$numberLong":"1720000000000"}}
```

A repeated split pattern can isolate the numeric text:

```text
SPLIT_INDEX(
    SPLIT_INDEX(
        <isolated-object>,
        """submitted_time"":{""$date"":{""$numberLong"":""",
        2
    ),
    """",
    1
)
```

Build the actual marker from the exact raw sample. Quote counts in this illustration are easy to misread; run `scripts/formula_lint.py` on the completed formula.

### Blank guard

Return numeric `0` when the extraction is blank:

```text
IF(
    <timestamp-text> = "",
    0,
    VAL(<timestamp-text>)
)
```

All candidates must have the same numeric type before `MAX` or `MIN`.

### Property order

A split that searches for a timestamp marker inside the already isolated object is usually resilient to property order within that segment. A delimiter that assumes the next object starts with a particular property is not. State the assumption and test a real record.

## Selecting the latest or earliest candidate

The training source documents binary signatures:

```text
MAX(a, b)
MIN(a, b)
```

For many candidates, create a balanced tree:

```text
MAX(
    MAX(candidate_1, candidate_2),
    MAX(candidate_3, candidate_4)
)
```

For ten candidates, use `scripts/build_binary_tree.py` rather than manually counting parentheses:

```bash
python3 scripts/build_binary_tree.py --function MAX --file candidates.txt --pretty
```

Each nonempty line in `candidates.txt` is one candidate expression. JSON arrays of strings are also supported.

### Latest versus last in text order

The latest timestamp is the maximum numeric timestamp. It is not necessarily:

- the first matching occurrence,
- the last occurrence in serialized text,
- the last object added,
- the object with the largest application or milestone GUID.

Use `MAX` for latest and `MIN` for earliest after invalid candidates have been removed.

### Earliest with zero sentinels

A zero sentinel works naturally with `MAX` because valid positive timestamps are greater than zero. It does not work directly with `MIN`, because zero would win. For earliest selection, use a high sentinel or exclude blanks through a different nested conditional strategy, then convert the sentinel back to blank.

## Converting and formatting epoch values

### Milliseconds to seconds

`DATE_READ(..., "U")` should receive **integer epoch seconds**. Do not feed it fractional seconds such as `1753128101.067`; in the verified application-root case this produced implausible years and a repeatedly incorrect July month.

Prefer an explicit integer conversion:

```text
FLOOR(<epoch-milliseconds> / 1000)
```

If selecting the latest application, keep the original millisecond values numeric through `MAX` so millisecond ordering is preserved, then convert only the winning timestamp to seconds. The verified long application example uses the first ten digits after `MAX`:

```text
VAL(LEFT(CONCAT("", <winning-epoch-milliseconds>), 10))
```

That works for positive 13-digit millisecond timestamps. Do not use plain `<milliseconds> / 1000` unless it is wrapped in `FLOOR`, `TRUNC`, or another verified integer conversion before `DATE_READ`.

### Epoch seconds to date

```text
DATE_READ(CONCAT("", <epoch-seconds>), "U")
```

### Final date format

```text
DATE_FORMAT(
    DATE_READ(CONCAT("", <epoch-seconds>), "U"),
    "m/d/Y"
)
```

For an ISO-style filename date:

```text
DATE_FORMAT(
    DATE_READ(CONCAT("", <epoch-seconds>), "U"),
    "Y-m-d"
)
```

## Eastern Time and daylight saving

The user-provided long example subtracts `18000` seconds before parsing, which is UTC-5. This can shift UTC timestamps to EST, but it is not DST-aware.

- EST: subtract `18000` seconds.
- EDT: subtract `14400` seconds.

For date-only output, the difference matters when a UTC timestamp falls near midnight. A record at 04:30 UTC may be the prior calendar day under EST but the same calendar day under EDT.

Use one of these approaches:

1. **Fixed offset explicitly requested:** apply the stated offset and label it EST or EDT, not generic year-round Eastern Time.
2. **Dates restricted to one season:** use the season's offset and state the date-range assumption.
3. **Historical dates across seasons:** do not claim a fixed offset is correct. Build explicit DST logic only if the available date functions can be validated for the required years, or state the limitation.
4. **Element already presents the extracted date in local time:** do not apply a second offset. Compare Evaluate output to a known record first.

## No-match handling

A maximum of all-zero candidates represents no valid match. Guard before date conversion where practical:

```text
IF(
    <latest-epoch-ms> = 0,
    "",
    DATE_FORMAT(
        DATE_READ(
            CONCAT("", FLOOR(<latest-epoch-ms> / 1000)),
            "U"
        ),
        "m/d/Y"
    )
)
```

Because Element formulas do not show a variable-binding function in the bundled references, this duplicates `<latest-epoch-ms>` unless the formula uses a sentinel-removal pattern.

The user-provided example formats the zero epoch after a negative offset and removes the resulting `12/31/1969` text with `REGEXP_REPLACE`. If using that strategy:

- verify the exact output separator and timezone,
- anchor the regex,
- explain the sentinel,
- test that a legitimate date cannot be removed accidentally,
- avoid an unescaped `/` inside the regex pattern. A pattern such as `"^12/31/1969$"` can surface a PHP `preg_replace(): Unknown modifier '3'` error in Element. Prefer a zero guard; if a sentinel regex is unavoidable, use a pattern that does not contain slash characters and verify it against the exact formatted output.

## Validation matrix

Evaluate at least these records or synthetic cases:

| Case | Expected result |
|---|---|
| No matching object | blank |
| Canonical type with an alternate/manual/imported `name` | still matched when `type` is the discriminator |
| One valid object | its date |
| Two valid objects | latest date |
| First object newer than second | first object's date; proves numeric `MAX` is used |
| Excluded major only | blank |
| Excluded major plus valid different major | valid different-major date |
| Missing major plus valid timestamp | included date |
| Valid major but missing timestamp | ignored |
| More matching objects than formula covers | documented limitation or expanded occurrence count |
| Timestamp just before/after UTC midnight | correct local calendar date under the stated timezone rule |
| Required properties reordered around the canonical marker | formula still recognizes the same object |
| Two same-type objects: one with null/missing metadata, one valid | only the valid object qualifies; no cross-object leakage |
| Changed object property order | formula still works, or the dependency is documented |
| Test Formula passes but Preview Export fails | inspect bracketed text inside quoted strings; no undefined pseudo-tokens remain |

## Failure modes

### Always returns the first date

Likely causes:

- only occurrence index `2` is inspected,
- the formula returns before building `MAX`,
- the timestamp candidates are strings and compare unexpectedly,
- later occurrences are not isolated correctly.

### Month is always July or year looks random

Likely causes:

- a millisecond value is parsed as seconds,
- the wrong substring is extracted,
- `DATE_READ` format does not match the string,
- a non-timestamp fragment is passed through `VAL`,
- quote or delimiter errors shift the extraction boundary.

Inspect the raw extracted timestamp first, before formatting.

### Returns `12/31/1969`

The no-match candidate became zero, a negative timezone offset was applied, and the epoch converted to the prior day. Add a zero guard or a tested sentinel-removal step.

### Missing-major objects are excluded

The formula probably tests for `major <> excluded` by extracting a major value, which fails when the property is absent. Reject only the exact excluded marker instead.

### Valid milestone is missed because its name differs

The formula may be enumerating occurrences by a display/source `name` even though the business rule is defined by canonical `type`. This is especially risky for manually added/import-created milestones. Return the raw milestone and compare `name` versus `type`; if `type` is the invariant criterion, switch the occurrence marker to the exact `type` value and reconstruct the object around that marker if necessary.

### Automatic milestones match but manual/imported milestones do not

Likely causes include a mutable `name` marker, prefix-only validation around an internal `type` marker, or an ordered eligibility regex that assumes properties such as `application_guid` and `term` always appear in one sequence. Manual/import-created objects can also contain extra optional properties or null metadata on a separate same-type occurrence.

Return one reconstructed manual/imported object by itself. Then test its canonical type, application, term, and excluded-major condition independently. If the same metadata passes independently but the combined candidate fails, remove the property-order assumption and validate against the full bounded object.

### Wrong object's major or timestamp is used

A condition may be searched against the full root string or an unbounded segment. Isolate one object first, and apply all tests inside that same segment.

If the wrong date appears specifically when the requested nth target object does **not** exist, inspect reconstruction logic next. A reconstruction can combine neighboring root-field text with an inserted marker and create a synthetic segment that looks valid. Before reconstructing any nth occurrence, guard it with `IF(SPLIT_INDEX([root-field], <marker>, <index>) = "", 0, <candidate>)`. Apply the guard to every planned candidate slot. See `references/root-field-occurrence-guards.md`.

### Formula breaks after adding an occurrence

Common causes are unbalanced parentheses, a binary `MAX` with too many arguments, or a quote-count error. Generate a balanced tree and run the linter.

### Test Formula works but Preview Export says undefined tokens

Likely cause: a quoted regex/string contains square-bracket text such as `[.]`, `[a-z]`, or `[0-9]`. Export Preview can tokenize those as field references before formula evaluation. Rewrite without bracket character classes and run the linter with `--export`.

### Term allow-list accepts every term

Likely causes:

- a boolean-returning membership helper is being used directly as an `IF` condition and its false result is represented as nonempty text,
- the term expression is not isolated to the same object,
- a broad substring test is matching more than intended.

First return the extracted term by itself. Then test one exact equality. Expand to an explicit OR allow-list before reintroducing compact regex logic.

### Escaped-dot regex makes every candidate blank

Do not assume a `\.` rewrite behaves identically to `[.]` in Element formula strings. If `[.]` worked in Test Formula but failed Preview Export, use an export-safe pattern or explicit equality checks and verify both Test Formula and Preview Export.

### Term-derived output is wrong even though the correct milestone was selected

Likely cause: a tenant term GUID was assigned a name/code/year from an assumed mapping. Treat term GUIDs as opaque. Return the selected raw term GUID first, then verify its actual code/name with user-provided taxonomy data, `DB_MAP`, or a focused Element diagnostic before hard-coding a semester/year/date. Any local simulation must use the verified mapping fixture rather than a guessed list order.

## Parsing cost and compact intermediates

For long cross-record formulas, preserve this reference's raw-occurrence guards and same-object boundaries but move downstream comparisons to compact validated records. See `references/compact-root-pipelines.md`. This is not a new root parser: current serializer evidence remains mandatory, and per-producer extraction may still repeat. The gain is removing repeated whole-root scans/maps from each comparison and outer projection.
