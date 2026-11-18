#!/usr/bin/env python3
"""Cria as legendas em inglês de um episódio, no tempo em que cada verso é cantado.
Uso: legendas_auto.py <num_ep> <musica.mp3> <config.json>   (grava "captions" dentro do config)
Precisa de faster-whisper e librosa. Alinha a letra escrita com as palavras ouvidas (Whisper) e usa os tempos.
"""
import sys, os, re, json, difflib, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerar_pacote as g
import librosa
from faster_whisper import WhisperModel

EN = {
    4: [("Wash, wash, wash your little hands,", "scrub, scrub, little bubbles!"),
        ("Played in the dirt, touched the floor,", "dirty little hands, no, no, no!"),
        ("Palm to palm, the backs too,", "between the fingers, don't miss any!"),
        ("Wash, wash, wash your little hands,", "scrub, scrub, little bubbles!"),
        ("Rinse them well, dry them too,", "clean little hands are good for you!"),
        ("Wash, wash, wash your little hands,", "scrub, scrub, little bubbles!")],
}
FINAL = {4: "Wash your hands before you eat!"}


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-z]+", s)


def main(num, mp3, cfg_path):
    ep = next(e for e in g.EPISODES if e["num"] == num)
    lines_pt, lines_en = [], []
    for i, s in enumerate(ep["shots"]):
        lines_pt += [s["l1"], s["l2"]]
        lines_en += list(EN[num][i])
    y, _ = librosa.load(mp3, sr=16000)
    m = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(y, language="pt", word_timestamps=True, condition_on_previous_text=False)
    heard = [(norm(w.word), w.start, w.end) for s in segs for w in s.words]
    heard = [(t[0], a, b) for t, a, b in heard if t]
    want = []  # (palavra, índice_da_linha)
    for li, ln in enumerate(lines_pt):
        for w in norm(ln):
            want.append((w, li))
    sm = difflib.SequenceMatcher(None, [w for w, _ in want], [h[0] for h in heard], autojunk=False)
    times = {}
    for tag, a0, a1, b0, b1 in sm.get_opcodes():
        if tag == "equal":
            for k in range(a1 - a0):
                li = want[a0 + k][1]
                times.setdefault(li, []).append((heard[b0 + k][1], heard[b0 + k][2]))
    caps, last_end = [], 0.0
    for li, en in enumerate(lines_en):
        blk = li // 2
        if li in times and len(times[li]) >= 2:
            st = min(a for a, _ in times[li]); en_t = max(b for _, b in times[li])
        else:  # sem alinhamento: usa o bloco de 10 s
            st = blk * 10 + (0.3 if li % 2 == 0 else 5.2); en_t = st + 4.3
        st = max(st - 0.05, last_end + 0.03)
        en_t = max(en_t + 0.25, st + 1.0)
        caps.append({"text": en, "start": round(st, 2), "end": round(en_t, 2)})
        last_end = en_t
    # evita que uma legenda invada a seguinte
    for i in range(len(caps) - 1):
        if caps[i]["end"] > caps[i + 1]["start"] - 0.03:
            caps[i]["end"] = round(caps[i + 1]["start"] - 0.03, 2)
    if num in FINAL:
        caps.append({"text": FINAL[num], "start": 56.0, "end": 59.2, "size": 72})
    cfg = json.load(open(cfg_path))
    cfg["captions"] = caps
    json.dump(cfg, open(cfg_path, "w"), ensure_ascii=False, indent=1)
    miss = [li for li in range(len(lines_pt)) if li not in times or len(times[li]) < 2]
    print(f"{len(caps)} legendas; versos sem alinhamento (usaram horário do bloco): {miss}")
    for c in caps: print(f"  {c['start']:5.2f}-{c['end']:5.2f}  {c['text']}")


if __name__ == "__main__":
    main(int(sys.argv[1]), sys.argv[2], sys.argv[3])
