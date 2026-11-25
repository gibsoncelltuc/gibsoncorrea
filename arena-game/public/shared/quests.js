// Modo carreira: capítulos em ordem. O servidor valida cada progresso; o cliente só mostra.
// type: talk (falar com NPC) | kill (derrotar N de um inimigo) | collect (pegar itens no mapa) | reach (chegar a um local)
export const CHAPTERS = [
  { id: 1, title: 'Bem-vindo à Vila Moeda', text: 'Fale com o Prefeito Ouro, na praça da vila (chegue perto e aperte E).', type: 'talk', npc: 'mayor', goal: 1, reward: { coins: 40, xp: 30 } },
  { id: 2, title: 'Limpeza dos Campos', text: 'Derrote 8 Gosmas nos campos ao redor da vila.', type: 'kill', enemy: 'slime', goal: 8, reward: { coins: 80, xp: 60 } },
  { id: 3, title: 'Cristais da Floresta', text: 'Colete 5 cristais brilhantes na Floresta Sussurrante (norte, siga a estrada).', type: 'collect', ids: ['cr1', 'cr2', 'cr3', 'cr4', 'cr5'], goal: 5, loc: 'forest', reward: { coins: 120, xp: 90 } },
  { id: 4, title: 'Dunas Escaldantes', text: 'Derrote 8 Escorpiões no Deserto (leste, siga a estrada).', type: 'kill', enemy: 'scorpion', goal: 8, loc: 'desert', reward: { coins: 160, xp: 130 } },
  { id: 5, title: 'Frio Mortal', text: 'Derrote 8 Lobos nas Montanhas Geladas (oeste, siga a estrada).', type: 'kill', enemy: 'wolf', goal: 8, loc: 'snow', reward: { coins: 200, xp: 170 } },
  { id: 6, title: 'Ruínas Esquecidas', text: 'Vá até as Ruínas Antigas (noroeste) e derrote 6 Esqueletos.', type: 'kill', enemy: 'skeleton', goal: 6, loc: 'ruins', reward: { coins: 260, xp: 230 } },
  { id: 7, title: 'O Rei Gosma', text: 'Suba ao Castelo (nordeste) e derrote o Rei Gosma, guardião dos portões. Leve boa armadura e habilidades!', type: 'kill', enemy: 'kingslime', goal: 1, loc: 'castle', reward: { coins: 500, xp: 400 } },
  { id: 8, title: 'O Dragão Ancião', text: 'O verdadeiro chefão despertou no Castelo! Derrote o Dragão Ancião, sozinho ou com amigos, para zerar o jogo.', type: 'kill', enemy: 'dragon', goal: 1, loc: 'castle', reward: { coins: 1500, xp: 1500, item: 'crown_hero' } },
];
export const FINAL_TITLE = 'Herói da Vila Moeda';
