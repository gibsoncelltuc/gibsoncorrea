#!/usr/bin/env python3
"""VERIFICADOR DO MODO DE ACAO DEFINITIVO (ordem do Gibson 21/11, MODO_DE_ACAO_DEFINITIVO.md). Aplica as regras do documento a cada cena:
 R2.1  toda frase tem >=1 verbo de acao VISUAL (frase so' de comentario e' proibida)            -> FALHA
 R4    no maximo 4 personagens principais em cena fechada                                       -> FALHA
 R5    momento de impacto (batalha/multidao/explosao) em plano ABERTO                           -> FALHA
 R4.1  negacao nao gera acao (cena com 'ninguem atirou' nao pode ter tiro)                      -> FALHA
 R4.7  uma acao forte por frase (3+ acoes fortes em uma cena)                                   -> AVISO
 R4.6  objeto heroi com close no comeco e no fim                                                -> AVISO
 R4.3  verbo importante no fim da frase: objeto/pose precisa comecar antes                      -> AVISO
uso: python3 verificar_modo_acao.py <id>  | --todos   (exit 1 se houver FALHA)  -> stories/<id>/modo_acao.md"""
import json, re, sys, os, unicodedata
os.chdir(os.path.dirname(os.path.abspath(__file__)))
nrm = lambda t: unicodedata.normalize('NFKD', t.lower()).encode('ascii', 'ignore').decode()
FORTES = re.compile(r'^(atirou|atiraram|disparou|dispararam|explodiu|explodiram|bombardeou|bombardearam|invadiu|invadiram|desembarcou|desembarcaram|marchou|marcharam|atacou|atacaram|correu|correram|fugiu|fugiram|pulou|pularam|caiu|cairam|socou|empurrou|empurraram|brigou|brigaram|abracou|abracaram|derrubou|jogou|jogaram|lancou|lancaram|construiu|montou|cavou|escalou|escalaram|capturou|prendeu|rendeu|renderam|venceu|derrotou|matou|morreu|voou|decolou|nadou|cavalgou)$')
def carregar(sid):
    B = json.load(open(f'videos/{sid}/beats.json'))
    sp = open(f'stories/{sid}/spec.js', encoding='utf-8').read() if os.path.exists(f'stories/{sid}/spec.js') else ''
    f3 = open(f'stories/{sid}/folha3_acao.md', encoding='utf-8').read() if os.path.exists(f'stories/{sid}/folha3_acao.md') else ''
    return B, sp, f3
def verificar(sid):
    B, sp, f3 = carregar(sid); beats = B['beats']; falhas = []; avisos = []
    pecas = {m.group(1): m.group(0) for m in re.finditer(r"S\('(b\d+)(?:_\d+)?', .*", sp)}
    acoes3 = {}
    for m in re.finditer(r'## Cena (b\d+) .*?(?=\n## Cena b\d+ |\Z)', f3, re.S): acoes3[m.group(1)] = len(re.findall(r'\| \d+ \| ', m.group(0)))
    for i, b in enumerate(beats):
        k = f'b{i}'; say = b['say']; n = nrm(say); pal = [nrm(w) for w in re.findall(r'[A-Za-zÀ-ú]+', say)]
        # R2.1
        if acoes3.get(k, 0) == 0 and not b.get('acao') and not b.get('batalha') and not b.get('crowd') and not b.get('voa') and not b.get('interacao'):
            falhas.append((k, 'R2.1 frase sem nenhuma acao visual catalogada (so comentario)'))
        # R4
        shot = b.get('shot', 'two'); wide = shot in ('wide', 'crowd', 'reveal', 'orbit', 'aereo', 'track')
        if not wide and len(b.get('who', [])) > 4: falhas.append((k, f'R4 {len(b["who"])} personagens principais em cena fechada (max 4)'))
        # R5
        if b.get('batalha') and shot not in ('wide', 'crowd', 'reveal', 'orbit', 'aereo', 'track'): falhas.append((k, f'R5 impacto/batalha em plano fechado ({shot}): use crowd/reveal/orbit'))
        # R4.1 negacao x tiro
        if re.search(r'ninguem (deu|atirou|disparou)|sem (dar |disparar |atirar )|nenhum tiro|nao (atiraram|dispararam|houve tiro)', n) and re.search(r"k: ['\"](burst|gun)['\"]", pecas.get(k, '')) and not b.get('tiros') is False:
            falhas.append((k, 'R4.1 narracao NEGA o tiro mas a cena tem clarao de tiro'))
        # R4.7
        fortes = {p for j, p in enumerate(pal) if FORTES.match(p) and not (set(pal[max(0, j - 3):j]) & {'nao', 'nem', 'nunca', 'sem', 'ninguem', 'nenhum'})}
        if len(fortes) >= 3: avisos.append((k, f'R4.7 {len(fortes)} acoes fortes na mesma frase ({", ".join(sorted(fortes))}): ideal dividir em cenas'))
        # R4.3 verbo no fim
        if len(pal) >= 8:
            ult = pal[-4:]
            if any(FORTES.match(p) for p in ult) and not (b.get('props') or b.get('animals') or b.get('crowd') or b.get('voa') or b.get('acao') or b.get('batalha')):
                avisos.append((k, 'R4.3 verbo forte no fim da frase e a cena nao tem objeto/pose antecipando'))
    h = B.get('heroi')
    if h and len(beats) >= 4:
        ini = any(re.search(re.escape(h.split('/')[-1]), json.dumps(b.get('props', []))) or b.get('detalhe') for b in beats[:3]); fim = any(re.search(re.escape(h.split('/')[-1]), json.dumps(b.get('props', []))) for b in beats[-3:])
        if not ini: avisos.append(('geral', f'R4.6 objeto heroi ({h}) sem aparecer no comeco'))
        if not fim: avisos.append(('geral', f'R4.6 objeto heroi ({h}) sem aparecer no fim'))
    md = [f'# MODO DE ACAO DEFINITIVO: {sid}', f'FALHAS: {len(falhas)}  |  AVISOS: {len(avisos)}', ''] + [f'- **FALHA** {k}: {t}' for k, t in falhas] + [f'- aviso {k}: {t}' for k, t in avisos]
    os.makedirs(f'stories/{sid}', exist_ok=True); open(f'stories/{sid}/modo_acao.md', 'w', encoding='utf-8').write('\n'.join(md) + '\n')
    return falhas, avisos
if __name__ == '__main__':
    if sys.argv[1] == '--todos':
        ids = []
        for f in ('queue.txt', 'fila_sessao_A.txt', 'fila_sessao_B.txt'):
            ids += [l.split()[0] for l in open(f) if l.strip() and not l.startswith('#')]
        tf = ta = 0
        for i in dict.fromkeys(ids):
            if not (os.path.exists(f'stories/{i}/spec.js') and os.path.exists(f'videos/{i}/beats.json')): continue
            fl, av = verificar(i); tf += len(fl); ta += len(av)
            if fl: print(f'{i}: {len(fl)} falha(s): ' + ' | '.join(f'{k} {t[:60]}' for k, t in fl[:3]))
        print(f'TOTAL: {tf} falhas, {ta} avisos')
    else:
        fl, av = verificar(sys.argv[1]); print(f'{sys.argv[1]}: {len(fl)} falhas, {len(av)} avisos')
        for k, t in fl: print('  FALHA', k, t)
        for k, t in av: print('  aviso', k, t)
        sys.exit(1 if fl else 0)
