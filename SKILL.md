---
name: element451-calculated-fields-v2
description: Write, edit, explain, review, and troubleshoot Element451 formulas used in imports, exports, Workflow/Rule Formula Fields, and calculated payments. Use when a user mentions calculated columns, formula actions, payment calculations, `[C#]` columns, Element field slugs, `DB_MAP`, `DS_MAP`, `TAXONOMY_MAP`, dates, labels, checkbox values, regex, application or milestone root fields, serialized JSON-like data, count/any/latest/earliest or linked argmax/argmin selection, parser or Preview Export errors, successful evaluation that does not persist, or incorrect formula output. Require current-task tenant fields, GUIDs, mappings, target type, and data shape; use only source-supported functions, return complete formulas, validate long formulas, and keep the solution in formulas when required.
---

# Element451 Calculated Fields

## Purpose

Produce paste-ready Element451 formulas for every currently documented formula context: Imports, Exports, Workflow/Rule Formula Fields, and calculated payments. Ground formulas in current official documentation, bundled function training, generalized runtime observations, and statically validated examples. Prioritize correctness, explicit assumptions, complete formulas, destination compatibility, and testable edge-case behavior.

## Tenant-neutral scope and identifier policy

Treat formula syntax, parsing techniques, runtime observations, and debugging lessons as reusable knowledge. Treat every institution's CRM configuration as request-scoped data.

- Require the user to provide the exact tenant-specific fields and identifiers needed for the current formula, including custom field slugs, application GUIDs, term GUIDs, major GUIDs, taxonomy or label GUIDs, data-source IDs, mapping values, domains, status names, and business thresholds.
- Never retrieve, infer, or reuse an institution's identifiers, mappings, field names, labels, or business rules from prior conversations, memory, historical skill additions, or bundled examples unless the user explicitly asks to reuse that information for the current task.
- A tenant or institution name by itself is not permission to preload known configuration. Use tenant-specific values only when they appear in the current conversation, are supplied in an attached redacted sample, are returned by a tenant source the user explicitly asks to consult, or the user explicitly requests reuse of known values.
- When required tenant data is missing, use conspicuous placeholders such as `<APPLICATION_GUID>`, `<TERM_GUID_1>`, `<DATA_SOURCE_ID>`, or `[user-custom-field-example]`. Fictional examples beginning with `school.*` and `[user-custom-field-example]` are illustrations only and must never be assumed to exist in a tenant.
- Do not infer semantic meaning from an identifier. A term GUID does not reveal its name, code, semester, or year; a taxonomy GUID does not reveal its label; a data-source ID does not reveal its columns. Obtain mappings from the user, a current tenant lookup, or a focused Evaluate diagnostic.
- Do not add institution-specific mapping tables or identifiable CRM configuration to this reusable skill. Before incorporating a future user example, anonymize tenant prefixes, numeric identifiers, custom slugs, domains, label names, and institution-specific business details while preserving the formula technique.

## Mandatory workflow

Follow these steps in order for every task:

1. **Classify the task.** Determine whether the user wants to create, edit, explain, review, or debug a formula.
2. **Classify the formula context.** Identify Import, Export, Workflow/Rule Formula Field, or calculated payment; source columns versus available Element/form tokens; target field or amount type; scope; and whether repeatable/root data is involved.
3. **Extract exact requirements.** Capture conditions, precedence, include/exclude rules, selection rule, output format, timezone, blank behavior, and tenant identifiers.
4. **Load only the relevant references.** Use the routing table below rather than loading every bundled source.
5. **Verify current behavior when material.** Open the live official page before claiming a function, menu, preview behavior, field setting, or limitation is current.
6. **Design the logic before writing syntax.** Break the formula into inputs, conditions, candidate values, selection, conversion, and final output.
7. **Construct the complete formula.** Preserve exact slugs and GUIDs, use straight quotes, guard blanks, and keep types consistent.
8. **Validate.** Run the bundled formatter/linter for nontrivial formulas and build a representative test matrix.
9. **Return the complete answer.** For an edit, always return the entire updated formula unless the user explicitly requests only a patch.

## Formula-only constraint

When the user requires a calculated field or says not to use another method:

- Solve the task with a calculated formula.
- Do not redirect to API scripts, segments, spreadsheet processing, custom code, or another Element feature.
- Mention another method only if the user asks for alternatives or the official formula engine cannot express a required operation; clearly distinguish that limitation from a preference.
- Do not shorten a long formula merely because another method would be easier.

