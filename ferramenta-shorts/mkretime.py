#!/usr/bin/env python3
"""usage: python3 mkretime.py <story_pt>   (needs stories/<story_pt>/retime_from = source story id and a script.txt with the SAME sentence/clause structure)
Aligns source-language and new-language narration (sentence -> clause level) and writes stories/<story_pt>/retime.js + retime.json (frame anchors EN->PT)."""
import json, sys, os, re
pt = sys.argv[1]; src = open(f'stories/{pt}/retime_from').read().strip(); lang = (open(f'stories/{pt}/retime_lang').read().strip() if os.path.exists(f'stories/{pt}/retime_lang') else 'pt')
def load(story):
    one = open(f'stories/{story}/script_one.txt').read().split()
    W = json.load(open(f'stories/{story}/work/words.json')); P = json.load(open(f'stories/{story}/work/phrases.json'))
    if len(one) != len(W): raise SystemExit(f'{story}: {len(one)} script tokens vs {len(W)} timed words')
    sents, clauses, cc = [], [], []
    for i, t in enumerate(one):
        cc.append(i)
        if t[-1] in ',;:': clauses.append(cc); cc = []
        if t[-1] in '.!?': clauses.append(cc); cc = []; sents.append(clauses); clauses = []
    if cc: clauses.append(cc)
    if clauses: sents.append(clauses)
    return one, W, sents, int(P['frames30'])
oe, We, Se, Te = load(src); op, Wp, Sp, Tp = load(pt)
if len(Se) != len(Sp): raise SystemExit(f'sentence count differs: {src} has {len(Se)}, {pt} has {len(Sp)} -- keep the same sentence structure')
fr = lambda t: int(round(t * 30))
A = [(0, 0)]; clause_level = 0
for a, b in zip(Se, Sp):
    pairs = list(zip(a, b)) if len(a) == len(b) else [(sum(a, []), sum(b, []))]
    clause_level += len(a) == len(b)
    for ca, cb in pairs:
        A.append((fr(We[ca[0]]['s']), fr(Wp[cb[0]]['s']))); A.append((fr(We[ca[-1]]['e']), fr(Wp[cb[-1]]['e'])))
A.append((Te, Tp)); A.sort(); out = []; mx = -1
for e, p in A:
    p = max(p, mx); mx = p
    if out and out[-1][0] == e: out[-1] = [e, p]
    else: out.append([e, p])
i18n = {}
if os.path.exists(f'stories/i18n_{lang}.json'): i18n = json.load(open(f'stories/i18n_{lang}.json'))
json.dump({'anchors': out, 'enTotal': Te, 'ptTotal': Tp}, open(f'stories/{pt}/retime.json', 'w'))
open(f'stories/{pt}/retime.js', 'w').write('const RETIME = ' + json.dumps({'anchors': out, 'enTotal': Te, 'ptTotal': Tp, 'i18n': i18n}, ensure_ascii=False) + ';\n')
print(f'retime {src} -> {pt}: {len(Se)} sentences ({clause_level} aligned by clause), {len(out)} anchors, {Te} -> {Tp} frames')
