# Arquitetura técnica — produção audiovisual programática

## Stack recomendada

### Núcleo

- **TypeScript + React:** componentes, rigs, dados de cena e timeline.
- **Remotion:** composição, timeline, prévia e renderização por frames.
- **@remotion/three + React Three Fiber + Three.js:** cenários 3D, luz, câmera, objetos e personagens 2D posicionados no espaço.
- **FFmpeg:** mux, encode, filtros, loudness e exportações.
- **Python:** validadores, contatos, utilitários de legenda e automação auxiliar.

A documentação de `ThreeCanvas` explica que ele sincroniza React Three Fiber com `useCurrentFrame()` do Remotion; animações devem ser declarativas e baseadas em frames, em vez de depender de `useFrame()` autônomo. Isso permite scrubbing e renderização determinística.

### Complementos

- **Blender:** modelagem e animação 3D complexa, rigging, Grease Pencil e exportação GLB/GLTF. Grease Pencil permite desenho/animação 2D integrado a um ambiente 3D.
- **SVG/Canvas:** personagens, expressões, placas, ícones, diagramas e props vetoriais.
- **Tone.js/Web Audio (opcional):** sons procedurais simples, sem gerar imagens/vídeos.

## Arquitetura de código

Separar o projeto em camadas:

```text
src/
  data/
    production.ts
    story.ts
    shots.ts
    audio-events.ts
  characters/
    rig/
    expressions/
    actions/
  world/
    sets/
    props/
    materials/
    lighting/
  camera/
    camera-rig.tsx
    camera-paths.ts
  animation/
    easing.ts
    timing.ts
    environment-motion.ts
  captions/
    word-captions.tsx
  audio/
    voice.tsx
    music.tsx
    sfx.tsx
  compositions/
    MainVideo.tsx
  Root.tsx
  index.tsx
```

## Contratos fundamentais

- `production.json` define resolução, fps, duração, idioma, safe zones, render profile e versão.
- `story.json` define roteiro e beats.
- `shots.json` define intervalos, câmera, ação, set, expressão, legendas e SFX.
- `word-timings.json` define intervalos reais das palavras da voz.
- `assets-manifest.json` registra path, função, fonte e licença de cada asset.

Não codificar títulos, números, duração ou frases de legenda dentro de componentes visuais. Usar dados.

## Regra de frame determinístico

Converter tempo em frame:

`timeSeconds = frame / fps`

Derivar todo estado a partir desse valor. Usar `interpolate`, curvas de easing e funções com seed fixo. Se precisar de partículas randômicas, gerar posições uma vez com PRNG semeado, nunca sortear em cada render.

## Personagem 2D no mundo 3D

Duas abordagens:

1. **Billboard / plane rig:** SVG transparente como texture em plane voltado para câmera. Melhor para 2D chapado e leitura estável.
2. **Rig de partes no plano XY:** cabeça, face, corpo, braços e pernas como meshes/curvas vetoriais separados, com pivôs. Melhor para animação articulada e interação com objetos.

Para interagir com o cenário, posicionar o rig em coordenadas do mundo e sincronizar mão/objeto por um ponto de contato. Evitar que o personagem pareça flutuar.

## Construção de ambiente

1. Modelar volumes simples.
2. Criar três camadas de profundidade.
3. Aplicar materiais toon ou PBR simplificado.
4. Configurar luz, sombras e ambient occlusion.
5. Adicionar textura procedural leve.
6. Programar elementos ambientais em ciclos com fase diferente.
7. Testar o cenário com um personagem em silhouette antes de detalhar.

## Renderização

- Usar Remotion CLI para prévia e render final.
- Com WebGL/Three.js, verificar a opção GL do Chromium; `angle` é uma opção documentada para ambientes de render headless.
- Fazer stills de controle em frames fixos e um preview antes do render completo.
- Se a máquina não tiver GPU adequada, testar fallback de software com resolução menor e render em lotes.
- Não assumir que um ambiente Claude Desktop/chat dispõe de GPU local, FFmpeg ou permissões de execução. Inspecionar o ambiente.

## Fluxo de instalação de projeto novo

1. Verificar `node --version`, `npm --version`, `python --version`, `ffmpeg -version` e Blender, se usado.
2. Criar projeto Remotion com versão compatível; instalar `remotion`, `@remotion/cli`, `@remotion/three`, `three`, `@react-three/fiber`, React e tipos correspondentes, mantendo as versões Remotion alinhadas.
3. Consultar exemplos/docs da versão efetivamente instalada antes de usar APIs.
4. Criar uma composição curta de teste com um plano, uma câmera e um personagem simples.
5. Renderizar e validar antes de expandir para o vídeo completo.

## Limitações importantes

- Remotion/Three.js pode renderizar a cena via Chromium/WebGL, mas uma skill sozinha não instala drivers ou habilita GPU ausente.
- Blender é complemento; não precisa entrar no caminho crítico de todos os vídeos.
- A complexidade de assets, resolução, fps, número de passes, sombras e DOF afeta custo e tempo de render. Criar qualidade por camadas, não por excesso de polígonos.

## Benchmark externo útil

Existe um projeto open-source próximo ao escopo: [mromidev/claude-animated-shorts](https://github.com/mromidev/claude-animated-shorts), cujo README descreve uma skill Claude com Three.js + Remotion, style bible medido em 20 Shorts, sete relatórios e 20 folhas de contato de referência. Consultar o estado atual do repositório, revisar o código/licença e comparar a implementação antes de adotá-lo. Não incorporar frames, personagens, scripts ou assets de terceiros sem verificar direitos e finalidade permitida.