## Minimum requirements to identify

Use information already supplied in the conversation. Do not repeat a question that has already been answered.

Identify as many of these as apply:

- **Context:** Import, Export, Workflow/Rule Formula Field, or calculated payment. Read `references/formula-contexts.md` when context affects inputs, scoping, preview, persistence, or output type.
- **Target:** destination field/column and expected data type.
- **Inputs:** exact `[C#]` references, field slugs, or root field.
- **Rule:** exact comparisons, AND/OR logic, priority, ranges, and include/exclude semantics.
- **Selection:** first, latest, earliest, highest priority, all, or a specific occurrence.
- **Mapping:** exact data-source ID, taxonomy/term/major type, match key, output key, and default.
- **Dates:** input representation, output format, timezone, and date-only versus datetime behavior.
- **Missing data:** blank, null, omitted property, zero, fallback, or preserve existing value.
- **Repeatable data:** a representative redacted root-field sample and maximum occurrences to inspect.

If an exact identifier or sample is essential and absent, prefer a clearly labeled placeholder formula plus a concise list of replacements over inventing a tenant value. Ask one focused question only when no meaningful formula can be produced without the missing value.

## Reference routing

Read these files only when relevant:

- **Context differences across Import, Export, Workflow/Rule Formula Field, and calculated payment:** `references/formula-contexts.md`
- **Function signatures and return behavior:** `references/formula-functions.md`
- **Common formula patterns:** `references/formula-patterns.md`
- **Capability coverage, uncertainty, and test priorities:** `references/formula-capability-matrix.md`
- **Applications, milestones, and serialized root fields:** `references/root-field-parsing.md`
- **Count, latest/earliest, threshold, and linked argmax/argmin root selection:** `references/root-field-selection.md`
- **Sparse nth-occurrence scans or neighboring-object leakage during root-field reconstruction:** `references/root-field-occurrence-guards.md`
- **Observed export-preview/root-field pitfalls:** `references/root-field-export-preview.md`
- **Complete guarded latest-application example:** `references/root-field-example-latest-application.md`
- **Parser errors, wrong output, context-specific persistence, and test planning:** `references/testing-debugging.md`
- **Current official page routes and source hierarchy:** `references/official-docs.md`
- **Uncommon function details or source discrepancies:** `references/source-function-training.md`
- **Improved generalized examples:** `references/source-formula-examples.md`
- **Advanced unverified date/time test targets:** `references/formula-frontier-tests.md`
- **Verified advanced milestone-root reconstruction/count evidence:** `references/formula-frontier-root-tests.md`

All identifiers and business values in bundled examples are fictional or generalized teaching data. Use them only to learn formula architecture. No bundled reference is an authoritative source for any tenant's fields, GUIDs, mappings, labels, domains, or business rules.

## Source and evidence rules

- Prefer a current exact official Element451 page for present product behavior.
- Use the bundled training reference for detailed signatures not visible in the Help Center, but mark uncertain current support and verify live when possible.
- Use bundled examples for formula architecture, not as proof that every identifier or assumption is portable.
- Preserve contradictions instead of silently reconciling them. For example, the bundled sources vary between raw `TRUE` and quoted `"TRUE"`; use current documentation and Evaluate to establish the actual return type.
- Do not invent a function because an equivalent exists in Excel, JavaScript, SQL, or PHP.
- Do not claim a formula was runtime-tested unless Element451 Evaluate output or user feedback proves it.
- Ask for redacted root data. Never request passwords, tokens, API keys, or unnecessary student information.

## Formula design rules

### Build from a logic outline

Internally reduce the request to this shape:

```text
inputs -> eligibility conditions -> candidate result(s) -> selection -> conversion -> final formatting -> blank/fallback
```

For nested rules, order branches by explicit business priority. For date selection, compare numeric timestamps rather than serialized order.

### Preserve exact identifiers

- Copy field slugs and GUIDs exactly as supplied.
- Do not correct apparent spelling errors in Element slugs such as historical `prefered` forms.
- Keep tenant-specific application, major, taxonomy, term, and data-source identifiers in visible constants so the user can audit them.
- Treat tenant GUIDs as opaque identifiers. Never infer a term name, code, semester, year, or other semantic meaning from GUID order, suffixes, a prior example, or an unsourced test fixture. When the output depends on that meaning, verify the GUID-to-name/code mapping from user-provided data, a current lookup, or a focused Element Evaluate diagnostic before hard-coding it.
- Clearly mark any placeholder such as `<EXCLUDED_MAJOR_GUID>` or `[C#]`.

