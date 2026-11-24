#!/usr/bin/env python3
# FICHA TECNICA DENTRO DAS FOLHAS (ordem do Gibson 24/11: "nao precisa criar outra folha, so' colocar mais dados").
# Depois do mkvideo, completa as folhas que ja existem:
#   FOLHA 2 (producao), em cada cena: FICHA TECNICA (local, camera, personagens com posicao, cada objeto com lugar/tamanho/estado,
#            efeitos, som, texto) + TAKES (quantos planos a cena tem, a duracao de cada um e o angulo/distancia da camera em cada take).
#   FOLHA 3 (acao), em cada cena: FISICA E MOVIMENTO (como cada acao acontece no corpo/objeto: tempo, direcao, o que fica no fim).
# Assim a ferramenta e quem revisa tem a cena inteira descrita, sem margem para "imaginar".
import json, re, os, sys, subprocess
ID = sys.argv[1]; D = f'stories/{ID}'
F2, F3, FE = f'{D}/folha2_producao.md', f'{D}/folha3_acao.md', f'{D}/folha2_enquadramento.md'
if not (os.path.exists(F2) and os.path.exists(F3)): sys.exit(0)
subprocess.run([sys.executable, 'enquadrar.py', ID, '--so-descrever'], capture_output=True)
B = json.load(open(f'videos/{ID}/beats.json')); BT = B['beats']
fe = open(FE, encoding='utf-8').read() if os.path.exists(FE) else ''
FICHA = {int(m.group(1)): m.group(2).strip() for m in re.finditer(r'^## b(\d+): .*?\n(.*?)(?=^## b|\Z)', fe, re.S | re.M)}
rt = open('web/runtime.js', encoding='utf-8').read()
VARS = [dict(az=float(a), el=float(e), d=float(d)) for a, e, d in re.findall(r'\{ az: (-?[\d.]+), el: (-?[\d.]+), d: ([\d.]+)', rt.split('const VARS = ')[1].split(';')[0])]
sp = open(f'{D}/spec.js', encoding='utf-8').read() if os.path.exists(f'{D}/spec.js') else ''
cutLen = int((re.search(r'cutLen: (\d+)', sp) or re.search(r'(66)', '66')).group(1)); vseed = int((re.search(r'vseed: (\d+)', sp) or re.search(r'(0)', '0')).group(1))
f3 = open(F3, encoding='utf-8').read()
TEMPO = {int(k): (float(a), float(b)) for k, a, b in re.findall(r'^## Cena b(\d+) - ([\d.]+)s a ([\d.]+)s', f3, re.M)}
def ang(v):
    s = []
    s.append('mesmo angulo' if abs(v['az']) < 3 else f'gira {abs(int(v["az"]))} graus para a {"direita" if v["az"] > 0 else "esquerda"}')
    if abs(v['el']) >= 3: s.append('camera mais alta, olhando um pouco de cima' if v['el'] > 0 else 'camera mais baixa, olhando um pouco de baixo')
    if abs(v['d'] - 1) >= 0.04: s.append('um pouco mais perto' if v['d'] < 1 else 'um pouco mais longe')
    return ', '.join(s)
