// ---------- cards ----------
const CW = 1200, CH = 2000, CM = 2.25; // canvas px, card height in metres (design 600x1000 -> 2.25 m)
const cardGeo = new THREE.PlaneGeometry(CM * 0.6, CM); cardGeo.translate(0, CM / 2 - CM * 0.025, 0);
const blobTex = P.tex(P.radial('20,14,30', 0.6));
const cardWind = { t: { value: 0 }, a: { value: 0.05 } }; const cardLight = { side: { value: 0 }, head: { value: 0.10 }, body: { value: 0.16 } };
class Card {
  constructor(scale = 1, idx = 0) { this.idx = idx;   // semente do vento pelo INDICE da carta (antes Math.random: cada navegador sorteava outra e os personagens/textos tremiam entre quadros)
    [this.c, this.g] = (() => { const c = document.createElement('canvas'); c.width = CW; c.height = CH; return [c, c.getContext('2d')]; })(); this.cw = CW; this.ch = CH;
    this.t = new THREE.CanvasTexture(this.c); this.t.colorSpace = THREE.SRGBColorSpace; this.t.anisotropy = 4;
    this.mat = new THREE.MeshBasicMaterial({ map: this.t, transparent: true, alphaTest: 0.02, side: THREE.DoubleSide, fog: true });
    this.uFlip = { value: 1 }; this.mat.onBeforeCompile = (sh) => { sh.uniforms.wT = cardWind.t; sh.uniforms.wA = cardWind.a; sh.uniforms.wS = this.seed = { value: (this.idx * 2.399963) % 6.2832 }; sh.uniforms.cSide = cardLight.side; sh.uniforms.cHead = cardLight.head; sh.uniforms.cBody = cardLight.body; sh.uniforms.cFlip = this.uFlip;
      sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform float cSide, cHead, cBody, cFlip;').replace('#include <aomap_fragment>', `#include <aomap_fragment>
      #ifdef USE_MAP
      { float hd = smoothstep(.565, .6, vMapUv.y); float hw = mix(.15, .2, hd); float uu = clamp((vMapUv.x - .5) / hw, -1., 1.) * cFlip; float tt = uu * cSide; float dk = smoothstep(-.15, .9, -tt); float g = mix(cBody, cHead, hd);
        reflectedLight.indirectDiffuse *= (1. - g * dk) * mix(vec3(1.), vec3(.9, .87, 1.), dk * .55); }
      #endif`);
      sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nuniform float wT, wA, wS;').replace('#include <begin_vertex>', `#include <begin_vertex>
      float hh_ = clamp((position.y + .056) / 2.25, 0., 1.); float top_ = hh_ * hh_; float hem_ = smoothstep(.55, .0, hh_) * smoothstep(0., .12, hh_);
      transformed.x += wA * (top_ * (.55 * sin(wT * 1.9 + wS) + .35 * sin(wT * 4.3 + wS * 2.)) + hem_ * .5 * sin(wT * 7. + hh_ * 11. + wS));
      transformed.y -= wA * top_ * .15 * (1. + sin(wT * 2.3 + wS));`); };
    this.mesh = new THREE.Mesh(cardGeo, this.mat); this.mesh.userData.card = true; this.mesh.userData.nd = cardNd(this.t); this.mesh.castShadow = true;
    this.mesh.customDepthMaterial = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking, map: this.t, alphaTest: 0.5 });
    this.blob = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: blobTex, transparent: true, depthWrite: false, fog: true }));
    this.blob.rotation.x = -Math.PI / 2; this.blob.userData.ndSkip = true; this.blob.renderOrder = 1;
    scene.add(this.mesh); scene.add(this.blob); this.key = ''; this.mesh.visible = this.blob.visible = false;
  }
  draw(key, fn, th = CH, crop = 0) {   // crop = fracao do alto da carta que fica visivel (0 = tudo): motorista dentro do carro mostra so' cabeca e ombros
    // th = altura (px) do canvas desta carta. Escolhida pelo tamanho do ator na tela (ver cardTier): multidao distante nao precisa de 1200x2000.
    if (key === this.key && th === this.ch && crop === this.crop) return; this.key = key; this.crop = crop;
    if (th !== this.ch) { this.ch = th; this.cw = Math.round(th * CW / CH); this.c.width = this.cw; this.c.height = this.ch; this.t.dispose(); }
    const g = this.g; g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, this.cw, this.ch); g.setTransform(this.cw / 600, 0, 0, this.ch / 1000, 0, 0);
    if (crop) { g.save(); g.beginPath(); g.rect(0, 0, 600, 1000 * crop); g.clip(); }
    const p = new T.Pen(g); fn(p); if (crop) g.restore(); this.t.needsUpdate = true;
    this.bbox = window.INSPECT ? contentBox(this.c) : null;
  }
}
const _cb = document.createElement('canvas'); _cb.width = 120; _cb.height = 200; const _cbg = _cb.getContext('2d', { willReadFrequently: true });
function contentBox(src) { _cbg.clearRect(0, 0, 120, 200); _cbg.drawImage(src, 0, 0, 120, 200); const d = _cbg.getImageData(0, 0, 120, 200).data; let x0 = 120, x1 = 0, y0 = 200, y1 = 0;
  for (let y = 0; y < 200; y++) for (let x = 0; x < 120; x++) if (d[(y * 120 + x) * 4 + 3] > 40) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
  return x1 < x0 ? null : { x0: x0 / 120, x1: (x1 + 1) / 120, y0: y0 / 200, y1: (y1 + 1) / 200 }; }
const cards = []; const getCard = (i) => cards[i] || (cards[i] = new Card(1, i));

// ---------- render targets & post ----------
const rtColor = new THREE.WebGLRenderTarget(W, H, { samples: (window.MSAA ?? 0), type: THREE.HalfFloatType });
const rtNd = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, minFilter: THREE.NearestFilter, magFilter: THREE.NearestFilter });
const rtInk = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType });
const fsCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1), fsGeo = new THREE.PlaneGeometry(2, 2);
const fs = (mat) => { const s = new THREE.Scene(); s.add(new THREE.Mesh(fsGeo, mat)); return s; };
const inkU = { col: { value: rtColor.texture }, nd: { value: rtNd.texture }, res: { value: new THREE.Vector2(W, H) }, focus: { value: 5 }, cinf: { value: 0 }, near: { value: 1 }, px: { value: 1.6 }, fogCol: { value: new THREE.Color() },
  sat: { value: 1.08 }, lift: { value: new THREE.Color(0, 0, 0) }, gain: { value: new THREE.Color(1, 1, 1) }, vig: { value: 0.22 }, flash: { value: 0 }, expo: { value: 1 }, zbl: { value: 0 }, gamt: { value: 1 }, gky: { value: [0.0345, 0.1828, 0.3812, 0.6605, 0.8814, 0.9631, 1] }, gkm: { value: [1.483, 1.404, 1.22, 0.987, 0.661, 0.435, 0.369] }, gsat: { value: new THREE.Vector3(0.983, 1.273, 1.457) }, gtS: { value: new THREE.Vector3(0.0647, -0.0137, -0.0541) }, gtM: { value: new THREE.Vector3(-0.0165, -0.0024, 0.0698) }, gtH: { value: new THREE.Vector3(-0.0075, -0.0004, 0.0267) }, gvig: { value: new THREE.Vector2(0.10, 0.45) } };
const inkScene = fs(new THREE.ShaderMaterial({ uniforms: inkU, vertexShader: `varying vec2 vUv; void main(){ vUv=uv; gl_Position=vec4(position.xy,0.,1.); }`,
  fragmentShader: `uniform sampler2D col, nd; uniform vec2 res; uniform float focus, cinf, near; uniform float px, sat, vig, flash, expo, zbl, gamt; uniform float gky[7], gkm[7]; uniform vec3 gsat, gtS, gtM, gtH; uniform vec2 gvig; uniform vec3 fogCol, lift, gain; varying vec2 vUv;

  vec3 srgb2lin(vec3 c){ return mix(c/12.92, pow((c+.055)/1.055, vec3(2.4)), step(.04045, c)); }
  vec3 lin2srgb(vec3 c){ return mix(c*12.92, 1.055*pow(max(c,0.), vec3(1./2.4))-.055, step(.0031308, c)); }
  vec3 rgb2lab(vec3 c){ vec3 l = srgb2lin(c); vec3 xyz = mat3(.4124,.2126,.0193, .3576,.7152,.1192, .1805,.0722,.9505) * l / vec3(.95047,1.,1.08883);
    vec3 f = mix(7.787*xyz + 16./116., pow(max(xyz,1e-5), vec3(1./3.)), step(.008856, xyz)); return vec3(116.*f.y-16., 500.*(f.x-f.y), 200.*(f.y-f.z)); }
  vec3 lab2rgb(vec3 L){ float fy = (L.x+16.)/116., fx = fy + L.y/500., fz = fy - L.z/200.; vec3 f = vec3(fx,fy,fz); vec3 t3 = f*f*f; vec3 xyz = mix((f-16./116.)/7.787, t3, step(.008856, t3)) * vec3(.95047,1.,1.08883);
    vec3 l = mat3(3.2406,-.9689,.0557, -1.5372,1.8758,-.2040, -.4986,.0415,1.0570) * xyz; return clamp(lin2srgb(l), 0., 1.); }
  // Reference-fitted display grade (tone curve through 7 knots, saturation by zone, 3-way tint, vignette) -- numbers measured on 20 reference shorts
  const float gx[7] = float[7](0., .1, .25, .5, .75, .9, 1.);
  float gradeCurve(float x){ x = clamp(x, 0., 1.); int i = 0; if (x > gx[1]) i = 1; if (x > gx[2]) i = 2; if (x > gx[3]) i = 3; if (x > gx[4]) i = 4; if (x > gx[5]) i = 5;
    float x0 = gx[i], h = gx[i+1] - x0, t = (x - x0) / h, t2 = t*t, t3 = t2*t;
    return (2.*t3 - 3.*t2 + 1.) * gky[i] + (t3 - 2.*t2 + t) * h * gkm[i] + (-2.*t3 + 3.*t2) * gky[i+1] + (t3 - t2) * h * gkm[i+1]; }
  vec3 gradeRC(vec3 src, vec2 uv){
    vec3 c = vec3(gradeCurve(src.r), gradeCurve(src.g), gradeCurve(src.b));
    float y = dot(c, vec3(.2126, .7152, .0722)); float wS = 1. - smoothstep(0., .55, y), wH = smoothstep(.45, 1., y), wM = 1. - wS - wH;
    float s = gsat.y + (gsat.x - gsat.y) * wS + (gsat.z - gsat.y) * wH; c = vec3(y) + s * (c - vec3(y));
    c += wS * gtS + wM * gtM + wH * gtH;
    float r = length(uv * 2. - 1.) * .70710678; c *= 1. - gvig.x * smoothstep(gvig.y, 1., r);
    return mix(src, clamp(c, 0., 1.), gamt); }
  float edgeAt(vec2 uv, float r){
    vec4 c = texture2D(nd, uv); if (dot(c.rgb,c.rgb) < .01) return 0.; float d = c.a; vec3 n = c.rgb*2.-1.;
    float e = 0.; float rr = r * clamp(7./d, .62, 1.25); float i0 = 1./d;
    for (int i=0;i<16;i++){ float a = float(i)*.785398 + (i>7 ? .39 : 0.); float k = i>7 ? .5 : 1.;
      vec2 o = vec2(cos(a), sin(a))*rr*k/res; vec4 s = texture2D(nd, uv+o);
      float ds = s.a; bool card = dot(s.rgb,s.rgb) < .01;
      if (card && ds > 0.) continue;            // character cards: never outlined by the world ink
      if (card) ds = 1e4;                        // sky
      vec3 ns = s.rgb*2.-1.;
      // depth jump, near side only -- measured against the local PLANE: on a flat surface 1/depth is affine on screen, so the opposite tap
      // predicts this one (2/d - 1/d2).  A plain depth ratio inked ground seen at a grazing angle as a huge black band at the horizon.
      float ip = i0; vec4 s2 = texture2D(nd, uv-o); if (dot(s2.rgb,s2.rgb) >= .01) ip = max(2.*i0 - 1./s2.a, 0.);
      e = max(e, smoothstep(.006, .02, (ip - 1./ds)/i0));
      if (!card && abs(ds-d)/d < .06) e = max(e, smoothstep(.93, .80, dot(n, ns)) * .9); // crease
    }
    return e * (1. - smoothstep(150., 450., d)*.3);
  }
  void main(){
    vec3 c = texture2D(col, vUv).rgb;
    if (zbl > .01) { vec3 acc = c; vec2 dir = (vec2(.5) - vUv); for (int i = 1; i < 9; i++) { acc += texture2D(col, vUv + dir * (float(i) / 8.) * zbl * .22).rgb; } c = acc / 9.; }
    { vec3 bl = vec3(0.); for (int i=0;i<12;i++){ float a_ = float(i)*.5236; vec2 o = vec2(cos(a_),sin(a_)) * (i<6 ? 14. : 34.) / res; vec3 s_ = texture2D(col, vUv+o).rgb; bl += max(s_ - .82, 0.); } c += bl * .07 * vec3(1.,.93,.82); }
    float e = edgeAt(vUv, px) * (1. - .75*zbl);
    c = mix(c, vec3(.012,.01,.014), e);
    if (flash < -0.5) c = vec3(e);
    c = c*gain + lift; c *= expo; c = clamp(c, 0., 1.); { vec3 d_ = gradeRC(lin2srgb(c), vUv); d_ = mix(d_, d_*d_*(3.-2.*d_), .24); c = srgb2lin(d_); }   // contraste medido no canal: mais preto profundo (4% dos pixels), mesma media
    c = mix(c, vec3(1.), flash);
    float dd = texture2D(nd, vUv).a; if (dd <= 0.) dd = 2000.; float kk = 1. - focus/dd; float coc_ = kk > 0. ? cinf*kk : min(-kk*cinf*near, cinf*1.4);
    gl_FragColor = vec4(c, coc_); }` }));
const dofU = { src: { value: rtInk.texture }, nd: { value: rtNd.texture }, res: { value: new THREE.Vector2(W, H) }, focus: { value: 5 }, cinf: { value: 0 }, near: { value: 1 } };
const dofScene = fs(new THREE.ShaderMaterial({ uniforms: dofU, vertexShader: `varying vec2 vUv; void main(){ vUv=uv; gl_Position=vec4(position.xy,0.,1.); }`,
  fragmentShader: `uniform sampler2D src, nd; uniform vec2 res; uniform float focus, cinf, near; varying vec2 vUv;
  // O CoC vem pronto no alfa de src (calculado no passe de tinta): 1 leitura por amostra em vez de 2. Numero de amostras proporcional a area do disco (min 8, max 48).
  void main(){
    vec4 s0 = texture2D(src, vUv); float c0 = s0.a;
    if (cinf < .5 || c0 < .6) { gl_FragColor = linearToOutputTexel(vec4(s0.rgb, 1.)); return; }
    int n = int(clamp(c0*c0*.9, 10., 48.));
    vec3 acc = vec3(0.); float wsum = 0.;
    for (int i=0;i<48;i++){ if (i >= n) break; float fi = float(i); float r = sqrt((fi+.5)/float(n)); float a = fi*2.39996;
      vec2 o = vec2(cos(a), sin(a))*r*c0/res; vec4 t = texture2D(src, vUv+o);
      float w = smoothstep(r*c0-1.5, r*c0+.5, t.a + .5);
      acc += t.rgb*w; wsum += w; }
    gl_FragColor = linearToOutputTexel(vec4(acc/max(wsum,1e-3), 1.)); }` }));
// final copy with sRGB handled by the renderer output (we render to screen with linear->sRGB in the shader chunk)
dofScene.children[0].material.toneMapped = false;

// ---------- per-frame state ----------
const tmpV = new THREE.Vector3();
function applyLight(L, f) {
  hemi.color.set(L.sky); hemi.groundColor.set(L.ground); hemi.intensity = L.hemi;
  sun.color.set(L.sun); sun.intensity = L.sunI;
  scene.fog.color.set(L.fog); scene.fog.near = L.fogNear; scene.fog.far = L.fogFar;
  skyU.top.value.set(L.skyTop); skyU.hor.value.set(L.skyHor); skyU.sunCol.value.set(L.sunDisc || '#000'); skyU.sunSize.value = L.sunSize || 0;
  inkU.sat.value = L.sat; inkU.gain.value.set(L.gain || '#ffffff'); inkU.lift.value.set(L.lift || '#000000');
}
function placeSun(L, focus) {
  // sun direction from azimuth/elevation in world space
  const az = rx(L.az), el = rx(L.el); tmpV.set(Math.cos(el) * Math.cos(az), Math.sin(el), Math.cos(el) * Math.sin(az));
  skyU.sunDir.value.copy(tmpV);
  sun.position.copy(focus).addScaledVector(tmpV, 80); sun.target.position.copy(focus);
  const ext = L.shadowExt || 30, sc = sun.shadow.camera; sc.left = -ext; sc.right = ext; sc.top = ext; sc.bottom = -ext; sc.near = 1; sc.far = 200; sc.updateProjectionMatrix();
}

// ---- resolucao adaptativa das cartas (otimizacao de render): altura do canvas = altura do ator na tela (+folga), em degraus de ~1.25x.
// Deterministico (depende so' do quadro, nunca do estado anterior) => shards/retomadas geram exatamente a mesma imagem. CARD_FULL=1 desliga.
const CARD_TIERS = [256, 320, 400, 500, 640, 800, 1000, 1280, 1600, 2000];
function cardTier(a, cam) {
  if (window.CARD_FULL) return CH;
  const s = a.s || 1, dx = a.x - cam.position.x, dy = a.y + 1.1 * s - cam.position.y, dz = a.z - cam.position.z;
  const d = Math.max(0.4, Math.hypot(dx, dy, dz)), px = (CM * s) / (2 * d * Math.tan(rx(cam.fov) / 2)) * H;
  const need = Math.min(CH, px * (window.CARD_HEADROOM || 1.2)); for (const t of CARD_TIERS) if (t >= need) return t; return CH;
}
function drawActors(list, cam) {
  cards.forEach((c) => { c.mesh.visible = c.blob.visible = false; });
  list.forEach((a, i) => {
    const c = getCard(i);
    c.draw(a.key, a.draw, cardTier(a, cam), a.crop || 0);
    c.mesh.visible = true; c.mesh.position.set(a.x, a.y, a.z);
    const s = a.s || 1; c.mesh.scale.set(s * (a.flip ? -1 : 1), s, s); c.uFlip.value = a.flip ? -1 : 1;
    c.mesh.rotation.set(0, Math.atan2(cam.position.x - a.x, cam.position.z - a.z) + (a.yaw || 0), a.roll || 0);
    if (a.keepColor) { const gn = inkU.gain.value; c.mat.color.setRGB(Math.min(1.5, 1.06 / Math.max(0.5, gn.r)), Math.min(1.5, 1.03 / Math.max(0.5, gn.g)), Math.min(1.5, 1.3 / Math.max(0.5, gn.b))); if (c.mat.fog) { c.mat.fog = false; c.mat.needsUpdate = true; } } else { if (a.tint) c.mat.color.set(a.tint); else { const gn = inkU.gain.value, k = 0.55, f_ = (v) => 1 + k * (Math.min(1.4, 1 / Math.max(0.6, v)) - 1); c.mat.color.setRGB(f_(gn.r), f_(gn.g), f_(gn.b)); }   /* compensa 55% da cor da luz: rosto continua branco (canal), sem virar laranja no por do sol */ if (!c.mat.fog) { c.mat.fog = true; c.mat.needsUpdate = true; } }
    if (c.mat.depthTest === !!a.front) { c.mat.depthTest = !a.front; c.mat.depthWrite = !a.front; c.mat.needsUpdate = true; }
    c.mat.opacity = a.alpha ?? 1;
    c.mesh.castShadow = a.shadow !== false;
    c.mesh.renderOrder = a.order || 2;
    if (a.blob !== false && !a.crop && a.y < DECK + 0.5) { c.blob.visible = true; c.blob.position.set(a.x, (a.ground ?? DECK) + 0.02, a.z); c.blob.scale.set(0.95 * s, 0.6 * s, 1); }
  });
}

const swapForNd = (on) => {
  scene.traverse((o) => {
    if (o.isPoints) { if (on) { o.userData.vis0 = o.visible; o.visible = false; } else if (o.userData.vis0 !== undefined) { o.visible = o.userData.vis0; delete o.userData.vis0; } return; }
    if (!o.isMesh) return;
    if (on) {
      o.userData.mat0 = o.material;
      if (o.userData.ndSkip) { o.userData.vis0 = o.visible; o.visible = false; return; }
      if (o === sky || o.userData.sky) { o.userData.vis0 = o.visible; o.visible = false; return; }
      o.material = o.userData.nd || ndMat;
    } else {
      o.material = o.userData.mat0; if (o.userData.vis0 !== undefined) { o.visible = o.userData.vis0; delete o.userData.vis0; }
    }
  });
};

window.inspectFrame = (f) => {
  window.INSPECT = true;
  const S = shotAt(f), C = window.TESTCAM ? { flash: 0, ...window.TESTCAM } : camAt(f), W_ = worldAt(f);
  setWeather(W_); worldState(W_, f); sceneryUpdate(W_, f);
  camera.position.set(...C.pos); camera.up.set(0, 1, 0); camera.lookAt(...C.look); camera.rotateZ(rx(C.roll || 0)); camera.fov = C.fov; camera.updateProjectionMatrix(); scene.updateMatrixWorld(true); camera.updateMatrixWorld(true);
  const acts = actorsAt(f, T), out = { f, shot: S.id, cam: { pos: C.pos, look: C.look, fov: C.fov }, actors: [] };
  const occl = []; scene.traverse((o) => { if (o.isMesh && o.visible && !o.userData.ndSkip && !o.userData.card && !o.userData.sky && !o.isInstancedMesh && o !== sky && o.material !== undefined) { let v = true, p = o; while (p) { if (!p.visible) v = false; p = p.parent; } if (v && !o.userData.nd) occl.push(o); } });
  const ray = new THREE.Raycaster(), cp = camera.position.clone();
  // camera inside geometry: short rays in 6 directions
  let inside = null; for (const d of [[0, 0, -1], [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]]) { const dir = new THREE.Vector3(...d).applyQuaternion(camera.quaternion); ray.set(cp, dir); ray.far = 0.35; const h = ray.intersectObjects(occl, false); if (h.length) { inside = (h[0].object.name || h[0].object.geometry.type) + '@' + h[0].distance.toFixed(2); break; } }
  if (!inside && C.pos[1] < DECK + 0.3) inside = 'below-ground@' + (C.pos[1] - DECK).toFixed(2);
  if (!inside) { // camera INSIDE a closed solid (house, truck, tank...): prefilter by the mesh's local bounding box, then confirm with double-sided rays (first hit is a back face from >=4 of 6 directions)
    const lp = new THREE.Vector3(), dirs = [[0, 0, -1], [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1]], ws = new THREE.Vector3(), sz = new THREE.Vector3();
    for (const o of occl) { const m = o.material; if (!m || m.side !== THREE.FrontSide || !o.geometry) continue; const g = o.geometry; if (!g.boundingBox) g.computeBoundingBox(); const bb = g.boundingBox; lp.copy(cp); o.worldToLocal(lp);
      if (!(lp.x > bb.min.x && lp.x < bb.max.x && lp.y > bb.min.y && lp.y < bb.max.y && lp.z > bb.min.z && lp.z < bb.max.z)) continue;
      o.getWorldScale(ws); bb.getSize(sz); if (Math.min(sz.x * Math.abs(ws.x), sz.y * Math.abs(ws.y), sz.z * Math.abs(ws.z)) < 0.7) continue;
      m.side = THREE.DoubleSide; let back = 0; for (const d of dirs) { ray.set(cp, new THREE.Vector3(...d)); ray.far = 80; const hs = ray.intersectObject(o, false); if (hs.length && hs[0].face && hs[0].face.normal.clone().transformDirection(o.matrixWorld).dot(ray.ray.direction) > 0) back++; } m.side = THREE.FrontSide;
      if (back >= 4) { inside = 'inside solid ' + (o.name || o.geometry.type); break; } } }
  out.cameraInside = inside;
  acts.forEach((a, i) => {
    const c = getCard(i); c.draw(a.key, a.draw); const bb = c.bbox; if (!bb) return;
    const s = a.s || 1, top = a.y + 2.194 * s, hgt = 2.25 * s;
    const right = new THREE.Vector3(cp.z - a.z, 0, -(cp.x - a.x)).normalize().multiplyScalar(0.675 * s * (a.flip ? -1 : 1));
    const P = (fx, fy) => new THREE.Vector3(a.x + right.x * (2 * fx - 1), top - fy * hgt, a.z + right.z * (2 * fx - 1)).project(camera);
    const pts = [P(bb.x0, bb.y0), P(bb.x1, bb.y0), P(bb.x0, bb.y1), P(bb.x1, bb.y1)];
    const xs = pts.map((p) => (p.x + 1) / 2), ys = pts.map((p) => (1 - p.y) / 2), behind = pts.some((p) => p.z > 1 || p.z < -1);
    const bx0 = Math.min(...xs), bx1 = Math.max(...xs), by0 = Math.min(...ys), by1 = Math.max(...ys);
    const ix = Math.max(0, Math.min(1, bx1) - Math.max(0, bx0)), iy = Math.max(0, Math.min(1, by1) - Math.max(0, by0)), area = (bx1 - bx0) * (by1 - by0), vis = area > 0 ? (ix * iy) / area : 0;
    // occlusion: rays to head / chest / feet of the drawn content
    const hits = []; for (const fy of [bb.y0 + 0.12 * (bb.y1 - bb.y0), bb.y0 + 0.38 * (bb.y1 - bb.y0)]) { const tgt = new THREE.Vector3(a.x, top - fy * hgt, a.z); const dir = tgt.clone().sub(cp); const dist = dir.length(); ray.set(cp, dir.normalize()); ray.far = dist - 0.3; const h = ray.intersectObjects(occl, false); hits.push(h.length ? { by: (h[0].object.name || h[0].object.geometry.type) + '/' + (h[0].object.material.color ? '#' + h[0].object.material.color.getHexString() : '?'), d: +h[0].distance.toFixed(2) } : null); }
    out.actors.push({ i, id: a.id || (a.key || '').slice(0, 8), x: +a.x.toFixed(2), z: +a.z.toFixed(2), dist: +cp.distanceTo(new THREE.Vector3(a.x, a.y, a.z)).toFixed(2), box: [+bx0.toFixed(3), +by0.toFixed(3), +bx1.toFixed(3), +by1.toFixed(3)], visible: +vis.toFixed(3), heightFrac: +(by1 - by0).toFixed(3), behind, occluded: hits.filter(Boolean).length, occluder: (hits.find(Boolean) || {}).by || null });
  });
  // 3D animals (props from the pool): project their world bounding boxes so the take inspector covers them too
  for (const nm of ['bear', 'horse', 'emu']) for (const o of (propPool[nm] || [])) { if (!o.visible) continue; const bb3 = new THREE.Box3().setFromObject(o); if (bb3.isEmpty()) continue;
    const cs = []; for (const x of [bb3.min.x, bb3.max.x]) for (const y of [bb3.min.y, bb3.max.y]) for (const z of [bb3.min.z, bb3.max.z]) cs.push(new THREE.Vector3(x, y, z).project(camera));
    const behind = cs.every((p) => p.z > 1 || p.z < -1), xs = cs.map((p) => (p.x + 1) / 2), ys = cs.map((p) => (1 - p.y) / 2), bx0 = Math.min(...xs), bx1 = Math.max(...xs), by0 = Math.min(...ys), by1 = Math.max(...ys);
    const ix = Math.max(0, Math.min(1, bx1) - Math.max(0, bx0)), iy = Math.max(0, Math.min(1, by1) - Math.max(0, by0)), area = (bx1 - bx0) * (by1 - by0), vis = area > 0 ? (ix * iy) / area : 0;
    out.actors.push({ i: 900, id: nm, animal3d: true, x: +o.position.x.toFixed(2), z: +o.position.z.toFixed(2), dist: +cp.distanceTo(o.position).toFixed(2), box: [+bx0.toFixed(3), +by0.toFixed(3), +bx1.toFixed(3), +by1.toFixed(3)], visible: +vis.toFixed(3), heightFrac: +(by1 - by0).toFixed(3), behind, occluded: 0, occluder: '' }); }
  return out;
};
const renderCore = (f) => {
  const S = shotAt(f), L = lightFor(S, f), C = window.TESTCAM ? { flash: 0, ...window.TESTCAM } : camAt(f);
  const W_ = worldAt(f); setWeather(W_);
  applyLight(L, f);
  sceneryLights(L, f, C, new THREE.Vector3(...C.look), null);
  weatherParticles(f, { x: C.pos[0], y: C.pos[1], z: C.pos[2] });
  camera.position.set(...C.pos); camera.up.set(0, 1, 0); camera.lookAt(...C.look); camera.rotateZ(rx(C.roll || 0));
  camera.fov = C.fov; camera.updateProjectionMatrix(); camera.updateMatrixWorld();
  worldState(W_, f); sceneryUpdate(W_, f);
  placeSun(L, new THREE.Vector3(...(C.shadowAt || C.look)));
  { const sd = sun.position.clone().sub(sun.target.position).normalize().transformDirection(camera.matrixWorldInverse); const ax = Math.abs(sd.x), k = Math.min(1, Math.max(0, ax / 0.35)); cardLight.side.value = Math.sign(sd.x) * k * k * (3 - 2 * k); }
  cardWind.t.value = f / 30; cardWind.a.value = (window.NOWIND ? 0 : 0.035 + 0.11 * WX.wind);
  const ACTS = actorsAt(f, T);
  drawActors([...ACTS, ...fxAt(f, T)], camera);
  sky.position.copy(camera.position);
  clouds.forEach((c) => { c.position.x = camera.position.x + (c.userData.rx ?? 0); c.position.z = camera.position.z + (c.userData.rz ?? -400); c.material.color.set(L.cloud || '#ffffff'); });   /* nuvem acompanha a luz (escura de noite e na chuva) */
  // pass A: colour
  renderer.setRenderTarget(rtColor); renderer.setClearColor(0x000000, 1); renderer.clear(); renderer.render(scene, camera);
  // pass B: normal + depth
  const fog = scene.fog; scene.fog = null; const sm = renderer.shadowMap.enabled; renderer.shadowMap.enabled = false; renderer.shadowMap.autoUpdate = false;
  swapForNd(true); renderer.setRenderTarget(rtNd); renderer.setClearColor(0x000000, 0); renderer.clear(); renderer.render(scene, camera); swapForNd(false);
  scene.fog = fog; renderer.shadowMap.enabled = sm; renderer.shadowMap.autoUpdate = true;
  if (window.DEBUG_ND) { const dm = new THREE.MeshBasicMaterial({ map: rtNd.texture }); const ds = fs(dm); renderer.setRenderTarget(null); renderer.render(ds, fsCam); return true; }
  // ink + grade
  const D = window.TESTCAM ? { focus: window.TESTCAM.focus || 5, cinf: window.TESTCAM.cinf || 4 } : dofAt(f);
  if (!window.TESTCAM && !(S.dof && S.dof.focus !== undefined)) {   // the lens always focuses on the NEAREST character in the middle of the frame (faces never go soft); only the background / foreground props blur
    const fw = new THREE.Vector3(); camera.getWorldDirection(fw); const cp_ = camera.position; let best = Infinity;
    const cand = [...ACTS.map((a) => [a.x, a.y + 1.1 * (a.s || 1), a.z]), ...(W_.props || []).filter((p) => p.asset === 'bear' || p.asset === 'horse' || p.asset === 'emu').map((p) => [p.x, p.y + 1.0, p.z])];
    for (const q of cand) { const v = new THREE.Vector3(q[0] - cp_.x, q[1] - cp_.y, q[2] - cp_.z), dep = v.dot(fw); if (dep < 0.6) continue; const pr = new THREE.Vector3(q[0], q[1], q[2]).project(camera); if (Math.abs(pr.x) > 0.85 || Math.abs(pr.y) > 0.92) continue; if (dep < best) best = dep; }
    if (best < Infinity && best < D.focus * 1.05) D.focus = best; else if (best < Infinity) D.focus = Math.min(D.focus, Math.max(best, D.focus * 0.6));
    D.near = 0.45; }
  { const G = (L.gsel ?? 0), mx = (a, b) => a + (b - a) * G;
    const D = { ky: [0, 0.1, 0.25, 0.5, 0.75, 0.9, 1], km: [1, 1, 1, 1, 1, 1, 1], sat: [1.05, 1.2, 1.15], tS: [-0.012, -0.018, 0.04], tM: [-0.006, -0.01, 0.036], tH: [0, 0, 0], vg: [0.10, 0.45], amt: 1 };
    const Gd = { ky: [0, 0.1, 0.25, 0.5, 0.75, 0.9, 1], km: [1, 1, 1, 1, 1, 1, 1], sat: [0.98, 1.1, 1.2], tS: [-0.01, -0.03, 0.07], tM: [-0.006, -0.02, 0.05], tH: [0, 0, 0], vg: [0.16, 0.40], amt: 1 };
    inkU.gky.value = D.ky.map((v, i) => mx(v, Gd.ky[i])); inkU.gkm.value = D.km.map((v, i) => mx(v, Gd.km[i])); inkU.gsat.value.set(...D.sat.map((v, i) => mx(v, Gd.sat[i]))); inkU.gtS.value.set(...D.tS.map((v, i) => mx(v, Gd.tS[i]))); inkU.gtM.value.set(...D.tM.map((v, i) => mx(v, Gd.tM[i]))); inkU.gtH.value.set(...D.tH.map((v, i) => mx(v, Gd.tH[i]))); inkU.gvig.value.set(mx(D.vg[0], Gd.vg[0]), mx(D.vg[1], Gd.vg[1])); inkU.gamt.value = window.GRADE_OFF ? 0 : (L.gamt ?? mx(D.amt, Gd.amt)); }
  inkU.zbl.value = C.zb || 0; inkU.px.value = 3.2; inkU.expo.value = L.exp ?? 1; inkU.sat.value = Math.max((L.sat ?? 1.08) * 1.05, 1.1); inkU.flash.value = window.DEBUG_E ? -1 : (C.flash || 0); inkU.vig.value = L.vig ?? 0.22;
  D.cinf *= (window.DOF_K ?? 0.6);   /* canal: fundo nitido ou so' levemente desfocado em 96% dos quadros */ inkU.focus.value = D.focus; inkU.cinf.value = D.cinf; inkU.near.value = D.near ?? 1;
  renderer.setRenderTarget(rtInk); renderer.render(inkScene, fsCam);
  // lens
  dofU.focus.value = D.focus; dofU.cinf.value = D.cinf; dofU.near.value = D.near ?? 1;
  renderer.setRenderTarget(null); renderer.render(dofScene, fsCam);
  return true;
};
// ---- transitions: cross-dissolve between shots (outgoing shot is re-rendered past its end and blended) ----
const compA = document.createElement('canvas'), compB = document.createElement('canvas'); compA.width = compB.width = canvas.width; compA.height = compB.height = canvas.height;
const cgA = compA.getContext('2d'), cgB = compB.getContext('2d'); let compOn = false;
window.renderFrame = (f) => {
  compOn = false; const si = SHOTS.findIndex((s) => f >= s.a && f <= s.b), S = SHOTS[si];
  if (S && S.tr && S.tr.type !== 'cut' && S.tr.N > 0 && si > 0 && f < S.a + S.tr.N && !window.NOTRANS && !window.TESTCAM) {
    const k = (f - S.a + 1) / (S.tr.N + 1), t = k * k * (3 - 2 * k);
    window.__force(si - 1); renderCore(f); window.__force(null); cgA.clearRect(0, 0, compA.width, compA.height); cgA.drawImage(canvas, 0, 0);
    renderCore(f); cgB.clearRect(0, 0, compB.width, compB.height); cgB.drawImage(canvas, 0, 0);
    cgA.globalAlpha = t; cgA.drawImage(compB, 0, 0); cgA.globalAlpha = 1; compOn = true; return true;
  }
  return renderCore(f);
};
window.getFrameDataURL = (q = 0.92) => (compOn ? compA : canvas).toDataURL('image/jpeg', q);
window.TOTAL = TOTAL;
window.ready = true;