### Keep types consistent

- Quote text literals; leave numeric literals unquoted.
- Convert timestamp text with `VAL` or another documented numeric conversion before `MAX`/`MIN`.
- Return numeric `0`, not text `"0"`, for invalid numeric candidates.
- Ensure map output matches the target field's expected representation: GUID, value, code, or name.
- Keep all branches compatible with the target field type.

### Guard missing data

Use short-circuiting `IF` branches to avoid parsing or converting blank values. Explicitly define behavior for:

- empty strings,
- missing optional JSON properties,
- omitted repeatable objects,
- failed maps,
- zero timestamps,
- no valid candidate.

Avoid exposing epoch fallback dates such as `12/31/1969`; guard zero before conversion or use a clearly explained, tested sentinel-removal pattern.

Do not use `DATE_READ` itself as strict date validation. User-verified Import Preview behavior shows that invalid/overflowing components can normalize into a later valid date (for example, a non-leap February 29 can roll into March 1). When strict validity matters, canonicalize the source, parse it, format the parsed value back to the same canonical representation, and require an exact round-trip match.

For **Import Preview**, do not assume a source-column datetime string preserves its time-of-day inside date functions. In a user-verified `Y-m-d H:i:s` probe, `DATE_READ(TRIM([C1]), "Y-m-d H:i:s")` formatted back as the correct date at `00:00:00`, and `DATE_COMPARE(TRIM([C1]), ...)` behaved as though the source time were midnight. Direct literal-to-literal `DATE_COMPARE` still distinguished seconds correctly. When an import formula needs sub-day precision, test the exact source representation first; prefer epoch seconds/milliseconds or separately extracted time components when possible.

For **Import Preview epoch timestamps**, integer epoch seconds parsed with `DATE_READ(..., "U")` are user-verified to preserve exact second-level values across tested DST transition boundaries. For epoch milliseconds, convert with `FLOOR(VAL(value) / 1000)` before parsing. An end-to-end post-2007 US Eastern conversion using dynamically calculated DST boundaries, seasonal `-14400`/`-18000` offsets, and final `DATE_READ(..., "U")`/`DATE_FORMAT` output is user-verified at exact 2026 spring/fall transition seconds in Import Preview. Keep this evidence scoped to Import Preview until the target Export or Workflow context is separately verified.

### Use safe syntax

- Use straight ASCII double quotes.
- Double embedded quote characters inside formula strings.
- Parenthesize compound conditions.
- Use `REGEXP_REPLACE`, not `REGEX_REPLACE`.
- Follow documented one-based `SPLIT_INDEX` examples.
- Treat `MAX` and `MIN` as binary according to the bundled training signature; nest them for multiple candidates.
- Use PHP-style date formats supported by the date functions.
- Do not add regex slash delimiters unless verified in the target context.
- For **export formulas**, avoid bracketed regex character classes such as `[.]`, `[a-z]`, or `[0-9]` inside quoted strings. Element support confirmed that Export Preview can interpret bracketed text inside a string as a field token and fail with `Expression have undefined tokens`, even when Test Formula succeeds. Prefer an equivalent pattern without square brackets, exact equality/OR checks, or another documented function, then verify with actual Preview Export.
- Do not assume `\\.` is a drop-in replacement for `[.]` in Element's export runtime. In a tenant-reported application case it passed token validation but failed to match as expected. Treat backslash-heavy regex rewrites as runtime-dependent and test them separately.
- When an allow-list is a small set of exact strings, prefer explicit equality joined with `|` over clever `CONTAINS` membership tricks unless the boolean return form has been verified. Boolean-returning functions may need an explicit comparison to `TRUE` or `"TRUE"` in the target context.

## Context-specific output rules

