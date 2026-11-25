#!/usr/bin/env bash
# APROVAR O STORYBOARD (obrigatorio antes do render, ordem do Gibson 19/11). So' rode DEPOIS de abrir e olhar stories/<id>/storyboard.jpg
# conferindo frase por frase com a folha 3 (cada acao acontecendo, ninguem cortado, cenario certo, objeto heroi visivel).
# EXIGE stories/<id>/revisao_storyboard.md (uma linha por frase, feita depois do storyboard atual).
# uso: ./aprovar_storyboard.sh <id>        (a aprovacao vale para ESTA versao das folhas; mudou o roteiro/ferramenta -> novo storyboard e nova aprovacao)
cd "$(dirname "$0")"; ID="${1:?id}"
[ -f stories/$ID/storyboard.jpg ] || { echo "sem storyboard: a fila gera sozinha (ou ./prechecar.sh $ID && cp stories/$ID/precheck.jpg stories/$ID/storyboard.jpg)"; exit 1; }
python3 verificar_folhas.py $ID || exit 1
# VISIBILIDADE (24/11, causa raiz do retrabalho): o motor mede se cada objeto citado aparece, se nada tapa a camera e se a camera nao esta dentro de objeto
[ -f stories/$ID/visibilidade.json ] && [ ! stories/$ID/visibilidade.json -ot stories/$ID/storyboard.jpg ] || { echo "FALTA A CHECAGEM DE VISIBILIDADE deste storyboard (a fila roda sozinha: node visivel.mjs $ID depois do build3.sh $ID)"; exit 1; }
python3 - "$ID" <<'PYV' || exit 1
import json, sys, re
i = sys.argv[1]; V = json.load(open(f'stories/{i}/visibilidade.json')); B = json.load(open(f'videos/{i}/beats.json'))
import os
ok = set(B.get('visivel_ok', [])) | (set(re.findall(r'^(b\d+):', open(f'stories/{i}/visivel_ok.txt').read(), re.M)) if os.path.exists(f'stories/{i}/visivel_ok.txt') else set())   # excecao consciente, com motivo: stories/<id>/visivel_ok.txt  ('b1: figurante da multidao encostando na borda')
f = [x for x in V['falhas'] if re.match(r'b\d+', x).group(0) not in ok]
if f: print('VISIBILIDADE REPROVADA (corrija o beats.json e gere o storyboard de novo):\n  ' + '\n  '.join(f)); sys.exit(1)
print('visibilidade OK')
PYV
# 25/11 LEITURA ESCRITA (Gibson: "a ferramenta tem que entender o contexto de cada frase"): quem aprova LEU cada frase e escreveu no beats o "encena" (sentido + passos)
python3 mkvideo.py $ID >/dev/null 2>&1; python3 ficha_nas_folhas.py $ID >/dev/null 2>&1; python3 encenacao.py conferir $ID >> stories/$ID/encenacao_falta.txt 2>/dev/null   # mao dupla: leitura x tela
if [ -s stories/$ID/encenacao_falta.txt ]; then echo "FALTA A LEITURA ESCRITA de frases (encenacao.py): leia cada frase e escreva no beats.json o \"encena\": {\"sentido\": afirmativa|negativa|hipotese|figurada|fato, \"passos\": [{quem, faz, alvo, na}]}:"; sed 's/^/  /' stories/$ID/encenacao_falta.txt; exit 1; fi
H=$(python3 -c "import json;print(json.load(open('stories/$ID/folhas.json'))['hash_producao'])")
# 25/11 (sessao A): a ferramenta muda o tempo todo (sync de 1 min); se o hash das folhas mudou mas NENHUMA CENA mudou (mesmo desenho de cada cena), o storyboard olhado continua valendo
if [ "$(cat stories/$ID/storyboard.hash 2>/dev/null)" != "$H" ] && [ -s stories/$ID/storyboard.cenas ]; then python3 mkvideo.py $ID >/dev/null 2>&1; python3 ficha_nas_folhas.py $ID >/dev/null 2>&1; ./build3.sh $ID >/dev/null 2>&1; H=$(python3 -c "import json;print(json.load(open('stories/$ID/folhas.json'))['hash_producao'])")
  if [ "$(python3 cenas_hash.py $ID 2>/dev/null | grep -v '^global')" = "$(cat stories/$ID/storyboard.cenas)" ]; then echo "$H" > stories/$ID/storyboard.hash; echo "so' a ferramenta mudou (nenhuma cena): o storyboard olhado continua valendo"; fi; fi
