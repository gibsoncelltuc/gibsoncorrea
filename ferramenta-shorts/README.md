# Ferramenta de shorts "batalha e curiosidade" — pacote automático

**Uso (3 comandos):**
```
./setup.sh          # 1x: instala dependências
./run_all.sh        # produz TODOS os vídeos de videos/*/beats.json (retomável: se cair, rode de novo)
# ou um só:  ./make_video.sh karansebes
```
Saída: `out/<id>/<Titulo>.mp4` (1080x1920, 30 fps, voz PT-BR, legenda, áudio ~-15 LUFS) + `out/<id>/review_sheet.jpg` (folha de contato). Cada vídeo leva ~1h de CPU (4 núcleos).

**Os 10 roteiros prontos** (em `videos/*/beats.json`, temas diferentes dos 10 da outra série): karansebes, texel1795, toledo1835, losangeles1942, hayha1939, kiska1943, bacalhau1958, petrich1925, paris1870, gansos390.

**Para criar outro vídeo:** copie um `beats.json` e troque as frases (`say`), cenário (`set`), figurinos (`outfits`) e, por cena: `shot` (wide|two|close|group|prop|crowd|track|low), `who` ("FIG:variante:expressão"), `props`, `animals`, `text`, `light`, `mood`, `fx`, `sfx`.

**Auto-verificação e autocorreção (já embutidas em make_video.sh):**
1. `autostyle.py` — mede cor/contraste/detalhe contra o canal de referência e corrige sozinho (exposição, desfoque, luz) até passar.
2. `fit.sh` — ajusta a câmera: afasta se corta/esconde/entra em objeto/personagem gigante; aproxima se minúsculo.
3. `gate_all.sh` — reprova antes do render (câmera, takes, estilo). Se reprovar, para e mostra o motivo em `logs/gate_<id>.txt`.
4. `qa_frames.py` — após o render procura quadros pretos/brancos/faixa escura/glitch e **re-renderiza só esses**.
5. `review_video.sh` — duração, loudness, congelados, pretos e folha de contato.

**Limites honestos:** cenário gerado por código (não modelado à mão); animais 3D simples; se o `autostyle` não convergir, o log avisa e é preciso ajustar `light`/`exp` no beats.json. Voz exige acesso a speech.platform.bing.com.
