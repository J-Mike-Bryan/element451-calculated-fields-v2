#!/usr/bin/env python3
"""Regression-test compact-table transformations with PHP PCRE, not Element451.

Tests only synthetic, already-normalized C/B records. It does not execute the
Element root extractor, lookups, timestamp coercion, or the export compiler.
"""
from __future__ import annotations
import argparse
import json
import random
import shutil
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from compact_record_pipeline import Pipeline, quote
from formula_lint import structural_checks, semantic_checks

PHP = r'''
$req = json_decode(stream_get_contents(STDIN), true, 512, JSON_THROW_ON_ERROR);
function apply_pattern($s, $p, $replacement) {
    $out = preg_replace('~'.$p.'~', $replacement, $s);
    if ($out === null) { throw new Exception(preg_last_error_msg()); }
    return $out;
}
$results = [];
foreach ($req as $job) {
    $s = $job['table']; $p = $job['patterns'];
    if ($job['rank_block']) { $s = apply_pattern($s, $p['reject_newer_rank'], ''); }
    if ($job['time_block']) { $s = apply_pattern($s, $p['reject_later_different_rank'], ''); }
    $s = apply_pattern($s, $p['remove_blockers'], '');
    $survivors = $s; $boolean = $s === '' ? 'FALSE' : 'TRUE';
    for ($i = 0; $i < $job['rounds']; $i++) {
        $s = apply_pattern($s, $p['reduce_pair'], $p['reduce_replacement']);
    }
    $match = []; $ok = preg_match('~'.$p['payload_extract'].'~', $s, $match);
    if ($ok === false) { throw new Exception(preg_last_error_msg()); }
    $results[] = ['survivors'=>$survivors, 'winner'=>$s,
                  'payload'=>$ok ? $match[1] : '', 'boolean'=>$boolean];
}
echo json_encode($results, JSON_THROW_ON_ERROR);
'''


def encode(candidates: list[tuple[int, int, str]], blockers: list[tuple[int, int]], p: Pipeline) -> str:
    return ''.join(f'C{k:0{p.rank_width}d}:{t:0{p.time_width}d}={v};' for k, t, v in candidates) + ''.join(
        f'B{k:0{p.rank_width}d}:{t:0{p.time_width}d};' for k, t in blockers)


def reference(candidates: list[tuple[int, int, str]], blockers: list[tuple[int, int]], p: Pipeline) -> dict:
    survivors = [c for c in candidates if not any(
        (p.reject_newer_rank and b[0] > c[0]) or
        (p.reject_later_different_rank and b[0] != c[0] and b[1] > c[1]) for b in blockers)]
    # Stable min keeps the first serialized row on an exact key/time tie.
    key = lambda c: ((-c[0] if p.rank_order == 'max' else c[0]),
                     (-c[1] if p.time_order == 'max' else c[1]))
    winner = min(survivors, key=key) if survivors else None
    return {'survivors': encode(survivors, [], p),
            'winner': encode([winner], [], p) if winner else '',
            'payload': winner[2] if winner else '',
            'boolean': 'TRUE' if survivors else 'FALSE'}


