import React, { useLayoutEffect, useMemo, useRef } from 'react';
import * as THREE from 'three';
import { INK } from '../characters/Rig';

const stadium = (w: number, h: number) => { const r = w / 2, hh = Math.max(0, (h - w) / 2), s = new THREE.Shape(); s.absarc(0, hh, r, 0, Math.PI, false); s.lineTo(-r, -hh); s.absarc(0, -hh, r, Math.PI, Math.PI * 2, false); s.closePath(); return new THREE.ShapeGeometry(s, 16); };
const MBm = (c: string) => <meshBasicMaterial color={c} toneMapped={false} />;

/** Bloco de soldados marchando (InstancedMesh) — "multidão de cabecinhas" observada no canal. Determinístico em t. */
export const Soldiers: React.FC<{ t: number; xc: number; z: number; cols?: number; rows?: number }> = ({ t, xc, z, cols = 8, rows = 5 }) => {
  const N = cols * rows;
  const r = { headO: useRef<THREE.InstancedMesh>(null!), headF: useRef<THREE.InstancedMesh>(null!), kepi: useRef<THREE.InstancedMesh>(null!), bodyO: useRef<THREE.InstancedMesh>(null!), body: useRef<THREE.InstancedMesh>(null!),
    belt: useRef<THREE.InstancedMesh>(null!), legO: useRef<THREE.InstancedMesh>(null!), leg: useRef<THREE.InstancedMesh>(null!), gun: useRef<THREE.InstancedMesh>(null!), lid: useRef<THREE.InstancedMesh>(null!), mouth: useRef<THREE.InstancedMesh>(null!) };
  const gBodyO = useMemo(() => stadium(1.0, 1.5), []), gBody = useMemo(() => stadium(0.9, 1.4), []);
  useLayoutEffect(() => {
    const o = new THREE.Object3D(); const set = (m: THREE.InstancedMesh, i: number) => { o.updateMatrix(); m.setMatrixAt(i, o.matrix); };
    for (let c = 0; c < cols; c++) for (let rw = 0; rw < rows; rw++) {
      const i = c * rows + rw, x = xc + (c - (cols - 1) / 2) * 2.7 + (rw % 2) * 0.3, zz = z - rw * 2.5;
      const ph = (t * 1.9 + ((i * 7) % 5) * 0.012) * Math.PI * 2, s = Math.sin(ph), cs = Math.cos(ph), bob = Math.abs(cs) * 0.07;
      const reset = () => { o.rotation.set(0, 0, 0); o.scale.set(1, 1, 1); };
      reset(); o.position.set(x, 3.17 + bob, zz); o.scale.set(0.6, 0.6, 1); set(r.headO.current, i);
      reset(); o.position.set(x + 0.02, 3.2 + bob, zz + 0.02); o.scale.set(0.52, 0.52, 1); set(r.headF.current, i);
      reset(); o.position.set(x + 0.02, 3.72 + bob, zz + 0.04); o.rotation.set(0, 0, 0.06); o.scale.set(0.5, 0.3, 1); set(r.kepi.current, i);
      reset(); o.position.set(x, 1.93 + bob, zz - 0.02); set(r.bodyO.current, i);
      reset(); o.position.set(x, 1.93 + bob, zz); set(r.body.current, i);
      reset(); o.position.set(x, 1.93 + bob, zz + 0.03); o.rotation.set(0, 0, 0.7); o.scale.set(0.15, 1.15, 1); set(r.belt.current, i);
      for (let k = 0; k < 2; k++) {
        const a = (k ? -s : s) * 0.62, knee = Math.max(0, k ? cs : -cs) * 0.8;
        reset(); o.position.set(x + (k ? 0.2 : -0.2), 1.38 + bob, zz + (k ? 0.0 : -0.08)); o.rotation.set(0, 0, a); o.updateMatrix();
        const hip = o.matrix.clone(); const lower = new THREE.Matrix4().makeTranslation(0, -0.55, 0).multiply(new THREE.Matrix4().makeRotationZ(knee)).multiply(new THREE.Matrix4().makeTranslation(0, -0.55, 0));
        const m = hip.multiply(lower); r.legO.current.setMatrixAt(i * 2 + k, m); r.leg.current.setMatrixAt(i * 2 + k, m);
      }
      reset(); o.position.set(x + 0.55, 2.6 + bob, zz + 0.06); o.rotation.set(0, 0, -0.18); set(r.gun.current, i);
      for (let k = 0; k < 2; k++) { reset(); o.position.set(x + (k ? 0.2 : -0.2), 3.21 + bob, zz + 0.08); set(r.lid.current, i * 2 + k); }
      reset(); o.position.set(x, 2.96 + bob, zz + 0.08); set(r.mouth.current, i);
    }
    (Object.values(r) as React.MutableRefObject<THREE.InstancedMesh>[]).forEach((rf) => { rf.current.instanceMatrix.needsUpdate = true; });
  });
  return (
    <group>
      <instancedMesh ref={r.headO} args={[undefined, undefined, N]} frustumCulled={false}><circleGeometry args={[1, 24]} />{MBm(INK)}</instancedMesh>
      <instancedMesh ref={r.headF} args={[undefined, undefined, N]} frustumCulled={false}><circleGeometry args={[1, 24]} />{MBm('#fbf8ff')}</instancedMesh>
      <instancedMesh ref={r.kepi} args={[undefined, undefined, N]} frustumCulled={false}><circleGeometry args={[1, 16, 0, Math.PI]} />{MBm('#2f4f8a')}</instancedMesh>
      <instancedMesh ref={r.bodyO} args={[gBodyO, undefined, N]} frustumCulled={false}>{MBm(INK)}</instancedMesh>
      <instancedMesh ref={r.body} args={[gBody, undefined, N]} frustumCulled={false}>{MBm('#2f4f8a')}</instancedMesh>
      <instancedMesh ref={r.belt} args={[undefined, undefined, N]} frustumCulled={false}><planeGeometry args={[1, 1]} />{MBm('#f6f1e6')}</instancedMesh>
      <instancedMesh ref={r.legO} args={[undefined, undefined, N * 2]} frustumCulled={false}><capsuleGeometry args={[0.085, 1.1, 3, 6]} />{MBm(INK)}</instancedMesh>
      <instancedMesh ref={r.leg} args={[undefined, undefined, N * 2]} frustumCulled={false}><capsuleGeometry args={[0.045, 1.1, 3, 6]} />{MBm('#6c8fc8')}</instancedMesh>
      <instancedMesh ref={r.gun} args={[undefined, undefined, N]} frustumCulled={false}><boxGeometry args={[0.09, 3.4, 0.05]} />{MBm('#3a3550')}</instancedMesh>
      <instancedMesh ref={r.lid} args={[undefined, undefined, N * 2]} frustumCulled={false}><boxGeometry args={[0.2, 0.05, 0.01]} />{MBm(INK)}</instancedMesh>
      <instancedMesh ref={r.mouth} args={[undefined, undefined, N]} frustumCulled={false}><boxGeometry args={[0.16, 0.035, 0.01]} />{MBm(INK)}</instancedMesh>
    </group>
  );
};
