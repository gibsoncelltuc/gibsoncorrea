# Arena das Moedas

RPG de ação 3D no navegador (Three.js) com economia entre jogadores: **loja, equipamentos visíveis no
personagem, habilidades, mercado, trocas diretas e torneios**. A moeda é **interna do jogo** (não vale dinheiro).

## Como jogar

```
cd arena-game
npm install          # instala three e ws
npm start            # abre em http://127.0.0.1:8800
HOST=0.0.0.0 npm start   # amigos na mesma rede entram por http://SEU-IP:8800
npm test             # 9 testes da economia
```

Controles: **WASD** mover · **Espaço**/clique atacar · **Q/E** ou botão direito + arrastar para girar a câmera ·
roda do mouse zoom · **Shift** correr · **1–5** habilidades · **B** Loja · **I** Inventário · **K** Habilidades ·
**M** Mercado · **T** Troca · **O** Torneios · **H** Ajuda.

## O que tem

| Recurso | Como funciona |
|---|---|
| Moedas | Ganha derrotando inimigos (Gosma, Bruto) e em torneios. Teto de 450 moedas/hora por jogador. |
| Loja | 17 itens: armas, cabeça, corpo, ferramentas e **pergaminhos de habilidade**. |
| Equipamento | Muda atributos (ataque, defesa, vida, velocidade, coleta, sorte) **e o visual** do personagem. |
| Habilidades | Investida, Bola de Fogo, Escudo, Cura, Redemoinho. Aprende-se usando o pergaminho e evolui até o nível 3 com moedas. |
| Mercado | Anuncie qualquer item livre (inclusive pergaminhos). O item fica em custódia até vender ou cancelar. Taxa de 5% destruída. |
| Troca direta | Dois jogadores trocam itens e moedas de forma atômica; revalida tudo no momento do "Aceitar"; expira em 10 min. |
| Torneios | Mata-mata de 4 ou 8, simulado no servidor com os atributos (equipamento importa). Vagas vazias viram bots. 10% do prêmio é destruído. |
| Personagem | Nível sobe com XP e aumenta vida e ataque. |

## Segurança da economia (o que está garantido e o que não está)

Garantido (testado em `test/economy.test.js`, incluindo um teste aleatório de 1.500 operações):
- Toda compra, venda, troca e torneio é validada no **servidor**; o cliente só pede.
- **Auditoria**: `moedas criadas = moedas dos jogadores + custódia de torneios + moedas destruídas`, verificada a cada operação.
- Não dá para comprar sem saldo, vender item equipado, comprar o próprio anúncio, comprar duas vezes o mesmo anúncio nem trocar item que já foi vendido.
- Recompensas de inimigo têm intervalo mínimo (350 ms) e teto por hora.

**Limites conhecidos (importante):**
- O combate roda no navegador. Um jogador malicioso pode avisar ao servidor que matou inimigos sem ter matado.
  O teto de 450 moedas/hora limita o estrago, mas **não impede**. Para valer dinheiro real, o combate precisa
  rodar no servidor.
- Não há senha: o personagem é guardado por um token no navegador (perdeu o token, perdeu a conta).
- Ainda não há outros jogadores visíveis na mesma arena em tempo real (a economia é multiplayer; o combate, por ora, é solo).
- Dados salvos em `data/game.json` (um arquivo). Serve para protótipo, não para milhares de jogadores.

## Sobre ligar a moeda a um token de verdade

Não está ligada. É uma decisão de produto e jurídica (ver conversa): primeiro valide a economia só dentro do jogo.
Se um dia houver token, o caminho seguro é: combate no servidor, contas com login real, saques limitados e revisão jurídica.
Nada aqui mexe com carteiras ou chaves privadas.

## Próximos passos sugeridos

1. Combate e inimigos no servidor (anti-trapaça) e jogadores visíveis na mesma arena.
2. Torneio com duelo real (PvP) em vez de simulação.
3. Mais itens, raridades, visuais, mapas e missões; balancear preços com dados de jogo.
4. Contas com login e banco de dados (SQLite).
