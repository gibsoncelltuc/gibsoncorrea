import * as THREE from './lib/three.module.js';
import * as T from './toon.js';
import * as P from './paint.js';
import { GLTFLoader } from './lib/GLTFLoader.js';
import { SHOTS, TOTAL, shotAt, camAt, dofAt, LIGHTS, lightFor, actorsAt, worldAt, fxAt, ASSETS, SETS_USED, SETX, HEROES } from './story.js';

const W = (typeof window !== 'undefined' && window.RENDER_W) || 1080, H = (typeof window !== 'undefined' && window.RENDER_H) || 1920;   // previews may render smaller
const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(W, H, false);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.NoToneMapping;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(40, W / H, 0.08, 1500);
const rx = (a) => a * Math.PI / 180;

// ---------- materials ----------
const grad = (() => { const d = new Uint8Array([90, 90, 90, 255, 255, 255, 255, 255]); const t = new THREE.DataTexture(d, 2, 1); t.minFilter = t.magFilter = THREE.NearestFilter; t.needsUpdate = true; return t; })();

// ---- PAINTED 3D look: world-space brush-stroke pigment variation on every toon material ----
THREE.MeshToonMaterial.prototype.customProgramCacheKey = function () { return this.userData && this.userData.noPaint ? 'liso' : 'pintado'; };   // sem isto o three reaproveitava o shader pintado e o noPaint nao valia
THREE.MeshToonMaterial.prototype.onBeforeCompile = function (sh) {
  if (this.userData && this.userData.noPaint) return;
  sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vWP; varying vec3 vWN;').replace('#include <begin_vertex>', '#include <begin_vertex>\n{ vec4 wp_ = modelMatrix * vec4(transformed,1.0);\n#ifdef USE_INSTANCING\n wp_ = modelMatrix * instanceMatrix * vec4(transformed,1.0);\n#endif\n vWP = wp_.xyz; vWN = normalize(mat3(modelMatrix) * objectNormal); }');
  sh.fragmentShader = sh.fragmentShader.replace('#include <common>', `#include <common>
varying vec3 vWP; varying vec3 vWN;
float h21(vec2 p){ vec3 p3 = fract(vec3(p.xyx)*.1031); p3 += dot(p3, p3.yzx+33.33); return fract((p3.x+p3.y)*p3.z); }
float vn(vec2 p){ vec2 i=floor(p), f=fract(p); f=f*f*(3.-2.*f); return mix(mix(h21(i),h21(i+vec2(1,0)),f.x), mix(h21(i+vec2(0,1)),h21(i+vec2(1,1)),f.x), f.y); }
float stroke(vec2 p, float ang, float len){ float c=cos(ang), s=sin(ang); vec2 q = vec2(c*p.x+s*p.y, -s*p.x+c*p.y); q.x /= len; return vn(q*vec2(3.2,3.9))*.6 + vn(q*vec2(7.,8.)+7.)*.4; }
vec3 paintMod(vec3 col, vec3 p, vec3 n){
  vec3 w = pow(abs(n), vec3(4.)); w /= (w.x+w.y+w.z+1e-4);
  float a = stroke(p.zy*.7, .55, 1.0)*w.x + stroke(p.xz*.7, -.35, 1.0)*w.y + stroke(p.xy*.7, .2, 1.0)*w.z;
  float b = vn(p.xz*.25+p.y*.11)*w.y + vn(p.zy*.25)*w.x + vn(p.xy*.25)*w.z;
  col *= .965 + .055*a;                        // visible brush strokes
  col += (b-.5) * vec3(.014,.005,-.013);       // pigment drift warm<->cool
  float g = vn(p.xz*9.+p.y*5.)*w.y + vn(p.zy*9.)*w.x + vn(p.xy*9.)*w.z; col *= .993 + .012*g; // fine grain (canal: campos chapados, ruido < 2%)
  return col; }
float hgt(vec3 p, vec3 n){ vec3 w = pow(abs(n), vec3(4.)); w /= (w.x+w.y+w.z+1e-4);
  float h = 0.; vec2 a = p.xz, b = p.zy, c = p.xy;
  h += (vn(a*3.1)*.5 + vn(a*8.7)*.3 + vn(a*23.)*.2)*w.y; h += (vn(b*3.1)*.5 + vn(b*8.7)*.3 + vn(b*23.)*.2)*w.x; h += (vn(c*3.1)*.5 + vn(c*8.7)*.3 + vn(c*23.)*.2)*w.z; return h; }`).replace('#include <map_fragment>', '#include <map_fragment>\n diffuseColor.rgb = paintMod(diffuseColor.rgb, vWP, normalize(vWN));').replace('#include <normal_fragment_maps>', `#include <normal_fragment_maps>
 { float h0 = hgt(vWP, normalize(vWN)); float dhx = dFdx(h0), dhy = dFdy(h0); vec3 q0 = dFdx(vViewPosition), q1 = dFdy(vViewPosition); vec3 R1 = cross(q1, normal), R2 = cross(normal, q0); float fDet = dot(q0, R1);
   float fade = 1. / (1. + .035*length(vViewPosition)); vec3 grad = sign(fDet) * (dhx*R1 + dhy*R2); normal = normalize(abs(fDet)*normal - 0.18*fade*grad); }`);
};
const toon = (opts) => new THREE.MeshToonMaterial({ gradientMap: grad, ...opts });
const texM = (c, rx_ = 1, ry_ = 1, color = '#ffffff') => toon({ map: P.tex(c, rx_, ry_), color });
const M = {
  plank: texM(P.planks(1), 1, 6), beam: texM(P.beam(2), 1, 2), beamDark: texM(P.beam(3, [28, 36, 30]), 1, 2),
  rot: texM(P.rotten(4), 1, 1), rotB: texM(P.rotten(14), 1, 1),
  stone: texM(P.stone(4), 1, 1), stoneMoss: texM(P.mossy(P.stone(4), 5, 1.2), 1, 1),
  grass: texM(P.grass(6), 40, 40), dirt: texM(P.dirt(7), 6, 30), plaster: texM(P.plaster(8), 1, 1), plaster2: texM(P.plaster(18, 28), 1, 1),
  roof: texM(P.roof(9), 2, 2), marble: texM(P.marble(10), 1, 1), marbleTop: toon({ color: '#ece2cf' }),
  trunk: toon({ color: '#6a4a32' }), cypress: toon({ color: '#3f6b36' }), pine: toon({ color: '#5c8a3c' }), bush: toon({ color: '#6c9a42' }),
  hill: toon({ color: '#7aa64c' }), hillFar: toon({ color: '#86ad60' }), mount: toon({ color: '#8fa7b8' }), snow: toon({ color: '#f4f6fa' }),
  iron: toon({ color: '#5c5a57' }), bronze: toon({ color: '#b08a4a' }), wood: toon({ color: '#7a5434' }), door: toon({ color: '#5a3a24' }),
  window: toon({ color: '#2b2430' }), red: toon({ color: '#b8282b' }),
};
M.banner = new THREE.MeshToonMaterial({ gradientMap: grad, map: P.tex(P.banner()), alphaTest: 0.5, side: THREE.DoubleSide });
// helmet
const helmetIn = P.tex(P.helmetInside()); helmetIn.wrapS = helmetIn.wrapT = THREE.ClampToEdgeWrapping;
M.helmIn = new THREE.MeshToonMaterial({ gradientMap: grad, map: helmetIn, side: THREE.BackSide });
M.helmOut = toon({ color: '#8f8a7e' });