- **Import:** use the supplied source-column shape and destination mapping. Define whether blank means skip, clear, preserve, or import an empty value.
- **Export:** identify scope, First/Last and Order By settings, downstream format, and date-only versus datetime behavior. Run both Evaluate/Test Formula and actual Preview Export.
- **Workflow/Rule Formula Field:** a successful evaluation does not prove the value was saved. Confirm that the destination field accepts the returned representation, especially for fields backed by fixed or custom data sources, and verify the actual profile write.
- **Calculated payment:** return a numeric amount in every branch. Define blank, zero, negative, fractional, threshold, and unexpected-option behavior before writing syntax.
- Do not assume a token available under one trigger, form, application, event, or formula context is available in another. Use the field picker or focused Evaluate diagnostic when scope is uncertain.

## Task workflows

### Create a new formula

1. Restate the rule internally in plain language.
2. Select source-supported functions.
3. Write small reusable conceptual pieces: normalized input, condition, candidate, map, date conversion, output.
4. Assemble the complete expression.
5. Format and lint it.
6. Test baseline, blank, excluded, boundary, and multiple-match cases as applicable.

### Edit an existing formula

1. Preserve all unrelated working logic.
2. Identify the smallest semantic change required.
3. Apply it consistently to every repeated branch or occurrence.
4. Revalidate the full parenthesis and quote structure.
5. Re-test previous cases plus the new edge case.
6. Return the entire updated formula, not just the changed fragment.

Examples of semantic distinctions to preserve:

- "Return the latest date" means numeric maximum, not first occurrence.
- "Exclude only major X" means include a different major and include a missing major.
- "No application" means blank, not a zero-epoch date.
- "Eastern time" requires an explicit DST assumption; a fixed UTC-5 offset is EST, not year-round ET.

### Review or explain a formula

1. Identify its inputs and output.
2. Trace each nested condition in execution order.
3. Explain map direction and defaults.
4. Identify type, blank, indexing, date, timezone, and portability risks.
5. Separate definite errors from assumptions that require Evaluate.
6. Do not rewrite unless the user asks for a correction; when correcting, provide the full formula.

### Debug a formula or screenshot error

1. Transcribe the exact formula/error from provided content without guessing hidden text.
2. Run static checks.
3. Isolate the smallest failing component.
4. Return raw intermediate values before formatting them.
5. Compare the result against a known contact in Evaluate.
6. Fix one semantic layer at a time.
7. Provide the complete corrected formula and a focused regression test list.

### Parse repeatable/root-field objects

Always read `references/root-field-parsing.md`. Also read `references/root-field-selection.md` when the request involves count, any-match, latest/earliest with thresholds, or returning a field associated with the winning object. Then:

1. Derive exact object markers and delimiters from the supplied root sample. When the business rule identifies a milestone by canonical `type` (for example `DEPOSIT`, `ADMIT`, or `WITHDRAW`), enumerate occurrences with the exact `"type":"<TYPE>"` marker rather than a milestone `name`. Names can change for manually added or imported milestones (for example `Client Import`), while the canonical type can remain the same. Use `name` as the occurrence marker only when the requirement itself is name-based or the user has explicitly established that name as invariant.
2. If the chosen marker occurs inside the object, identify the current object's prefix and suffix and reconstruct or pair them for the **same occurrence**; do not inspect the full root field for neighboring properties.
3. If scanning planned nth occurrences of a marker that can be absent, **prove that nth raw occurrence exists before reconstructing or inspecting it**. Use an outer short-circuit guard such as `IF(SPLIT_INDEX([root], marker, index) = "", 0, <candidate>)`. This is mandatory when reconstruction could otherwise combine neighboring-object text with an inserted marker. Read `references/root-field-occurrence-guards.md`.
4. Isolate or reconstruct only the confirmed-existing occurrence before testing its properties.
   - In a user-verified compact milestone-root evaluation, a missing nth canonical-type split returned blank; `name`-anchored prefix recovery plus a next-`name` object boundary reconstructed exactly one target object. Treat that as evidence for that serializer shape only, and re-derive the markers from each current root sample.
   - In the same tested serializer shape, independent exact application, term, and major marker checks plus nested `date.$date.$numberLong` extraction all stayed scoped to that reconstructed object. A combined candidate using `&` across application, term, exact-major exclusion, and timestamp-presence checks was also user-verified to return numeric `1` only when all conditions passed and numeric `0` when the application, term, or exclusion rule failed. A reconstructed object with explicit `"major":null` was user-verified to remain allowed when the rule excludes only one exact quoted major value. A separate five-slot raw-occurrence probe was user-verified to return numeric counts of `0`, `1`, and `2` for records with zero, one, and two target Deposit occurrences. A two-Deposit eligibility probe also returned `1`, `1`, `2`, and `0` for invalid/valid, valid/invalid, valid/valid, and invalid/invalid arrangements, verifying independent per-occurrence filtering plus `SUM` counting without cross-object metadata leakage; those probes used manually created Deposit milestones and therefore also verify this architecture on that creation path. Do not treat a manual-creation test as alternate-name proof unless the evaluated `name` actually differs; keep canonical-`type` and display-`name` evidence distinct. A separate five-slot coverage probe returned `5` for both exactly five and exactly six Deposit occurrences, user-verifying that slots 1-5 are counted and any sixth occurrence is intentionally outside coverage. A reconstructed Deposit with explicit `"term":null` was also user-verified to be detectable as null and to fail an exact allowed-term marker check, so null terms are rejected by an exact term allow-list. Finally, the complete five-slot count formula was user-verified as one assembled expression across an eight-case matrix (`0, 1, 0, 0, 1, 2, 5, 5` for zero, one valid, excluded major, null term, mixed pair, two valid, five valid, and six valid) with matching reported results in Element formula evaluation and actual Preview Export. Treat entirely omitted `major`/`term` properties and different serializer object-start ordering as separate portability behaviors that still need their own runtime verification.
