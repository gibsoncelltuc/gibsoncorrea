#!/usr/bin/env python3
"""Montagem com várias tomadas por seção (edição dinâmica) a partir de um JSON.

Cada tomada ("shot") corta um pedaço de um clipe, com reenquadramento opcional (zoom + âncora) e uma transição
para a tomada seguinte ("cut" = corte seco quase invisível, ou um efeito do ffmpeg: smoothleft, zoomin, circleopen,
fadewhite...). A música entra contínua do início ao fim. Legendas em inglês ancoradas pela borda de baixo.
Uso: python3 montar_edicao.py config.json
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "assets", "FredokaOne-Regular.ttf")


def caption_png(text, path, size=80):
    font = ImageFont.truetype(FONT, size)
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    words, maxw = text.split(), 960
    if probe.textlength(text, font=font) <= maxw:
        lines = [text]
    else:
        best = None
        for k in range(1, len(words)):
            a, b = " ".join(words[:k]), " ".join(words[k:])
            m = max(probe.textlength(a, font=font), probe.textlength(b, font=font))
            if best is None or m < best[0]:
                best = (m, [a, b])
        lines = best[1]
    lh, pad = int(size * 1.18), 36
    img = Image.new("RGBA", (W, lh * len(lines) + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        x, y = (W - d.textlength(ln, font=font)) / 2, pad + i * lh
        d.text((x, y + 7), ln, font=font, fill=(20, 40, 90, 120), stroke_width=14, stroke_fill=(20, 40, 90, 120))
        d.text((x, y), ln, font=font, fill=(255, 255, 255, 255), stroke_width=12, stroke_fill=(32, 92, 190, 255))
    img.save(path)
    return img.height


def main(path):
    cfg = json.load(open(path))
    base = os.path.dirname(os.path.abspath(path))
    rp = lambda p: p if os.path.isabs(p) else os.path.normpath(os.path.join(base, p))
    shots, music = cfg["shots"], rp(cfg["music"])
    total = sum(s["dur"] for s in shots)
    tmp = tempfile.mkdtemp()
    args, fc = [], []
    trd = []  # duração da transição depois de cada tomada
    for i, s in enumerate(shots):
        tr = s.get("tr", "cut")
        trd.append(0.0 if i == len(shots) - 1 else (0.06 if tr == "cut" else s.get("trdur", 0.35)))
    for i, s in enumerate(shots):
        args += ["-i", rp(s["clip"])]
        z, ax, ay = s.get("zoom", 1.0), s.get("ax", 0.5), s.get("ay", 0.5)
        f = f"[{i}:v]fps=24,scale={W}:{H},setsar=1,trim=start={s['start']}:duration={s['dur']},setpts=PTS-STARTPTS"
        if z > 1.0:
            f += (f",crop=w={W}/{z}:h={H}/{z}:x=({W}-{W}/{z})*{ax}:y=({H}-{H}/{z})*{ay},scale={W}:{H}:flags=lanczos")
        if trd[i] > 0:
            f += f",tpad=stop_mode=clone:stop_duration={trd[i]}"
        f += f",scale=w='trunc({W}*(1+0.04*min(t,{s['dur']})/{s['dur']})/2)*2':h=-2:eval=frame,crop={W}:{H}"
        f += ",eq=saturation=1.07:contrast=1.03,format=yuv420p"
        fc.append(f + f"[v{i}]")
    prev, t = "v0", 0.0
    sfx = []
    for k in range(len(shots) - 1):
        t += shots[k]["dur"]
        tr = shots[k].get("tr", "cut")
        name = "fade" if tr == "cut" else tr
        fc.append(f"[{prev}][v{k+1}]xfade=transition={name}:duration={trd[k]}:offset={t:.3f}[x{k}]")
        prev = f"x{k}"
        if tr != "cut":
            ms = int(max(t - 0.06, 0) * 1000)
            if tr == "fadewhite":
                fc.append(f"aevalsrc='(sin(2*PI*2093*t)+0.8*sin(2*PI*2637*t)+0.6*sin(2*PI*3136*t))*exp(-5*t)*0.10':d=0.7:s=48000,adelay={ms}|{ms}[s{k}]")
            else:
                fc.append(f"anoisesrc=d=0.45:c=pink:a=0.5:r=48000,bandpass=f=1700:w=1.6,afade=t=in:d=0.15,afade=t=out:st=0.18:d=0.27,volume=0.16,aformat=channel_layouts=stereo,adelay={ms}|{ms}[s{k}]")
            sfx.append(f"[s{k}]")
    mi = len(shots)
    args += ["-i", music]
    cap_bottom = cfg.get("caption_bottom", 1530)
    caps = cfg.get("captions", [])
    ci = mi + 1
    for j, c in enumerate(caps):
        png = os.path.join(tmp, f"cap{j}.png")
        h = caption_png(c["text"], png, c.get("size", 80))
        d = c["end"] - c["start"]
        args += ["-loop", "1", "-t", f"{d+0.1:.2f}", "-i", png]
        fc.append(f"[{ci+j}:v]format=rgba,fade=t=in:st=0:d=0.12:alpha=1,fade=t=out:st={max(d-0.12,0):.2f}:d=0.12:alpha=1,setpts=PTS+{c['start']}/TB[c{j}]")
        fc.append(f"[{prev}][c{j}]overlay=x=0:y={cap_bottom - h}:eof_action=pass:enable='between(t,{c['start']},{c['end']})'[o{j}]")
        prev = f"o{j}"
    fc.append(f"[{prev}]fade=t=out:st={total-0.6:.2f}:d=0.6[vout]")
    fc.append(f"[{mi}:a]atrim=duration={total},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={total}[mus]")
    fc.append(f"[mus]{''.join(sfx)}amix=inputs={1+len(sfx)}:normalize=0:duration=first,loudnorm=I=-14:TP=-2:LRA=7,afade=t=out:st={total-1.4:.2f}:d=1.4[aout]")
    out = rp(cfg["out"])
    cmd = ["ffmpeg", "-v", "error", "-y"] + args + ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]", "-t", f"{total}",
           "-c:v", "libx264", "-preset", "slow", "-crf", str(cfg.get("crf", 21)), "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
           "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip())


if __name__ == "__main__":
    main(sys.argv[1])
