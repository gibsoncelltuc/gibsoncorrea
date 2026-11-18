# Catálogo — "Povos Esquecidos", "Cidades no Tempo" e "Como Era a Vida" — PARA DEPOIS

**Estratégia do Gibson (2026):** short de 60 s (gancho forte, mostra como o povo vivia, termina com pergunta) para puxar público → os que performarem viram episódio de ~5 min no canal com mais detalhe.
**Antes de produzir cada um:** conferir os números marcados com (*) em 2 fontes, passar o roteiro para `videos/<id>/beats.json` (campo `"fontes"` com as referências abaixo), modelar no Blender só o que está em **FALTA**, `./prechecar.sh <id>` e olhar a folha.
**Limites da ferramenta que já foram considerados nos roteiros:** não existe lhama, camelo, canoa polinésia, nadar, cavalgar ou sentar → nenhum roteiro depende disso. Todos os personagens são anônimos/originais (um mensageiro, uma oleira, um menino), exceto figuras históricas reais (Mansa Musa, Mau Piailug).
Voz ≈ 2,65 palavras/s → 150–165 palavras = 57–62 s.

---

## Série 8 — "Povos Esquecidos" (título: "Povos Esquecidos EP NN: <título>")
Estrutura de todos: pergunta-gancho no 1º segundo → mapa → 3 "coisas que ninguém sabe" mostradas em cena → "Acontece que" (virada) → fecho com pergunta para comentário. Objeto-herói em close no começo, no meio e no fim. 2 grandes momentos em plano aberto.

| EP | Povo | Título | Cenário | Objeto-herói | Nota viral |
|----|------|--------|---------|--------------|-----------|
| 1 | Incas | O Império sem Roda, sem Dinheiro e sem Escrita | mountain | quipu (cordas com nós) — FALTA | 10 |
| 2 | Astecas | A Cidade que Flutuava num Lago | harbor + palace | grão de cacau / xícara (mug pronta) | 10 |
| 3 | Espartanos | Onde Menino Saía de Casa aos 7 Anos | countryside + palace | moeda-barra de ferro — FALTA | 9 |
| 4 | Nabateus | A Cidade Escavada na Rocha do Deserto | outback | jarro d'água — FALTA (simples) | 9 |
| 5 | Khmer | A Cidade Gigante Engolida pela Floresta | jungle | elefante (pronto) + reservatório | 9 |
| 6 | Mali | O Homem Mais Rico da História | outback | barra de ouro / moeda (pronta) | 10 |
| 7 | Minoicos | Banheiro com Descarga Há 3.500 Anos | palace + harbor | banheira de barro — FALTA | 9 |
| 8 | Vale do Indo | A Cidade com Esgoto e sem Rei | street/outback | tijolo padronizado — FALTA | 8 |
| 9 | Polinésios | Atravessaram o Oceano sem Bússola | harbor | canoa dupla — FALTA | 9 |
| 10 | Marajoaras (Brasil) | O Povo da Amazônia que Fazia Morros | jungle + harbor | urna marajoara — FALTA | 10 (público BR) |

### EP 1 — Incas: "O Império sem Roda, sem Dinheiro e sem Escrita"
**Roteiro (≈160 palavras):**
> Um império com 12 milhões de pessoas*, e nenhuma roda, nenhuma moeda e nenhuma escrita como a nossa. Esses eram os Incas, nos Andes, há 500 anos. Como mandar uma ordem por um país de montanhas? Correndo. Os chasquis eram mensageiros que corriam até a próxima casinha e passavam o recado adiante. Revezando, a mensagem andava uns 240 quilômetros por dia*, por estradas de pedra que somavam mais de 30 mil quilômetros. E sem escrita, como guardar as contas? Com cordões. O quipu era um feixe de cordas cheio de nós: cada nó, um número. Impostos, rebanhos e colheitas, tudo amarrado ali. Acontece que ninguém pagava imposto em dinheiro. Pagava em trabalho: cada família dava dias de serviço construindo pontes, terraços e estradas. E no frio das montanhas eles inventaram a batata desidratada: congelava à noite, secava ao sol e durava anos. Sem roda, sem moeda, sem escrita. E mesmo assim, um dos maiores impérios do mundo. Você sabia disso?

