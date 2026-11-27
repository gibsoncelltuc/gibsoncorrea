// ---------- scenery pack: wind grass, bushes, butterflies, foam, far mountains, rim light, sun glow, light shafts ----------
const rimLight = new THREE.DirectionalLight('#8fb4ff', 0); rimLight.castShadow = false; scene.add(rimLight); scene.add(rimLight.target);
const ND_SKIP = (m) => { m.userData.ndSkip = true; return m; };
// wind grass (instanced cones)
const tufts = []; let tuftMesh;
{
  const N = 3600, geo = new THREE.ConeGeometry(0.045, 0.55, 4); geo.translate(0, 0.27, 0);
  tuftMesh = new THREE.InstancedMesh(geo, toon({ color: '#ffffff' }), N); tuftMesh.castShadow = false; tuftMesh.receiveShadow = true; world.add(tuftMesh);
  const rg = P.rng(31), cols = ['#5fae43', '#6fbd4c', '#4f9a3a', '#86c456', '#7ab648'];
  for (let i = 0; i < N; i++) {
    let x, z, y, tries = 0;
    do {
      if (i < 2300) { x = -48 + rg() * 96; z = -30 + rg() * 52; y = hA2(x, z); if (islandMask(x, z) < 0.7) { tries++; continue; } if (Math.abs(x) < 6.6 && z > -6.2 && z < 2.4) { tries++; continue; } if (Math.hypot(x + 11, z + 8) < 4) { tries++; continue; } }
      else { x = BX - 46 + rg() * 92; z = -2 + rg() * 52; const lx = x - BX; y = DECK + 0.3 * Math.sin(lx * 0.2) + 0.2 * Math.sin(z * 0.3 + lx * 0.1) + (lx < -10 ? Math.min(4.2, (-10 - lx) * 0.25 * (1 + Math.sin(z * 0.1) * 0.2)) : 0); }
      break;
    } while (tries < 20);
    const s = 0.7 + rg() * 1.0; tufts.push({ x, y, z, s, ph: rg() * 6.28, ry: rg() * 6.28 }); tuftMesh.setColorAt(i, new THREE.Color(cols[i % cols.length]));
  }
  tuftMesh.instanceColor.needsUpdate = true;
}
const _m = new THREE.Matrix4(), _q = new THREE.Quaternion(), _e = new THREE.Euler(), _p = new THREE.Vector3(), _s = new THREE.Vector3();
// bushes (clusters of spheres) and boulders
const rb = P.rng(77);
for (let i = 0; i < 46; i++) { const x = -52 + rb() * 104, z = -34 + rb() * 54; if (islandMask(x, z) < 0.75 || (Math.abs(x) < 14 && z > -8 && z < 14) || Math.hypot(x + 11, z + 8) < 6) continue;
  const g = new THREE.Group(); g.position.set(x, hA2(x, z), z); world.add(g); for (let k = 0; k < 4; k++) add(new THREE.SphereGeometry(0.5 + rb() * 0.4, 9, 7), toon({ color: ['#4f9a3a', '#3f8a33', '#5fae43'][k % 3] }), (rb() - 0.5) * 1.1, 0.35, (rb() - 0.5) * 1.1, g).scale.y = 0.8; for (let k = 0; k < 5; k++) add(new THREE.SphereGeometry(0.07, 6, 5), toon({ color: ['#ff6b8a', '#ffd84a', '#ffffff'][k % 3] }), (rb() - 0.5) * 1.3, 0.55 + rb() * 0.4, (rb() - 0.5) * 1.3, g, { cast: false }); }
// butterflies over the garden
const butter = []; for (let i = 0; i < 8; i++) { const g = new THREE.Group(); const col = ['#ffd84a', '#ff8ab0', '#8fd0ff', '#ffffff'][i % 4]; for (const s of [-1, 1]) { const w = add(new THREE.CircleGeometry(0.11, 8), new THREE.MeshToonMaterial({ gradientMap: grad, color: col, side: THREE.DoubleSide }), 0, 0, 0, g, { cast: false }); w.geometry.translate(s * 0.1, 0, 0); w.userData.s = s; }
  g.userData = { k: i * 0.8 }; world.add(g); butter.push(g); }