def takes(k, b):
    a, z = TEMPO.get(k, (None, None))
    if a is None: return ['- TAKES: definidos quando a voz estiver pronta (tempo da cena)']
    fa, fb = round(a * 30), round(z * 30); ln = fb - fa + 1
    if b.get('explica'): return [f'- TAKES: 1 take de explicacao ({z - a:.1f} s): objeto no centro do estudio, rotulos entrando nas palavras']
    if b.get('impact') or b.get('batalha'): return [f'- TAKES: sequencia de acao em 3 cameras ({z - a:.1f} s): 1) plano medio baixo na tropa (30%); 2) travelling lateral acompanhando a acao (25%); 3) grua subindo ate a vista de cima do campo (45%)']
    n = max(1, round(ln / cutLen)) if not (b.get('veiculo') or b.get('montado')) else 1
    if n == 1: return [f'- TAKES: 1 take continuo ({z - a:.1f} s), a camera desliza devagar do enquadramento inicial ao final']
    out = [f'- TAKES: {n} takes (troca de angulo a cada ~{ln / n / 30:.1f} s, sem corte seco):']
    for j in range(n):
        t0 = a + j * (z - a) / n; t1 = a + (j + 1) * (z - a) / n; v = VARS[((fa // 66) + j + vseed) % len(VARS)]
        out.append(f'  - take {j + 1} ({t0:.1f}-{t1:.1f} s): {ang(v)}')
    return out
FIS = [(r'tomba|cai|morre|desmai', 'o corpo inclina para tras e cai no chao em ~0,4 s (poeira no impacto) e fica deitado ate o fim da cena'),
       (r'golpe|punch|soco|arranc', 'o braco avanca em ~0,2 s ate o alvo; quem leva o golpe recua meio passo, estrelinhas sobre a cabeca'),
       (r'tiro|atira|gun|disparo', 'clarao no cano da arma por ~0,25 s + estampido; a arma recua; o alvo (se houver) tomba'),
       (r'canh|explo|bomb|burst', 'clarao laranja que cresce em ~0,15 s, nuvem de fumaca que sobe e some em ~1 s, estrondo grave'),
       (r'corre|foge|persegu', 'passos rapidos com o corpo inclinado para frente; cruza o quadro de um lado ao outro'),
       (r'empurr', 'as duas maos empurram em ~0,3 s; o outro cambaleia para tras'),
       (r'comemor|danca|festa', 'bracos para cima e pulinhos curtos durante a frase'),
       (r'discut|grita|briga', 'os dois inclinam o tronco um para o outro alternando, bocas abertas, gesto de apontar'),
       (r'beb', 'leva a garrafa/caneca a boca, inclina a cabeca para tras, baixa de novo'),
       (r'escal|sobe', 'sobe a encosta/muro em passos curtos, maos a frente'),
       (r'pesca', 'puxa a linha/rede para cima com um tranco + respingo na agua'),
       (r'escrev|assin', 'segura o papel e mexe a mao como se escrevesse'),
       (r'dorme|cochil', 'olhos fechados, cabeca tomba de lado, sobe e desce devagar'),
       (r'aponta|mostra', 'braco estendido apontando para o objeto/lugar citado'),
       (r'batalha|tropa', 'tropa em fileiras; clarões piscando ao longo da fileira; alguns soldados caem; fumaca baixa'),
       (r'mapa', 'mapa entra em ~0,3 s e cobre a tela por 1-2 s, com o ponto do lugar pulsando'),
       (r'placa|texto', 'texto entra com um pulo de escala (~0,2 s) e fica ate o fim da cena')]
def fisica(k, bloco, b):
    out = ['', '**FISICA E MOVIMENTO (como cada acao acontece na tela):**']
    for lin in bloco.splitlines():
        m = re.match(r'\| \d+ \| (.*?) \| (.*?) \| (.*?) \| (\w+) \|', lin)
        if not m: continue
        pal, ac, anim = m.group(1), m.group(2), m.group(3); chave = (ac + ' ' + anim).lower()
        desc = next((d for rx, d in FIS if re.search(rx, chave)), f'executa: {anim}')
        if ac == 'BATALHA':
            _arm = any(B.get('outfits', {}).get(str(w).split(':')[0], {}).get('rifle') for w in (b.get('who') or []) + ((b.get('crowd') or {}).get('outfits') or []))
            if b.get('tiros') is False or not (_arm or re.search(r'atir|tiro|dispar|fuzil|bala', (b.get('say') or '').lower())): ac, desc = 'GRANDE MOMENTO', 'multidao atras dos personagens reage (susto/euforia) com efeito e som, SEM tiros e sem ninguem cair'
        out.append(f'- {ac} {"na palavra " + pal if pal != "-" else "(a cena toda)"}: {desc}')
    q = b.get('quadro') or {}
    for o in q.get('objetos', []):
        if o.get('estado') == 'chegando': out.append(f'- {o["objeto"]} CHEGANDO: entra pela esquerda do quadro e desliza ate o lugar da ficha em ~85% da cena (velocidade constante, sem tremer)')
        elif o.get('estado') == 'indo embora': out.append(f'- {o["objeto"]} INDO EMBORA: parte do lugar da ficha e sai pela direita do quadro ate o fim da cena')
    cr = b.get('crowd') or {}
    if cr.get('n'): out.append(f'- multidao de {cr["n"]}: {"marcha no lugar, passos sincronizados" if cr.get("march") else "parada, reagindo (" + str(cr.get("expr", "neutra")) + ")"}, sempre ATRAS dos personagens principais')
    return out if len(out) > 2 else []
def inserir(txt, cab_rx, extra_por_cena, marca):
    txt = re.sub(r'\n<!-- ' + marca + r' -->.*?<!-- /' + marca + r' -->', '', txt, flags=re.S)   # tira a versao anterior (idempotente)
    partes = re.split(r'(?=^## Cena b\d+)', txt, flags=re.M); out = []
    for p in partes:
        m = re.match(cab_rx, p)
        if m:
            k = int(m.group(1)); ex = extra_por_cena(k, p)
            if ex: p = p.rstrip('\n') + '\n<!-- ' + marca + ' -->\n' + '\n'.join(ex) + '\n<!-- /' + marca + ' -->\n\n'
        out.append(p)
    return ''.join(out)
def ex2(k, bloco):
    b = BT[k] if k < len(BT) else {}
    linhas = ['', '### FICHA TECNICA DA CENA (lugar, camera, personagens, objetos, efeitos, texto)']
    linhas += [l for l in FICHA.get(k, '- (sem ficha)').splitlines() if l.strip()]
    return linhas + takes(k, b)
def ex3(k, bloco):
    return fisica(k, bloco, BT[k] if k < len(BT) else {})
t2 = inserir(open(F2, encoding='utf-8').read(), r'## Cena b(\d+)', ex2, 'FICHA')
mt2 = os.path.getmtime(F2); open(F2, 'w', encoding='utf-8').write(t2)
t3 = inserir(f3, r'## Cena b(\d+)', ex3, 'FISICA'); open(F3, 'w', encoding='utf-8').write(t3)
n_takes = sum(int((re.search(r'TAKES: (\d+)', '\n'.join(takes(k, b))) or re.search(r'(1)', '1')).group(1)) if not (b.get('impact') or b.get('batalha')) else 3 for k, b in enumerate(BT))
print(f'FICHA NAS FOLHAS: {len(BT)} cenas, ~{n_takes} takes descritos (folha 2: ficha tecnica + takes; folha 3: fisica e movimento)')
