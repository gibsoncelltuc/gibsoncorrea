import React, { useLayoutEffect, useMemo, useRef } from 'react';
import * as THREE from 'three';
import { rng, mixHex, lerp, clamp, smoother } from '../lib/anim';
import { INK } from '../characters/Rig';

// ---------- Materiais toon (rampa de 4 passos: 168/206/236/255 — sombras nunca pretas) ----------
export const toonGrad = (() => {
  const d = new THREE.DataTexture(new Uint8Array([168, 206, 236, 255]), 4, 1, THREE.RedFormat);
  d.minFilter = d.magFilter = THREE.NearestFilter; d.needsUpdate = true; return d;
})();
export const Toon: React.FC<{ color: string; opacity?: number; emissive?: string }> = ({ color, opacity = 1, emissive }) => (
  <meshToonMaterial color={color} gradientMap={toonGrad} transparent={opacity < 1} opacity={opacity} emissive={emissive ?? '#000000'} />
);

// ---------- Ambiente (hora do dia / estação) ----------
export type Env = {
  top: string; mid: string; bot: string; sun: string; sunPos: [number, number, number]; sunI: number;
  hemiSky: string; hemiGround: string; hemiI: number; water: string; ground: string; foliage: string; fog: string; snow: number;
};
export const ENVS: Record<string, Env> = {
  dawn: { top: '#6c6fb0', mid: '#e39a8a', bot: '#ffd29a', sun: '#ffc27a', sunPos: [-30, 14, -40], sunI: 2.5, hemiSky: '#8a8fd0', hemiGround: '#7a5c86', hemiI: 1.1, water: '#6f87c6', ground: '#c9a46a', foliage: '#d69a45', fog: '#f0c6a0', snow: 0 },
  morning: { top: '#6fa5dc', mid: '#a9cdea', bot: '#f6dcae', sun: '#ffc27a', sunPos: [-18, 28, 20], sunI: 2.7, hemiSky: '#8fa3d8', hemiGround: '#80609a', hemiI: 1.0, water: '#5f8fc8', ground: '#d0aa6c', foliage: '#dca043', fog: '#e6d6c0', snow: 0 },
  autumn: { top: '#7a8ed0', mid: '#f0b080', bot: '#ffd8a0', sun: '#ffb468', sunPos: [24, 18, 18], sunI: 2.7, hemiSky: '#8a82c8', hemiGround: '#82568a', hemiI: 1.0, water: '#6a7fbf', ground: '#c89860', foliage: '#c9702e', fog: '#f0c8a0', snow: 0 },
  winter: { top: '#5b6aa8', mid: '#9ea6d4', bot: '#e0d4e6', sun: '#d8d0ff', sunPos: [-20, 20, 30], sunI: 2.0, hemiSky: '#8896d6', hemiGround: '#7a6aa6', hemiI: 1.25, water: '#7683b8', ground: '#ece6f2', foliage: '#b8a0b0', fog: '#d4cce4', snow: 1 },
  dusk: { top: '#3d3a78', mid: '#b4607e', bot: '#ffb070', sun: '#ff9f5e', sunPos: [34, 9, -30], sunI: 2.6, hemiSky: '#6a62b0', hemiGround: '#6a4a82', hemiI: 1.05, water: '#4d5aa6', ground: '#dcd2e8', foliage: '#9a7aa0', fog: '#d09ab0', snow: 1 },
  room: { top: '#e6c79a', mid: '#f1d6ae', bot: '#f6e2c0', sun: '#ffc27a', sunPos: [-10, 20, 25], sunI: 2.4, hemiSky: '#9ca4d8', hemiGround: '#8c6ca0', hemiI: 1.1, water: '#6f87c6', ground: '#d8b88e', foliage: '#d69a45', fog: '#f1d6ae', snow: 0 },
};
const ENV_KEYS = Object.keys(ENVS['dawn']) as (keyof Env)[];
export const mixEnv = (a: Env, b: Env, t: number): Env => {
  const o: any = {};
  for (const k of ENV_KEYS) {
    const va = a[k] as any, vb = b[k] as any;
    o[k] = typeof va === 'string' ? mixHex(va, vb, t) : Array.isArray(va) ? va.map((x: number, i: number) => lerp(x, vb[i], t)) : lerp(va, vb, t);
  }
  return o as Env;
};
export const envAt = (t: number, keysArr: [number, keyof typeof ENVS][]): Env => {
  if (t <= keysArr[0][0]) return ENVS[keysArr[0][1]];
  for (let i = 1; i < keysArr.length; i++) if (t <= keysArr[i][0]) return mixEnv(ENVS[keysArr[i - 1][1]], ENVS[keysArr[i][1]], smoother((t - keysArr[i - 1][0]) / (keysArr[i][0] - keysArr[i - 1][0])));
  return ENVS[keysArr[keysArr.length - 1][1]];
};

