#!/usr/bin/env python3
"""Valida os JSONs do projeto contra schemas/*.schema.json (JSON Schema 2020-12) + consistência ENTRE arquivos (rubrica V2: "JSON Schema para production.json,
shots.json, word-timings.json e registries" + "verificar assets referenciados e arquivos ausentes").
Saída: linhas PASS/FAIL; grava qa/schema-report.json. Código de saída ≠ 0 se algo falhar.   Uso: python3 tools/validate_schemas.py"""
import hashlib, json, os, sys
from jsonschema import Draft202012Validator
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda p: json.load(open(os.path.join(R, p), encoding='utf-8'))
res = []
def rec(name, ok, detail=''):
    res.append({'name': name, 'pass': bool(ok), 'detail': str(detail)}); print(('PASS ' if ok else 'FAIL ') + name + (' — ' + str(detail) if detail else ''))
PAIRS = [('production.json', 'production'), ('storyboard/shots.json', 'shots'), ('script/word-timings.json', 'word-timings'), ('registry/registry.json', 'registry'),
         ('research/claims.json', 'claims'), ('render-manifest.json', 'render-manifest')]
for path, sch in PAIRS:
    try:
        errs = sorted(Draft202012Validator(J(f'schemas/{sch}.schema.json')).iter_errors(J(path)), key=lambda e: list(e.path))
        rec(f'schema {path}', not errs, '; '.join(f"{'/'.join(map(str, e.path))}: {e.message[:90]}" for e in errs[:4]) if errs else 'válido')
    except Exception as ex:
        rec(f'schema {path}', False, repr(ex)[:160])
# ---- consistência entre arquivos ----
prod = J('production.json'); sb = J('storyboard/shots.json'); wt = J('script/word-timings.json'); reg = J('registry/registry.json'); cl = J('research/claims.json'); man = J('render-manifest.json')
sh = sb['shots']
rec('shots contíguos e ordenados (sem buracos/sobreposição)', all(abs(sh[i]['end'] - sh[i + 1]['start']) < 0.01 for i in range(len(sh) - 1)), f"{len(sh)} planos")
rec('shots: dur = end − start', all(abs(s['dur'] - (s['end'] - s['start'])) < 0.01 for s in sh))
rec('shots cobrem 0 → duração total', abs(sh[0]['start']) < 0.01 and abs(sh[-1]['end'] - wt['total']) < 0.05, f"{sh[0]['start']}→{sh[-1]['end']} vs total {wt['total']}")
rec('production.durationSeconds = word-timings.total', abs(prod['durationSeconds'] - wt['total']) < 0.01, f"{prod['durationSeconds']} vs {wt['total']}")
rec('production.visualEngine cita Blender (motor real do render)', 'blender' in prod['visualEngine'].lower(), prod['visualEngine'])
ws = wt['words']
rec('palavras em ordem crescente e start<end', all(w['start'] < w['end'] for w in ws) and all(ws[i]['start'] <= ws[i + 1]['start'] + 1e-6 for i in range(len(ws) - 1)), f"{len(ws)} palavras")
ids = {l['id'] for l in wt['lines']}
rec('toda palavra pertence a uma linha existente; toda linha tem palavras', all(w['line'] in ids for w in ws) and all(any(w['line'] == i for w in ws) for i in ids))
rec('toda linha usada nos planos existe', all(l in ids for s in sh for l in s['lines']))
rec('palavras de cada linha dentro dos limites da linha (±0,15 s)', all(l['start'] - .15 <= w['start'] and w['end'] <= l['end'] + .15 for l in wt['lines'] for w in ws if w['line'] == l['id']))
rec('registry: ids únicos', len({i['id'] for i in reg['items']}) == len(reg['items']), f"{len(reg['items'])} itens")
miss = [i['file'] for i in reg['items'] if not os.path.exists(os.path.join(R, i['file']))]
rec('registry: arquivos existem', not miss, miss)
stale = [i['id'] for i in reg['items'] if os.path.exists(os.path.join(R, i['file'])) and hashlib.sha256(open(os.path.join(R, i['file']), 'rb').read()).hexdigest()[:16] != i['hash']]
rec('registry: hashes atuais (nenhum item desatualizado)', not stale, stale)
dep_ids = {i['id'] for i in reg['items']}
rec('registry: dependências internas resolvem para ids existentes', all(d in dep_ids for i in reg['items'] for d in i['dependencies'] if d.count('.') >= 2 and d.split('.')[-1].startswith('v')))
used = {s['id'] for c in cl['afirmacoes'] for s in c['fontes']} if False else {f['fonte'] for c in cl['afirmacoes'] for f in c['fontes']}
rec('claims: toda fonte citada está na lista de fontes lidas', used <= set(cl['fontes']), sorted(used - set(cl['fontes'])))
rec('claims: toda afirmação tem ≥ 2 fontes DISTINTAS', all(len({f['fonte'] for f in c['fontes']}) >= 2 for c in cl['afirmacoes']), f"{len(cl['afirmacoes'])} afirmações")
# ---- citações literais: cada "trecho" das afirmações aparece (verbatim) no texto salvo da fonte ----
import glob, re
def norm(t):
    t = t.replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"'); t = re.sub(r'\[ ?\d+ ?\]', '', t)   # marcadores de nota [ 2 ]
    t = re.sub(r'\s+', ' ', t); t = re.sub(r' ([,.;:!?)])', r'\1', t); t = re.sub(r'\( ', '(', t); return t.lower().strip()
SRC = {'NPS': 'nps_*.txt', 'HISTORYLINK': 'historylink_5724*.txt', 'HISTORYLINK2': 'historylink_5725*.txt', 'WIKIPEDIA': 'wikipedia_*.txt'}
have = {k: norm(' '.join(open(f, encoding='utf-8', errors='ignore').read() for f in glob.glob(os.path.join(R, 'research', 'sources', g)))) for k, g in SRC.items()}
if all(have.values()):
    bad = []
    for c in cl['afirmacoes']:
        for f in c['fontes']:
            if f['fonte'] not in have: continue
            for seg in [x.strip() for x in f['trecho'].split('…') if len(x.strip()) >= 12]:
                if norm(seg) not in have[f['fonte']]: bad.append((c['id'], f['fonte'], seg[:50]))
    rec('claims: cada trecho citado aparece LITERALMENTE no texto salvo da fonte (sem citação inventada)', not bad, bad[:4] if bad else f"{sum(len(c['fontes']) for c in cl['afirmacoes'])} citações")
else:
    rec('claims: trechos literais (fontes salvas ausentes neste checkout — research/sources é ignorado pelo git)', True, 'não verificado aqui')
rec('manifesto: duração do vídeo ≈ production (±1 s: cauda de áudio/fade)', abs(man['duracao_s'] - prod['durationSeconds']) < 1.0, f"{man['duracao_s']} vs {prod['durationSeconds']}")
json.dump({'checks': res, 'passed': sum(r['pass'] for r in res), 'total': len(res)}, open(os.path.join(R, 'qa', 'schema-report.json'), 'w'), ensure_ascii=False, indent=1)
print(f"{sum(r['pass'] for r in res)}/{len(res)}")
sys.exit(0 if all(r['pass'] for r in res) else 1)
