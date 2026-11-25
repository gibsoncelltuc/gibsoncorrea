# Ep. 1: "🦷 Vamos escovar os dentinhos!" Prompts completos para o Google Flow

Formato: 4 clipes de 10 s = 40 s, vertical 9:16, 720p, com áudio cantado e efeitos gerados pelo próprio Flow.

Ordem de trabalho: **primeiro as imagens, depois os vídeos.** As imagens prendem o visual do Bento, e cada vídeo começa da imagem dele. Assim o personagem fica igual nos 4 pedaços.

---

## Regras de sincronia (já estão dentro dos prompts)

Cada clipe é gerado separado, então a música não vai "continuar" de um para o outro sozinha. Para o corte ficar invisível:

1. **Cada clipe canta um verso inteiro.** Nenhuma frase atravessa o corte.
2. **Respiro nas pontas.** Os primeiros 0,5 s têm só o instrumento. O canto termina até o segundo 9. O último 1 s tem só o instrumento. O corte cai no silêncio do canto.
3. **Mesma música em todos:** mesma voz, 100 BPM, dó maior, só ukulele, palmas e xilofone. Quanto menos instrumentos, menos diferença entre clipes.
4. **Pose de saída = pose de entrada.** O fim de cada clipe combina com a imagem inicial do próximo.
5. **Canto inferior esquerdo livre.** Ali entra o Libras depois. O lado direito fica para os botões do Shorts.

Quando você me mandar os 4 vídeos, eu junto com transição curta, igualo o volume e entrego o arquivo final para você só colocar o Libras.

---

## Opção A: mensagem única para o agente do Flow (tudo de uma vez)

Cole isto no chat do agente. Se ele não fizer tudo, use a Opção B (passo a passo), que tem os mesmos prompts separados.

```
Please create a 40-second vertical (9:16, 720p) kids music short in 4 video clips of 10 seconds each. Work in this order:

STEP 1 - Generate the character reference image (IMAGE 0), then use it as the reference/ingredient in every following image and video so the character looks identical.

STEP 2 - Generate the 4 starting images (IMAGE 1-4), each using IMAGE 0 as reference.

STEP 3 - Generate the 4 videos (CLIP 1-4). Each clip starts from its matching image (CLIP 1 from IMAGE 1, etc.) and uses IMAGE 0 as character reference. Every clip must have generated audio: the sung lyrics in Brazilian Portuguese plus the sound effects described.

Shared style for everything: high-quality stylized 3D animated feature-film look, soft rounded shapes, big expressive eyes, fluffy fur with soft glowing light, warm cinematic lighting, shallow depth of field, rich gentle colors, smooth natural character animation, no on-screen text, no logos, nothing scary. Keep the lower-left corner of every frame a simple, uncluttered background.

Character - Bento: a small chubby fluffy white-and-cream bunny with big shiny round eyes, long floppy ears with soft pink insides, rosy cheeks, tiny blue scarf, always smiling.

Setting: a cozy bright bathroom with soft blue-tiled walls, a small wooden step stool in front of a round sink, a green toothbrush with a round handle, a toothpaste tube, a little cup.

Shared audio for all 4 clips: a cheerful children's song in Brazilian Portuguese, sung by the same warm, gentle young female voice, 100 BPM, C major, accompanied ONLY by ukulele, soft hand claps and xylophone. Each clip: first 0.5 seconds ukulele only, the sung line finishes before second 9, last 1 second ukulele only.

IMAGE 0: character reference sheet of Bento, front view, side view and back view, neutral standing pose, plain white background.
IMAGE 1: Bento standing on the step stool in front of the sink, yawning with eyes half closed, the toothbrush and toothpaste next to him.
IMAGE 2: close medium shot of Bento with the toothbrush in his mouth and small soft white foam bubbles, ears up, happy eyes.
IMAGE 3: close-up of Bento's wide open smile, tiny cute round jelly-like candy creatures in pink, orange and purple with big silly eyes sitting on his teeth giggling, toothbrush ready.
IMAGE 4: Bento holding the little cup of water, mouth closed, cheeks puffed, about to rinse.

CLIP 1: Bento finishes yawning, stretches, hops once on the stool, proudly shows his little white teeth to the camera and picks up the toothbrush, squeezing a tiny bit of toothpaste. Ends holding the brush near his mouth. Sound effects: soft yawn, small hop, toothpaste squeeze. Sung lyrics: "Acordei, bocejei, que sono bom! Pega a escova, pasta pouquinha, vamos lá!"

CLIP 2: Bento brushes slowly in small circles, upper teeth then lower teeth, front then back, clear easy-to-follow motions, soft white foam bubbles growing, ears bouncing to the beat. Ends with a wide foamy smile. Sound effects: gentle brushing scrub in rhythm, little foam bubbles. Sung lyrics: "Em cima, embaixo, devagar, pra frente, pra trás, vou esfregar!"

CLIP 3: The tiny candy creatures, funny and not scary, slide off Bento's teeth as he brushes, wave goodbye and jump into the sink drain; little sparkles pop on each clean tooth. Ends with Bento smiling with clean teeth. Sound effects: tiny giggles, cartoon boings, water drain gurgle, sparkle chimes. Sung lyrics: "Tchau, tchau, bichinho do doce, no meu dentinho você não fica!"

CLIP 4: Bento rinses with the cup of water, gently spits into the sink, turns to the camera with a huge shining smile, sparkles around his teeth, does a happy little dance on the stool and ends with a thumbs-up pose. Sound effects: water swish, small splash in sink, sparkle "ting", cheerful claps. Sung lyrics: "De manhã e de noite, sem reclamar, sorriso brilhando, vem cantar!"
```

