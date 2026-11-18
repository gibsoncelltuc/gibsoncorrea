#!/usr/bin/env python3
# usage: python3 capacidades.py  -> grava CAPACIDADES.md: tudo que a ferramenta TEM hoje (cenarios, planos, objetos, animais, expressoes, interacoes, sons). Rode depois de modelar algo novo.
import re, os, glob
src = open('mkvideo.py', encoding='utf-8').read(); aud = open('audio_story.py', encoding='utf-8').read(); tb = open('web/toonbase.js', encoding='utf-8').read()
sets = re.search(r"SETS_X = \{([^}]*)\}", src).group(1); sets = re.findall(r"'(\w+)':", sets)
obj = re.findall(r"\(r'([^']*)', '([^']*)', [\d.]+, (True|False|'in')\)", src)
import json as _j
for _f in sorted(glob.glob('obj_dict.d/*.json')):
    try: obj += [(e[0], e[1], str(e[3]) if len(e) > 3 and e[3] is True else 'False') for e in _j.load(open(_f, encoding='utf-8')) if not any(e[1] == o[1] for o in obj)]
    except Exception: pass
lib = {d: sorted(os.path.basename(f)[:-4] for f in glob.glob(f'web/assets/library/{d}/*.glb')) for d in ('kit', 'buildings', 'vehicles', 'nature', 'tools', 'war')}
faces = sorted(set(re.findall(r"^\s{4}(\w+): \{\s*\n\s*eye:", tb, re.M)) | set(re.findall(r"(\w+): \{ eye: \[", tb)))
held = re.search(r"drawHeld[^\n]*", tb); hats = sorted(set(re.findall(r"hat === ['\"](\w+)['\"]", tb)))
sfx = [n for n in re.findall(r"^def (\w+)\(t[,)]", aud, re.M) if n not in ('tt',)]
L = ['# CAPACIDADES DA FERRAMENTA (gerado por capacidades.py - nao edite a mao)', '', 'Escreva o roteiro usando SO o que esta aqui. O que nao estiver, a folha 2 acusa como risco.', '',
     '## Cenarios ("set" no topo ou na cena)', ', '.join(sets) + '  | interiores: "interior": "madeira" | "pedra" | "loja"', '',
     '## Planos ("shot")', 'two (medio, 2 pessoas) | close (rosto) | group (3-4, corpo inteiro) | low (camera baixa, virada) | track (andando) | ABERTOS: reveal (grua abrindo), crowd (multidao), orbit (camera girando)', '',
     '## Hora e clima', '"hora": dia | amanhecer | pordosol | noite ; "clima": limpo | chuva | tempestade | neve | neblina | calor (a ferramenta tambem le essas palavras na narracao)', '',
     '## Expressoes (3o campo do "who": "FAZ:0:angry")', ', '.join(faces), '',
     '## Acoes e interacoes', '"acao": conversar | discutir | comemorar | dancar | nenhuma ; "interacao": empurrar | discutir | cochichar | entregar | susto | reverencia | pular ; "chega": true (entra andando) ; "batalha": true (tropa, tiros, fuga) ; "caminhoes": true', '',
     '## Objeto na mao (4o campo do "who": "FAZ:0:stern:coin")', 'bottle, mug, paper, book, lantern, pitchfork, staff, flag, torch, bag, coin, spyglass, shovel, tulip, money (notas de dolar), sword (espada)', '',
     '## Chapeus ("hat" no figurino)', ', '.join(hats) or '-', '',
     '## Figurino (campos de "outfits")', 'jacket, pants, boots (obrigatorios) | hat + cap (cor) | hair (cor, com hat: hair) | hairStyle: long|bun | beard (cor) | glasses: true | tie (cor da gravata) | pele (tom de pele) | sash, belt, buttons (cor) | build: stout|lanky | rifle: true (soldado). Caricaturas prontas: FIGURINOS_FAMOSOS.md', '',
     '## Profissoes prontas ("profissao" no figurino: {"PAD": {"profissao": "padeiro"}} e ajuste as cores se quiser)', 'padeiro, agricultor, nobre, politico, empresario, rei, general, soldado, marinheiro, cientista, medico, comerciante, pescador, padre, camponesa, jornalista. Cada personagem ganha barba, bigode ou oculos proprios pelo nome + variante; para fixar: "beard": "#cor" | "moustache": "#cor" | "glasses": true/false. Bandeira na mao: "holdCol" e "holdCol2" no figurino mudam as duas cores.', '',
     '## Animais (JA PRONTOS - NUNCA modele animal no Blender)', 'Entram SOZINHOS quando a narracao cita o animal (cachorro, gato, vaca/boi, ovelha, cabra/bode, porco, cavalo, burro/jumento, veado/cervo, raposa, lobo, coelho, leao, elefante, urso, galinha, galo, pato, ganso, gaivota, emu). Em cena andando/correndo (shot "track") o animal anda junto. Para posicionar a mao: "animals": [["dog", x, z]] com dog, cat, cow, sheep, goat, pig, horse, donkey, deer, fox, wolf, rabbit, lion, elephant, bear, chicken, rooster, duck, goose, gull; "emus": true. Desligar: "animais": false. Close de animal como objeto heroi: kit/dog_sit (cachorro sentado).', '',
     '## Objetos que entram SOZINHOS quando a narracao cita a palavra', *[f'- {a}  <- {r}' + ('  (fundo, so cena externa)' if b == 'True' else '  (so interior)' if b == "'in'" else '') for r, a, b in obj], '',
     '## Biblioteca 3D completa (use em "props": [["pasta/nome", x, z, escala]])', *[f'- {d}: {", ".join(v)}' for d, v in lib.items()], '- soltos: barrel, crate, cannon, ship', '',
     '## Sons ("sfx": ["nome@quadro"])', ', '.join(sfx), '',
     '## NAO existe (nao escreva cena que dependa disto)', 'nadar, cavalgar, escalar, sentar, deitar (mostre o resultado ou reescreva a frase); personagem dentro de veiculo aparecendo; mais de 4 personagens principais na mesma cena fechada.']
open('CAPACIDADES.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('CAPACIDADES.md:', len(obj), 'objetos automaticos,', sum(len(v) for v in lib.values()), 'modelos,', len(faces), 'expressoes,', len(sfx), 'sons')
