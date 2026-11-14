import React, { useLayoutEffect, useMemo, useRef } from 'react';
import * as THREE from 'three';
import { rng, mixHex, lerp, clamp, smoother } from '../lib/anim';
import { ModeCtx } from '../characters/Rig';
import { cloudTex, rayTex, dotTex } from './tex';

// ---------- Materiais toon (rampa de 4 passos: 168/206/236/255 — sombras nunca pretas) ----------
export const toonGrad = (() => {
  const d = new THREE.DataTexture(new Uint8Array([168, 206, 236, 255]), 4, 1, THREE.RedFormat);
  d.minFilter = d.magFilter = THREE.NearestFilter; d.needsUpdate = true; return d;
})();
export const Toon: React.FC<{ color: string; map?: THREE.Texture; opacity?: number; emissive?: string; side?: THREE.Side }> = ({ color, map, opacity = 1, emissive, side }) => {
  const { animatic } = React.useContext(ModeCtx);
  return <meshToonMaterial color={animatic ? '#a8a8b4' : color} map={animatic ? undefined : map} gradientMap={toonGrad} transparent={opacity < 1} opacity={opacity} emissive={emissive ?? '#000000'} side={side} />;
};

// ---------- Ambientes ----------
export type Env = { top: string; mid: string; bot: string; sun: string; sunPos: [number, number, number]; sunI: number; hemiSky: string; hemiGround: string; hemiI: number; fog: string; grass: [string, string, string]; water: [string, string, string] };
export const ENVS: Record<string, Env> = {
  golden: { top: '#3f7fe0', mid: '#8fbcf2', bot: '#ffd9a4', sun: '#ffb25e', sunPos: [-34, 20, -34], sunI: 2.7, hemiSky: '#86a8f0', hemiGround: '#8a62a8', hemiI: 1.0, fog: '#f2d8b4', grass: ['#d9b64e', '#8f8a3a', '#f0cf68'], water: ['#1c70b4', '#35a0d8', '#cdeeff'] },
  bright: { top: '#3a86e0', mid: '#9ccaf6', bot: '#e8f4ff', sun: '#ffe2b0', sunPos: [22, 30, 24], sunI: 2.4, hemiSky: '#8cb0f0', hemiGround: '#7a6aa8', hemiI: 1.1, fog: '#dcecf8', grass: ['#d9b64e', '#8f8a3a', '#f0cf68'], water: ['#1c70b4', '#35a0d8', '#cdeeff'] },
  dusk: { top: '#4a4198', mid: '#e0629a', bot: '#ffb765', sun: '#ff8f4a', sunPos: [-36, 7, -36], sunI: 2.5, hemiSky: '#7a62c0', hemiGround: '#7a4a92', hemiI: 1.05, fog: '#e8a8a0', grass: ['#c89a46', '#7a6a38', '#e8b85a'], water: ['#3a4a9a', '#7a6ac0', '#ffc8a0'] },
};
const KEYS = Object.keys(ENVS.golden) as (keyof Env)[];
export const mixEnv = (a: Env, b: Env, t: number): Env => {
  const o: any = {};
  for (const k of KEYS) { const va = a[k] as any, vb = b[k] as any;
    o[k] = typeof va === 'string' ? mixHex(va, vb, t) : Array.isArray(va) ? va.map((x: any, i: number) => (typeof x === 'string' ? mixHex(x, vb[i], t) : lerp(x, vb[i], t))) : lerp(va, vb, t); }
  return o as Env;
};
export const envAt = (t: number, ks: [number, keyof typeof ENVS][]): Env => {
  if (t <= ks[0][0]) return ENVS[ks[0][1]];
  for (let i = 1; i < ks.length; i++) if (t <= ks[i][0]) return mixEnv(ENVS[ks[i - 1][1]], ENVS[ks[i][1]], smoother((t - ks[i - 1][0]) / (ks[i][0] - ks[i - 1][0])));
  return ENVS[ks[ks.length - 1][1]];
};

