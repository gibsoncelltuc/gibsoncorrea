# PLANO DE PRODUÇÃO (pedido do Gibson) — quem faz o quê

Regra: cada sessão trabalha no SEU branch e só nos ids da sua lista. Antes de cada vídeo: `git fetch origin claude/bold-sagan-dskrsj && git merge --no-edit -X theirs FETCH_HEAD` (ferramenta mais nova). Seguir `OPERACAO.md` do passo 1 ao 7 em TODO vídeo (duas folhas, 0 risco, conferir, olhar a folha de contato, entregar em `entregas/<id>/`, commit + push, avisar a sessão principal com send_message). Um vídeo de cada vez. Marque aqui `[x]` ao entregar.

## Sessão principal (branch claude/bold-sagan-dskrsj)
Refazer com a ferramenta atual e as duas folhas (`./refazer_tudo.sh <id>` depois de zerar os riscos da folha 2):
- [x] EP 06 porco1859 · [x] EP 04 balde1325 · [x] EP 07 bolos1838 · [x] EP 01 karansebes · [x] EP 03 toledo1835 · [x] EP 08 zanzibar1896
- [ ] EP 02 emus1932 — folha 2 acusa 6 riscos (emu fora de cena em b3/b9, "montou", sem mapa, herói errado: ponha `"heroi": null` ou modele; corrigir o beats.json)
- [ ] EP 05 gansos390 — 7 riscos (cachorro sem modelo: modelar ou tirar; "dormiam/escalaram"; sem herói: use o ganso/galinha; 2 palavras sem efeito)
Depois: Curiosidade e Ciência CC 11–20.

## Sessão A (branch claude/prod-a-karansebes) — Guerras Inusitadas
- [x] EP 09 futebol1969
- [x] EP 11 A Guerra da Lagosta (Brasil × França, 1961) · [ ] EP 12 A Guerra da Orelha de Jenkins (1739) · [ ] EP 13 A Guerra do Banquinho Dourado (1900) · [ ] EP 14 A Guerra de 335 Anos (ilhas Scilly) · [ ] EP 15 A Guerra do Bacalhau (Islândia × Reino Unido)
- [ ] EP 16 A Guerra da Melancia (Panamá, 1856) · [ ] EP 17 A Guerra do Uísque (ilha Hans, Canadá × Dinamarca; cenário `arctic`) · [ ] EP 18 A Guerra do Cão Fugitivo (Grécia × Bulgária, 1925) · [ ] EP 19 A Guerra de Aroostook (lenhadores, 1838) · [ ] EP 20 A Batalha de Los Angeles (1942, atiraram no nada)

## Sessão B (branch claude/prod-b-emus) — Curiosidade e Ciência (`"serie": "Curiosidade e Ciência", "ep": N`)
- [x] EP 10 chaleira1784
- [x] CC 01 Newton e a maçã · [ ] CC 02 Arquimedes e o "Eureca" na banheira · [x] CC 03 Galileu e a torre de Pisa · [x] CC 04 Fleming e o mofo que virou penicilina · [ ] CC 05 O micro-ondas e o chocolate derretido
- [ ] CC 06 Pasteur e a vacina da raiva · [ ] CC 07 Franklin, a pipa e o raio · [ ] CC 08 Darwin e os tentilhões · [ ] CC 09 Mendel e as ervilhas · [ ] CC 10 Eratóstenes mede a Terra com uma sombra

## Curiosidade e Ciência CC 11–20 (sessão principal, depois das refações)
CC 11 Röntgen e o raio X da mão · CC 12 Tycho Brahe e o nariz de metal · CC 13 Semmelweis e lavar as mãos · CC 14 Kekulé e o sonho da cobra · CC 15 O post-it (a cola que não colava) · CC 16 O velcro e os carrapichos · CC 17 Goodyear e a borracha no fogão · CC 18 Os Montgolfier, o balão, a ovelha, o pato e o galo · CC 19 Marie Curie e o caderno radioativo · CC 20 A dança das abelhas

## Notas para os roteiros novos
- Fatos reais: confira data, lugar e nomes antes de escrever (se não tiver certeza de um detalhe, não afirme). Personagens desenhados são originais (bonecos), sem imitar pessoa real.
- 150–170 palavras, 10–11 cenas, gancho na 1ª frase, "Acontece que" na virada, piada curta no fecho (ver `MODO_RICKS.md`).
- Série de ciência: sem batalha. Os 2 grandes momentos são a descoberta/virada em plano aberto com gente reagindo (`"impact": true` + `crowd`), com efeito e som. Objeto herói = o objeto da descoberta (maçã, banheira, pipa...): quase todos precisam ser MODELADOS antes (passo 4 do `OPERACAO.md`), e depois `python3 capacidades.py`.
- Seguir o roteiro à risca: cada coisa citada tem que aparecer (linha CONFERIR da folha 2).
- Animal sem modelo (cachorro, cavalo, abelha, pássaro pousado...): modelar no estilo de `web/animals2d.js` ou contar a cena sem depender dele.

## Série 3 — "Poder e Fama" (Trump, Bukele, Elon Musk) — 20 vídeos, DEPOIS das listas acima
Ler `FIGURINOS_FAMOSOS.md` (figurinos prontos e REGRAS obrigatórias: só fato real conferido, sem fala inventada, tom de curiosidade). `"serie": "Poder e Fama", "ep": N`.
- Sessão A: PF 01–07 · Sessão B: PF 08–14 · Sessão principal: PF 15–20. Cada sessão escolhe os temas da lista de ideias do `FIGURINOS_FAMOSOS.md` (ou outros fatos conferidos), sem repetir: anote aqui o tema escolhido antes de começar.
