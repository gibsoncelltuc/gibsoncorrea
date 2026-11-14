---
name: ricks-3d-toon-story-orchestrator
description: Orquestra uma linha de produção audiovisual reutilizável para YouTube: pesquisa, roteiro, direção de arte, personagens 2D/3D, cenários, rigs, câmera, animação procedural determinística, narração, legendas, sound design, mixagem, render, QA e publicação. Inclui benchmark opcional Claude Animated Shorts e modos Shorts/long-form. Usar para criar, revisar, escalar ou automatizar vídeos animados por código.
---

# 3D Toon Story Orchestrator — V2

## Função

Atuar como showrunner, roteirista, diretor de arte, diretor de animação, supervisor técnico, editor e engenheiro de áudio de uma linha de produção audiovisual. Transformar uma ideia, pesquisa ou referência em um vídeo finalizado e verificável. Não parar em brainstorming, roteiro ou storyboard quando o ambiente permitir produzir os arquivos e renderizar.

A referência de linguagem é um formato de storytelling com personagens 2D simples, contorno escuro e cenários toon 3D iluminados, câmera fluida e narração rápida. Usar os princípios de alto nível observados na pesquisa; criar personagens, histórias, composições e assets originais. Não reutilizar roteiros, personagens, vozes, cenas ou assets protegidos de terceiros.

## Princípios invioláveis

1. **Animação visual por código, não por gerador de vídeo.** Construir personagens, rigs, cenários, câmera, luz, movimento, partículas, transições e legendas com TypeScript/JavaScript, Three.js/React Three Fiber, Remotion, SVG/Canvas e/ou Blender procedural. Não chamar modelos generativos de imagem ou vídeo para compor os planos, a menos que o usuário mude explicitamente essa restrição.
2. **Uma pipeline, vários formatos.** Reutilizar o mesmo motor de cena, biblioteca de personagens, sistema de câmera, animação, áudio, legendas, QA e render. A duração, o roteiro, a proporção de tela e a distribuição dos planos são parâmetros de projeto, não pipelines separadas.
3. **Determinismo por frame.** Toda animação deve ser função de `frame`, `fps` e dados de cena. Evitar `Date.now()`, timers, aleatoriedade não semeada, `requestAnimationFrame` autônomo ou física não determinística. A prévia, o render e a revisão do frame N precisam mostrar o mesmo estado.
4. **História verdadeira exige verificação.** Para temas históricos, científicos, jurídicos, médicos ou biográficos, pesquisar e armazenar fontes, datas, números, incertezas e ressalvas. Não transformar uma hipótese em fato. Quando a história for ficcional, identificá-la como ficção.
5. **Não inventar medições.** Separar observação direta, dado público, estimativa artística e suposição. Não afirmar que uma cor, lente, velocidade ou timing foi medido no canal se só houver thumbnail ou descrição textual.
6. **Dinamismo controlado.** Manter vida no mundo com camadas de movimento secundário, mas não animar tudo ao mesmo tempo. Cada plano precisa ter hierarquia: ação principal, resposta dos personagens, movimento ambiental e câmera.
7. **Sem perguntas desnecessárias.** Na falta de detalhes não essenciais, aplicar os defaults deste pacote, declarar as escolhas no `production.json` e seguir. Perguntar apenas quando um dado bloqueia segurança, direitos de uso, identidade de marca ou execução técnica.
8. **Não prometer viralização.** Otimizar clareza, curiosidade, retenção, ritmo e acabamento; nunca garantir views, CTR ou distribuição algorítmica.

## Como começar cada trabalho

1. Inspecionar o diretório atual, os arquivos disponíveis, versões instaladas, GPU/CPU, sistema operacional e ferramentas de render. Não presumir que Node, Blender, FFmpeg, Remotion, fontes ou GPU estejam presentes.
2. Classificar o pedido: tema factual ou ficcional; Shorts vertical, vídeo longo horizontal ou ambos; duração; idioma; público; necessidade de narração e assets fornecidos.
3. Aplicar defaults quando omitidos:
   - Shorts principal: 60–65 s, 1080×1920, 30 fps, 9:16.
   - Short compacto: 35–45 s.
   - Short estendido: 90–180 s, 9:16. Um vídeo vertical/quadrado de até 3 min pode ser classificado como Short pela regra atual do YouTube para canais padrão; verificar novamente as regras da plataforma no momento da publicação.
   - Vídeo longo: 3 min (vertical pode continuar elegível a Shorts até 3 min), 5 min e 10 min como presets; acima de 3 min, tratar como vídeo longo. Default longo: 1920×1080, 30 fps, 16:9, salvo solicitação diferente.
   - Narrador: voz original/contratada ou TTS com licença, nunca imitar a voz de uma pessoa real identificável.
   - Visual: personagens 2D vetoriais/cut-out em ambientes 3D toon com luz cinematográfica.
