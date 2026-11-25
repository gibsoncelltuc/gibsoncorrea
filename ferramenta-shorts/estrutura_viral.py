# ESTRUTURA VIRAL (ordem do Gibson 25/11, ESTRUTURA_VIRAL.md): confere o roteiro contra o "roteiro vencedor de Shorts".
#   python3 estrutura_viral.py <id>        -> lista do que falta; codigo 1 se reprovar (trava o render)
#   python3 estrutura_viral.py --todos     -> varredura de todos os roteiros (videos/*), tabela em VARREDURA_ESTRUTURA.md
import json, re, sys, os, glob, unicodedata
os.chdir(os.path.dirname(os.path.abspath(__file__)))
WPS = 2.5                      # palavras por segundo da voz (medido: 153 palavras = 60 s)
MIN_W, MAX_W, DURO_W = 75, 112, 125   # 30-45 s; limite duro 50 s
BLOCOS = ['gancho', 'promessa', 'prova', 'escalada', 'pagamento', 'loop']
TIPOS = {'perda', 'ganho', 'crenca', 'segredo'}
ENCHE = r'\b(tipo|sabe|entao|ne|ai|basicamente|na verdade|tipo assim)\b'
NUM = r'\d|\b(um|uma|dois|duas|tres|quatro|cinco|seis|sete|oito|nove|dez|onze|doze|vinte|trinta|cem|cento|mil|milhoes?|bilhao|bilhoes|metade|dobro|primeir\w*)\b'
CTA = r'comente|comentar|inscrev|curte|curtir|proximo video|link na'
def n_(t): return unicodedata.normalize('NFKD', str(t).lower()).encode('ascii', 'ignore').decode()
def frases(t): return [f.strip() for f in re.split(r'(?<=[.!?])\s+|:\s+(?=[A-ZÀ-Ú"])', t.strip()) if f.strip()]
def pal(t): return len(re.findall(r"[\wÀ-ú$%]+(?:[-'][\wÀ-ú]+)*", t))

