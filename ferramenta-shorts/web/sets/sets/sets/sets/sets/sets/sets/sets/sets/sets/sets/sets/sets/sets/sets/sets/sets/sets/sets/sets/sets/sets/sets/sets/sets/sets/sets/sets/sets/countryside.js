// SET countryside: meadows, dirt road, hedgerows, forest backdrop, a hill, a river with a pontoon bridge, a village, haystacks. Flat ground at DECK.
SETDEF.countryside = (X) => {
  const G = (cx, cz, w, d, mat, y = DECK, rep = 8) => groundPlane(X + cx, cz, w, d, mat, y, rep);
  G(0, 20, 220, 60, MW.grass); G(0, -22, 220, 56, MW.grass); G(0, -76, 220, 52, MW.grass);            // south bank | middle | north bank (river gap between z -50..-62 -> see water below)
  G(0, 14, 220, 6.5, MW.dirt, DECK + 0.03, 6);                                                         // road
  for (const s of [-1, 1]) add(box(220, 1.6, 1.2), toon({ color: '#6b5a3a' }), X, DECK - 0.8, -50.6 - (s > 0 ? 12.2 : 0), world, { cast: false });   // river banks
  // pontoon bridge across the river (along z) at x = +10
  for (let i = 0; i < 12; i++) add(box(4.6, 0.25, 1.05), MW.plank, X + 10, DECK + 0.05, -50.2 - i * 1.0, world); for (let i = 0; i < 6; i++) add(new THREE.CylinderGeometry(0.7, 0.7, 5, 10), toon({ color: '#6a6e5a' }), X + 10, DECK - 0.35, -51 - i * 2.2, world).rotation.z = Math.PI / 2;
  // hill with trees for the spy
  const hill = add(new THREE.SphereGeometry(1, 20, 12), MW.grass, X - 22, DECK - 0.2, -30, world); hill.scale.set(9, 3.4, 8);
  // hedgerows + oaks + pines
  for (let i = 0; i < 34; i++) { const x = -52 + i * 3.1; add(new THREE.SphereGeometry(1.1 + (i % 3) * 0.2, 9, 7), toon({ color: ['#4a8a38', '#3f7a32', '#5a9a40'][i % 3] }), X + x, DECK + 0.6, -36, world).scale.y = 0.8; }
  const rf = P.rng(66); for (let i = 0; i < 26; i++) { const x = -70 + rf() * 140, z = -80 - rf() * 40; pineAt(X + x, DECK, z, 1.1 + rf() * 0.9); }
  for (let i = 0; i < 14; i++) { const sgn = i % 2 ? 1 : -1, x = sgn * (50 + rf() * 40), z = 20 + rf() * 40; const o = libInst('nature/tree_oak', X + x, DECK, z, rf() * 6, 1.1 + rf() * 0.5); o.userData.sw = rf() * 6; trees.push(o); }
  for (const [x, z, n] of [[22, -44, 'buildings/house_small'], [30, -46, 'buildings/house_two'], [40, -45, 'buildings/church'], [-50, -90, 'buildings/barn'], [-42, -92, 'buildings/windmill']]) libInst(n, X + x, DECK, z, 0.2, 1.4);
  for (let i = 0; i < 5; i++) libInst('nature/haybale', X + 30 + i * 2.6, DECK, 4 + (i % 2) * 3, rf() * 6, 1.2);
  makeTufts(X, -10, 180, 100, 2600, ['#6fae43', '#5fa03a', '#86c456', '#7ab648'], (x, z) => !(z > 10.5 && z < 17.5) && !(z < -49 && z > -63), 0.5);
  farHills(X, -150, '#7d93b8', '#8aa0c4', 14, 260);
  // inflation yard: compressor + hose, tire tracks layer
  const yard = new THREE.Group(); world.add(yard); const comp = new THREE.Group(); comp.position.set(X + 3.4, DECK, 3.4); yard.add(comp); add(box(1.3, 0.9, 0.9), toon({ color: '#d9822b' }), 0, 0.7, 0, comp); add(new THREE.CylinderGeometry(0.28, 0.28, 0.16, 12), MW.dark, 0.6, 0.3, 0.5, comp).rotation.z = Math.PI / 2; add(new THREE.CylinderGeometry(0.28, 0.28, 0.16, 12), MW.dark, -0.6, 0.3, 0.5, comp).rotation.z = Math.PI / 2; add(box(0.9, 0.18, 0.5), MW.dark, 0, 1.25, 0, comp);
  const hose = (x0, z0, x1, z1) => { const a = new THREE.Vector3(x0, 0.2, z0), b = new THREE.Vector3(x1, 1.0, z1), d = b.clone().sub(a), len = d.length(); const m = add(new THREE.CylinderGeometry(0.07, 0.07, len, 6), toon({ color: '#2b2b30' }), 0, 0, 0, world, { cast: false }); m.position.copy(a.clone().add(b).multiplyScalar(0.5)); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize()); m.position.y += DECK; yard.add(m); return m; };
  hose(X + 3.4, 3.4, X + 0.8, 1.0);
  const trk = []; for (const dx of [-0.95, 0.95]) { const m = add(box(0.5, 0.03, 1), toon({ color: '#4a3b2a' }), X + dx, DECK + 0.05, 8, world, { cast: false }); trk.push(m); }
  SETDEF._cs = { X, trk, yard };
  UPD.push((W, f, t) => { const k = SETDEF._cs; k.yard.visible = !!W.yard; const tr = W.tracks || 0; k.trk.forEach((m) => { m.scale.z = Math.max(0.001, tr * 14); m.position.z = 8 - 0 - tr * 7 + 7; m.visible = tr > 0.01; }); });
};
