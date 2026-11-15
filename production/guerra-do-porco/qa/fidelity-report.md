# Relatório de fidelidade visual — piloto × referência do canal

Método: frames extraídos com FFmpeg das 2 gravações de referência (8,2 s cada, 60 fps; interface do app recortada) e do vídeo final; mesmas métricas objetivas aplicadas a ambos (faixa de legenda excluída). `scripts/fidelity_metrics.py` da skill documenta o método.

| métrica | referência (canal) | piloto v2 (Three.js, reprovado) | **piloto v3 (Blender)** | razão v3/ref |
|---|---:|---:|---:|---:|
| laplacian_var | 15.3823 | 9.0995 | **17.8776** | 1.16 |
| edge_density | 0.1883 | 0.0805 | **0.1783** | 0.95 |
| colorfulness | 0.2694 | 0.4092 | **0.2332** | 0.87 |
| sat_mean | 0.4498 | 0.5425 | **0.5069** | 1.13 |
| val_mean | 0.5565 | 0.7428 | **0.5185** | 0.93 |
| contrast_local | 0.0802 | 0.0535 | **0.0760** | 0.95 |
| vignette | 1.4746 | 1.5555 | **1.6679** | 1.13 |

**Leitura:** detalhe fino/bordas/contraste local medem a riqueza de cenário e textura (o piloto v2 estava 40–60 % abaixo); saturação/brilho medem a mood da cor. Métricas objetivas **não substituem** a comparação visual lado a lado (`qa/_local/fidelity_comparison.png`, não versionada por conter frames do canal).
