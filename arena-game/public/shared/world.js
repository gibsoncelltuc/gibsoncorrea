// Mapa do mundo aberto: lido PELO SERVIDOR (validações) e PELO CLIENTE (desenho). Mudou aqui, mudou nos dois.
export const WORLD_HALF = 320; // o mundo vai de -320 a +320
export const SEA_LEVEL = -1.2;
const TAU = Math.PI * 2;

export const LOCATIONS = {
  town: { x: 0, z: 0, r: 72, name: 'Vila Moeda' },
  mayor: { x: 7, z: -13, r: 4, name: 'Prefeito Ouro' },
  colosseum: { x: 84, z: 46, r: 32, name: 'Coliseu' },
  forest: { x: -10, z: -190, r: 75, name: 'Floresta Sussurrante' },
  desert: { x: 195, z: 5, r: 85, name: 'Deserto Escaldante' },
  pyramid: { x: 205, z: -35, r: 20, name: 'Pirâmide Dourada' },
  snow: { x: -205, z: -30, r: 85, name: 'Montanhas Geladas' },
  farm: { x: -110, z: 135, r: 62, name: 'Fazenda Sol' },
  beach: { x: 15, z: 192, r: 62, name: 'Praia do Farol' },
  castle: { x: 205, z: -215, r: 62, name: 'Castelo do Rei Gosma' },
  ruins: { x: -170, z: -190, r: 52, name: 'Ruínas Antigas' },
};
export const SPAWN = { x: 0, z: 20 };
export const ARENA_SPAWNS = [{ x: LOCATIONS.colosseum.x - 10, z: LOCATIONS.colosseum.z }, { x: LOCATIONS.colosseum.x + 10, z: LOCATIONS.colosseum.z }];
export const ARENA_RADIUS = 21;

// onde o inimigo de cada tipo pode ser derrotado (o servidor confere pela posição do jogador)
export const ENEMY_BIOMES = {
  slime: ['grass', 'farm', 'beach', 'forest', 'town'],
  brute: ['forest', 'castle', 'ruins'],
  scorpion: ['desert'],
  wolf: ['snow'],
  skeleton: ['ruins'],
  kingslime: ['castle'],
};
// dificuldade por bioma (multiplica vida e dano dos inimigos)
export const TIER = { grass: 1, town: 1, farm: 1, beach: 1.2, forest: 1.6, desert: 2.1, snow: 2.6, ruins: 3.2, castle: 4 };

export const CRYSTALS = [
  { id: 'cr1', x: -30, z: -150 }, { id: 'cr2', x: 22, z: -175 }, { id: 'cr3', x: -48, z: -205 }, { id: 'cr4', x: 35, z: -215 }, { id: 'cr5', x: -8, z: -238 },
];

// estradas ligando a vila aos destinos (pontos de controle; o cliente suaviza)
export const ROADS = [
  [[0, 20], [0, 70], [4, 120], [10, 160], [14, 188]],
  [[0, -20], [-4, -70], [-8, -120], [-10, -170]],
  [[30, 0], [80, -4], [130, -6], [180, -20], [205, -35]],
  [[-30, 0], [-80, -10], [-140, -20], [-195, -30]],
  [[-20, 25], [-55, 70], [-90, 110], [-110, 135]],
  [[40, 20], [70, 40], [84, 46]],
  [[150, -10], [175, -90], [190, -170], [205, -215]],
  [[-195, -30], [-190, -100], [-175, -160], [-170, -190]],
];

export const smooth = (a, b, x) => {
  const t = Math.min(1, Math.max(0, (x - a) / (b - a)));
  return t * t * (3 - 2 * t);
};
const dist = (x, z, l) => Math.hypot(x - l.x, z - l.z);
const noise = (x, z) => Math.sin(x * 0.045 + 1.3) * Math.cos(z * 0.039 - 0.7) * 1.7 + Math.sin(x * 0.021 + z * 0.017) * 2.4 + Math.sin(x * 0.11 - z * 0.09) * 0.45;

// lagos / oásis / mar (para água e para a altura do terreno)
export const LAKES = [
  { x: -70, z: -95, r: 26, name: 'Lago Espelho' },
  { x: 150, z: 45, r: 13, name: 'Oásis' },
  { x: -215, z: 20, r: 24, name: 'Lago Congelado', ice: true },
];

