# Linked latest-school selection from a serialized root field

## Overview

- [User-confirmed scope and evidence](#user-confirmed-scope-and-evidence)
- [Source discriminator and recency key](#source-discriminator-and-recency-key)
- [Verified assembled architecture](#verified-assembled-architecture)
- [Generate a similar formula](#generate-a-similar-formula)
- [Serializer assumptions and limits](#serializer-assumptions-and-limits)
- [Evaluate and Preview Export cases](#evaluate-and-preview-export-cases)

## User-confirmed scope and evidence

An October 2026 user confirmed that an assembled Element451 **Export** formula correctly returned the newest uploaded college's `name` from `[user-education-schools-root]` using the highest numeric `index_weight` among college objects. The user's confirmation was "That formula worked"; the exact validation surface (Test Formula, Preview Export, or completed export) and individual edge cases were not separately reported. Do **not** claim those were proven or generalize this as a guarantee of the serializer across tenants or other root fields.

The standalone `scripts/build_linked_index_weight_export.py` generator's default settings **reproduce the exact 19,650-character text of that delivered, user-confirmed formula** (excluding any final newline). The script is a reproducible construction method, not an Element formula interpreter. When any setting or source schema changes, validate the newly generated formula in Element.

## Source discriminator and recency key

An illustrative, fictional compact root looks like:

```json
[
  {"type":"college","entry_type":"home_schooled","name":"Example College A","index_weight":2},
  {"entry_type":"highschool","type":"highschool","name":"Example High School","index_weight":9},
  {"type":"college","entry_type":"college","name":"Example College B","index_weight":5}
]
```

This intentionally demonstrates why `type` versus `entry_type` must be inspected rather than assumed synonymous. In the user-supplied record, a valid college had `"type":"college"` but `"entry_type":"home_schooled"`. The working formula therefore checks the same bounded object's **`"type":"college"`**, not its `entry_type`. In the fictional example the result is `Example College B` (weight 5): the high school at weight 9 is ineligible.

The user specified that **larger `index_weight` means uploaded later**. Treat this as the provided ranking contract, not a universal timestamp or Element ordering guarantee. It is independent from root array position, `graduate_date`, and `name`. A later serialized high-school object must not displace the newest eligible college. If another current record shows different `type`/`entry_type` semantics, establish the correct discriminator with the user or an Evaluate diagnostic before copying the pattern.

## Verified assembled architecture

This is **an argmax/linked-output selection**, not a filter and `MAX` of school names:

1. Scan raw serialized school **objects**, using `SPLIT_INDEX([user-education-schools-root], "},{", n)` for `n=1..20`. The supplied data is compact JSON with the exact boundary `},{`; scans need one object per bounded segment. Check matching `type` and a numeric `index_weight` in that *same* segment.
2. For qualifying objects, emit one compact row shaped `C<zero-padded-weight>:<zero-padded-slot>=<slot>;`. For example, the college in slot 3 with weight 5 produces `C000005:03=03;`. Emit `""` for all other objects. **Do not filter out a valid college simply because `name` is absent.**
3. Use the skill's existing `Pipeline(rank_width=6, time_width=2, candidate_capacity=20, rank_order="max", time_order="max")` compact reducer. Here its `time` dimension is the **serialized slot ordinal used only for tie-breaking**, not a timestamp. The first comparison maximizes numeric weight; a weight tie chooses the **later** array slot. Five pair-reduction passes suffice for up to 20 candidates. Preserve the associated slot payload as the winner.
4. Parse the selected slot with `VAL(CONCAT("0", winner_slot))`; adding one yields its `SPLIT_INDEX` index. Use a harmless `{}` prefix with `CONCAT("{}", "},{", [user-education-schools-root])` so selected raw slot 1 maps unambiguously to split index 2.
5. **Only after the winning slot has been selected**, extract that same object's `name` with a quoted-property regex. This avoids borrowing `name` from another object. When there is no eligible college, the empty winning slot maps to the dummy `{}` object, whose missing name projects to `""`. When the winner has a blank or absent name, return `""`; do not fall back to an older named college.

The implementation avoids `[...]` regex character classes because Export Preview may interpret bracketed strings as field tokens. It uses the digit alternation `(?:0|1|2|3|4|5|6|7|8|9)` instead and relies on normal Element escaped string syntax. The reducer builds/reduces the candidate table once; it does not multiply a large full scan by each output projection.

The technique generalizes to a **serialized root whose objects have a stable eligible category, nonnegative integer priority and linked text output**. Do not transplant the school-specific property names or `},{` delimiter into an unrelated source without inspecting that source's actual JSON.

## Generate a similar formula

From the skill directory:

```bash
python3 scripts/build_linked_index_weight_export.py --output /tmp/linked-school-name.txt
python3 scripts/formula_lint.py /tmp/linked-school-name.txt --strict-functions --export
python3 scripts/formula_size_report.py /tmp/linked-school-name.txt
```

Defaults reproduce the working school formula: root `[user-education-schools-root]`, eligible `type=college`, ranking `index_weight`, output `name`, 20 raw school objects, six rank digits. Adapt with the following supported options:

```bash
python3 scripts/build_linked_index_weight_export.py \
  --root '[user-education-schools-root]' \
  --eligible-key type --eligible-value college \
  --rank-key index_weight --output-key name \
  --max-objects 20 --rank-width 6 \
  --output /tmp/linked-school-name.txt
```

Run the exact formula in Test Formula/Evaluate and **actual Preview Export**, because the locally generated output is not runtime-tested just by compiling or linting. A new output property can be substituted with `--output-key` while preserving the winner-selection algorithm. Change the eligibility or rank key only when its semantics are established for the new source.

For output with rich JSON escapes, arbitrary delimiters, nesting, or a requirement to preserve exact original character encoding, do not assume the simple regex projection is sufficient. Obtain a representative sample and design/test a different serializer-aware extraction.

## Serializer assumptions and limits

- The raw field is **compact JSON** whose array objects are separated by the exact string `},{`. Whitespace such as `}, {` or an embedded `},{` within a value would break this splitting scheme. It is not a generic JSON parser.
- School objects can place `type`, `index_weight`, and `name` in different property orders; checks run over the whole bounded object. Property names must match exactly and output `name` must be a JSON string for the extraction pattern.
- With defaults, **only the first 20 raw school objects** are examined, *not* the first 20 colleges. A 21st college can be missed. Raise `--max-objects` when actual data requires it, then check formula length and runtime.
- With defaults, `index_weight` must be a nonnegative unquoted decimal integer of at most **six digits** (`0..999999`). Seven-plus digits can silently truncate via `RIGHT`, changing the rank; negative, null, decimal, and quoted values are not covered. Increase `--rank-width` only when actual data warrants it and test the numeric transport.
- Sorting is by `index_weight` **not by physical order**. On equal weights, the later serialized object wins. That tie policy was part of the delivered formula but was not independently confirmed by a reported Element tie-case test.
- A missing or blank `name` on the selected object returns blank rather than falling back. A JSON string containing escaped `\"` requires separate testing because the simple `(.*?)` quoted-string capture may truncate at an escaped quote.
- The confirmed behavior is scoped to the school-root export case. Different function contexts, serializers, keys, ranks, output types or scan widths need their own Evaluate and Preview checks.

## Evaluate and Preview Export cases

Test the generated adaptation on redacted records for the following expected behaviors; only the assembled original success was user-reported:

| Case | Expected result |
|---|---|
| One college whose `type=college` but `entry_type=home_schooled` | That college's name |
| High school has higher weight than all colleges | Newest **college**, not the high school |
| Colleges appear in array order 10, 2, 8 | College with weight 10 |
| Newest college has no name, older college has a name | Blank (do not borrow older name) |
| No colleges or completely empty root | Blank |
| Two colleges have equal weights | Name from later serialized college |
| College beyond configured raw-object ceiling | Increase ceiling and retest; old formula may miss it |
| Weight too large, negative, quoted, fractional, or absent | Outside default supported shape; adapt only after validation |
| Name has punctuation or an escaped quotation mark | Check full correct string output; no generic guarantee |

For future field variants, repeat a small completed-export comparison against the corresponding source records and check row completeness, rather than treating generator equivalence as live verification.
