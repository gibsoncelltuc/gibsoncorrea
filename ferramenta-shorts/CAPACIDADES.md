# CAPACIDADES DA FERRAMENTA (gerado por capacidades.py - nao edite a mao)

Escreva o roteiro usando SO o que esta aqui. O que nao estiver, a folha 2 acusa como risco.

## Cenarios ("set" no topo ou na cena)
outback, countryside, arctic, palace, harbor, mountain, medieval, jungle, hall, stadium, street  | interiores: "interior": "madeira" | "pedra" | "loja"

## Planos ("shot")
two (medio, 2 pessoas) | close (rosto) | group (3-4, corpo inteiro) | low (camera baixa, virada) | track (andando) | ABERTOS: reveal (grua abrindo), crowd (multidao), orbit (camera girando)

## Hora e clima
"hora": dia | amanhecer | pordosol | noite ; "clima": limpo | chuva | tempestade | neve | neblina | calor (a ferramenta tambem le essas palavras na narracao)

## Expressoes (3o campo do "who": "FAZ:0:angry")
angry, bored, cry, dazed, grin, laugh, lick, nervous, neutral, pained, relief, relief_open, sad, scared, shock, shout, smile, smile_closed, smug, stern, surprised, suspicious, whistle

## Acoes e interacoes
"acao": conversar | discutir | comemorar | dancar | nenhuma ; "interacao": empurrar | discutir | cochichar | entregar | susto | reverencia | pular ; "chega": true (entra andando) ; "batalha": true (tropa, tiros, fuga) ; "caminhoes": true

## Objeto na mao (4o campo do "who": "FAZ:0:stern:coin")
bottle, mug, paper, book, lantern, pitchfork, staff, flag, torch, bag, coin, spyglass, shovel, tulip, money (notas de dolar)

## Chapeus ("hat" no figurino)
beret, bonnet, bowler, cap, crown, fez, hair, helmet, shako, shako_tall, slouch, straw, tophat, turban, wizard

## Animais
"animals": [["pig", x, z, "stand|walk", escala]] , [["chicken", ...]] ; "emus": true

## Objetos que entram SOZINHOS quando a narracao cita a palavra
- barrel  <- barril|barris|aguardente|cerveja|vinho|rum\b
- crate  <- caixote|caixas|carga|mercadoria
- cannon  <- canhao|canhoes|artilharia
- tools/bucket  <- balde|\bpoco\b
- nature/fountain  <- \bfonte\b|chafariz
- war/flagpole  <- bandeira|estandarte
- war/drum  <- tambor|tambores
- war/sandbags  <- trincheira|barricada|sacos de areia
- war/shield  <- escudo
- nature/haybale  <- \bfeno\b|trigo|plantac|colheita
- nature/scarecrow  <- espantalho
- tools/lantern  <- lanterna|lampiao|lamparina
- tools/ladder  <- escada
- tools/wheelbarrow  <- carrinho de mao
- tools/anvil  <- ferreiro|bigorna
- kit/tulip_red  <- tulipa|bulbo|\bflor\b|flores
- kit/grave  <- \bcova\b|tumulo|enterr|caixao|cemiterio
- nature/flowerbed  <- batata|horta|legume
- kit/ball  <- \bbola\b|futebol|\bgol\b|partida|estadio
- kit/kettle  <- chaleira|panela|\bsopa\b|caldeirao
- nature/picket_fence  <- \bcerca\b|cercado|curral|fazenda|\bhorta\b
- kit/cake_table  <- \bbolo|\bdoce|confeit|padaria|pastel
- kit/throne  <- \btrono\b|coroad  (so interior)
- kit/campfire  <- fogueira|acampamento|acamparam
- kit/tent  <- \btenda|barraca de campanha|acampamento  (fundo, so cena externa)
- kit/chest  <- \bbau\b|tesouro|\bcofre
- kit/stall  <- \bfeira\b|mercado|barraca|vendedor
- vehicles/locomotive  <- \btrem\b|locomotiva|ferrovia  (fundo, so cena externa)
- vehicles/wagon  <- carroca  (fundo, so cena externa)
- vehicles/tank  <- tanque de guerra|blindado  (fundo, so cena externa)
- buildings/castle_tower  <- torre|muralha|castelo|fortaleza|palacio  (fundo, so cena externa)
- buildings/windmill  <- moinho  (fundo, so cena externa)
- buildings/church  <- igreja|catedral  (fundo, so cena externa)
- buildings/lighthouse  <- \bfarol\b  (fundo, so cena externa)
- buildings/bridge  <- \bponte\b  (fundo, so cena externa)

## Biblioteca 3D completa (use em "props": [["pasta/nome", x, z, escala]])
- kit: ball, cake_table, campfire, chest, cross, grave, kettle, lobster, porch, room_shop, room_stone, room_wood, stall, tent, throne, tulip_bed, tulip_purple, tulip_red, tulip_striped, tulip_yellow
- buildings: apartment, barn, bridge, castle_tower, church, house_blue, house_small, house_two, lighthouse, shop, skyscraper, windmill
- vehicles: airplane, bicycle, car, car_blue, helicopter, jeep, locomotive, motorboat, motorcycle, sailboat, tank, taxi, truck, wagon
- nature: bench, bush, flowerbed, fountain, haybale, lamppost, picket_fence, rocks, scarecrow, tree_birch, tree_oak, tree_palm, tree_pine
- tools: anvil, axe, broom, bucket, hammer, ladder, lantern, pitchfork, rake, saw, scythe, shovel, telescope, wheelbarrow
- war: bow, bugle, bunker, cannonballs, drum, flagpole, helmet_army, helmet_knight, musket, pistol, quiver, sandbags, shield, sword
- soltos: barrel, crate, cannon, ship

## Sons ("sfx": ["nome@quadro"])
gun, cannon, squeal, snuffle, gibber, laughs, whoosh, ding, sting, thump, tick, creak, paper

## NAO existe (nao escreva cena que dependa disto)
cavalo e outros animais fora da lista; nadar, cavalgar, escalar, sentar, deitar; barco se movendo; fogo/incendio grande; personagem dentro de veiculo aparecendo; mais de 4 personagens principais na mesma cena fechada.
