#!/usr/bin/env python3
"""Gera, para os episódios 11 a 30, os arquivos PRONTOS PARA COLAR no Google Flow:
  episodios/EPNN-PRONTO.md  (roteiro, letra, legendas EN, mensagem das imagens, mensagem dos vídeos detalhada)
  FICHAS.md                 (prompts das fichas de todos os personagens)
  INDICE-30.md              (visão geral dos 30 episódios)
Uso: python3 gerar_pronto.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerar_pacote as g

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
EPS = os.path.join(BASE, "episodios")

NEG = ("extra ears, third ear, fourth ear, second pair of ears, duplicated ears, upright ears on Bento, ears standing up, ears pointing up, "
       "ears spread out like wings, extra arms, extra legs, extra paws, extra wings, extra fingers, extra toes, extra tails, two tails, extra eyes, "
       "extra beaks, extra heads, duplicated body, cloned character, merged bodies, melting, morphing, stretching limbs, twisted limbs, missing limbs, "
       "character splitting in two, face changing, color change, size change, outfit change, scarf changing, objects appearing, objects disappearing, "
       "duplicated objects, scene cut, fade, camera shake, fast motion, spinning, jumping, hopping, shrugging, text, subtitles, letters, watermark, logo, "
       "blurred bars, letterbox, black bars, borders, scary, creepy, dark, sudden movement, loud sound, music, singing, speech")

LOCK = {
    "Bento": "BENTO: a chubby lop-eared bunny, cream-white with beige patches, big dark eyes, rosy cheeks, a small blue knitted scarf, a short round tail. He has EXACTLY 2 ears, one on each side of his head, both soft and floppy and ALWAYS HANGING DOWN along the sides of his head from the first frame to the last; they NEVER stand up and NEVER spread like wings, and only sway gently. EXACTLY 2 eyes, 2 arms, 2 legs and 1 tail.",
    "Luna": "LUNA: a fluffy blue-gray kitten with a white chest and muzzle, big green eyes, a small pink bow at her neck. EXACTLY 2 small pointed ears standing on top of her head, 2 eyes, 2 arms, 2 legs and ONE single long fluffy tail.",
    "Tico": "TICO: a small round caramel-brown monkey with a cream face and belly, big dark eyes, a small green backpack. EXACTLY 2 round ears (one on each side), 2 eyes, 2 arms, 2 legs and ONE long curly tail.",
    "Pipo": "PIPO: a tiny round fluffy yellow duckling with big black eyes, a small orange beak, a tiny red bow tie. EXACTLY 2 eyes, 1 beak, 2 small wings and 2 orange feet.",
    "Olívia": "OLÍVIA: a gentle round brown owl with big golden eyes, a cream heart-shaped face, two small ear tufts, soft wings, an orange bow tie. EXACTLY 2 eyes, 2 ear tufts, 2 wings and 2 feet.",
    "Nina": "NINA: a cheerful 5-year-old girl with light-brown skin, big dark eyes, two curly puffs of dark hair tied with yellow ribbons, rosy cheeks, a green dress and white shoes, always fully dressed. EXACTLY 2 eyes, 2 hair puffs, 2 arms with simple rounded mitten-like hands, 2 legs.",
    "Davi": "DAVI: a cheerful 5-year-old boy with light-tan skin, big brown eyes, short wavy dark hair, rosy cheeks, an orange t-shirt, blue shorts and white sneakers, always fully dressed. EXACTLY 2 eyes, 2 arms with simple rounded mitten-like hands, 2 legs.",
}
STYLE = ("high-quality stylized 3D animated feature-film look, soft rounded shapes, big expressive eyes, fluffy fur, warm cinematic lighting, "
         "shallow depth of field, rich gentle colors, no text, no letters, no logos, nothing scary. Keep the lower-left corner of the frame simple and uncluttered.")


def nm(c): return "SHEET-" + c.upper().replace("Í", "I")


def locks(chars):
    return "\n".join(LOCK[c] for c in chars)


def img_message(ep):
    n = ep["num"]
    refs = " and ".join(nm(c) for c in ep["cast"])
    L = [f"Using the attached reference sheets {refs}, generate 6 separate images named E{n:02d}-1 to E{n:02d}-6. Generate them one at a time, in order. Every character must be exactly identical to its reference sheet.\n",
         "ASPECT RATIO (very important): every image must be VERTICAL portrait 9:16 (1080x1920), like a phone screen, filling the WHOLE frame. Do NOT make landscape 16:9 images. Do NOT add blurred bars, letterboxing or borders.\n",
         f"SETTING for all 6: {ep['setting']}.\n", f"STYLE for all 6: {STYLE}\n",
         "CHARACTERS:\n" + locks(ep["cast"]) + "\n",
         "Hands, paws and wings are simple, soft, rounded shapes. Never show extra fingers, toes, ears, tails or limbs.\n",
         f"NEGATIVE for all 6: {NEG}\n"]
    for i, s in enumerate(ep["shots"], 1):
        L.append(f"E{n:02d}-{i} (use {' and '.join(nm(c) for c in s['chars'])}): {s['cam']}. {s['img']}.\n")
    L.append("After each image, check it: count the ears, eyes, arms, legs, wings and tails of every character; check the image is truly vertical and has no blurred band. "
             "If anything is wrong, regenerate that image (up to 2 times) before moving on. When all 6 are done, show them together in order.")
    return "\n".join(L)


def vid_message(ep):
    n = ep["num"]
    refs = " and ".join(nm(c) for c in ep["cast"])
    L = [f"CONTEXT: I am making a 60-second vertical kids' short as 6 video clips of 10 seconds each. Generate the 6 videos ONE AT A TIME, in numbered order. Video V{n:02d}-k must use the attached image E{n:02d}-k as its FIRST FRAME. Use the attached reference sheets {refs} for the characters. Each video is exactly 10.0 seconds, VERTICAL portrait 9:16 (no landscape, no blurred bars, no letterbox), 720p, 24 fps, ONE continuous shot with NO cuts, NO scene changes, NO fades.\n",
         "CONTINUITY: reproduce the first-frame image exactly (same place, same objects, same lighting, same framing, same poses). Everything not mentioned in the timeline stays completely still. The characters look identical to their sheets in every single frame.\n",
         f"SETTING: {ep['setting']}.\n", "CHARACTERS:\n" + locks(ep["cast"]) + "\n",
         f"STYLE: {STYLE}\n",
         "MOTION: slow and gentle. One main action at a time, exactly as written. Small gestures only. No jumping, no hopping, no running, no spinning, no shrugging, no fast head turns, no fast waving. If an action would be hard to do without breaking anatomy, do a simpler version instead. Characters keep the same size and distance from the camera and never leave the frame. Objects keep their shape, color and number; nothing appears, disappears or duplicates.\n",
         "SOUND: only soft sound effects matched to the action. No music, no singing, no speech, no loud or sudden sounds.\n",
         "SELF-CHECK before delivering each video: count the ears, eyes, arms, legs, wings and tails of every character at 0 s, 2.5 s, 5 s, 7.5 s and 10 s"
         + (". Bento must show exactly 2 HANGING ears at every moment" if "Bento" in ep["cast"] else "")
         + ". If any count is wrong, regenerate before showing me.\n",
         f"NEGATIVE: {NEG}\n"]
    for i, s in enumerate(ep["shots"], 1):
        a1, a2, a3 = s["a"]
        names = " and ".join(nm(c) for c in s["chars"])
        L.append(f"VIDEO V{n:02d}-{i} (first frame = attached image E{n:02d}-{i}; use {names})\n"
                 f"FIRST FRAME, exactly: {s['img']}. Setting as described above.\n"
                 f"TIMELINE:\n0.0-3.0 s: {a1}.\n3.0-7.0 s: {a2}.\n7.0-10.0 s: {a3}.\n"
                 f"MUST NOT HAPPEN: no extra or duplicated body parts, no second tail, no extra ears; nobody jumps or leaves their place; objects never multiply; the framing never changes.\n"
                 f"CAMERA: {s['cam']}, 5% at most.\n"
                 f"LAST FRAME: the end pose of the timeline, characters calm and smiling.\n"
                 f"SOUND: {s['sfx']}.\n")
    L.append("After each video, check it frame by frame as in the SELF-CHECK. When all 6 are done, show them in order.")
    return "\n".join(L)


def write_ep(ep):
    n = ep["num"]
    M = [f"# Ep. {n:02d}: {ep['titulo']}\n",
         f"**Lição:** {ep['tema']}  \n**Personagens:** {', '.join(ep['cast'])}  \n**Duração:** 6 clipes de 10 s = 60 s  \n"
         f"**Fichas necessárias:** {', '.join(nm(c) for c in ep['cast'])} (prompts em `FICHAS.md`; Bento, Luna, Tico, etc. já gerados não precisam repetir)\n",
         "## Roteiro e letra (cena a cena)\n", "| Clipe | O que acontece | Letra (cantada) | Legenda (EN) |", "|---|---|---|---|"]
    for i, s in enumerate(ep["shots"], 1):
        what = "; ".join(s["a"])
        M.append(f"| {i} | {what} | {s['l1']} / {s['l2']} | {s['e1']} / {s['e2']} |")
    M += ["", "## Como usar (ordem)\n",
          "1. Se faltar a ficha de algum personagem, gere pela `FICHAS.md` (sem anexo).",
          "2. Cole a **Mensagem 1** (imagens) com as fichas anexadas. Confira cada imagem: vertical em tela cheia, sem faixa borrada, contagem de orelhas/olhos/patas.",
          "3. Me mande as imagens (todas, mesmo as repetidas). Eu escolho as 6 melhores e renomeio de 1 a 6. Se você já tem 6 boas, siga.",
          "4. Cole a **Mensagem 2** (vídeos) com as fichas e as 6 imagens aprovadas anexadas. Gere o clipe 4 primeiro como teste, se quiser economizar crédito.",
          "5. Me mande os 6 vídeos, um por mensagem. Eu gero a música (ACE-Step), escolho a melhor versão, monto a edição cinema e entrego com legenda em inglês.\n",
          "## Mensagem 1: as 6 imagens\n", "```\n" + img_message(ep) + "\n```\n",
          "## Mensagem 2: os 6 vídeos\n", "```\n" + vid_message(ep) + "\n```\n",
          "## Música e legendas (eu faço)\n",
          f"- Gerar música: `tools/gerar_musica.sh {n} 23 41`; escolher: `tools/escolher_musica.py {n} ...`; legendas: `tools/legendas_auto.py {n} musica.mp3 config.json`.",
          "- Montagem: `tools/montar_cine.py` (cortes no ritmo, cor de filme, transições, legendas com pop).\n",
          "## Publicação\n", f"- **Título:** {ep['yt_titulo']}", f"- **Descrição:** {ep['yt_desc']}",
          "- **Hashtags:** #shorts #infantil #musicainfantil #desenhoinfantil #educativo", "- **Público:** marcar \"feito para crianças\"",
          "- **Conteúdo sintético:** declarar uso de IA se o YouTube Studio pedir\n"]
    open(os.path.join(EPS, f"EP{n:02d}-PRONTO.md"), "w").write("\n".join(M))


def write_fichas():
    L = ["# Fichas dos personagens (gerar uma vez, guardar)\n",
         "Gere cada ficha **sem anexar nada**, em horizontal 16:9 (é de propósito: mostra frente, lado, costas e rosto). "
         "Confira a contagem de olhos, orelhas, braços, pernas, asas e rabo antes de guardar. O Bento já está aprovado.\n"]
    for c in ["Bento", "Luna", "Tico", "Pipo", "Olívia", "Nina", "Davi"]:
        L += [f"## {nm(c)}\n", "```\n" + g.sheet_prompt(c) + "\n```\n"]
    L += ["## Dica\n", "Depois das 7 fichas, anexe sempre as dos personagens do episódio. Guarde as imagens aprovadas com os nomes SHEET-BENTO, SHEET-LUNA etc.\n"]
    open(os.path.join(BASE, "FICHAS.md"), "w").write("\n".join(L))


def write_index():
    L = ["# 30 Shorts didáticos (Bento e Amigos)\n", "Ordem sugerida de publicação: 1 por dia. Os 1 a 10 têm prompts em `episodios/EPNN-*.md` (versão inicial) e `EP04-*` etc.; "
         "os 11 a 30 estão **prontos para colar** em `episodios/EPNN-PRONTO.md`.\n",
         "| # | Título | Lição | Personagens |", "|---|---|---|---|"]
    for e in g.todos():
        L.append(f"| {e['num']} | {e['titulo']} | {e['tema']} | {', '.join(e['cast'])} |")
    L += ["", "Já produzidos: 1, 2 e 4 (vídeos finais em `out/`). O 3 foi pulado a seu pedido.\n"]
    open(os.path.join(BASE, "INDICE-30.md"), "w").write("\n".join(L))


if __name__ == "__main__":
    for ep in g.NOVOS:
        write_ep(ep)
    write_fichas()
    write_index()
    print(f"{len(g.NOVOS)} episódios, fichas e índice gerados")
