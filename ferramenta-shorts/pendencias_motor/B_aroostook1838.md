# B_aroostook1838 — defeito da FERRAMENTA (negacao vira batalha)
- Frase: "...e ninguem morreu em combate." (cena b0, lenhadores). A palavra "combate" (mkvideo.py ~linha 823 e 2122) + "guerra" (IMPACT, linha 750) fez a ferramenta pôr ~40 soldados vermelhos e azuis misturados atras dos lenhadores, mesmo com "batalha": false e crowd n=0 no beat. Negacao ("ninguem morreu em combate") nao e' combate.
- Contornei no roteiro (troquei a palavra por "ninguem foi morto pelo inimigo" e "impact": false), mas qualquer roteiro de guerra sem luta com "sem combate/nenhum combate" sofre o mesmo.
- Pedido: no gerador, ignorar combate/batalha/lutaram precedidos de negacao (nao/nunca/nenhum/ninguem/sem) e respeitar "crowd": {"n": 0} do beat.
