#!/usr/bin/env python3
"""Gera a bíblia do canal e os 10 episódios (prompts completos para o Google Flow).

Uso: python3 gerar_pacote.py   (escreve em ../ e ../episodios/)
Para mudar um prompt, edite os dados abaixo e rode de novo.
"""
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
EPS_DIR = os.path.join(BASE, "episodios")
os.makedirs(EPS_DIR, exist_ok=True)

# ----------------------------------------------------------------- BLOCOS FIXOS
STYLE = ("High-quality stylized 3D animated feature-film look, soft rounded shapes, big expressive eyes, "
         "fluffy fur, warm cinematic lighting, shallow depth of field, rich gentle colors, smooth natural "
         "character animation, vertical 9:16, no on-screen text, no logos, nothing scary.")

NEG_VIDEO = ("NEGATIVE: upright or standing ears, a second pair of ears, three or four ears, extra or duplicated ears, arms, legs, hands, fingers, tails, eyes, heads; merged or "
             "melting limbs; a character splitting or morphing; color, size or outfit changes; characters appearing "
             "or disappearing; on-screen text, logos; scary or sudden elements or sounds; camera shake; fast spinning.")

NEG_IMG = ("NEGATIVE (never show): upright or standing ears, a second pair of ears, three or four ears, extra or duplicated ears, arms, legs, hands, fingers, tails, eyes or heads; "
           "merged or distorted limbs; text, letters, watermarks, logos; scary or dark elements; any character "
           "different from the reference sheets.")

MUSIC = ("Audio: original cheerful Brazilian children's pop song, same arrangement in every clip: 96 BPM, C major, "
         "ukulele, shaker, hand claps on beats 2 and 4, glockenspiel melody, soft bass; the same warm young "
         "female lead voice singing in Brazilian Portuguese, hook doubled by 4 children. Exactly 4 bars: vocal "
         "starts on beat 1, line 1 in bars 1-2, line 2 in bars 3-4; the music keeps flowing, no intro, no ending, "
         "no fade, no silence.")

RULE_VIDEO = ("Slow, simple, single continuous action; all body parts stay attached and in view; Bento's two "
              "floppy ears always hang down and only sway gently; identical look to the reference sheets throughout; lower-left corner stays uncluttered.")

# ----------------------------------------------------------------- PERSONAGENS
# nome -> (descrição, trava de anatomia)
CAST = {
    "Bento": ("Bento: a small chubby fluffy white-and-cream lop-eared bunny with big shiny dark round eyes, exactly TWO "
              "soft floppy ears that ALWAYS hang down along both sides of the head (one on each side, pink inside), "
              "NEVER standing upright, rosy cheeks, a small blue knitted scarf, a small round fluffy tail",
              "Bento has exactly 2 ears, both floppy and hanging down beside his cheeks (never upright, never a second "
              "pair), exactly 2 eyes, 2 arms, 2 legs and 1 small round tail"),
    "Luna": ("Luna: a small fluffy blue-gray kitten with big shiny green eyes, two small pointed ears with pink "
             "insides, a white chest, a small pink bow at her neck, one long curved tail",
             "Luna has exactly 2 eyes, 2 small pointed ears, 2 arms, 2 legs and 1 long tail"),
    "Tico": ("Tico: a small round caramel-brown monkey with big shiny dark eyes, a cream face and belly, two round "
             "ears, one long curly tail, a small green backpack",
             "Tico has exactly 2 eyes, 2 round ears, 2 arms, 2 legs and 1 curly tail"),
    "Pipo": ("Pipo: a tiny round fluffy yellow duckling with big shiny black eyes, a small orange beak, two tiny "
             "wings, two orange webbed feet, a tiny red bow tie",
             "Pipo has exactly 2 eyes, 1 beak, 2 wings and 2 feet"),
    "Olívia": ("Olívia: a gentle round brown owl with big shiny golden eyes, a cream heart-shaped face, two small "
               "ear tufts, soft wings, an orange bow tie, kind and calm",
               "Olívia has exactly 2 eyes, 2 ear tufts, 2 wings and 2 feet"),
    "Nina": ("Nina: a cheerful 5-year-old girl with light-brown skin, big shiny dark eyes, two curly puffs of dark "
             "hair tied with yellow ribbons, rosy cheeks, a green dress and white shoes",
             "Nina has exactly 2 eyes, 2 hair puffs, 2 arms with 2 simple relaxed hands, and 2 legs"),
    "Davi": ("Davi: a cheerful 5-year-old boy with light-tan skin, big shiny brown eyes, short wavy dark hair, "
             "rosy cheeks, an orange t-shirt, blue shorts and white sneakers",
             "Davi has exactly 2 eyes, 2 arms with 2 simple relaxed hands, and 2 legs"),
    "Docinhos": ("Docinhos: tiny round jelly-like candy creatures in pink, orange and purple, each with two big "
                 "silly eyes and a small smile, funny and friendly, never scary",
                 "each Docinho has exactly 2 eyes and a round body without arms or legs"),
}

SHORT = {
    "Bento": "Bento (chubby fluffy white-and-cream lop-eared bunny with exactly two floppy ears hanging down, blue scarf)",
    "Luna": "Luna (fluffy blue-gray kitten, pink bow)",
    "Tico": "Tico (round caramel-brown monkey, green backpack)",
    "Pipo": "Pipo (tiny yellow duckling, red bow tie)",
    "Olívia": "Olívia (round brown owl, orange bow tie)",
    "Nina": "Nina (5-year-old girl, two curly hair puffs with yellow ribbons, green dress)",
    "Davi": "Davi (5-year-old boy, short wavy hair, orange t-shirt, blue shorts)",
    "Docinhos": "the Docinhos (tiny round jelly candy creatures in pink, orange and purple)",
}

SHEET_EXTRA = {
    "Bento": "the hero of the series",
    "Luna": "Bento's best friend",
    "Tico": "Bento's playful friend",
    "Pipo": "a sweet little friend",
    "Olívia": "the wise, kind teacher and guardian of the group",
    "Nina": "a kind child friend",
    "Davi": "a kind child friend",
    "Docinhos": "three of them side by side in pink, orange and purple, only to be used in the toothbrushing episode",
}


def sheet_prompt(name):
    d, lock = CAST[name]
    return (f"Character reference sheet of {d}. {SHEET_EXTRA[name].capitalize()}. Front view, side view, back view "
            f"and one happy close-up of the face, neutral standing pose, plain white background, evenly spaced. "
            f"{lock}. {STYLE.replace('vertical 9:16, ', '')} Wide horizontal sheet. {NEG_IMG}")


