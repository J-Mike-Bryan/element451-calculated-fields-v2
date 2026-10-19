---
name: element451-calculated-fields-v2
description: Write, edit, explain, review, and troubleshoot Element451 Import/Export formulas, Workflow/Rule Formula Fields, and calculated payments. Use for [C#] columns, Element field slugs, DB_MAP/DS_MAP/TAXONOMY_MAP, dates, labels, checkbox values, regex, milestone/application roots, serialized data, count/any/latest/earliest, first/second/nth optional-field exports, or linked selection, parser/Preview Export errors, failed persistence, incorrect outputs, and oversized or slow formulas. Optimize repeated root scans with compact-record pipelines when appropriate; distinguish raw coverage from valid-match caps. Require current-task tenant identifiers, mappings, destination type, and data shape; use supported functions, return complete formulas, validate syntax and runtime separately, and keep formula-only solutions when required.
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
8. **Validate and measure.** Run the bundled formatter/linter for nontrivial formulas, measure source size/lookup call sites for long expressions, and build a representative test matrix. Optimize repeated computation before reducing coverage; read the compact-pipeline reference for oversized formulas.
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
- **Latest uploaded college/school by `index_weight` with linked `name`, `type` versus `entry_type`, and compact-root slot projection:** `references/school-root-index-weight.md`
- **First/second/nth milestone field exports, blank-slot preservation, independent label-derived values, and unsubscribe-email examples:** `references/root-field-ordinal-exports.md`
- **Oversized/slow root formulas, compact intermediate records, regex elimination and pairwise reduction, and raw-versus-valid coverage:** `references/compact-root-pipelines.md`
- **Tenant-neutral compact-pipeline compatibility and literal examples:** `references/compact-pipeline-compatibility-probe.txt`, `references/compact-pipeline-literal-input.txt`, `references/compact-pipeline-literal-output.txt`, `references/compact-pipeline-validation.json`
- **Multiple application export columns sharing one winner, term ranking, and packed-slot selection:** `references/application-root-linked-exports.md`
- **Milestone-first application fallback, blank season with a correct year, and aligned season/year outputs:** `references/term-root-fallback.md`
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

### Preserve ordinal slots and source meaning

For first/second/nth root-field outputs, read `references/root-field-ordinal-exports.md`. Distinguish the nth type-matching object from the nth nonblank or unique value; unless the rule explicitly filters blanks before selection, select the object first and then project its optional field. Preserve its empty slot rather than borrowing from another object or the current profile. State serialized ordering, duplicate policy, and coverage; two milestone columns do not guarantee all historical values are exported. Keep a separate label-derived value independent when the request defines independent sources. Do not infer current communication eligibility from historical event extraction alone.

### Preserve a linked field when choosing a record by numeric rank

When a repeatable root's highest numeric `index_weight` (or another validated rank) determines the winning object, do not simply assume the last serialized object or extract a `name` from the whole root. The user-confirmed Export school-root approach filters each bounded object, ranks eligible records by numeric `index_weight`, carries the object's **raw slot index** through a compact-table argmax reducer, then projects the output field from **that selected object**. In the reported source, `"type":"college"` identifies a college even when that same object's `entry_type` is `home_schooled`; inspect conflicting discriminator properties instead of treating their names as interchangeable. Select the winning record before handling a missing name: a blank winner must not borrow an older record's value. For this specific shape, read `references/school-root-index-weight.md` and use `scripts/build_linked_index_weight_export.py`; note fixed raw-object coverage, six-digit default rank width, and a later-serialized tie policy. The assembled school formula was user-reported working in Element Export, but new configurations still require Test Formula and actual Preview Export.

### Control formula growth before reducing coverage

Read `references/compact-root-pipelines.md` for large root-field formulas. A user-confirmed export optimization retained raw coverage while replacing repeated cross-record parser/map expansion with guarded compact-record producers, regex rejection passes, and linked-payload reduction. The generalized helper is separately locally tested; no universal Element caching or runtime-speed guarantee is implied.

- Treat approximately **500,000 characters** only as a user-reported performance warning from testing, **not an official limit**, safety boundary, or proven cause of missing rows.
- Construct the root-derived table once in the expression tree and pass each stage as one child of the next. Keep per-occurrence existence guards and same-object eligibility. Do not invent local variables or duplicate the full selector for blank checks.
- Normalize comparison keys from current-task mappings; keep fixed widths, exact timestamp precision, payload delimiters, group equality, tie policy, and missing-date rules explicit. Avoid huge floating-point packed scores.
- Reject each candidate before selecting the winner. Use existence after filtering for booleans; use enough adjacent reduction passes for the maximum candidate count when projecting a linked value.
- Never confuse the first N raw occurrences with the first N valid matches. Do not reduce coverage or introduce an application-root fallback without authorization.
- Record user confirmation at its reported scope. Require new adaptations to pass static checks, appropriate compatibility probes, Evaluate, Preview Export, and small-export ID/row reconciliation; a character reduction is not a speed benchmark.

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
- For **Import literal crosswalks** encoded as a delimiter table such as `|<fixed-width-key>=<value>|...`, normalize the incoming key before lookup when Import Preview may coerce identifier-like text and hide leading zeros. A user-verified Import fix restored a six-character key with `RIGHT(CONCAT("000000", TRIM([C#])), 6)`. When a statically clean escaped-delimiter `REGEXP_EXTRACT` lookup still returned blank for every known key, replacing the regex extraction with nested `SPLIT_INDEX` on the exact `|<normalized-key>=` boundary worked. If the business rule is to preserve an unknown identifier, append a synthetic `<normalized-key>=<normalized-key>|` fallback before splitting. Treat this as verified for that Import lookup architecture, not as evidence that regex is generally unreliable.
- For **export formulas**, avoid bracketed regex character classes such as `[.]`, `[a-z]`, or `[0-9]` inside quoted strings. Element support confirmed that Export Preview can interpret bracketed text inside a string as a field token and fail with `Expression have undefined tokens`, even when Test Formula succeeds. Prefer an equivalent pattern without square brackets, exact equality/OR checks, or another documented function, then verify with actual Preview Export.
- Do not assume `\\.` is a drop-in replacement for `[.]` in Element's export runtime. In a tenant-reported application case it passed token validation but failed to match as expected. Treat backslash-heavy regex rewrites as runtime-dependent and test them separately.
- When an allow-list is a small set of exact strings, prefer explicit equality joined with `|` over clever `CONTAINS` membership tricks unless the boolean return form has been verified. Boolean-returning functions may need an explicit comparison to `TRUE` or `"TRUE"` in the target context.
- Treat `[user-labels-all]` as a special label-membership case. User-verified probes show ordinary `CONTAINS` works correctly on literal strings, but two `CONTAINS` formulations behaved incorrectly on `[user-labels-all]` while `REGEXP_MATCH([user-labels-all], ".*<LABEL_GUID>.*") = TRUE` worked correctly. Prefer that regex membership pattern for labels unless the current raw label serialization has been inspected and a boundary-aware alternative has been proven on both positive and negative users. Do not generalize this anomaly into a claim that `CONTAINS` is globally broken.

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
   - For an ordinal projection, a missing optional output does not remove the selected object from the ordinal count. Read `references/root-field-ordinal-exports.md`; do not turn "second matching milestone, possibly blank" into "second nonblank email."
8. Choose the candidate type from the requested selection rule: for an **existence/any-match** check, return numeric `1` for a qualifying occurrence and `0` otherwise, then test `SUM(...) > 0`; for a count, return `SUM(...)`; for latest selection, use a valid numeric key or `0`; for earliest selection, use a valid key or a verified high sentinel rather than `0`. Before adding latest/most-recent logic to an any-match boolean, determine whether recency can actually change the output. If every already-qualifying occurrence implies the same TRUE result, filter first and use any-match; only use argmax/latest-first logic when the newest occurrence itself determines eligibility or when a value from the winning occurrence must be returned.
9. When selecting dates, extract and convert timestamps consistently and build a balanced nested `MAX`/`MIN` strategy appropriate to the sentinel rules. For argmax/argmin, keep each sort key and associated output tied to the same bounded object, state the tie policy, and never look up the winning value from the whole root field afterward.
   - For several outputs from one selected application, read `references/application-root-linked-exports.md`. Keep selection identical across companion columns; a missing output must not change the winner. Declare term normalization, unknown-term policy, cross-GUID ties, multi-degree semantics, and per-GUID coverage rather than treating them as universal defaults. Treat packed-score/slot-list selection as runtime-unverified until both Evaluate and Preview Export are observed.
10. Guard the no-match result before final conversion or formatting. For a milestone-first application fallback or companion season/year outputs, read `references/term-root-fallback.md`. Distinguish no eligible primary record from an eligible primary with an undecodable output; keep the same selector in every companion formula and change only the projection.
11. Convert milliseconds to **integer** epoch seconds before `DATE_READ(..., "U")`; never pass fractional epoch seconds. Apply the stated timezone rule and format.
12. If the final output maps a selected tenant GUID to a semantic value (for example Fall 2027 -> `09/01/2027`), verify the exact GUID mapping separately. A local/simulated test must use the real mapping fixture; do not let an invented GUID map make a test appear to pass.
13. For export formulas, run both Test Formula/Evaluate **and actual Preview Export**. If Preview Export alone reports undefined tokens, inspect square-bracket sequences inside quoted regex/string literals, not just real `[field-slug]` references.
14. State the maximum occurrence count covered by the formula. For large repeated scans, use `references/compact-root-pipelines.md` before lowering that ceiling; fixed raw coverage and a cap on qualifying records are different promises.

## Validation tools

For any long, nested, regex-heavy, or root-field formula, save it to a temporary text file and run:

```bash
python3 scripts/format_formula.py formula.txt -o formatted.txt
python3 scripts/formula_lint.py formatted.txt --strict-functions
# For export formulas, also enable export-preview-specific checks:
python3 scripts/formula_lint.py formatted.txt --strict-functions --export
```

For oversized formulas, measure source growth and test the generalized compact-record stage:

```bash
python3 scripts/formula_size_report.py formula.txt
python3 scripts/test_compact_record_pipeline.py
```

Use `scripts/compact_record_pipeline.py --help` to generate transforms over an already-valid compact table. Read `references/compact-root-pipelines.md` first; the helper does not supply tenant extraction, mappings, or business policy. PHP CLI is required only for its local regression test, not for the Element formula.

For many `MAX` or `MIN` candidates:

```bash
python3 scripts/build_binary_tree.py --function MAX --file candidates.txt --pretty
```

To expand a repeated candidate template that contains `{index}`, `{previous_index}`, or `{ordinal}`:

```bash
python3 scripts/build_occurrence_scan.py candidate-template.txt \
  --start-index 2 --count 10 --combine MAX -o candidates-formula.txt
```

To regenerate the user-confirmed linked latest-college Export architecture from `[user-education-schools-root]` and run its local construction regression (not an Element runtime test):

```bash
python3 scripts/build_linked_index_weight_export.py --output /tmp/college-name-formula.txt
python3 scripts/test_linked_index_weight_export.py
python3 scripts/formula_lint.py /tmp/college-name-formula.txt --strict-functions --export
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

To test abstract application ranking, global ties, aligned blank outputs, and per-GUID coverage:

```bash
python3 scripts/test_application_selection_invariants.py
```

This test uses fictional candidates and precomputed ranks; it does not execute Element formulas, parse live root data, or verify tenant maps.

To regression-check bounded primary/secondary term-source precedence and shared output projection:

```bash
python3 scripts/test_term_fallback_invariants.py
```

This additional test uses a fictional abstract rank model, not an Element formula interpreter.

To regression-check the provisional first/second optional-email extraction design:

```bash
python3 scripts/test_ordinal_email_exports.py
```

This tests a local Python model of the string operations against fictional JSON fixtures. It does not execute Element formulas or verify the live serializer, label membership, Evaluate, or Preview Export. The examples remain runtime-unverified.

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
7. A request to record lessons is not confirmation that a preceding formula worked. Retain missing-sample assumptions and unverified runtime status; report local checks only when their execution is available, not merely because a prior assistant claimed a test count.
8. Use **user-verified** only for behavior actually observed; keep untested formulas labeled **static-lint clean** or **design target**. A general "worked correctly" confirms the assembled solution only to the reported scope, not every branch, variant, execution surface, or suspected root cause. Do not apply that confirmation to a subsequently delivered companion formula without separate feedback.

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
