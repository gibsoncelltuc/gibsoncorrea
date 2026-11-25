# ENCENACAO ESCRITA (25/11, Gibson: "a ferramenta tem que entender o contexto de cada frase... solucao definitiva").
# A ferramenta (codigo) nao entende frase: le palavra por palavra. Quem ENTENDE e' a IA que escreve o roteiro.
# Por isso cada frase do beats.json leva a LEITURA da IA, escrita, e a ferramenta so' EXECUTA:
#
#   "encena": {
#     "sentido": "afirmativa" | "negativa" | "hipotese" | "figurada" | "fato",
#     "passos": [
#        {"quem": 0, "faz": "anda_ate", "alvo": "kit/bathtub", "na": "entrou"},
#        {"quem": 0, "faz": "entra_em", "alvo": "kit/bathtub", "na": "entrou"},
#        {"alvo": "kit/bathtub", "faz": "transborda", "na": "transbordou"}
#     ]
#   }
#
# sentido: afirmativa = aconteceu de verdade (tiro, explosao, briga aparecem); negativa ("nenhum tiro", "nunca veio"),
#          hipotese ("quase", "ameacou", "se tivesse"), figurada ("guerra de precos", "bateu recorde") = NADA de tiro/explosao/batalha;
#          fato = frase sem acao fisica (data, numero, explicacao) -> a cena mostra o objeto/lugar/personagens citados.
# passos: o que a TELA mostra, em ordem, preso na palavra "na" da narracao. Vocabulario em VOCAB (abaixo).
# Passo com verbo fora do VOCAB = FALTA (trava o render): a correcao e' CONSTRUIR a animacao na ferramenta, nunca pular.
import re, unicodedata

VOCAB = {   # faz -> (descricao tecnica para a folha 3, como a ferramenta executa)
    'anda_ate': ('caminha ate o objeto/lugar (entra andando pela lateral e para ao lado do alvo)', 'move'),
    'entra_em': ('entra DENTRO do objeto e senta (o objeto fica em volta da cintura, a fisica nao empurra para fora)', 'senta_dentro'),
    'transborda': ('o liquido de dentro do objeto transborda e escorre: respingos azuis em volta da borda + som de agua', 'splash'),
    'senta': ('senta no chao/banco', 'acao'), 'dorme': ('deita e dorme', 'acao'), 'ajoelha': ('ajoelha', 'acao'),
    'tomba': ('cai no chao', 'acao'), 'morre': ('cai e fica imovel', 'acao'), 'pula': ('pula', 'acao'), 'corre': ('corre', 'acao'),
    'golpe': ('da um golpe/soco no alvo', 'acao'), 'empurra': ('empurra o alvo', 'acao'), 'atira': ('atira com a arma (clarao na boca do cano + som)', 'acao'),
    'grita': ('grita com os bracos para cima', 'acao'), 'vence': ('comemora a vitoria', 'acao'), 'fala': ('fala apontando', 'acao'), 'olha': ('olha/aponta para o alvo', 'acao'),
    'pensa': ('mao no queixo, pensando', 'acao'), 'perde': ('mao na testa (derrota)', 'acao'), 'rende': ('maos para cima (rendicao)', 'acao'),
    'pega': ('pega/levanta o objeto', 'acao'), 'mistura': ('mexe a mistura', 'acao'), 'cai': ('deixa cair/joga o objeto', 'acao'),
    'constroi': ('martela/constroi', 'acao'), 'escreve': ('escreve no papel', 'acao'), 'entrega': ('entrega o objeto ao alvo', 'acao'),
    'chega': ('chega na cena', 'acao'), 'desaba': ('o objeto desaba', 'acao'),
    'mostra': ('a camera mostra o objeto/lugar citado (sem acao de personagem)', 'nada'),
}
def _motor():   # todas as acoes que o motor (mkvideo.py) ja executa, lidas do proprio codigo
    import os
    try: src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mkvideo.py'), encoding='utf-8').read()
    except Exception: return set()
    t = set(re.findall(r"tipo_ == '([a-z_]+)'", src)) | set(re.findall(r"'(x_[a-z]+)': \(", src))
    for g in re.findall(r"tipo_ in \(([^)]*)\)", src): t |= set(re.findall(r"'([a-z_]+)'", g))
    t |= set(re.findall(r"'([a-z_]+)': '(?:punch|push|up|lift|point|think|facepalm|plead|stir|throw|hammer|write)'", src))
    return t
