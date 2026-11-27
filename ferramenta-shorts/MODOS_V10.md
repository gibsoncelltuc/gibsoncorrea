# Modos da ferramenta (v13, 24/11)

Existe **um modo só**: o motor local (Three.js + Canvas 2D), 100% local, sem API externa e sem IA generativa.

O antigo "Modo 2" (clipes do Blender costurados no vídeo) foi aposentado: era um esqueleto que nenhuma etapa da fábrica chamava. O que ele prometia agora é feito dentro do motor:

- **Ação-chave de objeto** (carro decola, voa, pula, pousa, arranca): animação com VFX 3D preso no objeto (`web/vfx.js`) e câmera seguindo.
- **Explicação de ciência** sem personagem: campo `"explica"` no beat (`GUIA_DO_ROTEIRISTA.md`, "Cena de explicação").

O Blender continua sendo usado para **modelar** objetos (`blender/formas.py`, `blender/objetos_*.py`). Os arquivos antigos estão em `legado/`.
