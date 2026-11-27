// ---- ANIMAL CATALOG (2D, same inked/shaded card style as the cast). Side view, faces LEFT, soles at y=975.
// usage:  T.animalSide(p, { species: 'pig'|'cow'|'horse'|'sheep'|'goat'|'dog'|'cat'|'donkey', state: 'stand'|'root'|'trot'|'alert'|'fall', phase, down, blink, ear, tail, expr, fall, t, angel })
//         T.birdSide(p, { species: 'chicken'|'rooster'|'duck'|'goose'|'gull', state: 'stand'|'peck'|'walk'|'fly', phase, blink, t })
const AN = {
  pig:    { body: "#f7a8b8", shade: [0.84, 0.66, 0.74], belly: "#ffd0d9", dark: "#e58fa4", snout: "#f08aa0", nose: "#e8708a", ear: "pig", tail: "curl", hoof: "#efe0cc", sock: null, a: 228, b: 128, hipY: 790, kneeY: 868, legW: 44, neck: 78, head: { a: 96, b: 88, sn: 52, sh: 40 }, extra: "bristle" },
  cow:    { body: "#fbf7f0", shade: [0.82, 0.8, 0.88], belly: "#ffe3e8", dark: "#d8d2ca", snout: "#f4b6c0", nose: "#e8909e", ear: "cow", tail: "long", hoof: "#3a3238", sock: null, a: 245, b: 140, hipY: 770, kneeY: 860, legW: 46, neck: 92, head: { a: 92, b: 92, sn: 60, sh: 48 }, extra: "cowspots", horns: true, udder: true },
  bear:   { body: "#7a4e30", shade: [0.7, 0.6, 0.62], belly: "#8f6040", dark: "#5a361f", snout: "#a8764f", nose: "#2a1810", ear: "cow", tail: "stub", hoof: "#3a2418", sock: null, a: 235, b: 150, hipY: 770, kneeY: 860, legW: 54, neck: 84, head: { a: 92, b: 88, sn: 54, sh: 46 } },
  horse:  { body: "#a25f36", shade: [0.72, 0.62, 0.62], belly: "#b7774a", dark: "#7a4526", snout: "#8a4f2c", nose: "#3a2418", ear: "point", tail: "flow", hoof: "#3a2f2a", sock: "#f4eee4", a: 215, b: 105, hipY: 700, kneeY: 835, legW: 34, neck: 70, head: { a: 70, b: 98, sn: 92, sh: 40 }, mane: "#3a2418", tall: true },
  sheep:  { body: "#f6f2ea", shade: [0.82, 0.8, 0.9], belly: "#efe9dd", dark: "#d9d3c8", snout: "#3d343b", nose: "#2b2430", ear: "sheep", tail: "stub", hoof: "#2b2430", sock: null, a: 205, b: 120, hipY: 820, kneeY: 890, legW: 30, neck: 60, head: { a: 70, b: 72, sn: 40, sh: 34 }, wool: true, face: "#3d343b" },
  goat:   { body: "#efe3cf", shade: [0.8, 0.74, 0.8], belly: "#f7efe0", dark: "#cdbfa8", snout: "#e3d3ba", nose: "#4a3a30", ear: "goat", tail: "up", hoof: "#4a3a30", sock: null, a: 190, b: 100, hipY: 790, kneeY: 870, legW: 30, neck: 62, head: { a: 66, b: 74, sn: 44, sh: 30 }, horns: true, beard: true },
  dog:    { body: "#d49a5c", shade: [0.76, 0.66, 0.7], belly: "#f4e2c4", dark: "#a8703a", snout: "#e9c28f", nose: "#2b2430", ear: "floppy", tail: "wag", hoof: "#f4e2c4", sock: null, a: 170, b: 90, hipY: 800, kneeY: 880, legW: 28, neck: 54, head: { a: 70, b: 70, sn: 44, sh: 32 }, patch: "#f4e2c4" },
  cat:    { body: "#ec9a44", shade: [0.78, 0.62, 0.62], belly: "#fbe3c0", dark: "#c0702a", snout: "#fbe3c0", nose: "#f08aa0", ear: "pointcat", tail: "catlong", hoof: "#fbe3c0", sock: null, a: 150, b: 74, hipY: 840, kneeY: 905, legW: 24, neck: 46, head: { a: 62, b: 58, sn: 26, sh: 24 }, stripes: true, whiskers: true },
  donkey: { body: "#9a958f", shade: [0.74, 0.7, 0.78], belly: "#d8d2c8", dark: "#6e6a66", snout: "#e1dad0", nose: "#3a3330", ear: "long", tail: "tuft", hoof: "#3a3330", sock: null, a: 200, b: 100, hipY: 760, kneeY: 860, legW: 32, neck: 66, head: { a: 74, b: 84, sn: 70, sh: 36 }, mane: "#6e6a66" },
};

