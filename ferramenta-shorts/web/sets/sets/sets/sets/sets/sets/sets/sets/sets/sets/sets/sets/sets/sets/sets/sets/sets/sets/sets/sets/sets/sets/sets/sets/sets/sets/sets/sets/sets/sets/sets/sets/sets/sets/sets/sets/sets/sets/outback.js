// SET outback: red dirt, wheat fields (wind), eucalyptus, fences, rocks, windmill pump, farm, distant red ranges.
SETDEF.outback = (X) => {
  const red = toon({ color: '#b87a52' }), red2 = toon({ color: '#a86a44' });
  groundPlane(X, 0, 300, 220, red, DECK, 8);
  groundPlane(X, -22, 90, 34, toon({ color: '#d8a640' }), DECK + 0.02, 8);                         // wheat field bed
  groundPlane(X, 22, 300, 8, red2, DECK + 0.03, 6);                                                // dirt track
  const rf = P.rng(88);
  makeTufts(X, -22, 90, 34, 5200, ['#e8c14a', '#f0cd5a', '#d9a93a', '#f3d96e'], () => true, 0.9);   // wheat, wind-driven
  makeTufts(X, 10, 240, 60, 1800, ['#b9a25a', '#a8934e', '#c9b36a'], (x, z) => !(z > 18 && z < 26), 0.45);
  for (let i = 0; i < 16; i++) { const sg = i % 2 ? 1 : -1, x = sg * (14 + rf() * 70), z = -50 - rf() * 40 + (rf() > 0.7 ? 80 : 0); const g = new THREE.Group(); g.position.set(X + x, DECK, z); world.add(g); const s = 1 + rf() * 0.8;
    add(new THREE.CylinderGeometry(0.2 * s, 0.32 * s, 3.4 * s, 7), toon({ color: '#9a8a78' }), 0, 1.7 * s, 0, g);
    for (let k = 0; k < 3; k++) add(new THREE.SphereGeometry(1.2 * s, 9, 7), toon({ color: ['#7d9a6a', '#6f8c5e', '#8aa874'][k] }), (k - 1) * 1.0 * s, 3.8 * s + (k % 2) * 0.5, (k % 2) * 0.6, g); }
  for (let i = 0; i < 14; i++) { const o = libInst('nature/rocks', X + (rf() - 0.5) * 200, DECK, -40 - rf() * 40 + (i % 3 ? 70 : 0), rf() * 6, 1.4 + rf() * 1.6); o.userData.c0 = o.userData.c0; }
  for (let i = 0; i < 24; i++) libInst('nature/picket_fence', X - 46 + i * 3.8, DECK, -5.6, 0, 1.6);
  for (const [x, z, n] of [[-30, -60, 'buildings/barn'], [-18, -62, 'buildings/windmill'], [34, -58, 'buildings/house_small']]) libInst(n, X + x, DECK, z, 0.2, 1.5);
  for (let i = 0; i < 10; i++) libInst('nature/bush', X + (rf() - 0.5) * 160, DECK, 28 + rf() * 20, rf() * 6, 1.1);
  farHills(X, -140, '#c8845a', '#d49a6a', 16, 280);
};
