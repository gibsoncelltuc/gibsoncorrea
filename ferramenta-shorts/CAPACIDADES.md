# CAPACIDADES DA FERRAMENTA (gerado por capacidades.py - nao edite a mao)

Escreva o roteiro usando SO o que esta aqui. O que nao estiver, a folha 2 acusa como risco.

## Cenarios ("set" no topo ou na cena)
outback, countryside, arctic, palace, harbor, mountain, medieval, jungle, hall, stadium, street  | interiores: "interior": "madeira" | "pedra" | "loja"

## Planos ("shot")
two (medio, 2 pessoas) | close (rosto) | group (3-4, corpo inteiro) | low (camera baixa, virada) | track (andando) | ABERTOS: reveal (grua abrindo), crowd (multidao), orbit (camera girando)

## Hora e clima
"hora": dia | amanhecer | pordosol | noite ; "clima": limpo | chuva | tempestade | neve | neblina | calor (a ferramenta tambem le essas palavras na narracao)

## Expressoes (3o campo do "who": "FAZ:0:angry")
angry, annoyed, bored, cry, dazed, determined, distrust, grin, happy, laugh, lick, nervous, neutral, pained, pleading, relief, relief_open, sad, scared, shock, shout, smile, smile_closed, smug, stern, surprised, suspicious, whistle, worried

## Acoes e interacoes
"acao": conversar | discutir | comemorar | dancar | nenhuma ; "interacao": empurrar | discutir | cochichar | entregar | susto | reverencia | pular ; "chega": true (entra andando) ; "batalha": true (tropa, tiros, fuga) ; "caminhoes": true

## Objeto na mao (4o campo do "who": "FAZ:0:stern:coin")
bottle, mug, paper, book, lantern, pitchfork, staff, flag, torch, bag, coin, spyglass, shovel, tulip, money (notas de dolar), sword (espada)

## Chapeus ("hat" no figurino)
adrian, beret, bibico, bicorne, bonnet, boonie, bowler, brodie, cap, colonial, crown, fez, hair, helmet, kepi, m1, pickelhaube, quepe, shako, shako_tall, slouch, stahlhelm, straw, tophat, tricorn, turban, wizard

## Figurino (campos de "outfits")
jacket, pants, boots (obrigatorios) | hat + cap (cor) | hair (cor, com hat: hair) | hairStyle: long|bun | beard (cor) | glasses: true | tie (cor da gravata) | pele (tom de pele) | sash, belt, buttons (cor) | build: stout|lanky | rifle: true (soldado). Caricaturas prontas: FIGURINOS_FAMOSOS.md

## Profissoes prontas ("profissao" no figurino: {"PAD": {"profissao": "padeiro"}} e ajuste as cores se quiser)
padeiro, agricultor, nobre, politico, empresario, rei, general, soldado, marinheiro, cientista, medico, comerciante, pescador, padre, camponesa, jornalista. Cada personagem ganha barba, bigode ou oculos proprios pelo nome + variante; para fixar: "beard": "#cor" | "moustache": "#cor" | "glasses": true/false. Bandeira na mao: "holdCol" e "holdCol2" no figurino mudam as duas cores.

