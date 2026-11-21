#!/usr/bin/env python3
"""AUDITOR NARRACAO x TELA (21/11, ordem do Gibson: tudo que a narracao conta TEM que aparecer na tela).
A folha 3 antiga so conferia as acoes que a ferramenta JA reconhecia; verbo/objeto/lugar desconhecido ficava invisivel e a cena saia vazia.
Aqui a conta e' inversa: parte da NARRACAO e pergunta, frase por frase, se cada coisa narrada esta no spec da cena.
uso: python3 auditar_narracao.py <id> [-v]     |    python3 auditar_narracao.py --todos
Saida: stories/<id>/auditoria_narracao.md  +  linha de resumo. Exit 1 se houver lacuna."""
import json, re, sys, os, unicodedata, glob

def nrm(t): return unicodedata.normalize('NFKD', t.lower()).encode('ascii', 'ignore').decode()

# palavra da narracao -> assets/animais aceitos como "esta na tela"
ANIMAIS = {
    r'cavalo|cavalos|cavalaria|hussar': {'horse', 'horse_sela'}, r'cachorro|cachorros|\bcao\b|\bcaes\b|cadela': {'dog', 'kit/dog_sit'},
    r'\bgatos?\b': {'cat'}, r'elefante': {'elephant'}, r'porco|leitao': {'pig'}, r'\bboi\b|\bvaca': {'cow'}, r'ovelha': {'sheep'},
    r'\bcabra|\bbode': {'goat'}, r'burro|jumento': {'donkey'}, r'veado|cervo': {'deer'}, r'raposa': {'fox'}, r'\blobos?\b': {'wolf'},
    r'coelho': {'rabbit'}, r'\bleao|\bleoes': {'lion'}, r'\bursos?\b': {'bear'}, r'galinha': {'chicken'}, r'\bgalo\b': {'rooster', 'chicken'},
    r'\bpatos?\b': {'duck'}, r'ganso': {'goose', 'chicken'}, r'gaivota': {'gull'}, r'\bemus?\b': {'emus', 'emu'},
    r'macaco': {'kit/monkey_pong'}, r'\brato|roedor|ratazana': {'rato', 'kit/rato'}, r'bacalhau': {'kit/cod'}, r'pombo|passarinho|tentilh|\baves?\b': {'kit/finch'},
}
ANIMAIS_SEM_MODELO = r'canguru|dromedario|camelo|abelha|cobra|peixe\b'
LUGARES = {  # palavra -> (rotulo, aceita se o 'set'/interior/prop/texto da cena contiver algo de...)
    r'zoologico': ('ZOOLOGICO', {'cage', 'zoo', 'elephant'}), r'estadio|campo de futebol|gramado|partida|\bjogo de futebol|futebol': ('ESTADIO/CAMPO', {'stadium', 'ball'}),
    r'hospital|enfermaria': ('HOSPITAL', {'hospital'}), r'restaurante|cozinha|\bmesa\b|prato|jantar': ('MESA/RESTAURANTE', {'table', 'plate', 'loja', 'stall', 'cake_table', 'panela', 'kettle'}),
    r'praia|\bmar\b|porto|navio|cais|oceano': ('MAR/PORTO', {'harbor', 'ship', 'navio', 'ilha'}), r'montanha|\bmonte\b|colina|morro': ('MONTANHA', {'mountain'}),
    r'deserto': ('DESERTO', {'outback', 'palace'}), r'floresta|mata\b|selva': ('FLORESTA', {'jungle', 'tree'}), r'neve|gelo|congel|inverno': ('NEVE', {'arctic', 'neve'}),
    r'palacio|congresso|\bonu\b|tribunal': ('PALACIO/SALA', {'pedra', 'palace', 'hall'}), r'estudio|palco|plateia|apresentacao': ('PALCO/ESTUDIO', {'stadium', 'hall', 'palco'}),
}
VERBOS_ABSTRATOS = set('era foi eram foram tinha tinham estava estavam ficou ficaram disse disseram havia haviam podia podiam queria queriam sabia sabiam viu viram veio vieram deu deram achou acharam resolveu resolveram decidiu decidiram passou passaram chamou chamaram contou contam dizem diz acontece aconteceu significa tornou tornaram virou viraram ganhou ganharam perdeu perderam levou levaram durou duraram saiu sairam terminou acabou acabaram comecou comecaram continuou continuaram voltou voltaram esperava esperavam percebeu perceberam entendeu entenderam pensou pensaram achava achavam parecia pareciam existe existem existia existiam venceu venceram ficam fica ficava ficavam'.split())
RX_VERBO = re.compile(r'^[a-z]{4,}(ou|aram|eu|eram|iu|iram|ia|iam|ava|avam)$')
# verbos "de cena" que EXIGEM ver a acao (os que o Gibson citou + equivalentes). Cobertura = palavra aparece numa linha da folha 3 (acao com animacao).
ACAO_CENICA = r'cercou|cercaram|cercando|sitiou|invadiu|atacou|atirou|dispar|chutou|jogou|lancou|arremess|correram|correu|fugiu|fugiram|abracou|abracaram|comeu|comeram|bebeu|beberam|serviu|cozinh|plantou|cavou|construiu|montou|pintou|escreveu|assinou|votou|votaram|pagou|vendeu|comprou|entregou|dancou|cantou|rezou|lutou|brigou|empurrou|derrubou|caiu|morreu|explodiu|pousou|decolou|voou|navegou|marcharam|desembarc|rendeu|renderam|capturou|prendeu|mandou|usavam|usou|guardava|guardou|carregava|carregou|cortou|raspou|pegou|segurou|olharam|olhou|apontou|gritou|riu|riram|chorou|sentou|dormiu'