export function heightAt(x, z) {
  const L = LOCATIONS;
  let h = noise(x, z) * 0.42 + 1.5;
  const dT = dist(x, z, L.town);
  h *= smooth(L.town.r - 5, L.town.r + 45, dT);
  // coliseu e castelo: terreno plano
  h *= smooth(L.colosseum.r + 2, L.colosseum.r + 22, dist(x, z, L.colosseum));
  // deserto: dunas
  const dD = dist(x, z, L.desert);
  h += smooth(L.desert.r + 30, L.desert.r - 25, dD) * (Math.sin(x * 0.05 + z * 0.03) * 2.2 + Math.sin(x * 0.09 - z * 0.06) * 1.2 + 3.6);
  // neve: colinas altas
  const dS = dist(x, z, L.snow);
  h += smooth(L.snow.r + 40, L.snow.r - 20, dS) * (Math.abs(noise(x * 1.6, z * 1.6)) * 4.5 + 3);
  // castelo: platô elevado com rampa
  const dC = dist(x, z, L.castle);
  h = h * (1 - smooth(60, 100, 160 - dC)) + 16 * smooth(105, 55, dC);
  // ruínas: elevação suave
  h += smooth(L.ruins.r + 15, L.ruins.r - 20, dist(x, z, L.ruins)) * 3.5;
  // praia: desce até o mar ao sul
  h -= smooth(188, 292, z) * 7.5;
  for (const k of LAKES) h -= smooth(k.r + 9, k.r * 0.35, Math.hypot(x - k.x, z - k.z)) * 4.2;
  // borda do mundo: montanhas
  const d0 = Math.hypot(x, z);
  h += smooth(WORLD_HALF - 20, WORLD_HALF + 60, Math.max(Math.abs(x), Math.abs(z)) * 1.0) * 55 + Math.max(0, d0 - 380) * 0.2;
  return h;
}

// distância até a estrada mais próxima (para pintar o chão e achatar o terreno)
export function roadDist(x, z) {
  let best = Infinity;
  for (const road of ROADS) {
    for (let i = 0; i < road.length - 1; i++) {
      const [ax, az] = road[i];
      const [bx, bz] = road[i + 1];
      const dx = bx - ax;
      const dz = bz - az;
      const t = Math.max(0, Math.min(1, ((x - ax) * dx + (z - az) * dz) / (dx * dx + dz * dz)));
      best = Math.min(best, Math.hypot(x - (ax + t * dx), z - (az + t * dz)));
    }
  }
  return best;
}

// pesos de cada bioma na posição (para misturar cores) e bioma dominante
export function biomeWeights(x, z) {
  const L = LOCATIONS;
  const w = {
    town: smooth(L.town.r + 25, L.town.r - 15, dist(x, z, L.town)),
    desert: smooth(L.desert.r + 20, L.desert.r - 25, dist(x, z, L.desert)),
    snow: smooth(L.snow.r + 20, L.snow.r - 25, dist(x, z, L.snow)),
    forest: smooth(L.forest.r + 20, L.forest.r - 25, dist(x, z, L.forest)),
    farm: smooth(L.farm.r + 15, L.farm.r - 20, dist(x, z, L.farm)),
    beach: smooth(L.beach.r + 25, L.beach.r - 20, dist(x, z, L.beach)) * smooth(120, 165, z),
    castle: smooth(L.castle.r + 20, L.castle.r - 20, dist(x, z, L.castle)),
    ruins: smooth(L.ruins.r + 15, L.ruins.r - 20, dist(x, z, L.ruins)),
  };
  return w;
}
export function biomeAt(x, z) {
  const w = biomeWeights(x, z);
  let best = 'grass';
  let bv = 0.35;
  for (const [k, v] of Object.entries(w)) if (v > bv) (bv = v), (best = k);
  return best;
}
export const inWorld = (x, z) => Math.abs(x) <= WORLD_HALF && Math.abs(z) <= WORLD_HALF;
export const distTo = (x, z, key) => Math.hypot(x - LOCATIONS[key].x, z - LOCATIONS[key].z);

// ---------- aparência do avatar (índices em paletas fixas: o servidor nunca aceita cores livres) ----------
export const SKIN = ['#ffd9b8', '#f1c27d', '#d9a066', '#b57a4a', '#8a5a3a', '#5a3a28'];
export const HAIR_COLOR = ['#2b2118', '#5a3822', '#a0522d', '#d98b2b', '#e8d27a', '#c4453f', '#7a5ad6', '#2f8fd8'];
export const SHIRT = ['#4f86f7', '#e8564f', '#3fae6a', '#f0b429', '#a35cff', '#ff7ab0', '#2b2f4a', '#eeeeee', '#00b3a4', '#ff8a3d'];
export const PANTS = ['#35406b', '#2b2118', '#6b432c', '#3f3f46', '#1e6b52', '#7a2e3a', '#c8b89a', '#2b55b5'];
export const HAIR_STYLES = ['Curto', 'Espetado', 'Longo', 'Coque', 'Careca'];
export const FACES = ['Sorriso', 'Piscadinha', 'Feliz', 'Legal'];
export const defaultAppearance = () => ({ skin: 1, hair: 0, hairColor: 1, shirt: 0, pants: 0, face: 0 });
export function cleanAppearance(a = {}) {
  const lim = { skin: SKIN.length, hair: HAIR_STYLES.length, hairColor: HAIR_COLOR.length, shirt: SHIRT.length, pants: PANTS.length, face: FACES.length };
  const out = defaultAppearance();
  for (const [k, n] of Object.entries(lim)) {
    const v = Number(a[k]);
    if (Number.isInteger(v) && v >= 0 && v < n) out[k] = v;
  }
  return out;
}
export { TAU };
