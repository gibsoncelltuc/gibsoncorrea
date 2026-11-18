# Série "E Se" (What If) — 10 roteiros prontos (NÃO estão na fila)

Status: os 10 passaram no portão da ferramenta com **0 risco** (duas folhas geradas em `stories/<id>/`), ~57–64 s cada (voz real ≈ 2,65 palavras/s), fontes no campo `"fontes"` de cada `videos/<id>/beats.json` (saem na Folha 1).
**Para produzir quando o Gibson mandar:** `./prechecar.sh <id>` → olhar `stories/<id>/precheck.jpg` → `./novo_video.sh <id>`.

Estrutura usada em todos (estrutura validada da ferramenta): placa "E SE..." + pergunta no 1º segundo (gancho) → mapa → escalada de consequências → "Acontece que" (virada) → 2 grandes momentos em plano aberto com placa → objeto-herói em close no começo, no meio e no fim → fecho com frase de efeito/pergunta para comentário.

| # | id | Título | Gancho | Virada | Nota (viral) |
|---|----|--------|--------|--------|--------------|
| 1 | ese_pulo | E Se Todo Mundo Pulasse ao Mesmo Tempo? | 8 bilhões pulando: a Terra sai do lugar? | ela se mexe menos que um átomo; o problema é voltar pra casa | 9/10 |
| 2 | ese_humanos | E Se os Humanos Sumissem da Terra? | luzes apagando, cidades vazias | ruas viram floresta; pontes caem; pirâmides e plástico ficam | 9/10 |
| 3 | ese_holanda | E Se o Brasil Tivesse Sido Holandês? | um pedaço do Brasil foi holandês por 24 anos | Suriname fala holandês; a troca que deu Nova York aos ingleses | 10/10 (público BR) |
| 4 | ese_internet | E Se a Internet Acabasse por Um Dia? | e se caísse amanhã por 24 h? | pane de 2024 parou aeroportos; o pior seria não saber o que fazer com as mãos | 9/10 (comentários) |
| 5 | ese_sono | E Se Ninguém Precisasse Dormir? | +25 anos de vida acordado | Randy Gardner, 11 dias acordado; cérebro faz faxina dormindo | 8/10 |
| 6 | ese_dinheiro | E Se o Dinheiro Sumisse do Mundo? | sem nota, cartão nem conta | pedras gigantes de Yap; dinheiro é confiança | 8/10 |
| 7 | ese_lua | E Se a Lua Desaparecesse? | olhe para o céu hoje | marés, escuridão, eixo da Terra balançando | 9/10 |
| 8 | ese_napoleao | E Se Napoleão Tivesse Vencido em Waterloo? | uma tarde mudou a Europa | mesmo vencendo, provavelmente perderia | 7/10 |
| 9 | ese_buraco | E Se Você Cavasse até o Outro Lado da Terra? | o buraco até a China | sai no Pacífico perto do Japão; 40 minutos de queda | 10/10 |
| 10 | ese_titanic | E Se o Titanic Não Tivesse Afundado? | "impossível de afundar" afundou | o naufrágio criou as regras que salvaram milhares | 9/10 |

## Revisão individual (pontos fortes / fracos e o que foi refeito)
- **Pulo:** forte — pergunta absurda e curiosa, resposta surpreendente. Fraco: pouco "visual" no meio → reforcei com 2 multidões (pulo e "BUM!") e o globo em close.
- **Humanos:** forte — linha do tempo (1 dia, 2 dias, 20 anos, séculos) segura a retenção. Fraco inicial: "bombas" do metrô acendia explosão e cena parada → trocado por "máquinas", ação na cena. Animais (cachorro, gato, veado, lobo, coelho, raposa) entram em 3D.
- **Holanda:** forte — história real do Brasil + dois "plot twists" (Suriname e Nova York). Fraco inicial: cena longa e frase final com "batalhas" → reescritas.
- **Internet:** forte — fatos recentes (2021 e 2024), CTA no fim ("responde aí"). Fraco inicial: cena de 10 s → cortada.
- **Sono:** forte — número que choca (+25 anos), personagem real. Fraco inicial: 173 palavras (65 s) → enxugado.
- **Dinheiro:** forte — começa no cotidiano (padaria). Fraco inicial: "pão/pães" sem modelo 3D → reescrito; cenas enxugadas.
- **Lua:** forte — começa com convite ("olhe para o céu hoje"). Fraco inicial: 196 palavras (75 s) → cortado para 61 s.
- **Napoleão:** forte — virada inteligente. Fraco: tema menos popular para o público geral (nota 7) — mantido porque mistura batalha e "E se". Corrigido: água no cenário de campo (Santa Helena passa no porto), combate encenado.
- **Buraco:** forte — fantasia de infância + física surpreendente. Fraco inicial: 207 palavras (80 s) → cortado para 62 s.
- **Titanic:** forte — tema mundialmente conhecido + virada positiva. Fraco inicial: 202 palavras (78 s) → cortado para 62 s.

## Fatos conferidos (fontes no beats.json de cada um)
Jump (xkcd What If #8) · O Mundo Sem Nós (Alan Weisman) · Brasil Holandês 1630–1654, sinagoga Kahal Zur Israel, Tratado de Breda 1667 · pane CrowdStrike 19/07/2024 (~8,5 mi de PCs) e queda do Facebook 04/10/2021 (~6 h) · Randy Gardner 1964 (264 h) e limpeza do cérebro no sono (NIH) · pedras Rai de Yap · NASA/NOAA marés e afastamento da Lua (~3,8 cm/ano) · Waterloo 18/06/1815, Cem Dias · Poço de Kola (12,2 km), antípoda do Brasil no Pacífico, túnel da gravidade (~42 min) · Titanic 1912, SOLAS 1914, Patrulha Internacional do Gelo.

## Modelos 3D novos para esta série
`kit/moon` (Lua com crateras), `kit/iceberg` (ponta fora d'água, base gigante submersa). O resto usa a biblioteca (globo, celular, moeda, coroa, chaleira, bandeira, pá, animais, árvores, navio, ponte, arranha-céu).
