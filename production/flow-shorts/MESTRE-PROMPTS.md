# Prompt mestre + negativo mestre + protocolo para gastar menos crédito (Flow)

Vale para TODOS os episódios. Cole o MESTRE uma vez no começo do chat do agente, o NEGATIVO no campo de prompt negativo (ou no fim de cada vídeo) e depois cada vídeo.

## A. PROMPT MESTRE (colar uma vez, no começo do chat)

```
MASTER RULES. These rules apply to EVERY video I ask for in this chat.

FORMAT: each video is exactly 10.0 seconds, vertical portrait 9:16 (no landscape, no blurred bars, no letterbox, no borders), 720p, 24 fps, ONE continuous shot with NO cuts, NO scene changes, NO fades.

FIRST FRAME: the first frame of each video is the attached image with the same number. Reproduce it exactly: same room, same objects in the same places, same lighting, same camera angle and framing, same characters in the same poses. Everything not mentioned in the action stays completely still.

CHARACTERS (identical to their reference sheets in every single frame):
- BENTO: a chubby lop-eared bunny, cream-white with beige patches, big dark eyes, rosy cheeks, a small blue knitted scarf, a short round tail. He has EXACTLY 2 ears: one on the left side and one on the right side of his head. Both ears are soft, floppy and ALWAYS HANG DOWN along the sides of his head, from the first frame to the last. They NEVER stand up, NEVER point up, NEVER spread out sideways like wings. When he moves, his ears only swing gently while hanging. He has exactly 2 eyes, 1 nose, 1 mouth, 2 arms, 2 legs and 1 tail.
- LUNA: a fluffy blue-gray kitten with a white chest and muzzle, big green eyes, a small pink bow at her neck and 1 long fluffy tail. She has EXACTLY 2 small pointed ears standing on top of her head, 2 eyes, 2 arms, 2 legs and 1 tail (always a single tail).
- TICO: a small round caramel-brown monkey with a cream face and belly, big dark eyes, a small green backpack. EXACTLY 2 round ears (one on each side of the head), 2 eyes, 2 arms, 2 legs and 1 long curly tail.
- Hands and paws are simple, soft, rounded, mitten-like shapes. Never show extra fingers or toes.

MOTION: slow and gentle. One main action at a time, exactly as written in the timeline. Small gestures only. No jumping, no hopping, no running, no spinning, no shrugging, no fast head turns, no fast waving. If an action would be hard to do without breaking anatomy, do a simpler version instead (smile, blink, sway very slightly). Characters keep the same size and the same distance from the camera and never leave the frame.

CAMERA: only the camera move written in the video. Otherwise it is locked. Never zoom in or out by more than 5%.

OBJECTS: objects keep their shape, color and number. Nothing appears, disappears, duplicates or changes color. Water is a single stream. Bubbles are few, round, and float slowly.

SOUND: only soft sound effects matched to the action. No music, no singing, no speech, no loud or sudden sounds.

SELF-CHECK (do it silently before delivering each video): count the ears, eyes, arms, legs and tails of every character at 0 s, 2.5 s, 5 s, 7.5 s and 10 s. Bento must show exactly 2 HANGING ears at every moment. If any count is wrong, or any ear of Bento is up, regenerate it before showing me. Do not deliver a video that fails this check.
```

## B. NEGATIVO MESTRE (campo de prompt negativo, ou no fim de cada vídeo depois de "NEGATIVE:")

```
extra ears, third ear, fourth ear, second pair of ears, duplicated ears, upright ears on Bento, ears standing up, ears pointing up, ears spread out like wings, extra arms, extra legs, extra paws, extra fingers, extra toes, extra tails, two tails, extra eyes, extra heads, duplicated body, cloned character, merged bodies, melting, morphing, stretching limbs, twisted limbs, missing limbs, character splitting in two, face changing, color change, size change, outfit change, scarf changing, objects appearing, objects disappearing, duplicated objects, scene cut, fade, camera shake, fast motion, spinning, jumping, hopping, shrugging, text, subtitles, letters, watermark, logo, blurred bars, letterbox, black bars, borders, scary, creepy, dark, sudden movement, loud sound, music, singing, speech
```

## C. Protocolo para gastar menos crédito

1. **Confira a imagem inicial antes do vídeo.** Conte as orelhas. Imagem custa menos que vídeo; não gere vídeo em cima de imagem errada.
2. **Gere primeiro o vídeo mais arriscado** (o que tem 2 personagens se mexendo). Se ele passar, o resto costuma passar.
3. **Não refaça por defeito curto.** Me mande o clipe antes. Defeito de até uns 4 s eu escondo na edição (zoom, corte, troca de ângulo), como fiz no Episódio 2. Só refaça se o defeito durar mais de 4 s ou envolver o corpo todo.
4. **Se falhar, não repita o mesmo prompt.** Mande o clipe que falhou e me diga o que aconteceu: eu simplifico a ação daquele vídeo (menos movimento) e acrescento a regra específica.
5. **Uma geração por vídeo.** Não peça "melhore".
6. **Cole o MESTRE só uma vez** e use o mesmo chat. Assim o agente guarda as regras.
7. **Me mande todos os clipes, inclusive os ruins.** Eu mostro o que dá para aproveitar.

## D. O que causa orelha a mais (o que aprendemos)

- Pulo, quique, ombros levantados e braços abertos: as orelhas do Bento levantam ou abrem como asas.
- Cena aberta com 2 personagens: o modelo "inventa" um segundo par de orelhas.
- Virar a cabeça rápido, ficar de costas, abaixar a cabeça: orelhas se esticam.
- Pouca ação e câmera parada: quase nunca dá erro.
