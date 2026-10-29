#!/usr/bin/env python3
"""Offline lexical retrieval of bundled coaching cards; results are candidates, not diagnoses."""
import argparse, collections, json, math, re
from pathlib import Path
STOP=set('a an and are as at be by for from has in is it of on or that the their this to was were with'.split())
def tokens(text):
    return [w for w in re.findall(r'[a-z0-9]+', text.lower()) if w not in STOP]
def rank(cards, query, module=None, limit=5):
    candidates=[c for c in cards if module is None or c['module']==module]
    docs=[tokens(' '.join([c['title']]*3+[c['trigger']]*2+[c['action'],c['branches'],c['do_not_apply']])) for c in candidates]
    if not docs: return []
    average=sum(map(len,docs))/len(docs)
    df=collections.Counter(w for d in docs for w in set(d)); scored=[]
    for card,doc in zip(candidates,docs):
        tf=collections.Counter(doc);score=0
        for word in set(tokens(query)):
            f=tf[word]
            if f:
                idf=math.log(1+(len(docs)-df[word]+.5)/(df[word]+.5))
                score+=idf*f*2.2/(f+1.2*(.25+.75*len(doc)/average))
        if score:scored.append((score,card))
    return [dict(card,retrieval_score=round(score,4)) for score,card in sorted(scored,key=lambda x:(-x[0],x[1]['id']))[:limit]]
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('query',nargs='?',default='');p.add_argument('--module');p.add_argument('--limit',type=int,default=5)
    p.add_argument('--id',action='append',default=[]);p.add_argument('--profile',type=Path)
    args=p.parse_args();base=Path(__file__).resolve().parents[1]
    if args.profile: profile=args.profile
    else:
        profiles=list((base/'brand').glob('*/library/cards.json'))
        if len(profiles)!=1:p.error('Select a profile with --profile /path/to/brand/profile')
        profile=profiles[0].parents[1]
    cards=json.loads((profile/'library/cards.json').read_text())
    if args.id:
        missing=set(args.id)-{c['id'] for c in cards}
        if missing:p.error('Unknown card IDs: '+', '.join(sorted(missing)))
        result=[c for c in cards if c['id'] in args.id]
    else:
        if not args.query.strip():p.error('Supply a query or --id')
        if args.limit<1 or args.limit>20:p.error('--limit must be between 1 and 20')
        if args.module and args.module not in {c['module'] for c in cards}:p.error('Unknown module')
        result=rank(cards,args.query,args.module,args.limit)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