# ----------------------------------------------------------------- EPISÓDIOS
# shot: cam, img (composição da imagem inicial), act (ação do vídeo), sfx, l1, l2, chars (quem aparece)
EPISODES = [
 dict(num=1, slug="escovar-os-dentes", titulo="Escova, Escova, Vai!", tema="Escovar os dentes de manhã e de noite",
  cast=["Bento", "Docinhos"],
  setting="a cozy bright bathroom with soft blue-tiled walls, a small wooden step stool in front of a round white sink, a green toothbrush with a round handle, a small toothpaste tube, a little blue cup",
  yt_titulo="🦷 Escova, Escova, Vai! | Música infantil para escovar os dentes #shorts",
  yt_desc="O Bento ensina a escovar os dentinhos de manhã e de noite! Cante junto! 🐰🦷",
  shots=[
   dict(cam="medium close-up, eye level, slow push-in", chars=["Bento"],
        img="Bento standing on the step stool facing the camera with a big open happy smile, holding the green toothbrush up like a microphone",
        act="Bento bounces gently on the beat, waves the toothbrush in time with the song and winks at the camera",
        sfx="soft sparkle chime on beat 1, light foot taps on the stool",
        l1="Escova, escova, vai, vai, vai!", l2="Dentinho limpo, ai, ai, ai!"),
   dict(cam="medium shot, slow side move", chars=["Bento"],
        img="Bento on the stool, awake and smiling with a tiny yawn, reaching for the toothpaste tube on the sink edge",
        act="Bento stretches both arms up, then picks up the toothpaste and squeezes a pea-sized dot onto the brush",
        sfx="soft yawn, toothpaste squeeze pop",
        l1="De manhã e de noite, sem chorar,", l2="pasta de ervilha vou colocar!"),
   dict(cam="close-up on the face, front view, steady", chars=["Bento"],
        img="close-up of Bento's smiling face with the toothbrush at his mouth and a little white foam",
        act="Bento brushes slowly in small circles, first the top teeth then the bottom teeth, soft foam bubbles grow",
        sfx="gentle brushing scrub on the beat, tiny foam bubbles",
        l1="Em cima, embaixo, devagar,", l2="pra frente e pra trás, vou esfregar!"),
   dict(cam="medium shot, fun and bouncy", chars=["Bento", "Docinhos"],
        img="Bento on the stool with foam on his mouth, three tiny Docinhos peeking over the edge of the sink, giggling",
        act="Bento does a little shimmy on the beat while brushing, the three Docinhos bounce along on the sink edge",
        sfx="hand claps, tiny giggles, light boing on beats 2 and 4",
        l1="Escova, escova, vai, vai, vai!", l2="Dentinho limpo, ai, ai, ai!"),
   dict(cam="close-up, slow push-in", chars=["Bento", "Docinhos"],
        img="close-up of Bento's open smile with two Docinhos sitting on a tooth looking surprised, the toothbrush approaching",
        act="the toothbrush gently sweeps and the Docinhos slide off the teeth one by one, wave goodbye and hop down the drain, sparkles pop on each clean tooth",
        sfx="tiny giggles, cartoon boings, soft drain gurgle, sparkle chimes",
        l1="Tchau, tchau, docinho, vai embora já,", l2="meu dentinho limpo vai brilhar!"),
   dict(cam="medium shot, gentle push-in", chars=["Bento"],
        img="Bento on the stool holding the little blue cup with puffed cheeks, ready to rinse",
        act="Bento rinses, gently spits into the sink, turns to the camera with a huge shining smile and a thumbs-up, sparkles glint on his teeth",
        sfx="water swish, small splash, sparkle ting, cheerful claps",
        l1="Escova, escova, vai, vai, vai!", l2="Sorriso brilhando, ai, ai, ai!"),
  ]),
 dict(num=2, slug="guardar-os-brinquedos", titulo="Guarda, Guarda, Guarda Lá", tema="Guardar os brinquedos e cuidar das suas coisas",
  cast=["Bento", "Tico"],
  setting="a bright cozy kid's bedroom with a soft round rug, a low wooden shelf, a big blue toy box, a small bed with a yellow blanket, toys scattered on the floor: colorful rounded blocks, a toy car, a teddy bear, a red ball",
  yt_titulo="🧸 Guarda, Guarda, Guarda Lá | Música infantil para arrumar o quarto #shorts",
  yt_desc="O Bento e o Tico ensinam a guardar cada brinquedo no seu lugar! 🧸🐰🐵",
  shots=[
   dict(cam="medium shot, eye level, slow push-in", chars=["Bento"],
        img="Bento standing in the middle of the room full of scattered toys, hands on his cheeks with a surprised happy face",
        act="Bento points at the toys and bounces on the beat, then opens one arm toward the blue toy box",
        sfx="toy clinks, light pops, claps on beats 2 and 4",
        l1="Guarda, guarda, guarda lá,", l2="cada coisa em seu lugar!"),
   dict(cam="wide shot of the doorway, steady", chars=["Bento", "Tico"],
        img="Tico standing at the bedroom door looking at the messy floor, Bento next to him with an open-armed shrug",
        act="Tico looks around the floor and shrugs with a puzzled face, Bento shrugs too and they look at each other",
        sfx="soft boing, curious xylophone notes",
        l1="Quanta bagunça no meu chão!", l2="Cadê a bola? Eu não sei, não!"),
   dict(cam="medium shot, slow side move", chars=["Bento", "Tico"],
        img="Bento kneeling next to the blue toy box holding a rounded block, Tico near the low shelf holding a toy car",
        act="Bento puts three colorful blocks one by one into the toy box on the beat, Tico places the toy car on the low shelf",
        sfx="soft block clunks on the beat, small car roll",
        l1="Blocos na caixa, um, dois, três,", l2="carrinho na estante de uma vez!"),
   dict(cam="medium shot, bouncy", chars=["Bento", "Tico"],
        img="Bento hugging the teddy bear next to the small bed, Tico smiling beside him",
        act="Bento sets the teddy bear on the bed and pats it, Tico claps, both bounce gently on the beat",
        sfx="soft thump on the bed, claps, light giggles",
        l1="Guarda, guarda, guarda lá,", l2="cada coisa em seu lugar!"),
   dict(cam="close-up, then pull back, slow", chars=["Tico"],
        img="Tico crouching behind the toy box with a surprised smile, the red ball just visible",
        act="Tico peeks behind the toy box, finds the red ball and lifts it up with joy",
        sfx="surprise ting, happy boing, light claps",
        l1="Olha só quem estava ali atrás,", l2="a bolinha! Que bom, que bom, demais!"),
   dict(cam="wide shot of the tidy room, gentle push-in", chars=["Bento", "Tico"],
        img="the whole room neat and tidy, Bento and Tico in the middle holding the red ball between them, smiling",
        act="Bento and Tico gently pass the ball to each other once and then turn to the camera and wave",
        sfx="soft ball bounce, cheerful claps, sparkle ting",
        l1="Guarda, guarda, guarda lá,", l2="cada coisa em seu lugar!"),
  ]),
 dict(num=3, slug="mao-dada-na-rua", titulo="Mão na Mão", tema="Obedecer e atravessar a rua com segurança, de mão dada com um adulto",
  cast=["Bento", "Luna", "Olívia"],
  setting="a sunny cartoon street corner with a wide striped crosswalk, a round traffic light with big clear red and green lights, a leafy tree, a few quiet small colorful cars waiting far back behind the stop line",
  yt_titulo="🚦 Mão na Mão | Música infantil sobre atravessar a rua #shorts",
  yt_desc="O Bento e a Luna aprendem a atravessar a rua de mão dada com um adulto! 🚦🐰🐱",
  shots=[
   dict(cam="medium shot, eye level, slow push-in", chars=["Bento", "Luna", "Olívia"],
        img="Bento and Luna standing at the curb, each holding one of Olívia's wings, all three smiling at the camera",
        act="the three sway gently on the beat holding hands, and Bento looks left and right once",
        sfx="soft bird chirp, light claps, glockenspiel sparkle",
        l1="Mão na mão, olha pra lá, olha pra cá,", l2="só atravesso quando o sinal mudar!"),
   dict(cam="medium shot with the traffic light visible, steady", chars=["Bento", "Luna", "Olívia"],
        img="the three waiting at the curb while the traffic light above shows a clear red light",
        act="the red light glows, the three stop at the curb, Bento lifts one paw in a calm stop gesture",
        sfx="soft traffic light beep, gentle car hum far away",
        l1="O sinal ficou vermelho, vamos parar!", l2="A gente espera, sem correr, sem pular!"),
   dict(cam="medium shot, slow side move", chars=["Bento", "Luna"],
        img="Bento and Luna at the curb with their heads turned to the left, quiet cars waiting far back",
        act="Bento and Luna turn their heads slowly to the left, then to the right, on the beat, nodding that the street is calm",
        sfx="soft whoosh on each head turn, small ting",
        l1="Olha pra esquerda, olha pra direita,", l2="carrinho parado, a rua tá certa!"),
   dict(cam="medium shot, bouncy", chars=["Bento", "Luna", "Olívia"],
        img="the three standing at the curb holding hands, smiling and swaying",
        act="the three sway side to side on the beat holding hands, Olívia gently flaps her free wing",
        sfx="claps on beats 2 and 4, soft bird chirp",
        l1="Mão na mão, olha pra lá, olha pra cá,", l2="só atravesso quando o sinal mudar!"),
   dict(cam="wide shot of the crosswalk, tracking", chars=["Bento", "Luna", "Olívia"],
        img="the traffic light shows green, the three at the start of the crosswalk, the cars still waiting far back",
        act="the light turns green and the three walk calmly across the crosswalk holding hands, at a slow steady pace",
        sfx="green light ding, soft footsteps on the beat",
        l1="O verde acendeu, é hora de ir,", l2="passo por passo, sem se distrair!"),
   dict(cam="medium shot on the far sidewalk, gentle push-in", chars=["Bento", "Luna", "Olívia"],
        img="the three on the far sidewalk, smiling, still holding hands",
        act="the three reach the other side, hug gently and wave happily at the camera",
        sfx="happy sparkle chime, cheerful claps",
        l1="Mão na mão, olha pra lá, olha pra cá,", l2="só atravesso quando o sinal mudar!"),
  ]),
 dict(num=4, slug="lavar-as-maos", titulo="Lava, Lava as Mãozinhas", tema="Lavar as mãos antes de comer",
  cast=["Luna", "Bento"],
  setting="a bright cozy kitchen with a low white sink, a wooden step stool, a pump bottle of pink soap, a soft yellow towel, a small table with a plate of sliced apples",
  yt_titulo="🫧 Lava, Lava as Mãozinhas | Música infantil para lavar as mãos #shorts",
  yt_desc="A Luna e o Bento ensinam a lavar as mãozinhas antes de comer! 🫧🐱🐰",
  shots=[
   dict(cam="medium close-up, eye level, slow push-in", chars=["Luna"],
        img="Luna on the step stool at the sink smiling at the camera, both paws raised with soap bubbles on them",
        act="Luna bounces gently on the beat and rubs her paws together with bubbles, then shows them to the camera",
        sfx="soft soap bubble pops, sparkle chime on beat 1",
        l1="Lava, lava, lava as mãozinhas,", l2="esfrega, esfrega, bolhinhas!"),
   dict(cam="medium shot, slow side move", chars=["Luna", "Bento"],
        img="Bento and Luna standing near the sink with slightly dirty paws, Bento holding a toy car, a bit of cartoon dirt on his paws",
        act="Bento shows his dirty paws, Luna shakes her head playfully and points to the sink",
        sfx="soft boing, playful xylophone notes",
        l1="Brincou na terra, pegou no chão,", l2="mãozinha suja, não, não, não!"),
   dict(cam="close-up on the paws at the sink, steady", chars=["Luna"],
        img="close-up of Luna's two paws under the running tap with soft bubbles",
        act="Luna rubs her paws palm to palm, then the backs, then between the fingers, slowly on the beat, bubbles grow",
        sfx="running water, soft rubbing, bubbles on the beat",
        l1="Palma com palma, as costas também,", l2="entre os dedinhos, sem esquecer ninguém!"),
   dict(cam="medium shot, bouncy", chars=["Luna", "Bento"],
        img="Luna and Bento side by side at the sink, both with bubbly paws, smiling",
        act="Luna and Bento both rub their paws, bouncing gently on the beat, bubbles float up",
        sfx="claps on beats 2 and 4, bubble pops",
        l1="Lava, lava, lava as mãozinhas,", l2="esfrega, esfrega, bolhinhas!"),
   dict(cam="close-up, then medium, slow", chars=["Luna", "Bento"],
        img="Bento holding his clean paws under the tap, rinsing, Luna holding the yellow towel",
        act="Bento rinses the bubbles away, Luna hands him the towel and he dries his paws gently",
        sfx="rinsing water, soft towel rustle, sparkle ting",
        l1="Enxágua bem, seca também,", l2="mãozinha limpa faz bem, faz bem!"),
   dict(cam="medium shot at the little table, gentle push-in", chars=["Luna", "Bento"],
        img="Luna and Bento at the small table with the plate of sliced apples, both holding up their clean paws proudly",
        act="Luna and Bento show their clean paws to the camera, then each takes a slice of apple and smiles",
        sfx="happy sparkle chime, cheerful claps, light crunch",
        l1="Lava, lava, lava as mãozinhas,", l2="esfrega, esfrega, bolhinhas!"),
  ]),
 dict(num=5, slug="por-favor-e-obrigado", titulo="Por Favor e Obrigado", tema="Bons modos: por favor, obrigado, com licença e desculpa",
  cast=["Bento", "Pipo", "Nina"],
  setting="a sunny garden picnic with a red-and-white checkered blanket, a wicker basket, a plate of cookies, a jug of orange juice, green grass and a few flowers",
  yt_titulo="✨ Por Favor e Obrigado | Música infantil sobre bons modos #shorts",
  yt_desc="O Bento, o Pipo e a Nina ensinam as palavrinhas mágicas! ✨🐰🐥👧",
  shots=[
   dict(cam="medium shot, eye level, slow push-in", chars=["Bento", "Pipo", "Nina"],
        img="Bento, Pipo and Nina sitting together on the picnic blanket smiling at the camera",
        act="the three friends sway gently on the beat and each lifts one hand in a small happy wave",
        sfx="soft birdsong, sparkle chime on beat 1, light claps",
        l1="Por favor e obrigado,", l2="palavras mágicas, esse é o recado!"),
   dict(cam="medium shot, slow side move", chars=["Pipo", "Bento"],
        img="Pipo looking up at the jug of orange juice on the blanket, Bento next to him ready to pour",
        act="Pipo points to the juice with his wing and opens his beak to ask politely, Bento smiles and lifts the jug",
        sfx="soft juice pour, curious xylophone notes",
        l1="Pipo quer o suco e vai pedir:", l2="Por favor! E todo mundo vai sorrir!"),
   dict(cam="medium shot, steady", chars=["Pipo", "Bento"],
        img="Bento handing a small cup of juice to Pipo, who holds it with both wings",
        act="Pipo receives the cup and gives a little bow of thanks, then gently bumps into Bento and both smile and nod to say sorry",
        sfx="small cup clink, soft bump boing, gentle chime",
        l1="Ganhou o suco? Diz obrigado!", l2="Esbarrou sem querer? Desculpa, amigo!"),
   dict(cam="medium shot, bouncy", chars=["Bento", "Pipo", "Nina"],
        img="the three friends on the blanket holding cookies, smiling at each other",
        act="the three friends bounce gently on the beat and clink their cookies together in a cheerful toast",
        sfx="claps on beats 2 and 4, soft cookie tap, sparkle ting",
        l1="Por favor e obrigado,", l2="palavras mágicas, esse é o recado!"),
   dict(cam="close-up on Nina, then medium, slow", chars=["Nina", "Pipo"],
        img="Nina holding out a cookie to Pipo with a kind smile",
        act="Nina offers a cookie to Pipo, Pipo says thanks with a little bow, both smile warmly",
        sfx="soft sparkle chime, warm glockenspiel note",
        l1="Quem fala assim faz bem ao coração,", l2="todo mundo gosta de gentileza, então!"),
   dict(cam="wide shot of the picnic, gentle push-in", chars=["Bento", "Pipo", "Nina"],
        img="the three friends on the blanket, hugging gently, the picnic set around them",
        act="the three friends hug gently, turn to the camera together and wave",
        sfx="cheerful claps, sparkle chime, soft birdsong",
        l1="Por favor e obrigado,", l2="palavras mágicas, esse é o recado!"),
  ]),
 dict(num=6, slug="esperar-a-vez", titulo="Um, Dois, Três, Espera a Vez", tema="Disciplina e paciência: esperar a vez na fila do parquinho",
  cast=["Bento", "Nina", "Davi"],
  setting="a sunny playground with a small bright red slide and short ladder, a sandbox, green trees, a clear queue line of footprints painted on the ground in front of the ladder",
  yt_titulo="🛝 Um, Dois, Três, Espera a Vez | Música infantil sobre paciência #shorts",
  yt_desc="O Bento, a Nina e o Davi aprendem a esperar a vez no escorregador! 🛝🐰👧👦",
  shots=[
   dict(cam="medium shot, eye level, slow push-in", chars=["Bento", "Nina", "Davi"],
        img="Bento, Nina and Davi standing in a short line in front of the slide ladder, smiling at the camera",
        act="the three stand in line and bounce gently on the beat, Bento turns and smiles to the camera",
        sfx="playground ambience, soft claps, sparkle chime on beat 1",
        l1="Um, dois, três, é a minha vez?", l2="Eu espero, eu espero, chega a vez!"),
   dict(cam="wide shot of the slide, steady", chars=["Nina", "Davi", "Bento"],
        img="Nina at the top of the slide, Davi and Bento waiting in line at the bottom of the ladder",
        act="Nina is about to slide, Davi and Bento wait calmly in line with relaxed hands",
        sfx="soft playground sounds, curious xylophone notes",
        l1="Todo mundo quer escorregar,", l2="mas a fila é pra gente respeitar!"),
   dict(cam="medium shot, slow side move", chars=["Nina", "Davi", "Bento"],
        img="Nina sliding down the slide with a joyful smile, Davi next in line, Bento behind him",
        act="Nina slides down smoothly and lands standing, Davi steps up the ladder, Bento waits patiently with relaxed hands",
        sfx="soft slide whoosh, small happy laugh, claps",
        l1="Primeiro a Nina, depois o Davi,", l2="eu fico quietinho, tô aqui!"),
   dict(cam="medium shot, bouncy", chars=["Bento", "Nina", "Davi"],
        img="the three standing together in line again, smiling",
        act="the three stand in line and sway side to side on the beat",
        sfx="claps on beats 2 and 4, playground ambience",
        l1="Um, dois, três, é a minha vez?", l2="Eu espero, eu espero, chega a vez!"),
   dict(cam="medium shot, gentle push-in", chars=["Bento", "Davi"],
        img="Bento at the bottom of the ladder looking up with excitement, Davi waving from the bottom of the slide",
        act="Bento climbs the short ladder calmly, one step at a time, with a big smile, Davi waves encouragingly",
        sfx="soft ladder steps on the beat, happy sparkle chime",
        l1="Chegou a minha vez, que legal!", l2="Esperar com calma é muito genial!"),
   dict(cam="wide shot of the slide, tracking", chars=["Bento", "Nina", "Davi"],
        img="Bento at the top of the slide with Nina and Davi cheering at the bottom, all smiling",
        act="Bento slides down smoothly with a joyful smile and lands, Nina and Davi cheer, all three then wave at the camera",
        sfx="slide whoosh, cheerful claps, happy sparkle chime",
        l1="Um, dois, três, é a minha vez?", l2="Eu espero, eu espero, chega a vez!"),
  ]),
 dict(num=7, slug="dividir-e-bom", titulo="Metade Pra Mim, Metade Pra Você", tema="Dividir e compartilhar os brinquedos",
  cast=["Pipo", "Luna"],
  setting="a sunny sandbox corner of a playground with soft golden sand, one red bucket, one blue shovel, a few small trees in the background",
  yt_titulo="🪣 Metade Pra Mim, Metade Pra Você | Música infantil sobre dividir #shorts",
  yt_desc="O Pipo e a Luna descobrem como é bom dividir o balde! 🪣🐥🐱",
  shots=[
   dict(cam="medium shot, eye level, slow push-in", chars=["Pipo", "Luna"],
        img="Pipo and Luna sitting in the sand with the red bucket between them, both smiling at the camera",
        act="Pipo and Luna each hold one side of the red bucket and rock it gently on the beat",
        sfx="soft sand sounds, sparkle chime on beat 1, light claps",
        l1="Metade pra mim, metade pra você,", l2="dividir é bom de fazer!"),
   dict(cam="medium shot, slow side move", chars=["Pipo", "Luna"],
        img="Pipo holding the red bucket and Luna holding the blue shovel, both looking at each other thoughtfully",
        act="Pipo and Luna look at the bucket, look at each other, and tilt their heads curiously, thinking",
        sfx="soft thinking xylophone notes, small boing",
        l1="Só tem um balde, dois amigos,", l2="vamos pensar em como brincar juntos!"),
   dict(cam="medium shot, steady", chars=["Pipo", "Luna"],
        img="Luna scooping sand with the blue shovel and pouring it into the bucket held by Pipo",
        act="Luna scoops sand into the bucket, Pipo packs it gently and flips the bucket to make a little sand castle",
        sfx="soft sand pour, gentle pat on the beat, small ting",
        l1="Você enche com areia, eu faço o castelo,", l2="um de cada vez, que lindo, que belo!"),
   dict(cam="medium shot, bouncy", chars=["Pipo", "Luna"],
        img="Pipo and Luna beside a small sand castle, both smiling and holding the bucket together",
        act="Pipo and Luna bounce gently on the beat and pat the small castle together",
        sfx="claps on beats 2 and 4, soft sand pats",
        l1="Metade pra mim, metade pra você,", l2="dividir é bom de fazer!"),
   dict(cam="close-up, then medium, slow", chars=["Pipo", "Luna"],
        img="Pipo placing a tiny flag on top of the sand castle while Luna holds the shovel and smiles",
        act="Pipo places a tiny leaf flag on the castle, Luna taps the castle gently with the shovel, both smile warmly",
        sfx="soft sparkle chime, warm glockenspiel note",
        l1="Dividiu o balde, ganhou um amigo,", l2="brincar junto é bem mais divertido!"),
   dict(cam="wide shot of the sandbox, gentle push-in", chars=["Pipo", "Luna"],
        img="the finished sand castle in the middle, Pipo and Luna sitting on each side, hugging gently",
        act="Pipo and Luna hug gently next to the castle and turn to the camera and wave",
        sfx="cheerful claps, happy sparkle chime, soft birdsong",
        l1="Metade pra mim, metade pra você,", l2="dividir é bom de fazer!"),
  ]),
 dict(num=8, slug="hora-de-dormir", titulo="Lá, Lá, Lá, Hora de Dormir", tema="Rotina de dormir: banho, pijama, dentes, boa-noite",
  cast=["Bento", "Luna"],
  setting="a cozy warm bedroom at night with a soft glowing moon visible through the window, a small bed with a yellow blanket, a gentle round night light, a teddy bear, soft warm golden lamp light, never dark",
  yt_titulo="🌙 Lá, Lá, Lá, Hora de Dormir | Música de ninar infantil #shorts",
  yt_desc="O Bento e a Luna mostram a rotina para dormir bem! 🌙🐰🐱",
  shots=[
   dict(cam="medium shot, eye level, slow push-in", chars=["Bento"],
        img="Bento in blue pajamas standing next to his bed, smiling softly at the camera, the moon glowing in the window",
        act="Bento sways gently on the beat with a soft smile and a small sleepy yawn",
        sfx="soft night crickets, gentle sparkle chime on beat 1",
        l1="Lá, lá, lá, é hora de dormir,", l2="a lua vem me ninar e sorrir!"),
   dict(cam="medium shot, slow side move", chars=["Bento", "Luna"],
        img="Bento and Luna in pajamas next to the bed, Luna holding a small towel, Bento holding a toothbrush",
        act="Bento and Luna show their toothbrush and towel, then put on their pajama caps and smile",
        sfx="soft towel rustle, gentle xylophone notes",
        l1="Tomei banho, vesti pijama,", l2="escovei os dentes, vou pra cama!"),
   dict(cam="medium shot, steady", chars=["Bento", "Luna"],
        img="Bento placing a small book on the shelf, Luna holding the teddy bear",
        act="Bento closes a small book and puts it on the shelf, Luna sets the teddy bear on the pillow and pats it",
        sfx="soft book close, gentle pillow pat",
        l1="Guardei os brinquedos, fechei o livrinho,", l2="dei boa-noite ao meu ursinho!"),
   dict(cam="medium shot, gentle sway", chars=["Bento", "Luna"],
        img="Bento and Luna sitting on the edge of the bed, smiling softly at the camera",
        act="Bento and Luna sway gently side by side on the beat, with sleepy smiles",
        sfx="soft claps on beats 2 and 4, night crickets",
        l1="Lá, lá, lá, é hora de dormir,", l2="a lua vem me ninar e sorrir!"),
   dict(cam="close-up on the faces, slow push-in", chars=["Bento", "Luna"],
        img="Bento and Luna lying in the bed under the yellow blanket, eyes slowly closing, the teddy bear between them",
        act="Bento and Luna pull the blanket up, close their eyes slowly and take a deep calm breath",
        sfx="soft breath, gentle chimes, quiet night crickets",
        l1="Fecha o olhinho, respira devagar,", l2="sonhos bonitos vão chegar!"),
   dict(cam="wide shot of the bedroom, slow pull-back", chars=["Bento", "Luna"],
        img="Bento and Luna asleep in the bed under the blanket, the moon glowing warmly in the window",
        act="the moonlight twinkles softly in the window, Bento and Luna sleep peacefully with tiny smiles, the camera slowly pulls back",
        sfx="soft twinkling stars, gentle chime, quiet night crickets",
        l1="Lá, lá, lá, é hora de dormir,", l2="a lua vem me ninar e sorrir!"),
  ]),
 dict(num=9, slug="fruta-e-show", titulo="Fruta, Fruta, Quero Mais", tema="Comer frutas e uma alimentação saudável",
  cast=["Tico", "Davi", "Bento"],
  setting="a sunny kitchen garden corner with a small wooden table, a bowl with banana, red apple, strawberries and orange slices, a few leafy plants, soft warm morning light",
  yt_titulo="🍎 Fruta, Fruta, Quero Mais | Música infantil sobre frutas #shorts",
  yt_desc="O Tico, o Davi e o Bento descobrem como as frutas são gostosas! 🍎🍌🐵",
  shots=[
   dict(cam="medium shot, eye level, slow push-in", chars=["Tico", "Davi", "Bento"],
        img="Tico, Davi and Bento around the wooden table with the colorful fruit bowl, smiling at the camera",
        act="the three bounce gently on the beat and each lifts one piece of fruit toward the camera",
        sfx="soft fruit bounces, sparkle chime on beat 1, light claps",
        l1="Fruta, fruta, quero mais!", l2="Colorida e gostosa, eu cresço demais!"),
   dict(cam="close-up on the fruit bowl, slow side move", chars=["Tico", "Bento"],
        img="Tico holding a banana and Bento holding a red apple next to the fruit bowl, smiling",
        act="Tico lifts the banana and Bento lifts the apple and they show them to the camera, then point at the oranges and strawberries",
        sfx="soft fruit taps on the beat, curious xylophone notes",
        l1="A banana é amarela, a maçã vermelhinha,", l2="a laranja é redondinha, todas na cestinha!"),
   dict(cam="medium shot, steady", chars=["Davi", "Tico"],
        img="Davi rinsing a strawberry under a small tap while Tico watches with a thumbs-up",
        act="Davi rinses a strawberry and Tico points to a grown-up's hand off to the side holding a knife handle only? no knife; Davi shows an empty open hand asking a grown-up for help",
        sfx="soft water rinse, gentle pop",
        l1="Lava a fruta, descasca com cuidado,", l2="com ajuda de um adulto, tá combinado!"),
   dict(cam="medium shot, bouncy", chars=["Tico", "Davi", "Bento"],
        img="the three standing at the table each holding a slice of fruit, smiling",
        act="the three bounce gently on the beat holding their slices of fruit and clink them together in a cheerful toast",
        sfx="claps on beats 2 and 4, soft fruit taps",
        l1="Fruta, fruta, quero mais!", l2="Colorida e gostosa, eu cresço demais!"),
   dict(cam="close-up, slow push-in", chars=["Davi"],
        img="Davi taking a small bite of an apple slice with a happy chewing smile",
        act="Davi chews slowly with a happy smile, swallows, then flexes his small arm proudly",
        sfx="soft crunch, gentle chewing, sparkle ting",
        l1="Mastiga devagar, bem gostosinho,", l2="fruta dá força pro meu corpinho!"),
   dict(cam="wide shot of the table, gentle push-in", chars=["Tico", "Davi", "Bento"],
        img="the three at the table with empty plates and happy full faces, the fruit bowl nearly empty",
        act="the three rub their bellies happily, then turn to the camera together and wave",
        sfx="cheerful claps, happy sparkle chime",
        l1="Fruta, fruta, quero mais!", l2="Colorida e gostosa, eu cresço demais!"),
  ]),
 dict(num=10, slug="foco-um-de-cada-vez", titulo="Foco, Foco, Um de Cada Vez", tema="Foco e organização: arrumar a mochila com calma",
  cast=["Olívia", "Nina", "Bento"],
  setting="a bright cozy classroom corner with a small wooden desk, a cup of colorful pencils, a notebook, a round schoolbag, a big sunny window and a soft rug",
  yt_titulo="🎒 Foco, Foco, Um de Cada Vez | Música infantil sobre organização #shorts",
  yt_desc="A professora Olívia ensina a Nina e o Bento a arrumar a mochila com foco! 🎒🦉",
  shots=[
   dict(cam="medium shot, eye level, slow push-in", chars=["Olívia", "Nina", "Bento"],
        img="Olívia standing between Nina and Bento at the desk, all three smiling at the camera, the schoolbag open on the desk",
        act="the three sway gently on the beat and Olívia lifts one wing in a calm encouraging gesture",
        sfx="soft school bell ting, sparkle chime on beat 1, light claps",
        l1="Foco, foco, um de cada vez,", l2="eu consigo, eu consigo, eu sei fazer!"),
   dict(cam="medium shot, slow side move", chars=["Nina", "Bento"],
        img="Nina and Bento looking at the desk covered with a notebook, a cup of pencils and a lunchbox",
        act="Nina looks at the items and takes a slow deep breath, Bento does the same, then both smile calmly",
        sfx="soft breath, gentle xylophone notes",
        l1="Tem lápis, tem caderno, tem tanta coisa,", l2="respira fundo, uma por uma, com calma!"),
   dict(cam="medium shot, steady", chars=["Nina", "Bento"],
        img="Nina holding the notebook over the open schoolbag, Bento holding a pencil case",
        act="Nina puts the notebook in the schoolbag, Bento puts the pencil case in, then Nina puts in the lunchbox and zips the bag",
        sfx="soft paper rustle, gentle zip, taps on the beat",
        l1="Caderno primeiro, depois o estojo,", l2="lanche por cima, e fecha o zíper, que orgulho!"),
   dict(cam="medium shot, bouncy", chars=["Olívia", "Nina", "Bento"],
        img="Olívia, Nina and Bento around the desk with the closed schoolbag, smiling",
        act="the three sway gently on the beat and Nina and Bento lift their arms in a small cheer",
        sfx="claps on beats 2 and 4, soft school bell ting",
        l1="Foco, foco, um de cada vez,", l2="eu consigo, eu consigo, eu sei fazer!"),
   dict(cam="close-up on Olívia, slow push-in", chars=["Olívia", "Bento"],
        img="Olívia leaning down with a kind smile toward Bento, who is looking up proudly",
        act="Olívia nods proudly and gently pats Bento's head with her wing, Bento smiles and stands tall",
        sfx="warm glockenspiel note, soft sparkle chime",
        l1="Quem tem foco faz com carinho,", l2="um passo de cada vez, devagarinho!"),
   dict(cam="wide shot of the classroom corner, gentle push-in", chars=["Olívia", "Nina", "Bento"],
        img="the three standing together next to the neat desk with the closed schoolbag, smiling",
        act="Nina puts the schoolbag on her back, all three turn to the camera and wave",
        sfx="cheerful claps, happy sparkle chime, soft school bell ting",
        l1="Foco, foco, um de cada vez,", l2="eu consigo, eu consigo, eu sei fazer!"),
  ]),
]