export const Lights: React.FC<{ env: Env; at?: [number, number, number] }> = ({ env, at = [0, 0, 0] }) => (
  <>
    <hemisphereLight args={[env.hemiSky, env.hemiGround, env.hemiI]} />
    <directionalLight color={env.sun} intensity={env.sunI} position={[at[0] + env.sunPos[0], at[1] + env.sunPos[1], at[2] + env.sunPos[2]]} />
    <directionalLight color="#7185c0" intensity={0.45} position={[at[0] + 20, at[1] + 6, at[2] + 15]} />
  </>
);

export const Sky: React.FC<{ env: Env; at?: [number, number, number]; sunDisc?: boolean }> = ({ env, at = [0, 0, 0], sunDisc = true }) => {
  const geo = useMemo(() => { const g = new THREE.SphereGeometry(160, 24, 16); g.setAttribute('color', new THREE.BufferAttribute(new Float32Array(g.attributes.position.count * 3), 3)); return g; }, []);
  useLayoutEffect(() => {
    const col = geo.attributes.color as THREE.BufferAttribute, pos = geo.attributes.position;
    const top = new THREE.Color(env.top), mid = new THREE.Color(env.mid), bot = new THREE.Color(env.bot), c = new THREE.Color();
    for (let i = 0; i < pos.count; i++) {
      const h = clamp(pos.getY(i) / 160 * 1.6 + 0.12, 0, 1);
      if (h < 0.4) c.copy(bot).lerp(mid, h / 0.4); else c.copy(mid).lerp(top, (h - 0.4) / 0.6);
      col.setXYZ(i, c.r, c.g, c.b);
    }
    col.needsUpdate = true;
  });
  const s = env.sunPos; const n = Math.hypot(...s);
  return (
    <group position={at}>
      <mesh geometry={geo}><meshBasicMaterial vertexColors side={THREE.BackSide} fog={false} /></mesh>
      {sunDisc && (
        <group position={[(s[0] / n) * 140, (s[1] / n) * 140, (s[2] / n) * 140]}>
          <mesh lookAt={undefined as any}><circleGeometry args={[14, 32]} /><meshBasicMaterial color={env.sun} transparent opacity={0.28} fog={false} /></mesh>
          <mesh position={[0, 0, 0.1]}><circleGeometry args={[7, 32]} /><meshBasicMaterial color="#fff0c8" fog={false} /></mesh>
        </group>
      )}
    </group>
  );
};

export const Clouds: React.FC<{ t: number; at?: [number, number, number]; tint?: string; seed?: number; z?: number }> = ({ t, at = [0, 0, 0], tint = '#fff0e0', seed = 4, z = -110 }) => {
  const items = useMemo(() => { const r = rng(seed); return Array.from({ length: 9 }, () => ({ x: (r() - 0.5) * 260, y: 28 + r() * 30, s: 8 + r() * 10, sp: 0.4 + r() * 0.5 })); }, [seed]);
  return (
    <group position={[at[0], at[1], at[2] + z]}>
      {items.map((c, i) => (
        <group key={i} position={[((c.x + t * c.sp + 130) % 260) - 130, c.y, 0]} scale={[c.s, c.s * 0.34, 1]}>
          {[[-0.8, 0, 0.8], [0, 0.25, 1.1], [0.9, 0, 0.8]].map((b, j) => <mesh key={j} position={[b[0], b[1], 0]} scale={b[2]}><circleGeometry args={[1, 20]} /><meshBasicMaterial color={tint} transparent opacity={0.85} fog={false} /></mesh>)}
        </group>
      ))}
    </group>
  );
};

