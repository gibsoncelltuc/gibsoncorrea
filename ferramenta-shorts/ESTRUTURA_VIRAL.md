# ESTRUTURA OFICIAL DE ROTEIRO — ROTEIRO VIRAL DE SHORTS (ordem do Gibson, 25/11)

Vale para TODO roteiro (novo ou refeito), nas 3 sessoes, ACIMA das regras antigas de tamanho (55-75 s) e de chamada final.
Fonte: documento "O ROTEIRO VENCEDOR PARA YOUTUBE SHORTS (2026)" enviado pelo Gibson (copia integral no fim deste arquivo).
Checagem automatica: `python3 estrutura_viral.py <id>` (trava o render se falhar) e `python3 estrutura_viral.py --todos` (varredura).

## O que mudou na pratica (regras da ferramenta)

| Regra | Antes | Agora |
|---|---|---|
| Duracao | 55-75 s | **30-45 s** (ideal ate 35 s; limite duro 50 s). ~2,5 palavras por segundo = **75 a 110 palavras** no total |
| Tamanho da frase | livre | **no maximo 12 palavras por frase**; uma ideia por frase |
| Final | chamada falada "Agora nao deixe de comentar: qual deve ser o tema do proximo video?" | **LOOP**: a ultima frase emenda na primeira (gramatica ou imagem). A chamada para comentar sai da narracao (vai na descricao/comentario fixado) |
| Palavras de enchimento | toleradas | proibidas: "tipo", "sabe", "entao", "ne", "ai", "basicamente", "na verdade" |
| Gancho | frase forte | **um dos 4 tipos** + gancho em 3 camadas (imagem de impacto + texto na tela + frase de alto risco) |

## Os 6 blocos (cada cena do beats.json leva `"bloco"`)

| Tempo | `bloco` | O que a frase faz | Como a ferramenta mostra |
|---|---|---|---|
| 0-3 s | `gancho` | 1 frase, ate 12 palavras, de um dos 4 tipos. Nada de data, nada de "Oi" | cena de impacto + `"text"` (placa/titulo) na 1a cena |
| 3-10 s | `promessa` | expande o gancho e promete o pagamento ("eu preciso ver como termina") | cena com o heroi/objeto |
| 10-25 s | `prova` | micro-vitorias: frases curtas com NUMERO, NOME ou RESULTADO concreto. Pelo menos 1 antes dos 20 s | mapa, contador, placa, close do objeto |
| 25-40 s | `escalada` | a virada: "Mas a parte maluca e'...", fato inesperado, aposta sobe | grande momento (plano aberto, efeito) |
| 40-45 s | `pagamento` | resolve EXATAMENTE o que o gancho prometeu (honesto) | close do heroi / resultado |
| 45-50 s | `loop` | ultima frase que puxa a primeira (ex.: termina em "...e foi assim que" e o video recomeca em "Uma orelha cortada levou..."). | ultima imagem = mesma cena/enquadramento da 1a |

## Os 4 tipos de gancho (`"gancho_tipo"` no topo do beats.json)
1. `perda` — Ameaca de perda: "Se voce ainda faz X, esta perdendo..."
2. `ganho` — Promessa de ganho: "Existe um jeito de fazer Y em metade do tempo."
3. `crenca` — Quebra de crenca: "Todo mundo acha que X. Esta errado."
4. `segredo` — Segredo exposto: "O que ninguem te conta sobre X e' que..."
Para historia (nosso canal), a forma mais usada: `segredo` ("Ninguem te contou que uma orelha cortada comecou uma guerra.") e `crenca` ("Voce acha que guerra precisa de tiro? Esta nao teve nenhum.").
Gancho HONESTO: o pagamento entrega o que o gancho prometeu.

## Ritmo
- Imagem muda a cada 2-4 s (a ferramenta ja corta takes dentro da cena); nenhum enquadramento parado mais de 8 s (~3 frases).
- 80-85% assistem no mudo: a legenda queimada e o texto na tela contam a historia sozinhos.
- Titulo: com palavra-chave, mesma historia e mesmo titulo de antes.