# Correção de um trecho do ep. 9 (clipe 3): ação segura, sem faca
for ep in EPISODES:
    if ep["num"] == 9:
        ep["shots"][2]["act"] = ("Davi rinses a strawberry under the small tap, then shows both hands open to the camera as if "
                                 "asking for a grown-up's help, Tico gives a thumbs-up")


def lock_for(chars):
    d = "; ".join(SHORT[c] for c in chars)
    l = "; ".join(CAST[c][1] for c in chars)
    return d, l


def image_prompt(ep, sh):
    d, l = lock_for(sh["chars"])
    return (f"Using the attached reference sheets (keep every character exactly identical to its sheet): {d}.\n"
            f"Setting: {ep['setting']}.\n"
            f"Shot: {sh['cam']}. {sh['img']}.\n"
            f"Anatomy lock: {l}. All other body parts stay normal and attached.\n"
            f"{STYLE} Keep the lower-left corner simple and uncluttered.\n{NEG_IMG}")


def video_prompt(ep, sh):
    d, l = lock_for(sh["chars"])
    return (f"{STYLE}\n"
            f"Characters (identical to the attached reference sheets): {d}.\n"
            f"Setting: {ep['setting']}.\n"
            f"Shot: {sh['cam']}. Action: {sh['act']}.\n"
            f"Anatomy lock: {l}. Counts never change.\n"
            f"{RULE_VIDEO}\n"
            f"{MUSIC} Sound effects: {sh['sfx']}.\n"
            f"Sung lyrics, exactly these two lines and nothing else: \"{sh['l1']}\" / \"{sh['l2']}\"\n"
            f"{NEG_VIDEO}")


