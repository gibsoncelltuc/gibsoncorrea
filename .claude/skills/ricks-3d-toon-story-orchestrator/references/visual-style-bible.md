# Bíblia visual — 2D cut-out em cenário 3D toon

## Objetivo estético

Criar uma cena que pareça simples no desenho e rica na profundidade: personagens legíveis, quase icônicos, com contorno escuro e poucos detalhes; cenário com perspectiva 3D, iluminação direcional, sombras coloridas, planos em profundidade e pequenos detalhes atmosféricos. O contraste entre personagem gráfico e mundo dimensional é o princípio visual principal.

Não tratar esta bíblia como uma reprodução exata de um criador. São regras de direção e valores-base aproximados, definidos para uma identidade original.

## Sistema de personagem

- **Cabeça:** circular ou oval ampla, ocupando cerca de 40–55% da altura do personagem; face clara e limpa.
- **Olhos:** pontos/elipses simples, com pupila e direção de olhar controláveis individualmente.
- **Sobrancelhas:** traços separados para dar leitura de emoção em escala pequena.
- **Boca:** conjunto modular de formas: linha, arco, círculo aberto, sorriso, dentes, boca lateral, tremor.
- **Tronco:** forma simples e curta (gota, cápsula, trapézio arredondado); roupa com 1 cor principal e 1–2 detalhes.
- **Braços/pernas:** membros finos e articulados; mãos simples, mas com pose legível.
- **Contorno:** tinta escura, não preto absoluto em todas as condições; espessura consistente com escala de personagem (referência inicial 5–9 px em master 1080×1920, ajustada proporcionalmente).
- **Textura:** pequena irregularidade ou granulação suave apenas quando necessário; preservar a leitura vetorial limpa.
- **Identidade:** variar silhueta, cabelo, chapéu, roupa, acessório, proporção e paleta. Não copiar personagens ou roupas do canal.

## Paleta-base de direção

Os códigos abaixo são **amostras de partida**, não uma extração colorimétrica dos vídeos. Selecionar a paleta por episódio e validar em stills renderizados.

| Papel | HEX sugerido | Uso |
|---|---|---|
| Ink / contorno | `#191827` | Contornos, pupilas, linhas, texto sombreado |
| Face marfim | `#F4EBDD` | Rosto claro, elementos neutros |
| Luz quente | `#F8C58F` | Key light, madeira, pele iluminada, lanternas |
| Âmbar | `#E89A5A` | Acentos de luz quente |
| Sombra azul | `#5E6D9F` | Sombras frias, superfícies em penumbra |
| Azul profundo | `#293453` | Noite, sombra de arquitetura, fundos frios |
| Violeta | `#8274A7` | Reflexos frios, céu crepuscular, superfícies secundárias |
| Teal | `#4C9292` | Acento de ambiente/props, sem dominar |
| Vermelho queimado | `#B9574E` | Roupa/objeto de foco, alerta narrativo |
| Pedra quente | `#B6A6A0` | Alvenaria e pisos |
| Céu diurno | `#83B9E1` | Atmosfera diurna estilizada |

### Regras de paleta

1. Usar uma dominante (60%), uma secundária (30%) e um acento (10%) como ponto inicial, não como fórmula matemática rígida.
2. A luz quente pode contrastar com sombra azul/violeta; as sombras não precisam ser preto puro.
3. Evitar verde saturado como dominante em todos os episódios. Usar verde quando a história pedir natureza, uniforme, sinalização ou contexto específico.
4. Preservar contraste local entre personagem, fundo e legenda. Rosto e objeto explicativo devem ser os pontos de leitura mais claros.
5. Em noite, manter informação nas sombras; não esmagar pretos. Em cena quente, proteger tons de pele e superfícies claras.

## Cenário 3D

- Construir três planos legíveis: foreground com 1–2 elementos, midground com a ação, background com arquitetura/paisagem/atmosfera.
- Priorizar formas limpas e volumes simples; evitar realismo fotográfico. Usar bevels discretos em arestas importantes.
- Materiais: roughness relativamente alta, specular moderado, gradiente de cor, textura procedural sutil e variação de roughness. Evitar aparência plástica excessiva.
- Usar ambient occlusion suave para contato, não como mancha preta.
- Iluminação principal direcional grande/suave; fill frio discreto; rim light opcional para separar silhueta.
- Adicionar vida de ambiente: nuvem lenta, fumaça, fogo, água, bandeira, folhas, poeira, luz de janela, reflexos ou partículas, sempre justificados pelo local.
- Usar parallax real pela profundidade das camadas, não simplesmente mover o fundo inteiro.

## Iluminação e grade

- Definir primeiro a direção da key light e a hora do dia.
- Key/fill/rim devem ter hierarquia; não iluminar tudo igualmente.
- Preferir sombras coloridas e suaves com contato legível.
- Bloom muito discreto em fontes luminosas; evitar glow difuso no personagem.
- Color grade consistente entre planos do mesmo ambiente, com exposição e white balance controlados.
- Usar textura de papel/film grain com intensidade muito baixa; o ruído nunca deve competir com a legenda.

## Composição

### Vertical 9:16

- Manter olhos/rosto no terço superior ou médio, não escondidos pela legenda.
- Guardar área inferior central para as legendas; reservar margens laterais para UI de Shorts.
- Um personagem principal por quadro quando a fala explicar um mecanismo; usar reação/antagonista em plano separado ou em profundidade.
- Se houver objeto técnico, ampliar o objeto o suficiente para ser entendido em tela pequena.

### Horizontal 16:9

- Expandir a geografia do cenário, não apenas esticar o quadro vertical.
- Usar composição em terços, linhas de perspectiva e movimento lateral.
- Não reduzir o tamanho do personagem até ficar ilegível; manter o tamanho de face comparável ao mobile.

## Legenda

- Fonte sans-serif pesada, caixa baixa/alta conforme voz; branco, contorno escuro robusto, sombra curta.
- Exibir 1–2 palavras por vez quando a fala for rápida; palavras-chave podem ganhar acento de cor em raras ocasiões.
- Não usar parágrafos, banners persistentes ou emojis desnecessários.
- Sincronizar com a fala real; usar timestamps de palavra.
- Posição consistente, normalmente na faixa inferior central, mas nunca sobre a ação principal.
