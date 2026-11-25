// Catálogo do jogo: itens, habilidades, inimigos e regras de economia. Tudo balanceável aqui.
export const SLOTS = ['weapon', 'head', 'body', 'tool', 'back'];
export const SLOT_NAMES = { weapon: 'Arma', head: 'Cabeça', body: 'Corpo', tool: 'Ferramenta', back: 'Costas' };

// stats: atk (ataque), def (defesa), hp (vida), speed (velocidade), pickup (raio de coleta), luck (% moedas extras)
export const ITEMS = {
  sword_wood: { name: 'Espada de Madeira', slot: 'weapon', rarity: 'comum', price: 30, stats: { atk: 3 }, color: '#b08850' },
  sword_iron: { name: 'Espada de Ferro', slot: 'weapon', rarity: 'incomum', price: 120, stats: { atk: 8 }, color: '#c8ccd4' },
  sword_flame: { name: 'Lâmina Flamejante', slot: 'weapon', rarity: 'raro', price: 420, stats: { atk: 16 }, color: '#ff5a2a' },
  axe_titan: { name: 'Machado do Titã', slot: 'weapon', rarity: 'épico', price: 950, stats: { atk: 27, speed: -0.3 }, color: '#7b5cff' },

  hat_cloth: { name: 'Chapéu de Pano', slot: 'head', rarity: 'comum', price: 25, stats: { def: 1 }, color: '#9b6bd6' },
  helm_iron: { name: 'Elmo de Ferro', slot: 'head', rarity: 'incomum', price: 140, stats: { def: 4, hp: 10 }, color: '#a9afb9' },
  crown_gold: { name: 'Coroa Dourada', slot: 'head', rarity: 'épico', price: 800, stats: { def: 6, hp: 35 }, color: '#ffd24a' },

  cap_red: { name: 'Boné Vermelho', slot: 'head', rarity: 'comum', price: 35, stats: { def: 1 }, color: '#e8564f' },
  bunny_ears: { name: 'Orelhas de Coelho', slot: 'head', rarity: 'incomum', price: 150, stats: { def: 2, speed: 0.3 }, color: '#ffd0e6' },
  top_hat: { name: 'Cartola Elegante', slot: 'head', rarity: 'raro', price: 260, stats: { def: 3, luck: 8 }, color: '#2b2f4a' },
  crown_hero: { name: 'Coroa do Herói', slot: 'head', rarity: 'épico', price: 0, noShop: true, stats: { def: 8, hp: 50, atk: 4 }, color: '#ffd24a' },

  cape_red: { name: 'Capa Vermelha', slot: 'back', rarity: 'comum', price: 90, stats: { speed: 0.3 }, color: '#d8404f' },
  backpack: { name: 'Mochila de Aventura', slot: 'back', rarity: 'comum', price: 60, stats: { pickup: 1 }, color: '#8a5a3a' },
  wings_angel: { name: 'Asas de Anjo', slot: 'back', rarity: 'épico', price: 480, stats: { speed: 0.8, def: 2 }, color: '#ffffff' },

  tunic_green: { name: 'Túnica Verde', slot: 'body', rarity: 'comum', price: 20, stats: { def: 1 }, color: '#3fae6a' },
  armor_iron: { name: 'Armadura de Ferro', slot: 'body', rarity: 'incomum', price: 220, stats: { def: 7, hp: 20 }, color: '#8d94a0' },
  armor_shadow: { name: 'Manto das Sombras', slot: 'body', rarity: 'raro', price: 560, stats: { def: 10, speed: 0.5 }, color: '#2b2f4a' },

  lantern: { name: 'Lanterna', slot: 'tool', rarity: 'comum', price: 40, stats: { pickup: 1.5 }, color: '#ffe08a' },
  magnet: { name: 'Ímã de Moedas', slot: 'tool', rarity: 'raro', price: 300, stats: { pickup: 4 }, color: '#ff4d6d' },
  lucky_charm: { name: 'Amuleto da Sorte', slot: 'tool', rarity: 'épico', price: 700, stats: { luck: 15 }, color: '#46e0a0' },

  // pergaminhos de habilidade: usar consome o item e ensina a habilidade (e eles podem ser trocados/vendidos)
  scroll_dash: { name: 'Pergaminho: Investida', slot: null, kind: 'scroll', skill: 'dash', rarity: 'incomum', price: 80, stats: {}, color: '#7ad7ff' },
  scroll_fireball: { name: 'Pergaminho: Bola de Fogo', slot: null, kind: 'scroll', skill: 'fireball', rarity: 'raro', price: 250, stats: {}, color: '#ff7a3a' },
  scroll_shield: { name: 'Pergaminho: Escudo', slot: null, kind: 'scroll', skill: 'shield', rarity: 'incomum', price: 150, stats: {}, color: '#8ab4ff' },
  scroll_heal: { name: 'Pergaminho: Cura', slot: null, kind: 'scroll', skill: 'heal', rarity: 'raro', price: 220, stats: {}, color: '#74f0a7' },
  scroll_whirl: { name: 'Pergaminho: Redemoinho', slot: null, kind: 'scroll', skill: 'whirl', rarity: 'épico', price: 500, stats: {}, color: '#e0a0ff' },
};

