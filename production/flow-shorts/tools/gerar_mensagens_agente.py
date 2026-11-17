#!/usr/bin/env python3
"""Gera, para cada episódio, as mensagens prontas para colar no agente do Google Flow:
fichas novas, 6 imagens e 6 vídeos (sem música cantada: a música entra na edição).
Saída: ../episodios/EPNN-MENSAGENS-AGENTE.md"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerar_pacote as g

HAVE_SHEETS = {"Bento", "Docinhos"}      # fichas já aprovadas
BENTO_EARS = ("Bento is a LOP-EARED bunny: he has exactly TWO soft floppy ears that ALWAYS hang down along both sides of "
              "his head, one on each side, pink inside. His ears NEVER stand upright and he NEVER has a second pair of ears.")


def nm(c): return "SHEET-" + c.upper().replace("Í", "I")


def blocks(ep, with_audio):
    cast = ep["cast"]
    refs = " and ".join(nm(c) for c in cast)
    notes = (BENTO_EARS + "\n\n") if "Bento" in cast else ""
    locks = "; ".join(g.CAST[c][1] for c in cast)
    neg = ("NEGATIVE: upright or standing ears, a second pair of ears, three or four ears, extra or duplicated arms, legs, hands, "
           "fingers, tails, eyes, heads, beaks; merged or melting limbs; a character splitting or morphing; color, size or outfit "
           "changes; characters appearing or disappearing; text, letters, logos; scary or sudden elements.")
    return refs, notes, locks, neg


def fichas_msg(ep):
    new = [c for c in ep["cast"] if c not in HAVE_SHEETS]
    if not new: return None
    out = ["Generate %d character reference sheet(s), one image each, wide horizontal 16:9, plain white background, evenly spaced views: "
           "front view, side view, back view and one happy close-up of the face, neutral standing pose. Name them: %s.\n"
           % (len(new), ", ".join(nm(c) for c in new)),
           "Shared style: high-quality stylized 3D animated feature-film look, soft rounded shapes, big expressive eyes, warm cinematic "
           "lighting, rich gentle colors, no text, no letters, no logos, nothing scary.\n"]
    for c in new:
        out.append(f"{nm(c)}: {g.CAST[c][0]}. {g.CAST[c][1]}.\n")
    out.append("Check each sheet after generating. If any character has extra or duplicated ears, arms, legs, eyes, tails or a second set of "
               "any body part, regenerate that sheet (up to 2 times). Do not continue until all sheets are correct.")
    return "\n".join(out)


def imagens_msg(ep):
    n = ep["num"]; refs, notes, locks, neg = blocks(ep, False)
    L = [f"Using the attached reference sheets {refs}, generate 6 separate images, named E{n:02d}-1 to E{n:02d}-6. "
         "Generate them one at a time, in order. Every character must be exactly identical to its reference sheet.\n",
         "ASPECT RATIO (very important): every image must be VERTICAL portrait 9:16 (1080x1920), like a phone screen, filling the whole "
         "frame. Do NOT make landscape 16:9 images. Do NOT add blurred bars, letterboxing or borders.\n", notes + 
         f"COMMON SETTING for all 6: {ep['setting']}.\n",
         "COMMON STYLE for all 6: high-quality stylized 3D animated feature-film look, soft rounded shapes, big expressive eyes, fluffy fur, "
         "warm cinematic lighting, shallow depth of field, rich gentle colors, no text, no letters, no logos, nothing scary. Keep the "
         "lower-left corner of the frame simple and uncluttered.\n",
         f"ANATOMY LOCK for all 6: {locks}.\n", f"NEGATIVE for all 6: {neg[10:]}\n"]
    for i, s in enumerate(ep["shots"], 1):
        L.append(f"E{n:02d}-{i} (use {' and '.join(nm(c) for c in s['chars'])}): {s['cam']}. {s['img']}.\n")
    L.append("After each image, check it. Count the ears, eyes, arms, legs and tails of every character. If anything is extra, duplicated, "
             "upright when it should be floppy, or different from its sheet, regenerate that image (up to 2 times) before moving on. "
             "When all 6 are done, show them together in order.")
    return "\n".join(L)


def videos_msg(ep):
    n = ep["num"]; refs, notes, locks, neg = blocks(ep, True)
    L = [f"Using the attached reference sheets {refs} and the 6 starting images E{n:02d}-1 to E{n:02d}-6, generate 6 separate videos "
         f"named V{n:02d}-1 to V{n:02d}-6. Each video is exactly 10 seconds, VERTICAL portrait 9:16 (no landscape, no blurred bars), 720p. Generate them one at a time, in order. "
         f"Video V{n:02d}-k must START from image E{n:02d}-k as its first frame. Every character must stay exactly identical to its "
         "reference sheet from the first to the last frame.\n", notes +
         f"COMMON SETTING for all 6: {ep['setting']}.\n",
         "COMMON STYLE for all 6: high-quality stylized 3D animated feature-film look, soft rounded shapes, big expressive eyes, fluffy fur, "
         "warm cinematic lighting, shallow depth of field, rich gentle colors, smooth natural character animation, no on-screen text, "
         "no letters, no logos, nothing scary. Keep the lower-left corner of the frame simple and uncluttered.\n",
         f"ANATOMY LOCK for all 6 (counts never change during the clip): {locks}.\n",
         "MOVEMENT RULES for all 6: one slow, simple, continuous action; all body parts stay attached and in view; "
         + ("Bento's two floppy ears always hang down and only sway gently; " if "Bento" in ep["cast"] else "")
         + "no fast spinning; no camera shake; no cuts inside the clip.\n",
         "AUDIO for all 6: ONLY soft sound effects. No music, no singing, no speech.\n", f"NEGATIVE for all 6: {neg[10:]}\n"]
    for i, s in enumerate(ep["shots"], 1):
        L.append(f"V{n:02d}-{i} (start from E{n:02d}-{i}; use {' and '.join(nm(c) for c in s['chars'])})\n"
                 f"Shot: {s['cam']}. Action: {s['act']}.\nSound effects: {s['sfx']}.\n")
    L.append("After each video, check it frame by frame. Count the ears, eyes, arms, legs and tails of every character at the start, "
             "middle and end. If any character ever has extra or duplicated body parts, an upright ear where ears should hang, or changes "
             "look, regenerate that video (up to 2 times) before moving on. When all 6 are done, show them in order.")
    return "\n".join(L)


def main():
    for ep in g.EPISODES:
        P = [f"# Ep. {ep['num']:02d}: mensagens prontas para o agente do Flow\n",
             "Cole uma mensagem de cada vez, na ordem. Antes de cada passo, deixe anexado o que ele pede.\n"]
        f = fichas_msg(ep)
        if f:
            P += ["## Mensagem 1: fichas dos personagens novos\n", "```\n" + f + "\n```\n"]
        P += ["## Mensagem %d: as 6 imagens\n" % (2 if f else 1),
              "Anexe as fichas: " + ", ".join(nm(c) for c in ep["cast"]) + ".\n", "```\n" + imagens_msg(ep) + "\n```\n",
              "## Mensagem %d: os 6 vídeos\n" % (3 if f else 2),
              "Anexe as fichas e as 6 imagens aprovadas (conte as orelhas antes!).\n", "```\n" + videos_msg(ep) + "\n```\n",
              "## Depois\n", f"Me mande os 6 vídeos, **um por mensagem, na ordem 1 a 6**. A música do episódio eu gero à parte (ACE-Step) e monto por cima.\n"]
        path = os.path.join(g.EPS_DIR, f"EP{ep['num']:02d}-MENSAGENS-AGENTE.md")
        open(path, "w").write("\n".join(P))
        print(path)


if __name__ == "__main__":
    main()
