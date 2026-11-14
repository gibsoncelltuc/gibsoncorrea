# Bíblia de personagens — "A Guerra do Porco" (rig v2, estilo Ricks Clips observado)
Rig em `src/characters/Rig.tsx` (versão 2: evolui o rig do projeto *Tomé e o Lago* com o que foi observado nas referências do canal; ver `references/visual-reference-ricks-clips.md`).

**Anatomia (contrato do rig):** root · hips · torso (feijão/stadium com tecido padronizado) · neck/head (disco branco com crescente lavanda de sombra + contorno `#2a2230` grosso) · eyes (`lid` pálpebra pesada | `wide` choque | `arc` riso | `dot` | `x` morto) · pupils (`look`) · brows (`brows` + `angry`) · mouth (`line smirk smile grin laugh oh shout frown teeth`) · sweat (gotas animadas) · shoulders → upper arms → forearms → hands (luva branca redonda) · thighs → shins → feet · accessories (chapéus: palha, kepi, boné, bicorne, quepe; costeletas, bigode, barba, óculos, bochechas, uniforme com dragonas/botões/talabarte).
**Estados de atuação** (`src/characters/poses.ts`): idle (respiração/piscada/olhar), walk (pés sincronizados à velocidade), march, aimFire (antecipar → mirar → disparar → coice), smug, shock (pop + suor), laugh, stopHand (palma "pare" + abanar), point.
**Expressões combináveis:** neutral/smug (lid .4–.6), angry (angry + teeth), surprised/afraid (wide + oh + sweat), amused (arc + laugh), worried (frown + brows).

| Personagem | Papel | Visual (ficcional, original) |
|---|---|---|
| **Cutlar** | o colono americano que atira | chapéu de palha com fita azul, macacão jeans, barba ruiva, lid pesado |
| **Griffin** | o dono do porco (o "zombador") | boné de tweed, costeletas e bigode ruivos, colete oliva/ouro, bochechas, build 1.18 |
| **Soldados / Capitão** | escalada terrestre | kepi azul, casaco azul com botões dourados e talabarte branco, calça azul-clara (bloco instanciado + capitão em rig completo) |
| **Almirante Baynes** | quem recusa o ataque | bicorne preto com galão dourado, casaco azul-marinho com dragonas e medalha, costeletas/bigode brancos, calmo (lid .58) |
| **Auxiliar** | reação do almirante | quepe, casaco azul-escuro, bochechas, olhos arregalados + suor, luneta |
| **Porco** (`src/characters/Pig.tsx`) | o "herói" involuntário | rosa, contorno grosso, nariz com narinas, rabo em espiral; modos comer/trotar/morto (olho X, língua) |
Aparência e roupas são **artísticas**; nenhuma fala é atribuída a pessoas reais (só narração).
