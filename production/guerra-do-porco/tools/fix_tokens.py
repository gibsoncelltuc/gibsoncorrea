#!/usr/bin/env python3
"""Reaplica a pontuação do roteiro aos tokens de word-timings.json (o TTS devolve a palavra sem pontuação final)."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(f"{ROOT}/script/word-timings.json")); story = json.load(open(f"{ROOT}/script/story.json"))
norm = lambda s: re.sub(r"[^\w]", "", s.lower())
fixed = 0
for ln in story["lines"]:
    toks = ln["text"].split(); ws = [w for w in D["words"] if w["line"] == ln["id"]]
    if len(toks) != len(ws): print("aviso: tokens != palavras em", ln["id"], len(toks), len(ws)); continue
    for t, w in zip(toks, ws):
        if norm(t) == norm(w["text"]) and t != w["text"]: w["text"] = t; fixed += 1
json.dump(D, open(f"{ROOT}/script/word-timings.json", "w"), ensure_ascii=False, indent=1); print("tokens ajustados:", fixed)
