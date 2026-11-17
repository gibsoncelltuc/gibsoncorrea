// Teste de Veiculos -- GERADO por mkvideo.py a partir de videos/teste_veiculos/beats.json (edite o beats.json, nao este arquivo)
const X = 12000, DK = 6;
const WS = (i, off = 0) => TIMING.words[Math.min(i, TIMING.words.length - 1)][0] + off;   // frame em que a palavra de indice i comeca
const A = [0, WS(8, -3), WS(17, -3), TOTAL_F()];
const SPEC = {
  id: "teste_veiculos", exp: 1.0, total: TOTAL_F(), sets: ["street"], setx: { street: X },
  outfits: { CID: (v = 0, e = {}) => ({ _id: "cid", jacket: "#3b6fb5", pants: "#2d3550", boots: "#2a2218", hat: "hair", hair: "#4a3020", skin: ["#ffe2c2", "#f5c9a0", "#ecd0b6", "#c99067"][v % 4], ...(v % 7 === 4 ? { glasses: true } : {}), ...(v % 7 === 5 || v % 7 === 6 ? { beard: ['#3a2a1f', '#6b4a2a', '#8a8a86'][v % 3] } : {}), ...e }),
    SOL: (v = 0, e = {}) => ({ _id: "sol", jacket: "#6f7a3d", pants: "#5d6733", boots: "#2a2218", hat: "cap", cap: "#5d6733", rifle: true, skin: ["#ffe2c2", "#f5c9a0", "#ecd0b6", "#c99067"][v % 4], ...(v % 7 === 4 ? { glasses: true } : {}), ...(v % 7 === 5 || v % 7 === 6 ? { beard: ['#3a2a1f', '#6b4a2a', '#8a8a86'][v % 3] } : {}), ...e }) },
  assets: ["vehicles/car", "vehicles/jeep", "vehicles/taxi", "vehicles/truck"],
  kicks: [], flashes: [],
  shots: [
    { ...S('b0', A[0], A[1] - 1, X, "golden", { h: 2.3, d0: 7.0, d1: 5.8, hero: { hero: 'none' }, actors: [{ outfit: "CID", v: 0, at: [X + -2.648, 3.132], move: [[X + 3.352, 3.132], A[0], A[1] - 1, 'lin'], pose: 'stand', acting: 'low', expr: "smile", s: 0.62, y: 0.3, crop: 0.4, flip: false }], props: [{ asset: "vehicles/car", at: [X + -3, 1.5], move: [[X + 3, 1.5], A[0], A[1] - 1, 'lin'], s: 1.6, bob: 0.03 }] }), cam: [{ f: A[0], at: [X + -3, DK + 1.9, 1.5], d: 18, az: 12, el: 7, fov: 40 }, { f: A[1] - 1, at: [X + 3, DK + 1.9, 1.5], d: 16.2, az: -10, el: 8, fov: 40, ease: 'lin' }], nocut: true },
    { ...S('b1', A[1], A[2] - 1, X, "golden", { h: 2.3, d0: 7.0, d1: 5.8, hero: { hero: 'none' }, actors: [{ outfit: "CID", v: 5, at: [X + 2.648, 3.132], move: [[X + -3.352, 3.132], A[1], A[2] - 1, 'lin'], pose: 'stand', acting: 'low', expr: "stern", s: 0.62, y: 0.3, crop: 0.4, flip: true }], props: [{ asset: "vehicles/taxi", at: [X + 3, 1.5], move: [[X + -3, 1.5], A[1], A[2] - 1, 'lin'], s: 1.6, bob: 0.03 }] }), cam: [{ f: A[1], at: [X + 3, DK + 1.9, 1.5], d: 18, az: -12, el: 7, fov: 40 }, { f: A[2] - 1, at: [X + -3, DK + 1.9, 1.5], d: 16.2, az: 10, el: 8, fov: 40, ease: 'lin' }], nocut: true },
    { ...S('b2', A[2], A[3] - 1, X, "golden", { h: 2.3, d0: 7.0, d1: 5.8, hero: { hero: 'none' }, actors: [{ outfit: "SOL", v: 0, at: [X + -1.648, 3.132], move: [[X + 2.352, 3.132], A[2], A[3] - 1, 'lin'], pose: 'stand', acting: 'low', expr: "stern", s: 0.62, y: 0.3, crop: 0.4, flip: false }], props: [{ asset: "vehicles/jeep", at: [X + -2, 1.5], move: [[X + 2, 1.5], A[2], A[3] - 1, 'lin'], s: 1.6, bob: 0.03 }, { asset: "vehicles/truck", at: [X + 1.0, -3.5], s: 1.0, ry: 1.2 }] }), cam: [{ f: A[2], at: [X + -2, DK + 1.9, 1.5], d: 18, az: 12, el: 7, fov: 40 }, { f: A[3] - 1, at: [X + 2, DK + 1.9, 1.5], d: 16.2, az: -10, el: 8, fov: 40, ease: 'lin' }], nocut: true }
  ],
};