// ---------- Props ----------
const Box: React.FC<{ p: [number, number, number]; s: [number, number, number]; c: string; r?: [number, number, number] }> = ({ p, s, c, r }) => (
  <mesh position={p} scale={s} rotation={r}><boxGeometry args={[1, 1, 1]} /><Toon color={c} /></mesh>
);
export const WOOD = '#b9743e';
export const Chair: React.FC<{ c?: string }> = ({ c = WOOD }) => (
  <group>
    <Box p={[0, 0.5, 0]} s={[0.7, 0.1, 0.7]} c={c} />
    <Box p={[0, 0.95, -0.3]} s={[0.7, 0.8, 0.09]} c={c} />
    {[[-0.3, -0.3], [0.3, -0.3], [-0.3, 0.3], [0.3, 0.3]].map((l, i) => <Box key={i} p={[l[0], 0.22, l[1]]} s={[0.09, 0.5, 0.09]} c={c} />)}
  </group>
);
export const Table: React.FC<{ c?: string }> = ({ c = '#c48650' }) => (
  <group>
    <Box p={[0, 0.8, 0]} s={[1.9, 0.12, 1.1]} c={c} />
    {[[-0.8, -0.4], [0.8, -0.4], [-0.8, 0.4], [0.8, 0.4]].map((l, i) => <Box key={i} p={[l[0], 0.4, l[1]]} s={[0.12, 0.8, 0.12]} c={c} />)}
  </group>
);
export const Bed: React.FC = () => (
  <group>
    <Box p={[0, 0.3, 0]} s={[2.2, 0.35, 1.3]} c="#a4663a" />
    <Box p={[0, 0.55, 0.05]} s={[2.0, 0.22, 1.1]} c="#d96a5a" />
    <Box p={[-0.8, 0.72, 0.05]} s={[0.55, 0.16, 0.8]} c="#f6ecd8" />
    <Box p={[-1.12, 0.7, 0]} s={[0.1, 0.9, 1.3]} c="#a4663a" />
  </group>
);
export const Door: React.FC = () => (
  <group>
    <Box p={[0, 1.0, 0]} s={[1.0, 2.0, 0.12]} c="#8c5a3a" />
    <Box p={[0, 1.0, 0.07]} s={[0.8, 0.8, 0.02]} c="#a36e46" />
    <mesh position={[0.32, 1.0, 0.1]}><sphereGeometry args={[0.07, 10, 8]} /><meshBasicMaterial color="#f0c56a" /></mesh>
  </group>
);
export const FURN = [Chair, Table, Bed, Door, Chair, Chair, Table];

export const Tree: React.FC<{ p: [number, number, number]; s?: number; leaf: string; snow?: number }> = ({ p, s = 1, leaf, snow = 0 }) => (
  <group position={p} scale={s}>
    <mesh position={[0, 1.1, 0]}><cylinderGeometry args={[0.25, 0.36, 2.2, 6]} /><Toon color="#8a5a48" /></mesh>
    <mesh position={[0, 3.3, 0]}><coneGeometry args={[1.9, 3.2, 7]} /><Toon color={mixHex(leaf, '#ffffff', snow * 0.8)} /></mesh>
    <mesh position={[0, 4.9, 0]}><coneGeometry args={[1.35, 2.4, 7]} /><Toon color={mixHex(mixHex(leaf, '#f0b24a', 0.25), '#ffffff', snow * 0.85)} /></mesh>
  </group>
);
export const Mountain: React.FC<{ p: [number, number, number]; r: number; h: number; c: string; snow?: number }> = ({ p, r, h, c, snow = 0 }) => (
  <group position={p}>
    <mesh position={[0, h / 2, 0]}><coneGeometry args={[r, h, 6]} /><Toon color={c} /></mesh>
    <mesh position={[0, h * 0.86, 0]}><coneGeometry args={[r * 0.24, h * 0.28, 6]} /><Toon color={mixHex('#f2eef8', c, 1 - 0.55 - snow * 0.3)} /></mesh>
  </group>
);
export const House: React.FC<{ p: [number, number, number]; w?: number; h?: number; wall: string; roof: string; snow?: number; lit?: number }> = ({ p, w = 5, h = 3.4, wall, roof, snow = 0, lit = 0 }) => (
  <group position={p}>
    <Box p={[0, h / 2, 0]} s={[w, h, w * 0.8]} c={wall} />
    <mesh position={[0, h + 1.1, 0]} rotation={[0, Math.PI / 4, 0]} scale={[1, 1, 0.8]}><coneGeometry args={[w * 0.78, 2.4, 4]} /><Toon color={mixHex(roof, '#ffffff', snow * 0.7)} /></mesh>
    <Box p={[0, 1.0, w * 0.4 + 0.02]} s={[0.9, 1.8, 0.05]} c="#6a4a3a" />
    <Box p={[w * 0.28, 2.0, w * 0.4 + 0.03]} s={[0.9, 0.9, 0.05]} c={lit ? '#ffd68a' : '#7f9ccc'} />
  </group>
);

