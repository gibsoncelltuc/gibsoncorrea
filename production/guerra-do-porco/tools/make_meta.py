#!/usr/bin/env python3
"""production.json, storyboard/shots.json, legendas (.srt cartões/.srt frases/.ass) e script/*.md a partir de word-timings.json."""
import json, subprocess, sys, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(f"{ROOT}/script/word-timings.json")); story = json.load(open(f"{ROOT}/script/story.json"))
FPS = 30; KEEP_PUNCT = True   # observado nas referências do canal (ver references/visual-reference-ricks-clips.md)
def wstart(line, pre):
    n = lambda s: re.sub(r"[.,!?:;—-]", "", s.lower())
    return next(w["start"] for w in D["words"] if w["line"] == line and n(w["text"]).startswith(n(pre)))
L = {l["id"]: l for l in D["lines"]}
starts = [("S1", 0.0), ("S2", L["L2"]["start"] - .3), ("S3", L["L3"]["start"] - .3), ("S4", L["L4"]["start"] - .3), ("S5", L["L5"]["start"] - .3), ("S6", wstart("L5", "ninguém") - .3)]
info = {
 "S1": ("GANCHO: ato sem sentido, razão escondida (matar um porco → quase guerra)", "ground-level fov 60 → crane-up ao tiro; revela horizonte com navios e acampamento", "porco come; Cutlar mira e atira ('matou'); porco capota; navios surgem no horizonte ('guerra')", "BANG1 + flash + tremor", ["L1"]),
 "S2": ("SETUP: o porco do britânico invade a horta do americano; 'Ele atirou'", "tilt-up na bandeira britânica → dolly lateral pela cerca (placa SAN JUAN 1859) → push-in", "porco cruza a brecha e come; Cutlar nota, mira e dispara ('atirou')", "BANG2 + flash", ["L2"]),
 "S3": ("ZOMBADOR: cem dólares × dez (close inclinado)", "baixa, roll 0.13, push-in lento", "Griffin exibe nota $100 e ri; Cutlar suado com nota $10; porco morto entre eles", "notas, risada", ["L3"]),
 "S4": ("ESCALADA: centenas de soldados → cinco navios de guerra", "dolly lateral baixo acompanhando a marcha → sobe e panorâmica sobre os soldados até a frota", "bloco de 40 soldados em marcha (InstancedMesh) + capitão; fragatas em escalão", "marcha, canhão", ["L4"]),
 "S5": ("PAGAMENTO (1/2): o almirante recusa atacar", "baixa, roll −0.1, push-in no almirante", "auxiliar aponta a luneta; almirante levanta a mão ('pare'), auxiliar murcha", "gaivotas/mar", ["L5"]),
 "S6": ("PAGAMENTO (2/2) + LOOP: 'Ninguém morreu. Só o porco.' (túmulo no lugar do 1º quadro)", "pull-back até o enquadramento exato do quadro 0 (loop)", "túmulo com cruz e flores; os dois tiram o chapéu; mesmo enquadramento do gancho", "sino/acorde final", ["L5"]),
}
shots = []
for i, (sid, st) in enumerate(starts):
    en = starts[i + 1][1] if i + 1 < len(starts) else D["total"]
    shots.append({"id": sid, "start": round(st, 3), "end": round(en, 3), "lines": info[sid][4], "purpose": info[sid][0], "camera": info[sid][1], "action": info[sid][2], "audio": info[sid][3]})
os.makedirs(f"{ROOT}/storyboard", exist_ok=True)
# storyboard/shots.json agora vem da EDL (tools/make_storyboard.py) — não sobrescrever aqui
subprocess.run([sys.executable, os.path.join(ROOT, "tools", "make_storyboard.py")])
prod = {"title": story["title"], "slug": "guerra-do-porco", "language": "pt-BR", "format": "short-pilot", "width": 1080, "height": 1920, "fps": FPS, "durationSeconds": D["total"],
        "pilot_render": {"width": 540, "height": 960, "note": "piloto em baixa resolução a pedido do usuário; mesmo código renderiza 1080x1920"},
        "visualEngine": "remotion + three/R3F (swangle/SwiftShader CPU)", "visualGeneration": "procedural-code-only", "style_reference": "references/visual-reference-ricks-clips.md",
        "captions": {"wordsPerCard": "1-2", "keepPunctuation": KEEP_PUNCT, "font": "Montserrat 800", "y": "70%"},
        "audio": {"sampleRate": 44100, "channels": 2, "targetIntegratedLufs": -14, "maxTruePeakDbtp": -1.5}, "tts": D.get("engine"), "voice": D["voice"], "rate": D.get("rate", D.get("length_scale")),
        "pipelineVersion": "ricks-3d-toon-story-orchestrator V2 + cloud-render v3.1 + visual-reference"}