**Como mostrar:** mapa (Andes, Cusco) · chasqui correndo (track, mountain) e entregando o recado ("interacao": "entregar") · GRANDE MOMENTO 1: reveal da estrada nas montanhas com placa "30.000 km" · close do quipu · GRANDE MOMENTO 2: crowd construindo terraço/ponte · batata (FALTA modelar batata/chuño ou usar saco "bag") · fecho com close do quipu.
**Fontes:** UNESCO, Qhapaq Ñan – Andean Road System (whc.unesco.org/en/list/1459) · Britannica, "Inca" e "quipu" · Terence D'Altroy, *The Incas* (Wiley-Blackwell, 2014) · Gary Urton, *Signs of the Inka Khipu* (Univ. of Texas Press, 2003) · John Hyslop, *The Inka Road System* (1984).
**Conferir:** população (estimativas de 6 a 14 milhões, usar "milhões" se houver dúvida); velocidade dos chasquis (fontes falam em 200–240 km/dia).

### EP 2 — Astecas: "A Cidade que Flutuava num Lago"
**Roteiro (≈155 palavras):**
> Quando os espanhóis chegaram em 1519, encontraram uma cidade maior que quase todas as da Europa, construída no meio de um lago. Era Tenochtitlán, a capital dos Astecas, com uns 200 mil moradores*. Para plantar na água, eles criaram as chinampas: ilhas feitas de lama e plantas, presas por árvores, onde cresciam milho, feijão e flores. A água de beber vinha das montanhas por um aqueduto de pedra. No mercado de Tlatelolco, os espanhóis contaram mais de 60 mil pessoas num só dia*. E sabe qual era o troco? Grãos de cacau. Acontece que o chocolate dos Astecas não era doce: era uma bebida amarga, com pimenta, e só os ricos e guerreiros bebiam. E tem mais: todo menino, rico ou pobre, tinha que ir à escola. Hoje, em cima daquele lago, está a Cidade do México. E ainda dá para andar de barco nas últimas chinampas. Você trocaria seu dinheiro por cacau?

**Como mostrar:** mapa (México) · GRANDE MOMENTO 1: reveal da cidade no lago (harbor, com placa "200 mil") · camponês plantando na chinampa (shovel) · GRANDE MOMENTO 2: crowd no mercado · close do grão de cacau/moeda na mão (coin) e da xícara (mug) com cara de nojo ("lick"/"shock") · escola (interior pedra, menino com livro).
**Fontes:** Hernán Cortés, *Segunda Carta de Relación* (1520) · Bernal Díaz del Castillo, *História Verdadeira da Conquista da Nova Espanha* · Britannica, "Tenochtitlán" e "chinampa" · UNESCO, Xochimilco (whc.unesco.org/en/list/412) · Sophie e Michael Coe, *The True History of Chocolate* (1996).
**Conferir:** população (estimativas de 150 a 250 mil).

### EP 3 — Espartanos: "Onde Menino Saía de Casa aos 7 Anos"
**Roteiro (≈155 palavras):**
> Imagine sair de casa aos 7 anos para nunca mais morar com seus pais. Em Esparta, na Grécia antiga, era assim. Os meninos iam para a agogê, um treinamento duro: pouca comida, uma só capa no ano inteiro e, se roubassem comida sem ser pegos, eram elogiados. Se fossem pegos, apanhavam. Eles só voltavam a ser livres por volta dos 30 anos. E as meninas? Corriam, lutavam e podiam ter terras, coisa rara no mundo antigo. Acontece que Esparta tinha um jeito estranho de evitar ganância: o dinheiro era feito de barras de ferro pesadas. Para guardar uma pequena fortuna, você precisava de um quarto inteiro e de uma carroça para carregar. E eles falavam pouco. Quando um rei inimigo ameaçou: "se eu entrar em Esparta, vou destruir tudo", os espartanos responderam com uma palavra só: "Se". Por isso, até hoje, falar curto se chama ser lacônico. Você aguentaria uma semana em Esparta?