def fence(s):
    return "```\n" + s + "\n```\n"


def write_episode(ep):
    n = ep["num"]
    L = []
    L.append(f"# Ep. {n:02d}: {ep['titulo']}\n")
    L.append(f"**Tema:** {ep['tema']}  \n**Duração:** 6 clipes de 10 s = 60 s  \n**Personagens:** {', '.join(ep['cast'])}\n")
    L.append("## Letra completa (cada clipe = 2 versos)\n")
    for i, sh in enumerate(ep["shots"], 1):
        tag = {1: " (gancho + refrão)", 4: " (refrão)", 6: " (refrão final)"}.get(i, "")
        L.append(f"- **Clipe {i}{tag}:** {sh['l1']} / {sh['l2']}")
    L.append("")
    L.append("## Antes de começar\n")
    L.append("Tenha prontas as **fichas de personagem** (veja a BIBLIA-DO-CANAL.md): " +
             ", ".join(ep["cast"]) + ".\n")
    L.append("## Passo 1: gerar as 6 imagens iniciais (9:16)\n")
    L.append("Em cada imagem, anexe a ficha de quem aparece nela. Se uma imagem sair com orelha, braço ou olho a mais, **gere de novo**. Não siga adiante com imagem errada.\n")
    for i, sh in enumerate(ep["shots"], 1):
        L.append(f"### Imagem E{n:02d}-{i}  (anexar: {', '.join(sh['chars'])})\n")
        L.append(fence(image_prompt(ep, sh)))
    L.append("## Passo 2: gerar os 6 vídeos (10 s, 720p, 9:16)\n")
    L.append("Em cada vídeo, **comece pela imagem de mesmo número** e anexe as fichas de quem aparece. Gere um clipe de cada vez e confira antes do próximo.\n")
    for i, sh in enumerate(ep["shots"], 1):
        L.append(f"### Vídeo E{n:02d}-{i}  (começa da imagem E{n:02d}-{i}; anexar: {', '.join(sh['chars'])})\n")
        L.append(fence(video_prompt(ep, sh)))
    L.append("## Checklist de cada clipe\n")
    L.append("- [ ] Cada personagem tem a contagem certa de orelhas, olhos, braços, pernas e cauda, **do primeiro ao último quadro**?")
    L.append("- [ ] O personagem está igual à ficha (cor, lenço, tamanho)?")
    L.append("- [ ] A voz canta os 2 versos certos, em português, começando já no primeiro segundo?")
    L.append("- [ ] A música é a mesma dos outros clipes (ukulele, palminhas, mesma voz)?")
    L.append("- [ ] Nenhum texto escrito na tela e nada assustador?")
    L.append("- [ ] Se falhou em algo: gere de novo só aquele clipe. Não tente consertar com prompt maior.\n")
    L.append("## Quando terminar\n")
    L.append(f"Me mande os 6 clipes, **um por mensagem, na ordem 1 a 6**. Eu monto o vídeo de 60 s, igualo o volume e entrego pronto para você só colocar o Libras e publicar.\n")
    L.append("## Publicação\n")
    L.append(f"- **Título:** {ep['yt_titulo']}")
    L.append(f"- **Descrição:** {ep['yt_desc']}")
    L.append("- **Hashtags:** #shorts #infantil #musicainfantil #desenhoinfantil #educativo")
    L.append("- **Público:** marcar como \"feito para crianças\"")
    L.append("- **Conteúdo sintético:** declarar uso de IA se o YouTube Studio pedir\n")
    path = os.path.join(EPS_DIR, f"EP{n:02d}-{ep['slug']}.md")
    open(path, "w").write("\n".join(L))
    return path