// shoreline foam: ellipse ring around island A + strip along bay B
const foamMat = new THREE.ShaderMaterial({ transparent: true, depthWrite: false, uniforms: { t: { value: 0 } },
  vertexShader: 'varying vec2 vUv; varying vec3 vW; void main(){ vUv = uv; vW = (modelMatrix*vec4(position,1.)).xyz; gl_Position = projectionMatrix*viewMatrix*modelMatrix*vec4(position,1.); }',
  fragmentShader: 'uniform float t; varying vec2 vUv; varying vec3 vW; void main(){ float band = smoothstep(.0,.35,vUv.y)*(1.-smoothstep(.55,1.,vUv.y)); float w = .5+.5*sin(vW.x*1.7+vW.z*1.3 - t*2.2 + sin(vW.z*.6)*2.); float lace = step(.35, fract(sin(dot(floor(vW.xz*3.), vec2(12.9,78.2)))*43758.5)) ; gl_FragColor = vec4(1.,1.,1., band*(.35+.5*w)*(.6+.4*lace)); }' });
const foamA = new THREE.Mesh(new THREE.RingGeometry(0.93, 1.0, 96, 2), foamMat); foamA.rotation.x = -Math.PI / 2; foamA.scale.set(74.5, 54.5, 1); foamA.position.set(0, DECK - 1.28, -6); ND_SKIP(foamA); foamA.renderOrder = 2; world.add(foamA);
const foamB = new THREE.Mesh(new THREE.PlaneGeometry(150, 3.2, 2, 2), foamMat); foamB.rotation.x = -Math.PI / 2; foamB.position.set(BX, DECK - 1.28, -6.2); ND_SKIP(foamB); foamB.renderOrder = 2; world.add(foamB);
// far hills/islets on the horizon (hazy blue, rolling not pyramids)
for (let i = 0; i < 18; i++) { const a = -2.8 + i * 0.31, d = 540 + (i % 3) * 70, r = 90 + (i * 29) % 80, hh = 14 + (i * 13) % 26; const m = add(new THREE.SphereGeometry(1, 20, 10), toon({ color: i % 2 ? '#6f87ad' : '#7d94b8' }), Math.cos(a) * d, DECK - 4, -Math.abs(Math.sin(a)) * d - 140, world, { cast: false }); m.scale.set(r, hh, r * 0.6); }
// sun glow + light shafts
const glowTex = (() => { const [c, g] = cvs(256, 256); const gr = g.createRadialGradient(128, 128, 4, 128, 128, 128); gr.addColorStop(0, 'rgba(255,240,200,1)'); gr.addColorStop(0.25, 'rgba(255,220,160,.5)'); gr.addColorStop(1, 'rgba(255,200,120,0)'); g.fillStyle = gr; g.fillRect(0, 0, 256, 256); return c; })();
const sunGlow = ND_SKIP(new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: P.tex(glowTex), transparent: true, depthWrite: false, fog: false, blending: THREE.AdditiveBlending }))); sunGlow.renderOrder = -1; scene.add(sunGlow);
const shaftTex = (() => { const [c, g] = cvs(64, 256); const gr = g.createLinearGradient(0, 0, 64, 0); gr.addColorStop(0, 'rgba(255,230,170,0)'); gr.addColorStop(0.5, 'rgba(255,230,170,.9)'); gr.addColorStop(1, 'rgba(255,230,170,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 256); const g2 = g.createLinearGradient(0, 0, 0, 256); g2.addColorStop(0, 'rgba(0,0,0,0)'); g2.addColorStop(1, 'rgba(0,0,0,1)'); g.globalCompositeOperation = 'destination-in'; g.fillStyle = g2; g.fillRect(0, 0, 64, 256); return c; })();
const shafts = []; for (let i = 0; i < 7; i++) { const m = ND_SKIP(new THREE.Mesh(new THREE.PlaneGeometry(2.6, 22), new THREE.MeshBasicMaterial({ map: P.tex(shaftTex), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0.0, side: THREE.DoubleSide }))); m.renderOrder = 3; scene.add(m); shafts.push(m); }
// campfire sparks (B) 
const sparks = []; for (let i = 0; i < 14; i++) { const m = ND_SKIP(add(new THREE.SphereGeometry(0.05, 5, 4), new THREE.MeshBasicMaterial({ color: '#ffcf5a' }), 0, 0, 0, world, { cast: false })); sparks.push(m); }
// ship cannons (muzzles that run out of the gun ports) and wakes
const muzzles = []; ships.forEach((g, gi) => { for (let i = 0; i < 6; i++) for (const s of [-1, 1]) { const m = add(new THREE.CylinderGeometry(0.2, 0.26, 1.2, 10), toon({ color: '#17181c' }), s * 1.9, 1.85, 3.5 - i * 1.5, g.userData.sp, { cast: false }); m.rotation.z = Math.PI / 2; m.userData.s = s; m.userData.i = i; muzzles.push(m); } });

// ---------- WEATHER SYSTEM (always on in the engine): wind, gusts, rain, snow, fog, leaves, lightning ----------
// W.weather = { wind: 0..1.5, dx, dz (wind direction), rain: 0..1, snow: 0..1, fog: 0..1, leaves: 0..1 }. Defaults: light breeze.
const WX = { wind: 0.5, dx: 1, dz: 0.25, rain: 0, snow: 0, fog: 0, leaves: 0, gust: 0 };
const WX_DEFAULT = { wind: 0.5, dx: 1, dz: 0.25, rain: 0, snow: 0, fog: 0, leaves: 0 };
const windAt = (x, z, t) => { const g = 0.5 + 0.5 * Math.sin(t * 1.3 - (x * WX.dx + z * WX.dz) * 0.09 + Math.sin(z * 0.05) * 2); return WX.wind * (0.55 + 0.9 * g * (0.4 + 0.6 * WX.wind)); };   // traveling gust wave
const RAIN_N = 3000, SNOW_N = 1500, LEAF_N = 70;
const rainMesh = new THREE.InstancedMesh(new THREE.BoxGeometry(0.016, 1.0, 0.016), new THREE.MeshBasicMaterial({ color: '#cfe4ff', transparent: true, opacity: 0.55, depthWrite: false, fog: false }), RAIN_N); rainMesh.userData.ndSkip = true; rainMesh.frustumCulled = false; rainMesh.renderOrder = 4; scene.add(rainMesh);
const snowMesh = new THREE.InstancedMesh(new THREE.SphereGeometry(0.035, 5, 4), new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: 0.95, depthWrite: false, fog: false }), SNOW_N); snowMesh.userData.ndSkip = true; snowMesh.frustumCulled = false; snowMesh.renderOrder = 4; scene.add(snowMesh);
const leafMesh = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.16, 0.1), new THREE.MeshBasicMaterial({ color: '#ffffff', side: THREE.DoubleSide, transparent: true, depthWrite: false }), LEAF_N); leafMesh.userData.ndSkip = true; leafMesh.frustumCulled = false; leafMesh.renderOrder = 4; scene.add(leafMesh);
{ const c = ['#e0a13a', '#c4572c', '#8fb54a', '#f1c85a', '#b8743a']; for (let i = 0; i < LEAF_N; i++) leafMesh.setColorAt(i, new THREE.Color(c[i % c.length])); leafMesh.instanceColor.needsUpdate = true; }
const rp = P.rng(404), RSEED = [], SSEED = [], LSEED = []; for (let i = 0; i < RAIN_N; i++) RSEED.push([rp(), rp(), rp()]); for (let i = 0; i < SNOW_N; i++) SSEED.push([rp(), rp(), rp(), rp()]); for (let i = 0; i < LEAF_N; i++) LSEED.push([rp(), rp(), rp(), rp()]);
const _qq = new THREE.Quaternion(), _ee = new THREE.Euler(), _pp = new THREE.Vector3(), _ss = new THREE.Vector3(), _mm = new THREE.Matrix4();
function weatherParticles(f, camPos) {
  const t = f / 30, R = 10;
  rainMesh.visible = WX.rain > 0.02; if (rainMesh.visible) {
    const n = Math.floor(RAIN_N * Math.min(1, WX.rain)), slant = Math.atan2(WX.wind * 0.9, 1); rainMesh.count = n;
    for (let i = 0; i < n; i++) { const r = RSEED[i]; const y = ((r[1] * 16 - t * 15 * (0.8 + r[2] * 0.4)) % 16 + 16) % 16; _pp.set(camPos.x + (r[0] - 0.5) * 2 * R + (16 - y) * 0.3 * WX.wind * WX.dx, camPos.y - 4 + y, camPos.z + (r[2] - 0.5) * 2 * R + (16 - y) * 0.3 * WX.wind * WX.dz); _ee.set(0.0, 0, -slant * WX.dx); _qq.setFromEuler(_ee); _ss.set(1, 1, 1); _mm.compose(_pp, _qq, _ss); rainMesh.setMatrixAt(i, _mm); } rainMesh.instanceMatrix.needsUpdate = true; }
  snowMesh.visible = WX.snow > 0.02; if (snowMesh.visible) {
    const n = Math.floor(SNOW_N * Math.min(1, WX.snow)); snowMesh.count = n;
    for (let i = 0; i < n; i++) { const r = SSEED[i]; const y = ((r[1] * 14 - t * (1.0 + r[3] * 1.2)) % 14 + 14) % 14; _pp.set(camPos.x + (r[0] - 0.5) * 2 * R + Math.sin(t * 1.3 + r[3] * 9) * 0.6 + (14 - y) * 0.5 * WX.wind * WX.dx, camPos.y - 3 + y, camPos.z + (r[2] - 0.5) * 2 * R + Math.cos(t * 1.1 + r[3] * 7) * 0.5 + (14 - y) * 0.5 * WX.wind * WX.dz); _ss.setScalar(0.7 + r[3]); _mm.compose(_pp, _qq.identity(), _ss); snowMesh.setMatrixAt(i, _mm); } snowMesh.instanceMatrix.needsUpdate = true; }
  leafMesh.visible = WX.leaves > 0.02; if (leafMesh.visible) {
    const n = Math.floor(LEAF_N * Math.min(1, WX.leaves)); leafMesh.count = n;
    for (let i = 0; i < n; i++) { const r = LSEED[i]; const u = ((r[0] + t * (0.05 + 0.05 * WX.wind) * (0.6 + r[3])) % 1 + 1) % 1; _pp.set(camPos.x - 16 + u * 32 * WX.dx + Math.sin(t * 2 + r[1] * 9) * 0.8, camPos.y - 1.5 + r[2] * 6 + Math.sin(t * 1.5 + r[3] * 7) * 0.8, camPos.z - 14 + r[1] * 20); _ee.set(t * 3 + r[3] * 9, t * 2 + r[1] * 5, t * 4); _qq.setFromEuler(_ee); _ss.setScalar(1); _mm.compose(_pp, _qq, _ss); leafMesh.setMatrixAt(i, _mm); } leafMesh.instanceMatrix.needsUpdate = true; }
}