// ---------- ink / normal-depth contract ----------
const NOINK = 'noink'; // userData flag: never outlined (cards, fx, water handled specially)
const ndMat = new THREE.ShaderMaterial({
  vertexShader: `varying vec3 vN; varying float vD; void main(){ vN = normalize(normalMatrix*normal); vec4 mv = modelViewMatrix*vec4(position,1.); vD = -mv.z; gl_Position = projectionMatrix*mv; }`,
  fragmentShader: `varying vec3 vN; varying float vD; void main(){ vec3 n = normalize(vN); if(!gl_FrontFacing) n = -n; gl_FragColor = vec4(n*.5+.5, vD); }`,
  side: THREE.DoubleSide,
});
const cardNd = (map) => new THREE.ShaderMaterial({
  uniforms: { map: { value: map } },
  vertexShader: `varying vec2 vUv; varying float vD; void main(){ vUv=uv; vec4 mv = modelViewMatrix*vec4(position,1.); vD=-mv.z; gl_Position=projectionMatrix*mv; }`,
  fragmentShader: `uniform sampler2D map; varying vec2 vUv; varying float vD; void main(){ if(texture2D(map,vUv).a<.5) discard; gl_FragColor=vec4(0.,0.,0.,vD); }`,
  side: THREE.DoubleSide,
});
const waterNd = new THREE.ShaderMaterial({
  vertexShader: `varying float vD; void main(){ vec4 mv = modelViewMatrix*vec4(position,1.); vD=-mv.z; gl_Position=projectionMatrix*mv; }`,
  fragmentShader: `varying float vD; void main(){ gl_FragColor=vec4(.5,1.,.5,vD); }`,
});

