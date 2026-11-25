// Parâmetros do motor. Os marcados [VÍDEO] foram lidos no vídeo; [INFERIDO] são suposições.
export const CONFIG = {
  startEquity: 64, // [VÍDEO] capital inicial: capital - PnL = 64,00 em todos os quadros
  sizePctEquity: 0.18, // [VÍDEO] Sizer: "18% eq"
  stopLossPct: 0.08, // [VÍDEO] SL -8% (medido: 83,2K->76,5K e 47,8K->44,0K)
  tpR: 3, // [INFERIDO] alvo = 3R (+24%); a caixa verde do vídeo não deu para medir
  trailArmPct: 0.12, // [INFERIDO] do prompt do print: "trail after +12%"
  trailPct: 0.06, // [INFERIDO] distância do trailing
  maxPositions: 3, // [VÍDEO] "2 armed", "3 armed" no Stop Guard
  feePct: 0.005, // [CUSTO REAL] taxa por lado (DEX + prioridade) - o vídeo não mostra custos
  slippagePct: 0.015, // [CUSTO REAL] derrapagem por lado - o vídeo não mostra custos
  minTradeUsd: 5,
  cooldownMin: 15,
  scan: {
    minAgeMin: 30, // [PROMPT] pares de 30m a 72h
    maxAgeMin: 72 * 60,
    minMc: 40_000,
    maxMc: 20_000_000, // [PROMPT] mcap até US$ 20M
    minLiq: 15_000,
    min5mVol: 2_000,
    breakoutLookback: 10, // [INFERIDO] rompimento da máxima das últimas 10 velas
    volSpike: 2.5, // [INFERIDO] volume >= 2,5x a média de 20 velas
  },
  rug: {
    maxDevPct: 5, // [PROMPT] dev > 3% (aqui 5%, como no repositório de referência)
    minLpLockedPct: 85,
    maxTop10Pct: 25, // [PROMPT] top 10 > 25%
  },
};