function setWeather(W) { const w = window.WXO || W.weather || WX_DEFAULT; WX.wind = w.wind ?? 0.5; WX.dx = w.dx ?? 1; WX.dz = w.dz ?? 0.25; WX.rain = w.rain || 0; WX.snow = w.snow || 0; WX.fog = w.fog || 0; WX.leaves = w.leaves || 0; }
function sceneryUpdate(W, f) {
  const t = f / 30; foamMat.uniforms.t.value = t;
  for (let i = 0; i < tufts.length; i++) { const u = tufts[i]; { const wv = windAt(u.x, u.z, t); _e.set(Math.sin(t * 1.6 + u.ph) * 0.1 * (0.5 + wv) + wv * 0.55 * WX.dz, u.ry, Math.cos(t * 1.3 + u.ph) * 0.1 * (0.5 + wv) - wv * 0.55 * WX.dx); } _q.setFromEuler(_e); _p.set(u.x, u.y, u.z); _s.set(u.s, u.s, u.s); _m.compose(_p, _q, _s); tuftMesh.setMatrixAt(i, _m); } tuftMesh.instanceMatrix.needsUpdate = true;
  butter.forEach((g, i) => { const k = g.userData.k, a = t * 0.7 + k; g.visible = !!W.butter; g.position.set(-3 + Math.cos(a) * 5 + Math.sin(a * 2.3) * 1.2, DECK + 1.2 + Math.sin(a * 1.7) * 0.5 + 0.25 * i % 1, -2 + Math.sin(a * 0.9) * 4); g.rotation.y = a; g.children.forEach((w) => { w.rotation.y = w.userData.s * (0.2 + 0.9 * Math.abs(Math.sin(t * 13 + i))); }); });
  // clouds drift
  clouds.forEach((c, i) => { c.position.x += 0.02 + (i % 3) * 0.01; if (c.position.x > 900) c.position.x = -900; });
  // sparks + fire smoke at the US camp
  sparks.forEach((m, i) => { const ph = ((t * 0.7 + i / sparks.length) % 1); m.visible = !!W.fireB; m.position.set(BX - 20 + Math.sin(ph * 9 + i) * 0.5, DECK + 3.5 + 0.5 + ph * 3.6, 12 + Math.cos(ph * 7 + i) * 0.4); m.scale.setScalar(1 - ph); });
  // cannons run out of the gun ports ("pointed across the water")
  muzzles.forEach((m) => { const e = W.ports || 0; m.position.x = m.userData.s * (1.62 + 0.8 * e); m.visible = e > 0.01; });
}
function sceneryLights(L, f, C, focus) {
  if (WX.fog > 0) { scene.fog.near = Math.max(8, scene.fog.near * (1 - 0.85 * WX.fog)); scene.fog.far = Math.max(60, scene.fog.far * (1 - 0.7 * WX.fog)); scene.fog.color.lerp(new THREE.Color('#c9d2dc'), 0.6 * WX.fog); }
  if (WX.rain > 0.02) { scene.fog.color.lerp(new THREE.Color('#7f8da0'), 0.5 * WX.rain); scene.fog.far *= 1 - 0.4 * WX.rain; hemi.intensity *= 1 - 0.25 * WX.rain; sun.intensity *= 1 - 0.45 * WX.rain; }
  // rim light: opposite the sun, colored; sun glow in the sky; volumetric shafts on request
  const az = (L.az + 180) * Math.PI / 180, el = Math.max(8, L.el * 0.7) * Math.PI / 180;
  rimLight.color.set(L.rimC || '#9fc0ff'); rimLight.intensity = L.rimI ?? 0.55; rimLight.position.set(focus.x + Math.cos(el) * Math.cos(az) * 60, focus.y + Math.sin(el) * 60, focus.z + Math.cos(el) * Math.sin(az) * 60); rimLight.target.position.copy(focus);
  const sa = L.az * Math.PI / 180, se = L.el * Math.PI / 180; sunGlow.position.set(C.pos[0] + Math.cos(se) * Math.cos(sa) * 1000, C.pos[1] + Math.sin(se) * 1000, C.pos[2] + Math.cos(se) * Math.sin(sa) * 1000); sunGlow.lookAt(C.pos[0], C.pos[1], C.pos[2]); sunGlow.scale.setScalar(L.glow ? 520 : 0.0001); sunGlow.material.opacity = L.glow || 0;
  shafts.forEach((m, i) => { m.visible = !!L.shafts; if (!L.shafts) return; const k = i / (shafts.length - 1) - 0.5; m.material.opacity = L.shafts * (0.35 + 0.25 * Math.sin(f * 0.03 + i)); m.position.set(C.look[0] + k * 9 + Math.sin(f * 0.01 + i) * 0.4, C.look[1] + 8, C.look[2] - 3 - Math.abs(k) * 4); m.rotation.set(0, Math.atan2(C.pos[0] - m.position.x, C.pos[2] - m.position.z), -0.35); });
}