export const Tufts: React.FC<{ n: number; area: [number, number, number, number]; y?: number; color: string; seed?: number; sway?: number; t?: number }> = ({ n, area, y = 0, color, seed = 1, sway = 0, t = 0 }) => {
  const ref = useRef<THREE.InstancedMesh>(null!);
  const data = useMemo(() => { const r = rng(seed); return Array.from({ length: n }, () => ({ x: area[0] + r() * (area[1] - area[0]), z: area[2] + r() * (area[3] - area[2]), s: 0.18 + r() * 0.35, ry: r() * 6, ph: r() * 6 })); }, [n, seed, area[0], area[1], area[2], area[3]]);
  useLayoutEffect(() => {
    const m = new THREE.Object3D();
    data.forEach((d, i) => { m.position.set(d.x, y + d.s * 0.5, d.z); m.rotation.set(0, d.ry, Math.sin(t * 1.6 + d.ph) * sway); m.scale.set(d.s, d.s * 1.4, d.s); m.updateMatrix(); ref.current.setMatrixAt(i, m.matrix); });
    ref.current.instanceMatrix.needsUpdate = true;
  });
  return <instancedMesh ref={ref} args={[undefined, undefined, n]}><coneGeometry args={[0.5, 1, 4]} /><Toon color={color} /></instancedMesh>;
};

export const Snow: React.FC<{ t: number; amount: number; at: [number, number, number]; span?: [number, number, number] }> = ({ t, amount, at, span = [40, 18, 30] }) => {
  const N = 260; const ref = useRef<THREE.InstancedMesh>(null!);
  const data = useMemo(() => { const r = rng(77); return Array.from({ length: N }, () => ({ x: r(), y: r(), z: r(), sp: 0.5 + r() * 0.6, ph: r() * 6, s: 0.05 + r() * 0.07 })); }, []);
  useLayoutEffect(() => {
    const m = new THREE.Object3D();
    data.forEach((d, i) => {
      const y = (((d.y - t * 0.07 * d.sp) % 1) + 1) % 1;
      m.position.set(at[0] + (d.x - 0.5) * span[0] + Math.sin(t * 0.8 + d.ph) * 0.6, at[1] + y * span[1], at[2] + (d.z - 0.7) * span[2]);
      m.scale.setScalar(d.s * (i / N < amount ? 1 : 0)); m.updateMatrix(); ref.current.setMatrixAt(i, m.matrix);
    });
    ref.current.instanceMatrix.needsUpdate = true;
  });
  return <instancedMesh ref={ref} args={[undefined, undefined, N]}><circleGeometry args={[1, 8]} /><meshBasicMaterial color="#ffffff" fog={false} /></instancedMesh>;
};

export const Ripple: React.FC<{ p: [number, number, number]; age: number }> = ({ p, age }) => {
  if (age < 0 || age > 1.6) return null;
  return (
    <group position={[p[0], p[1] + 0.03, p[2]]} rotation={[-Math.PI / 2, 0, 0]}>
      {[0, 0.22, 0.44].map((d, i) => { const a = age - d; if (a < 0) return null; const r = 0.3 + a * 2.4; return (
        <mesh key={i}><ringGeometry args={[r, r + 0.12, 32]} /><meshBasicMaterial color="#ffffff" transparent opacity={clamp(1 - a / 1.2) * 0.85} depthWrite={false} /></mesh>); })}
    </group>
  );
};
export const Droplets: React.FC<{ p: [number, number, number]; age: number }> = ({ p, age }) => {
  if (age < 0 || age > 1.0) return null;
  const r = rng(31);
  return (
    <group position={p}>
      {Array.from({ length: 12 }, (_, i) => { const a = r() * Math.PI * 2, sp = 1.2 + r() * 2.2, vy = 3.5 + r() * 3.5; const y = vy * age - 9.8 * 0.5 * age * age; if (y < -0.05) return null;
        return <mesh key={i} position={[Math.cos(a) * sp * age * 0.6, y, Math.sin(a) * sp * age * 0.4]} scale={0.09 * (1 - age * 0.5)}><sphereGeometry args={[1, 8, 6]} /><meshBasicMaterial color="#ffffff" /></mesh>; })}
    </group>
  );
};

export const Shadow: React.FC<{ p: [number, number, number]; s: [number, number]; o?: number }> = ({ p, s, o = 0.35 }) => (
  <mesh position={p} rotation={[-Math.PI / 2, 0, 0]} scale={[s[0], s[1], 1]}><circleGeometry args={[1, 24]} /><meshBasicMaterial color="#3d2f5c" transparent opacity={o} depthWrite={false} /></mesh>
);
export { INK };