## Checklist (estrutura_viral.py confere cada item)
- [ ] gancho em camadas: 1a cena com texto na tela + frase do tipo escolhido
- [ ] narracao entre 30 e 45 s (75-110 palavras; ideal ate 35 s)
- [ ] legendas queimadas (a ferramenta ja faz)
- [ ] micro-pagamento (numero/nome/resultado) antes dos 20 s
- [ ] final conecta com o inicio (loop)
- [ ] promessa do gancho cumprida no `pagamento`
- [ ] nenhuma frase com mais de 12 palavras; nenhuma palavra de enchimento

## Postagem (para o Gibson)
Nao postar 30 de uma vez: 3 a 7 por semana (1 por dia no maximo), cada video com a sua janela de teste (30-60 min). Medir no Studio: VVSA (visto x deslizado) > 75%, retencao media > 70%, replays (retencao > 100%).

---

## DOCUMENTO ORIGINAL (enviado pelo Gibson em 25/11)

DOCUMENTO: O ROTEIRO VENCEDOR PARA YOUTUBE SHORTS (2026)
Foco: Estrutura de Roteiro, Gancho, Retenção e Loop para Furar a Bolha do Algoritmo.

1. A MÉTRICA QUE MANDA (E O FIM DO MITO DO CANIBALISMO)

Antes do roteiro, você precisa esquecer o medo de "canibalismo". O algoritmo do Shorts foi desacoplado do formato longo no final de 2025. Cada Short é testado individualmente para uma pequena audiência inicial (seed audience).

O que define se ele vai ser distribuído para mais gente não é a quantidade de vídeos que você posta, mas sim a sua capacidade de não ser pulado.

- A Métrica Rainha: VVSA (Viewed vs. Swiped Away). É a taxa de pessoas que assistiram versus as que deslizaram para o próximo vídeo.
- Metas para Monitorar no YouTube Studio:
  - VVSA: Acima de 75% é a meta para "bater o swipe". Abaixo de 50% significa que seu gancho está fraco.
  - Retenção Média (Average Percentage Viewed): Acima de 70% é considerada a "barra interna" de qualidade do YouTube.
  - Loop/Replays: Se a retenção passar de 100%, significa que as pessoas assistiram mais de uma vez. Esse é um dos sinais positivos mais fortes que existem.

Conclusão sobre postagem: Postar 30 vídeos de uma vez é um tiro no pé. Você está competindo com você mesmo pela janela de teste inicial (os primeiros 30–60 minutos) de cada vídeo. A estratégia correta é postar de forma consistente (3 a 7 por semana) para dar a cada vídeo a sua própria chance de passar pelo teste inicial.

2. A ESTRUTURA DO ROTEIRO: O "BOLO" DA RETENÇÃO

A estrutura vencedora não é sobre "ter uma ideia boa". É sobre engenharia de atenção. O roteiro deve ser construído para criar Micro-Pagamentos (micro-payoffs) a cada poucos segundos, pois um único pagamento no final (aos 40s) é tarde demais.

A RECEITA (ESTRUTURA DE 30–45 SEGUNDOS)

| Tempo | Bloco | Objetivo | O que fazer |
|---|---|---|---|
| 0–3s | O GANCHO (O Stop) | Vencer o swipe. | Use um Gancho em Camadas: Visual (cena impactante) + Texto na tela + Áudio (frase de alto risco). Nada de "Oi, galera". |
| 3–10s | A PROMESSA (Tensão) | Expandir o gancho e prometer o pagamento. | A frase deve fazer a pessoa pensar: "Eu preciso ver como isso termina". |
| 10–25s | MICRO-VITÓRIAS (A Prova) | Entregar valor rápido. | Frases curtas. Uma ideia por frase. Use números, nomes ou resultados concretos ("prova dura"). |
| 25–40s | A ESCALADA (A Virada) | Quebrar a expectativa. | Um insight contrário, um exemplo inesperado ou um "aqui está a parte maluca". Aumente a aposta. |
| 40–45s | O PAGAMENTO (O Clímax) | Resolver a promessa do gancho. | A entrega final precisa ser honesta e parecer "merecida". Se o gancho prometeu ouro, entregue ouro. |
| 45–50s | O LOOP (A Armadilha) | Forçar o replay. | A última frase/frame deve se conectar gramaticalmente ou visualmente com a primeira frase/frame. Ex: terminar com "…e é por isso que" e a primeira frase ser "Isso quebrou o algoritmo". |

