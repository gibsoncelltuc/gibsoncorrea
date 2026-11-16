// ---------- boot: load assets, build the sets this story uses ----------
const DRESS_ASSETS = [...new Set(SETS_USED.flatMap((s) => DRESS[s] || []))];
await loadLib([...new Set([...ASSETS, ...DRESS_ASSETS])]);
for (const s of SETS_USED) { SETDEF[s](SETX[s] ?? 0); SETS_BUILT.add(s); if (!window.NODRESS) dressSet(s, SETX[s] ?? 0); }