**Como mostrar:** mapa (Grécia) · menino se despedindo da mãe ("cry") · GRANDE MOMENTO 1: crowd de meninos treinando (sem armas de fogo; "acao": "comemorar"/correr) · menina correndo (track) · close da barra de ferro na carroça · GRANDE MOMENTO 2: reveal do mensageiro inimigo diante dos espartanos, placa "SE." · fecho com close da barra.
**Fontes:** Plutarco, *Vida de Licurgo* (moeda de ferro, agogê) · Xenofonte, *Constituição dos Lacedemônios* · Plutarco, *Ditos dos Lacônios* / *Moralia* (resposta "Se" a Filipe II) · Britannica, "Sparta" e "agoge" · Paul Cartledge, *The Spartans* (2003).

### EP 4 — Nabateus: "A Cidade Escavada na Rocha do Deserto"
**Roteiro (≈150 palavras):**
> No meio de um deserto onde quase não chove, um povo construiu uma cidade inteira escavando a pedra. Eram os Nabateus, e a cidade era Petra, na atual Jordânia, há uns 2 mil anos. Como viver ali sem rio? Eles caçavam cada gota. Canais escavados na rocha levavam a água da chuva para cisternas escondidas, e um sistema de canos de barro abastecia a cidade e até jardins. Com água garantida, Petra virou parada obrigatória das caravanas que levavam incenso e especiarias da Arábia para o Mediterrâneo. E os comerciantes ficaram ricos, cobrando pedágio e vendendo água para quem passava. Acontece que, séculos depois, Petra foi esquecida pelo mundo. Só os beduínos da região sabiam onde ela estava. Em 1812, um explorador suíço se disfarçou de viajante árabe e entrou escondido. Ele saiu de lá contando que tinha visto palácios dentro das montanhas. Hoje, Petra é uma das Sete Maravilhas do Mundo Moderno. Você conhecia?

**Como mostrar:** mapa (Jordânia) · deserto com "clima": "calor" · close do jarro d'água · GRANDE MOMENTO 1: reveal da fachada escavada (FALTA: fachada tipo "Tesouro" em arenito rosado) · caravana com burros (não existe camelo — escrever "caravanas", sem camelo) · explorador disfarçado (turbante) e "suspicious" do beduíno · GRANDE MOMENTO 2: crowd de turistas hoje.
**Fontes:** UNESCO, Petra (whc.unesco.org/en/list/326) · Britannica, "Petra" e "Nabataean" · Johann Ludwig Burckhardt, *Travels in Syria and the Holy Land* (1822) · Charles R. Ortloff, "The Water Supply and Distribution System of the Nabataean City of Petra", *Cambridge Archaeological Journal* (2005).

### EP 5 — Khmer: "A Cidade Gigante Engolida pela Floresta"
**Roteiro (≈150 palavras):**
> Há 900 anos, no meio da floresta do Camboja, existia uma das maiores cidades do mundo. Era Angkor, capital do Império Khmer. Ali construíram Angkor Wat, o maior templo religioso já erguido, com pedras levadas por elefantes e canais. Mas o segredo de Angkor era a água. Eles cavaram reservatórios gigantes: um deles tem 8 quilômetros de comprimento*. Na época das chuvas, guardavam a água; na seca, regavam os arrozais. Assim alimentavam centenas de milhares de pessoas. Acontece que esse sistema também foi a ruína: secas e enchentes muito fortes quebraram os canais, e a cidade foi se esvaziando. A floresta cobriu tudo. E em 2012, cientistas voaram de helicóptero com um laser que enxerga por baixo das árvores e descobriram ruas, casas e cidades inteiras escondidas. Angkor era muito maior do que se pensava, quase do tamanho de uma metrópole de hoje. O que mais será que a floresta está escondendo?

**Como mostrar:** mapa (Camboja) · elefante carregando (animal pronto, track) · GRANDE MOMENTO 1: reveal do templo (FALTA: templo de torres em degraus estilo Angkor, cartoon) · reservatório (harbor/água) com placa "8 km" · tempestade/seca ("clima") · GRANDE MOMENTO 2: helicóptero (helicopter_air pronto) varrendo a floresta com laser (efeito) · fecho com close do elefante.
**Fontes:** UNESCO, Angkor (whc.unesco.org/en/list/668) · Damian Evans et al., "Uncovering archaeological landscapes at Angkor using lidar", *PNAS* (2013) · Evans et al., "A comprehensive archaeological map of the world's largest preindustrial settlement complex at Angkor", *PNAS* (2007) · Brendan Buckley et al., "Climate as a contributing factor in the demise of Angkor", *PNAS* (2010).
**Conferir:** Baray Ocidental ≈ 8 km × 2,1 km.

