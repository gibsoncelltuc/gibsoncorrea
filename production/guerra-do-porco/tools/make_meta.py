#!/usr/bin/env python3
"""production.json, storyboard/shots.json, legendas (.srt cartões/.srt frases/.ass) e script/*.md a partir de word-timings.json."""
import json, subprocess, sys, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(f"{ROOT}/script/word-timings.json")); story = json.load(open(f"{ROOT}/script/story.json"))
FPS = 30; KEEP_PUNCT = True   # observado nas referências do canal (ver references/visual-reference-ricks-clips.md)
def wstart(line, pre):
    n = lambda s: re.sub(r"[.,!?:;—-]", "", s.lower())
    return next(w["start"] for w in D["words"] if w["line"] == line and n(w["text"]).startswith(n(pre)))
SB = json.load(open(f"{ROOT}/storyboard/shots.json", encoding="utf-8"))["shots"]   # lista de planos: no piloto vem da EDL (tools/make_storyboard.py); em vídeos novos é editada à mão
prod = {"title": story["title"], "slug": "guerra-do-porco", "language": "pt-BR", "format": "short-pilot", "width": 1080, "height": 1920, "fps": FPS, "durationSeconds": D["total"],
        "pilot_render": {"width": 540, "height": 960, "note": "piloto em baixa resolução a pedido do usuário; mesmo código renderiza 1080x1920"},
        "visualEngine": "blender 5.3 Cycles CPU (bpy) para os quadros + remotion (montagem/legendas) + ffmpeg (grade/áudio)", "visualGeneration": "procedural-code-only", "style_reference": "references/visual-reference-ricks-clips.md",
        "captions": {"wordsPerCard": "1-2", "keepPunctuation": KEEP_PUNCT, "font": "Montserrat 800", "y": "70%"},
        "audio": {"sampleRate": 44100, "channels": 2, "targetIntegratedLufs": -14, "maxTruePeakDbtp": -1.5}, "tts": D.get("engine"), "voice": D["voice"], "rate": D.get("rate", D.get("length_scale")),
        "pipelineVersion": "ricks-3d-toon-story-orchestrator V2 + cloud-render v3.1 + visual-reference"}
json.dump(prod, open(f"{ROOT}/production.json", "w"), ensure_ascii=False, indent=1)
vo = " ".join(l["text"] for l in D["lines"])
open(f"{ROOT}/script/voiceover.txt", "w", encoding="utf-8").write(vo + "\n")
with open(f"{ROOT}/script/script.md", "w", encoding="utf-8") as f:
    f.write(f"# {story['title']} — roteiro (piloto de 20 s)\n\n*História real dramatizada; ver `research/fact-check.md`. Narração pt-BR (Piper `pt_BR-cadu-medium`, dataset CC0), timestamps reais em `word-timings.json`.*\n\n| Beat | Plano | Início–fim | Texto | Intenção de voz | Visual sincronizado |\n|---|---|---|---|---|---|\n")
    intent = {l["id"]: l.get("intent", "") for l in story["lines"]}   # intenção de voz por linha: campo "intent" de script/story.json
    for l in D["lines"]:
        sh = next(x for x in SB if l["id"] in x["lines"])
        f.write(f"| {l['beat']} | {l['shot']} | {l['start']:.2f}–{l['end']:.2f} s | {l['text']} | {intent[l['id']]} | {sh['action']} |\n")
    f.write(f"\n**Duração total:** {D['total']:.2f} s ({len(re.findall(r'\w+', vo))} palavras). **Gancho:** {len(re.findall(r'\w+', D['lines'][0]['text']))} palavras (alvo 9–14).\n")
clean = (lambda s: s) if KEEP_PUNCT else (lambda s: re.sub(r"[.,!?:;—\"]+$", "", s))
chunks = []; w = D["words"]; i = 0
while i < len(w):
    a = w[i]; b = w[i + 1] if i + 1 < len(w) else None; ends = bool(re.search(r"[.!?:,;]$", a["text"]))   # a vírgula também fecha o cartão: o sintagma não atravessa a pausa
    if b and b["line"] == a["line"] and not ends and (len(a["text"]) <= 3 or (len(b["text"]) <= 3 and len(a["text"]) <= 6)): chunks.append((clean(a["text"]) + " " + clean(b["text"]), a["start"], b["end"])); i += 2
    else: chunks.append((clean(a["text"]), a["start"], a["end"])); i += 1
