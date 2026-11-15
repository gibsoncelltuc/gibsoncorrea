# Relatório de fidelidade visual — piloto × referência do canal

Método: frames extraídos com FFmpeg das 2 gravações de referência (8,2 s cada, 60 fps; interface do app recortada) e do vídeo final; mesmas métricas objetivas aplicadas a ambos (faixa de legenda excluída). `scripts/fidelity_metrics.py` da skill documenta o método.

| métrica | referência (canal) | piloto v2 (Three.js, reprovado) | **piloto v3 (Blender)** | razão v3/ref |
|---|---:|---:|---:|---:|
| laplacian_var | 15.3823 | 9.0995 | **15.7332** | 1.02 |
| edge_density | 0.1883 | 0.0805 | **0.1658** | 0.88 |
| colorfulness | 0.2694 | 0.4092 | **0.2347** | 0.87 |
| sat_mean | 0.4498 | 0.5425 | **0.4429** | 0.98 |
| val_mean | 0.5565 | 0.7428 | **0.5333** | 0.96 |
| contrast_local | 0.0802 | 0.0535 | **0.0712** | 0.89 |
| vignette | 1.4746 | 1.5555 | **1.6661** | 1.13 |

**Leitura:** detalhe fino/bordas/contraste local medem a riqueza de cenário e textura (o piloto v2 estava 40–60 % abaixo); saturação/brilho medem a mood da cor. Métricas objetivas **não substituem** a comparação visual lado a lado (`qa/_local/fidelity_comparison.png`, não versionada por conter frames do canal).
