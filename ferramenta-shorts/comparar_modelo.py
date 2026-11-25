#!/usr/bin/env python3
# COMPARATIVO REFERENCIA x MODELO 3D (25/11, Gibson: "cadê o print da banheira da epoca? era para ir para o Blender modelar... voce pulou etapa").
# Para cada OBJETO da pesquisa (heroi e objetos citados) que existe na biblioteca 3D: foto do modelo .glb (Blender) AO LADO dos prints da pesquisa.
# Sai referencias/<id>/comparativo.jpg. Quem aprova OLHA e escreve referencias/<id>/comparativo_ok.md, uma linha por objeto:
#   "kit/bathtub: OK - igual a referencia (banheira grega de terracota)"   ou   "kit/crown: REMODELAR - referencia e' coroa de louros, modelo e' coroa de pontas"
# aprovar_storyboard.sh recusa sem o comparativo conferido; REMODELAR trava ate o objeto ser refeito no Blender (blender/*.py) e comparado de novo.
# uso: python3 comparar_modelo.py <id>
import json, os, re, subprocess, sys, unicodedata
from PIL import Image, ImageDraw
ID = sys.argv[1]; R = f'referencias/{ID}'; os.makedirs(R, exist_ok=True)
B = json.load(open(f'videos/{ID}/beats.json', encoding='utf-8'))
n = lambda t: unicodedata.normalize('NFKD', str(t).lower()).encode('ascii', 'ignore').decode()
try: P = json.load(open(f'{R}/pesquisa.json', encoding='utf-8'))
except Exception: P = {'itens': []}
usados = []   # objetos 3D que aparecem nas cenas (props) + heroi
for b in B['beats']:
    for p in b.get('props') or []:
        if isinstance(p, list) and str(p[0]).startswith('kit/') and not re.search(r'kit/(room|rg_|marco|porch)', str(p[0])) and p[0] not in usados: usados.append(p[0])
    _ex = b.get('explica') if isinstance(b.get('explica'), dict) else {}
    if str(_ex.get('objeto', '')).startswith('kit/') and _ex['objeto'] not in usados: usados.append(_ex['objeto'])   # objeto da cena de EXPLICACAO tambem (Arquimedes: coroa medieval escapou por aqui)
if B.get('heroi') and B['heroi'] not in usados: usados.insert(0, B['heroi'])
try:   # o que VAI PARA A TELA manda (spec.js ja com as trocas de epoca: coroa de louros, bola de couro...): fora do spec nao entra
    _spec = open(f'stories/{ID}/spec.js', encoding='utf-8').read(); _ass = set(re.findall(r'asset: "(kit/[a-z0-9_]+)"', _spec)) | set(re.findall(r"asset: '(kit/[a-z0-9_]+)'", _spec))
    if _ass: usados = [a for a in usados if a in _ass] + sorted(a for a in _ass if a not in usados and not re.search(r'kit/(room|rg_|marco|porch|palete)', a))
except FileNotFoundError: pass
def prints_de(asset):   # prints da pesquisa para este objeto: item heroi, ou item cujo nome casa com o nome do asset / sinonimo PT
    nome = asset.split('/')[-1]; sin = {'bathtub': 'banheira', 'crown': 'coroa', 'scale': 'balanca', 'stove': 'fogao', 'petri': 'placa|prato', 'syringe': 'seringa', 'kettle': 'chaleira', 'boardgame': 'tabuleiro', 'flamethrower': 'lanca', 'sink': 'pia', 'phone': 'celular|telefone', 'bife_elefante': 'carne|bife', 'coroa_louros': 'coroa', 'bola_couro': 'bola', 'gosma': 'borracha|gosma', 'stove': 'fogao'}.get(nome, nome)
    out = []
    for it in P.get('itens', []):
        if it.get('tipo') in ('pessoas', 'lugar', 'epoca', 'tema'): continue   # retrato/paisagem nao e' referencia de OBJETO
        if it.get('tipo') == 'heroi' and B.get('heroi') == asset or re.search(sin, n(it.get('item', ''))) or nome in n(it.get('item', '')):
            out += [a['print'] for a in it.get('achados', []) if os.path.exists(a.get('print', ''))]
    return list(dict.fromkeys(out))[:3]
linhas = []
for a in usados[:10]:
    glb = f'web/assets/library/{a}.glb'
    if not os.path.exists(glb): continue
    foto = f'{R}/modelo_{a.split("/")[-1]}.png'
    if not os.path.exists(foto) or os.path.getmtime(foto) < os.path.getmtime(glb):
        subprocess.run(['blender', '-b', '--python', 'blender/foto34.py', '--', foto, glb], capture_output=True)
    linhas.append((a, foto if os.path.exists(foto) else None, prints_de(a)))
W, H = 1200, 300
img = Image.new('RGB', (W, max(1, len(linhas)) * H), 'white'); d = ImageDraw.Draw(img)
for k, (a, foto, prs) in enumerate(linhas):
    y = k * H; d.text((8, y + 6), f'{a}  (esquerda: MODELO 3D | direita: REFERENCIAS da pesquisa)' + ('' if prs else '  -> SEM REFERENCIA: pesquisar com "visual.buscas" em ingles'), fill='black')
    if foto:
        m = Image.open(foto).convert('RGB'); m.thumbnail((380, H - 30)); img.paste(m, (5, y + 25))
    for j, pr in enumerate(prs):
        try: r = Image.open(pr).convert('RGB'); r.thumbnail((260, H - 30)); img.paste(r, (400 + j * 268, y + 25))
        except Exception: pass
    d.line([(0, y + H - 1), (W, y + H - 1)], fill='#999999')
img.save(f'{R}/comparativo.jpg', quality=85)
print(f'COMPARATIVO: {len(linhas)} objeto(s) -> {R}/comparativo.jpg | sem referencia: ' + (', '.join(a for a, f, p in linhas if not p) or 'nenhum'))
print(f'OLHE e escreva {R}/comparativo_ok.md: "<objeto>: OK - ..." ou "<objeto>: REMODELAR - ..." (uma linha por objeto)')
