# B_aroostook1838 — defeito da FERRAMENTA (negacao vira batalha)
- Frase: "...e ninguem morreu em combate." (cena b0, lenhadores). A palavra "combate" (mkvideo.py ~linha 823 e 2122) + "guerra" (IMPACT, linha 750) fez a ferramenta pôr ~40 soldados vermelhos e azuis misturados atras dos lenhadores, mesmo com "batalha": false e crowd n=0 no beat. Negacao ("ninguem morreu em combate") nao e' combate.
- Contornei no roteiro (troquei a palavra por "ninguem foi morto pelo inimigo" e "impact": false), mas qualquer roteiro de guerra sem luta com "sem combate/nenhum combate" sofre o mesmo.
- Pedido: no gerador, ignorar combate/batalha/lutaram precedidos de negacao (nao/nunca/nenhum/ninguem/sem) e respeitar "crowd": {"n": 0} do beat.

# 2) Voz nao e' refeita quando o texto do roteiro muda (24/11)
- Mudei a 1a frase do roteiro depois da primeira geracao da voz: o stage "voice" ficou marcado como feito e o voice.mp3 (03:11) e script_one.txt continuaram com o texto ANTIGO ("ninguem morreu em combate"), enquanto script.txt ja tinha o novo. O video renderizou com a voz e a legenda antigas (so' percebi na folha de contato do mp4).
- Pedido: invalidar stages/voice (e work/) quando o hash do texto narrado mudar (script.txt x script_one.txt). Contornei: rm stages/voice voice.mp3 work antes de renderizar.

# 3) Falta o hold "axe" (machado na mao) (24/11)
- "lenhadores cortavam as arvores": a acao 'corta' so' poe poeira + toras; o personagem nao segura machado (HOLDS do mkvideo.py: rifle, mug, bottle, paper, book, lantern, torch, flag, sword, money, coin, shovel, bag, spyglass, tulip). Contornei com o prop tools/axe ao lado do lenhador, mas o pedido e' um hold 'axe' (machado na mao com o golpe do corta).