### EP 6 — Império do Mali: "O Homem Mais Rico da História"
**Roteiro (≈155 palavras):**
> Muitos dizem que o homem mais rico da história não foi um bilionário de hoje. Foi um rei africano: Mansa Musa, do Império do Mali, há 700 anos. O Mali tinha minas de ouro, e o ouro era trocado por um tesouro do deserto: o sal, que valia quase o mesmo peso em ouro em algumas épocas. Em 1324, Mansa Musa viajou até Meca com uma caravana de milhares de pessoas. No Cairo, ele gastou e deu tanto ouro de presente que, segundo um cronista da época, o ouro perdeu valor no Egito e ainda não tinha se recuperado doze anos depois. Acontece que o maior tesouro que ele trouxe de volta não foi ouro: foram sábios, livros e arquitetos. Timbuktu virou cidade de universidades, e uma mesquita inteira de barro, feita naquela época, está de pé até hoje. Milhares de manuscritos de lá ainda existem. Você conhecia Mansa Musa?

**Como mostrar:** mapa (Mali → Cairo → Meca) · GRANDE MOMENTO 1: reveal da caravana (burros e cavalos, placa "1324") · close da barra/moeda de ouro (coin) · troca sal × ouro ("interacao": "entregar") · mercadores do Cairo com "shock" · GRANDE MOMENTO 2: crowd em Timbuktu, livros na mão (book) · mesquita de barro (FALTA: mesquita de barro com estacas de madeira, estilo Djinguereber).
**Fontes:** Ibn Fadl Allah al-Umari, *Masalik al-Absar* (c. 1337), relato da visita ao Cairo (trad. em Levtzion & Hopkins, *Corpus of Early Arabic Sources for West African History*, 1981) · UNESCO, Timbuktu (whc.unesco.org/en/list/119) · Britannica, "Mansa Musa" e "Mali empire" · Digital History (Univ. of Houston), "An account of Mansa Musa's visit to Cairo in 1324".
**Cuidado:** não afirmar que "quebrou a economia" nem números exatos da fortuna (são estimativas modernas); manter "segundo um cronista da época".

### EP 7 — Minoicos: "Banheiro com Descarga Há 3.500 Anos"
**Roteiro (≈150 palavras):**
> Há 3.500 anos, enquanto boa parte da Europa morava em cabanas, um povo numa ilha grega tinha água encanada. Eram os Minoicos, da ilha de Creta. No palácio de Cnossos, com mais de mil salas*, havia canos de barro encaixados, esgoto e até um vaso que era lavado com água corrente. A rainha tinha banheira pintada, e o palácio tinha poços de luz para iluminar os andares de baixo. E nas paredes, pinturas mostram uma coisa maluca: jovens pulando por cima de touros, dando cambalhota no lombo do animal. Talvez daí tenha nascido a lenda do Minotauro, o monstro meio homem, meio touro, preso num labirinto. Acontece que essa civilização sumiu. Uma das maiores erupções vulcânicas da história explodiu na ilha vizinha de Santorini, e depois Creta foi dominada por outros povos. A escrita deles, chamada Linear A, até hoje ninguém conseguiu ler. Será que um dia alguém vai decifrar?

**Como mostrar:** mapa (Creta) · GRANDE MOMENTO 1: reveal do palácio (palace) · close da banheira pintada · jovem pulando por cima do touro ("interacao": "pular", boi pronto) · vulcão (kit/volcano pronto, de longe — sem close) · GRANDE MOMENTO 2: explosão do vulcão em plano aberto · placa com a escrita (paper).
**Fontes:** Britannica, "Minoan civilization", "Knossos", "Linear A" · J. Lesley Fitton, *Minoans* (British Museum Press, 2002) · Arthur Evans, *The Palace of Minos at Knossos* (1921–1935) · Museu Arqueológico de Heraklion (afresco do salto do touro).
**Conferir:** "mais de mil salas" (algumas fontes dizem ~1.300 cômodos); a ligação da erupção com o fim é debatida — por isso "e depois".

