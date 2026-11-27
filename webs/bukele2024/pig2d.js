// ---- the pig, drawn in the same inked/shaded card style as the cast (side view, faces LEFT) ----
export const PIGC = { body: "#f7a8b8", shade: [0.84, 0.66, 0.74], pink: "#f08aa0", pink2: "#e8708a", belly: "#ffd0d9", dark: "#e58fa4", bristle: "#d9728a", brow: "#c25c78", white: "#fff4ee", hoof: "#efe0cc", ink: INK };
const spiral = (cx, cy, t, wig) => { const pts = []; for (let i = 0; i <= 18; i++) { const a = i / 18 * 5.2 + wig, r = 20 - i * 0.8; pts.push([cx + Math.cos(a) * r * (1 - i / 40) + i * 1.2, cy - i * 2.2 + Math.sin(a) * r * 0.9]); } return pts; };
export const pigSideOld = (p, o = {}) => {
  const { state = "root", phase = 0, down = 0, blink = 0, ear = 0, tail = 0, expr = "normal", fall = 0, t = 0, light = rad(-120) } = o;
  const g = p.g, thick = thickAngle(light), ow = 6.5, u = 1.0;
  const trot = state === "trot" ? 1 : 0;
  const bob = trot * 7 * Math.cos(4 * Math.PI * phase) + (state === "root" ? 2.5 * Math.abs(Math.sin(t * 5.5)) : 0);
  const bodyC = [320, 742 + bob];
  g.save();
  if (fall > 0) { const ang = -fall * Math.PI * 0.96; g.translate(bodyC[0], bodyC[1]); g.rotate(ang); g.translate(-bodyC[0], -bodyC[1]); }
  p.rot = null;
  const legs = [{ x: 205, ph: 0 }, { x: 255, ph: 0.5 }, { x: 395, ph: 0.5 }, { x: 445, ph: 0 }];
  const drawLeg = (L, back) => {
    const sw = trot * Math.sin(2 * Math.PI * (phase + L.ph)) * 34, lift = trot * Math.max(0, Math.cos(2 * Math.PI * (phase + L.ph))) * 24;
    const hip = [L.x, 790 + bob], knee = [L.x + sw * 0.55 + (fall ? (L.x < 330 ? -30 : 30) : 0), 868 + bob * 0.4 - lift * 0.6], foot = [L.x + sw + (fall ? (L.x < 330 ? -44 : 46) : 0), 958 - lift - (fall ? 30 : 0)];
    const col = back ? PIGC.dark : PIGC.body;
    p.line([hip, knee, foot], col, 44 - (back ? 4 : 0));
    p.poly(rrect(foot[0] - 22, foot[1] - 26, foot[0] + 20, foot[1] + 10, 8), PIGC.white, 5);
    p.ell(foot[0] - 2, foot[1] + 8, 24, 11, PIGC.hoof, 4);
  };
  drawLeg(legs[1], true); drawLeg(legs[3], true);
  // tail (curly, wiggles)
  p.line(spiral(515, 690 + bob, t, tail), PIGC.body, 11);
  // body
  const body = blobPts(bodyC[0], bodyC[1], { a: 228, b: 128, nTop: 2.4, nBot: 2.05, egg: 0.06, asym: -0.04, rot: 0, noise: 0.012, seed: 17 }, 90);
  p.gradFill(body, PIGC.body, mul(PIGC.body, PIGC.shade), light, 0.2);
  p.clip(body, () => {
    p.ell(300, 868 + bob, 210, 52, PIGC.belly, 0);                               // lighter belly
    p.stroke([[170, 650 + bob], [250, 626 + bob], [370, 628 + bob], [470, 660 + bob]], 12, "#ffffff55");   // back light
    for (let i = 0; i < 4; i++) p.stroke([[420 + i * 8, 660 + i * 22 + bob], [446 + i * 5, 690 + i * 22 + bob]], 3, "#00000022");
    p.ell(450, 742 + bob, 78, 88, "#c8587014", 0);
  });
  p.inkRing(body, ow * 0.85, thick);
  // bristle ridge
  for (let i = 0; i < 9; i++) { const x = 190 + i * 38; p.poly([[x - 9, 622 + 2 * Math.abs(i - 4) + bob], [x + 2, 598 + 2 * Math.abs(i - 4) + bob + Math.sin(t * 6 + i) * 2], [x + 11, 624 + 2 * Math.abs(i - 4) + bob]], PIGC.bristle, 3); }
  drawLeg(legs[0], false); drawLeg(legs[2], false);
  // ---- head ----
  const hd = (state === "root" ? 52 + 22 * Math.sin(t * 5.5) : state === "alert" ? -28 : state === "trot" ? -6 : 0) + down;
  const hc = [118, 742 + bob + hd];
  const neck = blobPts(172, 742 + bob + hd * 0.5, { a: 78, b: 98, nTop: 2.2, nBot: 2.2, egg: 0, asym: 0, rot: 0, noise: 0.01, seed: 3 }, 50);
  p.gradFill(neck, PIGC.body, mul(PIGC.body, PIGC.shade), light, 0.2); p.inkRing(neck, ow * 0.7, thick);
  const head = blobPts(hc[0], hc[1], { a: 96, b: 88, nTop: 2.3, nBot: 2.0, egg: -0.1, asym: -0.04, rot: rad(-6), noise: 0.012, seed: 9 }, 70);
  p.gradFill(head, PIGC.body, mul(PIGC.body, PIGC.shade), light, 0.2);
  // snout + disc + nostrils
  const sn = blobPts(hc[0] - 98, hc[1] + 26, { a: 52, b: 40, nTop: 2.4, nBot: 2.2, egg: 0, asym: 0, rot: 0, noise: 0.008, seed: 5 }, 40);
  p.gradFill(sn, PIGC.pink, mul(PIGC.pink, [0.86, 0.8, 0.88]), light, 0.2); p.inkRing(sn, ow * 0.8, thick);
  const disc = blobPts(hc[0] - 138, hc[1] + 24, { a: 16, b: 34, nTop: 2.2, nBot: 2.2, egg: 0, asym: 0, rot: 0, noise: 0, seed: 6 }, 24);
  p.poly(disc, PIGC.pink2, 5);
  p.ell(hc[0] - 142, hc[1] + 12, 5, 9, INK, 0); p.ell(hc[0] - 142, hc[1] + 36, 5, 9, INK, 0);
  p.inkRing(head, ow * 0.85, thick);
  p.stroke([[hc[0] - 92, hc[1] + 56], [hc[0] - 60, hc[1] + 62], [hc[0] - 28, hc[1] + 52]], 4, INK);        // mouth
  if (expr === "happy") p.arc(hc[0] - 60, hc[1] + 50, 34, 18, 10, 170, 5, INK);
  // cheek blush
  p.ell(hc[0] - 34, hc[1] + 30, 20, 13, "#ff8fa8", 0);
  p.inkRing(head, ow * 0.85, thick);
  // eye
  const ex = hc[0] - 52, ey = hc[1] - 18;
  if (fall > 0.4 || expr === "x") { p.stroke([[ex - 14, ey - 14], [ex + 14, ey + 14]], 6, INK); p.stroke([[ex + 14, ey - 14], [ex - 14, ey + 14]], 6, INK); }
  else if (blink > 0.5 || expr === "sleep") p.stroke([[ex - 16, ey], [ex, ey + 6], [ex + 16, ey]], 6, INK);
  else { p.ell(ex, ey, 18, 20, "#ffffff", 4); p.ell(ex - 3, ey + 1, 11, 13, "#4a2c1c", 0); p.ell(ex - 4, ey + 1, 6, 8, INK, 0); p.dot(ex - 8, ey - 5, 3.2, "#ffffff"); }
  p.stroke([[ex - 22, ey - 28 - (expr === "alert" ? 6 : 0)], [ex + 2, ey - 34], [ex + 22, ey - 24]], 7, PIGC.brow);       // brow
  // ears: front ear flops over the head, back ear peeks behind
  const ea = ear * 14 + (state === "trot" ? 10 : 0) + (state === "alert" ? -16 : 0);
  const earBack = [[hc[0] + 20, hc[1] - 70], [hc[0] + 66, hc[1] - 120 - ea * 0.2], [hc[0] + 98, hc[1] - 60 + ea], [hc[0] + 52, hc[1] - 56]];
  p.poly(earBack, PIGC.dark, ow * 0.7);
  const earF = [[hc[0] - 4, hc[1] - 74], [hc[0] + 18, hc[1] - 132 - ea * 0.3], [hc[0] + 78, hc[1] - 94 + ea * 0.5], [hc[0] + 70, hc[1] - 18 + ea], [hc[0] + 36, hc[1] - 36]];
  p.gradFill(earF, PIGC.body, mul(PIGC.body, PIGC.shade), light, 0.2); p.inkRing(earF, ow * 0.7, thick);
  p.poly([[hc[0] + 14, hc[1] - 78], [hc[0] + 28, hc[1] - 112 - ea * 0.2], [hc[0] + 58, hc[1] - 86 + ea * 0.4], [hc[0] + 52, hc[1] - 40 + ea], [hc[0] + 36, hc[1] - 52]], PIGC.pink2, 0);
  if (o.angel) {
    const wf = Math.sin(t * 7) * 18;
    for (const k of [0, 1]) { const w = [[330 + k * 40, 660 + bob], [300 + k * 40, 540 - wf + bob], [380 + k * 40, 500 - wf * 1.2 + bob], [430 + k * 40, 590 - wf * 0.6 + bob], [410 + k * 40, 660 + bob]]; p.gradFill(w, "#ffffff", "#cfe0f5", light, 0.2); p.inkRing(w, ow * 0.7, thick); }
    p.ell(hc[0] + 10, hc[1] - 150, 52, 14, null, 8); p.ell(hc[0] + 10, hc[1] - 150, 52, 14, "#ffe08a", 5);
  }
  g.restore();
};
export const fxZZ = 0;

