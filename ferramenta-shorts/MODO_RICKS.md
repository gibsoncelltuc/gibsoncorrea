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

## 4. O que ainda NÃO está no nível do canal (honesto)
1. **Cenários**: o canal modela um cenário por história (interiores, ruas, navios). Nós temos poucos cenários genéricos ao ar livre. É a maior diferença que resta. Próximo passo: kit modular (paredes, pisos com juntas, portas, janelas, móveis) montado pelo beats.json.
2. **Figurino/variedade de personagem**: poucos chapéus/cabelos/barbas; soldados parecem clones; pernas/braços deveriam ser traço de tinta escura.
3. **Falas de personagem**: o beats.json só tem narração; falta marcar quem fala e mexer a boca.
4. **Objetos na mão e ações de corpo** (pegar, carregar, apontar com objeto).
5. Luz por cena (noite azul, interior quente) e cor da sombra lavanda no rosto.
6. Áudio: não foi possível medir o do canal (sem acesso ao som).
Detalhes e números: `ref_privado/audit/*.md` (personagens, enquadramento-camera, cenarios-props).

## 5. Como produzir um vídeo
1. Escreva `videos/<id>/beats.json` seguindo o §1 (copie um existente). 2. `python3 roteiro_check.py <id>`. 3. Ponha o id em `queue.txt`. 4. `bash run_queue.sh` (retomável; `bash status.sh` mostra o andamento). Saída: `out/<id>/<Titulo>.mp4` + `review_sheet.jpg`. Sempre olhar a folha de contato antes de publicar.
