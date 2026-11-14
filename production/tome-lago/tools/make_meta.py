#!/usr/bin/env python3
"""Gera production.json, shots.json, captions (.srt cartões + .srt por frase + .ass) a partir de word-timings.json."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(f"{ROOT}/script/word-timings.json")); story = json.load(open(f"{ROOT}/script/story.json"))
FPS = 30
order = ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]
info = {
 "S1": ("gancho+setup: ato sem sentido, razão escondida", "push-in lento do cais; segue o arremesso", "Tomé arremessa cadeiras no lago (2x), respingo + ondas"),
 "S2": ("zombador: sarcasmo", "close-up baixo, inclinado (roll), push-in", "Zeca ri e grita a frase; vilarejo ri ao fundo"),
 "S3": ("herói calmo, enigmático", "close baixo, push-in leve", "Tomé sorri, não explica"),
 "S4": ("escalada x3 (mesa, cama, porta) + estações", "câmera lateral lenta; outono→crepúsculo→inverno", "arremessos; multidão ri / aponta"),
 "S5": ("'você sabe': analogia cotidiana (dinheiro/carro)", "câmera acompanha Ana até o carro", "moedas no pote; roda do carro quebra; pote conserta"),
 "S6": ("pagamento mostrado, sem moral", "wide → tracking lateral ao longo da ponte", "balsa afunda; ponte de móveis sob a água; Tomé e Zeca atravessam"),
 "S7": ("loop: último quadro ecoa o primeiro", "dolly curto, enquadramento do gancho", "Zeca chega ao cais com uma cadeira"),
}
shots = []
for i, sid in enumerate(order):
    first = next(l for l in D["lines"] if l["shot"] == sid); nxt = next((l for l in D["lines"] if l["shot"] == order[i + 1]), None) if i + 1 < len(order) else None
    st = 0.0 if i == 0 else first["start"] - 0.3; en = nxt["start"] - 0.3 if nxt else D["total"]
    ln = [l["id"] for l in D["lines"] if l["shot"] == sid]
    shots.append({"id": sid, "start": round(st, 3), "end": round(en, 3), "lines": ln, "purpose": info[sid][0], "camera": info[sid][1], "action": info[sid][2]})
json.dump({"shots": shots}, open(f"{ROOT}/storyboard_shots.json", "w"), ensure_ascii=False, indent=1)
os.makedirs(f"{ROOT}/storyboard", exist_ok=True); os.replace(f"{ROOT}/storyboard_shots.json", f"{ROOT}/storyboard/shots.json")
json.dump({"title": story["title"], "slug": "tome-lago", "language": "pt-BR", "format": "short", "width": 1080, "height": 1920, "fps": FPS,
           "durationSeconds": D["total"], "visualEngine": "remotion-three (Three.js + R3F), render swangle/SwiftShader CPU", "visualGeneration": "procedural-code-only",
           "captionWordsPerCard": "1-2", "audio": {"sampleRate": 44100, "channels": 2, "targetIntegratedLufs": -14, "maxTruePeakDbtp": -1.5, "note": "alvos do perfil v3.1 do usuário (zip V2 sugere -15/-1.0)"},
           "pipelineVersion": "ricks-3d-toon-story-orchestrator V2 + perfil cloud-render v3.1", "tts": D.get("engine"), "voice": D["voice"]},
          open(f"{ROOT}/production.json", "w"), ensure_ascii=False, indent=1)

clean = lambda s: re.sub(r"[.,!?:;—\"]+$", "", re.sub(r'^["—]+', "", s))
chunks = []; w = D["words"]; i = 0
while i < len(w):
    a = w[i]; b = w[i + 1] if i + 1 < len(w) else None
    ends = bool(re.search(r"[.!?:]$", a["text"]))
    if b and b["line"] == a["line"] and not ends and (len(a["text"]) <= 3 or (len(b["text"]) <= 3 and len(a["text"]) <= 6)):
        chunks.append((clean(a["text"]) + " " + clean(b["text"]), a["start"], b["end"])); i += 2
    else: chunks.append((clean(a["text"]), a["start"], a["end"])); i += 1
def ts(t, sep=","): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f"{h:02d}:{m:02d}:{int(s):02d}{sep}{int(round((s - int(s)) * 1000)):03d}"
with open(f"{ROOT}/renders/final.srt", "w", encoding="utf-8") as f:
    for k, (tx, s0, e0) in enumerate(chunks):
        nxt = chunks[k + 1][1] - 0.1 if k + 1 < len(chunks) else D["total"]
        f.write(f"{k+1}\n{ts(max(0,s0-0.1))} --> {ts(min(e0+0.35, max(nxt, e0)))}\n{tx}\n\n")
with open(f"{ROOT}/renders/final_frases.srt", "w", encoding="utf-8") as f:
    for k, l in enumerate(D["lines"]): f.write(f"{k+1}\n{ts(l['start'])} --> {ts(l['end'])}\n{l['text']}\n\n")
with open(f"{ROOT}/renders/final.ass", "w", encoding="utf-8") as f:
    f.write("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n")
    f.write("Style: Cap,Montserrat ExtraBold,76,&H00FFFFFF,&H001A0E12,&H00000000,1,0,0,0,100,100,1,0,1,15,0,2,40,40,575,1\n\n[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n")
    for k, (tx, s0, e0) in enumerate(chunks):
        nxt = chunks[k + 1][1] - 0.1 if k + 1 < len(chunks) else D["total"]; e = min(e0 + 0.35, max(nxt, e0))
        a = lambda t: f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
        f.write(f"Dialogue: 0,{a(max(0,s0-0.1))},{a(e)},Cap,,0,0,0,,{{\\fscx108\\fscy108\\t(0,90,\\fscx100\\fscy100)}}{tx}\n")
print(len(chunks), "cartões de legenda;", len(shots), "shots")