// animais sem desenho 2D proprio: derivados de um parecido, com cor e orelha certas (antes: travava com "hipY")
Object.assign(AN, {
  wolf:     { ...AN.dog, body: "#8a8f98", belly: "#d8dce2", dark: "#5f646c", snout: "#c9ccd2", ear: "pointcat", tail: "long" },
  fox:      { ...AN.dog, body: "#e0782a", belly: "#fbeede", dark: "#a8501a", snout: "#fbeede", ear: "pointcat", tail: "flow" },
  deer:     { ...AN.goat, body: "#b07a48", belly: "#efe0c8", dark: "#7e5530", snout: "#d9b48a", nose: "#2b2430", tail: "stub", horns: true },
  rabbit:   { ...AN.cat, body: "#e8e2da", belly: "#ffffff", dark: "#bdb4aa", snout: "#ffffff", ear: "long", tail: "stub" },
  lion:     { ...AN.dog, body: "#d9a24a", belly: "#f2d49a", dark: "#a8742c", snout: "#f2d49a", ear: "pointcat", tail: "tuft", a: 220, b: 118, mane: "#8a4f1c" },
  elephant: { ...AN.cow, body: "#9aa0a8", belly: "#b6bbc2", dark: "#70757c", snout: "#9aa0a8", nose: "#70757c", ear: "cow", tail: "tuft", udder: false, horns: false, extra: null },
});

