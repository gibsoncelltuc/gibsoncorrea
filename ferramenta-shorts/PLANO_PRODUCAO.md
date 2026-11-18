# PLANO DE PRODUÇÃO (pedido do Gibson) — quem faz o quê

Regra: cada sessão trabalha no SEU branch e só nos ids da sua lista. Antes de cada vídeo: `git fetch origin claude/bold-sagan-dskrsj && git merge --no-edit -X theirs FETCH_HEAD` (ferramenta mais nova). Seguir `OPERACAO.md` do passo 1 ao 7 em TODO vídeo (duas folhas, 0 risco, conferir, olhar a folha de contato, entregar em `entregas/<id>/`, commit + push, avisar a sessão principal com send_message). Um vídeo de cada vez. Marque aqui `[x]` ao entregar.

## Sessão principal (branch claude/bold-sagan-dskrsj)
Refazer com a ferramenta atual e as duas folhas (`./refazer_tudo.sh <id>` depois de zerar os riscos da folha 2):
- [x] EP 06 porco1859 · [x] EP 04 balde1325 · [x] EP 07 bolos1838 · [x] EP 01 karansebes · [x] EP 03 toledo1835 · [x] EP 08 zanzibar1896
- [x] EP 02 emus1932 — folha 2 acusa 6 riscos (emu fora de cena em b3/b9, "montou", sem mapa, herói errado: ponha `"heroi": null` ou modele; corrigir o beats.json)
- [x] EP 05 gansos390 — 7 riscos (cachorro sem modelo: modelar ou tirar; "dormiam/escalaram"; sem herói: use o ganso/galinha; 2 palavras sem efeito)
Depois: Curiosidade e Ciência CC 11–20.

## Sessão A (branch claude/prod-a-karansebes) — Guerras Inusitadas
- [x] EP 09 futebol1969
- [x] EP 11 A Guerra da Lagosta (Brasil × França, 1961) · [x] EP 12 A Guerra da Orelha de Jenkins (1739) · [x] EP 13 A Guerra do Banquinho Dourado (1900) · [x] EP 14 A Guerra de 335 Anos (ilhas Scilly) · [x] EP 15 A Guerra do Bacalhau (Islândia × Reino Unido)
- [x] EP 16 A Guerra da Melancia (Panamá, 1856) · [x] EP 17 A Guerra do Uísque (ilha Hans, Canadá × Dinamarca; cenário `arctic`) · [ ] EP 18 A Guerra do Cão Fugitivo (Grécia × Bulgária, 1925) · [ ] EP 19 A Guerra de Aroostook (lenhadores, 1838) · [ ] EP 20 A Batalha de Los Angeles (1942, atiraram no nada)

## Sessão B (branch claude/prod-b-emus) — Curiosidade e Ciência (`"serie": "Curiosidade e Ciência", "ep": N`)
- [x] EP 10 chaleira1784
- [x] CC 01 Newton e a maçã · [ ] CC 02 Arquimedes e o "Eureca" na banheira · [x] CC 03 Galileu e a torre de Pisa · [x] CC 04 Fleming e o mofo que virou penicilina · [x] CC 05 O micro-ondas e o chocolate derretido
- [x] CC 06 Pasteur e a vacina da raiva · [x] CC 07 Franklin, a pipa e o raio · [x] CC 08 Darwin e os tentilhões · [x] CC 09 Mendel e as ervilhas · [ ] CC 10 Eratóstenes mede a Terra com uma sombra

## Curiosidade e Ciência CC 11–20 (sessão principal, depois das refações)
CC 11 Röntgen e o raio X da mão · CC 12 Tycho Brahe e o nariz de metal · CC 13 Semmelweis e lavar as mãos · CC 14 Kekulé e o sonho da cobra · CC 15 O post-it (a cola que não colava) · CC 16 O velcro e os carrapichos · CC 17 Goodyear e a borracha no fogão · CC 18 Os Montgolfier, o balão, a ovelha, o pato e o galo · CC 19 Marie Curie e o caderno radioativo · CC 20 A dança das abelhas
Entregues: CC 11 ✔ · CC 12 ✔ · CC 13 ✔ · CC 14 ✔ · CC 15 ✔ · CC 16 ✔ · CC 17 ✔ · CC 18 ✔ · CC 19 ✔ · CC 20 ✔ (série completa)

