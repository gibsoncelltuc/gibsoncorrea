
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

## Ep. 4 (18/11): montagem "cinema"
- Ordem dos clipes definida pelo CONTEÚDO (arquivos sem número): Luna com bolhas (1), Bento com carrinho (2), Luna lavando (3), os dois esfregando (4), toalha (5), maçãs (6).
- Faixa borrada embaixo (herdada das imagens 16:9 erradas) nos clipes 5 (até ~3,4 s) e 6 (até ~4,4 s). O detector automático SUBESTIMOU a faixa do clipe 6; conferir sempre olhando os quadros. Escondida na edição com reenquadramento (zoom 1.25 a 1.4 ancorado no topo).
- Música: 3 sementes tentadas; 23 venceu (letra 0,92). Semente 41 (primeira tentativa) cantou refrão errado e inverteu blocos (letra 0,59).
- Transição "zoomin" do ffmpeg deixa 1 quadro laranja em branco: NÃO usar. Usar dissolve/smoothleft/circleopen/fadewhite.
- Grade de cor: bloom só nas luzes fortes (curva de limiar) e correção quente mínima; a primeira versão deixou tudo estourado e amarelado.
- Ferramentas novas: tools/montar_cine.py (edição cinema), tools/legendas_auto.py (legendas em inglês no tempo cantado).
