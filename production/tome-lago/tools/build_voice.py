#!/usr/bin/env python3
"""Gera narração (edge-tts, pt-BR) por linha, com timestamps reais de palavra, e monta voice.wav."""
import asyncio, json, os, subprocess, sys, re
import edge_tts
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE, RATE, PITCH = "pt-BR-AntonioNeural", "+6%", "-2Hz"
story = json.load(open(f"{ROOT}/script/story.json"))
os.makedirs(f"{ROOT}/audio/lines", exist_ok=True)
SR = 44100

def run(cmd): subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

async def synth(line):
    text = line["text"]
    out = f"{ROOT}/audio/lines/{line['id']}.mp3"
    ev = []
    c = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH, boundary="WordBoundary",
                             proxy=os.environ.get("HTTPS_PROXY"))
    with open(out, "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio": f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                ev.append({"text": ch["text"], "start": ch["offset"]/1e7, "end": (ch["offset"]+ch["duration"])/1e7})
    run(["ffmpeg","-y","-i",out,"-ar",str(SR),"-ac","1",f"{ROOT}/audio/lines/{line['id']}.wav"])
    dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{ROOT}/audio/lines/{line['id']}.wav"]))
    return ev, dur

async def main():
    t = 0.6  # respiro inicial
    lines_out, words_out, concat = [], [], []
    for ln in story["lines"]:
        ev, dur = await synth(ln)
        t += ln["pause_before"]
        lines_out.append({**ln, "start": round(t,3), "end": round(t+dur,3), "dur": round(dur,3)})
        for w in ev:
            words_out.append({"line": ln["id"], "text": w["text"], "start": round(t+w["start"],3), "end": round(t+w["end"],3)})
        concat.append((ln["id"], t, dur))
        t += dur
    total = round(t + 1.4, 3)  # cauda para loop
    # montar voice.wav com adelay
    inputs, filt = [], []
    for i,(lid, st, d) in enumerate(concat):
        inputs += ["-i", f"{ROOT}/audio/lines/{lid}.wav"]
        filt.append(f"[{i}:a]adelay={int(st*1000)}|{int(st*1000)}[a{i}]")
    mix = "".join(f"[a{i}]" for i in range(len(concat))) + f"amix=inputs={len(concat)}:normalize=0,apad=whole_dur={total}[v]"
    run(["ffmpeg","-y",*inputs,"-filter_complex",";".join(filt)+";"+mix,"-map","[v]","-ar",str(SR),"-ac","1",f"{ROOT}/audio/voice.wav"])
    json.dump({"voice": VOICE, "rate": RATE, "pitch": PITCH, "engine": "edge-tts "+edge_tts.__version__ if hasattr(edge_tts,'__version__') else "edge-tts",
               "total": total, "lines": lines_out, "words": words_out},
              open(f"{ROOT}/script/word-timings.json","w"), ensure_ascii=False, indent=1)
    print("total", total, "words", len(words_out))
asyncio.run(main())