json.dump(prod, open(f"{ROOT}/production.json", "w"), ensure_ascii=False, indent=1)
vo = " ".join(l["text"] for l in D["lines"])
open(f"{ROOT}/script/voiceover.txt", "w", encoding="utf-8").write(vo + "\n")
with open(f"{ROOT}/script/script.md", "w", encoding="utf-8") as f:
    f.write(f"# {story['title']} — roteiro (piloto de 20 s)\n\n*História real dramatizada; ver `research/fact-check.md`. Narração pt-BR (edge-tts), timestamps reais em `word-timings.json`.*\n\n| Beat | Plano | Início–fim | Texto | Intenção de voz | Visual sincronizado |\n|---|---|---|---|---|---|\n")
    intent = {"L1": "curiosidade/descrença, rápido", "L2": "explicação seca; 'Ele atirou' seco, sem pausa dramática", "L3": "ironia leve; 'cem' enfático", "L4": "tensão crescente", "L5": "alívio irônico; 'Só o porco' lento"}
    for l in D["lines"]:
        sh = next(s for s in shots if l["id"] in s["lines"]) 
        f.write(f"| {l['beat']} | {l['shot']} | {l['start']:.2f}–{l['end']:.2f} s | {l['text']} | {intent[l['id']]} | {sh['action']} |\n")
    f.write(f"\n**Duração total:** {D['total']:.2f} s ({len(re.findall(r'\w+', vo))} palavras). **Gancho:** {len(re.findall(r'\w+', D['lines'][0]['text']))} palavras (alvo 9–14).\n")
clean = (lambda s: s) if KEEP_PUNCT else (lambda s: re.sub(r"[.,!?:;—\"]+$", "", s))
chunks = []; w = D["words"]; i = 0
while i < len(w):
    a = w[i]; b = w[i + 1] if i + 1 < len(w) else None; ends = bool(re.search(r"[.!?:]$", a["text"]))
    if b and b["line"] == a["line"] and not ends and (len(a["text"]) <= 3 or (len(b["text"]) <= 3 and len(a["text"]) <= 6)): chunks.append((clean(a["text"]) + " " + clean(b["text"]), a["start"], b["end"])); i += 2
    else: chunks.append((clean(a["text"]), a["start"], a["end"])); i += 1
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"
os.makedirs(f"{ROOT}/renders", exist_ok=True)
with open(f"{ROOT}/renders/final.srt", "w", encoding="utf-8") as f:
    for k, (tx, s0, e0) in enumerate(chunks):
        nxt = chunks[k + 1][1] - 0.1 if k + 1 < len(chunks) else D["total"]
        f.write(f"{k+1}\n{ts(max(0,s0-0.1))} --> {ts(min(e0+0.35, max(nxt, e0)))}\n{tx}\n\n")
with open(f"{ROOT}/renders/final_frases.srt", "w", encoding="utf-8") as f:
    for k, l in enumerate(D["lines"]): f.write(f"{k+1}\n{ts(l['start'])} --> {ts(l['end'])}\n{l['text']}\n\n")
with open(f"{ROOT}/renders/final.ass", "w", encoding="utf-8") as f:
    f.write("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n")
    f.write("Style: Cap,Montserrat ExtraBold,123,&H00FFFFFF,&H001A0E12,&H90000000,1,0,0,0,100,100,0,0,1,7,3,2,40,40,485,1\n\n[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n")
    for k, (tx, s0, e0) in enumerate(chunks):
        nxt = chunks[k + 1][1] - 0.1 if k + 1 < len(chunks) else D["total"]; e = min(e0 + 0.35, max(nxt, e0)); a = lambda t: f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
        f.write(f"Dialogue: 0,{a(max(0,s0-0.1))},{a(e)},Cap,,0,0,0,,{{\\fscx108\\fscy108\\t(0,90,\\fscx100\\fscy100)}}{tx}\n")
print(len(chunks), "cartões;", len(shots), "planos")
