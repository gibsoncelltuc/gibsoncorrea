"""youtube_txt.py <id> -> stories/<id>/youtube.txt (titulo, descricao, fontes, tags) e stories/<id>/roteiro.txt (narracao limpa)"""
import json, sys, re
ID = sys.argv[1]; B = json.load(open(f'videos/{ID}/beats.json')); M = json.load(open(f'stories/{ID}/meta.json'))
serie, ep, tit = B.get('serie', ''), B.get('ep', ''), B.get('title', '')
fala = [b['say'].strip() for b in B['beats'] if b.get('say')]
gancho = fala[0] if fala else ''
fontes = B.get('fontes', [])
tags = {'Guerras Inusitadas': '#historia #guerra #curiosidades #shorts #animacao',
        'Curiosidade e Ciência': '#ciencia #curiosidades #historia #shorts #animacao',
        'Poder e Fama': '#curiosidades #famosos #historia #shorts #animacao'}.get(serie, '#curiosidades #shorts #animacao')
d = [f"TÍTULO: {tit} | {serie} EP {ep:02d}" if isinstance(ep, int) else f"TÍTULO: {tit}", "",
     "DESCRIÇÃO:", gancho, "", ' '.join(fala[1:3]), "",
     f"Série {serie}, episódio {ep}. Inscreva-se para os próximos episódios!", ""]
if serie == 'Poder e Fama': d += ["Animação humorística. Personagens são caricaturas.", ""]
if fontes: d += ["Fontes:"] + [f"- {f}" for f in fontes] + [""]
d += [tags, "", "TAGS (separadas por vírgula):", ', '.join(t.strip('#') for t in tags.split()) + f", {serie.lower()}"]
open(f'stories/{ID}/youtube.txt', 'w').write('\n'.join(d) + '\n')
open(f'stories/{ID}/roteiro.txt', 'w').write(f"{serie} EP {ep} - {tit}\n\n" + '\n\n'.join(fala) + '\n')
print(f'stories/{ID}/youtube.txt')