// Habilidades: 3 níveis. Os números abaixo são usados pelo cliente (efeito) e pelo servidor (custo de evolução).
export const SKILLS = {
  dash: { name: 'Investida', key: '1', cd: [6, 5, 4], upgradeBase: 100, desc: 'Avança rápido na direção em que você olha.' },
  fireball: { name: 'Bola de Fogo', key: '2', cd: [5, 4.2, 3.5], dmg: [18, 28, 40], upgradeBase: 160, desc: 'Lança uma bola de fogo que causa dano.' },
  shield: { name: 'Escudo', key: '3', cd: [14, 12, 10], dur: [3, 4, 5], upgradeBase: 140, desc: 'Reduz o dano recebido pela metade por alguns segundos.' },
  heal: { name: 'Cura', key: '4', cd: [16, 14, 12], heal: [30, 50, 80], upgradeBase: 140, desc: 'Recupera vida.' },
  whirl: { name: 'Redemoinho', key: '5', cd: [10, 8.5, 7], dmg: [20, 32, 46], upgradeBase: 220, desc: 'Ataca todos os inimigos ao redor.' },
};
export const MAX_SKILL_LEVEL = 3;

// ---------- bestiário ----------
// Cada espécie tem nível (lv 1 = fraca ... 18 = muito forte), um "corpo" (base) e uma aparência (hue/sat/lum/scale/acc).
// Vida, ataque, moedas e XP crescem com o nível; o papel (role) muda o equilíbrio entre vida, dano e velocidade.
const ROLE = { norm: [1, 1, 1], tank: [1.7, 0.85, 0.85], fast: [0.7, 0.95, 1.35], glass: [0.6, 1.4, 1.05], brute: [1.4, 1.3, 0.9] };
const spec = (name, base, lv, role, look = {}, biomes = []) => {
  const [rh, ra, rs] = ROLE[role];
  return {
    name, base, lv, biomes, look,
    hp: Math.round(26 * 1.19 ** (lv - 1) * rh),
    atk: Math.round(5.5 * 1.13 ** (lv - 1) * ra * 10) / 10,
    speed: Math.round(2.3 * rs * (1 + lv * 0.012) * 10) / 10,
    coins: [Math.max(2, Math.round(2.2 * 1.2 ** (lv - 1))), Math.max(4, Math.round(5 * 1.2 ** (lv - 1)))],
    xp: Math.round(10 * 1.2 ** (lv - 1)),
    r: 0.8, aggro: 16 + (role === 'fast' ? 5 : 0),
  };
};
// medidas de colisão (r) por corpo
const BODY_R = { slime: 0.85, brute: 1.15, wolf: 1.0, scorpion: 0.9, skeleton: 0.8, bat: 0.8, spider: 0.95, golem: 1.5, ghost: 0.9, dragon: 3.8 };
const SP = {
  // campos, fazenda e praia (lv 1-4)
  slime: spec('Gosma', 'slime', 1, 'norm', {}, ['grass', 'farm', 'beach']),
  rat: spec('Ratazana', 'wolf', 1, 'fast', { hue: 20, sat: 0.4, lum: 0.75, scale: 0.5 }, ['grass', 'farm']),
  slime_blue: spec('Gosma Azul', 'slime', 2, 'norm', { hue: 170 }, ['grass', 'farm', 'beach']),
  crab: spec('Caranguejo', 'scorpion', 2, 'tank', { hue: -8, scale: 0.8 }, ['beach']),
  boar: spec('Javali', 'wolf', 3, 'brute', { hue: 25, sat: 0.7, lum: 0.7, scale: 0.9, acc: ['horns'] }, ['grass', 'farm']),
  slime_red: spec('Gosma Rubra', 'slime', 3, 'glass', { hue: -110, scale: 1.1 }, ['grass', 'beach']),
  // floresta (lv 3-8)
  goblin: spec('Goblin', 'skeleton', 3, 'fast', { hue: 70, sat: 1.1, lum: 0.6, scale: 0.75 }, ['forest']),
  spider: spec('Aranha', 'spider', 4, 'fast', {}, ['forest']),
  brute: spec('Bruto', 'brute', 5, 'brute', {}, ['forest', 'castle']),
  wolf_dark: spec('Lobo Sombrio', 'wolf', 6, 'norm', { hue: -10, sat: 0.3, lum: 0.35, acc: ['glow'] }, ['forest']),
  spider_giant: spec('Aranha Venenosa', 'spider', 7, 'glass', { hue: 90, scale: 1.4 }, ['forest']),
  treant: spec('Tronco Vivo', 'golem', 8, 'tank', { hue: 70, sat: 0.9, lum: 0.75, acc: ['spikes'] }, ['forest']),
  // deserto (lv 4-10)
  scorpion: spec('Escorpião', 'scorpion', 4, 'norm', {}, ['desert']),
  vulture: spec('Abutre', 'bat', 5, 'fast', { hue: 30, sat: 0.5, lum: 0.7, scale: 1.2 }, ['desert']),
  mummy: spec('Múmia', 'skeleton', 6, 'tank', { hue: 40, sat: 0.55, lum: 0.9 }, ['desert']),
  scorpion_black: spec('Escorpião Negro', 'scorpion', 7, 'glass', { hue: 0, sat: 0.1, lum: 0.3, scale: 1.15, acc: ['glow'] }, ['desert']),
  sand_golem: spec('Golem de Areia', 'golem', 9, 'tank', { hue: 38, sat: 0.7, lum: 1.15 }, ['desert']),
  // montanhas geladas (lv 6-12)
  wolf: spec('Lobo', 'wolf', 6, 'fast', {}, ['snow']),
  slime_ice: spec('Gosma de Gelo', 'slime', 7, 'norm', { hue: 55, lum: 1.25, scale: 1.2 }, ['snow']),
  wolf_white: spec('Lobo Branco', 'wolf', 8, 'norm', { hue: 0, sat: 0.1, lum: 1.45, scale: 1.1 }, ['snow']),
  bat_frost: spec('Morcego Gélido', 'bat', 9, 'fast', { hue: 90, lum: 1.2 }, ['snow']),
  yeti: spec('Yeti', 'brute', 10, 'tank', { hue: 195, sat: 0.2, lum: 1.45, scale: 1.2 }, ['snow']),
  ice_golem: spec('Golem de Gelo', 'golem', 12, 'tank', { hue: 175, sat: 0.9, lum: 1.3, acc: ['spikes'] }, ['snow']),
  // ruínas (lv 8-15)
  skeleton: spec('Esqueleto', 'skeleton', 8, 'norm', {}, ['ruins']),
  bat: spec('Morcego Noturno', 'bat', 9, 'fast', {}, ['ruins', 'castle']),
  ghost: spec('Fantasma', 'ghost', 10, 'glass', {}, ['ruins']),
  skeleton_knight: spec('Esqueleto Cavaleiro', 'skeleton', 11, 'brute', { hue: 215, sat: 0.8, lum: 0.65, scale: 1.25 }, ['ruins']),
  golem_stone: spec('Golem de Pedra', 'golem', 12, 'tank', {}, ['ruins']),
  wraith: spec('Espectro', 'ghost', 13, 'glass', { hue: 70, sat: 1.2, lum: 0.8, scale: 1.25, acc: ['horns'] }, ['ruins']),
  necromancer: spec('Necromante', 'skeleton', 14, 'glass', { hue: 270, sat: 1.2, lum: 0.55, acc: ['crown'] }, ['ruins']),
  // castelo (lv 13-18)
  imp: spec('Diabrete', 'bat', 13, 'fast', { hue: 150, sat: 1.3, lum: 0.9, acc: ['horns'] }, ['castle']),
  ogre_dark: spec('Ogro Negro', 'brute', 14, 'brute', { hue: -5, sat: 0.3, lum: 0.4, scale: 1.3, acc: ['spikes'] }, ['castle']),
  slime_lava: spec('Gosma de Lava', 'slime', 15, 'norm', { hue: -75, sat: 1.4, lum: 1.0, scale: 1.4, acc: ['glow'] }, ['castle']),
  dark_knight: spec('Cavaleiro Sombrio', 'skeleton', 16, 'brute', { hue: 260, sat: 0.4, lum: 0.3, scale: 1.35, acc: ['crown', 'glow'] }, ['castle']),
  reaper: spec('Ceifador', 'ghost', 17, 'glass', { hue: 0, sat: 0, lum: 0.25, scale: 1.5, acc: ['horns', 'glow'] }, ['castle']),
  golem_lava: spec('Golem de Magma', 'golem', 18, 'tank', { hue: -80, sat: 1.5, lum: 1.1, scale: 1.2, acc: ['spikes', 'glow'] }, ['castle']),
};
// chefes: stats escritos à mão. "at" = onde nascem; "gate" = só aparecem para quem já avançou na carreira.
const boss = (name, base, o) => ({ name, base, boss: true, biomes: [], aggro: 34, ...o });
const BOSSES = {
  crabking: boss('Rei Caranguejo', 'scorpion', { lv: 5, hp: 420, atk: 14, speed: 2.6, coins: [30, 55], xp: 90, r: 2.1, at: 'beach', look: { hue: -8, scale: 2.4, acc: ['crown'] } }),
  ent: boss('Ancião da Floresta', 'golem', { lv: 9, hp: 1100, atk: 22, speed: 2.2, coins: [60, 110], xp: 220, r: 3.0, at: 'forest', look: { hue: 85, sat: 0.9, lum: 0.8, scale: 2.2, acc: ['spikes', 'crown'] } }),
  pharaoh: boss('Faraó Escorpião', 'scorpion', { lv: 11, hp: 1500, atk: 26, speed: 3.0, coins: [80, 140], xp: 300, r: 2.6, at: 'desert', look: { hue: 45, sat: 1.3, lum: 1.25, scale: 2.6, acc: ['crown', 'glow'] } }),
  alpha: boss('Lobo Alfa Gélido', 'wolf', { lv: 13, hp: 1800, atk: 30, speed: 4.2, coins: [100, 170], xp: 380, r: 2.4, at: 'snow', look: { hue: 0, sat: 0.1, lum: 1.5, scale: 2.4, acc: ['glow'] } }),
  lich: boss('Rei Lich', 'skeleton', { lv: 15, hp: 2300, atk: 36, speed: 2.8, coins: [130, 210], xp: 480, r: 2.4, at: 'ruins', look: { hue: 275, sat: 1.3, lum: 0.6, scale: 2.5, acc: ['crown', 'horns', 'glow'] } }),
  kingslime: boss('Rei Gosma', 'slime', { lv: 16, hp: 2600, atk: 40, speed: 2.4, coins: [160, 240], xp: 600, r: 2.9, at: 'castle', look: {} }),
  dragon: boss('Dragão Ancião', 'dragon', { lv: 20, hp: 7500, atk: 62, speed: 3.4, coins: [500, 800], xp: 2500, r: 3.8, at: 'castle', gate: 7, aggro: 60, phases: true, look: {} }),
};
export const ENEMIES = {};
for (const [id, d] of Object.entries(SP)) ENEMIES[id] = { ...d, r: BODY_R[d.base] * (d.look.scale ?? 1) };
for (const [id, d] of Object.entries(BOSSES)) ENEMIES[id] = d;
// espécies que contam como outra na carreira (ex.: "Gosma Azul" também vale como Gosma)
for (const [id, d] of Object.entries(ENEMIES)) d.family = id;
ENEMIES.slime_blue.family = ENEMIES.slime_red.family = 'slime';
ENEMIES.slime_blue.family = 'slime';