PUNCT = re.compile(r"[.!?:,;]$")
def merge_short(ch, tmin=0.30, maxc=20):
    """cartão com janela de exibição < 0,30 s (palavras funcionais ditas rápido: "de um") é fundido ao vizinho, no limite de 20 caracteres — legível a olho nu;
    um cartão que termina em vírgula funde com o ANTERIOR (a vírgula fecha o sintagma), os demais com o PRÓXIMO"""
    i = 0
    while i < len(ch):
        tx, s0, e0 = ch[i]; dur = (ch[i + 1][1] - s0) if i + 1 < len(ch) else 9
        if dur < tmin:
            can_prev = i > 0 and len(ch[i - 1][0]) + 1 + len(tx) <= maxc and not PUNCT.search(ch[i - 1][0])
            can_next = i + 1 < len(ch) and len(tx) + 1 + len(ch[i + 1][0]) <= maxc and not PUNCT.search(tx)
            if PUNCT.search(tx) and can_prev: ch[i - 1:i + 1] = [(ch[i - 1][0] + " " + tx, ch[i - 1][1], e0)]; i -= 1; continue
            if can_next: ch[i:i + 2] = [(tx + " " + ch[i + 1][0], s0, ch[i + 1][2])]; continue
            if can_prev: ch[i - 1:i + 1] = [(ch[i - 1][0] + " " + tx, ch[i - 1][1], e0)]; i -= 1; continue
        i += 1
    return ch
FUNC = {"o", "a", "os", "as", "de", "do", "da", "dos", "das", "um", "uma", "em", "e", "no", "na", "que", "dois", "duas"}
def keep_phrases(ch, maxc=18):
    """cartão que termina em artigo/preposição/numeral ("navios de", "Só o", "e dois") leva a palavra seguinte da mesma frase: o sintagma não é partido entre cartões"""
    i = 0
    while i + 1 < len(ch):
        tx, s0, e0 = ch[i]; last = re.sub(r"[.,!?:;—-]", "", tx.split()[-1].lower())
        if last in FUNC and not PUNCT.search(tx) and len(tx) + 1 + len(ch[i + 1][0]) <= maxc: ch[i:i + 2] = [(tx + " " + ch[i + 1][0], s0, ch[i + 1][2])]; continue
        i += 1
    return ch
chunks = keep_phrases(merge_short(chunks))
def windows(ch, total, lead=0.1, tail=0.35, tmin=0.30, cps=20.0):
    """(início, fim) de cada cartão: entra 0,1 s antes da palavra; um cartão curto "empresta" tempo do anterior para cumprir ≥ 0,30 s e ≤ 20 caracteres/s (leitura confortável)"""
    st = [max(0.0, s0 - lead) for _, s0, _ in ch]; en = []
    for k, (tx, s0, e0) in enumerate(ch):
        nxt = ch[k + 1][1] - lead if k + 1 < len(ch) else total; en.append(min(e0 + tail, max(nxt, e0)))
    need = [max(tmin, len(tx) / cps) for tx, _, _ in ch]; eff = lambda k: (min(en[k], st[k + 1]) if k + 1 < len(ch) else en[k]) - st[k]
    for k in range(1, len(ch)):
        d = need[k] - eff(k)
        if d > 1e-6:
            take = min(d, max(0.0, eff(k - 1) - need[k - 1]))
            if take > 0: st[k] -= take
    return list(zip(st, [min(en[k], st[k + 1]) if k + 1 < len(ch) else en[k] for k in range(len(ch))]))
WIN = windows(chunks, D["total"])
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"
os.makedirs(f"{ROOT}/renders", exist_ok=True)
with open(f"{ROOT}/renders/final.srt", "w", encoding="utf-8") as f:
    for k, (tx, s0, e0) in enumerate(chunks): f.write(f"{k+1}\n{ts(WIN[k][0])} --> {ts(WIN[k][1])}\n{tx}\n\n")
with open(f"{ROOT}/renders/final_frases.srt", "w", encoding="utf-8") as f:
    for k, l in enumerate(D["lines"]): f.write(f"{k+1}\n{ts(l['start'])} --> {ts(l['end'])}\n{l['text']}\n\n")
with open(f"{ROOT}/renders/final.ass", "w", encoding="utf-8") as f:
    f.write("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n")
    f.write("Style: Cap,Montserrat ExtraBold,123,&H00FFFFFF,&H001A0E12,&H90000000,1,0,0,0,100,100,0,0,1,7,3,2,40,40,485,1\n\n[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n")
    a = lambda t: f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
    for k, (tx, s0, e0) in enumerate(chunks): f.write(f"Dialogue: 0,{a(WIN[k][0])},{a(WIN[k][1])},Cap,,0,0,0,,{{\\fscx108\\fscy108\\t(0,90,\\fscx100\\fscy100)}}{tx}\n")
print(len(chunks), "cartões;", len(SB), "planos")
