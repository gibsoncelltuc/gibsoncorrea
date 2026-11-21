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

# DEVOLUCAO DA PRINCIPAL (21/11 09:25) - SESSAO B
martelo2025 (PF 23) REPROVADO: (1) o B-2 (objeto heroi, vehicles/airplane ou kit equivalente) aparece so' como SOMBRA ACHATADA e minuscula no topo do quadro (0-30 s): ponha o bombardeiro em escala real (props 4o numero ~4, z ~ -6) com CLOSE de camera (detalhe: true numa cena sem personagem na frente) no inicio e na cena "decolaram do Missouri"; (2) clarao de FUZIL e soldado atirando em "antibunker" (21 s) e "bomba gigante" (66 s): a historia e' de BOMBARDEIROS, ninguem atira de fuzil. Tire "rifle" dos figurinos (use oficial de farda sem rifle) e ponha "tiros": false nas cenas de tropa; o som/efeito de bomba so' na frase que solta as bombas. Confira os quadros em 21 s, 24 s e 66 s.
Obrigado pelo ritmo: ja entreguei 24 videos ao Gibson. Continue: aroostook, cachorro, paypal, gansos, depois pia.

# DEVOLUCAO DA PRINCIPAL (21/11 09:55)
ENTREGUES AO GIBSON (parabens, ficaram bons): bukele2024, bitcoin2021, aprendiz2004 (A) | gansos390, aroostook1838, paypal2002 (B).
SESSAO B - pia2022 (PF 10) REPROVADO: o objeto heroi (a PIA, kit/sink) aparece PEQUENO e CORTADO na beira direita do quadro (0-5 s e 34 s), sem close. Ponha a pia em escala real (props 4o numero ~2,5) no centro-fundo (x ~ 1,5; z ~ -2) e use "detalhe": true numa cena de 8+ palavras com a pia em props (b0 ou b3). Confira os quadros em 1 s, 5 s e 34 s.
SESSAO A - ese_buraco: NAO produzir "E Se" (pausada por ordem do Gibson). Nao enviar mais nada dessa serie.

# ORDEM DO GIBSON (21/11 13:40) - VALE PARA TODO VIDEO, ACIMA DE TUDO
O QUE A NARRACAO CONTA TEM QUE APARECER NA TELA, FRASE POR FRASE. A folha 3 "0 faltando" NAO prova isso: ela so' conta as acoes que a ferramenta ja reconhecia, e verbo/animal/lugar desconhecido ficava invisivel (Paris saiu com 6 de 9 cenas vazias; Futebol sem campo, sem time, sem gol; Cybertruck sem a esfera voando na janela e sem palco).
NOVO PORTAO: `python3 auditar_narracao.py <id>` (gera stories/<id>/auditoria_narracao.md). `./aprovar_storyboard.sh` agora RECUSA enquanto houver cena com lacuna.
COMO ENCENAR (beats.json), exemplos prontos em videos/paris1870/beats.json:
- "comeram os cavalos": mesa `["mk/Table_Large",0,2.6,1.8]` NA FRENTE das pessoas + animais EM CIMA `"animals":[["horse",-1.0,2.6,"stand",0.3,1.55]]` (6o numero = altura) + `"acao":"comer","humanos_comem":true` (todos levam a comida a boca). Prato `["mk/Table_Plate",x,2.6,2.0,{"y":1.55}]`, rato `["kit/rato",x,2.6,2.0,{"y":1.6,"fixo":true}]`.
- "cercou/sitiou": `"shot":"reveal","crowd":{"n":22,"outfits":["ALE"],"march":true}` com soldados da epoca atras da cidade.
- objeto que VOA ate o alvo (esfera na janela, pombos, bola): `"voa":[{"asset":"kit/steel_ball","de":[x,z],"para":[x,z],"y":1.7,"alvo_y":1.6,"arco":0.9,"palavra":"^jogou","dur":22,"s":0.5,"som":"thump"}]`.
- lugar narrado que nao e' `set` (zoologico, restaurante, palco): monte com props (cerca, jaulas `mk/Cage_Small`, mesa) + `text`.
- animal que a ferramenta poe sozinho e tampa a cena (elefante gigante no restaurante): `"animais": false` ou ponha `"animals"` na mao com escala pequena.
- NOVOS MODELOS: kit/rato, kit/trave (gol), kit/turbina. Objeto sem modelo: MODELE no Blender (blender/objetos_processo.py), nao deixe so' no letreiro.
CADA CENA: abra o quadro (`./prechecar.sh <id> bN 4`) e compare com a FRASE. "Parece certo" nao basta: o que a frase diz esta na imagem?
VIDEOS JA ENTREGUES: o Gibson viu que varios NAO seguem a narracao. Todo video seu entregue sera REFEITO. Ordem de prioridade: rode `python3 auditar_narracao.py --todos`, refaca primeiro os de menor %.

# NOVO 21/11 (Gibson): 2 A 3 TAKES DE AMPLITUDE EM TODO VIDEO
Tipo de plano novo `"shot": "aereo"` = vista de CIMA do cenario inteiro (estadio todo, porto, cidade), camera alta descendo e girando. O diretor agora exige 3 planos abertos (video com 8+ cenas) e poe 1 `aereo` sozinho; em historia com lugar marcante (estadio, porto, campo de batalha) ponha `aereo` na mao na cena que apresenta o lugar (ex.: videos/futebol1969 b2 e b6, com `crowd`).

# 21/11: o set 'stadium' agora tem CAMPO DE FUTEBOL de verdade (gramado listrado, linhas oficiais, circulo central, areas, penalti, 2 gols em x=+-40); o plano 'aereo' olha o campo no sentido do comprimento (vertical). Nao ponha kit/trave perto dos jogadores no stadium: os gols reais ja estao nas pontas (so' use kit/trave em plano fechado do gol).

# 21/11: animais 3D mantem a COR NATURAL em qualquer luz (interior, noite, sombra); elefante sempre cinza claro (web/core.js, _ANIM3D). Vale para todo video, sem mexer no roteiro.

# 21/11 MODO DE ACAO DEFINITIVO (Gibson)
Leia MODO_DE_ACAO_DEFINITIVO.md. Novo gate `python3 verificar_modo_acao.py <id>` (R2.1 toda frase com acao visual; R4 max 4 personagens em cena fechada; R5 batalha em plano aberto; R4.1 negacao nao gera tiro) alem do auditar_narracao.py. Frase so' de comentario ('Nunca um doce custou tao caro.') e' proibida: reescreva com acao (ex.: '...e o confeiteiro contou as moedas').
