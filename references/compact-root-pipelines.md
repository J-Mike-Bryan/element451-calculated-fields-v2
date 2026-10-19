# Compact root-field pipelines: filter, serialize, compare, project

## Table of contents

- [Purpose and evidence](#purpose-and-evidence)
- [Performance warning, not an official limit](#performance-warning-not-an-official-limit)
- [When to use this method](#when-to-use-this-method)
- [Obtain the current task contract](#obtain-the-current-task-contract)
- [Why large expressions grow](#why-large-expressions-grow)
- [Stage 1: guarded producers](#stage-1-guarded-producers)
- [Stage 2: normalized compact records](#stage-2-normalized-compact-records)
- [Stage 3: eliminate blocked candidates](#stage-3-eliminate-blocked-candidates)
- [Stage 4: select and project](#stage-4-select-and-project)
- [How fixed-width regex comparisons work](#how-fixed-width-regex-comparisons-work)
- [Reusable generator and examples](#reusable-generator-and-examples)
- [Coverage is a separate decision](#coverage-is-a-separate-decision)
- [Compatibility probe](#compatibility-probe)
- [Validation and deployment](#validation-and-deployment)
- [Failure modes and debugging](#failure-modes-and-debugging)
- [Evidence maintenance and source links](#evidence-maintenance-and-source-links)

## Purpose and evidence

Use this method to reduce repeated root extraction and lookup expansion in a standalone Element451 formula. Construct a small, validated text table inside the formula; run comparisons and selection against that table; return a payload or existence result. No saved helper field, auxiliary export column, API request, JavaScript execution, or general-purpose JSON parser is involved.

**Evidence update, September 2026:** the user reported that the delivered optimized export formulas worked well. Record the assembled compact-list approach as **user-confirmed in the reported export use case**. The report did not separately identify Evaluate, Preview Export, completed-export row reconciliation, timing measurements, every branch, or every individual diagnostic result. Do not invent that detail or require the original implementation to be described as wholly runtime-unverified after this feedback.

Distinguish that confirmation from the new, generalized generator bundled with this reference: the generator's role labels, configurable widths, ordering options, and policy switches have **local PHP PCRE regression tests**, not separate Element451 runtime confirmation. Revalidate each newly generated adaptation.

An observed optimization reduced the date-expression source from about 3.89 million to 109,195 characters and the boolean source from about 2.62 million to 96,544 characters, retaining the prior raw-occurrence coverage. These are source-size measurements, not execution-time speedups or universal target sizes. Do not carry the original institution's formulas or mappings into a new tenant. The historical counts in prior work are not this package's fresh test count.

## Performance warning, not an official limit

The user reported significant slowdowns and possible omitted export rows with very long formulas and described **approximately 500,000 characters** as a warning point from their own testing. They explicitly clarified that this is **not an official Element451 limit**.

Use that number only as an approximate, user-observed investigation trigger. Never claim that:

- 500,000 is an official hard maximum, parser limit, or universal timeout boundary;
- 499,999 characters is safe, or every longer formula necessarily fails;
- character count alone was proven to cause omitted rows;
- a smaller formula proves correctness, speed, or row completeness.

Measure the actual expression submitted, not the ZIP size or only a formatted preview. Distinguish Unicode character count from UTF-8 byte count, count with/without trailing newline consistently, and report nesting depth and source-level lookup call sites separately. A large regex can still be expensive on large subjects. Several calculated columns can repeat substantial work independently. No cross-column caching is established by this architecture.

Run `scripts/formula_size_report.py`. Its default warning is deliberately labeled approximate and user-reported; it is informational, not a syntax-validation failure. Treat any target character budget as task-specific engineering guidance rather than an Element guarantee.

## When to use this method

Prefer the existing guarded numeric `MAX`/`MIN` or `SUM` patterns for simple scalar questions. Consider a compact pipeline when repeated cross-record checks, linked outputs, tie-breaking, or repeated winner expressions make formulas unwieldy. Optimize shared construction before reducing coverage.

This method is especially useful when many root candidates require expensive maps, while the comparison needs only a normalized rank, a timestamp, and a small payload. It is not a general JSON query language, unbounded loop, automatic memoization feature, or substitute for obtaining the actual serialized schema.

## Obtain the current task contract

Collect the following from the current request or an explicitly authorized source. Do not inherit the original institution's settings:

1. Root token, exact discriminator, object boundaries, timestamp path and units.
2. Application/other identifier allow-lists; major/classification mapping; scalar-first versus any-associated-value semantics; behavior for inactive and unmapped values.
3. Primary rank mapping, ordering, equivalence normalization, year/century interpretation, and unknown-rank policy.
4. Separate eligibility rules for result candidates and evidence/blocker records.
5. Exact blocking predicates, exceptions, strict versus inclusive comparisons, missing-date policy, and whether cancellation of an earlier blocker is relevant.
6. Sort key direction, tie rule, associated payload, blank output, boolean representation, and timezone requirement.
7. Raw slots to scan per discriminator, maximum candidate rows, and any separately authorized limit on qualifying records.

Do not assume matching records must share exactly the same application or major identifier. "Each belongs to this allowed group" differs from "both share this exact identifier." Include additional equality fields in the compact schema when the current rule requires them.

## Why large expressions grow

Without local variables, a naive candidate-versus-evidence expression can repeatedly embed the entire root parser, maps, and evidence scan for every candidate, then repeat the resulting selector for no-match detection and projection. Complexity in **source expansion** can approach candidate count times evidence count times repeated outer uses. That statement does not establish an Element runtime complexity bound.

Use a compositional pipeline instead. The following is design notation, not paste-ready Element syntax:

```text
raw root
-> one guarded producer per covered raw slot
-> CONCAT(candidate rows, evidence rows)
-> candidate-elimination transform(s)
-> remove evidence rows
-> existence check OR bounded pairwise reduction
-> return payload
```

Every outer transform must contain its child expression **once** as an argument. Avoid `IF(big_selector = "", "", project(big_selector))` when a proven blank-safe projection can consume the selector once.

Be precise about "parse once": one producer is emitted per slot, but a producer may still repeat extraction for a guard, normalized value, and payload because no local binding exists. This method removes repeated *full scan expansion downstream*; it does not prove that Element caches every extraction or map. Never introduce an unsupported `LET`, lambda, array filter, or user-defined function.

## Stage 1: guarded producers

Read `references/root-field-parsing.md` and `references/root-field-occurrence-guards.md` first. Preserve the working serializer assumptions unless current samples justify a change.

For each planned occurrence:

1. Test the raw nth discriminator occurrence before reconstructing anything. Return empty text for absent slots.
2. Reconstruct/bound the current object's prefix and suffix; never let another object supply its properties.
3. Apply inexpensive exact identifier checks before more expensive maps.
4. Map the current object's classification once where a safe allow-list representation permits it.
5. Validate/map its rank, then validate date and payload requirements.
6. Emit one compact row, or an empty string if the record does not qualify.

Keep short-circuiting `IF` guards. In the user-confirmed implementation, replacing several repeated scalar comparisons on one mapped value with a single anchored alternation reduced map call sites. This is appropriate only for a verified regex-safe allow-list; arbitrary tenant strings need escaping or explicit equality. Do not replace exact GUID equality with an unescaped regex whose periods become wildcards. Do not extrapolate label-field `CONTAINS` anomalies to ordinary strings.

When a core major attribute must resolve inactive records, preserve the established `FIRST(DB_MAP("major", major_guid, "guid", "degrees", ""))` architecture when applicable. Obtain the degree allow-list from the current task. `FIRST` means first-associated classification, not any classification. Do not silently change that policy while optimizing.

Candidate and blocker date requirements can differ. A missing timestamp may prevent chronological evidence but still allow rank-based evidence under the requested rule. Conversely, a result that requires a date may need to reject an undated candidate in its boolean companion too. Define this; do not infer it.

## Stage 2: normalized compact records

The reusable generator uses generic roles **C** (candidate) and **B** (blocker/evidence), not product status names. Use this grammar:

```text
C<fixed-width rank>:<fixed-width timestamp>=<safe payload>;
B<fixed-width rank>:<fixed-width timestamp>;
```

For example, a synthetic three-character rank and sixteen-character timestamp might produce:

```text
C014:0001700000000100=item_a;C014:0001700000000300=item_b;B013:0001700000000200;
```

These ranks are fictional already-normalized values, not real term codes or GUID mappings. The timestamp is a sort key; the illustrative payload is not a date assertion.

**Construction invariants:**

- Emit every C row before every B row. Forward-looking evidence checks depend on this ordering, even when the original root is interleaved.
- Emit no spaces or line breaks between rows. Invalid records produce no row, not a partially filled row.
- Encode rank/time as equal-width nonnegative ASCII decimal strings. Validate width and range before padding.
- Preserve a collision-free rank for categories that must count as distinct. Normalization may merge variants only when the current task explicitly declares them equivalent.
- Use a rank that preserves the intended chronological ordering; do not infer order from a GUID's numeric suffix. Prefer enough year information to avoid an unstated century rollover.
- Keep the payload single-line and delimiter-safe. It must not contain `;` or text that can impersonate a C/B record. Date-only numeric payloads are convenient. Arbitrary names, JSON, or other free text require a tested escaping/encoding scheme; the included helper does not provide one.
- Preserve full timestamp precision for ordering, even when the displayed payload is date-only.

### Numeric transport and width

An established construction pads with `RIGHT(CONCAT(zero_padding, numeric_timestamp), width)`. This is safe only after domain validation: `RIGHT` silently truncates over-width input. Do not let malformed, negative, fractional, or scientific-notation values masquerade as fixed-width integer keys.

Sixteen digits is a **representation width**, not proof that all sixteen-digit numbers survive `VAL` and numeric-to-text conversion exactly. When floating-point transport is possible, remain within an independently verified exact-integer domain (a conservative binary64 boundary is 2^53 - 1), or preserve validated raw digit strings without a numeric round trip. Ordinary thirteen-digit epoch milliseconds fit that conservative bound, but still test actual Element serialization. Do not pack rank and milliseconds into an enormous arithmetic score and assume low-order digits remain exact.

If zero is the missing-time sentinel, keep that convention separate from candidate eligibility. Do not convert a zero sentinel into a real date. Literal-table PCRE tests cannot verify Element numeric coercion.

### Date payloads versus timestamp keys

In the confirmed compact date architecture, each eligible result candidate computes its formatted date payload once in its producer, using integer epoch seconds for `DATE_READ(..., "U")`; the raw millisecond key remains attached for comparison. The reducer carries that payload unchanged. It is incorrect to describe this exact implementation as formatting only the eventual winner.

A newly designed variant can instead carry raw milliseconds and format only the selected payload, but that is an adaptation requiring a safe blank guard and no duplicated selector. Do not change timezone handling as an accidental part of optimization.

## Stage 3: eliminate blocked candidates

Define rejection independently from ranking. Keep all relevant evidence rows until every rejection pass has completed. Remove only the C row; use a lookahead to inspect evidence without consuming it. Otherwise one match can accidentally destroy a blocker needed to reject another candidate.

The helper offers two **opt-in predicates**, not default institutional policy:

```text
reject_newer_rank:
    exists eligible B with B.rank > C.rank

reject_later_different_rank:
    exists eligible B with B.timestamp > C.timestamp
    AND B.rank != C.rank
```

Enable only the predicates the current user requires. In the second predicate, exact timestamp equality is not "after," and same normalized rank bypasses only that predicate. Evidence from another rank can still reject the candidate. A matching-rank exception is not a blanket permission overriding every other blocker.

The generic same-rank key must represent the equivalence group needed by the exception. If sort rank and group identity are different concepts, expand the schema rather than applying `rank != rank` to a lossy key.

Apply these predicates to **each candidate before selecting the winner**. Selecting first and rejecting only that winner can hide another surviving candidate. A later result-candidate record can remain eligible after an earlier one was superseded; do not collapse their timestamps prematurely.

After all filters, remove B records with their exact row grammar. The resulting string contains only surviving C rows, or is empty.

## Stage 4: select and project

### Existence

After eliminating disqualified candidates and removing B rows, the string is nonempty exactly when at least one C survives. Use one `IF(filtered_table <> "", "TRUE", "FALSE")` without running an unnecessary selection tournament. These are text booleans; adapt to the requested destination type.

The filtered table above is conceptual notation. The generator fully expands its single child expression; it does not insert an undefined variable or export-column reference.

### Linked payload selection

Select adjacent pairs by the requested primary rank direction, then timestamp direction. Preserve the entire winning row so the payload cannot detach from its keys. An exact key/time tie keeps the left row in the bundled generator, establishing deterministic earliest-serialized priority.

Use a global replacement that turns each adjacent pair into one winning row. An unpaired final row remains unchanged. After one pass, at most ceil(N/2) candidates remain. Emit **ceil(log2(N)) passes** for a maximum of N candidates; for N=1, emit zero passes. For ten candidates, four passes suffice; for seventeen, five are required. The capacity is the maximum C rows, not all candidate-plus-evidence rows.

This is a generated, finite number of nested replacements, not a runtime loop or convergence test. Insufficient passes silently leave multiple survivors, and a final first-match extraction may return the wrong one. State the capacity and test at/above it.

Finish with `REGEXP_EXTRACT(reduced_table, "=(.*?);")` only when empty-input behavior and payload safety are established. Preserve a legitimately blank payload on the selected winner; do not automatically choose a lower-ranked record with a nonblank payload. Companion output columns must share exactly the same eligibility and selector, even when their payload projections differ.

## How fixed-width regex comparisons work

The comparison stage uses decimal order, not raw string order on unpadded timestamps. Given equal-width nonnegative digit strings, numeric order equals lexicographic order. Find their common prefix and the first position where the digits differ. For a strict greater-than comparison, the right-side differing digit must be larger.

The generator captures an arbitrary common digit prefix with a named group, then enumerates the possible differing left digits 0 through 8 and corresponding larger right digits. For less-than, it enumerates left digits 1 through 9 and the smaller right digits. Identical strings have no differing position and therefore do not satisfy a strict comparison.

The surrounding row grammar and terminating delimiters are essential. They constrain field widths and prevent a prefix/suffix match from becoming a comparison across different fields. The prefix capture may backtrack to the actual first differing digit. Test long shared prefixes, leading zeros, equal values, and differences at every position.

### Export-compatible regex construction

Use noncapturing digit alternation `(?:0|1|2|3|4|5|6|7|8|9)` instead of square-bracket digit classes. The delivered method avoided both square-bracket regex classes and regex backslash escapes to reduce known Export Preview transport risks. Use `(?P<name>...)` for named captures and `(?P=name)` for pattern backreferences; these are not Element variables.

Use `${n}` for a numbered **replacement** capture. Do not confuse replacement captures with named pattern backreferences. Noncapturing groups must remain noncapturing when editing the generated patterns.

The bundled pair selector captures three comparison groups before its winner groups. Therefore its replacement is `${4}${5}`: one branch populates the right winner, the other populates the left winner. Unmatched alternate-branch captures must become empty for this construction. Adding a new capturing group shifts those indices and can corrupt output without an obvious syntax error. Rebuild and retest rather than hand-editing capture numbers.

PHP documentation supports the underlying syntax, but does not by itself prove that an Element wrapper, other formula context, or future release exposes every construct unchanged. User confirmation supports the delivered assembled export method, not every possible PCRE feature. Keep small compatibility tests available.

## Reusable generator and examples

Use `scripts/compact_record_pipeline.py` to generate the compact-table transforms, preserving the nested child expression once at each stage. It accepts an Element expression that already constructs the validated C/B table. It does **not** build tenant-specific root extraction, decide eligibility, look up terms, or sanitize arbitrary payloads.

A complete synthetic input expression is in `references/compact-pipeline-literal-input.txt`. Generate a payload result with explicit mathematical ordering and opt-in blockers:

```bash
python3 scripts/compact_record_pipeline.py \
  --input references/compact-pipeline-literal-input.txt \
  --output /mnt/data/compact-example.txt \
  --projection payload --rank-width 3 --time-width 16 \
  --candidate-capacity 3 --rank-order max --time-order min \
  --reject-newer-rank --reject-later-different-rank
python3 scripts/formula_lint.py /mnt/data/compact-example.txt --strict-functions --export
```

The expected synthetic payload is `item_b`: the first candidate is blocked by later evidence for a different rank; the second survives. This illustrates the algorithm only, not an institution's withdrawal policy. Change `--projection boolean` to produce `"TRUE"` for the same table.

A complete generated copy is included as `references/compact-pipeline-literal-output.txt`. No placeholders or omitted branches occur in that literal example. For real data, replace the input expression with the guarded producers built from the current task and validate the complete resulting formula.

## Coverage is a separate decision

Never equate **first K raw occurrences** with **first K qualifying records**. If the first three raw records fail the eligibility filter, a qualifying fourth is missed by a three-slot scan. To stop at three valid records, first inspect a defined raw universe, filter, then count retained candidates; an arbitrary raw position cap is not a valid-match cap.

The successful optimization retained the prior fixed raw coverage rather than discarding additional valid records. Reuse that principle, not an institution-specific default number. A smaller post-filter table still requires scanning enough raw records to establish membership. Discarding a fourth valid blocker can change a status result even when such records are rare. Do not promise semantic equivalence beyond the accepted coverage.

For a one-based marker split where occurrence one is segment two, inspect segment **N+2** to flag an N+1st raw occurrence. Guard that diagnostic with the same verified marker semantics. A coverage flag means possible truncation, not proof the output is wrong. Distinguish per-type, per-GUID, and total-root ceilings.

Apply these principles separately to `[user-applications-root]`. Do not add an application fallback, assume milestone boundaries match application boundaries, or count application-submit milestones as application objects unless requested. A future application's three-valid-record cap requires its own serializer, submission test, mapping, and candidate-order definition.

## Compatibility probe

Use the bundled `references/compact-pipeline-compatibility-probe.txt` in a new target context. Its expected result is `PASS`. The probe has no tenant fields or mappings and is reproduced here:

<!-- formula-lint: export -->
```text
IF(
    (REGEXP_REPLACE("stage04", "^stage(..)$", "0${1}") = "004")
    & (REGEXP_MATCH("014:014", "^(?P<t>...):(?P=t)$") = TRUE)
    & (REGEXP_MATCH("014:013", "^(?P<t>...):(?P=t)$") = FALSE)
    & (REGEXP_REPLACE("AB", "(?:(A)(X)|(A)(B))", "${1}${4}") = "B")
    & (RIGHT(CONCAT("0000000000000000", MAX(0, VAL("1700000000123"))), 16) = "0001700000000123")
    & (REGEXP_EXTRACT("", "=(.*?);") = ""),
    "PASS",
    "FAIL"
)
```

Do not claim the user separately ran this generalized probe. A FAIL/parser error is a reason to isolate the failing primitive, not to deploy the full adaptation. Probe success does not prove row parsing, maps, policies, coverage, or full-export performance.

## Validation and deployment

Run the following checks before calling an adaptation ready:

1. Lint the complete formula with `--strict-functions --export`. Format a readable copy and verify that string literal contents are unchanged. Never minify by deleting whitespace inside all strings.
2. Measure raw/paste-ready characters, bytes, nesting depth, field references, and lookup call sites. Identify the component responsible for remaining expansion; do not use ZIP compression as an optimization metric.
3. Run `scripts/test_compact_record_pipeline.py`. It uses PHP CLI and synthetic normalized records. It checks pair reduction, evidence filters, ties, equality boundaries, odd capacities, varying widths, ordering combinations, and source-expression nonduplication. It does not execute Element or the root producer.
4. Inspect actual producers with redacted current records. Test absent raw slots, alternate milestone names, reordered properties, mixed eligibility, and later valid occurrences after invalid earlier ones.
5. Run the compatibility probe and real-contact Evaluate. Test unknown maps/ranks, inactive records where applicable, missing/zero timestamps, same-group exceptions, later evidence for an earlier group, and a surviving second candidate after the first was invalidated.
6. Run actual Preview Export. Then run a small real export with stable IDs and compare **both expected IDs and total rows**, not just the calculated values. Examine validation, empty-value behavior, scope, and operation errors before attributing missing rows solely to source length.
7. Check records near local midnight for the intended timezone, and compare millisecond/second boundaries before date-only formatting. Verify completeness at maximum coverage and flag records exceeding it.

The fresh generalized helper regression run added with this reference passed **1,202 compact-table cases and 384 generated-formula static checks**, with zero mismatches. Those numbers describe this local test run, not user tests or Element execution. See `references/compact-pipeline-validation.json` for the retained run summary. The reproducible test script is the retained evidence; avoid treating old historical stress-test counts as newly rerun.

## Failure modes and debugging

| Symptom | Investigate |
|---|---|
| A later qualifying raw occurrence disappears | Raw coverage was reduced, or a valid-count cap was applied before eligibility. |
| Candidate falsely acquires a neighboring date | Missing raw-occurrence guard, incorrect object boundary, or unbounded property lookup. |
| Matching group unexpectedly blocks candidate | Group normalization collision/error, or a second independent blocker that the exception does not waive. |
| A second legitimate candidate is never considered | Selection ran before rejection, or the evidence scan was truncated. |
| Output contains partial keys or another payload | Capture numbering changed, delimiter collision occurred, or pair reduction consumed the wrong row. |
| More than one C row survives the tournament | Capacity exceeds the configured reduction rounds, or replacements are not global in this context. |
| Near-equal timestamps compare incorrectly | Unequal widths, leading sign, scientific notation, overflow/truncation, or lossy numeric transport. |
| Empty result becomes an epoch date | Sentinel converted without eligibility/blank handling. |
| Evaluate succeeds but export fails | Preview tokenization, wrapper differences, limits, or export settings; inspect the actual error. |
| Shorter formula is still slow or loses rows | Large subjects, repeated columns, regex backtracking/limits, costly maps, scope/validation, and operation-level failures; source size alone is not a diagnosis. |

Expose intermediate table output during debugging: producer table, post-first-filter, post-second-filter, C-only survivors, each reduction round, final payload. Return these only against redacted data or appropriate authorized records; do not publish student information as skill examples.

## Evidence maintenance and source links

Keep the procedural method tenant-neutral. Do not bundle the original institution's production formulas, identifier prefixes, numeric GUIDs, degree allow-lists, term abbreviations/equivalence conventions, custom fields, or business hierarchy as reusable defaults. Generic C/B records, explicit policy switches, fictional ranks, and source-size observations are sufficient to reproduce the technique.

Maintain separate confidence labels for: official Element function examples; PHP regex semantics; local static/PCRE tests; the user's reported assembled export success; and independently verified Evaluate/Preview/completed-export results. Extend evidence only as far as the report supports.

Official pages checked for this update (2026-09-28):

- Element451 calculated fields and contact-level evaluation: https://help.element451.io/en/articles/9007704-calculated-fields
- PHP named pattern backreferences: https://www.php.net/manual/en/regexp.reference.back-references.php
- PHP replacement captures: https://www.php.net/manual/en/function.preg-replace.php

The Element page documents common formula use and evaluation; it does not establish an official 500,000-character ceiling or an Element guarantee for this entire regex pipeline. PHP sources explain the underlying syntax, not tenant-specific Element behavior. Recheck current exact documentation when making new product claims.
