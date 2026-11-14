# Benchmark externo: Claude Animated Shorts — auditoria e integração

## Identificação

- Repositório: https://github.com/mromidev/claude-animated-shorts
- Nome usado pelo projeto: `cartoon-3d-short` / Claude Animated Shorts.
- Stack declarada: Three.js, Remotion, `@remotion/three`, Node, Python 3 e FFmpeg.
- Licença declarada: MIT para código e documentação; os frames de referência são material de estudo e não devem ser redistribuídos/publicados.
- O README declara um exemplo de 67 segundos (“The Bridge That Fell for a Song”), 20 Shorts estudados, sete relatórios técnicos, 20 contact sheets com 60 frames cada (1.200 frames) e 38 frames de referência em tamanho integral.
- Fonte primária: README e SKILL.md do repositório. Conferir novamente antes de cada atualização.

## Veredito

**ADOTAR COMO BENCHMARK E FONTE OPCIONAL DE TÉCNICAS; NÃO ADOTAR COMO SISTEMA PRINCIPAL SEM AUDITORIA.**

Pontos fortes declarados e visíveis na documentação:
- pipeline completo de um Short vertical de 55–70 s;
- cenas 3D em Three.js dentro do Remotion;
- personagens 2D/cut-out num mundo 3D;
- relatórios sobre movimento, profundidade, textura, personagens, luz, contornos e color grade;
- sincronização de reações visuais com timestamps de palavras;
- geração/mixagem de música e SFX;
- ferramentas para stills, folhas comparativas e QA frame a frame.

Limites que impedem declarar equivalência total:
- a demonstração pública destacada é um exemplo de 67 s; isso não valida por si só long-form de 3–10 min;
- as instruções da skill original incluem preferências específicas do autor (inglês, sem legendas, voz estável), incompatíveis com um sistema universal em português;
- o README alerta para diretório temporário grande (~1,3 GB copiado por bundle), portanto armazenamento e cache devem ser planejados;
- o workflow exige ambiente local com Node, Python, FFmpeg e render WebGL/Chromium;
- um conjunto de 20 referências não demonstra que todos os vídeos do canal-alvo foram analisados ou que os resultados são equivalentes;
- não há garantia de desempenho algorítmico ou de views.

## Integração recomendada

1. Manter o projeto principal do usuário independente.
2. Clonar o benchmark em `external/claude-animated-shorts/` somente quando o usuário/ambiente autorizar acesso à rede.
3. Registrar o commit efetivamente obtido em `external/benchmark-lock.json`; nunca inventar hash ou assumir que `main` é imutável.
4. Ler primeiro `README.md`, `SKILL.md`, `LICENSE`, `package.json`/lockfiles, scripts e lista de assets.
5. Fazer auditoria de segurança: downloads, shell commands, subprocessos, telemetria, paths absolutos, escrita fora do projeto, credenciais e dependências.
6. Executar o exemplo isolado em diretório de teste, sem misturar assets do usuário.
7. Comparar saída visual e técnica: duração, fps, resolução, determinismo, render time, memória, flicker, contorno, DOF, movimento, consistência, áudio e legibilidade.
8. Portar apenas padrões/ideias aprovados. Não copiar frames de referência, personagens, roteiros, vozes ou assets do canal analisado.
9. Guardar uma tabela `benchmark-diff.md`: recurso, implementação upstream, implementação própria, decisão (adotar/adaptar/rejeitar), justificativa e teste.
10. Repetir a auditoria quando atualizar o commit.

## Comandos de obtenção manual

```bash
mkdir -p external
# Revisar o endereço antes de clonar; usar diretório isolado.
git clone --depth 1 https://github.com/mromidev/claude-animated-shorts.git external/claude-animated-shorts
cd external/claude-animated-shorts
git rev-parse HEAD
```

O hash retornado deve ser salvo no lockfile junto com data de obtenção e versão de Node/Python. Não executar scripts de instalação ou render antes da revisão.

## Referências de leitura

- README: https://github.com/mromidev/claude-animated-shorts
- Skill: https://github.com/mromidev/claude-animated-shorts/blob/main/SKILL.md
- Relatório de movimento: https://github.com/mromidev/claude-animated-shorts/blob/main/references/reports/motion.md

## Relação com Ricks Clips

O benchmark é uma referência de engenharia para a família visual “personagens 2D em mundo 3D”. A auditoria do canal Ricks Clips permanece um conjunto de evidências separado. Não assumir que o benchmark mediu o canal Ricks Clips; não fundir os dois conjuntos sem conferir origem e metodologia de cada frame.
