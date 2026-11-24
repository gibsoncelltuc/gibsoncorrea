#!/usr/bin/env python3
# COERENCIA DO ROTEIRO (24/11, causa raiz levantada nos videos refeitos hoje). Roda dentro do verificar_folhas.py (trava o render).
# Cada regra corresponde a um defeito real que passou pelas 4 folhas:
#  R1 LUGAR: "regiao" (predios do fundo) diferente do lugar da historia (Lagosta em Pernambuco com predios franceses).
#  R2 REGIAO INVALIDA: valor que a ferramenta nao conhece cai no padrao europeu sem avisar.
#  R3 LADOS IGUAIS: dois grupos que se enfrentam com a mesma cor de farda (Bolos: mexicanos e franceses iguais).
#  R4 GANCHO HESITANTE: 1a frase com data ou ressalva ("Segundo uma versao", "Era 1925...") derruba a retencao nos 5 s.
# Excecao consciente no topo do beats.json: "coerencia_ok": ["R1", ...]
import json, re, sys, unicodedata
i = sys.argv[1]; B = json.load(open(f'videos/{i}/beats.json')); BT = B['beats']; ok = set(B.get('coerencia_ok', []))
n = lambda s: unicodedata.normalize('NFD', str(s).lower()).encode('ascii', 'ignore').decode()
src = open('mkvideo.py', encoding='utf-8').read()
REG = re.findall(r"\('(\w+)', r'([^']+)'\)", src[src.index('_REG_PAIS = '):src.index('_REG_BASE')])
VALIDAS = {r for r, _ in REG} | {'nenhuma', 'generica'}
erros = []
reg = B.get('regiao')
if reg and reg not in VALIDAS and 'R2' not in ok: erros.append(f'R2 regiao "{reg}" nao existe (validas: {", ".join(sorted(VALIDAS))}); Brasil/America Latina = colonial')
# lugar da historia: o mapa do roteiro manda; senao a 1a cena que cita lugar
lugar = (next((n(b['mapa']) for b in BT if b.get('mapa')), None) or n(' '.join(b['say'] for b in BT[:3]))).replace('sao francisco', 'california')
det = next((r for r, rx in REG if re.search(rx, lugar)), None)
if reg and reg not in ('nenhuma', 'generica') and det and reg != det and not (det == 'europa' and reg in ('franca', 'holanda')) and not ({det, reg} == {'oriente', 'classico'}) and 'R1' not in ok:
    erros.append(f'R1 a historia se passa em "{lugar[:40]}" (regiao {det}) mas o roteiro pede predios "{reg}": troque "regiao" para "{det}"')
# lados que se enfrentam
O = B.get('outfits', {})
for k, b in enumerate(BT):
    g = [x for x in ((b.get('crowd') or {}).get('outfits') or []) if x in O]
    lados = {}
    for x in g: lados.setdefault(str(O[x].get('jacket', '')).lower(), []).append(x)
    if b.get('batalha') and 'R3' not in ok:
        for cor, xs in lados.items():
            if len(xs) >= 2 and cor: erros.append(f'R3 b{k}: {", ".join(xs)} se enfrentam com a mesma farda ({cor}): de a cada lado uma cor')
# R5: farda FINAL (depois da farda automatica da epoca, lida do spec.js): dois exercitos diferentes na mesma cena com a mesma cor (Uisque: canadenses e dinamarqueses camuflados iguais)
import os
if os.path.exists(f'stories/{i}/spec.js') and 'R5' not in ok:
    sp = open(f'stories/{i}/spec.js', encoding='utf-8').read()
    FJ = {k: (j, 'rifle: true' in body) for k, j, body in re.findall(r'(\w+): \(v = 0, e = \{\}\) => \(\{ _id: "\w+", jacket: "(#[0-9a-fA-F]+)"([^)]{0,400})', sp)}
    vistos = set()
    for k, b in enumerate(BT):
        ks = {str(w).split(':')[0] for w in (b.get('who') or [])} | set((b.get('crowd') or {}).get('outfits') or [])
        ms = [x for x in ks if x in FJ and FJ[x][1]]
        for a_ in ms:
            for b_ in ms:
                if a_ < b_ and FJ[a_][0].lower() == FJ[b_][0].lower() and (a_, b_) not in vistos and not any(a_ in g_ and b_ in g_ for g_ in B.get('aliados', [])):   # aliados do mesmo lado ("aliados": [["USA", "CAN"]]) podem ter a mesma farda
                    vistos.add((a_, b_)); erros.append(f'R5 b{k}: {a_} e {b_} saem com a MESMA farda ({FJ[a_][0]}) depois da farda automatica da epoca: ponha "uniforme_fixo": true com cor propria em cada lado')
# R6: a folha 3 catalogou BATALHA numa frase sem luta (Lagosta: "barcos franceses pescavam" virou tropa atirando)
if os.path.exists(f'stories/{i}/folha3_acao.md') and 'R6' not in ok:
    f3 = open(f'stories/{i}/folha3_acao.md', encoding='utf-8').read()
    for m in re.finditer(r'^## Cena b(\d+) .*?\n> "(.*?)"(.*?)(?=^## Cena|\Z)', f3, re.S | re.M):
        if int(m.group(1)) >= len(BT): continue   # cena da chamada final (nao esta no roteiro)
        _b6 = BT[int(m.group(1))]; _arm = any(O.get(str(w).split(':')[0], {}).get('rifle') for w in (_b6.get('who') or []) + ((_b6.get('crowd') or {}).get('outfits') or []))
        _tiro = _b6.get('tiros') is not False and (_arm or re.search(r'atir|tiro|dispar|fuzil|bala', n(m.group(2))))   # so' vira tiroteio de verdade com arma em cena ou palavra de tiro
        if '| BATALHA |' in m.group(3) and _tiro and not _b6.get('batalha') and not re.search(r'guerra|batalh|lut|atac|atir|tiro|bomb|combat|invad|cerc|ataque|canh|soldad|tropa|exercit|confront|briga|brigar', n(m.group(2))):
            erros.append(f'R6 b{m.group(1)}: a ferramenta pos BATALHA (tropa atirando) numa frase sem luta: ponha "batalha": false, "tiros": false na cena')
# R7: cenario "palace" e' PRAIA de areia (navio em cima da areia): so' com praia/litoral/palacio na historia
for k, b in enumerate(BT):
    if b.get('set') == 'palace' and not b.get('interior') and 'R7' not in ok and not re.search(r'praia|areia|litoral|palacio|costa', n(b.get('say', ''))):
        erros.append(f'R7 b{k}: cenario "palace" desenha uma PRAIA de areia; a frase nao fala de praia: use harbor (cais), countryside ou interior')
# gancho
s0 = n(BT[0]['say']) if BT else ''
if re.match(r'(segundo|dizem|conta-se|contam|reza a lenda|era (mil|o ano)|em (mil|\d{3,4})|no ano de)', s0) and 'R4' not in ok:
    erros.append('R4 gancho comeca com data ou ressalva ("' + BT[0]['say'][:40] + '..."): abra com o fato mais surpreendente, sem data')
if erros: print('COERENCIA:'); [print(' -', e) for e in erros]; sys.exit(1)
print('COERENCIA OK (lugar, regiao, fardas dos lados, gancho)')
