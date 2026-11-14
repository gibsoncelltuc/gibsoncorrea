#!/usr/bin/env python3
"""Registry versionado (V2: biblioteca reutilizável) com hash sha256 dos arquivos de cada item."""
import hashlib, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
h = lambda p: hashlib.sha256(open(f"{ROOT}/{p}", "rb").read()).hexdigest()[:16]
def item(i, ver, desc, file, deps, scene, lic="original do projeto", src="src/"):
    return {"id": i, "version": ver, "description": desc, "file": file, "dependencies": deps, "license": lic, "source": src, "hash": h(file), "compatibility": "remotion>=4, three>=0.17x, r3f", "test_scene": scene}
R = {"registry_version": "1.0", "project": "guerra-do-porco", "items": [
 item("rig.character.v2", "2.0.0", "Rig 2D cut-out: cabeça sombreada, olhos lid/wide/arc/dot/x, sobrancelhas, bocas, suor, feijão com tecido, membros macarrão, mãos de luva, chapéus/acessórios", "src/characters/Rig.tsx", ["three", "src/world/tex.ts"], "CharSheet"),
 item("rig.pig.v1", "1.0.0", "Porco 2D cut-out (comer/trotar/morto, olho X, rabo em espiral)", "src/characters/Pig.tsx", ["src/characters/Rig.tsx"], "CharSheet"),
 item("motion.library.v2", "2.0.0", "idle, walk, march, aimFire, smug, shock, laugh, stopHand, point (funções puras de t)", "src/characters/poses.ts", ["src/lib/anim.ts"], "CharSheet"),
 item("cast.piloto.v1", "1.0.0", "Elenco do piloto: Cutlar, Griffin, Soldado, Baynes, Auxiliar", "src/characters/cast.ts", ["rig.character.v2"], "CharSheet"),
 item("world.island.v1", "1.0.0", "Ilha: horta, cabana, cerca com brecha, pasto, ovelhas, acampamento, praia, mar, montanhas", "src/world/island.tsx", ["src/world/common.tsx", "src/world/props.tsx", "src/world/ships.tsx"], "Porco@S1"),
 item("world.ships.v1", "1.0.0", "Fragata genérica, frota em escalão, mar, convés", "src/world/ships.tsx", ["src/world/tex.ts"], "Porco@S4,S5"),
 item("world.soldiers.v1", "1.0.0", "Bloco de soldados em marcha (InstancedMesh)", "src/world/soldiers.tsx", [], "Porco@S4"),
 item("world.textures.v1", "1.0.0", "Texturas procedurais Canvas (grama, solo, madeira, vela, bandeiras, notas, placa...)", "src/world/tex.ts", [], "Porco@S1-S6"),
 item("camera.rig.v1", "1.0.0", "Câmera por chaves (smootherstep, arco, sway, tremor de tiro, roll)", "src/camera.tsx", ["src/lib/timing.ts"], "Porco"),
 item("captions.v1", "1.0.0", "Legendas 1–2 palavras, Montserrat 800, pop 108→100 %, pontuação mantida", "src/captions/Captions.tsx", ["@fontsource/montserrat"], "Porco", "SIL OFL 1.1 (fonte)"),
 item("audio.build.v1", "1.0.0", "Música/SFX/ambiência sintetizados + eventos ancorados nas palavras", "tools/build_audio.py", ["numpy"], "audio/sfx-events.json"),
 item("audio.mix.v1", "1.0.0", "Mixagem: ganhos por LUFS, sidechain ~13 dB, loudnorm 2 passos −14/−1,5, alimiter", "tools/mix.py", ["ffmpeg"], "audio/mix-report.json"),
]}
json.dump(R, open(f"{ROOT}/registry/registry.json", "w"), indent=1, ensure_ascii=False); print(len(R["items"]), "itens no registry")
