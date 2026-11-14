# Sistema de produção reutilizável

## Objetivo

Transformar o projeto em uma biblioteca audiovisual evolutiva, em vez de reconstruir personagens, cenário e câmera do zero em cada vídeo.

## Registries

Manter arquivos versionados:
- `registries/characters.json`
- `registries/rigs.json`
- `registries/expressions.json`
- `registries/motions.json`
- `registries/environments.json`
- `registries/props.json`
- `registries/materials.json`
- `registries/cameras.json`
- `registries/audio-presets.json`
- `registries/assets.json`

Cada item deve conter `id`, `version`, `description`, `file`, `dependencies`, `license`, `author/source`, `hash`, `compatibility` e `test_scene`.

## Character rig contract

Um rig padrão deve expor pivôs e controles estáveis: root, hips, torso, neck, head, eyes, pupils, brows, mouth, shoulders, upper arms, forearms, hands, thighs, shins, feet e accessories. Personagens simplificados podem omitir partes, mas devem manter o contrato com valores neutros.

Expressões são presets combináveis: neutral, curious, skeptical, surprised, afraid, angry, amused, confused, focused, relieved, determined, sad. A expressão é composta por olhos/sobrancelhas/boca e pode ser interpolada.

## Motion contract

Cada movimento recebe `startFrame`, `durationFrames`, `seed`, `intensity`, `target`, `priority` e `blendMode`. Ações compostas devem incluir antecipação, ação, contato, reação e recuperação quando apropriado.

Biblioteca inicial: idle_breath, idle_weight_shift, blink, look_at, head_turn, point, shrug, gasp, recoil, nod, shake_head, walk, run, stop, reach, grasp, pull, push, lift, drop, stumble, sit, stand, speak, laugh, whisper, explain.

## Camera contract

Cada preset recebe `position`, `lookAt`, `fov`, `roll`, `focusTarget`, `dof`, `startFrame`, `durationFrames`, `easing` e `motivation`. Presets: establish, push_in, pull_back, lateral_glide, orbit_reveal, tilt_reveal, rack_focus, insert_macro, reaction_closeup, tracking_follow, overhead_diagram.

## Continuidade

Validar entre planos: screen direction, eixo de 180°, posição relativa, escala, mão ocupada, prop state, olhar, direção de luz, clima, hora e continuidade de figurino. Quando houver salto temporal/espacial, sinalizar visualmente.

## Asset provenance e segurança

Não baixar modelos/texturas de forma automática sem verificar licença, atribuição, restrições comerciais e origem. Não usar assets de terceiros sem registrar a licença no registry. Não incorporar referência privada do canal ao pacote distribuível.

## Render escalável

- Cache de modelos, texturas, áudio e bundles.
- Render segmentado por cena ou intervalo de frames.
- Manifesto com hash dos inputs e parâmetros.
- Reexecução apenas dos segmentos alterados.
- Arquivo de logs e tempo por frame.
- Perfis `preview`, `draft`, `final` e `archive`.