---

## Opção B: passo a passo (se o agente não fizer tudo de uma vez)

### Passo 1: imagens

**IMAGEM 0: ficha do personagem**
```
Character reference sheet of Bento: a small chubby fluffy white-and-cream bunny with big shiny round eyes, long floppy ears with soft pink insides, rosy cheeks, tiny blue scarf, always smiling. Front view, side view and back view, neutral standing pose, plain white background. High-quality stylized 3D animated feature-film look, soft rounded shapes, big expressive eyes, fluffy fur, warm cinematic lighting, gentle rich colors, no text, no logos.
```

Para as imagens 1 a 4, **anexe a IMAGEM 0 como referência** e use formato vertical 9:16.

**IMAGEM 1**
```
Using the reference character Bento (chubby fluffy white-and-cream bunny, big shiny round eyes, floppy ears with soft pink insides, rosy cheeks, tiny blue scarf). Bento standing on a small wooden step stool in front of the sink in a cozy bright bathroom with soft blue-tiled walls, yawning with eyes half closed, a green toothbrush and a toothpaste tube next to him. High-quality stylized 3D animated feature-film look, soft rounded shapes, warm cinematic lighting, gentle rich colors, vertical 9:16, lower-left corner simple and uncluttered, no text, no logos.
```

**IMAGEM 2**
```
Using the reference character Bento (chubby fluffy white-and-cream bunny, big shiny round eyes, floppy ears with soft pink insides, rosy cheeks, tiny blue scarf). Close medium shot of Bento in the cozy bright bathroom with soft blue-tiled walls with the green toothbrush in his mouth and small soft white foam bubbles, ears up, happy eyes. High-quality stylized 3D animated feature-film look, soft rounded shapes, warm cinematic lighting, gentle rich colors, vertical 9:16, lower-left corner simple and uncluttered, no text, no logos.
```

**IMAGEM 3**
```
Using the reference character Bento (chubby fluffy white-and-cream bunny, big shiny round eyes, floppy ears with soft pink insides, rosy cheeks, tiny blue scarf). Close-up of Bento's wide open smile in the cozy bright bathroom with soft blue-tiled walls, tiny cute round jelly-like candy creatures in pink, orange and purple with big silly eyes sitting on his teeth and giggling, friendly and not scary, the green toothbrush ready. High-quality stylized 3D animated feature-film look, soft rounded shapes, warm cinematic lighting, gentle rich colors, vertical 9:16, lower-left corner simple and uncluttered, no text, no logos.
```

**IMAGEM 4**
```
Using the reference character Bento (chubby fluffy white-and-cream bunny, big shiny round eyes, floppy ears with soft pink insides, rosy cheeks, tiny blue scarf). Bento on the step stool holding a little cup of water, mouth closed, cheeks puffed, about to rinse, cozy bright bathroom with soft blue-tiled walls. High-quality stylized 3D animated feature-film look, soft rounded shapes, warm cinematic lighting, gentle rich colors, vertical 9:16, lower-left corner simple and uncluttered, no text, no logos.
```

### Passo 2: vídeos

Para cada clipe, **comece pela imagem do mesmo número** (quadro inicial) e anexe a IMAGEM 0 como referência. Modelo: Omni 1.1 Flash, 720p, 9:16, 10 s.