for _t in _motor():
    if _t not in VOCAB: VOCAB[_t] = (('acao do motor: ' + _t.replace('x_', '')), 'acao')
SENTIDOS = ('afirmativa', 'negativa', 'hipotese', 'figurada', 'fato')
CONTEINER = r'bathtub|banheira|tina|barril|barrel|barco|boat|caixa|crate|carro|car|cama|bed|poco|well|panela|caldeir'

def _n(t): return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', str(t).lower()).encode('ascii', 'ignore').decode())

def aplicar(B, slots, ZS):
    """Traduz "encena" de cada beat para os campos que o motor ja executa. Chamado no comeco do mkvideo."""
    for b in B['beats']:
        e = b.get('encena')
        if not isinstance(e, dict): continue
        s = e.get('sentido')
        if s in ('negativa', 'hipotese', 'figurada'):   # nada de violencia na tela, o roteiro decidiu
            b['batalha'] = False; b['tiros'] = False; b['_sentido_lido'] = s
        acoes = [a for a in (b.get('acoes') or []) if not a.get('_de_encena')]
        who = b.get('who') or []
        for p in e.get('passos') or []:
            faz = p.get('faz'); na = p.get('na') or ''; q = int(p.get('quem', 0) or 0); alvo = p.get('alvo')
            if faz == 'anda_ate': b['_anda_quem'] = q
            elif faz == 'entra_em':
                if who:
                    x0 = slots(len(who))[min(q, len(who) - 1)]
                    pr = [x for x in (b.get('props') or []) if not (isinstance(x, list) and str(x[0]) == str(alvo))]
                    b['props'] = pr + [[alvo, x0, round(ZS[min(q, len(ZS) - 1)] + 0.35, 2), 1.15, {'fixo': True, 'nocol': True}]]
                acoes.append({'palavra': na, 'tipo': 'senta', 'quem': q, '_de_encena': True})
                for k_ in ('cx', 'cz', 'd0', 'd1', '_auto_vis'): b.pop(k_, None)
            elif faz == 'transborda': b.setdefault('_splash_na', []).append([na, alvo])
            elif faz in VOCAB and VOCAB[faz][1] == 'acao' and p.get('forcar'):   # so' forca quando a tela ainda nao faz (a conferencia mao dupla marca 'forcar')
                a = {'palavra': na, 'tipo': faz, 'quem': q, '_de_encena': True}
                if 'alvo_quem' in p: a['alvo'] = p['alvo_quem']
                acoes.append(a)
        if acoes: b['acoes'] = acoes

def validar(B):
    """Riscos que TRAVAM o render: frase sem leitura escrita, sentido invalido, passo que a ferramenta nao sabe fazer, palavra fora da frase."""
    R = []
    if B.get('encenacao_obrigatoria') is False: return R
    for i, b in enumerate(B['beats']):
        if b.get('_cta'): continue
        e = b.get('encena')
        if not isinstance(e, dict): R.append((i, 'frase SEM LEITURA ESCRITA ("encena": sentido + passos): a IA tem que ler a frase e escrever o que a tela mostra')); continue
        if e.get('rascunho'): R.append((i, 'leitura em RASCUNHO (gerada pela maquina): a IA tem que LER a frase, corrigir sentido/passos e apagar "rascunho"'))
        if e.get('sentido') not in SENTIDOS: R.append((i, f'sentido "{e.get("sentido")}" invalido (use {", ".join(SENTIDOS)})'))
        ws = [_n(w) for w in b.get('say', '').split()]
        for p in e.get('passos') or []:
            if p.get('faz') not in VOCAB: R.append((i, f'FALTA ANIMACAO "{p.get("faz")}": construir na ferramenta (encenacao.py VOCAB + motor) antes de renderizar'))
            na = _n(p.get('na', ''))
            if na and not any(na == w or na in w for w in ws): R.append((i, f'passo "{p.get("faz")}" preso na palavra "{p.get("na")}", que nao esta na frase'))
            if p.get('faz') in ('entra_em', 'transborda') and not re.search(CONTEINER, str(p.get('alvo', ''))): R.append((i, f'"{p.get("faz")}" pede um recipiente (banheira, barril, barco...): alvo "{p.get("alvo")}"'))
        if e.get('sentido') in ('negativa', 'hipotese', 'figurada') and any(p.get('faz') in ('atira', 'golpe') for p in e.get('passos') or []):
            R.append((i, f'sentido {e.get("sentido")} com tiro/golpe na tela: contradicao'))
    return R

