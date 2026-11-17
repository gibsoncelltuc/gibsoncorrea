#!/usr/bin/env python3
"""Cria o pedido JSON do ACE-Step para um episódio. Uso: musica_pedido.py <num_ep> <seed> <saida.json>"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerar_pacote as g

num, seed, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
ep = next(e for e in g.EPISODES if e["num"] == num)
sh = ep["shots"]
tag = {0: "Chorus", 1: "Verse 1", 2: "Verse 2", 3: "Chorus", 4: "Bridge", 5: "Final Chorus"}
lyrics = "\n\n".join(f"[{tag[i]}]\n{s['l1']}\n{s['l2']}" for i, s in enumerate(sh))
req = {
    "lm_model": "acestep-5Hz-lm-1.7B-Q8_0.gguf",
    "synth_model": "acestep-v15-turbo-Q8_0.gguf",
    "caption": ("Cheerful Brazilian children's pop song, bouncy ukulele strumming, shaker, hand claps on beats 2 and 4, "
                "bright glockenspiel melody, soft round bass, extremely catchy singalong earworm hook with a simple repeated chorus, "
                "warm friendly adult male lead vocal with a kids choir doubling the chorus, playful and happy, clean polished mix, "
                "no long intro, each section lasts exactly 4 bars, the vocal starts right on the first beat of every section, "
                "clear Portuguese pronunciation of every word, no instrumental break"),
    "lyrics": lyrics, "duration": 60, "bpm": 96, "vocal_language": "pt", "keyscale": "C major",
    "timesignature": "4", "inference_steps": 8, "guidance_scale": 1.0, "shift": 3.0, "seed": seed,
}
json.dump(req, open(out, "w"), ensure_ascii=False, indent=2)
print(lyrics)
