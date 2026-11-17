# MODO RICKS — especificação medida e como usar (para qualquer modelo de IA)
Medido em 14 dos 20 shorts animados mais vistos do canal de referência (6,6 a 34 milhões de views; 48 quadros reais 1080x1920 + transcrições) e nos relatórios de 20 shorts do repositório claude-animated-shorts. Dados brutos: `ref_privado/` (fora do git). Histórias, personagens e frases são SEMPRE originais; copiamos técnica, não conteúdo.

## 1. Roteiro (a parte que mais pesa na retenção)
| Medida | Canal | Regra para os nossos roteiros (PT-BR) |
|---|---|---|
| Duração | mediana 65 s | 55–70 s |
| Ritmo da narração | 213 palavras/min, quase sem pausa | voz Antonio +10% ou mais; sem frase de enchimento |
| Gancho | termina em 3,8 s; 10–16 palavras | 1ª frase = paradoxo ou ação absurda contada como fato, com algo em jogo. NUNCA começar por data ("Em 1788...") |
| Frases | ~14 palavras | curtas, faladas, presente ou passado simples |
| Falas de personagem | 1–2 por vídeo | pelo menos 1 fala curta entre aspas (deboche, dúvida) |
| Estrutura | gancho → cenário em 1–2 frases → escalada (3–6 batidas, os outros riem/duvidam) → pergunta/mistério → virada ("Acontece que...") → explicação do mecanismo → final irônico curto | seguir nesta ordem |
| Final | última frase curta, fecha a ironia; o vídeo acaba na última palavra | sem "inscreva-se", sem resumo |
Verificador: `python3 roteiro_check.py <id>` (avisa o que foge da regra).

## 2. Imagem
| Medida | Canal | Nossa ferramenta (já aplicado) |
|---|---|---|
| Personagens por quadro | mediana 2 (máx. 5) | diretor limita multidão: 5–10 figurantes; no máx. 2 planos abertos por vídeo (`max_wide` no beats.json) |
| Altura do personagem principal | ~51% do quadro; cabeça ~29% da largura | planos mais fechados em `mkvideo.py` TEMPL (two 7→5,8 m; close 4,8→4; group 9→7,4) |
| Planos | médio/médio-aberto 70%, aberto 25%, close raro | idem |
| Legenda | 1–2 palavras, branca, contorno preto, centro em 70% da altura, letra ~2,8% da altura | `caps.py` (Inter Black 88 px em y=1338) |
| Desfoque de fundo | nenhum ou leve em 96% dos quadros | bloom e poeira reduzidos (`web/tail.js`, `web/weather.js`) |
| Cenário | próprio de cada história; interior em 1/3 dos quadros | **AINDA FALTA** (ver §4) |
| Câmera | quase sem corte seco; segura ~80% do tempo com leve aproximação; mudanças em "arrancadas" que desaceleram; fusões curtas | já existia (glide, push-in, fusão) |

## 3. Velocidade
Rasterizador Mesa llvmpipe no lugar do SwiftShader (`launch.mjs`, `RASTER=swiftshader` volta ao antigo): 0,47 s/quadro com 1 navegador (antes 1,92 s), imagem equivalente. A raea (motor do vídeo "5x mais rápido") foi analisada: o ganho dela vem de GPU; sem GPU o próprio projeto mede ~2 s/quadro em cena simples, e portar exigiria reescrever personagens e pós-processamento. Não adotada.

## 4. O que ainda NÃO está no nível do canal (honesto, atualizado)
Resolvido desde a última versão: interiores com parede perto (`interior` no beat), fachada automática ao ar livre, falas com boca mexendo, luz por cena, sombra lavanda, pernas/braços em tinta, abertura e final em plano médio, câmera na altura do personagem, roteiros no molde do canal.
Ainda falta:
1. **Variedade de personagem**: poucos chapéus e cabelos; figurino raso (sem estampa, cinto, detalhe).
2. **Objetos na mão e ações de corpo** (pegar, carregar, apontar com objeto); caminhada ainda dura.
3. **Texto em placas** da cena em vez de título flutuante.
4. **Cenário modelado por história** (navio, trem, fábrica): hoje só os 11 cenários + 3 interiores.
5. Áudio do canal não foi medido (sem acesso ao som).
Tabela completa ponto a ponto: `COMPARATIVO_RICKS.md`.
## 5. Como produzir um vídeo
1. Escreva `videos/<id>/beats.json` seguindo o §1 (copie um existente). 2. `python3 roteiro_check.py <id>`. 3. Ponha o id em `queue.txt`. 4. `bash run_queue.sh` (retomável; `bash status.sh` mostra o andamento). Saída: `out/<id>/<Titulo>.mp4` + `review_sheet.jpg`. Sempre olhar a folha de contato antes de publicar.

## 6. Auditorias fechadas em 17/11 (feitas direto nos 48 quadros reais dos 14 vídeos, sem agentes)
| Área | Canal (p10 / mediana / p90) | Nosso antes | O que mudou na ferramenta |
|---|---|---|---|
| Luminância média | 0,29 / 0,445 / 0,635 | 0,43 a 0,59 | mantida; contraste em S de 24% no passe final (`web/tail.js`) |
| Pixels muito escuros | 0,6% / 4,4% / 23% | 1,1% a 2,9% | mesmo ajuste de contraste (mais preto profundo) |
| Saturação | 0,33 / 0,44 / 0,59 | 0,39 a 0,47 | já batia; sem mudança |
| Nitidez | 0,035 / 0,062 / 0,108 | 0,050 a 0,054 | desfoque de lente a 60% (`DOF_K`), bloom e poeira reduzidos |
| Legenda | centro em 70,5% da altura; letra 2,8% | 70% ; ~2,9% | já batia; sem mudança |
| Animação | sem vídeo do canal para medir movimento; base = relatórios de terceiros | tremor entre quadros | tremor corrigido (semente fixa); boca mexe em falas entre aspas |
| Áudio | sem acesso ao som; relatório de terceiros: -14 LUFS, música 5-10 dB abaixo da voz | -15 LUFS | alvo de loudness subiu 1 dB (`assemble.sh`) |
Limite honesto: animação e áudio NÃO foram medidos por mim no canal (não há vídeo nem som baixados); o que está aplicado vem de relatório de terceiros.

## 7. Regras fixas novas (valem para todo vídeo)
- **Plano de impacto (blockbuster):** até 2 por vídeo (`max_impact`), nos momentos-chave detectados na narração (tiro, ataque, fuga, pânico, batalha...). Plano aberto com a tropa em formação. Se a frase fala de tiro, clarões piscam pela tropa e toca som de tiro. Se nenhum trecho for detectado, o clímax (~60% do vídeo) vira plano aberto. `"impact": false` no beat desliga.
- **Exército uniforme:** multidão usa só as 4 variantes padrão do uniforme (sem óculos/barba). Óculos e barba ficam para personagens nomeados (variantes 4 a 6 em `who`, ex.: "FARM:5:smile").
- **Exército chegando:** 18 soldados marchando quando a narração fala de tropa chegando.