def checar(id_):
    B = json.load(open(f'videos/{id_}/beats.json', encoding='utf-8')); bt = B.get('beats', [])
    falhas = []; avisos = []
    says = [b.get('say', '') for b in bt]
    if says and re.search(CTA, n_(says[-1])): avisos.append('ultima frase e\' chamada para comentar (vai sair: final agora e\' o LOOP)')
    corpo = [s for s in says if not re.search(CTA, n_(s))] if len(says) > 1 else says
    W = sum(pal(s) for s in corpo); seg = W / WPS
    if W > DURO_W: falhas.append(f'longo demais: {W} palavras (~{seg:.0f} s); maximo {MAX_W} (~45 s), ideal ate ~88 (35 s)')
    elif W > MAX_W: falhas.append(f'acima de 45 s: {W} palavras (~{seg:.0f} s); cortar para {MAX_W} ou menos')
    elif W < MIN_W: falhas.append(f'curto demais: {W} palavras (~{seg:.0f} s); minimo {MIN_W} (30 s)')
    longas = [(k, f) for k, s in enumerate(says) for f in frases(s) if pal(f) > 12]
    for k, f in longas[:6]: falhas.append(f'b{k}: frase com {pal(f)} palavras (max 12): "{f[:70]}"')
    if len(longas) > 6: falhas.append(f'... mais {len(longas) - 6} frase(s) com mais de 12 palavras')
    enc = [(k, m.group(0)) for k, s in enumerate(says) for m in re.finditer(ENCHE, n_(s))]
    for k, w in enc[:4]: falhas.append(f'b{k}: palavra de enchimento "{w}"')
    g = says[0] if says else ''
    if B.get('gancho_tipo') not in TIPOS: falhas.append('falta "gancho_tipo" (perda | ganho | crenca | segredo) no topo do beats.json')
    if pal(frases(g)[0] if frases(g) else '') > 12: falhas.append('gancho (1a frase) com mais de 12 palavras: nao cabe em 3 s')
    if re.search(r'\b(1\d{3}|20\d{2})\b|\bmil (seiscentos|setecentos|oitocentos|novecentos|e )|\bdois mil\b|\bem \w+ de\b', n_(frases(g)[0] if frases(g) else '')): falhas.append('gancho comeca com data (data vai para a prova)')
    if bt and not (bt[0].get('text') or bt[0].get('hud')): falhas.append('b0 sem texto na tela: gancho precisa de 3 camadas (imagem + TEXTO + frase)')
    bl = [b.get('bloco') for b in bt]
    faltam = [x for x in BLOCOS if x not in bl]
    if faltam: falhas.append('blocos faltando ("bloco" em cada cena): ' + ', '.join(faltam))
    else:
        ordem = [BLOCOS.index(x) for x in bl if x in BLOCOS]
        if ordem != sorted(ordem): falhas.append('blocos fora de ordem (gancho > promessa > prova > escalada > pagamento > loop)')
        if bl[0] != 'gancho': falhas.append('a 1a cena tem que ser o gancho')
        if bl[-1] != 'loop': falhas.append('a ultima cena tem que ser o loop')
        acum = 0; ok_prova = False
        for b in bt:
            if b.get('bloco') == 'prova' and re.search(NUM, n_(b.get('say', ''))) and acum / WPS <= 20: ok_prova = True
            acum += pal(b.get('say', ''))
        if not ok_prova: falhas.append('sem micro-pagamento (numero/nome/resultado) na prova antes dos 20 s')
        lp = next((b for b in reversed(bt) if b.get('bloco') == 'loop'), {})
        if not lp.get('loop_visual', True) is False and not lp.get('loop_visual'): avisos.append('loop: a ferramenta repete a imagem da 1a cena na ultima ("loop_visual": true automatico)')
        if not B.get('loop_frase_ok'): falhas.append('loop nao conferido: a ultima frase precisa emendar na primeira; depois de ler as duas em sequencia, ponha "loop_frase_ok": true')
        if not B.get('gancho_cumprido'): falhas.append('pagamento nao conferido: escreva em "gancho_cumprido" a frase do pagamento que entrega o que o gancho prometeu')
    return W, seg, falhas, avisos

IGN = re.compile(r'^(teste_|zz_|porco_piloto|sino_bench)|\.md$')
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--todos':
        ids = sorted(d for d in os.listdir('videos') if not IGN.search(d) and os.path.exists(f'videos/{d}/beats.json'))
        L = ['# VARREDURA — ESTRUTURA VIRAL (estrutura_viral.py --todos)', '', '| id | palavras | ~seg | frases >12 | falhas |', '|---|---|---|---|---|']
        ok = 0
        for id_ in ids:
            W, seg, F, A = checar(id_); ok += not F
            nl = sum(1 for f in F if 'palavras (max 12)' in f) + sum(int(re.search(r'mais (\d+)', f).group(1)) for f in F if f.startswith('... mais'))
            L.append(f'| {id_} | {W} | {seg:.0f} | {nl} | {len(F)}: ' + ' / '.join(f for f in F if 'palavras (max 12)' not in f and not f.startswith('...'))[:300] + ' |')
        L += ['', f'{ok}/{len(ids)} roteiros dentro da estrutura.']
        open('VARREDURA_ESTRUTURA.md', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L[-1:])); print('-> VARREDURA_ESTRUTURA.md')
        sys.exit(0)
    id_ = sys.argv[1]; W, seg, F, A = checar(id_)
    print(f'ESTRUTURA VIRAL {id_}: {W} palavras (~{seg:.0f} s)')
    for a in A: print('  aviso:', a)
    for f in F: print('  FALHA:', f)
    print('ESTRUTURA VIRAL OK' if not F else f'ESTRUTURA VIRAL REPROVADA ({len(F)} item(ns)) -> ESTRUTURA_VIRAL.md')
    sys.exit(1 if F else 0)