def cenas_do_spec(sid):
    s = open(f'stories/{sid}/spec.js', encoding='utf-8').read()
    partes = re.split(r"(?=S\('b\d+(?:_\d+)?', )", s)
    cenas = {}
    for p in partes:
        m = re.match(r"S\('(b\d+)(?:_\d+)?', [^,]+, [^,]+, (X\w*),", p)
        if not m: continue
        k = m.group(1); d = cenas.setdefault(k, {'set': set(), 'animals': set(), 'assets': set(), 'actors': 0, 'texto': set(), 'poses': set(), 'fx': set()})
        d['set'].add(m.group(2).replace('X_', '').replace('X', 'street'))
        d['animals'] |= set(re.findall(r'animal: "(\w+)"|bird: "(\w+)"', p) and [a or b for a, b in re.findall(r'animal: "(\w+)"|bird: "(\w+)"', p)])
        d['assets'] |= set(re.findall(r'asset: ["\']([\w/]+)', p))
        d['actors'] = max(d['actors'], len(re.findall(r'pp\(X\w*, "', p)) + len(re.findall(r'outfit: "', p)))
        d['texto'] |= set(re.findall(r'txt\(X\w*, [^,]+, [^,]+, "([^"]+)"', p))
        d['poses'] |= set(re.findall(r"pose: '(\w+)'", p)) | set(re.findall(r"'(kneel|fall|sleep|sit)'\]", p))
        d['fx'] |= set(re.findall(r"k: ['\"](\w+)['\"]", p))
        if "carregado" in p: d['poses'].add('carrega')
    return cenas

def acoes_folha3(sid):
    t = open(f'stories/{sid}/folha3_acao.md', encoding='utf-8').read(); out = {}
    for m in re.finditer(r'## Cena (b\d+) .*?(?=\n## Cena b\d+ |\Z)', t, re.S):
        out[m.group(1)] = [(w.strip(), a.strip()) for w, a in re.findall(r'\| \d+ \| (.+?) \([\d.]+s\) \| ([A-Z_a-z]+: ?[^|]*?) \|', m.group(0))]
    return out