### EP 8 — Vale do Indo: "A Cidade com Esgoto e sem Rei"
**Roteiro (≈150 palavras):**
> Há 4.500 anos, onde hoje é o Paquistão, existia uma cidade planejada melhor que muitas cidades de hoje. Era Mohenjo-daro, da civilização do Vale do Indo. As ruas eram retas, em quadras. Quase toda casa tinha banheiro e um cano que ia para um esgoto coberto na rua. Os tijolos tinham sempre a mesma proporção, em cidades a centenas de quilômetros umas das outras, como se existisse uma norma técnica. Tinha até uma grande piscina pública, o Grande Banho, impermeabilizada com piche natural. Acontece que os arqueólogos não acharam palácio gigante, nem tumba de rei cheia de ouro, nem muitas armas. Ninguém sabe direito quem mandava ali. E eles tinham escrita, em pequenos selos com animais, mas até hoje ninguém conseguiu decifrar. Por volta de 1900 antes de Cristo, as cidades foram sendo abandonadas, provavelmente por mudanças no clima e nos rios. Uma cidade sem rei: você acha que daria certo hoje?

**Como mostrar:** mapa (Paquistão/Índia) · GRANDE MOMENTO 1: reveal da cidade em quadras (street, cores de tijolo) · close do tijolo · morador mostrando o cano ("conversar") · Grande Banho (água) com crowd · selo com animal (boi/elefante prontos como imagem do selo) · GRANDE MOMENTO 2: rio secando ("calor"), gente indo embora (track).
**Fontes:** UNESCO, Mohenjo-daro (whc.unesco.org/en/list/138) · Britannica, "Indus civilization" · Jonathan Mark Kenoyer, *Ancient Cities of the Indus Valley Civilization* (1998) · Harappa.com (projeto arqueológico de Harappa) · Giosan et al., "Fluvial landscapes of the Harappan civilization", *PNAS* (2012).

### EP 9 — Polinésios: "Atravessaram o Oceano sem Bússola"
**Roteiro (≈155 palavras):**
> O maior oceano do mundo foi explorado por gente sem bússola, sem mapa e sem metal. Os Polinésios saíram em canoas duplas e colonizaram ilhas espalhadas por um triângulo maior que o Brasil: Havaí, Nova Zelândia e Ilha de Páscoa. Como sabiam o caminho? Liam a natureza. As estrelas nascendo no horizonte apontavam a direção. O balanço das ondas mostrava onde havia ilha. E certos pássaros, de manhã, voavam para o mar; à tarde, voltavam para a terra. Era só seguir. Acontece que, por muito tempo, os europeus disseram que tudo aquilo tinha sido sorte, barcos perdidos levados pelo vento. Então, em 1976, um navegador chamado Mau Piailug guiou uma canoa do Havaí até o Taiti, mais de 4 mil quilômetros, sem nenhum instrumento. E chegou, guiado só pelas estrelas, pelas ondas e pelos pássaros. E até a batata-doce, que é da América do Sul, chegou às ilhas antes de Colombo. Você confiaria nas estrelas?

**Como mostrar:** mapa (Pacífico, triângulo) · GRANDE MOMENTO 1: reveal da canoa dupla no mar (FALTA: canoa dupla com vela em garra de caranguejo) · noite estrelada ("hora": "noite") · gaivota (pronta) voando · europeus duvidando ("smug"/"suspicious") · GRANDE MOMENTO 2: chegada no Taiti com crowd comemorando ("acao": "comemorar") · close da canoa.
**Fontes:** Polynesian Voyaging Society / Hōkūleʻa, "The Story of Hōkūleʻa" (hokulea.com) · Ben Finney, *Voyage of Rediscovery* (1994) · David Lewis, *We, the Navigators* (1972) · Roullier et al., "Historical collections reveal patterns of diffusion of sweet potato in Oceania", *PNAS* (2013) · Britannica, "Polynesian culture".