[ "$(cat stories/$ID/storyboard.hash 2>/dev/null)" = "$H" ] || { echo "o storyboard e' de uma versao ANTIGA das folhas: gere de novo (rm stories/$ID/storyboard.jpg e relance a fila)"; exit 1; }
if [ ! -f stories/$ID/grade_acoes.jpg ] || [ stories/$ID/grade_acoes.jpg -ot stories/$ID/storyboard.jpg ]; then echo "FALTA A GRADE DE ACOES: ./prechecar.sh $ID acoes  (1 quadro no INSTANTE de cada acao da folha 3) e OLHE cada quadro: a acao escrita embaixo esta acontecendo?"; exit 1; fi
python3 - "$ID" <<'PYR' || exit 1
# REVISAO ESCRITA OBRIGATORIA (ordem do Gibson 19/11: toda sessao revisa e corrige como a principal). stories/<id>/revisao_storyboard.md,
# feita DEPOIS do storyboard atual, com UMA linha por frase: "bN: OK - <o que aparece na tela nessa frase>" ou "bN: CORRIGIDO - <defeito> -> <correcao>".
# Cada linha precisa citar algo da propria frase (palavra da narracao) e ter 8+ palavras: aprovar "no olho" sem comparar frase por frase nao passa.
import json, os, re, sys, unicodedata
i = sys.argv[1]; R = f'stories/{i}/revisao_storyboard.md'; SB = f'stories/{i}/storyboard.jpg'
n = lambda t: unicodedata.normalize('NFKD', t.lower()).encode('ascii', 'ignore').decode()
if not os.path.exists(R) or os.path.getmtime(R) < os.path.getmtime(SB):
    print(f'FALTA A REVISAO ESCRITA: abra {SB}, compare frase por frase com stories/{i}/folha3_acao.md e escreva {R} (uma linha por frase: "bN: OK - o que aparece" ou "bN: CORRIGIDO - defeito -> correcao"). Achou defeito? CORRIJA antes (regra mestra).'); sys.exit(1)
B = json.load(open(f'videos/{i}/beats.json'))['beats']; L = {}
for ln in open(R):
    m = re.match(r'\s*[-*]?\s*b(\d+)\s*[:\-]\s*(.+)', ln)
    if m: L[int(m.group(1))] = m.group(2)
falta = []
for k, b in enumerate(B):
    t = L.get(k)
    if not t: falta.append(f'b{k}: sem linha'); continue
    pal = {w for w in re.findall(r'[a-z]{5,}', n(b['say']))}
    if len(t.split()) < 8 or not (pal & set(re.findall(r'[a-z]{5,}', n(t)))): falta.append(f'b{k}: linha curta ou sem citar nada da frase')
    elif re.search(r'pendente|a corrigir|vou corrigir|defeito(?!.*->)', n(t)) and 'corrigido' not in n(t): falta.append(f'b{k}: defeito sem correcao (regra mestra: corrija antes de aprovar)')
# OLHAR IGUAL A PRINCIPAL (ordem do Gibson 24/11, COMO_OLHAR.md): a revisao tem de mostrar que o quadro foi comparado com a PESQUISA e que os defeitos foram PROCURADOS
txt = n(open(R, encoding='utf-8').read())
mp = re.search(r'^\s*pesquisa\s*:\s*(.+)$', txt, re.M)
if os.path.exists(f'referencias/{i}/moodboard.jpg') and not (mp and len(mp.group(1).split()) >= 10): falta.append('falta a linha "pesquisa: ..." (10+ palavras: o que o quadro de referencias referencias/%s/moodboard.jpg estabelece e o que voce comparou)' % i)
md = re.search(r'^\s*defeitos procurados\s*:\s*(.+)$', txt, re.M)
_k = [k for k in ('cenario', 'epoca', 'tamanho', 'cortado', 'multidao', 'legenda', 'acao', 'objeto') if md and k in md.group(1)]
if len(_k) < 8: falta.append('falta a linha "defeitos procurados: ..." respondendo os 8 itens (cenario, epoca, tamanho, cortado, multidao, legenda, acao, objeto) -- veja COMO_OLHAR.md')
if falta: print('REVISAO INCOMPLETA:', '; '.join(falta[:8])); sys.exit(1)
print(f'revisao escrita OK ({len(B)} frases conferidas)')
PYR
echo "$H" > stories/$ID/STORYBOARD_OK; rm -f stories/$ID/AGUARDA_STORYBOARD; echo "STORYBOARD APROVADO: $ID ($H). A fila renderiza na proxima volta."
