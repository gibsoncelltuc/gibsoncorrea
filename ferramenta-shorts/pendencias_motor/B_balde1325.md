# B_balde1325 — defeitos da FERRAMENTA no cenario "medieval" (1325)
- Quadros b0, b1, b6, b7 do storyboard: o set `medieval` mostra predios amarelos altos de 4 andares com muitas janelas iguais (parecem predio de apartamentos, que a FICHA proibe para 1325) e POSTE DE LAMPIAO de rua (lampiao e' proibido pela epoca e nao foi trocado). Fica em qualquer roteiro que use `medieval` antes de 1400.
- b5: cerca branca de madeira (tipo moderno de quintal) no campo ao lado do soldado caido.
- Contornei: cenas de campo/batalha em `loc_campo`; cidade (b0, b1, b7) ficou em `medieval` porque o roteiro cita as cidades.
- Pedido: set `medieval` com casas baixas de tijolo/pedra de 2 andares, sem poste de lampiao e sem cerca branca; ou bloquear `medieval` + lampiao quando o ano < 1500.
- Modelei `kit/balde_madeira` (blender/objetos_balde.py) porque o balde da biblioteca (`tools/bucket`) e' de metal cinza e o balde da pesquisa e' de madeira com aros de ferro.

# Estado final do video renderizado (24/11, depois das correcoes de roteiro)
- Restam, e sao do MOTOR: (1) predios amarelos altos + poste de lampiao nos quadros 0-6 s (set medieval); (2) cerca branca de quintal nos quadros de campo (b2 em 13-18 s e b5 em 34-37 s: o "loc_campo" poe essa cerca); (3) o balde heroi so' aparece grande a partir de 4,5 s (props na b0 ficam na borda).
- O roteiro esta com fatos conferidos (Wikipedia, Battle of Zappolino): balde levado como TROFEU depois da batalha (a historia do roubo previo e' lenda do poema La secchia rapita), 30 mil de Bolonha x menos de 8 mil de Modena, cerca de 2 mil mortos.