## Animais (JA PRONTOS - NUNCA modele animal no Blender)
Entram SOZINHOS quando a narracao cita o animal (cachorro, gato, vaca/boi, ovelha, cabra/bode, porco, cavalo, burro/jumento, veado/cervo, raposa, lobo, coelho, leao, elefante, urso, galinha, galo, pato, ganso, gaivota, emu). Em cena andando/correndo (shot "track") o animal anda junto. Para posicionar a mao: "animals": [["dog", x, z]] com dog, cat, cow, sheep, goat, pig, horse, donkey, deer, fox, wolf, rabbit, lion, elephant, bear, chicken, rooster, duck, goose, gull; "emus": true. Desligar: "animais": false. Close de animal como objeto heroi: kit/dog_sit (cachorro sentado).

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
- kit/tower_mini  <- mechazilla|pauzinhos|torre de lancamento
- kit/volcano  <- \bvulcao\b|\bvulcoes\b  (fundo, so cena externa)
- kit/bitcoin  <- \bbitcoins?\b|moeda digital|dinheiro digital
- kit/miners  <- \bcomputadores\b|mineradoras?|\bservidores\b
- kit/boardgame  <- tabuleiro|jogo de mesa
- kit/monkey_pong  <- \bmacacos?\b|\bpong\b|\bpager\b
- kit/tequila_bolt  <- \btequila\b|teslaquila|\bgarrafas?\b
- kit/tires  <- \bpneus?\b
- kit/rocket  <- \bfoguete\b|\bfoguetes\b|falcon
- kit/roadster  <- \broadster\b|\btesla\b
- kit/ballot_box  <- \burnas?\b|cedulas?
- kit/helicopter_air  <- helicopteros?  (fundo, so cena externa)
- kit/bunker_bomb  <- \bbunker\b|antibunker
- kit/phone  <- \bcelular\b|\bselfie\b
- kit/prison  <- \bprisao\b|presidio|penitenciaria  (fundo, so cena externa)
- kit/white_house  <- casa branca  (fundo, so cena externa)
- kit/starlink_sat  <- \bsatelites?\b|starlink
- kit/starlink_dish  <- \bantena\b
- kit/ear_jar  <- \borelha\b
- kit/golden_stool  <- \bbanquinho\b
- kit/scroll  <- \btratado\b
- kit/cod  <- \bbacalhau\b
- kit/melon  <- \bmelancias?\b
- kit/whisky  <- \b(uísque|uisque|whisky)\b
- kit/logs  <- \b(toras?|troncos?)\b
- kit/searchlight  <- \bholofotes?\b
- kit/tv  <- \btelevisao\b|\btv\b
- kit/flamethrower  <- lanca.?chamas
- kit/extinguisher  <- \bextintor(es)?\b
- kit/cybertruck  <- \bcybertruck\b|\bpicapes?\b
- kit/steel_ball  <- \besferas?\b|\bbolas? de aco\b
- kit/apple  <- \bmaca\b|\bmacas\b|\bmacieiras?\b
- kit/bathtub  <- \bbanheira\b|\bbanho\b
- kit/crown  <- \bcoroa\b
- kit/feather  <- \bpenas? de (ave|ganso|escrever)\b|\bpluma\b
- kit/petri  <- \bplacas? de petri\b|\bmofo\b|\bbolor\b
- kit/microwave  <- \bmicro-?ondas\b|\bmicroondas\b
- kit/chocolate  <- \bchocolate\b
- kit/egg  <- \bovos?\b
- kit/popcorn  <- \bpipocas?\b|\bmilho\b
- kit/syringe  <- \binjecao\b|\binjecoes\b|\bseringa\b|\bvacina\b
- kit/kite  <- \bpipas?\b
- kit/key  <- \bchave\b
- kit/lightning_rod  <- \bpararaios\b
- kit/finch  <- \btentilhoes?\b|\bpassarinhos?\b|\baves?\b
- kit/pea_green  <- \bervilhas?\b
- kit/globe  <- \bglobo\b|\bplaneta\b
- kit/stick  <- \bvaras?\b
- kit/coin  <- \bmoedas?\b
- kit/sink  <- \bpias?\b

