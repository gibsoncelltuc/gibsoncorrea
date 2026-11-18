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

## Figurino (campos de "outfits")
jacket, pants, boots (obrigatorios) | hat + cap (cor) | hair (cor, com hat: hair) | hairStyle: long|bun | beard (cor) | glasses: true | tie (cor da gravata) | pele (tom de pele) | sash, belt, buttons (cor) | build: stout|lanky | rifle: true (soldado). Caricaturas prontas: FIGURINOS_FAMOSOS.md

## Animais
"animals": [["pig", x, z, "stand|walk", escala]] , [["chicken", ...]] ; "emus": true

## Objetos que entram SOZINHOS quando a narracao cita a palavra
- barrel  <- \bbarril\b|\bbarris\b|aguardente|cerveja|\bvinho\b|\brum\b
- crate  <- caixote|\bcaixas\b|\bcarga\b|mercadoria
- cannon  <- \bcanhao\b|\bcanhoes\b|artilharia
- tools/bucket  <- \bbaldes?\b|\bpoco\b
- nature/fountain  <- \bfonte\b|chafariz
- war/flagpole  <- \bbandeiras?\b|estandarte
- war/drum  <- \btambor\b|\btambores\b
- war/sandbags  <- trincheira|barricada|sacos de areia
- war/shield  <- \bescudos?\b
- nature/haybale  <- \bfeno\b|trigo|plantac|colheita
- nature/scarecrow  <- espantalho
- tools/lantern  <- lanterna|lampiao|lamparina
- tools/ladder  <- \bescadas?\b
- tools/wheelbarrow  <- carrinho de mao
- tools/anvil  <- ferreiro|bigorna
- kit/tulip_red  <- \btulipas?\b|\bbulbos?\b|\bflor\b|\bflores\b
- kit/grave  <- \bcova\b|tumulo|enterr|caixao|cemiterio
- nature/flowerbed  <- \bbatatas?\b|\bhorta\b|\blegumes?\b
- kit/ball  <- \bbola\b|futebol|\bgol\b|partida|estadio
- kit/kettle  <- \bchaleira\b|\bpanelas?\b|\bsopa\b|caldeirao
- kit/apple  <- \bmaca\b|\bmacas\b|\bmacieiras?\b
- kit/bathtub  <- \bbanheira\b|\bbanho\b
- kit/feather  <- \bpena\b
- kit/crown  <- \bcoroa\b
- nature/picket_fence  <- \bcerca\b|cercado|curral|fazenda|\bhorta\b
- kit/cake_table  <- \bbolos?\b|\bdoces?\b|confeit|padaria|\bpastel\b|\bpasteis\b
- kit/throne  <- \btrono\b|coroad  (so interior)
- kit/campfire  <- fogueira|acampamento|acamparam
- kit/tent  <- \btenda|barraca de campanha|acampamento  (fundo, so cena externa)
- kit/chest  <- \bbau\b|tesouro|\bcofre
- kit/stall  <- \bfeira\b|\bmercado\b|\bbarracas?\b|\bvendedor\b
- vehicles/locomotive  <- \btrem\b|locomotiva|ferrovia  (fundo, so cena externa)
- vehicles/wagon  <- \bcarrocas?\b  (fundo, so cena externa)
- vehicles/tank  <- tanque de guerra|blindado  (fundo, so cena externa)
- buildings/castle_tower  <- \btorres?\b|\bmuralhas?\b|\bcastelo\b|\bfortaleza\b|\bpalacio\b  (fundo, so cena externa)
- buildings/windmill  <- \bmoinhos?\b  (fundo, so cena externa)
- buildings/church  <- \bigreja\b|\bcatedral\b  (fundo, so cena externa)
- buildings/lighthouse  <- \bfarol\b  (fundo, so cena externa)
- buildings/bridge  <- \bponte\b  (fundo, so cena externa)

## Biblioteca 3D completa (use em "props": [["pasta/nome", x, z, escala]])
- kit: apple, ball, bathtub, cake_table, campfire, chest, cross, crown, feather, grave, kettle, pisa_tower, porch, room_shop, room_stone, room_wood, stall, tent, throne, tulip_bed, tulip_purple, tulip_red, tulip_striped, tulip_yellow
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