def write_bible():
    L = []
    L.append("# Bíblia do canal: Bento e Amigos (Shorts infantis didáticos em 3D)\n")
    L.append("Este arquivo é o que **não muda** de episódio para episódio. Os episódios estão na pasta `episodios/`.\n")
    L.append("## 1. Como o trabalho funciona (resumo)\n")
    L.append("1. **Uma vez só:** gerar as fichas dos personagens (seção 3).")
    L.append("2. **Por episódio:** gerar 6 imagens iniciais → gerar 6 vídeos de 10 s, cada um começando da imagem de mesmo número → me mandar os 6 clipes → eu monto os 60 s.")
    L.append("3. **Depois:** Libras no canto, legenda e publicação.\n")
    L.append("## 2. Estilo fixo\n")
    L.append("Estilo de filme de animação 3D, formas arredondadas e fofas. Este bloco entra em TODO prompt (já está colado dentro de cada prompt dos episódios):\n")
    L.append(fence(STYLE))
    L.append("## 3. Fichas dos personagens (gerar uma vez, guardar)\n")
    L.append("Gere cada ficha em horizontal (16:9), com fundo branco. Guarde as imagens: elas serão anexadas como referência em todo clipe. **O Bento já existe**: pode usar a ficha que você gerou no teste, ou gerar de novo com o prompt abaixo para ficar igual aos outros.\n")
    for name in CAST:
        L.append(f"### Ficha: {name}\n")
        L.append(fence(sheet_prompt(name)))
    L.append("### Ficha extra (opcional): grupo com todos juntos\n")
    L.append("Gere **depois** das fichas individuais, anexando todas. Serve para manter os tamanhos relativos.\n")
    L.append(fence("A lineup of all the characters standing side by side on a plain white background, using the attached reference sheets, "
                   "keeping each one identical to its sheet and in realistic relative sizes: Bento the bunny, Luna the kitten, Tico the monkey, "
                   "Pipo the duckling (smallest), Olívia the owl, Nina the girl and Davi the boy (tallest). Everyone smiling at the camera. "
                   + STYLE.replace("vertical 9:16, ", "") + " Wide horizontal image. " + NEG_IMG))
    L.append("## 4. Anti-alucinação: o que muda nos prompts a partir de agora\n")
    L.append("Você teve orelha duplicada. Isso acontece quando o modelo precisa inventar o que está \"fora de quadro\" e quando o personagem se mexe muito. Cada prompt agora tem 4 proteções:\n")
    L.append("1. **Trava de anatomia por personagem**, com contagem exata (por exemplo: \"exactly 2 eyes, 2 long floppy ears, 2 arms, 2 legs and 1 tail\"). Fica dentro de todo prompt de imagem e de vídeo.")
    L.append("2. **Regras de movimento:** ação simples e lenta, orelhas se movem só de leve e de uma peça só, nada de giro rápido.")
    L.append("3. **Bloco NEGATIVE** no fim de todo prompt, listando o que nunca pode aparecer (orelhas, braços, pernas, olhos, caudas ou cabeças a mais, personagem se dividindo, mudando de cor, texto na tela, susto).")
    L.append("4. **Poucos personagens por cena:** no máximo 3, e a maioria dos clipes tem 1 ou 2. Quanto menos personagem, menos erro.\n")
    L.append("Bloco NEGATIVE usado nos vídeos:\n")
    L.append(fence(NEG_VIDEO))
    L.append("**Se o Flow tiver um campo próprio de \"prompt negativo\"**, cole ali só o texto depois de \"NEGATIVE:\". Se não tiver, deixe do jeito que está, no fim do prompt.\n")
    L.append("**Se mesmo assim sair com defeito:** gere de novo só aquele clipe (às vezes 2 ou 3 vezes). Não adianta reescrever o prompt para um clipe que falhou uma vez. Se um mesmo clipe falhar 3 vezes, me conte o que aconteceu e eu simplifico a ação dele.\n")
    L.append("## 5. Música: a receita do refrão grudento\n")
    L.append("**Atenção:** a pesquisa ao vivo de músicas virais não funcionou nesta sessão (as ferramentas de busca estavam sem créditos). Isto aqui vem do que eu conheço de músicas infantis de sucesso, como *Baby Shark*, *Galinha Pintadinha*, *Mundo Bita* e *Cocomelon*. É uma base criativa. **As letras e as melodias dos 10 episódios são originais.**\n")
    L.append("O que essas músicas têm em comum e o que eu usei:\n")
    L.append("| Característica | Como está nos 10 episódios |")
    L.append("|---|---|")
    L.append("| Andamento de 90 a 110 BPM, tom maior | 96 BPM, dó maior, sempre |")
    L.append("| Melodia curta, poucas notas, passos pequenos (escala pentatônica) | Refrão de 2 versos, sem saltos grandes |")
    L.append("| **Refrão que se repete muito** | O refrão toca 3 vezes por episódio (clipes 1, 4 e 6) |")
    L.append("| Palavras que imitam som e gesto (nhac, ai ai ai, bolhinhas) | Em todos os refrões |")
    L.append("| Perguntas e respostas, \"chamada e resposta\" | Verso 1 chama, verso 2 responde |")
    L.append("| Rimas simples | Quase todos os versos rimam |")
    L.append("| Coro de crianças no refrão | Pedido em todo prompt |")
    L.append("| Ação que a criança imita (esfregar, bater palma, pular) | Cada verso tem um gesto na tela |")
    L.append("| Poucos instrumentos, brilhantes | Ukulele, shaker, palmas, glockenspiel e baixo |\n")
    L.append("### O truque da sincronia entre clipes\n")
    L.append("Cada clipe tem 10 s. A 96 BPM, 10 s são **exatamente 16 tempos = 4 compassos**. Por isso:\n")
    L.append("- Cada clipe é uma \"fatia\" de 4 compassos da música: o canto começa no tempo 1 e termina no fim do compasso 4.")
    L.append("- Cada clipe canta **2 versos**: um nos compassos 1 e 2, outro nos compassos 3 e 4.")
    L.append("- Cada clipe pede que a música **não termine**: sem acorde final, sem fade, sem aplauso. Assim o corte cai no tempo 1 do clipe seguinte, no mesmo ritmo.")
    L.append("- A **mesma descrição de arranjo e de voz** está copiada em todos os clipes.")
    L.append("- O **refrão repetido** funciona como cola: mesmo que a melodia mude um pouco de um clipe para outro, a criança reconhece as mesmas palavras.\n")
    L.append("**Limite honesto:** o Flow gera cada clipe separado e pode variar a melodia ou o timbre da voz. Eu não consigo garantir que seja idêntico. Quando você me mandar os clipes, eu confiro as durações e o volume e corto exatamente no compasso. Se a voz ou o estilo mudarem demais em algum clipe, gere esse clipe de novo.\n")
    L.append("Bloco de áudio usado em todos os clipes:\n")
    L.append(fence(MUSIC))
    L.append("## 6. Regras do YouTube e cuidado com conteúdo infantil\n")
    L.append("**Atenção:** também não consegui consultar as regras atuais por busca (sem créditos). O que escrevo abaixo é do que eu sei. **Confirme no YouTube Studio e na Central de Ajuda do YouTube** antes de publicar, porque as regras mudam. Procure por: \"conteúdo feito para crianças\", \"política de segurança infantil\" e \"conteúdo inautêntico\" no Programa de Parcerias.\n")
    L.append("- **Marcar todos os vídeos como \"feito para crianças\".** Isso é obrigatório para esse público.")
    L.append("- **Nada assustador:** sem sustos, sombras, monstros de verdade, violência, perigo imitável. Os \"Docinhos\" do Ep. 1 são bolinhas de geleia engraçadas, não monstros.")
    L.append("- **Segurança:** o Ep. 3 (rua) mostra os carros parados longe, nunca em movimento perto das crianças. O Ep. 9 (frutas) não mostra faca: a criança pede ajuda a um adulto. Em tudo que ensina hábito de saúde, peça para um profissional revisar quando possível.")
    L.append("- **Tudo original:** músicas, letras, personagens e roteiros são nossos. Não use música, personagem, marca ou voz de ninguém. Nos prompts eu não cito nenhuma marca.")
    L.append("- **Conteúdo repetitivo ou feito em massa:** o YouTube pode limitar a monetização de canais que postam vídeos praticamente iguais. Para se proteger: cada episódio tem **história, letra, cenário e lição próprios**, e você adiciona sua curadoria (roteiro, montagem, Libras). Evite postar muitos vídeos por dia no começo.")
    L.append("- **IA:** declare quando o YouTube Studio pedir a opção de conteúdo sintético ou alterado.")
    L.append("- **Títulos e descrições honestos:** sem clickbait, sem prometer o que o vídeo não tem.")
    L.append("- **Comentários e anúncios:** em vídeo \"feito para crianças\", comentários e anúncios personalizados ficam desligados. Isso é normal.\n")
    L.append("## 7. Montagem e transições (o que eu faço)\n")
    L.append("- Corto cada clipe **exatamente no compasso** (10,000 s), sem sobra.")
    L.append("- Transição de apenas 2 a 4 quadros e um *crossfade* de áudio bem curto, só para suavizar. Como o canto começa no tempo 1 e o ritmo não para, o corte tende a ficar no tempo.")
    L.append("- Igualo o volume entre os clipes e ajusto para o padrão do YouTube (-14 LUFS).")
    L.append("- Para o visual ligar melhor entre dois clipes, os clipes **terminam e começam em poses parecidas**: o personagem fica no mesmo lado da tela e com a mesma escala. É por isso que cada imagem inicial é planejada.")
    L.append("- Se você quiser ainda mais continuidade, no Flow dá para usar o **último quadro de um clipe como início do próximo** (se o recurso existir na sua versão). Me diga se existir que eu adapto os prompts.\n")
    L.append("## 8. Calendário sugerido\n")
    L.append("| Ordem | Episódio | Lição |")
    L.append("|---|---|---|")
    for ep in EPISODES:
        L.append(f"| {ep['num']} | {ep['titulo']} | {ep['tema']} |")
    L.append("\nPublique 1 por dia ou a cada 2 dias no começo. Veja no YouTube Studio quais têm mais \"assistiu até o fim\" e repita o tema parecido.\n")
    L.append("## 9. Depois dos 10\n")
    L.append("Junte 3 ou 4 Shorts do mesmo tema num vídeo longo de 3 a 5 minutos, com o Short servindo de trailer. O Libras entra tanto nos Shorts quanto nos longos (decidimos depois como).\n")
    path = os.path.join(BASE, "BIBLIA-DO-CANAL.md")
    open(path, "w").write("\n".join(L))
    return path


def write_index():
    L = ["# Pacote: 10 Shorts didáticos de 60 s (Bento e Amigos)\n",
         "Comece por **BIBLIA-DO-CANAL.md** (fichas dos personagens, regras anti-erro, música, regras do YouTube).",
         "Depois siga os episódios na ordem.\n",
         "| # | Arquivo | Título | Lição | Personagens |", "|---|---|---|---|---|"]
    for ep in EPISODES:
        L.append(f"| {ep['num']} | episodios/EP{ep['num']:02d}-{ep['slug']}.md | {ep['titulo']} | {ep['tema']} | {', '.join(ep['cast'])} |")
    L.append("")
    L.append("O vídeo de teste (40 s, sem a bíblia) está em `EP01-escovar-dentes.md` e em `out/`. Ele **não** faz parte do pacote novo.")
    open(os.path.join(BASE, "INDICE.md"), "w").write("\n".join(L))


if __name__ == "__main__":
    for ep in EPISODES:
        assert len(ep["shots"]) == 6, ep["num"]
        for sh in ep["shots"]:
            for c in sh["chars"]:
                assert c in CAST, (ep["num"], c)
    print(write_bible())
    write_index()
    for ep in EPISODES:
        print(write_episode(ep))
