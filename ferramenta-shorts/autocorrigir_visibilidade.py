# AUTOCORRECAO DE VISIBILIDADE (ordem do Gibson 24/11: "a ferramenta tem que resolver sozinha na hora da animacao").
# Le stories/<id>/visibilidade.json (medido no motor por visivel.mjs) e CONSERTA o beats.json sozinha, sem esperar ninguem:
#   - objeto citado que nao aparece  -> 1a vez: traz o objeto para perto do centro do quadro (objeto pequeno) ou mira a camera nele
#                                       em plano aberto (objeto grande: navio, submarino, aviao, casa...), sem multidao na frente;
#                                       2a vez: objeto na frente dos personagens e maior; 3a vez: cena do objeto (camera so' nele).
#   - objeto tapando a camera        -> se e' um "props" da cena: vai para o lado e para tras; se nao: troca o enquadramento.
#   - camera dentro de objeto        -> o objeto vai para longe (fica inteiro no fundo) e a mira da camera sai dele.
#   - animal citado pequeno          -> camera mais perto e animais maiores (2a vez: animais na frente, plano de grupo).
# Cada conserto fica anotado em stories/<id>/autocorrecoes.md. Saida 0 = mudou algo (refazer as folhas/storyboard); 1 = nada a fazer.
import json, re, sys, os, datetime
i = sys.argv[1]; V = json.load(open(f'stories/{i}/visibilidade.json')); P = f'videos/{i}/beats.json'; D = json.load(open(P)); BT = D['beats']
GRANDE = re.compile(r'navio|ship|boat|submarino|aviao|airplane|tanque|tank|casa|house|predio|building|castelo|igreja|torre|ponte|trem|locomotiva|onibus|caminhao|truck|balloon|balao|foguete|rocket|well|poco', re.I)
log = []; mudou = False
def num(x):
    try: return float(x)
    except Exception: return 0.0
