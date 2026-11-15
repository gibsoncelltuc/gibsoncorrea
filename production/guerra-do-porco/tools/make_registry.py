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
 item("rig.character.v4", "4.0.0", "personagem cut-out 3D: contorno de tinta IRREGULAR (espessura variável, fino do lado da luz, em pedaços), membros de tinta finos, feições medidas, 9 bocas, suor, tecidos, chapéus, poses por frame", L + "char.py", ["mat.library.v1"], "S3"),
 item("rig.pig.v3", "3.0.0", "porco cut-out 3D com contorno irregular (comer/trotar/morto, olho X, flip com pulo)", L + "pig.py", ["rig.character.v4"], "S1"),
 item("rig.crowd.v2", "2.0.0", "MULTIDÃO DE PERSONAGENS REAIS: cada pessoa é um Char completo e único (rosto, chapéu, pelos, altura, passo, olhar) + fuzil + porta-bandeira; regra: nunca bonecos genéricos", L + "crowd.py", ["rig.character.v4", "props.v1"], "S4"),
 item("dress.props.v1", "1.0.0", "objetos de cena: barris/caixotes com letras, feno, carrinho, balde, ferramentas, toco, lenha, carroça, celeiro, poço, ovelhas, galinhas, espantalho, varal, cerca de estacas, lampião, fogueira, fuzis, balas, cordas, leme, sino, escada, caminho de terra, detalhes no chão", L + "dress.py", ["tex.painted.v2", "mat.library.v1"], "blender/lookdev_dress.py"),
 item("tex.painted.v2", "2.0.0", "texturas pintadas à mão por código: tábuas com pregos, aduelas, palha, celeiro, corda, ferro, lona, pedra, rocha, anéis de tora, amurada de fragata, vela de lona, decalques com letras estampadas, caminho de terra", L + "paint.py", ["numpy", "Pillow"], "blender/lookdev_dress.py"),
 item("sets.piloto.v1", "1.0.0", "vestimenta de cada plano (posições dos objetos pensadas na câmera) + fumaça da chaminé", L + "sets.py", ["dress.props.v1", "world.farm.v1"], "blender/stills.py"),
 item("props.v1", "1.0.0", "mosquete, notas, luneta, canhão, túmulo, fumaça, clarão em camadas, bandeira com vento, tenda", L + "props.py", ["mat.library.v1"], "S1/S3/S5/S6"),
 item("motion.library.v3", "3.0.0", "idle/walk/march/aim/shock/laugh/stop/point + câmera por chaves + timing das palavras (funções puras de t)", L + "anim.py", [], "check_framing.py"),
 item("shots.piloto.v2", "2.0.0", "coreografia dos 6 planos do piloto, ancorada nos timestamps reais", L + "shots.py", ["motion.library.v3", "rig.character.v4", "world.farm.v1", "sets.piloto.v1"], "render_shot.py"),
 item("lib.render.v1", "1.0.0", "Cycles CPU, mundo degradê, sol, câmera com DOF", L + "renderlib.py", ["bpy"], "stills.py"),
 item("post.ffmpeg.v2", "2.0.0", "rota só-FFmpeg: dissolve por alfa, grade compartilhada, legendas ASS, áudio", "blender/post.py", ["ffmpeg"], "renders/pilot_540.mp4"),
 item("grade.shared.v1", "1.0.0", "grade de cor compartilhada: split-tone, bloom, preto levantado (tinta ameixa), vinheta, grão; calibrada contra as métricas dos prints", L + "grade.py", ["ffmpeg"], "qa/fidelity-report.md"),
 item("montage.remotion.v1", "1.0.0", "montagem em Remotion: composição Montage (planos+dissolves+áudio) e Captions (legendas em PNG com alfa) + grade FFmpeg (grade.py)", "montage/Montage.tsx", ["remotion", "@fontsource/montserrat", "grade.shared.v1"], "tools/montage.sh"),
 item("audio.build.v1", "1.0.0", "música/SFX/ambiência sintetizados ancorados nas palavras", "tools/build_audio.py", ["numpy"], "audio/sfx-events.json"),
 item("audio.mix.v1", "1.0.0", "mixagem: ganhos por LUFS, sidechain ~13 dB, loudnorm 2 passos −14/−1,5", "tools/mix.py", ["ffmpeg"], "audio/mix-report.json"),
]}
json.dump(R, open(f"{ROOT}/registry/registry.json", "w"), indent=1, ensure_ascii=False); print(len(R["items"]), "itens no registry")