5. Unless property order is proven invariant, validate required properties against the **full bounded/reconstructed object**, not only the text before or after the type marker. Test independent properties independently when practical; do not rely on an ordered regex such as `application.*term` unless that order is verified.
   - Apply the same **raw occurrence guard -> bounded current object -> independent same-object checks -> typed candidate -> fixed coverage** discipline to `[user-applications-root]`. Prefer the target application `guid` as the discriminator when it is stable, but derive the application object-start and next-object boundaries from the current application sample rather than copying milestone markers or assuming `guid` is always first.
6. Apply all conditions to that same isolated object. A second object with the same type but null, missing, or disallowed metadata must not borrow values from a qualifying neighbor.
7. Include missing optional properties when the rule says only one exact value is excluded.
8. Choose the candidate type from the requested selection rule: for an **existence/any-match** check, return numeric `1` for a qualifying occurrence and `0` otherwise, then test `SUM(...) > 0`; for a count, return `SUM(...)`; for latest selection, use a valid numeric key or `0`; for earliest selection, use a valid key or a verified high sentinel rather than `0`.
9. When selecting dates, extract and convert timestamps consistently and build a balanced nested `MAX`/`MIN` strategy appropriate to the sentinel rules. For argmax/argmin, keep each sort key and associated output tied to the same bounded object, state the tie policy, and never look up the winning value from the whole root field afterward.
10. Guard the no-match result before final conversion or formatting.
11. Convert milliseconds to **integer** epoch seconds before `DATE_READ(..., "U")`; never pass fractional epoch seconds. Apply the stated timezone rule and format.
12. If the final output maps a selected tenant GUID to a semantic value (for example Fall 2027 -> `09/01/2027`), verify the exact GUID mapping separately. A local/simulated test must use the real mapping fixture; do not let an invented GUID map make a test appear to pass.
13. For export formulas, run both Test Formula/Evaluate **and actual Preview Export**. If Preview Export alone reports undefined tokens, inspect square-bracket sequences inside quoted regex/string literals, not just real `[field-slug]` references.
14. State the maximum occurrence count covered by the formula.

## Validation tools

For any long, nested, regex-heavy, or root-field formula, save it to a temporary text file and run:

```bash
python3 scripts/format_formula.py formula.txt -o formatted.txt
python3 scripts/formula_lint.py formatted.txt --strict-functions
# For export formulas, also enable export-preview-specific checks:
python3 scripts/formula_lint.py formatted.txt --strict-functions --export
```

For many `MAX` or `MIN` candidates:

```bash
python3 scripts/build_binary_tree.py --function MAX --file candidates.txt --pretty
```

To expand a repeated candidate template that contains `{index}`, `{previous_index}`, or `{ordinal}`:

```bash
python3 scripts/build_occurrence_scan.py candidate-template.txt \
  --start-index 2 --count 10 --combine MAX -o candidates-formula.txt
```

To lint every annotated formula block in edited references:

```bash
python3 scripts/lint_reference_formulas.py references/source-formula-examples.md
```

