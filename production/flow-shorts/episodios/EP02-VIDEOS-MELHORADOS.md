# Ep. 02: seleção das imagens e prompts de vídeo melhorados

## Imagens escolhidas (anexar nesta ordem, como imagem 1 a 6)

| # | Arquivo | Cena |
|---|---|---|
| 1 | 347374167_1794950238948966.jpeg | Bento surpreso, mãos nas bochechas, quarto bagunçado |
| 2 | 150467485_1794950243945254.jpeg | Porta: Tico com as mãos na cintura, Bento dando de ombros |
| 3 | 121418709_1794950255565207.jpeg | Bento com a bola listrada perto da caixa, Tico com o carrinho |
| 4 | 100267205_1794950262557368.jpeg | Bento abraçando o ursinho perto da cama, Tico sentado |
| 5 | 425262207_1794951857033596.jpeg | Tico espiando atrás da caixa azul, bola vermelha no chão |
| 6 | 553042718_1794950282520479.jpeg | Bento e Tico segurando a bola vermelha, quarto arrumado |

Descartada: 668144145_1794950250607955.jpeg (a imagem saiu em 16:9 com faixas borradas em cima e embaixo).

## Mensagem para o agente do Flow (os 6 vídeos)

```
CONTEXT: I am making a 60-second vertical kids' short as 6 video clips of 10 seconds each. Generate the 6 videos ONE AT A TIME, in numbered order (video 1, then 2, ... then 6). For each video, use the attached image with the same number as its FIRST FRAME (image 1 -> video 1, image 2 -> video 2, and so on). Use the attached character sheets SHEET-BENTO and SHEET-TICO as the references for the characters. Each video is exactly 10 seconds, vertical 9:16, 720p.

CONTINUITY: Keep the room, the rug, the lighting, the toys and the characters exactly as in the first-frame image. Do not add or remove toys. The characters look identical to their sheets from the first frame to the last frame.

BENTO: a lop-eared bunny with exactly TWO soft floppy ears that ALWAYS hang down along both sides of his head, one on each side. His ears NEVER stand upright and he NEVER has a second pair of ears. Bento has exactly 2 eyes, 2 arms, 2 legs and 1 small round tail.
TICO: a small monkey with exactly 2 eyes, 2 round ears, 2 arms, 2 legs and 1 curly tail.

STYLE: high-quality stylized 3D animated feature-film look, soft rounded shapes, big expressive eyes, fluffy fur, warm cinematic lighting, smooth natural character animation, no text, no letters, no logos, nothing scary. Keep the lower-left corner of the frame simple and uncluttered.

MOVEMENT RULES: one slow, simple, continuous action per clip, exactly as described; all body parts stay attached and in view; ears only sway gently; no fast spinning; no camera shake; no cuts inside the clip.

AUDIO: ONLY soft sound effects. No music, no singing, no speech.

NEGATIVE: upright or standing ears, a second pair of ears, three or four ears, extra or duplicated arms, legs, hands, fingers, tails, eyes, heads; merged or melting limbs; a character splitting or morphing; color, size or outfit changes; characters appearing or disappearing; toys appearing or multiplying; text, letters, logos; scary or sudden elements.

VIDEO 1 (first frame = image 1; use SHEET-BENTO)
First frame: Bento stands on a round woven cream rug in a messy kid's bedroom, both hands on his cheeks, surprised and happy. Toys are scattered around him (blocks, a red toy car, a red ball, a teddy bear lying down). An open blue toy box is at the left, a bed with a yellow blanket at the right.
Action: 0-3 s Bento slowly lowers his hands from his cheeks and looks around at the toys, turning his head gently left, then right. 3-7 s he lifts one arm and points toward the open blue toy box on the left, then bounces gently twice on the spot. 7-10 s he turns to the camera with a big smile and a small nod.
Camera: slow, steady push-in.
Last frame: Bento facing the camera, smiling, arms relaxed.
Sound effects: soft toy clinks, two light bounces, a small happy chime.

VIDEO 2 (first frame = image 2; use SHEET-BENTO and SHEET-TICO)
First frame: seen through an open bedroom door, Tico (left, hands on his hips, puzzled face) and Bento (right, arms open in a shrug) stand on the floor of a messy room full of colorful blocks, a toy car, a red ball and a teddy bear. A blue toy box, a bed with a yellow blanket and a bookshelf are behind them.
Action: 0-3 s Tico slowly looks across the floor from left to right with a puzzled face. 3-7 s Tico shrugs his shoulders and takes his hands off his hips; Bento shrugs with open palms and turns his head toward Tico. 7-10 s they look at each other, then both look back at the messy room and nod once.
Camera: locked, no movement.
Last frame: both standing side by side, facing the messy room.
Sound effects: a soft puzzled "hmm" xylophone tune, two light boings.

VIDEO 3 (first frame = image 3; use SHEET-BENTO and SHEET-TICO)
First frame: Bento stands on a rainbow rug beside an open blue toy box, holding a striped ball. Tico stands on the right near a wooden bookshelf, holding a small toy car. Colorful blocks are scattered on the rug, a red ball is at the right edge, a teddy bear lies at the bottom left.
Action: 0-3 s Bento gently puts the striped ball into the open toy box. 3-7 s he picks up one colorful block from the rug and puts it into the box while Tico takes one step toward the shelf. 7-10 s Tico sets the toy car on the lower shelf of the bookshelf and steps back; Bento picks up another block.
Camera: a short, slow, gentle move to the right.
Last frame: the toy car on the shelf, Bento holding a block above the toy box.
Sound effects: soft block clunks, a small car roll, a light pop.

VIDEO 4 (first frame = image 4; use SHEET-BENTO and SHEET-TICO)
First frame: Tico sits on a patterned cream rug at the left, talking with a happy face. Bento sits next to a wooden bed with a yellow blanket, hugging a brown teddy bear. Blocks, a red ball and a toy car are on the rug; a blue toy bin with a star is at the back.
Action: 0-3 s Bento looks at Tico and smiles, still hugging the teddy bear. 3-7 s Bento turns toward the bed, places the teddy bear gently on the pillow and pats its head once. 7-10 s Tico claps his hands twice and both smile. Both stay sitting.
Camera: very slow push-in.
Last frame: the teddy bear on the bed, Bento and Tico sitting and smiling.
Sound effects: a soft thump on the bed, two gentle claps, a light giggle.

VIDEO 5 (first frame = image 5; use SHEET-TICO)
First frame: Tico peeks from behind the left side of a blue toy box, one hand on the box edge, smiling. A red ball lies on the patterned rug at the bottom right. Toy shelves are behind, a bed with a yellow blanket is at the left.
Action: 0-3 s Tico steps out from behind the box and looks down at the red ball. 3-7 s he walks to the ball, bends down and picks it up with both hands. 7-10 s he lifts the ball up in front of him with a joyful face.
Camera: a slow pull-back that reveals more of the room.
Last frame: Tico holding the red ball up, smiling.
Sound effects: a surprise "ting", soft footsteps, a happy boing.

VIDEO 6 (first frame = image 6; use SHEET-BENTO and SHEET-TICO)
First frame: in a tidy bedroom, Bento and Tico stand facing each other on a rainbow round rug, both holding a red ball between them, smiling. A blue toy box and a bookshelf are at the left, a bed with a yellow blanket at the right.
Action: 0-3 s Tico gently hands the ball to Bento. 3-6 s Bento holds the ball, smiles and gently hands it back. 6-10 s both turn to the camera and wave one hand, smiling.
Camera: slow, gentle push-in.
Last frame: both waving at the camera.
Sound effects: a soft ball tap, cheerful claps, a sparkle chime.

CHECK: after each video, check it frame by frame. Count the ears, eyes, arms, legs and tails of every character at the start, middle and end. If any character ever has extra or duplicated body parts, an upright ear, or changes look, regenerate that video (up to 2 times) before moving on. When all 6 are done, show them in order.
```
