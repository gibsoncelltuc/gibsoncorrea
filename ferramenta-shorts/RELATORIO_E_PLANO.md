# Relatório geral + plano de correção (leia primeiro)

## Contexto (resumo de todas as sessões)
O usuário (fala português; quer TUDO em português) criou um canal de shorts verticais de "guerras estranhas e curiosidades", estilo do canal de referência Ricks Clips (cores vivas, textura pintada, câmera em movimento, personagens expressivos). A ferramenta aqui renderiza em CPU (sem GPU), ~1 h por vídeo de 60 s. Feito: 10 histórias de guerra em inglês (v3), depois versões em português (voz PT-BR). Entregues em PT: Emus, Exército de Balões, Balde. Em produção/pendentes na série PT: Onoda, Uísque, Zanzibar, Pastéis, Jenkins, Futebol, Wojtek (specs prontos em stories/*_pt na máquina de origem; não estão neste zip, só os 3 entregues). Pedidos adicionais: Guerra do Porco; mais 10 vídeos novos (roteiros em `videos/`, não renderizados); melhorar o Emus; mais animação de corpo; animais bem modelados.
Problema operacional: o ambiente na nuvem reiniciava a cada 20-40 min e derrubava a fila → o usuário vai rodar localmente (notebook ligado 24 h, sem GPU, deve levar ~1 h/vídeo).

## Estado dos 3 vídeos entregues (todos em videos_prontos/, versão leve; técnica OK: 1080x1920, 30 fps, ~-15 LUFS, sem congelados/pretos)
### 1) A Guerra dos Emus (70 s)
Pronto: narração, legenda, câmera acompanhando caminhão/bando, soldados com expressões, pôr do sol final, correções do motor.
Falhas: emus parecem "batata com pescoço" (modelo cru); abertura lenta; boa parte dos personagens parada; takes de multidão pequenos ("back": emus minúsculos); caminhão ok mas cenário simples.
Plano: (a) trocar emu por modelo melhor (importar/modelar, ver regra 1); (b) refazer só os takes: abertura (0-5 s), 'against', 'back', 'score' com ações (soldado apontando, correndo, fazendo gesto ao espectador); (c) `qa_frames --rerender`/apagar faixa + `render_missing.sh` + `assemble.sh`. Fonte: stories/emu_pt/spec.js (shots por id).
### 2) O Exército Feito de Balões (68 s)
Pronto: cenas coloridas, tanques infláveis, noite/pôr do sol, texto sobrepostos, take do rio corrigido (câmera estava dentro de casa).
Falhas: final do pincel sem ação (só sorriso); muitos takes de tanque/boneco parado; noite escura; 'hide' pouco legível.
Plano: ação "pintor pinta o tanque" / "soldado enche o tanque com bomba de ar" (regra 2); clarear `night`; refazer só takes pump, brush, hide.
### 3) A Guerra do Balde (54 s)
Pronto: praça colorida (paralelepípedo aquecido), soldados expressivos, cavalaria rastreada, torre, balde.
Falhas: ninguém pega/mostra o balde quando a narração fala dele; cavalos crus (perna reta, "orelha de gato"); praça repetitiva.
Plano: shot 'stole': soldado pega o balde do poço e corre; 'triumph': soldados carregam o balde até a torre; trocar cavalo por modelo melhor; refazer só esses takes.

## Pendências globais e como resolver (ordem de prioridade)
1. **Ações de corpo e objetos (não existe no motor).** Onde: `web/toonbase.js` (bodyFront: tabela de gestos G, braços 'top'), `web/acting.js` (actFor: gesto por palavra), `web/runtime.js` (actorsAt: move/pose). Fazer: (i) pose 'carry' (braços à frente segurando um prop que segue a mão), 'point', 'run' (ciclo de corrida), 'hand-over'; (ii) em beats.json novo campo `act`: ["pegar:bucket", "andar:+6", "entregar:OUT"]; o prop é anexado à mão do ator (posição = ator + offset por frame). (iii) lexicon em acting.js: palavra-objeto → ação. Verificar com storyboard + 1 take de teste antes de refazer vídeos.
2. **Animais.** Testar pacotes CC0 Quaternius (animais animados) importando glb; verificar animações andar/correr; senão modelar no Blender (`pip install bpy`; no ambiente de origem usado o Blender 5.3) e exportar glb com partes nomeadas (body, head, legs, tail). Atualizar `web/assets/animals/*.glb`, `G3D`/`is3` em runtime.js. Gravar a regra: nenhum animal sem modelo bom.
3. **Quarta parede / interação com o espectador:** já há olhar para a câmera e gestos (acting.js); ampliar: personagem fala para a câmera em frases-chave, aponta, "ei, você!". Adequar ao formato vertical.
4. **Gerador `mkvideo.py`:** rodar `./make_video.sh karansebes` completo e corrigir erros; depois os outros 9; produzir 10 vídeos novos + Guerra do Porco (criar `videos/porco1859/beats.json`: Pig War 1859, San Juan Island, porco de Lyman Cutlar comeu batatas, quase guerra EUA×Reino Unido, 12 anos de ocupação conjunta, árbitro Kaiser Guilherme I em 1872; usar animal 'pig').
5. **Voz com licença comercial:** edge-tts é não oficial. Trocar por Azure Speech/ElevenLabs/Google TTS: alterar só `produce_voice.sh` (gerar voice.mp3 e depois `timing.py`).
6. Nunca afrouxar o gate de estilo: ajustar a cena. Sempre revisar folha de contato antes de entregar.

## Instalação rápida
`./setup.sh` (instala edge-tts, Pillow, numpy, Playwright, fontes) → `./make_video.sh karansebes`. Requisitos: Node 20+, Python 3.10+, ffmpeg. Windows: WSL/Git Bash. O motor roda em Chromium headless com WebGL por software (SwiftShader).

## Contato com o usuário
Sempre em português, curto, sem enrolar; avisar o que foi feito, o que falta e ser honesto com limites.
