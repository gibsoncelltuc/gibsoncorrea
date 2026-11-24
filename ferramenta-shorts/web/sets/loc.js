// ===== LOCACOES LIMPAS (v13, 24/11): cenarios SEM tema de outro video. Nada de celeiro, moinho, trigo, saco de areia, barril:
// so' chao + horizonte + o que a pesquisa visual (DOSSIE) mandar por em "itens". Cada uma tem seu X (mkvideo SETS_X).
// globalThis.LOCCFG = { loc_pista: { chao: '#333', itens: [[asset, dx, z, s, ry], ...], linhas: false, horizonte: 'nenhum' }, ... }  (vem do roteiro: "locacao")
const _locCfg = (n) => (globalThis.LOCCFG && globalThis.LOCCFG[n]) || {};
const _locItens = (n, X) => { for (const it of (_locCfg(n).itens || [])) { if (!LIBA[it[0]]) continue; libInst(it[0], X + (it[1] || 0), DECK, it[2] || -12, it[4] || 0, it[3] || 1); } };
const _locBoxCity = (X, z0, cols, n = 16, seed = 31) => { const r = P.rng(seed); for (let i = 0; i < n; i++) { const w = 7 + r() * 9, h = 10 + r() * 34, x = X - 130 + i * (260 / n) + r() * 6; const g = new THREE.Group(); g.position.set(x, DECK, z0 - r() * 30); world.add(g);
    add(box(w, h, w * 0.8), toon({ color: cols[i % cols.length] }), 0, h / 2, 0, g); const wm = new THREE.MeshBasicMaterial({ color: globalThis.LOC_NOITE ? '#ffe9a8' : '#cfe3f2' });
    for (let a = 0; a < Math.floor(h / 3.2); a++) for (let b = 0; b < 3; b++) { if (globalThis.LOC_NOITE && r() < 0.45) continue; const m = add(box(w * 0.2, 1.2, 0.08), wm, (b - 1) * w * 0.3, 2.2 + a * 3.2, w * 0.4 + 0.05, g); m.castShadow = false; } } };
