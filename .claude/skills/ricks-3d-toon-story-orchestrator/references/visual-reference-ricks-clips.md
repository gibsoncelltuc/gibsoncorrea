# Referência visual observada — canal Ricks Clips (material enviado pelo usuário)

**Origem das evidências:** 4 prints da página do canal (capa, grade de Shorts, miniaturas) e 2 gravações de tela de Shorts (8,2 s cada, iPhone, 1290×2796 @ 60 fps), analisadas frame a frame (contact sheets 5 fps, detecção de cortes, zoom 1:1 em personagens). **Observado** = visto diretamente nos frames. **Inferido** = dedução. **Não medido** = não verificável com este material (ex.: motor de render, FOV exato, curvas de easing, trilha).

## Personagem (observado)
- Cabeça redonda branca com leve tom lavanda e **sombreamento suave**; **contorno escuro grosso** (≈3–4 % do diâmetro da cabeça, quase preto-azulado).
- Corpo **feijão/cápsula** com contorno grosso e **roupa com padrão** (xadrez/tweed, bolinhas, listras), colarinho, gravata, lenço de bolso, botões dourados grandes, suspensórios/macacão.
- Membros **macarrão**: linhas escuras finas (braços com cotovelo, pernas longas e finas); **mãos pequenas redondas**; pés pequenos.
- **Olhos:** sem “bola branca grande”. Padrão base = **pálpebra pesada**: linha superior grossa + pupila pequena logo abaixo (olhar blasé/zombeteiro). Choque = olhos redondos de contorno com pupilas minúsculas + **gotas de suor**. Riso = olhos fechados em arco + boca aberta com **dentes em grade**.
- **Sobrancelhas** grossas, curtas e inclinadas; boca pequena (linha, smirk); **bochechas rosadas** em alguns personagens; props de boca/mão (cigarro, pretzel, binóculo/lente).
- Chapéus/acessórios detalhados (coco, palheta com fita, boné, pena, óculos redondos, gravata-borboleta de bolinhas).

## Cenário (observado)
- 3D toon “pintado”, **muito detalhado**: tábuas de madeira com perspectiva forte, barril com aros metálicos, quadro-negro com letreiros, papéis rasgados espalhados no chão (decals), grama alta, estrada de terra, vitrine/janela de madeira, rua com prédios e placas, bandeira, postes e fios, colina verde ao fundo.
- **Luz quente direcional forte** (laranja) contra **sombras azul/roxas**; **raios de luz volumétricos** e poeira; névoa atmosférica na profundidade; vinheta; leve bloom.
- Céu saturado (azul-claro com nuvens; crepúsculo magenta/roxo/laranja). Multidões = muitas cabecinhas repetidas em arquibancada. Alguns assets 3D mais realistas (ex.: cavalo malhado) misturados ao estilo.
- Capim de primeiro plano em movimento (parallax), profundidade de campo suave.

## Câmera e montagem (observado)
- **Grande angular** com distorção de perspectiva, **câmera baixa** (altura do chão/barril), planos médios e **close-ups extremos** (rosto ocupando o quadro, lente/objeto como moldura).
- **Sempre em movimento lento** (push-in, dolly lateral); viagens rápidas com motion blur.
- **Transições:** dissolve curto (~0,3–0,5 s) entre lugares/tempos; **zoom através de uma lente/objeto** como match-cut; sem cortes secos dentro do mesmo lugar.
- Ritmo: planos de ~1,5–3,5 s; narração ≈ 2,7–3 palavras/s (inglês); dissolve a cada ~2–3 s.

## Legendas (observado)
- 1–2 palavras por vez, sans-serif **extra-bold (família Montserrat 800/900)**, branco, **contorno escuro grosso** e sombra curta, centralizadas a **≈ 70 % da altura** do quadro. **Mantêm pontuação** (vírgula, ponto) — ex.: “dark.”, “Hey,”, “ever”, “mirror man.”.
- **Medido** em ~160 quadros 540×960 dos 2 vídeos de referência (método: bbox do preenchimento branco com vizinhança escura): altura de ascendente ≈ **29 px (5,4 % da altura)**, ≈ 20 px por caractere (“favorite’s” = 198 px), **linha de base a 72,7 %** da altura, contorno fino (~3,5 px a 540 px) + sombra suave. Receita ASS (PlayRes 1080×1920, libass): `Fontsize 123`, `Outline 7`, `Shadow 3`, `BackColour &H90000000`, `MarginV 485` → mede 30 px / linha de base 72,8 %. (A primeira versão do piloto usava os 76 px/15 px da v3.1 e ficou ~1,6× menor e com contorno “bolha”.)

## Cor (observado)
- Saturada: laranja/ocre quente, azul-céu, vermelho/ocre, magenta no pôr do sol. **Verde de relva aparece dominante em alguns planos** (campo, colina).

## Conflitos com o texto da skill e decisões (para auditoria)
| Ponto | Skill | Observação nos frames | Decisão no piloto |
|---|---|---|---|
| Pontuação das legendas | v3.1: “sem pontos finais” | pontuação **mantida** | seguir a observação (`captions.keepPunctuation = true`, configurável) |
| Tamanho/posição das legendas | v3.1: Montserrat 800, 76 px, contorno 15 px, y≈1345 (70 %) | ascendente 5,4 % da altura (≈ 123 em ASS 1080×1920), contorno ~7, sombra, linha de base 72,7 % | seguir a medição (ver receita acima) |
| Verde nunca lidera | v3.1: verde → 55 % para ouro | relva verde dominante em planos abertos | manter regra da skill (campo oliva/dourado, verde só secundário); revisar com o usuário |
| Olhos | V2: ponto + pupila | pálpebra pesada + pupila pequena | adotar a observação (rig v2: `lid`) |
| Membros | “macarrão”/luva | linhas escuras finas, mãos redondas | membros escuros finos, mãos redondas pequenas (luva branca como acento) |
