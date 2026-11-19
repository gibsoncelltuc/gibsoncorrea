// Set dressing: scatters small foreground/mid-ground props (barrels, crates, lanterns, signs, hay, rocks, bushes) so every take has layered depth.
const DRESS = {
  countryside: ['nature/haybale', 'crate', 'barrel', 'tools/bucket', 'nature/bush', 'tools/lantern', 'nature/rocks'],
  outback: ['nature/rocks', 'crate', 'barrel', 'nature/bush', 'tools/shovel', 'nature/haybale', 'tools/bucket'],
  arctic: ['nature/rocks', 'crate', 'barrel', 'tools/lantern', 'nature/rocks'],
  palace: ['crate', 'barrel', 'tools/lantern', 'nature/bush', 'war/drum'],
  jungle: ['nature/bush', 'nature/rocks', 'crate', 'barrel', 'tools/lantern', 'tools/axe'],
  medieval: ['barrel', 'crate', 'tools/lantern', 'war/shield', 'war/sandbags', 'tools/anvil', 'nature/haybale'],
  street: ['barrel', 'crate', 'tools/lantern', 'nature/bench', 'nature/bush', 'tools/ladder'],
  hall: ['barrel', 'crate', 'tools/lantern', 'war/drum', 'mk/Bench'],
  stadium: ['nature/bench'],
  harbor: ['crate', 'barrel', 'tools/lantern', 'war/cannonballs', 'tools/bucket'],
  mountain: ['nature/rocks', 'war/sandbags', 'crate', 'barrel', 'tools/shovel', 'tools/lantern'],
};
const SWAY = []; let _swayInit = false;
function dressSet(name, X) {
  if (!_swayInit) { _swayInit = true; UPD.push((W, f, t) => { SWAY.forEach((o) => { const wd = windAt(o.position.x, o.position.z, t); o.rotation.z = Math.sin(t * (1.6 + 1.4 * wd) + o.userData.sw) * o.userData.swA * (0.5 + WX.wind * 1.4 + wd); o.rotation.x = Math.sin(t * 1.3 + o.userData.sw * 2) * o.userData.swA * 0.5; }); }); }
  const list = DRESS[name]; if (!list) return;
  if (!['hall', 'stadium', 'harbor', 'arctic'].includes(name)) { const N = 110, g = new THREE.IcosahedronGeometry(1, 0), im = new THREE.InstancedMesh(g, toon({ color: '#ffffff' }), N), rq = P.rng(5 + name.length), mx = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler(), v = new THREE.Vector3(), sc = new THREE.Vector3();
    const cols = ['#8a8178', '#a39a8c', '#6f675e', '#b3a898', '#7d7468'];
    for (let i = 0; i < N; i++) { const s = 0.04 + rq() * 0.13; v.set(X + (rq() - 0.5) * 34, DECK + s * 0.3, -14 + rq() * 28); e.set(rq() * 6, rq() * 6, rq() * 6); q.setFromEuler(e); sc.set(s * (1 + rq()), s, s * (1 + rq())); mx.compose(v, q, sc); im.setMatrixAt(i, mx); im.setColorAt(i, new THREE.Color(cols[i % 5])); }
    im.castShadow = false; im.receiveShadow = true; world.add(im); } const rf = P.rng(900 + name.length * 13);
  const put = (n, x, z, s) => { if (!LIBA[n]) return; const o = libInst(n, X + x, DECK, z, rf() * 6.28, s); if (/bush|tree|lantern|haybale|scarecrow|flowerbed/.test(n)) { o.userData.sw = rf() * 6; o.userData.swA = n.includes('lantern') ? 0.09 : 0.035; SWAY.push(o); } return o; };
  const fg = list.filter((n) => !/bucket|haybale|bush|tree|palm|ladder|bench|flowerbed|sandbags/.test(n)); const fgl = fg.length ? fg : list;
  for (const k of [-1, 0, 1]) for (let i = 0; i < 5; i++) { const n = fgl[Math.floor(rf() * fgl.length)]; const side = rf() < 0.5 ? -1 : 1; const x = k * 8 + side * (2.6 + rf() * 2.8); put(n, x, 5.2 + rf() * 3.0, 0.42 + rf() * 0.3); }
  for (const k of [-1, 0, 1]) for (let i = 0; i < 4; i++) { const n = list[Math.floor(rf() * list.length)]; const side = rf() < 0.5 ? -1 : 1; const x = k * 8 + side * (3.2 + rf() * 5); put(n, x, -2.5 - rf() * 5, 0.9 + rf() * 0.6); }
}
