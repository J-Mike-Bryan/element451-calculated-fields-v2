#!/usr/bin/env python3
"""Build a tenant-neutral Element formula suffix for an already-filtered table.

This is a formula GENERATOR, not an Element runtime or JSON parser. Input must
be one expression producing C<rank>:<time>=<payload>; rows, then B<rank>:<time>;
rows. All ranks/times must be validated, nonnegative fixed-width ASCII digits.
Payloads must be single-line, contain no semicolon, and contain no fake C/B row
fragments. Use references/compact-root-pipelines.md before adapting this code.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

DIGIT = '(?:0|1|2|3|4|5|6|7|8|9)'
PAYLOAD = '(?:(?!;).)*'


def quote(value: str) -> str:
    """Escape Element string syntax; do not add PCRE slash delimiters."""
    return '"' + value.replace('"', '""') + '"'


def alternatives(values: range) -> str:
    items = [str(v) for v in values]
    if not items:
        raise ValueError('A digit comparison must have a nonempty range.')
    return items[0] if len(items) == 1 else '(?:' + '|'.join(items) + ')'


def first_difference(bridge: str, prefix_name: str, right: str) -> str:
    """Compare equally wide keys using a shared prefix and first unequal digit.

    The surrounding pattern supplies the captured shared prefix and the key
    terminator. `bridge` crosses from the end of the left key to the right key.
    All groups generated here are noncapturing except the named backreference.
    """
    if right not in {'greater', 'smaller'}:
        raise ValueError('right must be greater or smaller')
    result = []
    for left in range(9) if right == 'greater' else range(1, 10):
        values = range(left + 1, 10) if right == 'greater' else range(left)
        result.append(
            f'{left}{DIGIT}*{bridge}(?P={prefix_name})'
            f'{alternatives(values)}{DIGIT}*'
        )
    return '(?:' + '|'.join(result) + ')'


@dataclass(frozen=True)
class Pipeline:
    rank_width: int
    time_width: int
    candidate_capacity: int
    rank_order: str
    time_order: str
    reject_newer_rank: bool = False
    reject_later_different_rank: bool = False

    def __post_init__(self) -> None:
        if not 1 <= self.rank_width <= 16 or not 1 <= self.time_width <= 16:
            raise ValueError('Widths must be between 1 and 16; verify exact numeric transport separately.')
        if not 1 <= self.candidate_capacity <= 10000:
            raise ValueError('candidate_capacity must be between 1 and 10000 (generator guard, not an Element limit).')
        if self.rank_order not in {'max', 'min'} or self.time_order not in {'max', 'min'}:
            raise ValueError('Orders must be max or min.')

    @property
    def rounds(self) -> int:
        return (self.candidate_capacity - 1).bit_length()

    def patterns(self) -> dict[str, str]:
        rank = DIGIT + '{' + str(self.rank_width) + '}'
        time = DIGIT + '{' + str(self.time_width) + '}'
        row = f'C{rank}:{time}={PAYLOAD};'
        block = f'B{rank}:{time};'
        # Lookahead finds evidence but only the C row is consumed/deleted.
        rank_bridge = f':{time}={PAYLOAD};.*B'
        rank_test = 'C(?P<h>' + DIGIT + '*)' + first_difference(rank_bridge, 'h', 'greater') + ':'
        term_block = f'(?={rank_test}){row}'
        time_bridge = f'={PAYLOAD};.*B(?!(?P=t):){rank}:'
        time_test = f'C(?P<t>{rank}):(?P<p>{DIGIT}*)' + first_difference(time_bridge, 'p', 'greater') + ';'
        time_block = f'(?={time_test}){row}'
        # Adjacent reduction: prefer right only when it strictly wins. Ties keep left.
        key_bridge = f':{time}={PAYLOAD};C'
        right_key = 'C(?P<k>' + DIGIT + '*)' + first_difference(
            key_bridge, 'k', 'greater' if self.rank_order == 'max' else 'smaller'
        ) + ':'
        date_bridge = f'={PAYLOAD};C(?P=s):'
        right_time = f'C(?P<s>{rank}):(?P<r>{DIGIT}*)' + first_difference(
            date_bridge, 'r', 'greater' if self.time_order == 'max' else 'smaller'
        ) + '='
        # k,s,r are capture groups 1,2,3; winners are capture groups 4 and 5.
        pair = f'(?:(?=(?:{right_key}|{right_time})){row}({row})|({row}){row})'
        return {
            'reject_newer_rank': term_block,
            'reject_later_different_rank': time_block,
            'remove_blockers': block,
            'reduce_pair': pair,
            'reduce_replacement': '${4}${5}',
            'payload_extract': '=(.*?);',
        }

    def formula(self, table_expression: str, output: str) -> str:
        if output not in {'payload', 'boolean'}:
            raise ValueError('output must be payload or boolean')
        result = table_expression.strip()
        if not result:
            raise ValueError('The table expression is empty.')
        p = self.patterns()
        for enabled, name in [
            (self.reject_newer_rank, 'reject_newer_rank'),
            (self.reject_later_different_rank, 'reject_later_different_rank'),
            (True, 'remove_blockers'),
        ]:
            if enabled:
                result = f'REGEXP_REPLACE({result},{quote(p[name])},"")'
        if output == 'boolean':
            return f'IF({result}<>"","TRUE","FALSE")'
        for _ in range(self.rounds):
            result = f'REGEXP_REPLACE({result},{quote(p["reduce_pair"])},{quote(p["reduce_replacement"])})'
        return f'REGEXP_EXTRACT({result},{quote(p["payload_extract"])})'


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', required=True, type=Path, help='One Element expression that constructs the validated table.')
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--projection', choices=['payload', 'boolean'], required=True)
    ap.add_argument('--rank-width', type=int, required=True)
    ap.add_argument('--time-width', type=int, required=True)
    ap.add_argument('--candidate-capacity', type=int, required=True)
    ap.add_argument('--rank-order', choices=['max', 'min'], required=True)
    ap.add_argument('--time-order', choices=['max', 'min'], required=True)
    ap.add_argument('--reject-newer-rank', action='store_true')
    ap.add_argument('--reject-later-different-rank', action='store_true')
    args = ap.parse_args()
    try:
        p = Pipeline(args.rank_width, args.time_width, args.candidate_capacity,
                     args.rank_order, args.time_order, args.reject_newer_rank,
                     args.reject_later_different_rank)
        result = p.formula(args.input.read_text(encoding='utf-8-sig'), args.projection)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result + '\n', encoding='utf-8')
        print(json.dumps({'configuration': asdict(p), 'reduction_rounds': p.rounds,
                          'formula_characters_excluding_final_newline': len(result),
                          'element_runtime_verified': False,
                          'note': 'Generated adaptation; lint and test in Evaluate AND Preview Export.'}, indent=2))
    except (ValueError, OSError) as exc:
        ap.error(str(exc))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