export const animalSide = (p, o = {}) => {
  if ((o.species || "pig") === "pig") return pigToon(p, o);
  const A = AN[o.species || "pig"], g = p.g, light = o.light ?? rad(-120), thick = thickAngle(light), ow = 6.5;
  const { state = "stand", phase = 0, down = 0, blink = 0, ear = 0, tail = 0, expr = "normal", fall = 0, t = 0 } = o;
  const trot = state === "trot" ? 1 : 0, root = state === "root";
  const bob = trot * 7 * Math.cos(4 * Math.PI * phase) + (root ? 2.5 * Math.abs(Math.sin(t * 5.5)) : 0);
  const bodyC = [320, A.hipY - 48 + bob];
  g.save();
  if (fall > 0) { const ang = -fall * Math.PI * 0.96; g.translate(bodyC[0], bodyC[1]); g.rotate(ang); g.translate(-bodyC[0], -bodyC[1]); }
  p.rot = null;
  const legX = [bodyC[0] - A.a * 0.58, bodyC[0] - A.a * 0.32, bodyC[0] + A.a * 0.38, bodyC[0] + A.a * 0.62];
  const drawLeg = (x, ph, back) => {
    const sw = trot * Math.sin(2 * Math.PI * (phase + ph)) * 34, lift = trot * Math.max(0, Math.cos(2 * Math.PI * (phase + ph))) * 24;
    const hip = [x, A.hipY + bob], knee = [x + sw * 0.55 + (fall ? (x < 330 ? -30 : 30) : 0), A.kneeY + bob * 0.4 - lift * 0.6], foot = [x + sw + (fall ? (x < 330 ? -44 : 46) : 0), 958 - lift - (fall ? 30 : 0)];
    p.line([hip, knee, foot], back ? A.dark : A.body, A.legW - (back ? 4 : 0));
    if (A.sock) p.poly(rrect(foot[0] - A.legW * 0.5, foot[1] - 30, foot[0] + A.legW * 0.5, foot[1] + 8, 8), A.sock, 5);
    p.ell(foot[0] - 2, foot[1] + 8, A.legW * 0.55, 11, A.hoof, 4);
  };
  drawLeg(legX[1], 0.5, true); drawLeg(legX[3], 0, true);
  // tail
  const tb = [bodyC[0] + A.a - 12, bodyC[1] - 52];
  if (A.tail === "curl") { const pts = []; for (let i = 0; i <= 18; i++) { const a = i / 18 * 5.2 + tail, r = 20 - i * 0.8; pts.push([tb[0] + 8 + Math.cos(a) * r * (1 - i / 40) + i * 1.2, tb[1] - 40 - i * 2.2 + Math.sin(a) * r * 0.9]); } p.line(pts, A.body, 11); }
  if (A.tail === "long" || A.tail === "flow" || A.tail === "tuft") { const L = A.tail === "flow" ? 230 : 190; const sway = Math.sin(t * 3) * 14 + tail * 20; const pts = [[tb[0], tb[1] + 20], [tb[0] + 26 + sway * 0.3, tb[1] + L * 0.4], [tb[0] + 16 + sway, tb[1] + L * 0.85]]; p.line(pts, A.tail === "flow" ? A.mane : A.dark, A.tail === "flow" ? 22 : 9); p.ell(pts[2][0], pts[2][1] + 10, A.tail === "flow" ? 26 : 22, A.tail === "flow" ? 40 : 30, A.tail === "flow" ? A.mane : "#3a2f2a", 5); }
  if (A.tail === "stub") p.ell(tb[0] + 6, tb[1] + 16, 20, 26, A.body, 5);
  if (A.tail === "up") p.line([[tb[0], tb[1] + 20], [tb[0] + 22, tb[1] - 36], [tb[0] + 34, tb[1] - 46 + Math.sin(t * 6) * 4]], A.body, 14);
  if (A.tail === "wag") p.line([[tb[0], tb[1] + 20], [tb[0] + 34, tb[1] - 40 + Math.sin(t * 14) * 10], [tb[0] + 56, tb[1] - 84 + Math.sin(t * 14) * 18]], A.body, 16);
  if (A.tail === "catlong") p.line([[tb[0], tb[1] + 30], [tb[0] + 60, tb[1] + 10 + Math.sin(t * 3) * 8], [tb[0] + 92, tb[1] - 80], [tb[0] + 78 + Math.sin(t * 3) * 10, tb[1] - 150]], A.body, 16);
  // body
  const body = blobPts(bodyC[0], bodyC[1], { a: A.a, b: A.b, nTop: 2.4, nBot: 2.05, egg: 0.06, asym: -0.04, rot: 0, noise: A.wool ? 0.03 : 0.012, seed: 17 }, A.wool ? 120 : 90);
  p.gradFill(body, A.body, mul(A.body, A.shade), light, 0.2);
  p.clip(body, () => {
    p.ell(bodyC[0] - 20, bodyC[1] + A.b * 0.78, A.a * 0.92, A.b * 0.42, A.belly, 0);
    p.stroke([[bodyC[0] - A.a * 0.7, bodyC[1] - A.b * 0.8], [bodyC[0] - A.a * 0.3, bodyC[1] - A.b * 0.95], [bodyC[0] + A.a * 0.3, bodyC[1] - A.b * 0.93], [bodyC[0] + A.a * 0.8, bodyC[1] - A.b * 0.6]], 12, "#ffffff44");
    if (A.extra === "cowspots") { for (const [x, y, rx, ry] of [[-110, -40, 62, 48], [20, -70, 54, 40], [120, 10, 70, 54], [-30, 40, 40, 30]]) p.ell(bodyC[0] + x, bodyC[1] + y, rx, ry, "#2b2530", 0); }
    if (A.patch) p.ell(bodyC[0] + 40, bodyC[1] - 20, 58, 44, A.patch, 0);
    if (A.stripes) for (let i = 0; i < 6; i++) p.stroke([[bodyC[0] - 100 + i * 36, bodyC[1] - A.b], [bodyC[0] - 90 + i * 36, bodyC[1] - A.b * 0.2]], 8, A.dark);
    if (A.wool) for (let i = 0; i < 14; i++) p.ell(bodyC[0] - 190 + i * 28, bodyC[1] - A.b * 0.7 + (i % 3) * 14, 26, 22, "#ffffff55", 0);
  });
  p.inkRing(body, ow * 0.85, thick);
  if (A.wool) for (let i = 0; i < 16; i++) { const a = i / 16 * Math.PI * 2; if (Math.sin(a) < 0.2) p.ell(bodyC[0] + Math.cos(a) * A.a * 0.98, bodyC[1] + Math.sin(a) * A.b * 0.98, 26, 24, A.body, 4); }
  if (A.extra === "bristle") for (let i = 0; i < 9; i++) { const x = bodyC[0] - 130 + i * 38; p.poly([[x - 9, bodyC[1] - 120 + 2 * Math.abs(i - 4)], [x + 2, bodyC[1] - 144 + 2 * Math.abs(i - 4) + Math.sin(t * 6 + i) * 2], [x + 11, bodyC[1] - 118 + 2 * Math.abs(i - 4)]], "#d9728a", 3); }
  if (A.mane) { for (let i = 0; i < 7; i++) { const x = bodyC[0] - A.a * 0.8 + i * 16; p.poly([[x, bodyC[1] - A.b * 0.9], [x - 18 + Math.sin(t * 4 + i) * 5, bodyC[1] - A.b * 0.9 - 54], [x + 24, bodyC[1] - A.b * 0.85]], A.mane, 4); } }
  if (A.udder) p.ell(bodyC[0] + 90, bodyC[1] + A.b - 6, 34, 26, "#f4b6c0", 5);
  drawLeg(legX[0], 0, false); drawLeg(legX[2], 0.5, false);
  // neck + head
  const H = A.head, hd = (root ? 52 + 22 * Math.sin(t * 5.5) : state === "alert" ? -28 : state === "trot" ? -6 : 0) + down;
  const hx = bodyC[0] - A.a - (A.tall ? 40 : 10), hy = bodyC[1] - (A.tall ? 70 : 0) + hd;
  const neckPts = blobPts(bodyC[0] - A.a + 40, bodyC[1] - (A.tall ? 60 : 0) + hd * 0.5, { a: A.neck, b: A.tall ? 120 : 98, nTop: 2.2, nBot: 2.2, egg: 0, asym: 0, rot: A.tall ? rad(-24) : 0, noise: 0.01, seed: 3 }, 50);
  p.gradFill(neckPts, A.body, mul(A.body, A.shade), light, 0.2); p.inkRing(neckPts, ow * 0.7, thick);
  const head = blobPts(hx, hy, { a: H.a, b: H.b, nTop: 2.3, nBot: 2.0, egg: -0.1, asym: -0.04, rot: A.tall ? rad(24) : rad(-6), noise: 0.012, seed: 9 }, 70);
  const faceCol = A.face || A.body;
  p.gradFill(head, faceCol, mul(faceCol, A.shade), light, 0.2);
  const sn = blobPts(hx - H.a - H.sn * 0.5 + 12, hy + (A.tall ? 38 : 26), { a: H.sn, b: H.sh, nTop: 2.4, nBot: 2.2, egg: 0, asym: 0, rot: A.tall ? rad(12) : 0, noise: 0.008, seed: 5 }, 40);
  p.gradFill(sn, A.snout, mul(A.snout, [0.86, 0.8, 0.88]), light, 0.2); p.inkRing(sn, ow * 0.8, thick);
  if (A.ear === "pig" || A.species === "pig" || (o.species || "pig") === "pig") { const disc = blobPts(hx - H.a - H.sn * 0.9, hy + 24, { a: 16, b: 34, nTop: 2.2, nBot: 2.2, egg: 0, asym: 0, rot: 0, noise: 0, seed: 6 }, 24); p.poly(disc, A.nose, 5); p.ell(hx - H.a - H.sn - 4, hy + 12, 5, 9, INK, 0); p.ell(hx - H.a - H.sn - 4, hy + 36, 5, 9, INK, 0); }
  else p.ell(hx - H.a - H.sn + 18, hy + (A.tall ? 44 : 22), 9, 11, A.nose, 0);
  p.inkRing(head, ow * 0.85, thick);
  p.stroke([[hx - H.a + 4, hy + 56], [hx - H.a + 36, hy + 62], [hx - H.a + 68, hy + 52]], 4, INK);
  if (expr === "happy") p.arc(hx - H.a + 36, hy + 50, 34, 18, 10, 170, 5, INK);
  // horns / beard
  if (A.horns) { const hc = A.species === "goat" || (o.species === "goat") ? "#d8cdb8" : "#f0e6cf"; p.line([[hx + 6, hy - H.b + 6], [hx + 16, hy - H.b - 40], [hx - (o.species === "goat" ? -22 : 8), hy - H.b - 70]], hc, 16); }
  if (A.beard) p.poly([[hx - H.a + 24, hy + 52], [hx - H.a + 50, hy + 112 + Math.sin(t * 3) * 4], [hx - H.a + 66, hy + 52]], "#f4ecdc", 5);
  if (A.whiskers) for (const k of [-1, 0, 1]) { p.stroke([[hx - H.a - 6, hy + 28 + k * 8], [hx - H.a - 56, hy + 20 + k * 18]], 3, INK); }
  // eye
  const ex = hx - H.a * 0.5, ey = hy - H.b * 0.2;
  if (fall > 0.4 || expr === "x") { p.stroke([[ex - 14, ey - 14], [ex + 14, ey + 14]], 6, INK); p.stroke([[ex + 14, ey - 14], [ex - 14, ey + 14]], 6, INK); }
  else if (blink > 0.5 || expr === "sleep") p.stroke([[ex - 16, ey], [ex, ey + 6], [ex + 16, ey]], 6, INK);
  else { p.ell(ex, ey, 18, 20, "#ffffff", 4); p.ell(ex - 3, ey + 1, 11, 13, "#4a2c1c", 0); p.ell(ex - 4, ey + 1, 6, 8, INK, 0); p.dot(ex - 8, ey - 5, 3.2, "#ffffff"); }
  p.stroke([[ex - 22, ey - 28 - (expr === "alert" ? 6 : 0)], [ex + 2, ey - 34], [ex + 22, ey - 24]], 7, A.dark);
  // ears
  const ea = ear * 14 + (state === "trot" ? 10 : 0) + (state === "alert" ? -16 : 0);
  const E = (pts, c) => { p.gradFill(pts, c, mul(c, A.shade), light, 0.2); p.inkRing(pts, ow * 0.7, thick); };
  const e0 = [hx + H.a * 0.3, hy - H.b * 0.8];
  if (A.ear === "pig" || (o.species || "pig") === "pig") { p.poly([[hx + 20, hy - 70], [hx + 66, hy - 120 - ea * 0.2], [hx + 98, hy - 60 + ea], [hx + 52, hy - 56]], A.dark, ow * 0.7); E([[hx - 4, hy - 74], [hx + 18, hy - 132 - ea * 0.3], [hx + 78, hy - 94 + ea * 0.5], [hx + 70, hy - 18 + ea], [hx + 36, hy - 36]], A.body); p.poly([[hx + 14, hy - 78], [hx + 28, hy - 112 - ea * 0.2], [hx + 58, hy - 86 + ea * 0.4], [hx + 52, hy - 40 + ea], [hx + 36, hy - 52]], A.nose, 0); }
  else if (A.ear === "point" || A.ear === "pointcat") { const h = A.ear === "pointcat" ? 70 : 90; E([[e0[0] - 14, e0[1] + 10], [e0[0] + 6, e0[1] - h - ea * 0.3], [e0[0] + 34, e0[1] + 6]], A.body); p.poly([[e0[0] - 4, e0[1] + 4], [e0[0] + 8, e0[1] - h * 0.65], [e0[0] + 24, e0[1] + 2]], A.belly, 0); }
  else if (A.ear === "long") { E([[e0[0] - 16, e0[1] + 12], [e0[0] - 6, e0[1] - 150 - ea * 0.4], [e0[0] + 30, e0[1] - 140], [e0[0] + 36, e0[1] + 8]], A.body); p.poly([[e0[0] - 2, e0[1]], [e0[0] + 2, e0[1] - 120], [e0[0] + 18, e0[1] - 116], [e0[0] + 22, e0[1] + 2]], A.belly, 0); }
  else if (A.ear === "floppy") E([[e0[0] - 8, e0[1] + 6], [e0[0] + 30, e0[1] - 20], [e0[0] + 56, e0[1] + 60 + ea], [e0[0] + 22, e0[1] + 86 + ea], [e0[0] - 6, e0[1] + 40]], A.dark);
  else if (A.ear === "cow") E([[e0[0] - 10, e0[1] + 18], [e0[0] + 64, e0[1] - 8 + ea * 0.4], [e0[0] + 84, e0[1] + 30 + ea], [e0[0] + 6, e0[1] + 40]], "#2b2530");
  else if (A.ear === "goat") E([[e0[0] - 10, e0[1] + 18], [e0[0] + 66, e0[1] - 4 + ea * 0.4], [e0[0] + 76, e0[1] + 26 + ea], [e0[0] + 6, e0[1] + 34]], A.body);
  else if (A.ear === "sheep") E([[e0[0] - 6, e0[1] + 16], [e0[0] + 50, e0[1] - 4 + ea * 0.3], [e0[0] + 62, e0[1] + 30 + ea], [e0[0] + 4, e0[1] + 36]], A.face || A.body);
  g.restore();
};
// ---- birds ----
const BD = {
  chicken: { body: "#fbf6ee", wing: "#f1e6d4", tailC: "#e9dcc6", beak: "#f2b84a", comb: "#e0403c", leg: "#f2b84a", s: 1.0, comb2: false },
  rooster: { body: "#c8622a", wing: "#8a3a1c", tailC: "#2e6a4a", beak: "#f2b84a", comb: "#e0403c", leg: "#d8a03a", s: 1.15, comb2: true },
  duck:    { body: "#ffe36a", wing: "#f2c84a", tailC: "#f2c84a", beak: "#f08a2a", comb: null, leg: "#f08a2a", s: 0.95, flat: true },
  goose:   { body: "#fbfbf8", wing: "#e8e8e2", tailC: "#e8e8e2", beak: "#f08a2a", comb: null, leg: "#f08a2a", s: 1.3, flat: true, longNeck: true },
  emu:     { body: "#8a6a4e", wing: "#6e523c", tailC: "#5a4232", beak: "#6a5a4a", comb: null, leg: "#7a6a58", s: 1.45, flat: false, longNeck: true, nl: 150, lift: 70 },
  gull:    { body: "#f7f9fc", wing: "#9aa7ba", tailC: "#dfe6ef", beak: "#f2b84a", comb: null, leg: "#f2a05a", s: 1.0, flat: false },
};
export const birdSide = (p, o = {}) => {
  const B = BD[o.species || "chicken"], g = p.g, light = rad(-120), thick = thickAngle(light), ow = 6;
  const { state = "stand", phase = 0, blink = 0, t = 0 } = o; const walk = state === "walk" ? 1 : 0, peck = state === "peck" ? Math.max(0, Math.sin(t * 7)) : 0;
  g.save(); g.translate(300, 975); g.scale(B.s, B.s); g.translate(-300, -975); p.rot = null;
  const bob = walk * 6 * Math.abs(Math.sin(phase * Math.PI * 4));
  const bc = [310, 800 - bob - (B.lift || 0)];
  // legs
  for (const [x, ph] of [[300, 0], [340, 0.5]]) { const sw = walk * Math.sin(2 * Math.PI * (phase + ph)) * 26; p.line([[x, bc[1] + 60], [x + sw * 0.5, 920], [x + sw, 968]], B.leg, 9); p.line([[x + sw - 22, 968], [x + sw + 4, 968], [x + sw + 24, 962]], B.leg, 7); }
  // tail feathers
  for (let i = 0; i < 4; i++) p.poly([[bc[0] + 90, bc[1] - 20], [bc[0] + 150 + i * 8, bc[1] - 90 - i * 22 + Math.sin(t * 5 + i) * 4], [bc[0] + 110 + i * 4, bc[1] + 10]], i % 2 ? B.tailC : B.wing, 4);
  // body
  const body = blobPts(bc[0], bc[1], { a: 110, b: 82, nTop: 2.2, nBot: 2.0, egg: -0.1, asym: 0, rot: rad(-8), noise: 0.01, seed: 4 }, 70);
  p.gradFill(body, B.body, mul(B.body, [0.8, 0.76, 0.84]), light, 0.2); p.inkRing(body, ow * 0.85, thick);
  const wing = blobPts(bc[0] + 20, bc[1] - 4 + Math.sin(t * 10 * (state === "fly" ? 1 : 0.1)) * (state === "fly" ? 30 : 2), { a: 64, b: 44, nTop: 2.2, nBot: 2.2, egg: 0.1, asym: 0, rot: rad(14), noise: 0.01, seed: 8 }, 40);
  p.gradFill(wing, B.wing, mul(B.wing, [0.8, 0.76, 0.84]), light, 0.2); p.inkRing(wing, ow * 0.7, thick);
  // neck + head
  const nl = B.nl || (B.longNeck ? 120 : 70), hd = peck * 90; const hx = bc[0] - 96 - peck * 40, hy = bc[1] - nl - 30 + hd;
  p.line([[bc[0] - 70, bc[1] - 30], [bc[0] - 96, bc[1] - nl * 0.6 + hd * 0.4], [hx, hy + 8]], B.body, B.longNeck ? 34 : 44);
  const head = blobPts(hx, hy, { a: B.longNeck ? 34 : 44, b: B.longNeck ? 30 : 42, nTop: 2.3, nBot: 2.1, egg: 0, asym: 0, rot: 0, noise: 0.01, seed: 2 }, 40);
  p.gradFill(head, B.body, mul(B.body, [0.8, 0.76, 0.84]), light, 0.2); p.inkRing(head, ow * 0.75, thick);
  if (B.comb) { for (let i = 0; i < (B.comb2 ? 4 : 3); i++) p.ell(hx - 6 + i * 14, hy - 40 - (i % 2) * 8, 11, 14, B.comb, 4); p.ell(hx - 40, hy + 34, 9, 16, B.comb, 4); }
  p.poly(B.flat ? [[hx - 40, hy + 6], [hx - 96, hy + 14], [hx - 92, hy + 30], [hx - 38, hy + 26]] : [[hx - 40, hy + 2], [hx - 78, hy + 16], [hx - 40, hy + 28]], B.beak, 5);
  if (blink > 0.5) p.stroke([[hx - 24, hy - 4], [hx - 10, hy - 2]], 5, INK); else { p.ell(hx - 16, hy - 6, 9, 10, "#ffffff", 3); p.dot(hx - 18, hy - 5, 4.2, INK); p.dot(hx - 20, hy - 8, 1.6, "#ffffff"); }
  g.restore();
};