export const Lights: React.FC<{ env: Env; at?: [number, number, number] }> = ({ env, at = [0, 0, 0] }) => (
  <>
    <hemisphereLight args={[env.hemiSky, env.hemiGround, env.hemiI * 1.25]} />
    <ambientLight color="#d4c4e8" intensity={0.55} />
    <directionalLight color={env.sun} intensity={env.sunI} position={[at[0] + env.sunPos[0], at[1] + env.sunPos[1], at[2] + env.sunPos[2]]} />
    <directionalLight color="#6a80d0" intensity={0.5} position={[at[0] + 24, at[1] + 8, at[2] + 18]} />
  </>
);

export const Sky: React.FC<{ env: Env; at?: [number, number, number] }> = ({ env, at = [0, 0, 0] }) => {
  const geo = useMemo(() => { const g = new THREE.SphereGeometry(450, 24, 16); g.setAttribute('color', new THREE.BufferAttribute(new Float32Array(g.attributes.position.count * 3), 3)); return g; }, []);
  useLayoutEffect(() => {
    const col = geo.attributes.color as THREE.BufferAttribute, pos = geo.attributes.position;
    const top = new THREE.Color(env.top), mid = new THREE.Color(env.mid), bot = new THREE.Color(env.bot), c = new THREE.Color();
    for (let i = 0; i < pos.count; i++) { const h = clamp(pos.getY(i) / 450 * 1.9 + 0.1, 0, 1); if (h < 0.35) c.copy(bot).lerp(mid, h / 0.35); else c.copy(mid).lerp(top, (h - 0.35) / 0.65); col.setXYZ(i, c.r, c.g, c.b); }
    col.needsUpdate = true;
  });
  const s = env.sunPos, n = Math.hypot(...s);
  return (
    <group position={at}>
      <mesh geometry={geo}><meshBasicMaterial vertexColors side={THREE.BackSide} fog={false} toneMapped={false} /></mesh>
      <group position={[(s[0] / n) * 420, (s[1] / n) * 420, (s[2] / n) * 420]} rotation={[0, Math.atan2(-s[0], -s[2]), 0]}>
        <mesh><circleGeometry args={[70, 32]} /><meshBasicMaterial color={env.sun} transparent opacity={0.22} fog={false} toneMapped={false} blending={THREE.AdditiveBlending} depthWrite={false} /></mesh>
        <mesh position={[0, 0, 0.1]}><circleGeometry args={[30, 32]} /><meshBasicMaterial color="#fff4d0" fog={false} toneMapped={false} /></mesh>
      </group>
    </group>
  );
};

export const Clouds: React.FC<{ t: number; at?: [number, number, number]; seed?: number; tint?: string; z?: number }> = ({ t, at = [0, 0, 0], seed = 4, tint = '#ffffff', z = -330 }) => {
  const tex = cloudTex();
  const items = useMemo(() => { const r = rng(seed); return Array.from({ length: 10 }, () => ({ x: (r() - 0.5) * 700, y: 60 + r() * 90, w: 90 + r() * 110, sp: 0.8 + r() * 1.2 })); }, [seed]);
  return (
    <group position={[at[0], at[1], at[2] + z]}>
      {items.map((c, i) => (
        <mesh key={i} position={[((c.x + t * c.sp + 350) % 700) - 350, c.y, 0]} scale={[c.w, c.w * 0.5, 1]}>
          <planeGeometry args={[1, 1]} /><meshBasicMaterial map={tex} color={tint} transparent opacity={0.92} depthWrite={false} fog={false} toneMapped={false} />
        </mesh>
      ))}
    </group>
  );
};

