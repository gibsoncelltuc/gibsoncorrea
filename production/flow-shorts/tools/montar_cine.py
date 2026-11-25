#!/usr/bin/env python3
"""Montador "cinema" para os Shorts: várias tomadas por seção, reenquadramento, transições, color grading de filme,
brilho suave (bloom), vinheta, grão, legenda com efeito de pop, whoosh/brilho sonoro, mixagem e fade final.

Uso: python3 montar_cine.py config.json
Extras do JSON em relação ao montar_edicao.py:
  "grade": {"bloom":0.20,"vignette":true,"grain":3,"warm":0.03,"contrast":1.05,"saturation":1.08}
  por tomada: "push": 0.05 (zoom suave ao longo da tomada), "speed": 0.9 (câmera lenta leve), "ax","ay" (âncora do reenquadramento)
Se a tomada pedir mais tempo do que o clipe tem, o último quadro é congelado (sem quebrar a duração total).
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
    lh, pad = int(size * 1.18), 40
    img = Image.new("RGBA", (W, lh * len(lines) + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        x, y = (W - d.textlength(ln, font=font)) / 2, pad + i * lh
        d.text((x, y + 8), ln, font=font, fill=(15, 30, 80, 140), stroke_width=15, stroke_fill=(15, 30, 80, 140))
        d.text((x, y), ln, font=font, fill=(255, 255, 255, 255), stroke_width=12, stroke_fill=(32, 92, 190, 255))
    img.save(path)
    return img.height


def main(path):
    cfg = json.load(open(path))
    base = os.path.dirname(os.path.abspath(path))
    rp = lambda p: p if os.path.isabs(p) else os.path.normpath(os.path.join(base, p))
    shots, music = cfg["shots"], rp(cfg["music"])
    g = {"bloom": 0.10, "vignette": True, "grain": 2, "warm": 0.012, "contrast": 1.03, "saturation": 1.05}
    g.update(cfg.get("grade", {}))
    total = sum(s["dur"] for s in shots)
    tmp = tempfile.mkdtemp()
    args, fc = [], []
    trd = []
    for i, s in enumerate(shots):
        tr = s.get("tr", "cut")
        trd.append(0.0 if i == len(shots) - 1 else (0.05 if tr == "cut" else s.get("trdur", 0.4)))
    for i, s in enumerate(shots):
        args += ["-i", rp(s["clip"])]
        z, ax, ay = s.get("zoom", 1.0), s.get("ax", 0.5), s.get("ay", 0.5)
        sp = s.get("speed", 1.0)
        need = s["dur"] + trd[i]
        f = (f"[{i}:v]fps=24,scale={W}:{H}:flags=lanczos,setsar=1,trim=start={s['start']},setpts=PTS-STARTPTS,"
             f"tpad=stop_mode=clone:stop_duration=2.5,trim=duration={need * sp:.3f},setpts=PTS/{sp}")
        if z > 1.0:
            f += f",crop=w={W}/{z}:h={H}/{z}:x=({W}-{W}/{z})*{ax}:y=({H}-{H}/{z})*{ay},scale={W}:{H}:flags=lanczos"
        push = s.get("push", 0.035)
        f += f",scale=w='trunc({W}*(1+{push}*min(t,{s['dur']})/{s['dur']})/2)*2':h=-2:eval=frame:flags=bicubic,crop={W}:{H},format=yuv420p"
        fc.append(f + f"[v{i}]")
    prev, t = "v0", 0.0
    sfx = []
    for k in range(len(shots) - 1):
        t += shots[k]["dur"]
        tr = shots[k].get("tr", "cut")
        name = "fade" if tr == "cut" else tr
        fc.append(f"[{prev}][v{k+1}]xfade=transition={name}:duration={trd[k]}:offset={t:.3f}[x{k}]")
        prev = f"x{k}"
        ms = int(max(t - 0.06, 0) * 1000)
        if tr == "fadewhite":
            fc.append(f"aevalsrc='(sin(2*PI*2093*t)+0.8*sin(2*PI*2637*t)+0.6*sin(2*PI*3136*t))*exp(-5*t)*0.10':d=0.7:s=48000,adelay={ms}|{ms}[s{k}]")
            sfx.append(f"[s{k}]")
        elif tr != "cut":
            fc.append(f"anoisesrc=d=0.45:c=pink:a=0.5:r=48000,bandpass=f=1700:w=1.6,afade=t=in:d=0.15,afade=t=out:st=0.18:d=0.27,volume=0.16,aformat=channel_layouts=stereo,adelay={ms}|{ms}[s{k}]")
            sfx.append(f"[s{k}]")
        elif shots[k + 1].get("pop"):
            fc.append(f"aevalsrc='sin(2*PI*880*t)*exp(-28*t)*0.12':d=0.25:s=48000,adelay={ms}|{ms}[s{k}]")
            sfx.append(f"[s{k}]")
    # ---- grade de cinema (uma vez, no vídeo inteiro)
    gr = [f"eq=contrast={g['contrast']}:saturation={g['saturation']}",
          f"colorbalance=rs={g['warm']}:gs=0.0:bs=-{g['warm']}:rm={g['warm']/2}:bm=-{g['warm']/2}:rh={g['warm']}:bh=-{g['warm']}",
          "curves=all='0/0 0.25/0.235 0.75/0.77 1/1'"]
    chain = ",".join(gr)
    if g["bloom"] > 0:
        fc.append(f"[{prev}]{chain},split[ga][gb];[gb]curves=all='0/0 0.7/0 1/1',gblur=sigma=28[gbl];[ga][gbl]blend=all_mode=screen:all_opacity={g['bloom']}[gv]")
    else:
        fc.append(f"[{prev}]{chain}[gv]")
    post = []
    if g["vignette"]: post.append("vignette=angle=PI/5:mode=backward")
    if g["grain"]: post.append(f"noise=alls={g['grain']}:allf=t")
    post.append("format=yuv420p")
    fc.append(f"[gv]{','.join(post)}[gf]")
    prev = "gf"
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
        # pop: nasce 16% maior e assenta em 0,16 s; depois fade-out
        fc.append(f"[{ci+j}:v]format=rgba,scale=w='trunc(iw*(1+0.16*max(0,1-t/0.16))/2)*2':h=-2:eval=frame,"
                  f"fade=t=in:st=0:d=0.10:alpha=1,fade=t=out:st={max(d-0.12,0):.2f}:d=0.12:alpha=1,setpts=PTS+{c['start']}/TB[c{j}]")
        fc.append(f"[{prev}][c{j}]overlay=x='(main_w-overlay_w)/2':y='{cap_bottom}-overlay_h':eof_action=pass:enable='between(t,{c['start']},{c['end']})'[o{j}]")
        prev = f"o{j}"
    fc.append(f"[{prev}]fade=t=in:st=0:d=0.25,fade=t=out:st={total-0.7:.2f}:d=0.7[vout]")
    fc.append(f"[{mi}:a]atrim=duration={total},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={total},"
              f"highpass=f=60,acompressor=threshold=-18dB:ratio=2.2:attack=15:release=160:makeup=1.5[mus]")
    mix_in = "".join(sfx)
    fc.append(f"[mus]{mix_in}amix=inputs={1+len(sfx)}:normalize=0:duration=first,loudnorm=I=-14:TP=-2:LRA=7,afade=t=in:st=0:d=0.15,afade=t=out:st={total-1.6:.2f}:d=1.6[aout]")
    out = rp(cfg["out"])
    cmd = ["ffmpeg", "-v", "error", "-y"] + args + ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]", "-t", f"{total}",
           "-c:v", "libx264", "-preset", cfg.get("preset", "slow"), "-crf", str(cfg.get("crf", 18)), "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
           "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip())


if __name__ == "__main__":
    main(sys.argv[1])