// ---------- helpers ----------
const add = (geo, mat, x = 0, y = 0, z = 0, parent = scene, opts = {}) => {
  const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.castShadow = opts.cast ?? true; m.receiveShadow = true; parent.add(m); return m;
};
const box = (w, h, d) => new THREE.BoxGeometry(w, h, d);
const uvScale = (geo, su, sv) => { const uv = geo.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) * su, uv.getY(i) * sv); return geo; };
/** box with world-scaled UVs per face (texel density 1 tile per `t` metres) */
const tbox = (w, h, d, t = 2) => {
  const g = box(w, h, d), uv = g.attributes.uv;
  const dims = [[d, h], [d, h], [w, d], [w, d], [w, h], [w, h]];
  for (let f = 0; f < 6; f++) for (let k = 0; k < 4; k++) { const i = f * 4 + k; uv.setXY(i, uv.getX(i) * dims[f][0] / t, uv.getY(i) * dims[f][1] / t); }
  return g;
};

// ---------- sky ----------
const skyU = { top: { value: new THREE.Color() }, hor: { value: new THREE.Color() }, sunDir: { value: new THREE.Vector3() }, sunCol: { value: new THREE.Color() }, sunSize: { value: 0 }, stars: { value: 0 } };
const sky = new THREE.Mesh(new THREE.SphereGeometry(1200, 32, 16), new THREE.ShaderMaterial({
  uniforms: skyU, side: THREE.BackSide, depthWrite: false, fog: false,
  vertexShader: `varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
  fragmentShader: `uniform vec3 top, hor, sunDir, sunCol; uniform float sunSize, stars; varying vec3 vP;
    void main(){ float h = clamp(vP.y,0.,1.); vec3 c = mix(hor, top, pow(h, .42)); if(vP.y<0.) c = hor;
      float s = dot(normalize(vP), normalize(sunDir)); c += sunCol * (smoothstep(1.-sunSize, 1.-sunSize*.6, s) + .35*pow(max(s,0.), 24.)*step(.001,sunSize));
      if (stars > 0.) { vec3 d = normalize(vP); vec2 uv = vec2(atan(d.z, d.x) * 70., d.y * 140.); vec2 g = floor(uv); float r = fract(sin(dot(g, vec2(12.9898, 78.233))) * 43758.5453);   /* CEU ESTRELADO a noite (19/11) */
        vec2 f = fract(uv) - .5; float st = step(.982, r) * smoothstep(.22, .0, length(f)) * smoothstep(.04, .22, d.y); c += vec3(1., .97, .88) * st * stars * (.55 + .45 * fract(r * 91.)); }
      gl_FragColor = vec4(c,1.); }`,
}));
sky.userData.sky = true; scene.add(sky);

// ---------- lights ----------
const hemi = new THREE.HemisphereLight('#ffffff', '#ffffff', 1); scene.add(hemi);
const sun = new THREE.DirectionalLight('#ffffff', 2); sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048); sun.shadow.bias = -0.0006; sun.shadow.normalBias = 0.03; sun.shadow.radius = 2;
scene.add(sun); scene.add(sun.target);
scene.fog = new THREE.Fog('#ffffff', 40, 600);