### EP 10 — Marajoaras: "O Povo da Amazônia que Fazia Morros"
**Roteiro (≈155 palavras):**
> Muito antes de Cabral chegar, na ilha de Marajó, no Pará, vivia um povo que construía morros com as próprias mãos. Os Marajoaras viveram ali por quase mil anos, mais ou menos entre os anos 400 e 1400. Todo ano a ilha alagava. Então eles empilhavam terra e fizeram os tesos: aterros altos, alguns do tamanho de um campo de futebol, onde ficavam as casas, secas no meio da cheia. E eles eram mestres no barro. Faziam potes, pratos e urnas pintadas com desenhos tão detalhados que hoje estão em museus do mundo inteiro. As mulheres usavam até uma tanga feita de cerâmica. Acontece que as urnas mais bonitas eram funerárias: guardavam os ossos dos antepassados, com rostos desenhados. Por muito tempo, achou-se que a Amazônia nunca teve povos assim, organizados. Os Marajoaras provam o contrário: eram milhares de pessoas, com chefes, artistas e festas. Você sabia que essa história é brasileira?

**Como mostrar:** mapa (Marajó, PA) · GRANDE MOMENTO 1: cheia ("clima": "chuva", água) e reveal do teso com casas em cima · oleira pintando o pote (close na mão) · close da urna marajoara (FALTA: urna com rosto estilizado, padrão geométrico vermelho/preto sobre creme) · tanga de cerâmica (FALTA, pequeno) · GRANDE MOMENTO 2: crowd de visitantes no museu ("interior": "pedra").
**Fontes:** Denise Pahl Schaan, *Cultura Marajoara* (Senac, 2009) e "Marajó: Arqueologia, Iconografia, História e Patrimônio" · Museu Paraense Emílio Goeldi (acervo marajoara) · Anna C. Roosevelt, *Moundbuilders of the Amazon* (Academic Press, 1991) · Museu Nacional/UFRJ (coleção marajoara).
**Conferir:** tamanho dos maiores tesos e o período (datas variam por fonte: ~400–1300/1400 d.C.).

**Modelos 3D a fazer no Blender quando a série começar (estilo arredondado, nunca Minecraft):** quipu, barra de ferro espartana, jarro nabateu, fachada de Petra, templo Angkor, mesquita de barro de Timbuktu, banheira minoica, tijolo do Indo, canoa dupla polinésia, urna e tanga marajoara, batata (chuño). Os demais (elefante, boi, gaivota, burro, cavalo, vulcão, helicóptero, moeda, xícara, livro, pá) já estão prontos.

---

## Série 9 — "Cidades no Tempo" (título: "Um Dia em <cidade>, <ano>")
Formato: um morador comum (personagem original) atravessa o dia → 3 detalhes chocantes de como se vivia → "Acontece que" → ligação com hoje. Ideias (roteiro completo só quando for produzir):

| # | Cidade e ano | Gancho | Detalhe surpreendente | Fonte inicial | Nota |
|---|--------------|--------|------------------------|---------------|------|
| 1 | Roma, 80 d.C. | "Prédio de 6 andares, sem elevador e sem banheiro." | Banheiros públicos coletivos, esponja no palito; inauguração do Coliseu com 100 dias de jogos | Suetônio; Mary Beard, *SPQR* | 10 |
| 2 | Pompeia, 79 d.C. | "As pichações nas paredes falam de política e de amor." | Grafites eleitorais e lanchonetes de rua (thermopolium) | Parque Arqueológico de Pompeia | 9 |
| 3 | Londres, 1858 | "O verão em que a cidade fedeu tanto que o Parlamento fugiu." | O "Grande Fedor" gerou o sistema de esgoto que existe até hoje | Museu de Londres; Bazalgette | 9 |
| 4 | Tóquio (Edo), 1720 | "A maior cidade do mundo reciclava quase tudo." | Até o cocô era vendido como adubo | Susan Hanley, *Everyday Things in Premodern Japan* | 9 |
| 5 | Rio de Janeiro, 1808 | "Uma rainha e 10 mil portugueses chegaram de surpresa." | Casas tomadas com "P.R." na porta ("Ponha-se na Rua") | Laurentino Gomes, *1808* | 10 (BR) |
| 6 | Rio de Janeiro, 1904 | "A cidade se revoltou contra uma vacina." | Revolta da Vacina e o Rio "bota-abaixo" | Fiocruz; Sidney Chalhoub, *Cidade Febril* | 10 (BR) |
| 7 | Ouro Preto, 1750 | "A cidade mais rica das Américas ficava em Minas." | Ouro escondido em santos de pau oco | Laura de Mello e Souza, *Desclassificados do Ouro* | 9 (BR) |
| 8 | Nova York, 1920 | "Beber era proibido, e a cidade tinha 30 mil bares secretos." | Lei Seca e speakeasies | Daniel Okrent, *Last Call* | 9 |
| 9 | Paris, 1900 | "Uma calçada que andava sozinha." | Esteira rolante da Exposição Universal | BnF/Gallica (Exposição de 1900) | 8 |
| 10 | Bagdá, 900 d.C. | "A cidade dos livros no mundo." | Casa da Sabedoria e a fábrica de papel | Jim Al-Khalili, *A Casa da Sabedoria* | 8 |
| 11 | Constantinopla, 1453 | "A muralha que resistiu mil anos caiu num dia." | O canhão gigante e a porta esquecida aberta | Roger Crowley, *1453* | 9 |
| 12 | Veneza, 1500 | "Uma fábrica que montava um navio por dia." | O Arsenal de Veneza, linha de montagem antes de Ford | Frederic Lane, *Venice: A Maritime Republic* | 8 |

