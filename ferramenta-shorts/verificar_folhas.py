#!/usr/bin/env python3
# VERIFICACAO DAS 3 FOLHAS (ordem do Gibson 19/11): o video so' renderiza se a ferramenta GEROU e LEU as tres folhas e se a producao SEGUE a folha 3.
# uso: python3 verificar_folhas.py <id> [--render]   (--render tambem confere se o web/story.js montado para o render carrega a mesma folha 3)
import sys, os, re, json, hashlib
ID = sys.argv[1]; D = f'stories/{ID}'; erros = []
F = {n: f'{D}/{n}' for n in ('folha1_roteiro.md', 'folha2_producao.md', 'folha3_acao.md')}
for n, p in F.items():
    if not os.path.exists(p): erros.append(f'{n} NAO EXISTE (rode python3 mkvideo.py {ID})')
base = max(os.path.getmtime(f'videos/{ID}/beats.json'), os.path.getmtime('mkvideo.py'))
for n, p in F.items():
    if os.path.exists(p) and os.path.getmtime(p) < base - 1: erros.append(f'{n} DESATUALIZADA (o roteiro ou a ferramenta mudou depois): rode python3 mkvideo.py {ID}')
try: J = json.load(open(f'{D}/folhas.json'))
except Exception: J = None; erros.append('folhas.json ausente: as folhas nao foram geradas pela ferramenta atual')
if J:
    if J['riscos']: erros.append(f"folha 2: {J['riscos']} RISCO(S) em aberto (corrija o roteiro; so' renderiza com 0)")
    if J['faltando']: erros.append(f"folha 3: {J['faltando']} ACAO(OES) SEM ANIMACAO (linhas FALTA)")
    f3 = open(F['folha3_acao.md'], encoding='utf-8').read().splitlines() if os.path.exists(F['folha3_acao.md']) else []
    L = [l for l in f3 if l.startswith('| ') and not l.startswith('| #')]
    h = hashlib.sha1('\n'.join(L).encode()).hexdigest()[:12]
    if h != J['hash_folha3']: erros.append('folha 3 foi alterada a mao ou nao e a que a ferramenta gerou (assinatura diferente): rode python3 mkvideo.py ' + ID)
    sp = open(f'{D}/spec.js', encoding='utf-8').read() if os.path.exists(f'{D}/spec.js') else ''
    m = re.search(r'// FOLHA3 (\w+) (\d+)', sp)
    if not m or m.group(1) != h: erros.append('a producao (spec.js) NAO segue a folha 3 atual: rode python3 mkvideo.py ' + ID)
    if '--render' in sys.argv:
        if open(f'{D}/STORYBOARD_OK').read().strip() != h if os.path.exists(f'{D}/STORYBOARD_OK') else True: erros.append('STORYBOARD NAO APROVADO para esta versao das folhas (olhe stories/' + ID + '/storyboard.jpg e rode ./aprovar_storyboard.sh ' + ID + ')')
        st = open('web/story.js', encoding='utf-8').read() if os.path.exists('web/story.js') else ''
        if f'// FOLHA3 {h}' not in st: erros.append('o que vai para o render (web/story.js) nao carrega a folha 3 deste video')
    n_acoes = len([l for l in L if l.rstrip().endswith('| OK |')])
if erros:
    print('BLOQUEADO - 3 FOLHAS:'); [print(' -', e) for e in erros]; sys.exit(1)
print(f"3 FOLHAS OK: lidas e seguidas (folha 3: {J['acoes']} acoes com animacao, assinatura {J['hash_folha3']})")