/** Raios de luz volumétricos (planos aditivos) — observado no canal (god rays + poeira). */
export const Shafts: React.FC<{ t: number; at: [number, number, number]; yaw?: number; n?: number; color?: string; strength?: number }> = ({ t, at, yaw = 0.5, n = 5, color = '#ffd89a', strength = 1 }) => {
  const tex = rayTex();
  return (
    <group position={at} rotation={[0, yaw, 0]}>
      {Array.from({ length: n }, (_, i) => (
        <mesh key={i} position={[i * 2.6 - n * 1.3, 8, -i * 0.6]} rotation={[0, 0, 0.42]} scale={[1.8 + (i % 3) * 1.2, 22, 1]}>
          <planeGeometry args={[1, 1]} /><meshBasicMaterial map={tex} color={color} transparent opacity={(0.2 + 0.1 * Math.sin(t * 0.8 + i * 1.7)) * strength} blending={THREE.AdditiveBlending} depthWrite={false} fog={false} toneMapped={false} />
        </mesh>
      ))}
    </group>
  );
};

export const Dust: React.FC<{ t: number; center: [number, number, number]; n?: number; span?: number; color?: string }> = ({ t, center, n = 70, span = 9, color = '#fff0c8' }) => {
  const ref = useRef<THREE.InstancedMesh>(null!); const tex = dotTex();
  const data = useMemo(() => { const r = rng(55); return Array.from({ length: n }, () => ({ x: r(), y: r(), z: r(), s: 0.03 + r() * 0.06, ph: r() * 6, sp: 0.15 + r() * 0.2 })); }, [n]);
  useLayoutEffect(() => {
    const m = new THREE.Object3D();
    data.forEach((d, i) => { const y = (((d.y + t * d.sp * 0.1) % 1) + 1) % 1; m.position.set(center[0] + (d.x - 0.5) * span + Math.sin(t * 0.6 + d.ph) * 0.4, center[1] + y * span * 0.6, center[2] + (d.z - 0.7) * span); m.scale.setScalar(d.s * (0.6 + 0.4 * Math.sin(t * 2 + d.ph))); m.updateMatrix(); ref.current.setMatrixAt(i, m.matrix); });
    ref.current.instanceMatrix.needsUpdate = true;
  });
  return <instancedMesh ref={ref} args={[undefined, undefined, n]} frustumCulled={false}><planeGeometry args={[1, 1]} /><meshBasicMaterial map={tex} color={color} transparent blending={THREE.AdditiveBlending} depthWrite={false} toneMapped={false} fog={false} /></instancedMesh>;
};

export const Tufts: React.FC<{ n: number; area: [number, number, number, number]; y?: number; color: string; color2?: string; seed?: number; sway?: number; t?: number; h?: number }> = ({ n, area, y = 0, color, color2, seed = 1, sway = 0, t = 0, h = 1 }) => {
  const ref = useRef<THREE.InstancedMesh>(null!);
  const data = useMemo(() => { const r = rng(seed); return Array.from({ length: n }, () => ({ x: area[0] + r() * (area[1] - area[0]), z: area[2] + r() * (area[3] - area[2]), s: (0.16 + r() * 0.34) * h, ry: r() * 6, ph: r() * 6, c: r() })); }, [n, seed, area[0], area[1], area[2], area[3], h]);
  useLayoutEffect(() => {
    const m = new THREE.Object3D(); const c1 = new THREE.Color(color), c2 = new THREE.Color(color2 ?? color), c = new THREE.Color();
    data.forEach((d, i) => { m.position.set(d.x, y + d.s * 0.6, d.z); m.rotation.set(0, d.ry, Math.sin(t * 1.7 + d.ph + d.x * 0.3) * sway); m.scale.set(d.s * 0.32, d.s * 1.5, d.s * 0.32); m.updateMatrix(); ref.current.setMatrixAt(i, m.matrix); c.copy(c1).lerp(c2, d.c); ref.current.setColorAt(i, c); });
    ref.current.instanceMatrix.needsUpdate = true; if (ref.current.instanceColor) ref.current.instanceColor.needsUpdate = true;
  });
  return <instancedMesh ref={ref} args={[undefined, undefined, n]}><coneGeometry args={[0.5, 1, 4]} /><Toon color="#ffffff" /></instancedMesh>;
};

