// SET harbor: wooden pier over open sea (the water plane shows), crates, a ship, lighthouse.
SETDEF.harbor = (X) => {
  groundPlane(X, -80, 600, 340, toon({ color: '#2f86b8' }), DECK - 1.2, 8); for (let i = 0; i < 24; i++) { const w = add(box(5 + (i % 3) * 2, 0.04, 0.12), toon({ color: '#e8f6ff' }), X - 40 + (i * 7) % 90, DECK - 1.15, -6 - (i * 13) % 70, world, { cast: false }); w.userData.wv = i; }
  for (let i = 0; i < 40; i++) add(box(3.2, 0.25, 7), MW.plank, X - 38 + i * 3.25, DECK - 0.05, 4, world);
  add(box(130, 1.4, 22), toon({ color: '#b9b3a6' }), X + 26, DECK - 0.75, -10.4, world); add(box(130, 0.3, 0.6), toon({ color: '#8f897c' }), X + 26, DECK + 0.1, -21.2, world);   /* cais de pedra atras do pier: tropa e multidao nao pisam na agua */
  for (let i = 0; i < 14; i++) add(new THREE.CylinderGeometry(0.3, 0.3, 3.0, 8), MW.trunk, X - 36 + i * 5.6, DECK - 1.6, 7.2, world);
  for (let i = 0; i < 6; i++) libInst('crate', X - 30 + i * 11, DECK, -3 - (i % 2) * 1.5, 0.1 * i, 1.1);
  libInst('ship', X + 4, DECK - 1.2, -26, 0.1, 0.8); libInst('buildings/lighthouse', X - 48, DECK - 0.3, -10, 0, 1.4);
  farHills(X, -150, '#7d93b8', '#8aa0c4', 12, 300);
};
UPD.push((W, f, t) => { world.children.forEach((m) => { if (m.userData && m.userData.wv !== undefined) { m.position.x += Math.sin(t * 0.6 + m.userData.wv) * 0.01; m.scale.x = 1 + 0.25 * Math.sin(t * 1.3 + m.userData.wv * 2); } }); });
