# Instalação da skill

## Claude.ai

1. Mantenha o arquivo ZIP com a pasta `ricks-3d-toon-story-orchestrator/` como raiz interna.
2. No Claude, abra **Settings → Capabilities/Features → Skills** (o rótulo pode variar conforme a interface).
3. Ative o uso de Skills, escolha **Upload skill** e envie o ZIP.
4. Habilite a skill após o upload.
5. Teste com: `Use a skill 3D Toon Story Orchestrator e produza um Short de 65 segundos sobre [tema].`

A disponibilidade de Skills personalizadas depende do plano, do recurso de execução de código e das políticas atuais da conta. Consulte a ajuda oficial do Claude caso o menu tenha mudado.

## Claude Code

Copie a pasta inteira para um destes caminhos:

- Pessoal: `~/.claude/skills/ricks-3d-toon-story-orchestrator/`
- Projeto: `.claude/skills/ricks-3d-toon-story-orchestrator/`

Depois, em uma conversa no projeto, peça: `Use ricks-3d-toon-story-orchestrator para criar e renderizar um Short sobre [tema].`

## Conteúdo do pacote

- `SKILL.md`: orquestrador principal.
- `references/`: pesquisa do canal, bíblia visual, motor narrativo, animação, câmera, áudio, arquitetura e QA.
- `templates/project/`: presets JSON de produção, planos e timestamps de exemplo.
- `templates/remotion-starter/`: ponto de partida de código para uma cena 2D/3D sincronizada por frame.
- `scripts/`: validação de timeline, geração de SRT e mixagem de áudio FFmpeg.

A skill é a camada de instruções e orquestração. A renderização precisa ocorrer num ambiente com Node, Chromium/WebGL, Remotion e FFmpeg instalados e acesso aos arquivos do projeto.
