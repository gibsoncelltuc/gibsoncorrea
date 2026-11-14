#!/usr/bin/env python3
"""Narração edge-tts pt-BR, sintetizada FRASE A FRASE (controle de respiro), com timestamps reais de palavra.
Cada frase é aparada pelos próprios limites de palavra e posicionada na linha do tempo; gera voice.wav e word-timings.json."""
import asyncio, json, os, re, subprocess
import edge_tts
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE, RATE, PITCH = "pt-BR-AntonioNeural", "+14%", "-2Hz"
SEG_GAP, LEAD, TAIL = 0.10, 0.25, 0.85
SR = 44100
story = json.load(open(f"{ROOT}/script/story.json"))
os.makedirs(f"{ROOT}/audio/lines", exist_ok=True)
def run(cmd): subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
async def synth(text, name):
    out = f"{ROOT}/audio/lines/{name}.mp3"
    for attempt in range(5):
        ev = []
        try:
            c = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH, boundary="WordBoundary", proxy=os.environ.get("HTTPS_PROXY"))
            with open(out, "wb") as f:
                async for ch in c.stream():
                    if ch["type"] == "audio": f.write(ch["data"])
                    elif ch["type"] == "WordBoundary": ev.append({"text": ch["text"], "start": ch["offset"] / 1e7, "end": (ch["offset"] + ch["duration"]) / 1e7})
            if ev: return out, ev
        except Exception as e:
            print("tentativa", attempt + 1, name, "falhou:", type(e).__name__)
        await asyncio.sleep(1.5 * (attempt + 1))
    raise RuntimeError("TTS falhou: " + name)
async def main():
    t = LEAD; lines_out, words_out, placed = [], [], []
    for ln in story["lines"]:
        sentences = [s for s in re.split(r"(?<=[.!?])\s+", ln["text"].strip()) if s]
        t += ln["pause_before"]; l_start = t; l_end = t
        for si, sent in enumerate(sentences):
            name = f"{ln['id']}_{si}"; mp3, ev = await synth(sent, name)
            a = max(0.0, ev[0]["start"] - 0.05); b = ev[-1]["end"] + 0.13; d = b - a
            wav = f"{ROOT}/audio/lines/{name}.wav"
            run(["ffmpeg", "-y", "-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", mp3, "-ar", str(SR), "-ac", "1", wav])
            placed.append((wav, t))
            for w in ev: words_out.append({"line": ln["id"], "text": w["text"], "start": round(t + w["start"] - a, 3), "end": round(t + w["end"] - a, 3)})
            l_end = t + d; t += d + SEG_GAP
        t -= SEG_GAP
        lines_out.append({**ln, "start": round(l_start, 3), "end": round(l_end, 3), "dur": round(l_end - l_start, 3)})
    total = round(t + TAIL, 3)
    inputs, filt = [], []
    for i, (wav, st) in enumerate(placed):
        inputs += ["-i", wav]; filt.append(f"[{i}:a]adelay={int(st*1000)}|{int(st*1000)}[a{i}]")
    mix = "".join(f"[a{i}]" for i in range(len(placed))) + f"amix=inputs={len(placed)}:normalize=0,apad=whole_dur={total}[v]"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filt) + ";" + mix, "-map", "[v]", "-ar", str(SR), "-ac", "1", f"{ROOT}/audio/voice.wav"])
    json.dump({"voice": VOICE, "rate": RATE, "pitch": PITCH, "engine": "edge-tts " + edge_tts.__version__ if hasattr(edge_tts, "__version__") else "edge-tts",
               "total": total, "lines": lines_out, "words": words_out}, open(f"{ROOT}/script/word-timings.json", "w"), ensure_ascii=False, indent=1)
    print("total", total, "palavras", len(words_out))
asyncio.run(main())
import subprocess, sys; subprocess.run([sys.executable, os.path.join(ROOT, "tools", "fix_tokens.py")])