To regression-check the fictional compact-JSON Deposit reconstruction/count fixture used by the verified advanced root test:

```bash
python3 scripts/test_frontier_designs.py
```

This fixture test does not emulate Element451. It catches local Deposit marker/index/reconstruction/count mistakes only.

When the user supplies a valid JSON `[user-milestones-root]` sample, inspect the actual objects before designing string markers:

```bash
python3 scripts/inspect_milestone_root.py sample.json \
  --type DEPOSIT \
  --application-guid <application-guid> \
  --exclude-major <major-guid> \
  --term-guid <allowed-term-guid>
```

Repeat `--term-guid` for each allowed term. Add verified `--term-map <guid>=<code-or-name>` values when the final output depends on term semantics. This script is a data-shape diagnostic only; it does not emulate Element's formula runtime.

The linter is static. It cannot prove runtime support, data shape, map contents, timezone, or return types. Element451 Evaluate remains required for runtime confirmation. For exports, Evaluate/Test Formula is not sufficient by itself; also run Preview Export because its token-validation layer can reject strings that Evaluate accepts.

## Required test thinking

For simple formulas, mentally verify at least true, false, and blank cases. For complex formulas, provide or internally use a matrix that includes:

- one valid record,
- the same canonical milestone type under alternate/manual/imported names when `type` is the business discriminator,
- the same qualifying object with required properties reordered around the canonical marker,
- multiple same-type objects where one has null/missing metadata and another qualifies,
- no valid record,
- zero occurrences of the target root-field marker while neighboring objects contain plausible dates or matching properties,
- fewer target occurrences than the formula's planned maximum slots,
- multiple valid records in nonchronological order,
- exact excluded value,
- different value,
- missing optional property,
- missing timestamp,
- threshold/date boundary,
- maximum occurrence coverage,
- timezone boundary near midnight,
- Workflow/Rule destination write actually persists after a successful Test Formula result,
- calculated-payment blank, zero, negative, fractional, threshold, and unexpected-option behavior,
- any tenant GUID-to-name/code/date mapping used by the final output, using verified mappings rather than guessed fixtures.

Never say these cases passed unless they were actually evaluated. Use wording such as "expected result" for logical tests and "verified" only for observed Element output.

## Incorporating test feedback

When a user reports Element runtime results for a frontier or uncertain formula:

1. Record the exact context: Import, Export Evaluate, Preview Export, Workflow/Rule Test Formula, actual persisted write, or calculated payment.
2. Isolate the smallest expression that reproduces the behavior.
3. Separate formula evaluation from destination persistence or export compilation.
4. Preserve the exact error text and expected/actual result.
5. Generalize the lesson and anonymize tenant fields, GUIDs, mappings, domains, and policy values before adding it to the skill.
6. Add regression cases to the relevant reference.
7. Use **user-verified** only for behavior actually observed; keep untested formulas labeled **static-lint clean** or **design target**.

## Output contract

Use this structure by default, adapting only when the task is very simple:

### Formula

Return one complete paste-ready formula in a fenced `text` code block. Use readable multiline formatting for nested formulas.

### What it does

Explain the logic in execution order, focusing on selection, exclusions, mappings, dates, and blank handling.

### Assumptions and limits

Include only material assumptions, such as tenant placeholders, occurrence coverage, serialized-object order, boolean representation, or fixed timezone offset.

### Evaluate checks

Give a short set of concrete records/cases to preview when the formula is complex or behavior is tenant-dependent.

Additional response rules:

- Lead with the formula when the user primarily wants code.
- Do not split a single formula across multiple code fences.
- Do not use ellipses inside a formula.
- Do not omit repeated branches because they are long.
- Do not return pseudocode as though it were paste-ready.
- For a requested edit, explicitly say what changed in one sentence and then provide the full formula.
- Link the exact official documentation when the answer depends on current documented behavior.
- Keep explanations concise relative to the formula unless the user asks for a tutorial.

## Quality standard

A strong answer is:

- valid-looking Element syntax,
- complete rather than abbreviated,
- tied to exact user data and business rules,
- explicit about blanks and edge cases,
- careful about date units and timezones,
- auditable for tenant-specific identifiers,
- validated structurally,
- checked against the correct formula context and destination type,
- honest about what still requires Element Evaluate, Preview Export, persistence verification, or payment testing.
