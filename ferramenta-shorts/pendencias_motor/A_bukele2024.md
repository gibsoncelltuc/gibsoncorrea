# A_bukele2024 (24/11)
1. mkvideo.py linha ~162: regex hospital tem `leito` sem \b -> "eleitores" vira interior hospital (cena b8 "motivo mais citado pelos eleitores"). Corrigido no roteiro com interior:false, mas qualquer roteiro com "eleitores/eleitor" sofre. Usar \bleito\b.
2. mkvideo.py linha ~268: "el salvador|san salvador" poe kit/volcano em TODAS as cenas do video (aparece atras em eleicao/comemoracao/comente). Deveria so' entrar na cena que cita o lugar.
3. verificar_execucao: beat com set == set do video (apos v13 jungle->loc_campo) esperava X_loc_campo; contornei pondo set do video = loc_campo.