export const Shadow: React.FC<{ p: [number, number, number]; s: [number, number]; o?: number }> = ({ p, s, o = 0.35 }) => (
  <mesh position={p} rotation={[-Math.PI / 2, 0, 0]} scale={[s[0], s[1], 1]}><circleGeometry args={[1, 24]} /><meshBasicMaterial color="#3d2f5c" transparent opacity={o} depthWrite={false} /></mesh>
);

/** Bandeira ondulando (vértices em função de t). */
export const Flag: React.FC<{ tex: THREE.Texture; t: number; w?: number; h?: number; amp?: number; phase?: number }> = ({ tex, t, w = 4, h = 2.5, amp = 0.35, phase = 0 }) => {
  const geo = useMemo(() => new THREE.PlaneGeometry(w, h, 12, 6), [w, h]);
  useLayoutEffect(() => {
    const p = geo.attributes.position;
    for (let i = 0; i < p.count; i++) { const u = (p.getX(i) + w / 2) / w; p.setZ(i, Math.sin(u * 7 - t * 5.2 + phase) * amp * u + Math.sin(u * 3 - t * 2.1) * amp * 0.4 * u); p.setY(i, p.getY(i) + Math.sin(u * 5 - t * 4 + phase) * 0.06 * u); }
    p.needsUpdate = true;
  });
  return <mesh geometry={geo} position={[w / 2, 0, 0]}><meshBasicMaterial map={tex} side={THREE.DoubleSide} toneMapped={false} /></mesh>;
};
export const FlagPole: React.FC<{ p: [number, number, number]; h?: number; tex: THREE.Texture; t: number; phase?: number; flip?: boolean }> = ({ p, h = 10, tex, t, phase = 0, flip }) => (
  <group position={p}>
    <mesh position={[0, h / 2, 0]}><cylinderGeometry args={[0.12, 0.16, h, 8]} /><Toon color="#c9b48a" /></mesh>
    <mesh position={[0, h + 0.1, 0]}><sphereGeometry args={[0.22, 10, 8]} /><meshBasicMaterial color="#f0c250" /></mesh>
    <group position={[0.1, h - 1.4, 0]} scale={[flip ? -1 : 1, 1, 1]}><Flag tex={tex} t={t} phase={phase} /></group>
  </group>
);

export const Puff: React.FC<{ p: [number, number, number]; t: number; t0: number; dur?: number; r?: number; color?: string; rise?: number; drift?: [number, number] }> = ({ p, t, t0, dur = 1.6, r = 0.6, color = '#f4f1f4', rise = 2.4, drift = [0.6, 0] }) => {
  const u = (t - t0) / dur; if (u < 0 || u > 1) return null;
  return <mesh position={[p[0] + drift[0] * u * 2, p[1] + rise * u, p[2] + drift[1] * u]} scale={r * (0.5 + 1.6 * Math.sqrt(u))}><sphereGeometry args={[1, 12, 10]} /><meshBasicMaterial color={color} transparent opacity={0.85 * (1 - u)} depthWrite={false} toneMapped={false} /></mesh>;
};
export const MuzzleFlash: React.FC<{ p: [number, number, number]; t: number; t0: number; s?: number; rot?: number }> = ({ p, t, t0, s = 1, rot = 0 }) => {
  const u = (t - t0) / 0.16; if (u < 0 || u > 1) return null;
  return (
    <group position={p} rotation={[0, 0, rot]} scale={s * (1.1 - u * 0.5)}>
      <mesh rotation={[0, 0, u * 1.4]}><circleGeometry args={[1.35, 8]} /><meshBasicMaterial color="#ff9a2a" toneMapped={false} depthWrite={false} /></mesh>
      <mesh rotation={[0, 0, -u]} position={[0, 0, 0.01]}><circleGeometry args={[0.85, 6]} /><meshBasicMaterial color="#ffe27a" toneMapped={false} depthWrite={false} /></mesh>
      <mesh position={[0, 0, 0.02]}><circleGeometry args={[0.4, 12]} /><meshBasicMaterial color="#ffffff" toneMapped={false} depthWrite={false} /></mesh>
    </group>
  );
};
