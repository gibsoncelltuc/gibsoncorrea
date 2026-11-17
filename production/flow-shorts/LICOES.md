
## Clipes refeitos (17/11): tudo certo
- Os 6 clipes novos do Ep. 1 (1080p) passaram na varredura a cada 0,5 s: 2 orelhas caídas em todos os quadros.
- Pasta `ep01-v2/` = clipes novos na ordem V01-1..6 (refrão, bocejo e pasta, escovando, Docinhos dançando, Docinhos indo embora, enxágue e joinha).
- Edição: `tools/montar_edicao.py ep01_edicao_60s.json` (várias tomadas por seção, reenquadramentos, transições, whoosh, legendas em inglês ancoradas embaixo).
- Limite do teste: a varredura é amostral (a cada 0,5 s); um erro que dura menos de meio segundo pode passar. Sempre assistir o vídeo final inteiro.

## Ep. 2 (17/11): montado
- Os 6 clipes chegaram fora de ordem (nomes de arquivo sem número). Ordem definida pelo CONTEÚDO: bagunça/Bento surpreso (1), porta (2), guardar brinquedos na caixa (3), abraço no ursinho (4), Tico acha a bola (5), passar a bola e acenar (6). Pasta `ep02-clips/V02-1..6`.
- Clipe da porta: o Bento deixa uma orelha em pé por ~4 s (3,5 a 7,5 s). Escondido na edição com um zoom no Tico (zoom 1.8 ancorado à esquerda).
- Música: 3 sementes testadas; semente 41 venceu (letra 0,92; blocos com 0,4 s de desvio). Semente 23: 0,76 (3 blocos fora). Seed 77 interrompida.
- Edição: `tools/montar_edicao.py ep02_edicao_60s.json`.
