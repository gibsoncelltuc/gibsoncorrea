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
bottle, mug, paper, book, lantern, pitchfork, staff, flag, torch, bag, coin, spyglass, shovel, tulip, money (notas de dolar), sword (espada)

## Chapeus ("hat" no figurino)
beret, bonnet, bowler, cap, crown, fez, hair, helmet, shako, shako_tall, slouch, straw, tophat, turban, wizard

## Figurino (campos de "outfits")
jacket, pants, boots (obrigatorios) | hat + cap (cor) | hair (cor, com hat: hair) | hairStyle: long|bun | beard (cor) | glasses: true | tie (cor da gravata) | pele (tom de pele) | sash, belt, buttons (cor) | build: stout|lanky | rifle: true (soldado). Caricaturas prontas: FIGURINOS_FAMOSOS.md

## Profissoes prontas ("profissao" no figurino: {"PAD": {"profissao": "padeiro"}} e ajuste as cores se quiser)
padeiro, agricultor, nobre, politico, empresario, rei, general, soldado, marinheiro, cientista, medico, comerciante, pescador, padre, camponesa, jornalista. Cada personagem ganha barba, bigode ou oculos proprios pelo nome + variante; para fixar: "beard": "#cor" | "moustache": "#cor" | "glasses": true/false. Bandeira na mao: "holdCol" e "holdCol2" no figurino mudam as duas cores.

## Animais
"animals": [["pig", x, z, "stand|walk", escala]] ; tambem "chicken", "goose", "horse" (cavalo 3D), "bear" (urso 3D) ; "emus": true. Modelos 3D prontos na raiz de web/assets: horse, sheep, bear, emu, pig, boat, ship, cannon, barrel, crate, tent, mgun (metralhadora).

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
- kit/crookes_tube  <- \btubo\b|\btubos\b
- kit/xray_plate  <- \bchapa\b|\bossos\b|\braio x\b|\braios x\b|radiografia|\btela\b
- kit/brass_nose  <- \bnariz\b|\bnarizes\b|protese
- kit/wash_basin  <- \bbacia\b|\bbacias\b|\blavar\b|lavassem|\bcloro\b|clorada
- kit/snake_ring  <- \bcobras?\b|serpentes?|\banel\b|benzeno|\brabo\b
- kit/postit  <- post-?it|bloquinhos?|marcadores?|hinario|papeizinhos
- kit/burr  <- carrapichos?|velcro|ganchinhos?
- kit/stove  <- \bfogao\b|\bfogoes\b|borracha|vulcaniz|enxofre
- kit/balloon  <- \bbalao\b|\bbaloes\b
- kit/curie_box  <- \bcadernos?\b|\bchumbo\b|radioativ|\bfrascos?\b
- kit/beehive  <- \bcolmeias?\b|\babelhas?\b|\bfavos?\b|\bmel\b
- kit/clipper  <- maquina de raspar|\braspou\b|\braspar\b|\braspada\b|\bcareca\b
- kit/tower_catch  <- mechazilla|pauzinhos|torre de lancamento  (fundo, so cena externa)
- kit/volcano  <- \bvulcao\b|\bvulcoes\b  (fundo, so cena externa)
- kit/bitcoin  <- \bbitcoins?\b|moeda digital|dinheiro digital
- kit/miners  <- \bcomputadores\b|mineradoras?|\bservidores\b
- kit/boardgame  <- tabuleiro|jogo de mesa
- kit/monkey_pong  <- \bmacacos?\b|\bpong\b|\bpager\b
- kit/tequila_bolt  <- \btequila\b|teslaquila|\bgarrafas?\b
- kit/apple  <- \bmaca\b|\bmacas\b|\bmacieiras?\b
- kit/bathtub  <- \bbanheira\b|\bbanho\b
- kit/crown  <- \bcoroa\b

## Biblioteca 3D completa (use em "props": [["pasta/nome", x, z, escala]])
- kit: apple, ball, balloon, balloon_air, barrel_r, bathtub, beehive, bitcoin, boardgame, booster_air, brass_nose, burr, cake_table, campfire, chest, clipper, crookes_tube, cross, crown, curie_box, ear_jar, feather, fire, flag_pole, golden_stool, grave, kettle, lobster, microwave, miners, monkey_pong, petri, pisa_tower, porch, postit, ring, room_shop, room_stone, room_wood, snake_ring, stall, stove, syringe, tent, tequila_bolt, throne, tower, tower_catch, tulip_bed, tulip_purple, tulip_red, tulip_striped, tulip_yellow, volcano, wash_basin, xray_plate
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
