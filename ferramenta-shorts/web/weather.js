// ---------- weather + lighting extras (shared by every story): rim light, sun glow, light shafts, WEATHER (wind/rain/snow/fog/leaves) ----------
const rimLight = new THREE.DirectionalLight('#8fb4ff', 0); rimLight.castShadow = false; scene.add(rimLight); scene.add(rimLight.target);
const ND_SKIP = (m) => { m.userData.ndSkip = true; return m; };

// ---- dust motes floating in the light (Ricks Clips: specks drifting in the sunbeams) ----
const MOTES = 220, moteGeo = new THREE.BufferGeometry(); moteGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(MOTES * 3), 3));
const moteMat = new THREE.PointsMaterial({ size: 0.075, color: '#fff0c4', transparent: true, opacity: 0.6, depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true, fog: false });
const motes = ND_SKIP(new THREE.Points(moteGeo, moteMat)); motes.frustumCulled = false; motes.renderOrder = 6; scene.add(motes);
const moteSeed = Array.from({ length: MOTES }, (_, i) => { const r = P.rng(700 + i); return [r(), r(), r(), r(), r(), r()]; });
function updateMotes(f, C, on) {
  motes.visible = on; if (!on) return; const px = C.pos, lk = C.look; let fx = lk[0] - px[0], fy = lk[1] - px[1], fz = lk[2] - px[2]; const fl = Math.hypot(fx, fy, fz) || 1; fx /= fl; fy /= fl; fz /= fl;
  let rx_ = fz, rz_ = -fx; const rl = Math.hypot(rx_, rz_) || 1; rx_ /= rl; rz_ /= rl; const ux = -fy * rx_, uy = fx * rz_ - fz * rx_, uz = fy * rz_; const t = f / 30; const pos = moteGeo.attributes.position;
  for (let i = 0; i < MOTES; i++) { const s = moteSeed[i], d = 2.5 + s[0] * 14, ox = (s[1] - 0.5) * d * 0.9, oy = (s[2] - 0.5) * d * 1.5;
    const dx = Math.sin(t * (0.4 + s[3]) + s[4] * 6) * 0.5, dy = Math.sin(t * (0.3 + s[5] * 0.5) + s[3] * 6) * 0.45 - ((t * 0.15 * (0.4 + s[4])) % 1.2), dz = Math.cos(t * (0.35 + s[4]) + s[1] * 6) * 0.5;
    pos.setXYZ(i, px[0] + fx * d + rx_ * ox + ux * oy + dx, px[1] + fy * d + uy * oy + dy, px[2] + fz * d + rz_ * ox + uz * oy + dz); }
  pos.needsUpdate = true; moteMat.opacity = 0.35 + 0.3 * Math.min(1, (C.moteK ?? 1)); }
// sun glow + light shafts
const glowTex = (() => { const [c, g] = cvs(256, 256); const gr = g.createRadialGradient(128, 128, 4, 128, 128, 128); gr.addColorStop(0, 'rgba(255,240,200,1)'); gr.addColorStop(0.25, 'rgba(255,220,160,.5)'); gr.addColorStop(1, 'rgba(255,200,120,0)'); g.fillStyle = gr; g.fillRect(0, 0, 256, 256); return c; })();
const sunGlow = ND_SKIP(new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: P.tex(glowTex), transparent: true, depthWrite: false, fog: false, blending: THREE.AdditiveBlending }))); sunGlow.renderOrder = -1; scene.add(sunGlow);
const shaftTex = (() => { const [c, g] = cvs(64, 256); const gr = g.createLinearGradient(0, 0, 64, 0); gr.addColorStop(0, 'rgba(255,230,170,0)'); gr.addColorStop(0.5, 'rgba(255,230,170,.9)'); gr.addColorStop(1, 'rgba(255,230,170,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 256); const g2 = g.createLinearGradient(0, 0, 0, 256); g2.addColorStop(0, 'rgba(0,0,0,0)'); g2.addColorStop(1, 'rgba(0,0,0,1)'); g.globalCompositeOperation = 'destination-in'; g.fillStyle = g2; g.fillRect(0, 0, 64, 256); return c; })();
const shafts = []; for (let i = 0; i < 7; i++) { const m = ND_SKIP(new THREE.Mesh(new THREE.PlaneGeometry(2.6, 22), new THREE.MeshBasicMaterial({ map: P.tex(shaftTex), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0.0, side: THREE.DoubleSide }))); m.renderOrder = 3; scene.add(m); shafts.push(m); }
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
function sceneryLights(L, f, C, focus) {
  if (WX.fog > 0) { scene.fog.near = Math.max(8, scene.fog.near * (1 - 0.85 * WX.fog)); scene.fog.far = Math.max(60, scene.fog.far * (1 - 0.7 * WX.fog)); scene.fog.color.lerp(new THREE.Color('#c9d2dc'), 0.6 * WX.fog); }
  if (WX.rain > 0.02) { scene.fog.color.lerp(new THREE.Color('#7f8da0'), 0.5 * WX.rain); scene.fog.far *= 1 - 0.4 * WX.rain; hemi.intensity *= 1 - 0.25 * WX.rain; sun.intensity *= 1 - 0.45 * WX.rain; }
  // rim light: opposite the sun, colored; sun glow in the sky; volumetric shafts on request
  const az = (L.az + 180) * Math.PI / 180, el = Math.max(8, L.el * 0.7) * Math.PI / 180;
  rimLight.color.set(L.rimC || '#9fc0ff'); rimLight.intensity = L.rimI ?? 0.55; rimLight.position.set(focus.x + Math.cos(el) * Math.cos(az) * 60, focus.y + Math.sin(el) * 60, focus.z + Math.cos(el) * Math.sin(az) * 60); rimLight.target.position.copy(focus);
  const sa = L.az * Math.PI / 180, se = L.el * Math.PI / 180; sunGlow.position.set(C.pos[0] + Math.cos(se) * Math.cos(sa) * 1000, C.pos[1] + Math.sin(se) * 1000, C.pos[2] + Math.cos(se) * Math.sin(sa) * 1000); sunGlow.lookAt(C.pos[0], C.pos[1], C.pos[2]); sunGlow.scale.setScalar(L.glow ? 520 : 0.0001); sunGlow.material.opacity = L.glow || 0;
  updateMotes(f, C, !!L.shafts);
  shafts.forEach((m, i) => { m.visible = !!L.shafts; if (!L.shafts) return; const k = i / (shafts.length - 1) - 0.5; m.material.opacity = L.shafts * (0.35 + 0.25 * Math.sin(f * 0.03 + i)); m.position.set(C.look[0] + k * 9 + Math.sin(f * 0.01 + i) * 0.4, C.look[1] + 8, C.look[2] - 3 - Math.abs(k) * 4); m.rotation.set(0, Math.atan2(C.pos[0] - m.position.x, C.pos[2] - m.position.z), -0.35); });
}