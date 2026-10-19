#!/usr/bin/env python3
"""Local regression for generator shape and school-selection design.

Only the original delivered formula was user-confirmed inside Element451. This
script does not emulate Element formula execution and cannot verify Preview Export.
"""

import hashlib
from build_linked_index_weight_export import generate

# Fingerprint of the user-confirmed 19,650-character baseline, without newline.
BASELINE_SHA256 = "44e03ac953d858d158a611a4c61b8a51f76e9dc71b1d503433802244ac0a032a"


def expected_school_name(records):
    """Python model of *intended* semantics, not an Element runtime evaluator."""
    eligible = [
        (r["index_weight"], i, r.get("name", ""))
        for i, r in enumerate(records)
        if r.get("type") == "college" and
        type(r.get("index_weight")) is int and
        0 <= r["index_weight"] <= 999999
    ]
    return max(eligible)[2] if eligible else ""


def test_baseline():
    formula = generate()
    assert len(formula) == 19650, len(formula)
    assert hashlib.sha256(formula.encode("utf-8")).hexdigest() == BASELINE_SHA256
    assert formula.count('IF((REGEXP_MATCH(') == 20
    assert '"""name"":""(.*?)"""' in formula


def test_overrides():
    f = generate(root='[user-example-root]', eligible_value='university',
                 rank_key='sequence_no', output_key='institution',
                 max_objects=3, rank_width=4)
    assert '[user-example-root]' in f
    assert '"""type"":""university"""' in f
    assert '"""sequence_no"":' in f
    assert '"""institution"":""(.*?)"""' in f
    assert f.count('IF((REGEXP_MATCH(') == 3
    for bad in ['<not-a-token>', '[unsafe] stuff']:
        try:
            generate(root=bad)
        except ValueError:
            pass
        else:
            raise AssertionError('bad root accepted')


def test_intended_semantics():
    cases = [
        ([{'type':'college','entry_type':'home_schooled','name':'A','index_weight':1}], 'A'),
        ([{'type':'college','name':'A','index_weight':1},
          {'type':'highschool','name':'HS','index_weight':99},
          {'type':'college','name':'B','index_weight':3}], 'B'),
        ([{'type':'college','name':'A','index_weight':20},
          {'type':'college','name':'B','index_weight':2},
          {'type':'college','name':'C','index_weight':9}], 'A'),
        ([{'type':'college','name':'A','index_weight':1},
          {'type':'college','index_weight':3}], ''),
        ([{'type':'highschool','name':'HS','index_weight':99}], ''),
        ([], ''),
        ([{'type':'college','name':'A','index_weight':5},
          {'type':'college','name':'B','index_weight':5}], 'B'),
    ]
    for records, expected in cases:
        assert expected_school_name(records) == expected


if __name__ == '__main__':
    test_baseline()
    test_overrides()
    test_intended_semantics()
    print('PASS: exact original formula, generator overrides, and intended-selection model')
    print('NOTE: not an Element451 runtime or Preview Export test')