def ficha(b, tempo_da_palavra=None):
    """Texto tecnico da encenacao para a folha 3 (o que a tela vai mostrar, passo a passo)."""
    e = b.get('encena')
    if not isinstance(e, dict): return []
    L = [f'- LEITURA DA FRASE: sentido {e.get("sentido", "?").upper()}' + (' (nada de tiro, explosao ou batalha na tela)' if e.get('sentido') in ('negativa', 'hipotese', 'figurada') else '')]
    who = b.get('who') or []
    for k, p in enumerate(e.get('passos') or [], 1):
        q = p.get('quem'); nome = str(who[q]).split(':')[0] if q is not None and q < len(who) else 'objeto'
        t = tempo_da_palavra(p.get('na')) if tempo_da_palavra and p.get('na') else None
        L.append(f'  {k}) {nome} {VOCAB.get(p.get("faz"), ("FALTA ANIMACAO",))[0]}' + (f' | alvo: {p["alvo"]}' if p.get('alvo') else '') + (f' | na palavra "{p["na"]}"' if p.get('na') else '') + (f' ({t:.1f}s)' if t is not None else ''))
    return L

def _linhas_folha3(i):
    """{bN: [(palavra, rotulo)]} das linhas executadas na folha 3."""
    import os
    out, cena = {}, None
    p = f'stories/{i}/folha3_acao.md'
    if not os.path.exists(p): return out
    for l in open(p, encoding='utf-8'):
        m = re.match(r'## Cena (b\d+)', l)
        if m: cena = m.group(1); out[cena] = []; continue
        r = re.match(r'\| [\d!]+ \| (.+?)(?: \([\d.]+s\))? \| (.+?) \|', l)
        if r and cena: out[cena].append((_n(r.group(1)), r.group(2)))
    return out

def conferir(i):
    """MAO DUPLA: cada passo da leitura tem que estar executado na folha 3; e nada de tiro/explosao/batalha em frase negativa/hipotese/figurada."""
    import json
    B = json.load(open(f'videos/{i}/beats.json', encoding='utf-8')); F = _linhas_folha3(i); R = []
    for k, b in enumerate(B['beats']):
        e = b.get('encena')
        if not isinstance(e, dict): continue
        rows = F.get(f'b{k}', [])
        for p in e.get('passos') or []:
            faz = p.get('faz'); na = _n(p.get('na', ''))
            if faz in ('mostra', 'anda_ate', 'fala', 'olha') or ('quem' not in p and faz not in ('entra_em', 'transborda')): continue
            rot = {'entra_em': 'senta', 'transborda': 'splash'}.get(faz, faz)
            if not any(rot in r_ for w_, r_ in rows): R.append((k, f'passo "{faz}" (palavra "{p.get("na")}") NAO foi executado na tela (folha 3 nao mostra): ajustar a cena ou construir a animacao'))
        if e.get('sentido') in ('negativa', 'hipotese', 'figurada'):
            bad = [r_ for w_, r_ in rows if re.search(r'BATALHA|burst|ACAO: atira|flash', r_) and 'sem tiro' not in r_]
            if bad: R.append((k, f'frase {e.get("sentido")} e a tela mostra {bad[0]}: tirar'))
    return R

