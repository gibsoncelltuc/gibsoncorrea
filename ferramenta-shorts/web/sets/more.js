// More sets: arctic, palace (Zanzibar shore), jungle, medieval, street, hall, stadium.
SETDEF.arctic = (X) => {
  groundPlane(X, 0, 300, 220, MW.snow, DECK, 8); groundPlane(X, -30, 120, 60, toon({ color: '#a9c2f2' }), DECK + 0.02, 8);
  const rf = P.rng(21); for (let i = 0; i < 22; i++) libInst('nature/rocks', X + (rf() - 0.5) * 180, DECK, -10 - rf() * 70, rf() * 6, 1.6 + rf() * 2.2);
  const h = add(new THREE.SphereGeometry(1, 20, 12), toon({ color: '#92aee6' }), X, DECK - 1, -80, world); h.scale.set(60, 14, 30);
  if (typeof SPEC_FLAGS !== 'undefined' && SPEC_FLAGS) { makeFlag('canada', X - 9, DECK + 3.4, -3, 2.2, 1.2, 3.4, 0); makeFlag('denmark', X + 9, DECK + 3.4, -3, 2.2, 1.2, 3.4, 0); }   /* bandeiras so' quando o roteiro pede (elas apareciam em qualquer cena de neve) */ makeTufts(X, 0, 200, 120, 500, ['#e8f0f8', '#d6e4f0'], () => true, 0.2); farHills(X, -150, '#a9bfd8', '#b9cde4', 18, 300);
};
SETDEF.palace = (X) => {
  groundPlane(X, 0, 300, 220, MW.sand, DECK, 8); groundPlane(X, 40, 300, 60, toon({ color: '#d4bd88' }), DECK + 0.02, 8);
  const rf = P.rng(33); for (let i = 0; i < 16; i++) libInst('nature/tree_palm', X + (rf() - 0.5) * 160, DECK, -30 - rf() * 40, rf() * 6, 1.6);
  libInst('buildings/castle_tower', X - 12, DECK, -55, 0, 1.6); libInst('buildings/house_two', X + 6, DECK, -56, 0, 1.3); libInst('buildings/house_two', X + 22, DECK, -58, 0, 1.2);
  libInst('buildings/church', X - 34, DECK, -60, 0.2, 1.2); farHills(X, -150, '#9ab8b0', '#aac8c0', 10, 300);
};
SETDEF.jungle = (X) => {
  groundPlane(X, 0, 300, 220, toon({ color: '#3a6a2e' }), DECK, 8); groundPlane(X, 10, 300, 8, toon({ color: '#6a5a3a' }), DECK + 0.03, 6);
  const rf = P.rng(44);
  for (let i = 0; i < 44; i++) { const g = new THREE.Group(); const x = (rf() - 0.5) * 140, z = -10 - rf() * 80 + (i % 6 === 0 ? 46 : 0); g.position.set(X + x, DECK, z); world.add(g); const s = 1.1 + rf() * 1.0;
    add(new THREE.CylinderGeometry(0.22 * s, 0.34 * s, 5 * s, 7), toon({ color: '#6a4a32' }), 0, 2.5 * s, 0, g);
    for (let k = 0; k < 4; k++) add(new THREE.SphereGeometry((1.5 + (k % 2) * 0.5) * s, 9, 7), toon({ color: ['#2f7a30', '#3f8a3a', '#25702c', '#4a9a40'][k] }), (k - 1.5) * 1.1 * s, 5.4 * s + (k % 2) * 0.7 * s, (k % 3 - 1) * 0.8 * s, g); }
  for (let i = 0; i < 28; i++) libInst('nature/bush', X + (rf() - 0.5) * 120, DECK, -10 - rf() * 40 + (i % 3 === 0 ? 30 : 0), rf() * 6, 1.6 + rf());
  makeTufts(X, 0, 200, 140, 2600, ['#3f8a3a', '#2f7a30', '#52a044'], () => true, 0.6); farHills(X, -150, '#5a8a6a', '#6a9a7a', 16, 300);
};
SETDEF.medieval = (X) => {
  const cobW = MW.cobble.clone(); cobW.color.set('#ffd9bd');   // warm the grey cobbles (the square was the least colourful ground)
  groundPlane(X, 0, 300, 220, cobW, DECK, 10); groundPlane(X, -60, 300, 100, MW.grass, DECK + 0.01, 10); makeFlag('modena', X - 10, DECK + 3.4, -6, 2.2, 1.2, 3.4, 0); makeFlag('bologna', X + 10, DECK + 3.4, -6, 2.2, 1.2, 3.4, 0); libInst('nature/fountain', X + 12, DECK, 2, 0, 0.8);
  for (let i = 0; i < 9; i++) libInst('buildings/house_small', X - 70 + i * 17, DECK, -50 - (i % 2) * 6, 0.1 * i, 1.0);
  libInst('buildings/castle_tower', X - 34, DECK, -80, 0, 1.0); libInst('buildings/castle_tower', X + 40, DECK, -84, 0, 1.0); libInst('buildings/church', X + 4, DECK, -78, 0, 1.0);
  for (let i = 0; i < 16; i++) libInst('nature/tree_oak', X + (i % 2 ? 1 : -1) * (30 + (i * 7) % 40), DECK, -20 - (i * 5) % 30, i, 1.2);
  makeTufts(X, -60, 200, 60, 600, ['#6fae43', '#5fa03a'], () => true, 0.45); farHills(X, -150, '#7d93b8', '#8aa0c4', 14, 300);
};
SETDEF.street = (X) => {
  groundPlane(X, 0, 300, 220, MW.cobble, DECK, 10);
  for (let i = 0; i < 9; i++) { libInst(i % 3 === 0 ? 'buildings/shop' : 'buildings/house_two', X - 60 + i * 14, DECK, -36 - (i % 2) * 4, 0, 1.0); libInst(i % 2 ? 'buildings/apartment' : 'buildings/house_blue', X - 60 + i * 14, DECK, -70, 0, 1.0); }
  for (let i = 0; i < 6; i++) libInst('nature/lamppost', X - 30 + i * 12, DECK, -14, 0, 1.2);
  farHills(X, -150, '#9aa4b8', '#aab4c8', 8, 300);
};
SETDEF.hall = (X) => {
  groundPlane(X, 0, 120, 100, MW.marble, DECK, 8);
  for (const sx of [-1, 1]) for (let i = 0; i < 6; i++) { add(new THREE.CylinderGeometry(0.6, 0.6, 9, 14), MW.stone, X + sx * 12, DECK + 4.5, 8 - i * 9, world); }
  add(box(120, 14, 1), MW.stone, X, DECK + 7, -44, world); add(box(1, 14, 100), MW.stone, X - 24, DECK + 7, 0, world); add(box(1, 14, 100), MW.stone, X + 24, DECK + 7, 0, world);
  for (let i = 0; i < 6; i++) { add(box(8, 0.3, 2.2), MW.wood, X - 16 + (i % 2) * 28 - 6, DECK + 0.6, -6 - Math.floor(i / 2) * 5, world); }
  add(box(6, 0.4, 3), MW.wood, X, DECK + 0.6, -18, world); add(box(6, 6, 0.5), toon({ color: '#7a1c1c' }), X, DECK + 4, -22, world);
};
SETDEF.stadium = (X) => {
  groundPlane(X, 0, 200, 140, MW.grass, DECK, 4); groundPlane(X, 0, 200, 4, MW.white, DECK + 0.03, 4);
  const fans = []; const rf = P.rng(77), cols = ['#d8282f', '#27408b', '#f1ece0', '#e8c45a', '#2f8a4a', '#7b5ac9'];
  for (let r = 0; r < 5; r++) { add(box(160, 1.2, 3.2), toon({ color: '#9a9a9f' }), X, DECK + 0.6 + r * 1.2, -34 - r * 3.2, world);
    for (let i = 0; i < 52; i++) { const m = add(new THREE.SphereGeometry(0.55, 8, 6), toon({ color: cols[(i * 7 + r * 3 + Math.floor(rf() * 3)) % 6] }), X - 62 + i * 2.4 + (r % 2) * 1.2, DECK + 1.9 + r * 1.2, -34 - r * 3.2, world, { cast: false }); m.userData.fan = [r, i]; fans.push(m); } }
  for (const sx of [-1, 1]) { add(new THREE.CylinderGeometry(0.1, 0.1, 3, 8), MW.white, X + sx * 24, DECK + 1.5, 0, world); add(new THREE.CylinderGeometry(0.1, 0.1, 3, 8), MW.white, X + sx * 24, DECK + 3, 3, world).rotation.x = Math.PI / 2; }
  UPD.push((W, f, t) => { fans.forEach((m, k) => { const [r, i] = m.userData.fan; m.position.y = DECK + 1.9 + r * 1.2 + 0.28 * Math.abs(Math.sin(t * 4 + i * 1.7 + r)); }); });
  makeTufts(X, 0, 190, 130, 1800, ['#4f9a3e', '#5aa844'], () => true, 0.2); farHills(X, -150, '#8a96b8', '#9aa6c8', 8, 300);
};
