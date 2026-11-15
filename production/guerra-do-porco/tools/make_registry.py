#!/usr/bin/env python3
"""Registry versionado (V2: biblioteca reutilizável) — itens do pipeline Blender com hash sha256 de cada arquivo."""
import hashlib, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
h = lambda p: hashlib.sha256(open(f"{ROOT}/{p}", "rb").read()).hexdigest()[:16]
def item(i, ver, desc, file, deps, scene, lic="original do projeto"):
    return {"id": i, "version": ver, "description": desc, "file": file, "dependencies": deps, "license": lic, "source": file, "hash": h(file), "compatibility": "bpy>=5.3 (Cycles CPU), numpy, Pillow", "test_scene": scene}
L = "blender/lib/"
R = {"registry_version": "2.0", "project": "guerra-do-porco", "items": [
 item("tex.painted.v1", "1.0.0", "texturas pintadas por código: tábuas, grama, solo, toras, telhas, vela, casco, bandeiras EUA/UK, notas, letreiros, tecidos", L + "texlib.py", ["numpy", "Pillow"], "blender/stills.py S1"),
 item("mat.library.v1", "1.0.0", "materiais Cycles: imagem/ruído pintados, AO, neblina atmosférica por distância, cutout emissivo, raios de luz falsos", L + "mats.py", ["tex.painted.v1"], "blender/stills.py S1"),
 item("world.nature.v1", "1.0.0", "terreno (campos em retalhos), grama/flores instanciadas, horta, cerca, cabana, placa, abetos, nuvens, mar, montanhas, colinas", L + "nature.py", ["mat.library.v1"], "S1"),
 item("world.ships.v1", "1.0.0", "fragata genérica loftada com UV de portinholas, velas, vergas, enxárcias, bandeira; frota em escalão", L + "ships.py", ["world.nature.v1"], "S1/S4"),
 item("world.deck.v1", "1.0.0", "convés: tábuas, amurada, canhões, mastro, bandeira, mar e frota ao fundo", L + "deck.py", ["world.ships.v1"], "S5"),
 item("world.farm.v1", "1.0.0", "composição da fazenda + ambientes golden/bright/dusk (céu degradê, sol, neblina)", L + "farm.py", ["world.nature.v1", "lib.render.v1"], "S1-S4,S6"),
 item("rig.character.v3", "3.0.0", "personagem cut-out 3D: cabeça sombreada, olhos lid/wide/arc/dot/x, sobrancelhas, 9 bocas, suor, tecidos, acessórios, poses por frame", L + "char.py", ["mat.library.v1"], "S3"),
 item("rig.pig.v2", "2.0.0", "porco cut-out 3D (comer/trotar/morto, olho X, flip com pulo)", L + "pig.py", ["rig.character.v3"], "S1"),
 item("rig.crowd.v1", "1.0.0", "soldados enxutos em marcha (blocos)", L + "crowd.py", ["rig.character.v3"], "S4"),
 item("props.v1", "1.0.0", "mosquete, notas, luneta, canhão, túmulo, fumaça, clarão em camadas, bandeira com vento, tenda", L + "props.py", ["mat.library.v1"], "S1/S3/S5/S6"),
 item("motion.library.v3", "3.0.0", "idle/walk/march/aim/shock/laugh/stop/point + câmera por chaves + timing das palavras (funções puras de t)", L + "anim.py", [], "check_framing.py"),
 item("shots.piloto.v1", "1.0.0", "coreografia dos 6 planos do piloto, ancorada nos timestamps reais", L + "shots.py", ["motion.library.v3", "rig.character.v3", "world.farm.v1"], "render_shot.py"),
 item("lib.render.v1", "1.0.0", "Cycles CPU, mundo degradê, sol, câmera com DOF", L + "renderlib.py", ["bpy"], "stills.py"),
 item("post.ffmpeg.v1", "1.0.0", "dissolve por alfa, grade split-tone, bloom, vinheta, grão, legendas ASS, áudio", "blender/post.py", ["ffmpeg"], "renders/pilot_540.mp4"),
 item("audio.build.v1", "1.0.0", "música/SFX/ambiência sintetizados ancorados nas palavras", "tools/build_audio.py", ["numpy"], "audio/sfx-events.json"),
 item("audio.mix.v1", "1.0.0", "mixagem: ganhos por LUFS, sidechain ~13 dB, loudnorm 2 passos −14/−1,5", "tools/mix.py", ["ffmpeg"], "audio/mix-report.json"),
]}
json.dump(R, open(f"{ROOT}/registry/registry.json", "w"), indent=1, ensure_ascii=False); print(len(R["items"]), "itens no registry")
