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
  groundPlane(X, 0, 200, 140, MW.grass, DECK, 4);
  /* CAMPO DE FUTEBOL DE VERDADE (ordem do Gibson 21/11): gramado listrado, linhas brancas oficiais (limite, meio de campo, circulo central, areas, marca do penalti, meia-lua), dois gols. Proporcao 105x68 (aqui 80x52), eixo maior no X. */
  { const PL = 80, PW = 52, PZ = 10, Y1 = DECK + 0.02, Y2 = DECK + 0.045, LW = 0.32, white = MW.white;
    for (let i = 0; i < 10; i++) add(box(PL / 10, 0.02, PW), toon({ color: i % 2 ? '#4aa63a' : '#5cb848' }), X - PL / 2 + PL / 20 + i * PL / 10, Y1, PZ, world);   /* faixas do gramado */
    const L = (cx, cz, w, d) => add(box(w, 0.03, d), white, X + cx, Y2, cz, world);
    L(0, PZ - PW / 2, PL, LW); L(0, PZ + PW / 2, PL, LW); L(-PL / 2, PZ, LW, PW); L(PL / 2, PZ, LW, PW); L(0, PZ, LW, PW);   /* limite + linha do meio */
    const ring = (cx, cz, r0, r1, a0, a1) => { const m = new THREE.Mesh(new THREE.RingGeometry(r0, r1, 56, 1, a0, a1 - a0), white); m.rotation.x = -Math.PI / 2; m.position.set(X + cx, Y2, cz); world.add(m); return m; };
    ring(0, PZ, 7.0 - LW / 2, 7.0 + LW / 2, 0, Math.PI * 2); { const dot = new THREE.Mesh(new THREE.CircleGeometry(0.45, 20), white); dot.rotation.x = -Math.PI / 2; dot.position.set(X, Y2, PZ); world.add(dot); }   /* circulo central */
    for (const sx of [-1, 1]) {
      const gx = sx * PL / 2, ax = gx - sx * 12.7 / 2, bx = gx - sx * 4.2 / 2;
      L(sx * (PL / 2 - 12.7), PZ, LW, 31); L(ax * 0 + sx * (PL / 2 - 12.7 / 2), PZ - 15.5, 12.7, LW); L(sx * (PL / 2 - 12.7 / 2), PZ + 15.5, 12.7, LW);   /* grande area */
      L(sx * (PL / 2 - 4.2), PZ, LW, 14); L(sx * (PL / 2 - 4.2 / 2), PZ - 7, 4.2, LW); L(sx * (PL / 2 - 4.2 / 2), PZ + 7, 4.2, LW);   /* pequena area */
      { const dot = new THREE.Mesh(new THREE.CircleGeometry(0.4, 16), white); dot.rotation.x = -Math.PI / 2; dot.position.set(X + sx * (PL / 2 - 8.5), Y2, PZ); world.add(dot); }   /* marca do penalti */
      ring(sx * (PL / 2 - 8.5), PZ, 7.0 - LW / 2, 7.0 + LW / 2, sx > 0 ? Math.PI * 0.5 + 0.9 : -Math.PI * 0.5 + 0.9, sx > 0 ? Math.PI * 1.5 - 0.9 : Math.PI * 0.5 - 0.9);   /* meia-lua */
      /* GOL: duas traves, travessao e rede */
      for (const dz of [-3.7, 3.7]) add(new THREE.CylinderGeometry(0.1, 0.1, 2.6, 10), white, X + gx, DECK + 1.3, PZ + dz, world);
      add(box(0.2, 0.2, 7.5), white, X + gx, DECK + 2.6, PZ, world);
      add(box(2.2, 0.03, 7.5), toon({ color: '#e8e8e8' }), X + gx + sx * 1.1, DECK + 0.05, PZ, world);
      for (let k = 0; k < 8; k++) add(box(0.04, 2.5, 0.04), toon({ color: '#e8e8e8' }), X + gx + sx * 2.2, DECK + 1.25, PZ - 3.5 + k, world);
    }
  }
  const NR = 8, Z0 = -18, DZ = 2.7, DY = 1.8;   /* ARQUIBANCADA LOTADA (ordem do Gibson 19/11): 9 degraus altos e perto do campo */
  for (let r = 0; r < NR; r++) add(box(170, DY, DZ + 0.05), toon({ color: r % 2 ? '#8e8e96' : '#9a9aa2' }), X, DECK + DY / 2 + r * DY, Z0 - r * DZ, world);
  add(box(170, 3.5, 1), toon({ color: '#c8c8d0' }), X, DECK + 0.6, Z0 + DZ / 2 + 0.6, world);   /* mureta na beira do campo */
  add(box(170, 2.2, 0.6), toon({ color: '#27408b' }), X, DECK + NR * DY + 1.6, Z0 - NR * DZ, world);   /* faixa do alto */
  for (const sx of [-1, 1]) { add(new THREE.CylinderGeometry(0.1, 0.1, 3, 8), MW.white, X + sx * 24, DECK + 1.5, 0, world); add(new THREE.CylinderGeometry(0.1, 0.1, 3, 8), MW.white, X + sx * 24, DECK + 3, 3, world).rotation.x = Math.PI / 2; }
  /* TORCIDA: atlas com 10 torcedores x 2 quadros (bracos para cima / acenando, gritando, rindo) desenhados com o MESMO tracado dos personagens; centenas de copias na GPU pulando fora de fase */
  const NV = 10, CWp = 300, CHp = 500, cv = document.createElement('canvas'); cv.width = NV * CWp; cv.height = 2 * CHp; const g = cv.getContext('2d');
  const camis = ['#d8282f', '#27408b', '#f1ece0', '#e8c45a', '#2f8a4a', '#7b5ac9', '#e07a2a', '#1f2f5c', '#c25a7a', '#3aa0c8'], cab = ['#2b2018', '#5a3a24', '#e8c45a', '#1b1b1f', '#8a4f1c'];
  for (let v = 0; v < NV; v++) for (let q = 0; q < 2; q++) {
    const o = { jacket: camis[v], pants: ['#3b3f52', '#2a2a30', '#4a5a7a'][v % 3], boots: '#2a2a30', skin: T.SKINS[v % T.SKINS.length], hat: v % 4 === 3 ? 'cap' : 'hair', hair: cab[v % 5], hatColor: camis[(v + 3) % NV] };
    g.setTransform(CWp / 600, 0, 0, CHp / 1000, v * CWp, q * CHp);
    try { T.bodyFront(new T.Pen(g), o, { blink: false, mode: 'stand', phase: 0, expr: q ? (v % 2 ? 'shout' : 'laugh') : (v % 2 ? 'laugh' : 'grin'), gest: q ? 'wave2' : 'up', gk: 1, gt: v * 0.3, tilt: (v % 3 - 1) * 5 }); } catch (e) { console.warn('torcida', e); }
  }
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  const FH = 2.5, geo = new THREE.PlaneGeometry(FH * 0.6, FH); geo.translate(0, FH / 2, 0);
  const pos = [], cell = [], ph = []; const rf = P.rng(77);
  for (let r = 0; r < NR; r++) for (let x = -84; x <= 84; x += 0.95) { pos.push(X + x + (rf() - 0.5) * 0.3, DECK + (r + 1) * DY - 0.15, Z0 - r * DZ + 0.2 + (rf() - 0.5) * 0.3); cell.push(Math.floor(rf() * NV)); ph.push(rf() * 6.283); }
  const N = cell.length, ig = new THREE.InstancedBufferGeometry(); ig.index = geo.index; ig.setAttribute('position', geo.attributes.position); ig.setAttribute('uv', geo.attributes.uv);
  ig.setAttribute('ofs', new THREE.InstancedBufferAttribute(new Float32Array(pos), 3)); ig.setAttribute('cell', new THREE.InstancedBufferAttribute(new Float32Array(cell), 1)); ig.setAttribute('ph', new THREE.InstancedBufferAttribute(new Float32Array(ph), 1)); ig.instanceCount = N;
  const uT = { value: 0 }, VS = `attribute vec3 ofs; attribute float cell, ph; uniform float tt; varying vec2 vUv; varying float vD;
    void main(){ float k = step(.5, fract(tt * .9 + ph / 6.283)); vUv = vec2((cell + uv.x) / ${NV}.0, (uv.y + (1. - k)) / 2.);
      vec3 p = position; float sw = sin(tt * 5. + ph) * .09; p.x += sw * p.y * .25;
      vec4 mv = modelViewMatrix * vec4(ofs + vec3(0., abs(sin(tt * 7. + ph)) * .32, 0.), 1.); mv.xy += p.xy; vD = -mv.z; gl_Position = projectionMatrix * mv; }`;
  const mat = new THREE.ShaderMaterial({ uniforms: { map: { value: tex }, tt: uT }, vertexShader: VS, side: THREE.DoubleSide,
    fragmentShader: `uniform sampler2D map; varying vec2 vUv; varying float vD; void main(){ vec4 c = texture2D(map, vUv); if (c.a < .5) discard; gl_FragColor = vec4(c.rgb * .96, 1.); }` });
  mat.toneMapped = false;
  const nd = new THREE.ShaderMaterial({ uniforms: { map: { value: tex }, tt: uT }, vertexShader: VS, side: THREE.DoubleSide,
    fragmentShader: `uniform sampler2D map; varying vec2 vUv; varying float vD; void main(){ if (texture2D(map, vUv).a < .5) discard; gl_FragColor = vec4(0., 0., 0., vD); }` });
  const crowd = new THREE.Mesh(ig, mat); crowd.frustumCulled = false; crowd.userData.nd = nd; crowd.castShadow = false; world.add(crowd);
  UPD.push((W, f, t) => { uT.value = t; });
  makeTufts(X, 0, 190, 130, 1800, ['#4f9a3e', '#5aa844'], () => true, 0.2); farHills(X, -150, '#8a96b8', '#9aa6c8', 8, 300);
};