def cases(random_cases: int) -> list[tuple[Pipeline, list, list]]:
    rng = random.Random(4512026)
    result = []
    explicit = [
        ([], []), ([(14, 100, 'only')], []),
        ([(14, 100, 'blocked')], [(15, 0)]),
        ([(14, 100, 'earlier_group_later_time')], [(13, 101)]),
        ([(14, 100, 'same_group_exception')], [(14, 101)]),
        ([(14, 100, 'equal_time')], [(13, 100)]),
        ([(14, 100, 'old'), (14, 102, 'new')], [(13, 101)]),
        ([(14, 100, 'first'), (14, 100, 'second')], []),
        ([(14, 300, 'late'), (14, 100, 'early'), (13, 400, 'other')], []),
        ([(14, 100, 'candidate')], [(14, 999), (13, 101)]),
        ([(999, 9999999999999998, 'big'), (999, 9999999999999999, 'bigger')], []),
        ([(0, 1, 'zero_rank'), (1, 1, 'one_rank')], []),
    ]
    for rank_order in ('max', 'min'):
        for time_order in ('min', 'max'):
            for rank_block in (False, True):
                for time_block in (False, True):
                    p = Pipeline(3, 16, 10, rank_order, time_order, rank_block, time_block)
                    result.extend((p, c, b) for c, b in explicit)
    for capacity in (1, 2, 3, 5, 10, 11, 16, 17, 32, 33):
        p = Pipeline(3, 16, capacity, 'max', 'min', True, True)
        c = [(50, 1000 - i, f'item_{i}') for i in range(capacity)]
        result.append((p, c, []))
    for _ in range(random_cases):
        capacity = rng.choice((1, 3, 10, 17, 33))
        rw, tw = rng.choice(((2, 4), (3, 16), (4, 13)))
        p = Pipeline(rw, tw, capacity, rng.choice(('max','min')), rng.choice(('max','min')),
                     rng.choice((False,True)), rng.choice((False,True)))
        rank_pool = [rng.randrange(10**rw) for _ in range(4)]
        base = rng.randrange(1, 10**tw - 100)
        time_pool = [0, 1, base, base + 1, base + 2, 10**tw - 1]
        c = [(rng.choice(rank_pool), rng.choice(time_pool[1:]), f'item_{i}')
             for i in range(rng.randrange(capacity + 1))]
        b = [(rng.choice(rank_pool), rng.choice(time_pool)) for _ in range(rng.randrange(16))]
        result.append((p, c, b))
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--random-cases', type=int, default=1000)
    ap.add_argument('--report', type=Path)
    args = ap.parse_args()
    if not shutil.which('php'):
        print('PHP CLI is required for this local PCRE test. Element runtime tests are separate.', file=sys.stderr)
        return 2
    if args.random_cases < 0:
        ap.error('--random-cases must be nonnegative')
    suite = cases(args.random_cases)
    jobs = [dict(table=encode(c,b,p), patterns=p.patterns(), rounds=p.rounds,
                 rank_block=p.reject_newer_rank, time_block=p.reject_later_different_rank) for p,c,b in suite]
    response = subprocess.run(['php', '-r', PHP], input=json.dumps(jobs), text=True, capture_output=True, timeout=90)
    if response.returncode:
        print(response.stderr, file=sys.stderr)
        return 1
    observed = json.loads(response.stdout)
    assert len(observed) == len(suite)
    for i, ((p,c,b), actual) in enumerate(zip(suite, observed)):
        expected = reference(c,b,p)
        if actual != expected:
            raise AssertionError(json.dumps({'case':i, 'config':asdict(p), 'table':jobs[i]['table'],
                                             'actual':actual, 'expected':expected}, indent=2))
    # Lint complete generated literal examples for each projection and policy combination.
    formula_checks = 0
    for p,c,b in suite[:192]:
        for mode in ('payload','boolean'):
            formula = p.formula(quote(encode(c,b,p)), mode)
            diagnostics = structural_checks(formula) + semantic_checks(formula, strict_functions=True, export_context=True)
            errors = [d for d in diagnostics if d.severity == 'error']
            assert not errors, errors
            assert formula.count(quote(encode(c,b,p))) >= 1
            formula_checks += 1
    # The source table expression must occur once; it must never be duplicated by a reducer.
    p = Pipeline(3,16,10,'max','min',True,True)
    marker = 'CONCAT("source_expression_marker")'
    assert p.formula(marker, 'payload').count(marker) == 1
    assert p.formula(marker, 'boolean').count(marker) == 1
    for name, pat in p.patterns().items():
        assert '[' not in pat and ']' not in pat and '\\' not in pat, name
    report = {'compact_table_cases':len(suite), 'formula_static_checks':formula_checks,
              'mismatches':0, 'engine':'local PHP PCRE', 'element451_runtime_tested':False,
              'scope':'Synthetic normalized records only; not root parsing, tenant lookups, coercion, or performance.'}
    print(json.dumps(report, indent=2))
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