SETDEF.loc_pista = (X) => {   // pista de testes / patio de evento moderno: asfalto escuro, faixas, sem nada rural
  const c = _locCfg('loc_pista'); groundPlane(X, 0, 320, 240, toon({ color: c.chao || '#3a3d45' }), DECK, 8);
  if (c.linhas !== false) { const wl = toon({ color: '#e9e9e2' }), yl = toon({ color: '#e8c33a' }); for (let i = -14; i <= 14; i++) { const m = add(box(3.4, 0.02, 0.22), wl, X + i * 7, DECK + 0.03, 3.2, world); m.castShadow = false; }
    for (const z of [-7.5, 8.5]) { const m = add(box(260, 0.02, 0.2), yl, X, DECK + 0.03, z, world); m.castShadow = false; } }
  if ((c.horizonte || 'colinas') === 'colinas') farHills(X, -150, c.cor_horizonte || '#2c3140', '#343a4c', 14, 300);
  else if (c.horizonte === 'cidade') _locBoxCity(X, -90, ['#4b5568', '#5a6478', '#3f4858', '#667189']);
  _locItens('loc_pista', X);
};
SETDEF.loc_patio = (X) => {   // patio de fabrica / area industrial moderna: concreto claro e galpoes lisos ao fundo
  const c = _locCfg('loc_patio'); groundPlane(X, 0, 320, 240, toon({ color: c.chao || '#9a9c9f' }), DECK, 8);
  const jm = toon({ color: '#85878b' }); for (let i = -10; i <= 10; i++) { const m = add(box(0.12, 0.02, 60), jm, X + i * 8, DECK + 0.02, -6, world); m.castShadow = false; }
  if (c.horizonte !== 'nenhum') { const r = P.rng(57); for (let i = 0; i < 7; i++) { const w = 26 + r() * 16, h = 9 + r() * 5, g = new THREE.Group(); g.position.set(X - 120 + i * 40, DECK, -70 - r() * 14); world.add(g); add(box(w, h, 22), toon({ color: ['#c9cdd3', '#b7bcc4', '#d6d9dd'][i % 3] }), 0, h / 2, 0, g); add(box(w + 0.6, 0.7, 22.6), toon({ color: '#6d7480' }), 0, h + 0.35, 0, g); add(box(5, 5, 0.2), toon({ color: '#58606c' }), 0, 2.5, 11.05, g); } }
  farHills(X, -190, c.cor_horizonte || '#9fb1c4', '#aebdcd', 12, 330); _locItens('loc_patio', X);
};
SETDEF.loc_deserto = (X) => {   // deserto limpo: areia, dunas e pedras. SEM fazenda, SEM trigo, SEM cerca
  const c = _locCfg('loc_deserto'); groundPlane(X, 0, 320, 240, toon({ color: c.chao || '#dcbf85' }), DECK, 8);
  const r = P.rng(71), dn = [toon({ color: '#d3b477' }), toon({ color: '#e3c992' })];
  for (let i = 0; i < 16; i++) { const m = add(new THREE.SphereGeometry(1, 16, 8), dn[i % 2], X + (r() - 0.5) * 300, DECK - 0.5, -60 - r() * 70, world); m.scale.set(22 + r() * 26, 3 + r() * 5, 14 + r() * 12); m.castShadow = false; }
  if (LIBA['nature/rocks']) for (let i = 0; i < 12; i++) libInst('nature/rocks', X + (r() - 0.5) * 200, DECK, -34 - r() * 40, r() * 6, 1.2 + r() * 1.6);
  farHills(X, -150, c.cor_horizonte || '#c9a26e', '#d6b381', 14, 290); _locItens('loc_deserto', X);
};
SETDEF.loc_campo = (X) => {   // campo aberto limpo: grama, arvores longe e colinas. SEM casa, SEM celeiro, SEM moinho
  const c = _locCfg('loc_campo'); groundPlane(X, 0, 320, 240, toon({ color: c.chao || '#86b35a' }), DECK, 8);
  makeTufts(X, 0, 200, 70, 2200, ['#7fae52', '#93bf63', '#6f9f48'], () => true, 0.32);
  const r = P.rng(93); if (LIBA['nature/tree_oak']) for (let i = 0; i < 18; i++) libInst('nature/tree_oak', X + (r() - 0.5) * 260, DECK, -42 - r() * 50, r() * 6, 1.3 + r() * 0.9);
  farHills(X, -150, c.cor_horizonte || '#6f9a66', '#80a977', 14, 290); _locItens('loc_campo', X);
};
SETDEF.loc_montanha = (X) => {   // montanha limpa: chao de pedra, picos. SEM saco de areia, SEM castelo, SEM igreja
  const c = _locCfg('loc_montanha'); groundPlane(X, 0, 320, 240, toon({ color: c.chao || '#8d8a80' }), DECK, 8);
  const r = P.rng(41), pk = [toon({ color: '#75727a' }), toon({ color: '#8a8790' }), toon({ color: '#e9edf2' })];
  for (let i = 0; i < 11; i++) { const h = 40 + r() * 50, x = X - 170 + i * 34 + r() * 10, z = -120 - r() * 50; const m = add(new THREE.ConeGeometry(26 + r() * 16, h, 7), pk[i % 2], x, DECK + h / 2 - 2, z, world); m.castShadow = false; const s = add(new THREE.ConeGeometry(9, h * 0.28, 7), pk[2], x, DECK + h * 0.86 - 2, z, world); s.castShadow = false; }
  if (LIBA['nature/rocks']) for (let i = 0; i < 16; i++) libInst('nature/rocks', X + (r() - 0.5) * 180, DECK, -22 - r() * 40, r() * 6, 1.3 + r() * 2.2);
  _locItens('loc_montanha', X);
};
SETDEF.loc_cidade = (X) => {   // cidade moderna (depois de 1950): asfalto, calcada, predios de vidro/concreto. SEM lampiao, SEM barril
  const c = _locCfg('loc_cidade'); groundPlane(X, 0, 320, 240, toon({ color: c.chao || '#50535a' }), DECK, 8);
  const cal = add(box(300, 0.16, 6), toon({ color: '#b9bcc0' }), X, DECK + 0.08, -9.5, world); cal.castShadow = false;
  const wl = toon({ color: '#e9e9e2' }); for (let i = -14; i <= 14; i++) { const m = add(box(3.0, 0.02, 0.2), wl, X + i * 7, DECK + 0.03, 4.2, world); m.castShadow = false; }
  _locBoxCity(X, -22, ['#8fa3b8', '#a9b7c6', '#7b8fa6', '#c4ccd6', '#6d7f96'], 18, 33); _locBoxCity(X, -70, ['#75869c', '#8b9ab0', '#63748b'], 14, 35); _locItens('loc_cidade', X);
};
SETDEF.loc_estudio = (X) => {   // ESTUDIO DE EXPLICACAO (cena de ciencia sem personagem): chao escuro com grade, fundo liso, nada mais
  const c = _locCfg('loc_estudio'); groundPlane(X, 0, 400, 400, new THREE.MeshBasicMaterial({ color: c.chao || '#2a5fa8', fog: false }), DECK, 8);
  const gm = new THREE.MeshBasicMaterial({ color: c.grade || '#6fb0f0', fog: false }); for (let i = -30; i <= 30; i++) { const a = add(box(0.05, 0.01, 140), gm, X + i * 2, DECK + 0.015, -20, world), b = add(box(140, 0.01, 0.05), gm, X, DECK + 0.015, -20 + i * 2, world); a.castShadow = b.castShadow = false; a.userData.ndSkip = b.userData.ndSkip = true; }
  const bk = add(new THREE.PlaneGeometry(600, 240), new THREE.MeshBasicMaterial({ color: c.fundo || '#3273c4', fog: false }), X, DECK + 100, -95, world); bk.castShadow = false; bk.userData.ndSkip = true;
};
