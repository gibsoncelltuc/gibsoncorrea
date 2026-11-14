# Bíblia de personagens (rig reutilizável — `src/characters/Rig.tsx`)
Rig 2D cut-out em plano XY dentro de cena 3D (R3F). Contorno `#2a2230` (offset de 0.04 u), cabeça branca `#fbf6ee` (r=0.555), olhos de ponto + pupila com `look`, sobrancelhas independentes,
boca modular (`closed/open/smile/smirk/oh/laugh/worry`), membros "macarrão" de 2 segmentos (ombro/cotovelo, quadril/joelho), mãos de luva (bola branca), sombra de contato roxa (`#3d2f5c`, 35%).
Parâmetros de `Pose`: x,y,z, face(±1), scale, bob, lean, tilt, armL/armR[ombro,cotovelo], legL/legR[quadril,joelho], look, blink, brows, mouth, open, squash.
`Look`: shirt/pants/shoe, chapéu (palha/chef/boné/lenço), barba, bigode, avental, óculos, build (largura).
| Personagem | Papel | Visual |
|---|---|---|
| Tomé | herói calmo, nunca explica | chapéu de palha, barba cinza, camisa azul `#6f87c6` |
| Zeca | zombador | chapéu de padeiro, bigode, avental, camisa terracota, build 1.25 |
| Ana | metáfora do "você sabe" | lenço vermelho, cabelo marrom, camisa teal |
| Vilarejo (5 variações) | coro | bonés/lenços/óculos, cores variadas |
Ações (`src/characters/poses.ts`): idle (respiração/piscada), walk (ciclo com swing e joelho), throwChair (antecipação → ação → overshoot → settle, instante de soltar = 0.95 s),
laugh, speaking (boca guiada por timestamps reais de palavra), gesture (pose-a-pose com easeOutBack). Cinemática direta `handPos()` liga o objeto à mão no instante do arremesso.