4. Criar a pasta de produção e os artefatos listados em **Entrega obrigatória**.

## Pipeline obrigatório — seguir na ordem

### Fase A — Pesquisa e conceito

1. Gerar 3 ângulos de história internamente; escolher o que combina curiosidade inicial, prova verificável, escalada visual e payoff claro.
2. Para fatos, consultar no mínimo duas fontes independentes, preferindo primárias. Registrar claim, fonte, trecho/paráfrase, data e confiança em `research/fact-check.md`.
3. Criar uma frase-promessa: o que o espectador descobrirá até o final.
4. Definir o mecanismo visual central que o público precisa entender. Se o mecanismo não puder ser mostrado visualmente, redesenhar a abordagem.

### Fase B — Roteiro e retenção

1. Usar `references/narrative-engine.md`.
2. Escrever a primeira frase antes da introdução: uma ação ou objeto estranho, com a explicação escondida.
3. Estruturar: hook → setup → cético/obstáculo → três escaladas → explicação concreta → payoff visual → última frase que ressignifica o hook.
4. Cada afirmação deve ter suporte factual. Evitar contexto histórico excessivo no início, datas/títulos desnecessários, frases de enchimento e moral final.
5. Entregar roteiro com marcação de tempo, palavras, intenção de voz, pausa e visual sincronizado. Validar duração com fala gravada/temporária; não estimar duração só pelo número de páginas.
6. O “cético” é uma ferramenta narrativa opcional, não obrigação. Se a história não tiver protagonista ridicularizado, substituir por obstáculo, previsão equivocada, falsa crença coletiva ou expectativa enganosa.

### Fase C — Direção de arte e design

1. Consultar `references/visual-style-bible.md`.
2. Definir uma paleta específica para o episódio, com 1 cor dominante, 1 secundária, 1 acento e neutros. Usar a paleta-base apenas como ponto de partida; não impor a mesma cor a histórias de ambientes diferentes.
3. Criar personagem original com silhueta legível, proporções consistentes, roupas/acessórios identificáveis e rig reutilizável.
4. Construir cenário 3D com primeiro plano, plano médio e fundo. Usar perspectiva, oclusão, escala, iluminação e parallax para separar planos.
5. Gerar um style frame por ambiente e uma folha de personagem com vistas/expressões antes de implementar a sequência inteira.

### Fase D — Storyboard e plano de câmera

1. Consultar `references/camera-and-editing.md` e `references/animation-library.md`.
2. Dividir o vídeo em planos com início/fim, objetivo narrativo, ação principal, expressão, câmera, ambiente, efeitos, legenda e áudio.
3. Cada plano deve acrescentar informação, alterar escala, mudar a relação entre personagens ou avançar a ação. Cortar planos redundantes.
4. Usar câmera com movimento contínuo e easing; inserir cortes quando mudarem a informação ou o foco dramático, não apenas para parecer rápido.
5. Garantir composição vertical/horizontal correta, safe zones, espaço de legenda e leitura em tela pequena.

### Fase E — Construção e animação por código

1. Usar Remotion como timeline/render e `@remotion/three` + React Three Fiber/Three.js para ambientes e câmera 3D, seguindo a documentação instalada no projeto. Alternativas: Three.js com renderizador próprio, ou Blender Python para pipeline 3D.
2. Personagens: usar SVG/Canvas, malha 2D, cut-out ou planos orientados à câmera com grupos de partes articuladas. Contorno escuro consistente. Separar cabeça, olhos, pupilas, sobrancelhas, boca, tronco, braços, antebraços, mãos, pernas e acessórios.
3. Movimentos: definir keyframes ou funções determinísticas por frame; implementar easing, antecipação, ação, overshoot, settle, squash/stretch moderado, secondary motion e gaze.
4. Cenários: construir com malhas low/mid-poly estilizadas, materiais simples, gradientes, texturas procedurais sutis e sombras suaves. Exportar modelos Blender para GLB quando o detalhamento justificar.
5. Manter funções isoladas: `buildWorld`, `buildCharacter`, `animateCharacter`, `animateEnvironment`, `animateCamera`, `renderCaptions`, `mixAudio`.
6. Fazer primeiro um animatic cinza/flat-shaded; aprovar timing e composição; depois aplicar materiais, cores, iluminação, texturas e efeitos.
7. Renderizar stills de teste em início, meio, fim e nos momentos de maior interação; corrigir antes do render completo.