feitos = set()
for falha in V.get('falhas', []):
    m = re.match(r'b(\d+)\S*: (.*)', falha)
    if not m: continue
    if (m.group(1), m.group(2)) in feitos: continue   # a mesma falha em varias tomadas da cena = um conserto por volta
    feitos.add((m.group(1), m.group(2)))
    k = int(m.group(1)); txt = m.group(2); b = BT[k]; n = int(b.get('_auto_vis', 0))
    if n >= 3: log.append(f'b{k}: ja corrigida 3 vezes, {txt} -> fica para o olho'); continue
    props = b.setdefault('props', [])
    a = re.search(r'"([^"]+)"', txt); a = a.group(1) if a else ''
    idx = next((j for j, p in enumerate(props) if str(p[0]) == a), None)
    if 'nao aparece' in txt or 'planejou' in txt:
        if idx is None: props.append([a, 0.0, 0.6, 1.2]); idx = len(props) - 1
        p = props[idx]; x, z = num(p[1]), num(p[2]); s = num(p[3]) if len(p) > 3 else 1.0
        if GRANDE.search(a):
            if n == 0: b.update({'shot': 'wide', 'cx': round(x, 1), 'cz': round(z * 0.7, 1), 'h': 2.8, 'd0': round(max(13.0, abs(z) * 0.8 + 8), 1), 'd1': round(max(11.0, abs(z) * 0.8 + 5), 1)}); b['crowd'] = {'n': 0}; acao = f'camera em plano aberto mirando o objeto (cx {b["cx"]}, cz {b["cz"]}), sem multidao na frente'
            elif n == 1: p[1] = 0.0; b.update({'cx': 0.0, 'cz': round(z * 0.7, 1), 'd0': round(abs(z) * 0.6 + 10, 1), 'd1': round(abs(z) * 0.6 + 7, 1)})   # objeto grande NAO vem para perto (vira parede): fica no fundo, centralizado; b['who'] = (b.get('who') or [])[:1]; acao = 'objeto centralizado no fundo (sem trazer para perto), so 1 personagem na frente'
            else: b['who'] = (b.get('who') or [])[:1]; b['crowd'] = {'n': 0}; b.update({'cx': 0.0, 'cz': round(num(p[2]) * 0.7, 1), 'd0': round(abs(num(p[2])) + 7, 1), 'd1': round(abs(num(p[2])) + 5, 1)}); acao = 'camera mais perto do objeto, 1 personagem de lado'
        else:
            if n == 0: p[1], p[2] = round(max(-1.6, min(1.6, x * 0.5)), 1), round(max(z, -1.0) if z < 0.6 else min(z, 1.2), 1); acao = f'objeto trazido para perto do centro ({p[1]}, {p[2]})'
            elif n == 1: p[1], p[2] = 0.6, 1.0; s = max(s, 1.5); acao = 'objeto na frente dos personagens e maior'
            else: p[1], p[2] = 0.0, 1.4; s = max(s, 2.0); b['detalhe'] = True; acao = 'close no objeto'
            if len(p) > 3: p[3] = s
            else: p.append(s)
    elif 'tapando a camera' in txt:
        if idx is not None: p = props[idx]; p[1] = 4.6 if num(p[1]) >= 0 else -4.6; p[2] = min(num(p[2]), -3.0); acao = f'"{a}" foi para o lado e para tras ({p[1]}, {p[2]})'
        else:
            seq = ['two', 'wide', 'group', 'low']; cur = b.get('shot', 'two'); b['shot'] = seq[(seq.index(cur) + 1) % len(seq)] if cur in seq else 'wide'; b['detalhe'] = False; acao = f'enquadramento trocado para "{b["shot"]}" (o que tapava e cenario)'
    elif 'CORTADO' in txt:
        if n == 0: b['shot'] = 'wide' if b.get('shot') != 'wide' else 'group'; b['detalhe'] = False; acao = f'enquadramento mais aberto ("{b["shot"]}") para o personagem caber inteiro'
        else:
            w = b.get('who') or []
            if len(w) > 1: b['who'] = w[:max(1, len(w) - 1)]; acao = 'um personagem a menos na cena (o da borda saia cortado)'
            else: b['d0'] = round(num(b.get('d0', 9)) + 3, 1); b['d1'] = round(num(b.get('d1', 8)) + 3, 1); acao = 'camera mais afastada para o personagem caber inteiro'
    elif 'cobrindo a tela' in txt:
        if idx is not None: p = props[idx]; p[2] = round(min(num(p[2]), -6.0) - 12.0, 1); b.update({'cx': round(num(p[1]) * 0.5, 1), 'cz': round(num(p[2]) * 0.5, 1), 'd0': round(abs(num(p[2])) * 0.6 + 10, 1), 'd1': round(abs(num(p[2])) * 0.6 + 7, 1)}); acao = f'"{a}" afastado para o fundo ({p[2]}) com a camera aberta (nao vira parede)'
        else: b['shot'] = 'wide'; b['fachada'] = False; acao = 'plano aberto sem fachada (o que cobria a tela era cenario)'
    elif 'PONTINHO' in txt:   # personagem minusculo (camera longe por causa de objeto grande): camera perto dos personagens, objeto grande mais para o fundo
        d0, d1 = num(b.get('d0', 20)), num(b.get('d1', 18)); nd0, nd1 = min(20.0, max(9.0, d0 * 0.45)), min(18.0, max(8.0, d1 * 0.45))
        for p in props:
            if GRANDE.search(str(p[0])) and len(p) > 2: p[2] = round(num(p[2]) - (d0 - nd0), 1)
        b['d0'], b['d1'] = round(nd0, 1), round(nd1, 1); b['cz'] = 0.0; b['h'] = min(num(b.get('h', 3)), 3.5)
        acao = f'camera perto dos personagens (d {b["d0"]}) e objeto grande empurrado para o fundo (continua inteiro pela perspectiva)'
    elif 'objeto ENORME' in txt:   # objeto pequeno cobrindo o quadro: menor e sem o close automatico
        if idx is not None:
            p = props[idx]
            if len(p) > 3 and not isinstance(p[3], dict): p[3] = round(num(p[3]) * 0.6, 2)
            else: p.insert(3, 0.7)
        b['detalhe'] = False; acao = f'"{a}" menor e sem close (cobria o quadro)'
    elif 'animal citado' in txt:   # bicho citado pequeno demais: camera mais perto e bicho maior/na frente
        an = b.get('animals') or []
        for a_ in an:
            while len(a_) < 5: a_.append([0.0, 0.6, 'stand', 1.0][len(a_) - 1])
            a_[4] = round(min(2.6, num(a_[4]) * 1.35), 2)
            if n >= 1: a_[2] = round(max(num(a_[2]), 1.2), 1)
        b['d0'] = round(max(6.0, num(b.get('d0', 11)) * 0.6), 1); b['d1'] = round(max(5.0, num(b.get('d1', 10)) * 0.6), 1)
        if n >= 1 and b.get('shot') == 'wide': b['shot'] = 'group'
        acao = f'camera mais perto (d {b["d0"]}->{b["d1"]}) e animais maiores' + (' e na frente dos personagens' if n >= 1 else '')
    elif 'DENTRO' in txt:
        if idx is not None: p = props[idx]; p[2] = round(min(num(p[2]), -8.0) - 14.0, 1)
        for c in ('cx', 'cz'): b.pop(c, None)
        acao = f'"{a}" afastado para o fundo e mira da camera fora dele'
    else: continue
    b['_auto_vis'] = n + 1; mudou = True; log.append(f'b{k}: {txt} -> {acao}')
import subprocess, shutil
def riscos():
    o = subprocess.run(['python3', 'mkvideo.py', i], capture_output=True, text=True).stdout
    m_ = re.findall(r'-> (\d+) RISCO', o); return int(m_[-1]) if m_ else 99
if mudou:
    antes = riscos(); shutil.copy(P, P + '.antes_autovis'); json.dump(D, open(P, 'w'), ensure_ascii=False, indent=1)
    if riscos() > antes:
        shutil.copy(P + '.antes_autovis', P); subprocess.run(['python3', 'mkvideo.py', i], capture_output=True); log.append('conserto DESFEITO: criaria risco novo nas folhas (fica para o olho)'); mudou = False
with open(f'stories/{i}/autocorrecoes.md', 'a') as f:
    f.write(f'\n## {datetime.datetime.now():%d/%m %H:%M} autocorrecao de visibilidade\n' + ''.join(f'- {l}\n' for l in log))
print('\n'.join(log) or 'nada a corrigir'); sys.exit(0 if mudou else 1)
