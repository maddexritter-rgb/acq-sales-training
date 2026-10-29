#!/usr/bin/env python3
"""Normalize Trellus details or AssemblyAI JSON without network access."""
import argparse
import json
import math
import re
from pathlib import Path


def number(value):
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError('Invalid timestamp')
    return float(value)


def normalize(data):
    turns = []
    if 'provider_response' in data:
        data = data['provider_response']
    if 'turn_data' in data:
        raw = data['turn_data']
        data = {'sessionId': data.get('session_id'), 'turnData': {**raw, 'isCustomers': raw.get('is_customers')}}
    if 'turnData' in data:
        raw = data['turnData']
        fields = [raw.get(k, []) for k in ('starts', 'ends', 'texts', 'isCustomers')]
        if not fields[2] or len({len(x) for x in fields}) != 1:
            raise ValueError('Empty or mismatched Trellus turn arrays')
        kind, sid, mapped = 'trellus', data.get('sessionId'), 'provider_roles'
        for i, (start, end, text, customer) in enumerate(zip(*fields)):
            if type(customer) is not bool:
                raise ValueError('Invalid Trellus customer flag')
            turns.append(dict(turn_id=i+1, start=number(start), end=number(end),
                              speaker='customer' if customer else 'agent',
                              role='buyer' if customer else 'rep', text=text))
    elif data.get('utterances'):
        if data.get('status') not in (None, 'completed'):
            raise ValueError('ASR is not completed')
        kind, sid, mapped = 'assemblyai', data.get('id'), 'unconfirmed'
        for i, u in enumerate(data['utterances']):
            start, end = number(u.get('start')), number(u.get('end'))
            turns.append(dict(turn_id=i+1, start=None if start is None else start/1000,
                              end=None if end is None else end/1000, speaker=u.get('speaker'),
                              role='unknown', text=u.get('text'), confidence=u.get('confidence')))
    else:
        raise ValueError('Unsupported schema or no speaker turns; inspect source format')
    for t in turns:
        if not isinstance(t['text'], str) or not t['text'].strip():
            raise ValueError('Empty turn text')
        if t['start'] is not None and t['end'] is not None and t['end'] < t['start']:
            raise ValueError('Turn ends before it starts')
    return dict(source_id=sid, source_type=kind, timing_unit='seconds',
                role_mapping_status=mapped, observed_call_result='unknown',
                verified_deal_outcome='unknown', turns=turns)


def normalize_text(text, kind):
    def stamp(value):
        bits = value.replace(',', '.').split(':')
        if len(bits) not in (2, 3):
            raise ValueError('Invalid subtitle timestamp')
        nums = [float(x) for x in bits]
        if any(x < 0 or not math.isfinite(x) for x in nums) or nums[-1] >= 60 or nums[-2] >= 60:
            raise ValueError('Invalid subtitle timestamp')
        return sum(n * 60**i for i, n in enumerate(reversed(nums)))
    turns = []
    if kind in ('srt', 'vtt'):
        for block in re.split(r'\n\s*\n', text.replace('\r\n', '\n').strip()):
            lines = block.splitlines()
            timing = next((i for i, x in enumerate(lines) if '-->' in x), None)
            if timing is None:
                if kind == 'vtt' and (block.startswith('WEBVTT') or block.startswith(('NOTE', 'STYLE', 'REGION'))):
                    continue
                raise ValueError('Subtitle block missing timing')
            start, end = lines[timing].split('-->', 1)
            start, end = stamp(start.strip()), stamp(end.strip().split()[0])
            body = '\n'.join(lines[timing+1:]).strip()
            if not body or end < start:
                raise ValueError('Empty or reversed subtitle cue')
            turns.append(dict(turn_id=len(turns)+1, start=start, end=end, speaker=None, role='unknown', text=body))
    else:
        for line, body in enumerate(text.splitlines(), 1):
            if body.strip():
                turns.append(dict(turn_id=len(turns)+1, source_line=line, start=None, end=None, speaker=None, role='unknown', text=body))
    if not turns:
        raise ValueError('Empty transcript')
    return dict(source_id=None, source_type=kind, timing_unit='seconds', role_mapping_status='unconfirmed', observed_call_result='unknown', verified_deal_outcome='unknown', turns=turns)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path)
    p.add_argument('output', type=Path)
    args = p.parse_args()
    kind = args.input.suffix.lower().lstrip('.')
    raw = args.input.read_text(encoding='utf-8-sig')
    if kind == 'json':
        result = normalize(json.loads(raw))
    elif kind in ('txt', 'md', 'srt', 'vtt'):
        result = normalize_text(raw, kind)
    else:
        p.error('Supported extensions: json, txt, md, srt, vtt')
    with args.output.open('x') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Normalized {len(result['turns'])} turns; outcome remains unknown")


if __name__ == '__main__':
    main()
