# Lab Terminal — motor de trading em modo SIMULADO

Engenharia reversa de um painel de "bot de memecoins" visto em vídeo, reconstruído como um motor
de **paper trading** (sem dinheiro real, sem carteira, sem chave privada) com painel em HTML.

> **Os dados são sintéticos.** O painel exibe sempre a faixa "SIMULAÇÃO". Não use capturas dele como
> se fossem resultados reais.

## Como rodar (Node 22 ou mais novo, sem dependências)

```
cd grok-lab
npm test                                  # 7 testes do motor
npm run sim -- --ticks 1440 --seed 1      # 24 h simuladas, resumo no terminal
npm run mc  -- --runs 300 --ticks 1440    # Monte Carlo: 300 mercados diferentes
npm start -- --seed 7 --tick 400          # painel em http://127.0.0.1:8787
```

## O que foi lido do vídeo e o que é suposição

| Item | Origem |
|---|---|
| Capital inicial US$ 64 (capital − PnL = 64,00 em todos os quadros) | vídeo |
| 7 agentes: Scanner, Rug Check, Sizer, Executor, Stop Guard, Take Profit, Logger | vídeo |
| Sizer = 18% do capital | vídeo |
| Stop de −8% (medido em 2 posições legíveis) | vídeo |
| Várias posições abertas ("2 armed", "3 armed") | vídeo |
| Gráfico de velas de 1 min em valor de mercado, marcador "Buy", caixas TP (verde) e SL (vermelha) | vídeo |
| Alvo de 3R (+24%), trailing após +12% com recuo de 6% | **inferido** (a caixa verde do vídeo não deu para medir) |
| Regra de entrada: rompimento da máxima das últimas 10 velas + volume ≥ 2,5× a média | **inferido** (o vídeo não mostra a regra) |
| Filtros do Rug Check (mint, freeze, LP, dev, top 10, clone, liquidez) | prompt do print + vídeo ("clone of", "REJECT") |
| Taxa 0,5% e derrapagem 1,5% por lado | **custo real que o vídeo não mostra** |

## Resultado honesto (mercado sintético, 300 execuções de 24 h, US$ 64 iniciais)

- Mediana final: **US$ 62** (−3%). Intervalo p5–p95: US$ 50 a US$ 76. Melhor caso: US$ 100.
- 41% terminaram acima do capital inicial. **0%** chegaram a +100%. Acerto médio: 45%.

Isso não prova nada sobre o mercado real: é um modelo de passeio aleatório com rugs, onde as entradas
não têm vantagem. Mostra apenas que as mesmas regras de risco (stop −8%, 18% por trade), com custos
reais de taxa e derrapagem, **não geram sozinhas** o +1.963% em 4 h do vídeo. Para algo assim aparecer,
os números precisam vir de outro lugar (demo, edição ou dados inventados).

## Limitações

- Mercado simulado: não há dados ao vivo. O próximo passo seria um adaptador de **paper trading com
  dados reais** (DexScreener / GeckoTerminal / RugCheck), que precisa ser testado na sua máquina.
- Rugs reais costumam impedir a saída; aqui a saída sempre executa (gap na abertura), o que é otimista.
- Ordem intra-vela conservadora (mínima antes da máxima), sem latência de rede.
- Não há execução real: nenhuma função assina transações nem usa chave privada.
