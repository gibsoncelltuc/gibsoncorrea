# Música original do Ep. 1 gerada com ACE-Step 1.5 (aberto, MIT, roda em CPU)

- Programa: https://github.com/ServeurpersoCom/acestep.cpp (compilado em CPU, sem BLAS)
- Modelos: Serveurperso/ACE-Step-1.5-GGUF (LM 1.7B Q8_0, DiT turbo Q8_0, VAE, Qwen3-Embedding Q8_0)
- Pedido: `ep01_pedido_acestep.json` (letra em português, 96 BPM, dó maior, 60 s, voz masculina)
- Tempo na máquina de 4 núcleos: ~9 min (LM ~100 s + síntese ~7 min)
- Comandos: `ace-lm --models models --request ep01.json` e depois `ace-synth --models models --request ep010.json`
- Para outra versão: mudar `"seed"` no JSON.