**CLIPE 1 (começa da IMAGEM 1)**
```
High-quality stylized 3D animated feature-film look, soft rounded shapes, big expressive eyes, fluffy fur with soft glowing light, warm cinematic lighting, shallow depth of field, rich gentle colors, smooth natural character animation, vertical 9:16, no on-screen text, no logos, nothing scary. Bento the chubby fluffy white-and-cream bunny with a tiny blue scarf finishes yawning, stretches, hops once on the step stool, proudly shows his little white teeth to the camera and picks up the green toothbrush, squeezing a tiny bit of toothpaste. Ends holding the brush near his mouth.
Audio: cheerful children's song in Brazilian Portuguese, warm gentle young female voice, 100 BPM, C major, only ukulele, soft hand claps and xylophone. First 0.5 s ukulele only; sung line ends before second 9; last 1 s ukulele only. Sound effects: soft yawn, small hop, toothpaste squeeze.
Sung lyrics: "Acordei, bocejei, que sono bom! Pega a escova, pasta pouquinha, vamos lá!"
```

**CLIPE 2 (começa da IMAGEM 2)**
```
High-quality stylized 3D animated feature-film look, soft rounded shapes, big expressive eyes, fluffy fur with soft glowing light, warm cinematic lighting, shallow depth of field, rich gentle colors, smooth natural character animation, vertical 9:16, no on-screen text, no logos, nothing scary. Bento the chubby fluffy white-and-cream bunny with a tiny blue scarf brushes his teeth slowly in small circles, upper teeth then lower teeth, front then back, clear easy-to-follow motions, soft white foam bubbles growing, ears bouncing to the beat. Ends with a wide foamy smile.
Audio: cheerful children's song in Brazilian Portuguese, warm gentle young female voice, 100 BPM, C major, only ukulele, soft hand claps and xylophone. First 0.5 s ukulele only; sung line ends before second 9; last 1 s ukulele only. Sound effects: gentle brushing scrub in rhythm, little foam bubbles.
Sung lyrics: "Em cima, embaixo, devagar, pra frente, pra trás, vou esfregar!"
```

**CLIPE 3 (começa da IMAGEM 3)**
```
High-quality stylized 3D animated feature-film look, soft rounded shapes, big expressive eyes, fluffy fur with soft glowing light, warm cinematic lighting, shallow depth of field, rich gentle colors, smooth natural character animation, vertical 9:16, no on-screen text, no logos, nothing scary. Tiny funny round jelly-like candy creatures in pink, orange and purple with big silly eyes slide off Bento's teeth as he brushes, wave goodbye and jump into the sink drain; little sparkles pop on each clean tooth. Ends with Bento, the chubby fluffy white-and-cream bunny with a tiny blue scarf, smiling with clean teeth.
Audio: cheerful children's song in Brazilian Portuguese, warm gentle young female voice, 100 BPM, C major, only ukulele, soft hand claps and xylophone. First 0.5 s ukulele only; sung line ends before second 9; last 1 s ukulele only. Sound effects: tiny giggles, cartoon boings, water drain gurgle, sparkle chimes.
Sung lyrics: "Tchau, tchau, bichinho do doce, no meu dentinho você não fica!"
```

**CLIPE 4 (começa da IMAGEM 4)**
```
High-quality stylized 3D animated feature-film look, soft rounded shapes, big expressive eyes, fluffy fur with soft glowing light, warm cinematic lighting, shallow depth of field, rich gentle colors, smooth natural character animation, vertical 9:16, no on-screen text, no logos, nothing scary. Bento the chubby fluffy white-and-cream bunny with a tiny blue scarf rinses with the cup of water, gently spits into the sink, turns to the camera with a huge shining smile, sparkles around his teeth, does a happy little dance on the stool and ends with a thumbs-up pose.
Audio: cheerful children's song in Brazilian Portuguese, warm gentle young female voice, 100 BPM, C major, only ukulele, soft hand claps and xylophone. First 0.5 s ukulele only; sung line ends before second 9; last 1 s ukulele only. Sound effects: water swish, small splash in the sink, sparkle "ting", cheerful claps.
Sung lyrics: "De manhã e de noite, sem reclamar, sorriso brilhando, vem cantar!"
```

---

## Checklist antes de me mandar

- [ ] O Bento está igual nos 4? Se um saiu diferente, gere de novo só aquele.
- [ ] A letra saiu em português e dá para entender? Se uma palavra saiu errada, gere de novo aquele clipe.
- [ ] Nenhum texto escrito apareceu na tela?
- [ ] Mande os 4 arquivos, **um por mensagem**, na ordem 1, 2, 3, 4.
