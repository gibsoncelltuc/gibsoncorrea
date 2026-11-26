#!/usr/bin/env bash
# REVISAO FINAL FRASE A FRASE (ordem do Gibson 24/11): vale para a principal E para as sessoes A/B, sem excecao.
# 1) gera out/<id>/frase_a_frase.jpg (1 quadro do mp4 no meio de cada frase, com a frase escrita)
# 2) quem revisou ABRE a imagem (Read) e escreve stories/<id>/revisao_final.md: uma linha por frase
#    "fN: OK - <o que aparece, citando palavra da frase>"  ou  "fN: CORRIGIDO - <defeito> -> <correcao>" (e refaz o video antes)
#    + "gancho: <o que prende nos 5 primeiros segundos>"  + "piloto: <comparado com o Roadster EP25: mesmo nivel>"
# 3) sem revisao valida o video NAO e' entregue nem enviado a principal (enviar_para_principal.sh e entrega da principal checam).
# uso: bash revisao_final.sh <id>          (gera a imagem e valida a revisao, se existir)
cd "$(dirname "$0")"; ID="${1:?id}"
M=$(ls -t out/$ID/*.mp4 2>/dev/null | grep -v trecho | head -1); [ -f "$M" ] || { echo "sem mp4 em out/$ID"; exit 1; }
[ out/$ID/frase_a_frase.jpg -nt "$M" ] || bash frase_a_frase.sh none $ID "$PWD/$M" "$PWD/out/$ID/frase_a_frase.jpg" >/dev/null
echo "ABRA E OLHE: out/$ID/frase_a_frase.jpg"
python3 - "$ID" "$M" <<'PY'
import json, sys, re, os, unicodedata
i, m = sys.argv[1], sys.argv[2]
n = lambda s: unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode()
P = json.load(open(f'stories/{i}/work/phrases.json'))['phrases']; f = f'stories/{i}/revisao_final.md'
if not os.path.exists(f) or os.path.getmtime(f) < os.path.getmtime(m):
    print(f'FALTA REVISAO: escreva {f} (uma linha por frase f0..f{len(P)-1}, linha gancho: e linha piloto:) DEPOIS de olhar a imagem'); sys.exit(1)
T = open(f).read(); L = {int(a): b for a, b in re.findall(r'^f(\d+):\s*(.+)$', T, re.M)}; err = []
for k, p in enumerate(P):
    l = L.get(k, '')
    pal = [w for w in re.findall(r'[a-z]{4,}', n(p['text']))]
    if len(l) < 20 or not (l.startswith(('OK', 'CORRIGIDO'))) or (pal and not any(w in n(l) for w in pal)): err.append(f'f{k} ("{p["text"][:40]}"): linha curta, sem OK/CORRIGIDO ou sem citar a frase')
for k_ in ('gancho:', 'piloto:'):
    if not re.search(r'^' + k_ + r'\s*\S.{15,}', T, re.M): err.append(f'falta a linha "{k_} ..."')
if err: print('REVISAO FINAL INCOMPLETA:\n  ' + '\n  '.join(err[:12])); sys.exit(1)
print(f'REVISAO FINAL OK ({len(P)} frases conferidas no video)')
PY