## Série 10 — "Como Era a Vida" (título: "Como Era a Vida nos Anos <70/80/90> em <lugar>")
Formato: família comum (personagens originais) → objetos da época em close (TV, telefone, dinheiro) → preços e costumes → "Acontece que" → comparação com hoje → pergunta "você viveu isso?" (engajamento alto nos comentários). Precisa de objetos de época no Blender (orelhão, TV de tubo, ficha telefônica, fita K7, disquete).

| # | Época e lugar | Gancho | Detalhe surpreendente | Fonte inicial | Nota |
|---|---------------|--------|------------------------|---------------|------|
| 1 | Brasil, anos 70 | "Ligar para outra cidade era uma aventura." | Orelhão (1972), ficha, TV em cores chegando (1972), tri na Copa de 70 | Telebrás/Museu das Telecomunicações; Memória Globo | 10 (BR) |
| 2 | Brasil, anos 80 | "O preço mudava de manhã para a tarde." | Inflação, fiscais do Sarney, Plano Cruzado (1986), remarcadora de preço | Banco Central (histórico das moedas) | 10 (BR) |
| 3 | Brasil, anos 90 | "A moeda mudou e ninguém acreditava." | Plano Real (1994), internet discada e o barulho do modem | Banco Central; Museu de Valores | 10 (BR) |
| 4 | Brasil, anos 2000 | "Todo mundo tinha um perfil no Orkut." | Lan house, ringtone, MSN | Google (fim do Orkut, 2014) | 9 (BR) |
| 5 | EUA, anos 50 | "Médico fazendo propaganda de cigarro na TV." | Anúncios de cigarro, cinema drive-in | Stanford Research Into the Impact of Tobacco Advertising | 9 |
| 6 | URSS, anos 80 | "Esperar 10 anos na fila para comprar um carro." | Filas para tudo e o carro Lada | Britannica; arquivos de época | 9 |
| 7 | Japão, anos 80 | "O terreno do palácio imperial valia mais que a Califórnia inteira." | A bolha econômica | The Economist / estudos sobre a bolha | 8 |
| 8 | Berlim, 1961–1989 | "Uma família dividida por um muro da noite para o dia." | Fugas por túneis e balões | Fundação Muro de Berlim | 9 |
| 9 | Londres, anos 60 | "A cidade onde a minissaia nasceu." | Beatles, Carnaby Street | V&A Museum | 7 |
| 10 | Mundo, 1999 | "O medo de que os computadores parassem na virada do ano." | Bug do milênio | relatórios do governo dos EUA (Y2K) | 9 |

## Ordem sugerida
Povos Esquecidos primeiro (Marajoaras → Incas → Mali → Astecas → Esparta), alternando com um "Como Era a Vida" brasileiro (anos 80 e anos 90 têm o maior potencial de comentário). Os que mais performarem viram episódio longo (~5 min): mesmo cenário e personagens, mais detalhe (cotidiano, comida, casa, religião, fim do povo).
