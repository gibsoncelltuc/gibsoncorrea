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

export const ENEMIES = {
  slime: { name: 'Gosma', hp: 30, atk: 6, speed: 2.2, coins: [3, 8], xp: 12 },
  brute: { name: 'Bruto', hp: 90, atk: 14, speed: 2.8, coins: [12, 24], xp: 40 },
  scorpion: { name: 'Escorpião', hp: 55, atk: 10, speed: 3.0, coins: [6, 12], xp: 22 },
  wolf: { name: 'Lobo', hp: 70, atk: 12, speed: 3.6, coins: [8, 16], xp: 28 },
  skeleton: { name: 'Esqueleto', hp: 85, atk: 15, speed: 2.9, coins: [10, 20], xp: 34 },
  kingslime: { name: 'Rei Gosma', hp: 900, atk: 28, speed: 2.4, coins: [60, 100], xp: 200 },
};

export const RULES = {
  startCoins: 100,
  marketFeePct: 0.05, // 5% de cada venda no mercado é queimado (reduz inflação)
  tournamentRakePct: 0.1, // 10% do prêmio é queimado
  tradeTtlMs: 10 * 60_000,
  maxCoinsPerHour: 450, // teto de moedas ganhas matando inimigos (anti-abuso)
  minClaimGapMs: 350,
  maxPrice: 1_000_000,
  battleFee: 10, // aposta de cada jogador no duelo (vai para a custódia)
  battleRakePct: 0.1, // 10% do total é destruído
  battleSeconds: 90,
  battleCooldownMs: 450,
};

export const baseStats = (level) => ({ hp: 100 + 10 * (level - 1), atk: 8 + 2 * (level - 1), def: 0, speed: 0, pickup: 0, luck: 0 });
export const levelFromXp = (xp) => Math.floor(Math.sqrt(xp / 40)) + 1;
export const xpForLevel = (level) => 40 * (level - 1) * (level - 1);