## Notas para os roteiros novos
- Fatos reais: confira data, lugar e nomes antes de escrever (se não tiver certeza de um detalhe, não afirme). Personagens desenhados são originais (bonecos), sem imitar pessoa real.
- 150–170 palavras, 10–11 cenas, gancho na 1ª frase, "Acontece que" na virada, piada curta no fecho (ver `MODO_RICKS.md`).
- Série de ciência: sem batalha. Os 2 grandes momentos são a descoberta/virada em plano aberto com gente reagindo (`"impact": true` + `crowd`), com efeito e som. Objeto herói = o objeto da descoberta (maçã, banheira, pipa...): quase todos precisam ser MODELADOS antes (passo 4 do `OPERACAO.md`), e depois `python3 capacidades.py`.
- Seguir o roteiro à risca: cada coisa citada tem que aparecer (linha CONFERIR da folha 2).
- Animal sem modelo (cachorro, cavalo, abelha, pássaro pousado...): modelar no estilo de `web/animals2d.js` ou contar a cena sem depender dele.

## Série 3 — "Poder e Fama" (Trump, Bukele, Elon Musk) — 20 vídeos, DEPOIS das listas acima
Ler `FIGURINOS_FAMOSOS.md` (figurinos prontos e REGRAS obrigatórias: só fato real conferido, sem fala inventada, tom de curiosidade). `"serie": "Poder e Fama", "ep": N`.
- Sessão A: PF 01–07 · Sessão B: PF 08–14 · Sessão principal: PF 15–20. Cada sessão escolhe os temas da lista de ideias do `FIGURINOS_FAMOSOS.md` (ou outros fatos conferidos), sem repetir: anote aqui o tema escolhido antes de começar.
- Sessão principal escolheu (fora da lista de ideias, para não repetir): PF 15 = Trump na WrestleMania 23 (2007) · PF 16 = os braços que pegam o foguete no ar (Starship, 2024) · PF 17 = Bukele e o bitcoin minerado com vulcão (2021) · PF 18 = Trump: The Game, o jogo de tabuleiro (1989) · PF 19 = o macaco da Neuralink que jogou Pong com a mente (2021) · PF 20 = Tesla e a tequila (Teslaquila, 2020).
- Sessão principal, pacote "5 maiores histórias de cada um" (pedido do Gibson): PF 21 reeleição de Trump 2024 · PF 22 captura de Maduro (Força Delta, 2026) · PF 23 Martelo da Meia-Noite (B-2 no Irã, 2025) · PF 24 Falcon 9 pousa de ré (2015) · PF 25 Roadster que pula carros (2026) · PF 26 Bukele reeleito com 84,6% (2024) · PF 27 CECOT, a mega-prisão (2023) · PF 28 selfie de Bukele na ONU (2019). NÃO repetir estes temas.
- Divisão do render: os 8 do pacote (PF 21–28) foram passados para a sessão B produzir (18/11, 18:45).

## Série 4 — "E Se" (What If) — 10 roteiros PRONTOS, fora da fila (aguardando ordem do Gibson)
Ver `videos/E_SE_ROTEIROS.md`. Produzir com `./prechecar.sh <id>` e `./novo_video.sh <id>` só quando o Gibson mandar, depois de terminar a fila atual.
- Ordem do Gibson (18/11 ~21h): os "E Se" SÓ começam depois que a fila principal terminar os 11 refeitos (Cachorro, Aroostook, Los Angeles, Eratóstenes, Roadster, Bitcoin, Pia, Cybertruck, Lança-chamas, O Aprendiz, PayPal). Divisão quando liberar: sessão A = ese_pulo, ese_humanos, ese_holanda, ese_internet, ese_sono · sessão B (depois dos PF 22–28) = ese_dinheiro, ese_lua, ese_napoleao, ese_buraco, ese_titanic.

## Série 5 — "Histórias Incríveis" (histórias reais emocionantes) — CATALOGADA, para depois
Ver `videos/CATALOGO_HISTORIAS_EMOCIONANTES.md` (20 ideias com gancho, virada e objetos). Só produzir quando o Gibson mandar, depois dos "E Se".

## Séries 6 e 7 — "Como Funciona" e "Histórias de Empresas" — CATALOGADAS, para depois
Ver `videos/CATALOGO_COMO_FUNCIONA_E_EMPRESAS.md` (15 temas técnicos + 10 empresas). Estratégia do Gibson: tudo começa como short de 60 s; os que performarem viram versão de 3–5 min. "Como Funciona" vai precisar de modelos 3D em corte (Blender) quando começar.
