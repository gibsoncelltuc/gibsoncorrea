#!/usr/bin/env python3
# IMPRESSAO DIGITAL DE CADA CENA (24/11, pedido do Gibson: "refazer so' o trecho com defeito e remontar, nao o video inteiro").
# Imprime: "global <hash>" (motor de desenho web/*.js, voz/tempos, cabecalho do spec: figurinos, assets, A[]...)
#          "bN <hash>" para cada cena (a linha S('bN', ...) do spec.js + o ajuste de camera dela no fit.js).
# O make_video compara com a impressao guardada no ultimo render: mudou so' cena -> refaz so' os trechos dela; mudou o global -> video inteiro.
import sys, re, hashlib, glob, json, os
i = sys.argv[1]; D = f'stories/{i}'
h = lambda s: hashlib.md5(s.encode('utf-8', 'ignore')).hexdigest()[:10]
spec = open(f'{D}/spec.js', encoding='utf-8').read().split('\n')
fit = {}
try: fit = json.loads(re.search(r'SPEC\.fit = (\{.*?\});', open(f'{D}/fit.js', encoding='utf-8').read()).group(1))
except Exception: pass
web = ''.join(open(f, encoding='utf-8', errors='ignore').read() for f in sorted(glob.glob('web/*.js') + glob.glob('web/sets/*.js')) if not f.endswith('story.js'))
web = re.sub(r'/\*ADITIVO\*/.*?/\*FIM ADITIVO\*/', '', web, flags=re.S)   # 25/11 codigo ADITIVO: ramo novo que so' roda com opcao NOVA (ex.: hat 'laurel'); nao muda nenhum quadro ja renderizado -> nao derruba os trechos dos outros videos. So' marque assim codigo que video antigo nunca alcanca.
voz = open(f'{D}/work/phrases.json', encoding='utf-8').read() if os.path.exists(f'{D}/work/phrases.json') else ''
glob_ = []; cenas = {}
for l in spec:
    m = re.match(r"\s*(?:\{ \.\.\.)*(?:\{ \.\.\.)?\s*S\('(b\d+)'", l)
    if m: cenas.setdefault(m.group(1), []).append(l); continue
    if l.startswith('// FOLHA3'): continue   # carimbo da folha 3 muda a cada cena: nao entra no global
    glob_.append(l)
print('global', h(web + voz + '\n'.join(glob_)))
for k, ls in cenas.items():
    print(k, h('\n'.join(ls) + json.dumps({kk: vv for kk, vv in fit.items() if re.match(rf'^{k}(\D|$)', kk)}, sort_keys=True)))