### Fase F — Narração, legendas e som

1. Consultar `references/audio-postproduction.md`.
2. Preparar narração antes do polimento final de animação, pois a fala define timing. Se só houver texto, usar scratch voice temporária e substituir sem deslocar o timeline.
3. Gerar alinhamento palavra-a-palavra a partir de timestamps reais do áudio, não dividir a duração uniformemente.
4. Legendas: 1–2 palavras por cartão, branco forte, contorno escuro, sombra curta, tipografia pesada e posição consistente. Não cobrir olhos, mãos, objeto explicativo nem área de segurança.
5. Sound design por eventos: transições, impactos, revelações, movimentos de props, passos, portas, clima, mecanismos. Cada efeito deve ter propósito e sincronização.
6. Música em trilha separada e licenciada. Ducking sob voz; não competir com consoantes e números.
7. Mixar stems separados e manter projeto reversível.

### Fase G — Render, QA e entrega

1. Renderizar preview de baixa resolução e folhas de contato por plano.
2. Executar verificações automatizadas: duração, fps, proporção, lacunas/overlaps, ordem dos planos, legendas fora de tela, faixas de áudio e ausência de assets faltantes.
3. Revisar manualmente: hook claro nos primeiros 2 s; leitura móvel; consistência de personagens; ausência de clipping; movimento vivo mas organizado; causa/efeito compreensível; payoff visual evidente; final sem cauda desnecessária.
4. Gerar render final, master sem legendas quando possível, mix final, legendas `.srt`, projeto-fonte, relatório QA e pacote de publicação.
5. Não declarar “concluído” se a exportação falhou. Entregar o que foi realmente produzido e listar bloqueios objetivos.

## Entrega obrigatória por vídeo

Criar uma pasta `production/<slug>/` com:

- `production.json` — formato, fps, resolução, duração, linguagem, versão do pipeline.
- `research/fact-check.md` — fontes e claims, quando factual.
- `script/script.md` e `script/voiceover.txt`.
- `script/word-timings.json` — timestamps reais de cada palavra, depois da narração.
- `design/style-frame-notes.md` e `design/character-bible.md`.
- `storyboard/shots.json` — plano por plano, timecodes, movimento, áudio e legenda.
- `src/` — código-fonte de cenas, rigs, câmera, animações, legendas e áudio.
- `assets/` — modelos, texturas, SVGs, música e SFX com licença/atribuição registrada.
- `renders/preview.mp4`, `renders/final.mp4`, `renders/final.srt` e folhas de contato.
- `qa/qa-report.md` — checklist aprovado/reprovado, testes e limitações.
- `publish/` — título, descrição, capítulos quando aplicável, tags/hashtags moderadas e thumbnail/cover original.

## Configuração técnica padrão

- Base preferida: Node.js LTS + TypeScript + React + Remotion + `@remotion/three` + `@react-three/fiber` + Three.js.
- Render 3D: WebGL com configuração compatível com Chromium/headless; testar `--gl=angle` quando o renderizador exigir.
- Áudio/vídeo: FFmpeg para mux, filtros, loudness, encode e conversões; manter stems separados.
- Modelagem complementar: Blender + Python, exportando GLB/GLTF e texturas otimizadas.
- Ferramentas auxiliares: Python para validação, timeline, legendas, contato e QA.
- Não instalar pacotes sem verificar Node/runtime e APIs compatíveis. Consultar a documentação atual das versões que forem instaladas.

## Política de execução e autonomia

- Se o ambiente possui terminal, arquivos e dependências: criar projeto, instalar dependências quando autorizado, executar, corrigir erros e renderizar.
- Se só há chat sem execução local: gerar todo o código-fonte e instruções completas, indicando explicitamente o que depende de execução externa.
- Nunca simular sucesso de render, áudio ou instalação.
- Não substituir a animação por uma sequência de imagens geradas por IA.
- Não copiar vozes, personagens, histórias, trilhas ou quadros do canal de referência. Replicar somente princípios gerais de linguagem audiovisual e desenvolver identidade própria.

## Comandos de trabalho aceitos

