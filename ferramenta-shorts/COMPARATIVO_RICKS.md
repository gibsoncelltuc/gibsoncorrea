# Comparativo: canal de referência × nossa ferramenta (17/11/2026)
Base: 14 vídeos fichados entre os 20 shorts animados mais vistos do canal (quadros reais 1080x1920 + transcrições) e 3 auditorias concluídas (personagens, enquadramento/câmera, cenários). "Nosso antes" = Karansebes de 16/11. Dados brutos: `ref_privado/` (fichas em `cards/`, auditorias em `audit/`).
Situação: ✅ aplicado e visto em vídeo · 🟡 aplicado em parte · ❌ não feito · ❔ não medido no canal.

## 1. Roteiro e ritmo
| Ponto | Canal | Nosso antes | Situação |
|---|---|---|---|
| Duração | mediana 65 s | 62–70 s | ✅ já batia |
| Ritmo da narração | 213 palavras/min, quase sem pausa | ~146 palavras/min | 🟡 Karansebes e Emus reescritos (155 e 154 palavras, frases curtas); voz segue em +10% |
| Gancho | termina em 3,8 s; paradoxo contado como fato | abre por data ("Em 1788...") | ✅ Karansebes e Emus reescritos sem data; `roteiro_check.py` aprova |
| Falas de personagem | 1–2 por vídeo | 0 | ✅ falas entre aspas nos dois roteiros; boca mexe |
| Estrutura | gancho → cenário → escalada → virada ("You see,") → explicação → final irônico curto | narração cronológica | ✅ nos dois roteiros (virada "Acontece que", final curto) |

## 2. Enquadramento e câmera
| Ponto | Canal | Nosso antes | Situação |
|---|---|---|---|
| Planos abertos | 18% dos quadros | 64% | ✅ diretor limita a 2 abertos comuns + 2 de impacto |
| Largura da cabeça principal | mediana 26% da largura | 11% | ✅ planos fechados em `mkvideo.py` (não medi de novo o número) |
| Personagens por quadro | mediana 1,5; até 3 em 87% | mediana 10 | ✅ figurantes reduzidos; tropa só nos planos de impacto |
| Abertura do vídeo | 18 de 20 abrem em plano médio/fechado | sempre plano aberto recuando | ✅ diretor abre sempre em plano médio |
| Final do vídeo | 16 de 20 terminam em plano médio/fechado | sempre plano aberto | ✅ diretor fecha sempre em plano médio |
| Altura da câmera nos abertos | 0,8× a altura do personagem | 1,6–2,8× (vista de cima) | ✅ câmera na altura do personagem (h 2,3–2,5) |
| Enquadramentos por vídeo | 25–31 (um a cada ~2 s) | 17 (um a cada 3,7 s) | 🟡 sub-cortes a cada 54 quadros (~1,8 s) |
| Cortes secos | 0–1 por vídeo | 8 | ✅ dissolve curto entre cenas |
| Golpe de câmera | 0,23% da altura, só em impacto físico | 1,2–4%, 13 por vídeo | ✅ só em impacto, ×0,35 |
| Texto na imagem | em placas/objetos da cena (37% dos quadros); título flutuante quase nunca | título flutuante no céu em 32% | ❌ título ainda flutuante (placas não feitas) |
| Personagem cortado na borda | raro | acontece | ✅ regra nova no controle de qualidade afasta a câmera sozinha |
| Legenda | 38 px por letra, centro em 70,3% | 40 px, 70,0% | ✅ já batia |

## 3. Personagens
| Ponto | Canal | Nosso antes | Situação |
|---|---|---|---|
| Proporção, espessura de perna/braço, rosto | — | igual ao canal | ✅ já batia |
| Clones | cada personagem diferente | mesmo chapéu, casaco e porte | 🟡 óculos, barba, 7 variantes; tropa fica uniforme de propósito |
| Chapéus / cabelos / barbas | ≥25 chapéus, ≥8 cabelos, barbas com hachura, óculos em 6 vídeos | 6 chapéus, 1 cabelo, 1 bigode | 🟡 +óculos e barba; chapéus e cabelos novos ❌ |
| Cor de perna/braço | tinta escura (contraste 115–150 contra o chão) | com calça clara, contraste 7–10 | ✅ pernas e braços em tinta escura |
| Sombra do rosto | lavanda | pêssego/laranja sob luz quente | ✅ sombra lavanda; rosto não alaranja mais |
| Figurino | estampas, botões, cintos, detalhes | raso | ❌ |
| Mãos | seguram objetos | vazias | ❌ |
| Contorno da cabeça | lado fino/grosso, razão ~3 | razão 1,85 | ❌ |