def auditar(sid, verboso=False):
    B = json.load(open(f'videos/{sid}/beats.json'))['beats']
    C = cenas_do_spec(sid); F = acoes_folha3(sid); linhas = []; ok = 0; lacunas_total = 0
    for i, b in enumerate(B):
        k = f'b{i}'; say = b['say']; n = nrm(say); c = C.get(k, {'set': set(), 'animals': set(), 'assets': set(), 'actors': 0, 'texto': set(), 'poses': set(), 'fx': set()})
        lac = []
        for rx, aceitos in ANIMAIS.items():
            if re.search(rx, n) and not (c['animals'] & aceitos or any(a.split('/')[-1] in aceitos or a in aceitos for a in c['assets'])):
                lac.append(f'ANIMAL narrado ({re.search(rx, n).group(0)}) NAO aparece')
        if re.search(ANIMAIS_SEM_MODELO, n): lac.append(f'ANIMAL/OBJETO sem modelo na biblioteca ({re.search(ANIMAIS_SEM_MODELO, n).group(0)}): modelar (Blender) ou mostrar por cartaz/prato')
        ambiente = ' '.join(list(c['set']) + list(c['assets']) + list(c['animals']) + list(c['texto'])).lower() + ' ' + nrm(str(b.get('interior') or '')) + ' ' + nrm(str(b.get('set') or ''))
        for rx, (rot, aceitos) in LUGARES.items():
            if re.search(rx, n) and not any(a in nrm(ambiente) for a in aceitos):
                lac.append(f'LUGAR/CENARIO narrado ({rot}) NAO aparece')
        acoes = F.get(k, []); palavras_acao = ' '.join(nrm(w) for w, _ in acoes) + ' ' + ' '.join(nrm(str(v.get('palavra', ''))).replace('^', '') for v in (b.get('voa') or []))   # projetil 'voa' conta como animacao da palavra
        for w in re.findall(r'[a-zA-ZÀ-ú]+', say):
            nw = nrm(w)
            if re.match(ACAO_CENICA, nw) and nw[:5] not in palavras_acao:
                lac.append(f'ACAO narrada ("{w}") sem animacao na folha 3')
        if not acoes and not any(x in ('react', 'cheer', 'dance', 'argue', 'eat') for x in c['poses']) and not any(x in c['assets'] for x in ('kit/finch',)) and c['actors'] <= 3 and len(say.split()) > 6:
            lac.append('CENA PARADA: ninguem faz nada e nada do que foi narrado aparece')
        lac = list(dict.fromkeys(lac)); lacunas_total += len(lac)
        if not lac: ok += 1
        linhas.append((k, say, lac, c, acoes))
    cobertura = round(100 * ok / max(1, len(B)))
    md = [f'# AUDITORIA NARRACAO x TELA: {sid}', f'Cenas 100% fieis: {ok}/{len(B)} ({cobertura}%). Lacunas: {lacunas_total}', '']
    for k, say, lac, c, acoes in linhas:
        md.append(f'## {k} {"OK" if not lac else "LACUNA"} - {say}')
        md.append(f'- na tela: set={sorted(c["set"])} animais={sorted(c["animals"])} objetos={sorted(a.split("/")[-1] for a in c["assets"])} atores={c["actors"]} acoes_folha3={[w for w, _ in acoes]}')
        for l in lac: md.append(f'- **FALTA:** {l}')
    open(f'stories/{sid}/auditoria_narracao.md', 'w', encoding='utf-8').write('\n'.join(md) + '\n')
    return cobertura, lacunas_total, len(B), md

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if sys.argv[1] == '--todos':
        ids = []
        for f in ('queue.txt', 'fila_sessao_A.txt', 'fila_sessao_B.txt'):
            ids += [l.split()[0] for l in open(f) if l.strip() and not l.startswith('#')]
        res = []
        for i in dict.fromkeys(ids):
            try:
                if os.path.exists(f'stories/{i}/spec.js') and os.path.exists(f'stories/{i}/folha3_acao.md'): res.append((i,) + auditar(i)[:3])
            except Exception as e: print('ERRO', i, e)
        res.sort(key=lambda r: r[1])
        for i, cob, lac, n in res: print(f'{cob:3d}% fiel  {lac:3d} lacunas  {n:2d} cenas  {i}')
        print(f'MEDIA: {sum(r[1] for r in res) // max(1, len(res))}% das cenas fieis ({len(res)} videos)')
    else:
        cob, lac, n, md = auditar(sys.argv[1]); print(f'{sys.argv[1]}: {cob}% fiel, {lac} lacunas em {n} cenas')
        if '-v' in sys.argv or lac: print('\n'.join(l for l in md if l.startswith('## ') and 'LACUNA' in l or l.startswith('- **FALTA')))
        sys.exit(1 if lac else 0)