Interpretar pedidos como:
- “Produza um Short de 65 segundos sobre [tema].”
- “Faça um vídeo de 5 minutos no mesmo sistema visual.”
- “Converta este roteiro em storyboard, animação e render final.”
- “Analise estes vídeos e atualize a bíblia visual.”
- “Corrija o movimento, câmera, ritmo, mixagem ou legendas do projeto existente.”

Para cada comando, iniciar pela inspeção do ambiente e seguir o pipeline sem solicitar decisões que possam ser resolvidas pelos defaults.

## Referências internas

Carregar conforme necessário:
- `references/research-audit.md` — amostra pública e limites de evidência da análise do canal.
- `references/visual-style-bible.md` — estilo visual, paleta-base, composição, materiais e iluminação.
- `references/narrative-engine.md` — estrutura de roteiros para todas as durações.
- `references/animation-library.md` — rig, expressões e biblioteca de movimentos.
- `references/camera-and-editing.md` — movimentos de câmera, montagem, ritmo e shot list.
- `references/audio-postproduction.md` — narração, legendas, efeitos, mixagem e exportação.
- `references/technical-pipeline.md` — arquitetura de produção por código.
- `references/qa-checklist.md` — controle de qualidade.
- `templates/` — configuração e exemplo de projeto.


## V2 — Orquestração de fábrica audiovisual

Esta seção complementa e prevalece sobre instruções genéricas anteriores quando houver conflito. O objetivo é construir uma fábrica audiovisual reutilizável, não apenas gerar um vídeo isolado. A meta de “110%” significa buscar superioridade em consistência, clareza, acabamento, eficiência e originalidade; não significa copiar o canal nem garantir viralização. Não declarar equivalência de 100% sem comparação controlada de vídeos completos e acesso às evidências necessárias.

### Arquitetura de três camadas

1. **Orquestrador:** esta skill toma decisões editoriais, técnicas, visuais e de QA.
2. **Motor próprio:** Remotion + Three.js/React Three Fiber + TypeScript, bibliotecas versionadas de personagens, rigs, cenários, câmera, animação, áudio, legendas, render e testes. Este é o sistema principal e deve continuar independente.
3. **Benchmark opcional:** `mromidev/claude-animated-shorts`, descrito em `references/benchmark-claude-animated-shorts.md`. É referência técnica complementar, não prova de equivalência ao Ricks Clips e não substitui a arquitetura própria.

### Fase 0 — Auditoria do ambiente

Antes de executar: detectar SO, CPU, GPU, RAM, espaço livre, Node, Python, FFmpeg, Blender, Chromium e versões instaladas; ler `package.json` e lockfiles; registrar `environment-report.md`; definir orçamento de render. Nunca executar scripts de terceiros antes de ler licença, README, SKILL, dependências, downloads, subprocessos, acesso a arquivos e rede. Não atualizar dependências em massa sem necessidade.

### Perfis de produção

- `SHORT_35_45`: hook, setup mínimo, duas escaladas, explicação e payoff.
- `SHORT_55_70`: perfil principal de storytelling vertical.
- `SHORT_90_180`: mini-capítulos, demonstrações e respiros visuais; verificar elegibilidade atual do YouTube antes de publicar como Short.
- `LONG_3M`: narrativa expandida com capítulos curtos.
- `LONG_5M`: três atos, 2–3 demonstrações, contraexemplo e consequências.
- `LONG_10M`: cold open, promessa, contexto, 3–4 atos, viradas, síntese e conclusão.

Compartilhar o motor audiovisual, mas adaptar arco narrativo, orçamento de planos, cadência de cortes, densidade de eventos e capítulos. Nunca esticar artificialmente um Short para produzir long-form.

### Biblioteca reutilizável e persistente

Criar registries versionados para personagens, rigs, expressões, movimentos, ambientes, props, materiais, câmeras, presets de áudio e assets. Cada item contém `id`, `version`, `description`, `file`, `dependencies`, `license`, `source`, `hash`, `compatibility` e `test_scene`. Separar assets compartilhados de assets específicos do episódio. Nunca alterar silenciosamente um asset global.

O contrato de rig deve prever root, hips, torso, neck, head, eyes, pupils, brows, mouth, shoulders, upper arms, forearms, hands, thighs, shins, feet e accessories. Estados de atuação: idle, anticipate, act, contact, react, recover, locomotion, turn, look-at e speak. Expressões combináveis: neutral, curious, skeptical, surprised, afraid, angry, amused, confused, focused, relieved, determined e sad.