## 4. Cenários e objetos
| Ponto | Canal | Nosso antes | Situação |
|---|---|---|---|
| Locações por vídeo | 3 a 8 | 1 | 🟡 `set` e `interior` por cena; Emus usa 2 locações |
| Quadros em interior | 44% | 0% | ✅ kit de interior no Blender (madeira, pedra, loja) — campo `interior` no beat |
| Parede/fachada perto dos personagens | 85% dos quadros (a 2–8 m) | 0% (construção a 36–86 m) | ✅ interior com parede a ~5 m; ao ar livre o diretor põe fachada atrás em plano médio |
| Superfícies | campo chapado + linhas pintadas (ruído < 2%) | ruído em 16–38% dos pixels | ✅ aplicado em 17/11 (conferência visual) |
| Cor do gramado | claro e saturado | escuro | ✅ |
| Chão com juntas/tábuas desenhadas | 73% dos quadros | 0% | 🟡 interiores com tábuas/lajotas; rua com pedras; grama/terra lisas (como no canal) |
| Móveis (94 prontos) | interiores mobiliados | nunca usados | ✅ estante, mesa, cadeira e baú entram sozinhos no interior |
| Objetos genéricos (caixote, barril, pedrinhas) | objetos da própria história | iguais em todo cenário | 🟡 pedrinhas reduzidas; caixote/barril continuam |
| Veículos | cabine aberta, motorista dentro, lataria lisa | bloco fechado | ✅ carro, táxi, jipe refeitos no Blender |
| Animais | — | emu "batata" | 🟡 emu refeito; os demais não revisados |

## 5. Luz, cor e acabamento (medido por mim nos 48 quadros)
| Ponto | Canal (mediana) | Nosso antes | Situação |
|---|---|---|---|
| Saturação | 0,44 | 0,39–0,47 | ✅ já batia |
| Luminância | 0,445 | 0,43–0,59 | ✅ dentro da faixa |
| Pixels muito escuros | 4,4% | 1,1–2,9% | 🟡 contraste aplicado; não medi de novo |
| Nitidez | 0,062 | 0,050–0,054 | 🟡 desfoque reduzido; não medi de novo |
| Luz muda com a história | noite azul, interior quente, dia claro | uma luz por vídeo | 🟡 troca por palavra-chave ("noite", "amanhecer") |

## 6. Animação e áudio
| Ponto | Canal | Nosso | Situação |
|---|---|---|---|
| Tremor entre quadros | não tem | tinha | ✅ corrigido |
| Boca ao falar | sim | não | ✅ |
| Pegar/carregar objetos, caminhada natural | sim | não | ❌ |
| Momentos de impacto | sim | não tinha | ✅ plano aberto com tropa, clarões e som de tiro |
| Áudio (voz, música, efeitos) | ❔ sem acesso ao som | — | ❔ só subi o volume 1 dB com base em relatório de terceiros |

## 7. Velocidade
| | Antes | Agora |
|---|---|---|
| Vídeo completo de ~1900 quadros | ~57 min | ~19 min ✅ |

## O que mais pesa e ainda falta (em ordem)
1. Roteiros no molde do canal (gancho, ritmo, falas, final).
2. Cenários: várias locações por vídeo, interiores mobiliados, parede perto dos personagens, chão com juntas.
3. Câmera: abrir e fechar em plano médio, câmera na altura do personagem, mais enquadramentos, menos corte seco e golpes menores, texto em placas.
4. Personagens: perna/braço escuros, sombra lavanda, mais chapéus/cabelos/figurino, objetos na mão.
5. Auditorias que não rodaram com agentes (luz, legenda, animação, áudio): luz e legenda eu medi sozinho; animação e áudio continuam sem medida.
