# Motor long-form — 3, 5 e 10 minutos

## Princípio

Compartilhar o mesmo sistema de personagem, cenário, câmera, animação, áudio, legenda, render e QA dos Shorts. Não simplesmente esticar a timeline. A narrativa e o ritmo precisam mudar com a duração.

## Orçamento narrativo inicial

| Duração | Palavras iniciais | Macroestrutura |
|---|---:|---|
| 3 min | 420–540 | hook, contexto, 2–3 beats de escalada, mecanismo, payoff |
| 5 min | 700–900 | cold open, contexto, ato 1, ato 2, contraexemplo, ato 3, payoff |
| 10 min | 1.400–1.750 | cold open, promessa, contexto, 3–4 atos, viradas, síntese |

A velocidade real depende do idioma, da densidade de fatos e da interpretação. Calibrar com scratch voice/voz final e ajustar texto; não acelerar a fala para caber à força.

## Micro-retensão

Criar uma nova mudança de expectativa, informação, escala ou pergunta a cada 20–45 segundos. Cada capítulo precisa conter:
- uma pergunta local;
- uma informação nova;
- uma imagem/ação que explique ou contradiga a hipótese;
- uma transição causal para o capítulo seguinte.

Evitar cliffhangers falsos, repetição de resumo e capítulos que só adicionam contexto sem avançar a história.

## Orçamento visual

- Abrir cada ato com geografia ou mudança de escala.
- Intercalar wide/medium/close/insert conforme função narrativa.
- Reutilizar sets e personagens com mudanças de luz, hora, clima, props e blocking.
- Planejar cenas de demonstração mais longas quando o mecanismo exigir compreensão.
- Não manter movimento de câmera constante só para “ter movimento”; pausas visuais podem melhorar clareza.
- Reusar o mesmo asset, mas variar composição, staging, ação e iluminação de forma motivada.

## Retenção sem exaustão

- Alternar densidade: sequência rápida → plano de compreensão → escalada → revelação.
- Reservar o payoff central para depois de evidência suficiente, sem atrasá-lo artificialmente.
- Criar pequenos payoffs a cada capítulo e um payoff maior no final.
- Reintroduzir a pergunta central após cada desvio de contexto.

## Compatibilidade de formato

- 9:16: vídeo vertical; texto e ação no centro seguro, com margem para UI da plataforma.
- 16:9: compor para telas maiores, manter foco claro e evitar simplesmente ampliar o layout vertical.
- 1:1: usar somente quando houver motivo editorial/distribuição.
- A engine recebe `aspectRatio`, `resolution`, `fps`, `captionSafeArea` e `platformProfile` como configuração.

## Reutilização

Cada ato deve ser composto por cenas/planos com IDs próprios e contratos de entrada/saída. A mesma cena pode ser renderizada isoladamente para revisão e depois montada no episódio completo.