// ---- "O PORQUINHO" — the user-approved pig design (round head, pointy ears, big snout, blush, thin dark legs). Faces LEFT (flip in the card).
// expressions: principal (smile + tongue) | eat (happy eyes + potato) | scared | neutral | dead (X eyes). state picks one if expr is not given.
export const PIGT = { body: "#ffb6d2", belly: "#ffcce0", earIn: "#ff8fb8", snout: "#ff9cc2", nostril: "#7a2c45", cheek: "#ff95ba", mouthIn: "#6b1f2f", leg: "#2e1c1e", potato: "#c49a5a", tongue: "#e8717a", shadow: "#d6d1cb" };
export const pigToon = (p, o = {}) => {
  const g = p.g, { state = "stand", phase = 0, blink = 0, ear = 0, tail = 0, fall = 0, t = 0 } = o;
  const expr = o.expr && o.expr !== "normal" ? o.expr : state === "root" ? "eat" : state === "alert" ? "scared" : state === "trot" ? "principal" : state === "fall" ? "dead" : "neutral";
  const trot = state === "trot" ? 1 : 0, bob = trot * 7 * Math.abs(Math.sin(2 * Math.PI * phase * 2)) + (state === "root" ? 3 * Math.abs(Math.sin(t * 5.5)) : 0);
  const bc = [350, 742 - bob], OL = 9;
  g.save(); p.rot = null;
  p.ell(330, 962 + (fall > 0 ? 6 : 0), 270, 26, PIGT.shadow, 0);
  if (fall > 0) { const f = Math.min(1, fall), e = f * f * (3 - 2 * f), sy = Math.cos(f * Math.PI), Y0 = bc[1] + (843 - bc[1]) * e; g.translate(0, Y0); g.scale(1, Math.abs(sy) < 0.04 ? 0.04 : sy); g.translate(0, -bc[1]); }
  // legs: thin dark sticks with little feet; diagonal pairs swing when trotting
  const leg = (x, ph, back) => { const sw = trot * Math.sin(2 * Math.PI * (phase + ph)) * 20 + (fall >= 1 ? Math.sin(t * 11 + ph * 6) * 14 : 0), lift = trot * Math.max(0, Math.cos(2 * Math.PI * (phase + ph))) * 22; const hip = [x, bc[1] + 112], foot = [x + sw, 950 - lift - (fall > 0 ? 40 : 0)]; p.stroke([hip, [x + sw * 0.5, (hip[1] + foot[1]) / 2], foot], 15, PIGT.leg); p.ell(foot[0] + (back ? 4 : -4), foot[1] + 6, 20, 9, PIGT.leg, 0); };
  leg(250, 0.5, true); leg(470, 0, true);
  // tail: out of the rump, up, then a big loop (as in the reference sheet)
  { const tw = Math.sin(t * 8) * 4 + tail * 6; const B = [bc[0] + 184, bc[1] - 14]; const pts = [B, [B[0] + 30, B[1] - 20 + tw * 0.3], [B[0] + 46, B[1] - 56 + tw]];
    const C = [B[0] + 28 + tw * 0.5, B[1] - 84]; for (let i = 0; i <= 22; i++) { const a = (-20 + i * 17) * Math.PI / 180, r = 26 - i * 0.55; pts.push([C[0] + Math.cos(a) * r, C[1] - Math.sin(a) * r]); }
    p.stroke(pts, 10, PIGT.leg); }
  // body
  p.ell(bc[0], bc[1], 192, 132, PIGT.body, OL);
  p.clip(blobPts(bc[0], bc[1], { a: 188, b: 128, nTop: 2, nBot: 2, egg: 0, asym: 0, rot: 0, noise: 0, seed: 1 }, 70), () => { p.ell(bc[0] - 10, bc[1] + 52, 150, 70, PIGT.belly, 0); p.stroke([[bc[0] - 150, bc[1] - 70], [bc[0] - 90, bc[1] - 112], [bc[0] + 10, bc[1] - 124]], 16, "#ffffffaa"); });
  p.ell(bc[0], bc[1], 192, 132, null, OL);
  leg(215, 0, false); leg(505, 0.5, false);
  // head (big round, overlapping the front of the body)
  const hd = (state === "root" ? 26 + 18 * Math.sin(t * 5.5) : state === "alert" ? -22 : 0), hc = [168, 712 - bob * 0.6 + hd];
  const ew = ear * 12 + (trot ? 8 : 0) + (state === "alert" ? -10 : 0);
  for (const s of [-1, 1]) {   // ears first (behind the head)
    const base = [[hc[0] + s * 96, hc[1] - 70], [hc[0] + s * (116 + ew * 0.3), hc[1] - 188 + ew * 0.4], [hc[0] + s * 22, hc[1] - 118]];
    p.poly(base, PIGT.body, OL); p.poly([[hc[0] + s * 84, hc[1] - 92], [hc[0] + s * (100 + ew * 0.2), hc[1] - 164 + ew * 0.3], [hc[0] + s * 38, hc[1] - 118]], PIGT.earIn, 0);
    { const ax = hc[0] + s * (116 + ew * 0.3), ay = hc[1] - 188 + ew * 0.4; p.stroke([[ax - s * 14, ay + 6], [ax + s * 6, ay - 6], [ax + s * 22, ay + 10]], 8, PIGT.leg); p.stroke([[ax - s * 8, ay + 14], [ax + s * 8, ay + 6]], 6, PIGT.earIn); }
  }
  p.ell(hc[0], hc[1], 128, 126, PIGT.body, OL);
  p.stroke([[hc[0] - 92, hc[1] - 52], [hc[0] - 64, hc[1] - 92], [hc[0] - 20, hc[1] - 108]], 14, "#ffffffbb");   // shine
  for (const s of [-1, 1]) p.ell(hc[0] + s * 84, hc[1] + 30, 30, 19, PIGT.cheek, 0);                           // blush
  // eyes
  const ex = (s) => [hc[0] + s * 50, hc[1] - 22];
  for (const s of [-1, 1]) {
    const [x, y] = ex(s);
    if (expr === "dead") { p.stroke([[x - 16, y - 16], [x + 16, y + 16]], 7, INK); p.stroke([[x + 16, y - 16], [x - 16, y + 16]], 7, INK); }
    else if (expr === "eat" || blink > 0.5) p.arc(x, y + 4, 18, 14, 200, 340, 7, INK);
    else if (expr === "scared") { p.ell(x, y, 22, 24, "#ffffff", 6); p.ell(x + (s > 0 ? -3 : 3), y + 2, 9, 11, INK, 0); p.arc(x, y - 36, 24, 14, 200, 340, 6, INK); }
    else { const r = expr === "neutral" ? 12 : 21; p.ell(x, y, r, r * 1.05, "#2b1a22", 0); p.dot(x - r * 0.3, y - r * 0.35, r * 0.28, "#ffffff"); }
  }
  // snout
  p.ell(hc[0], hc[1] + 38, 66, 44, PIGT.snout, OL);
  p.ell(hc[0] - 22, hc[1] + 36, 11, 18, PIGT.nostril, 0); p.ell(hc[0] + 22, hc[1] + 36, 11, 18, PIGT.nostril, 0);
  // mouth
  if (expr === "scared" || expr === "dead") p.ell(hc[0], hc[1] + 104, 16, 22, PIGT.mouthIn, 5);
  else if (expr === "principal") { p.arc(hc[0], hc[1] + 96, 36, 16, 20, 160, 7, INK); p.ell(hc[0] + 6, hc[1] + 112, 9, 12, PIGT.tongue, 3); }
  else if (expr === "eat") { p.arc(hc[0], hc[1] + 96, 28, 12, 20, 160, 6, INK); p.ell(hc[0] + 26, hc[1] + 96, 36, 25, PIGT.potato, 6); for (const [dx, dy] of [[14, -4], [30, 6], [40, -6]]) p.dot(hc[0] + dx + 8, hc[1] + 96 + dy, 3, "#7a5a2a"); }
  else p.arc(hc[0], hc[1] + 98, 24, 10, 20, 160, 6, INK);
  // angel extras
  if (o.angel) {
    const wf = Math.sin(t * 7) * 16;
    for (const k of [0, 1]) for (let i = 0; i < 4; i++) { const wx = bc[0] + 20 + k * 46 + i * 12, wy = bc[1] - 120 - i * 20 - wf * (0.4 + i * 0.25); p.ell(wx, wy, 56 - i * 6, 24, "#ffffff", 7); }
    p.ell(hc[0], hc[1] - 178, 62, 15, null, 9); p.ell(hc[0], hc[1] - 178, 62, 15, "#ffe08a", 5);
  }
  g.restore();
};

export const pigSide = (p, o = {}) => pigToon(p, o);
