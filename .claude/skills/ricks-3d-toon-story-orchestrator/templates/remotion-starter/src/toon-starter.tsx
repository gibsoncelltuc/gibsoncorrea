import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { ThreeCanvas } from '@remotion/three';

const Character: React.FC<{ frame: number }> = ({ frame }) => {
  const bob = Math.sin(frame * 0.09) * 0.035;
  const sway = Math.sin(frame * 0.045) * 0.035;
  const blink = Math.sin(frame * 0.021) > 0.985;

  return (
    <group position={[-0.15, -0.25 + bob, 0.2]} rotation={[0, sway, 0]}>
      {/* Legs: black stroke under colored legs */}
      <mesh position={[-0.16, 0.28, 0]} rotation={[0, 0, -0.06]}>
        <cylinderGeometry args={[0.045, 0.055, 0.58, 12]} />
        <meshBasicMaterial color="#191827" />
      </mesh>
      <mesh position={[0.16, 0.28, 0]} rotation={[0, 0, 0.06]}>
        <cylinderGeometry args={[0.045, 0.055, 0.58, 12]} />
        <meshBasicMaterial color="#191827" />
      </mesh>
      {/* Torso as simple 2D cut-out */}
      <mesh position={[0, 0.82, 0.02]} scale={[0.44, 0.62, 1]}>
        <circleGeometry args={[0.52, 40]} />
        <meshBasicMaterial color="#191827" />
      </mesh>
      <mesh position={[0, 0.84, 0.04]} scale={[0.39, 0.56, 1]}>
        <circleGeometry args={[0.52, 40]} />
        <meshBasicMaterial color="#B9574E" />
      </mesh>
      {/* Arms */}
      <mesh position={[-0.43, 0.92, 0.02]} rotation={[0, 0, -0.42]}>
        <cylinderGeometry args={[0.045, 0.045, 0.62, 12]} />
        <meshBasicMaterial color="#191827" />
      </mesh>
      <mesh position={[0.43, 0.92, 0.02]} rotation={[0, 0, 0.42]}>
        <cylinderGeometry args={[0.045, 0.045, 0.62, 12]} />
        <meshBasicMaterial color="#191827" />
      </mesh>
      {/* Head outline and face */}
      <mesh position={[0, 1.75, 0.08]} scale={[1.0, 1.0, 1]}>
        <circleGeometry args={[0.61, 64]} />
        <meshBasicMaterial color="#191827" />
      </mesh>
      <mesh position={[0, 1.75, 0.10]} scale={[0.94, 0.94, 1]}>
        <circleGeometry args={[0.61, 64]} />
        <meshBasicMaterial color="#F4EBDD" />
      </mesh>
      {/* Eyes */}
      {[-0.19, 0.19].map((x) => (
        <mesh key={x} position={[x, 1.82, 0.13]} scale={[1, blink ? 0.1 : 1, 1]}>
          <circleGeometry args={[0.055, 24]} />
          <meshBasicMaterial color="#191827" />
        </mesh>
      ))}
      {/* Small open mouth */}
      <mesh position={[0.02, 1.57, 0.135]}>
        <circleGeometry args={[0.07, 24]} />
        <meshBasicMaterial color="#191827" />
      </mesh>
    </group>
  );
};

const Set: React.FC<{ frame: number }> = ({ frame }) => {
  const cloudX = interpolate(frame, [0, 1950], [-2.8, 2.8]);
  const treeTurn = Math.sin(frame * 0.025) * 0.05;

  return (
    <>
      <color attach="background" args={["#83B9E1"]} />
      <ambientLight intensity={0.85} />
      <directionalLight position={[-3, 6, 5]} intensity={2.2} color="#FFD8AC" />
      <directionalLight position={[4, 3, -4]} intensity={0.65} color="#7185C0" />

      {/* Ground */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.04, 0]}>
        <planeGeometry args={[30, 30]} />
        <meshStandardMaterial color="#8B8C9E" roughness={1} />
      </mesh>

      {/* Background architecture */}
      <mesh position={[-3.4, 1.35, -2.8]}>
        <boxGeometry args={[2.8, 3.0, 0.7]} />
        <meshStandardMaterial color="#B5A4A0" roughness={0.9} />
      </mesh>
      <mesh position={[3.1, 1.05, -3.1]}>
        <boxGeometry args={[2.5, 2.4, 0.7]} />
        <meshStandardMaterial color="#6E718F" roughness={0.95} />
      </mesh>
      <mesh position={[-3.4, 3.0, -2.42]}>
        <boxGeometry args={[0.55, 0.75, 0.08]} />
        <meshBasicMaterial color="#F8C58F" />
      </mesh>

      {/* Moving cloud */}
      <group position={[cloudX, 3.6, -4.2]}>
        <mesh position={[-0.35, 0, 0]} scale={[0.65, 0.22, 0.18]}>
          <sphereGeometry args={[1, 18, 12]} />
          <meshBasicMaterial color="#F5E8E1" />
        </mesh>
        <mesh position={[0.12, 0.08, 0]} scale={[0.38, 0.28, 0.18]}>
          <sphereGeometry args={[1, 18, 12]} />
          <meshBasicMaterial color="#F5E8E1" />
        </mesh>
      </group>

      {/* Tree silhouette with gentle sway */}
      <group position={[2.8, 0.2, -1.8]} rotation={[0, 0, treeTurn]}>
        <mesh position={[0, 0.75, 0]}>
          <cylinderGeometry args={[0.07, 0.12, 1.5, 8]} />
          <meshStandardMaterial color="#514A59" />
        </mesh>
        <mesh position={[0, 1.75, 0]}>
          <sphereGeometry args={[0.66, 16, 12]} />
          <meshStandardMaterial color="#4F7F7A" roughness={1} />
        </mesh>
      </group>

      <Character frame={frame} />
    </>
  );
};

export const ToonStarter: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const cameraX = interpolate(frame, [0, 65 * 30], [-0.45, 0.45]);
  const cameraZ = interpolate(frame, [0, 65 * 30], [10.5, 9.8]);

  return (
    <AbsoluteFill style={{ backgroundColor: '#83B9E1' }}>
      <ThreeCanvas
        width={width}
        height={height}
        camera={{ position: [cameraX, 1.2, cameraZ], fov: 34 }}
        style={{ width: '100%', height: '100%' }}
      >
        <Set frame={frame} />
      </ThreeCanvas>
      {/* Simple timed title card; replace with word-level caption component. */}
      <AbsoluteFill
        style={{
          justifyContent: 'flex-end',
          alignItems: 'center',
          paddingLeft: 90,
          paddingRight: 90,
          paddingBottom: 220,
          pointerEvents: 'none',
        }}
      >
        <div
          style={{
            color: '#FFFFFF',
            fontFamily: 'Arial, sans-serif',
            fontWeight: 900,
            fontSize: 82,
            lineHeight: 1.0,
            textAlign: 'center',
            WebkitTextStroke: '5px #191827',
            paintOrder: 'stroke fill',
            textShadow: '0 4px 0 #191827',
          }}
        >
          {frame < 65 * 30 ? 'A strange discovery' : ''}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
