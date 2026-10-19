# Term selection with a secondary root-field source

## Table of contents

- [Evidence and limits](#evidence-and-limits)
- [Define fallback by eligibility, not by a blank output](#define-fallback-by-eligibility-not-by-a-blank-output)
- [Transfer conditions between roots explicitly](#transfer-conditions-between-roots-explicitly)
- [Diagnose a missing season independently of the year](#diagnose-a-missing-season-independently-of-the-year)
- [Keep season and year on one selector](#keep-season-and-year-on-one-selector)
- [Preserve guarded same-object parsing](#preserve-guarded-same-object-parsing)
- [Bound numeric source priorities](#bound-numeric-source-priorities)
- [Regression checks](#regression-checks)

## Evidence and limits

Record the September 2026 feedback narrowly: after receiving revised term-season export formulas with normalization, a same-term mapped-name fallback, revised object bounding, and an application-root fallback, the user reported that the formula worked correctly. This supports **user-reported success of the assembled season solution in that task**. The user did not identify the individual records, degree variant, isolated failing component, or whether the confirmation came from Evaluate, Preview Export, or a completed export. Do not claim every branch or both variants were separately runtime-tested.

The companion year formulas were subsequently delivered, but no separate user confirmation of their runtime results was supplied. A maintenance comparison of the delivered files verified that each season/year pair has the same selection expression, with only the final projection changed. This is structural evidence, not an Element runtime test. Do not promote earlier assistant-reported simulation counts into user-verified results.

Do not assert a definitive cause for the original missing-season symptom. Several layers were changed together, and the affected term's raw code/name and root object were not supplied. Keep the possible normalization and record-boundary explanations as hypotheses.

Keep identifiers, degree allow-lists, term abbreviations, session equivalences, period order, hierarchy, source precedence, century assumptions, and scan ceilings request-scoped. Do not bundle the original production formulas or tenant mappings.

## Define fallback by eligibility, not by a blank output

When the requested policy gives milestones precedence over applications, select an eligible milestone first and use an application only when no scanned milestone satisfies the declared eligibility conditions. Do not let a newer application override an eligible milestone. Treat this as a requested policy, not a platform default.

Distinguish three states:

1. No eligible primary record exists: allow the secondary-source scan to supply the result.
2. An eligible primary record exists but the requested output cannot be decoded: retain that primary selection and apply the declared unknown-output policy.
3. An eligible primary record exists with a decodable output: return that projection.

A blank season is not, by itself, proof of state 1. Avoid implementing source fallback as `primary season = ""` unless fallback on decoding failure is explicitly required. A nonblank but unrecognized term code can satisfy an existing eligibility rule while yielding an unknown season. Conversely, when the declared eligibility requires a nonblank mapped code, a missing or blank code makes the record ineligible even if its name is recognizable. Preserve the requested distinction; do not silently add or remove that requirement.

Select the most recent eligible secondary term according to the task's own term ordering. Return the declared empty value when neither source has a qualifying candidate.

## Transfer conditions between roots explicitly

Use the correct field from each bounded object: an application-definition identifier can appear as `application_guid` on a milestone and `guid` on an application. Verify these keys in the current serializer. They are not interchangeable with a registration identifier.

Apply the same requested application allow-list and mapped major classification independently to each source's own object. Reuse `FIRST(DB_MAP("major", major_guid, "guid", "degrees", ""))` when the task calls for the existing scalar core-major degree mapping, including the previously observed inactive-major behavior. Do not turn `FIRST` into an any-associated-degree test.

Apply canonical type eligibility and any requested milestone hierarchy only to milestones. Do not invent corresponding application types, status requirements, submitted-only filters, timestamps, or completeness preferences. Add such application restrictions only when requested.

## Diagnose a missing season independently of the year

A correct numeric year does not prove that the season was decoded or that independently written columns selected the same record. A formula can recognize a year suffix while failing to recognize the prefix used for the season.

Inspect the selected term GUID, its raw mapped code/name, the normalized code, and the independently derived year and period. Use visible boundaries to reveal whitespace. This diagnostic requires replacing the conspicuous placeholder with a verified current-task term GUID:

<!-- formula-lint: export -->
```text
CONCAT(
    "Raw code: >",
    DB_MAP("term", "<TERM_GUID>", "guid", "code", ""),
    "< | Normalized code: >",
    UPPER(TRIM(DB_MAP("term", "<TERM_GUID>", "guid", "code", ""))),
    "< | Raw name: >",
    DB_MAP("term", "<TERM_GUID>", "guid", "name", ""),
    "<"
)
```

Normalize case and surrounding spaces before matching when those differences are insignificant under the task's code convention. Do not treat an unrecognized abbreviation as a known season without a mapping. A mapped-name fallback may resolve the **same term's** period when its code prefix is unrecognized; define the permitted name patterns and keep that decoding fallback separate from source fallback. A name check after eligibility does not make a blank code eligible.

Do not automatically blame numbered session variants. If the formula already uses only a fixed-length prefix and the variants share that prefix, the added session digit alone cannot explain a different result. Collapse sessions only when the user states that they are equivalent. Derive supported code forms, period ordering, and the year window from the current request. Numeric suffix validation alone does not establish that the complete term code is valid.

## Keep season and year on one selector

Generate companion formulas from one shared selection expression. Keep candidate inventory, same-object extraction, eligibility, source precedence, term normalization, unknown-term policy, hierarchy, ties, and occurrence limits identical. Change only the final season/year projection. Compare the selectors programmatically while ignoring formatting outside quoted strings; do not normalize characters inside literal markers or regex patterns.

Adding fallback to only the season formula can produce a season with no year on application-only records. Update the companion selector too when requested, but do not modify a working companion output without authorization.

Define the sorting precedence explicitly. Most-recent-term-first with milestone hierarchy only inside an equal term differs from year-first, then hierarchy, then period. Under equal-term-only hierarchy, choosing another milestone in that same term cannot change the season or year; it may still matter for a later associated output.

Validate missing-data behavior before formatting. A numeric source-priority offset must not leak into the displayed year or period. Avoid using a legitimate year as a generic no-match sentinel; use an explicit no-candidate state or prove that the chosen sentinel is outside the requested year domain. A field named "academic year" does not by itself authorize changing a calendar-year result into an academic-year range.

## Preserve guarded same-object parsing

Read `references/root-field-parsing.md` and `references/root-field-occurrence-guards.md`. Guard every raw nth occurrence before reconstruction, then obtain all required properties from the same bounded record.

When several milestone types share one application allow-list, a working per-application occurrence scan can be retained with an independent canonical-type check. Do not enumerate by a mutable display-name value. Distinguish using the `name` property as a verified structural boundary from matching a particular milestone name.

A `name`-anchored milestone prefix/suffix reconstruction and a `guid`-first application boundary are serializer-specific techniques, not universal JSON parsing. Do not copy either boundary without the current sample or scoped user confirmation. A suspicious punctuation delimiter is a diagnostic lead, not proof of the actual defect. Account for spacing, reordered keys, nested duplicate `term`/`major`/`name`/`guid` keys, and imitated boundary text. Broader key-based boundaries can avoid one punctuation assumption while retaining other structural risks.

State coverage separately for each root and allowed identifier. In a raw per-identifier scan, ineligible occurrences consume slots; an eligible primary record beyond the ceiling can therefore make the formula fall back even though an eligible milestone exists elsewhere in the unscanned data. Never describe bounded fallback as an exhaustive absence check.

## Bound numeric source priorities

An explicit primary-exists branch is the clearest source-precedence design. A packed numeric score can avoid repeating a large primary selection expression, but use it only with a bounded domain and a verified decoding scheme. The delivered season solution used source-priority offsets plus term/type ranks; do not copy its numeric constants as reusable defaults.

Use these design invariants:

- Reserve zero for an absent or ineligible candidate. Give an eligible candidate a positive source score even when a permitted unknown term has zero detail rank.
- Make the lowest eligible primary score greater than the highest possible secondary score. A plain `MAX` over untagged term ranks does not implement fallback.
- Make each higher-priority dimension dominate the entire range of all lower-priority dimensions. Keep milestone-type rank below one unit of term rank when type is only a same-term tie-breaker.
- Remove source and subordinate rank components correctly before formatting either projection. Preserve unknown-output state; do not manufacture a year from a zero detail rank.
- Check integer precision and score bounds, then recheck them if year range, periods, types, sources, or encoding bases change. Do not assert performance improvements without measurements.

This source/term score is not the aligned output-slot-list design in `references/application-root-linked-exports.md`. Success of one does not prove the other's delimiter, empty-slot, or runtime behavior.

## Regression checks

Run `python3 scripts/test_term_fallback_invariants.py` for the fictional, abstract source-ranking model. The tests do not parse root fields, resolve live maps, or execute Element formulas.

For the actual delivered formulas, check: eligible primary only; eligible application only; older eligible primary versus newer application; no eligible record; invalid earlier occurrence followed by a valid one; both classification groups; known and unrecognized term prefixes; case/space variants; an approved same-term name fallback; blank-code eligibility; eligible primary with undecodable output; year and period boundaries; equal-term hierarchy; sparse occurrences; ineligible raw slots; each coverage ceiling and one beyond it; and matching season/year selectors. Verify Evaluate and actual Preview Export separately when available, and record exactly which results the user confirms.