export const RULES = {
  startCoins: 100,
  marketFeePct: 0.05, // 5% de cada venda no mercado é queimado (reduz inflação)
  tournamentRakePct: 0.1, // 10% do prêmio é queimado
  tradeTtlMs: 10 * 60_000,
  maxCoinsPerHour: 1500, // teto de moedas ganhas matando inimigos (anti-abuso)
  minClaimGapMs: 350,
  maxPrice: 1_000_000,
  battleFee: 10, // aposta de cada jogador no duelo (vai para a custódia)
  battleRakePct: 0.1, // 10% do total é destruído
  battleSeconds: 90,
  battleCooldownMs: 450,
  attackCooldownMs: 400, // intervalo mínimo entre golpes (servidor)
  reviveMs: 2500,
  bossRespawnMs: 120_000,
  eliteChance: 0.07, // chance de um monstro nascer "Elite" (mais vida/dano, mais recompensa)
};

export const baseStats = (level) => ({ hp: 100 + 10 * (level - 1), atk: 8 + 2 * (level - 1), def: 0, speed: 0, pickup: 0, luck: 0 });
export const levelFromXp = (xp) => Math.floor(Math.sqrt(xp / 40)) + 1;
export const xpForLevel = (level) => 40 * (level - 1) * (level - 1);
