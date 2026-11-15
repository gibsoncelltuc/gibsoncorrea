# Bíblia de personagens — "A Guerra do Porco" (v3, Blender)
Rig em `blender/lib/char.py` (classe `Char`), porco em `lib/pig.py`, soldados instanciados em `lib/crowd.py`, props em `lib/props.py`. É o mesmo contrato de anatomia do rig 2D cut-out do projeto anterior, agora com **malhas 3D reais, sombras reais e contorno grosso por trás** (look do canal observado em `references/visual-reference-ricks-clips.md`).

**Anatomia (contrato do rig):** root · hips · torso (forma feijão/stadium com tecido pintado) · neck/head (disco branco com sombra lavanda + contorno `#2a2230` grosso atrás) · eyes (`lid` pálpebra pesada | `wide` choque | `arc` riso | `dot` | `x` morto) · pupils (`look`) · brows (+`angry`) · mouth (`line smirk smile grin laugh oh shout frown teeth`) · sweat (gotas) · shoulders → upper arms → forearms → hands (luva branca redonda; membros finos e escuros em "macarrão", como no canal) · thighs → shins → feet · acessórios (chapéus: palha, kepi, boné de tweed, bicorne, quepe; costeletas, bigode, barba, bochechas, óculos, uniforme com dragonas/botões/talabarte).
**Atuação** (`lib/anim.py`, função pura de `t` ancorada em `script/word-timings.json`): idle (respiração/piscada/olhar), walk, march, aim_up/aim_fire (antecipar → mirar → disparar → coice), smug, shock (pop + suor), laugh, stop (palma "pare" + abanar), point.
**Expressões combináveis:** neutral/smug (pálpebra .4–.6), angry (brows + dentes), surprised/afraid (wide + oh + suor), amused (arc + laugh), worried (frown + brows).

| Personagem | Papel | Visual (ficcional, original) |
|---|---|---|
| **Cutlar** | o colono americano que atira | chapéu de palha com fita azul, macacão azul-arroxeado, barba loura-areia, pálpebra pesada |
| **Griffin** | o dono do porco ("zombador") | boné de tweed, costeletas e bigode alaranjados, colete com debrum dourado, bochechas, build 1,18 |
| **Soldados / Capitão** | escalada terrestre | kepi azul, casaco azul com botões dourados e talabarte branco, calça azul-clara (bloco instanciado + capitão em rig completo) |
| **Almirante Baynes** | quem recusa o ataque | bicorne preto com galão dourado e cocar, casaco azul-marinho com dragonas e medalha, costeletas/bigode brancos, calmo (pálpebra .58) |
| **Auxiliar** | reação do almirante | quepe, casaco azul-escuro, bochechas, olhos arregalados + suor, luneta |
| **Porco** (`lib/pig.py`) | o "herói" involuntário | rosa, contorno grosso, focinho com narinas, rabo em espiral; modos comer/trotar/morto (olho X, língua) |
Aparência e roupas são **artísticas**; nenhuma fala é atribuída a pessoas reais (só narração).