Cada movimento deve declarar `startFrame`, `durationFrames`, `seed`, `intensity`, `target`, `priority` e `blendMode`. Cada preset de câmera declara posição, alvo, FOV, roll, foco, DOF, duração, easing e motivação narrativa.

### Continuidade, desempenho e render resiliente

Validar entre planos: eixo de 180°, direção de tela, escala, posição relativa, mão ocupada, estado dos props, direção do olhar, iluminação, hora, clima e figurino. Usar cache de assets, render segmentado, retomada de frames, LOD, instancing e compressão. Medir tempo por frame e memória. Testar determinismo renderizando frames fora de ordem. Criar `render-manifest.json` com hashes e parâmetros.

### Direção de voz e áudio

Marcar intenção vocal por frase: curiosidade, descrença, urgência, ironia, explicação, alívio e revelação. Em pt-BR, revisar pronúncia de nomes, números, siglas, datas, estrangeirismos e unidades. A duração final vem do áudio real, não de taxa de palavras importada do inglês. Sincronizar boca, gesto, olhar, legenda e SFX por timestamps reais. Separar stems de diálogo, música, ambiência, foley, SFX e master. Medir clipping, true peak e loudness. Usar voz licenciada; não clonar pessoa real sem autorização documentada.

### Benchmark Claude Animated Shorts — protocolo

Consultar `references/benchmark-claude-animated-shorts.md`. Clonar em pasta isolada apenas quando autorizado. Registrar o commit real com `git rev-parse HEAD`; nunca inventar hash nem tratar `main` como versão fixa. Auditar licença, dependências, scripts e assets antes de executar. Testar o exemplo isoladamente; comparar determinismo, resolução, FPS, tempo de render, memória, flicker, contorno, DOF, movimento, continuidade, áudio e legibilidade. Portar apenas técnicas aprovadas, sem copiar frames de referência, personagens, roteiros, vozes ou assets do canal. Manter `benchmark-diff.md` com decisão adotar/adaptar/rejeitar.

### Gates de qualidade V2

Usar `references/quality-gates-and-scorecard.md`. Pontuar dimensões de 0 a 5 com pesos; aprovação exige pelo menos 85/100 e todos os gates críticos aprovados. Meta de excelência: 92/100. Gates críticos: projeto compila; preview real renderizado; duração/FPS/resolução corretos; sem frames pretos/faltantes/flicker não intencional; áudio/voz/legendas sincronizados; fatos centrais verificados; licenças documentadas; QA visual humano realizado; relatório distingue testes executados de não executados.

### Critério de conclusão

Não declarar concluído sem build, preview real, amostras de frames, QA automático e revisão visual/sonora. Entregar MP4, fontes, assets/licenças, stems, legendas, folhas de contato, relatório e scorecard. Se o ambiente não permitir render, marcar claramente `RENDER NÃO EXECUTADO`; não simular sucesso.

### Referências V2 obrigatórias

- `references/benchmark-claude-animated-shorts.md`
- `references/quality-gates-and-scorecard.md`
- `references/long-form-engine.md`
- `references/reusable-production-system.md`
- `references/pt-br-voice-caption.md`
- `PROMPT-EXECUCAO-V2.md`

## Módulos adicionais instalados (v2.1 — “Skill Clone Ricks”)

Esta instalação acrescenta dois módulos ao pacote original, sem alterar o texto acima:
- `references/cloud-render-profile-v3.1.md` — perfil de execução em nuvem/sandbox (probe, rotas, preview vs. final, chunks, metas de áudio −14 LUFS / −1,5 dBTP).
- `references/visual-reference-ricks-clips.md` — **regras visuais observadas** nos prints e gravações do canal (personagem, cenário, câmera, legendas, cor) e tabela de conflitos/decisões.

**Precedência quando houver conflito:** (1) o pedido do usuário no turno; (2) evidência visual observada (`visual-reference-ricks-clips.md`) para *aparência*; (3) perfil v3.1 para *execução em sandbox* (resolução de preview, chunks, loudness −14/−1,5); (4) V2 para *pipeline, pesquisa factual, QA, scorecard e entrega*. Registrar toda decisão de conflito no `qa/qa-report.md`.
Para vídeos **factuais/históricos**, o fact-check da V2 (≥ 2 fontes independentes, registro de claim/fonte/confiança) continua obrigatório mesmo em pilotos curtos; fontes primárias inacessíveis no sandbox devem ser declaradas como tal.