def rascunho(i, salvar=True):
    """Primeira leitura AUTOMATICA (a partir do que o motor entendeu) para a IA REVISAR. Marca "rascunho": true; a aprovacao exige revisado."""
    import json, sentido as S
    P = f'videos/{i}/beats.json'; B = json.load(open(P, encoding='utf-8')); F = _linhas_folha3(i); n = 0
    for k, b in enumerate(B['beats']):
        if isinstance(b.get('encena'), dict) or b.get('_cta'): continue
        passos = []
        for w_, r_ in F.get(f'b{k}', []):
            m = re.match(r'ACAO: ([a-z_]+)', r_)
            if m and m.group(1) in VOCAB: passos.append({'quem': 0, 'faz': m.group(1), 'na': w_})
            elif 'splash' in r_ and any(re.search(CONTEINER, str(p_[0])) for p_ in (b.get('props') or []) if isinstance(p_, list)):
                passos.append({'faz': 'transborda', 'alvo': next(str(p_[0]) for p_ in b['props'] if isinstance(p_, list) and re.search(CONTEINER, str(p_[0]))), 'na': w_})
        if not passos: passos = [{'faz': 'mostra', 'na': (b['say'].split() or [''])[0].strip('.,!?')}]
        b['encena'] = {'sentido': S.classificar(b.get('say', '')), 'passos': passos, 'rascunho': True}; n += 1
    if salvar: json.dump(B, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    L = [f'# LEITURA DAS FRASES - {i} (revisar cada linha; corrigir no beats.json "encena" e apagar "rascunho")']
    for k, b in enumerate(B['beats']):
        e = b.get('encena') or {}
        L.append(f'b{k} [{e.get("sentido")}{" RASCUNHO" if e.get("rascunho") else ""}] "{b.get("say")}"')
        for p in e.get('passos') or []: L.append(f'    - {p.get("faz")} quem={p.get("quem", "-")} alvo={p.get("alvo", "-")} na="{p.get("na")}"')
    open(f'stories/{i}/leitura.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    return n

def forcar(i):
    """Passos da leitura que a tela nao executou viram acao EXPLICITA (forcar); roda depois de conferir."""
    import json
    P = f'videos/{i}/beats.json'; B = json.load(open(P, encoding='utf-8')); F = _linhas_folha3(i); n = 0
    for k, b in enumerate(B['beats']):
        e = b.get('encena')
        if not isinstance(e, dict): continue
        rows = F.get(f'b{k}', [])
        for p in e.get('passos') or []:
            faz = p.get('faz')
            if faz in ('mostra', 'anda_ate', 'entra_em', 'transborda') or VOCAB.get(faz, ('', ''))[1] != 'acao': continue
            if 'quem' not in p: continue   # acao de bicho/grupo sem personagem definido: nao forca em ninguem (a cena dos animais cuida)
            if not any(faz in r_ for w_, r_ in rows) and not p.get('forcar'): p['forcar'] = True; n += 1
    json.dump(B, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return n

def revisar(i, texto):
    """Aplica a LEITURA da IA escrita em linhas curtas: 'bN S passo; passo'  S = A|N|H|G|F (afirmativa, negativa, hipotese, figurada, fato)
    passo = faz@palavra[:quem][>alvo]  (alvo = objeto 'kit/x' ou indice de personagem). Apaga o rascunho dessas frases."""
    import json
    P = f'videos/{i}/beats.json'; B = json.load(open(P, encoding='utf-8')); SM = {'A': 'afirmativa', 'N': 'negativa', 'H': 'hipotese', 'G': 'figurada', 'F': 'fato'}
    for l in texto.strip().splitlines():
        m = re.match(r'\s*b(\d+)\s+([ANHGF])\s*(.*)$', l.strip())
        if not m: continue
        k, sen, rest = int(m.group(1)), SM[m.group(2)], m.group(3)
        passos = []
        for ps in [x.strip() for x in rest.split(';') if x.strip()]:
            mm = re.match(r'([a-z_]+)@([^:>]+)(?::(\d+))?(?:>(.+))?$', ps)
            if not mm: raise SystemExit(f'passo mal escrito em b{k}: {ps}')
            p = {'faz': mm.group(1), 'na': mm.group(2).strip()}
            if mm.group(3) is not None: p['quem'] = int(mm.group(3))
            if mm.group(4):
                a = mm.group(4).strip()
                if a.isdigit(): p['alvo_quem'] = int(a)
                else: p['alvo'] = a
            passos.append(p)
        B['beats'][k]['encena'] = {'sentido': sen, 'passos': passos}
    json.dump(B, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    import sys
    cmd, i = sys.argv[1], sys.argv[2]
    if cmd == 'rascunho': print(f'{i}: {rascunho(i)} frase(s) com leitura em RASCUNHO -> stories/{i}/leitura.md (REVISAR)')
    elif cmd == 'forcar': print(f'{i}: {forcar(i)} passo(s) forcado(s)')
    elif cmd == 'revisar': revisar(i, open(sys.argv[3], encoding='utf-8').read() if len(sys.argv) > 3 else sys.stdin.read()); print(f'{i}: leitura revisada aplicada')
    elif cmd == 'conferir':
        r = conferir(i)
        for k, m in r: print(f'b{k} {m}')
        sys.exit(1 if r else 0)
