// river
const waterU = { t: { value: 0 }, deep: { value: new THREE.Color('#2f6f8f') }, shal: { value: new THREE.Color('#5fa8bf') }, glint: { value: new THREE.Color('#e9f6ff') } };
const waterMat = new THREE.ShaderMaterial({
  uniforms: { ...THREE.UniformsUtils.clone(THREE.UniformsLib.fog), ...waterU }, fog: true,
  vertexShader: `#include <fog_pars_vertex>
    varying vec3 vW; void main(){ vec4 w = modelMatrix*vec4(position,1.); vW = w.xyz; vec4 mvPosition = viewMatrix*w; gl_Position = projectionMatrix*mvPosition;
    #include <fog_vertex>
    }`,
  fragmentShader: `#include <fog_pars_fragment>
    uniform float t; uniform vec3 deep, shal, glint; varying vec3 vW;
    float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1,311.7)))*43758.5453); }
    float noise(vec2 p){ vec2 i=floor(p), f=fract(p); f=f*f*(3.-2.*f); return mix(mix(hash(i),hash(i+vec2(1,0)),f.x), mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),f.x), f.y); }
    void main(){ vec2 p = vW.xz*vec2(.35,.12) + vec2(0., -t*.25);
      float n = noise(p) * .6 + noise(p*2.3 + 7.) * .4; float edge = smoothstep(10., 17., abs(vW.x));
      vec3 c = mix(deep, shal, .35 + .4*n + .4*edge);
      float streak = smoothstep(.72, .78, noise(vW.xz*vec2(.8,.09) + vec2(0., -t*.6))) * (1.-edge*.5);
      c = mix(c, glint, streak*.75);
      gl_FragColor = vec4(c,1.);
      #include <fog_fragment>
    }`,
});
const water = new THREE.Mesh(new THREE.PlaneGeometry(60, 2300), waterMat); water.rotation.x = -Math.PI / 2; water.position.y = 0;
water.userData.nd = waterNd; water.receiveShadow = false; scene.add(water);