3. OS 4 TIPOS DE GANCHO QUE FUNCIONAM (0–3s)

Você deve escolher um destes para a sua primeira frase/primeiro frame. Não use introduções suaves.

1. Ameaça de Perda: "Se você ainda faz [X], está perdendo dinheiro/tempo/alcance."
2. Promessa de Ganho: "Existe uma forma de fazer [Y] em metade do tempo. E é simples."
3. Quebra de Crença: "Todo mundo te disse que [crença popular] era verdade. Está errado."
4. Segredo Exposto: "O que ninguém te conta sobre [tema] é que…"

Dica de Ouro: O gancho deve ser honesto. Prometer algo que o vídeo não entrega causa uma queda brusca de retenção no meio do vídeo, e o algoritmo pune isso.

4. RITMO E EDIÇÃO: O QUE O ALGORITMO "SENTE"

O algoritmo não "assiste" ao seu vídeo; ele lê os sinais de comportamento. Para manter a retenção alta, o roteiro precisa prever o ritmo da edição.

- Mude o visual a cada 2–4 segundos. Nunca mantenha o mesmo enquadramento ou imagem por mais de 8 segundos (ou ~3 frases).
- Assuma que 80–85% estão no mudo. Escreva o roteiro pensando nas legendas queimadas. O texto na tela deve contar a história sozinho.
- Uma ideia por frase. Elimine completamente palavras de preenchimento ("tipo", "sabe", "então"). Nenhuma frase deve ter mais de 12 palavras.

5. TEMPLATE PRÁTICO (COPIE E PREENCHA)

Use este esqueleto para os seus vídeos estilo Rick 2D/3D.

| Seção | O que escrever (Exemplo Genérico) |
|---|---|
| TÍTULO (com palavra-chave) | "O erro de roteiro que mata 90% dos Shorts" |
| 0–3s (Gancho em Camadas) | Visual: Close no personagem com expressão de choque. Texto: "PARE de postar assim". Áudio: "Se o seu Short não passa dos 200 views, o problema não é o algoritmo." |
| 3–10s (Promessa) | "O problema é que você está entregando tudo de uma vez. Eu vou te mostrar a estrutura de 3 micro-pagamentos que força a retenção." |
| 10–25s (Micro-Vitórias) | "Primeiro: o gancho. 50% das pessoas saem nos primeiros 3 segundos. Segundo: o visual. Troque de cena a cada 2 segundos. Terceiro: o loop. A última frase precisa puxar a primeira." |
| 25–40s (Escalada) | "Mas aqui está a parte que ninguém fala: não adianta editar rápido se a sua promessa é mentira. Um gancho desonesto cria um buraco de retenção que o algoritmo detecta na hora." |
| 40–45s (Pagamento) | "Então, a receita é: Gancho honesto + Micro-pagamentos + Loop. É isso que separa um vídeo de 200 views de um de 200 mil." |
| 45–50s (Loop) | "Agora que você sabe a estrutura… o próximo passo é saber como prender nos primeiros 3 segundos." (A edição volta para o frame do gancho inicial). |

CHECKLIST FINAL ANTES DE POSTAR

- [ ] O gancho tem visual + texto + áudio trabalhando juntos?
- [ ] O vídeo tem menos de 35 segundos (ideal para completar a visualização)?
- [ ] As legendas estão queimadas e legíveis no mudo?
- [ ] Existe pelo menos um micro-pagamento antes dos 20 segundos?
- [ ] O final do vídeo se conecta intencionalmente com o início (loop)?
- [ ] A promessa do gancho foi realmente cumprida no final?

Com essa estrutura, você para de "apostar" no algoritmo e começa a engenheirar a retenção. Aplique isso aos seus 30 vídeos, poste um por dia (ou 4-5 por semana) e analise o VVSA no Studio para saber qual gancho está funcionando melhor.
