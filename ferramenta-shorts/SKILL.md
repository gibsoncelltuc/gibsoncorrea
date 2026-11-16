---
name: shorts-batalha-curiosidade
description: Produz shorts verticais 1080x1920 (60 s) de batalhas e curiosidades históricas em estilo cartoon 2D-em-3D (personagens "bean head" em cenários 3D pintados), com narração PT-BR, legenda, música e efeitos gerados por código. Auto-verifica e auto-corrige antes e depois do render. Use quando o usuário pedir novos vídeos desse canal, refazer takes, ou criar roteiros.
---
# Shorts Batalha & Curiosidade — instruções ponta a ponta
**Leia primeiro RELATORIO_E_PLANO.md (contexto, estado dos 3 vídeos, pendências e como resolver).**

## 1. Como produzir (3 caminhos)
- **Vídeo novo (automático):** `./setup.sh` (1x) → criar `videos/<id>/beats.json` (copie um de `videos/`) → `./make_video.sh <id>`. Todos de uma vez: `./run_all.sh` (retomável).
- **Refazer só takes com falha:** apague os quadros `out/<id>/frames/fNNNN.jpg` dos takes ruins (use `qa_frames.py --rerender` ou apague por faixa) e rode `./render_missing.sh <id> <N>` e `./assemble.sh <id> <Titulo>`. Nunca re-renderize o vídeo inteiro.
- **Versões PT dos 3 vídeos entregues:** `stories/emu_pt`, `ghost_pt`, `bucket_pt` (specs, cues, voz, fit já prontos) — `./pipeline_pt.sh` (edite a lista `L`).
Tempo: ~1 h por vídeo de 60 s em 4 núcleos de CPU, sem GPU.

## 2. Fluxo interno (make_video.sh)
roteiro → voz (edge-tts) → tempos por palavra → `mkvideo.py` (beats → spec.js + cues.py) → `autostyle.py` → `fit.sh` → `gate_all.sh` → `snap.sh` → render em 3 fatias (`render_missing.sh`) → `qa_frames.py` (+1 reparo) → `assemble.sh` → `review_video.sh`.

## 3. Auto-verificação e autocorreção (já implementadas)
- `autostyle.py`: mede cor/contraste/detalhe/contorno contra o canal de referência e ajusta exposição, desfoque e luz sozinho (até 6 rodadas). **Ajuste a cena, nunca afrouxe o teste.**
- `fit.sh`: afasta a câmera (×1,12) se herói cortado/escondido, câmera dentro de objeto, personagem >125% do quadro, ninguém visível; aproxima (×0,89) se minúsculo.
- `gate_all.sh`: câmera + takes + estilo; reprova ANTES do render.
- Regras no `qa_takes.mjs`: câmera abaixo do chão, câmera dentro de sólido (casa, caminhão), herói fora/pequeno.
- `qa_frames.py`: preto, branco, congelado, faixa escura no horizonte, glitch; re-renderiza só esses quadros.
- `review_video.sh`: duração, loudness (alvo ~-15 LUFS), congelados, pretos, folha de contato (1 quadro/1,5 s). **Sempre olhar a folha de contato e 3-4 quadros em tamanho real. Ao dividir imagem para olhar, cortar em múltiplos da altura da linha.**
- Storyboard antes do render: `node storyboard.mjs <id> sb.jpg 360 && python3 sbsheet.py sb.json sb.jpg`.

## 4. Correções já feitas nesta ferramenta (histórico)
Faixa escura no horizonte (contorno agora usa plano local); câmera piso suave (não fica abaixo do chão); foco no personagem mais próximo; desfoque em 1/3 dos takes; detecção de câmera dentro de casa; regras de composição globais; rastreamento de câmera com velocidade constante (`ease:'lin'`, `move:[..,'lin']`, `nocut`); ator sobre veículo (`y` função); nuvem de poeira; cavalo `s` 0,7; estilo por história (neve azul-violeta, paralelepípedo quente, exposição 0,72 + cinf 4 em Zanzibar); render balanceado; pipeline retomável.

## 5. REGRAS OBRIGATÓRIAS (a ferramenta deve seguir sempre)
1. **Animais:** todo animal usa modelo bom (3D Blender/Quaternius CC0), nunca o modelo cru. Se o animal não existe, MODELAR/importar antes de produzir. Escala cavalo 0,7; urso 1,0; emu 1,6 só enquanto o modelo atual for usado.
2. **Ações, não só expressão:** a cada cena, pelo menos um personagem faz algo com o corpo (andar, correr, pegar/segurar/mostrar o objeto do tema, entregar, apontar). Quando a narração cita um objeto, mostrar o personagem pegando/usando-o.
3. **Interação com o espectador (quarta parede):** olhar para a câmera em momentos-chave (já há no acting.js); gestos para o espectador.
4. Roteiro: números por extenso para a voz, dígitos no texto da tela; "dizem que" onde fontes divergem; conferir fatos.
5. Falar com o usuário SEMPRE em português; entregar vídeo só depois de revisar.

## 6. O QUE AINDA FALTA (honesto)
- **Ações de corpo com objetos** (regra 2): NÃO implementadas no motor (hoje: pose parada, marcha, gestos de braço). Maior pendência visual.
- **Animais melhores:** emu "batata", cavalo cru; pacotes Quaternius CC0 de animais animados (quaternius.itch.io/lowpoly-animated-animals, opengameart.org) são candidatos: testar se trazem animações andar/correr. Blender (`pip install bpy`, scripts em `docs`/histórico) para modelar.
- Gerador `mkvideo.py`: testado de ponta a ponta só até o gate no Karánsebes; nenhum vídeo gerado foi renderizado até o fim — pode haver ajustes no primeiro.
- Os 10 roteiros novos (`videos/`) não foram renderizados; só Karánsebes tem prévia.
- Guerra do Porco: ainda não produzida (usar `mkvideo.py`).
- Emus: refazer takes (emus em batata, abertura lenta, multidão pequena); Balão: final do pincel sem ação, noite escura; Balde: mostrar boneco pegando o balde, cavalos crus.
- Voz: `edge-tts` é não oficial; para monetização usar Azure Speech/ElevenLabs/Google TTS (licença comercial) e regravar.
- Não testado fora do ambiente de origem; scripts são bash (Windows: WSL/Git Bash). Container na nuvem reiniciava e derrubava a fila: rodar localmente.
- Cenário gerado por código é simples; sem GPU. Não existe alternativa mais rápida que o render atual sem GPU.
- Os outros 7 vídeos da série PT (onoda..wojtek) estavam em produção; Onoda com render completo e em montagem.

## 7. Arquivos
`web/` motor (three.js + cartões 2D, sets, biblioteca de ~170 objetos CC0, animais glb) · `mkvideo.py` gerador · `autostyle.py` · `make_video.sh`/`run_all.sh` · `stories/_h.js` ajudantes (S, pp, mv, txt, W) · `docs/` análises do canal de referência e addendum técnico · `videos/` 10 roteiros novos · `stories/*_pt` os 3 vídeos entregues.
