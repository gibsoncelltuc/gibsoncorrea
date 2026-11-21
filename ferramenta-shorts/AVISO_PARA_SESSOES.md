# AVISO DA PRINCIPAL (20/11 22:55) - leia no proximo sync
1) SESSAO A: bukele2024 (PF 26) REPROVADO na conferencia quadro a quadro: El Salvador saia com predios de tijolo vermelho de Nova York (o motor lia "America Central" como EUA). Motor corrigido (mkvideo.py, _REG_PAIS): agora usa predios coloniais. Faca: `rm -f stories/bukele2024/{DONE,STORYBOARD_OK,AUTO_APROVADO,storyboard.jpg}; rm -rf ckpt/bukele2024 out/bukele2024/frames`, rode `python3 mkvideo.py bukele2024`, revise o storyboard novo (revisao escrita) e refaca. Procure o mesmo defeito em outros videos de America Latina da sua fila (cecot2023 saiu certo).
2) TODAS: a principal so confere videos ENVIADOS HOJE (apos 17:05Z). Videos AUTO_APROVADO (aprendiz2004, futebol1969, lancachamas2018, reeleicao2024, abelhas1945, kekule1865) precisam de revisao quadro a quadro de VOCES antes de enviar (conferir.sh + auditar_acoes.sh); sem isso a principal devolve.
3) canhao/artilharia "apontados" = parado, sem tiro nem explosao (motor corrigido). Corpo caido fica sobre o chao (motor corrigido).

# DEVOLUCAO DA PRINCIPAL (21/11 00:35) - SESSAO B
Balde (EP04) e Bolos (EP07): APROVADOS e entregues ao Gibson.
REPROVADOS (corrijam o beats.json, gerem storyboard novo, revisem e reenviem; o sha novo chega como NOVO):
- aroostook1838, cena final do porco "Feijao" (48-51 s): o porco fica CORTADO pela borda do quadro e tem uma faixa branca estranha embaixo dele. Reenquadre (porco inteiro no quadro) e confira o quadro em 49,5 s e 51 s.
- cachorro1925, cenas do soldado com o cachorro (13-22 s): o cachorro se sobrepoe ao 2o soldado e parece que ele CAVALGA o cachorro. Afaste os dois (cachorro ao lado, nao na frente do corpo) e confira os quadros em 14,5 s, 19,5 s e 21,5 s.

# DEVOLUCAO DA PRINCIPAL (21/11 00:45) - SESSAO A
bukele2024 segue pendente (ver aviso anterior). cecot2023 entregue.
REPROVADOS (corrijam o beats.json, storyboard novo, revisao escrita, reenviem):
- aprendiz2004 (PF 13), 49-52 s "No Brasil, no mesmo ano...": a cena do Brasil sai com predios de tijolo e arranha-ceu de Nova York. Ponha "regiao": "colonial" (ou "marco") na cena do Brasil / "set" diferente e confira o quadro em 50 s. E o close da barraca de limonada (21 s) vira um BLOCO marrom ilegivel: tire "detalhe" dessa cena ou afaste a barraca (props mais para tras) e confira o quadro em 21 s.
- cybertruck2019 (PF 11): objeto heroi (Cybertruck) so aparece pequeno ao fundo ou atras dos personagens, NUNCA em close. Ponha o carro em escala real (~3 bonecos de comprimento) no inicio com close de camera (detalhe: true numa cena com o carro em props, z perto de -2), e outro close no fim. Confira quadros em 1 s e 40 s.
Lembrete: escala real de objeto heroi (balao, carro, foguete, torre) e close nele.

# DEVOLUCAO DA PRINCIPAL (21/11 03:15)
SESSAO A - lancachamas2018 (PF 12) REPROVADO: (1) o lanca-chamas (objeto heroi, kit/flamethrower) NUNCA aparece: ponha em props com escala real (~1 boneco) e close de camera (detalhe) no inicio e no fim; (2) a Californa sai com predios de tijolo de Nova York: use "regiao" propria ou "marco" (Hollywood) e confira o quadro em 1 s e 25 s.
SESSAO B - paypal2002 (PF 14) REPROVADO: (1) o Roadster vermelho aparece PEQUENO como brinquedo (18-24 s): escala real, ~3 bonecos de comprimento (props 4o numero ~3), conferir quadros em 19 s e 22 s; (2) as moedas ficam GIGANTES, do tamanho dos personagens: reduza a escala do kit/coin (<=0,5) ou tire; (3) cenario repete rua/casa em quase todas as cenas: variar.
SESSAO B - gansos390 (EP 05) REPROVADO: ERRO DE EPOCA grave. Roma 390 a.C. com soldados de CASACA VERMELHA e cinturao cruzado (farda do seculo XIX). Use figurino da epoca: tunica, couraca/capacete de bronze (hat: helmet), sem "rifle", sem casaca; "regiao": "classico". Confira o quadro em 5 s e 45 s.
REGRA GERAL (Gibson, 20/11): roupas, fardas e objetos TEM que ser da epoca da historia; escala real de carro/aviao/foguete/torre/balao.

# DEVOLUCAO DA PRINCIPAL (21/11 05:10) - SESSAO A
Entregues ao Gibson: zanzibar1896, emus1932, chaleira1784, roadsterpulo2026, maduro2026. Obrigado, ficaram bons.
REPROVADO: bitcoin2021 (PF 09): El Salvador (mapa certo) mas as cenas de rua saem com PREDIOS DE TIJOLO DE NOVA YORK (0-10 s e 39-42 s). E o mesmo defeito do bukele2024. O motor ja foi corrigido na principal (america central = predios coloniais): faca `git fetch origin claude/serene-dirac-ckwlt5 && git merge -X theirs FETCH_HEAD`, `python3 mkvideo.py bitcoin2021`, confira `grep -o "rg_[a-z_0-9]*" stories/bitcoin2021/spec.js | sort | uniq -c` (tem que sair rg_colonial_*), gere storyboard novo, revise e reenvie. Faca o mesmo para bukele2024 (pendente desde 20/11).
Ainda nao conferi bacalhau1958 (avulso): confira voce quadro a quadro antes de eu olhar.
