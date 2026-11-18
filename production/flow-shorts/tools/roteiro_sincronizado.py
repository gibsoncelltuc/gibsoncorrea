#!/usr/bin/env python3
"""Roteiro sincronizado: cada ação do vídeo presa ao segundo em que a palavra é cantada. Uso: roteiro_sincronizado.py N
Lê ../musicas-virais/tempos/NN.json (alinhar_musica.py) + cenas_musicas.py e grava ../roteiros-sincronizados/NN-slug.md"""
import sys, os, json, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gerar_pacote as g, gerar_pronto  # registra Bentinho/Mamãe/Papai em g.CAST
import musicas_virais as m
from cenas_musicas import CENAS
OUT = os.path.join(HERE, "..", "roteiros-sincronizados"); os.makedirs(OUT, exist_ok=True)
CLIP = 10.0
norm = lambda w: re.sub(r"[^a-zà-ú]", "", w.lower())
BPM_TXT = "{bpm} BPM, ukulele, soft shaker, gentle hand claps, glockenspiel melody, soft bass, warm friendly male lead voice with a sweet kids choir"

def fence(s): return "```text\n" + s + "\n```"

def build(n):
    T = json.load(open(os.path.join(HERE, "..", "musicas-virais", "tempos", f"{n:02d}.json"), encoding="utf-8"))
    P = T["palavras"]; song = m.SONGS[n]; md = []; avisos = []
    md.append(f"# Roteiro sincronizado: {song['titulo']}\n")
    md.append(f"Música de {T['dur']:.1f} s (cortar em **60,0 s** na edição), {song['bpm']} BPM. São **6 clipes de 10 s** no Flow. "
              f"Cada ação abaixo acontece no segundo em que a palavra é cantada. Tempos medidos na música pronta; "
              f"{T['cobertura']:.0%} das palavras tiveram o tempo medido direto, o resto foi calculado entre palavras vizinhas.\n")
    md.append("**Como usar:** gere as 6 imagens iniciais, depois cada vídeo de 10 s a partir da imagem do mesmo número. O som do Flow será trocado pela música, "
              "mas a letra no prompt faz a boca e os gestos acompanharem.\n")
    for k, c in enumerate(CENAS[n]):
        a, b = k * CLIP, (k + 1) * CLIP
        ws = [w for w in P if a <= w["t0"] < b]
        if not ws: avisos.append(f"clipe {k+1}: sem palavras cantadas"); continue
        # linhas cantadas neste clipe
        lines = {}
        for w in ws: lines.setdefault(w["line"], []).append(w)
        sung = []
        for li, lw in lines.items():
            sung.append(" ".join(x["w"] for x in lw))
        timed = " ".join(f"{w['w']} ({w['t0']-a:.1f}s)" for w in ws)
        pausas = [f"{x['t1']-a:.1f}–{y['t0']-a:.1f}s" for x, y in zip(ws, ws[1:]) if y["t0"] - x["t1"] >= 0.35]
        # eventos
        ev = []; usados = set()
        for key in c["keys"]:
            word, act = key[0], key[1]; nth = key[2] if len(key) > 2 else 1
            hits = [w for w in ws if norm(w["w"]) == norm(word)]
            if len(hits) < nth: avisos.append(f"clipe {k+1}: palavra '{word}' (#{nth}) não está nesta janela"); continue
            w = hits[nth - 1]; ev.append((w["t0"] - a, w["w"], act))
        ev.sort()
        for (t1, w1, _), (t2, w2, _) in zip(ev, ev[1:]):
            if t2 - t1 < 1.2: avisos.append(f"clipe {k+1}: ações em '{w1}' e '{w2}' ficam a {t2-t1:.1f}s uma da outra (rápido demais para o Flow)")
        corte = [w for w in P if w["t0"] < b < w["t1"]]
        # fim de frase cortada
        last = ws[-1]; prox = [w for w in P if w["line"] == last["line"] and w["t0"] >= b]
        if prox: avisos.append(f"clipe {k+1}: a frase \"{' '.join(x['w'] for x in lines[last['line']])} ...\" continua no clipe {k+2} ({' '.join(x['w'] for x in prox)}). Termine o clipe no meio do gesto e comece o próximo com a mesma pose.")
        d, l = zip(*[g.CAST[x] for x in c["chars"]])
        ts = "; ".join(f"at {t:.1f} s the voice sings “{w}” → {act}" for t, w, act in ev)
        img = (f"Using the attached reference sheets (keep every character exactly identical to its sheet): {'; '.join(d)}.\n"
               f"Setting: {c['setting']}.\nShot: {c['cam']}. Starting pose: {c['img']}.\n"
               f"Anatomy lock: {'; '.join(l)}. All other body parts stay normal and attached.\n"
               f"{g.STYLE} Vertical 9:16, full frame, no black or blurred bars. Keep the lower-left corner simple and uncluttered.\n{g.NEG_IMG}")
        vid = (f"{g.STYLE}\nCharacters (identical to the attached reference sheets): {'; '.join(d)}.\nSetting: {c['setting']}.\n"
               f"Shot: {c['cam']}. Start exactly from the attached start image.\n"
               f"Timed action, everything slow, simple and gentle, one action at a time: {ts}. Between these moments the characters just sway softly to the beat.\n"
               f"Anatomy lock: {'; '.join(l)}. Counts never change.\n{g.RULE_VIDEO}\n"
               f"Audio: original cheerful Brazilian children's song, {BPM_TXT.format(bpm=song['bpm'])}; no intro, no ending, no fade, no silence. "
               f"Sung in Brazilian Portuguese, exactly these words at these times (seconds from clip start) and nothing else: {timed}.\n{g.NEG_VIDEO}")
        md.append(f"\n---\n\n## Clipe {k+1}: {a:.0f}–{b:.0f} s\n")
        md.append(f"**Personagens:** {', '.join(c['chars'])}\n\n**Letra cantada neste trecho:**\n")
        for li, lw in lines.items(): md.append(f"- {' '.join(x['w'] for x in lw)}  _(começa em {lw[0]['t0']-a:.1f}s)_")
        md.append("\n**O que acontece na tela, no tempo da palavra:**\n")
        for t, w, act in ev: md.append(f"- **{t:.1f}s** — “{w}”: {act}")
        if pausas: md.append(f"\n**Pausas para respirar (cabe um olhar/sorriso):** {', '.join(pausas)}")
        md.append(f"\n**Mensagem de IMAGEM (anexe as fichas dos personagens):**\n\n{fence(img)}\n")
        md.append(f"**Mensagem de VÍDEO (use a imagem {k+1} como início):**\n\n{fence(vid)}\n")
    md.append("\n---\n\n## Edição final\n\n- Cortar a música em 60,0 s.\n- Cortes entre clipes nos segundos 10, 20, 30, 40 e 50.\n- Trocar o áudio do Flow pela música aprovada.")
    if avisos:
        md.append("\n## Atenção (frases que cruzam o corte e palavras fora da janela)\n"); md += [f"- {x}" for x in avisos]
    p = os.path.join(OUT, f"{n:02d}-{song['slug']}.md"); open(p, "w", encoding="utf-8").write("\n".join(md) + "\n")
    return p, avisos

if __name__ == "__main__":
    for n in map(int, sys.argv[1:]):
        p, av = build(n); print(p); [print("  AVISO:", x) for x in av]