## Biblioteca 3D completa (use em "props": [["pasta/nome", x, z, escala]])
- kit: apple, b2_air, balanca, ball, balloon, balloon_air, ballot_box, bancada, barrel_r, bathtub, beehive, bitcoin, boardgame, booster_air, borracha, brass_nose, bunker_bomb, burr, cake_table, campfire, carro_50, carro_antigo, carro_redondo, chest, chocolate, clipper, cod, coin, crookes_tube, cross, crown, curie_box, cybertruck, dog_sit, ear_jar, egg, enxofre, extinguisher, falcon9_land, falcon_air, feather, finch, finch_long, finch_thick, fire, flag_pole, flamethrower, frasco, globe, golden_stool, gosma, grave, helicopter_air, hospital_ext, iceberg, kettle, key, kite, lightning_rod, lobster, logs, lupa, maca, marco_alpes, marco_atomium, marco_bigben, marco_brandemburgo, marco_canaveral, marco_capitolio, marco_casabranca, marco_chichenitza, marco_coliseu, marco_cristo, marco_eiffel, marco_goldengate, marco_hollywood, marco_liberdade, marco_mesquita, marco_olinda, marco_operasydney, marco_piramides, marco_pisa, marco_saobasilio, marco_viena, melon, microscopio, microwave, miners, monkey_pong, moon, mountain_bunker, panela, pea_green, pea_yellow, petri, phone, pisa_tower, popcorn, porch, postit, prison, rg_africa_1, rg_africa_2, rg_classico_1, rg_classico_2, rg_colonial_1, rg_colonial_2, rg_colonial_3, rg_eua_1, rg_eua_2, rg_eua_3, rg_europa_1, rg_europa_2, rg_europa_3, rg_franca_1, rg_franca_2, rg_franca_3, rg_holanda_1, rg_holanda_2, rg_holanda_3, rg_japao_1, rg_japao_2, rg_japao_3, rg_oriente_1, rg_oriente_2, rg_oriente_3, rg_russia_1, rg_russia_2, ring, roadster, roadster26, roadster26_air, roadster_air, rocket, room_africa_shop, room_africa_stone, room_africa_wood, room_azul_shop, room_azul_stone, room_azul_wood, room_classico_shop, room_classico_stone, room_classico_wood, room_colonial_shop, room_colonial_stone, room_colonial_wood, room_eua_shop, room_eua_stone, room_eua_wood, room_europa_shop, room_europa_stone, room_europa_wood, room_franca_shop, room_franca_stone, room_franca_wood, room_holanda_shop, room_holanda_stone, room_holanda_wood, room_hospital, room_japao_shop, room_japao_stone, room_japao_wood, room_oriente_shop, room_oriente_stone, room_oriente_wood, room_rosa_shop, room_rosa_stone, room_rosa_wood, room_russia_shop, room_russia_stone, room_russia_wood, room_shop, room_stone, room_verde_shop, room_verde_stone, room_verde_wood, room_wood, scroll, searchlight, sink, snake_ring, stall, starlink_dish, starlink_sat, starlink_train, steel_ball, stick, stove, syringe, tent, tequila_bolt, throne, tires, tower, tower_catch, tower_mini, tubos, tulip_bed, tulip_purple, tulip_red, tulip_striped, tulip_yellow, tv, volcano, wash_basin, well, whisky, white_house, xray_plate
- buildings: apartment, barn, bridge, castle_tower, church, house_blue, house_small, house_two, lighthouse, shop, skyscraper, windmill
- vehicles: airplane, bicycle, car, car_blue, helicopter, jeep, locomotive, motorboat, motorcycle, sailboat, tank, taxi, truck, wagon
- nature: bench, bush, flowerbed, fountain, haybale, lamppost, picket_fence, rocks, scarecrow, tree_birch, tree_oak, tree_palm, tree_pine
- tools: anvil, axe, broom, bucket, hammer, ladder, lantern, pitchfork, rake, saw, scythe, shovel, telescope, wheelbarrow
- war: bow, bugle, bunker, cannonballs, drum, flagpole, helmet_army, helmet_knight, musket, pistol, quiver, sandbags, shield, sword
- soltos: barrel, crate, cannon, ship

## Sons ("sfx": ["nome@quadro"])
gun, cannon, squeal, snuffle, gibber, laughs, whoosh, ding, sting, thump, tick, creak, paper

## NAO existe (nao escreva cena que dependa disto)
nadar, cavalgar, escalar, sentar, deitar (mostre o resultado ou reescreva a frase); personagem dentro de veiculo aparecendo; mais de 4 personagens principais na mesma cena fechada.
