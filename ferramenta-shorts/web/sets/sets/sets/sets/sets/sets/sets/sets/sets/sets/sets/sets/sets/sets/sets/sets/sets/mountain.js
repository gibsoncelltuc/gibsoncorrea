// SET mountain: rocky war-torn slope (Monte Cassino): grey-brown rock ground, boulders, dead trees, ruins, sandbags, smoke-grey sky.
SETDEF.mountain = (X) => {
  groundPlane(X, 0, 300, 220, toon({ color: '#8c8478' }), DECK, 8); groundPlane(X, 12, 300, 10, toon({ color: '#7a6e5e' }), DECK + 0.03, 6);
  const rf = P.rng(55); makeTufts(X, 0, 240, 160, 900, ['#7f8a5a', '#6e7a4e', '#8c9660'], () => true, 0.3);
  for (let i = 0; i < 70; i++) libInst('nature/rocks', X + (rf() - 0.5) * 120, DECK, -12 - rf() * 50 + (i % 3 === 0 ? 40 : 0), rf() * 6, 0.7 + rf() * 1.6);
  for (let i = 0; i < 18; i++) { const w = add(box(1.6 + rf(), 0.5 + rf() * 0.6, 0.5), toon({ color: '#9a9488' }), X + (rf() - 0.5) * 70, DECK + 0.3, -6 - rf() * 22, world); w.rotation.y = rf() * 3; }
  for (let i = 0; i < 14; i++) { const g = new THREE.Group(); g.position.set(X + (rf() - 0.5) * 160, DECK, -16 - rf() * 40); world.add(g); add(new THREE.CylinderGeometry(0.1, 0.2, 2.6, 6), toon({ color: '#4a3a30' }), 0, 1.3, 0, g); }
  for (let i = 0; i < 6; i++) libInst('war/sandbags', X - 14 + i * 5, DECK, 8 + (i % 2) * 2, 0, 1.4);
  const hill = add(new THREE.SphereGeometry(1, 20, 12), toon({ color: '#8f8576' }), X, DECK - 1, -90, world); hill.scale.set(70, 26, 40);
  libInst('buildings/castle_tower', X + 8, DECK + 20, -86, 0, 1.6); libInst('buildings/church', X - 12, DECK + 18, -88, 0.3, 1.4);
  farHills(X, -170, '#8a8c92', '#9a9ca2', 18, 300);
};
