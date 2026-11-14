# Quality gates e scorecard — V2

## Regra de aprovação

Pontuar cada dimensão de 0 a 5 e converter para 100. Aprovação exige nota total >= 85/100 **e** nenhum gate crítico reprovado. Meta de excelência: >= 92/100. Uma nota não substitui revisão humana.

## Pesos

| Dimensão | Peso | Evidência mínima |
|---|---:|---|
| Narrativa e retenção | 15 | roteiro, promessa/payoff, beat map, revisão de clareza |
| Fidelidade factual/editorial | 10 | fact-check com fontes e claims |
| Identidade visual | 15 | style frame, character sheet, environment sheet, paleta |
| Animação e atuação | 15 | teste de movimento, contato, expressões, continuidade |
| Câmera e montagem | 10 | shot list, curva de câmera, ritmo e composição |
| Áudio e sincronização | 10 | stems, word timings, loudness/peak e sync report |
| Render e estabilidade | 10 | build, frame samples, reprodução e render manifest |
| Legibilidade/acessibilidade | 5 | legendas, contraste, safe zones, idioma |
| Reutilização/manutenibilidade | 5 | registries, IDs, assets versionados, docs |
| Originalidade e direitos | 5 | licença/atribuição, assets originais, sem cópia de cenas |

## Gates críticos — falha reprova independentemente da nota

- [ ] O projeto compila e a composição abre.
- [ ] Um segmento real foi renderizado; não basta gerar JSON ou código.
- [ ] Duração, FPS, resolução e aspect ratio conferem com o manifesto.
- [ ] Não há frame ausente, preto, congelado ou piscando sem intenção.
- [ ] Narração, boca/gesto, legenda e eventos sonoros estão sincronizados.
- [ ] Nenhuma afirmação factual central sem fonte.
- [ ] Nenhum asset/voz/trilha sem licença ou autorização documentada.
- [ ] Nenhuma clonagem de voz de pessoa real sem autorização explícita.
- [ ] Nenhuma dependência externa executada sem auditoria básica.
- [ ] O relatório distingue testes executados de verificações não executadas.

## Verificações automatizáveis

- JSON Schema para `production.json`, `shots.json`, `word-timings.json` e registries.
- Frames de amostra em 0%, 10%, 25%, 50%, 75%, 90% e 100% de cada cena.
- Verificar frames duplicados consecutivos por hash/perceptual hash; sinalizar, não reprovar automaticamente quando hold for intencional.
- Verificar duração e streams com `ffprobe`.
- Detectar clipping/peak e medir loudness com FFmpeg `ebur128`/`loudnorm` em modo análise.
- Verificar SRT: timecodes crescentes, sem sobreposição indevida, sem linhas vazias ou fora da duração.
- Verificar assets referenciados e arquivos ausentes.
- Renderizar um mesmo frame em execuções separadas e comparar hash/pixel diff com tolerância documentada.

## Revisão humana obrigatória

1. Assistir ao vídeo inteiro em velocidade normal, com som.
2. Assistir ao vídeo sem som para verificar se a ação visual se sustenta.
3. Ouvir apenas a faixa de voz para clareza, ritmo e pronúncia.
4. Ver em tela pequena para legibilidade.
5. Rever cortes, reações e payoff em velocidade reduzida.
6. Comparar com a bíblia visual do próprio projeto e com referências permitidas; nunca comparar copiando o conteúdo de terceiros.

## Estrutura de scorecard.json

```json
{
  "rubric_version": "2.0",
  "score_total": 0,
  "pass_threshold": 85,
  "critical_gates_passed": false,
  "dimensions": {
    "narrative": {"score_0_to_5": 0, "evidence": [], "issues": []},
    "facts": {"score_0_to_5": 0, "evidence": [], "issues": []},
    "visual_identity": {"score_0_to_5": 0, "evidence": [], "issues": []},
    "animation": {"score_0_to_5": 0, "evidence": [], "issues": []},
    "camera_editing": {"score_0_to_5": 0, "evidence": [], "issues": []},
    "audio_sync": {"score_0_to_5": 0, "evidence": [], "issues": []},
    "render_stability": {"score_0_to_5": 0, "evidence": [], "issues": []},
    "accessibility": {"score_0_to_5": 0, "evidence": [], "issues": []},
    "reusability": {"score_0_to_5": 0, "evidence": [], "issues": []},
    "originality_rights": {"score_0_to_5": 0, "evidence": [], "issues": []}
  },
  "not_tested": [],
  "reviewed_by": "",
  "review_date": ""
}
```
