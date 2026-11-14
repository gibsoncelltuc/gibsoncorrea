$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Dest = Join-Path $Root 'external/claude-animated-shorts'
$Repo = 'https://github.com/mromidev/claude-animated-shorts.git'
if (Test-Path $Dest) {
    throw "Destino já existe: $Dest. Revise o conteúdo manualmente; o script não sobrescreve clones existentes."
}
New-Item -ItemType Directory -Force -Path (Join-Path $Root 'external') | Out-Null
git clone --depth 1 $Repo $Dest
$Commit = (git -C $Dest rev-parse HEAD).Trim()
Set-Content -Path (Join-Path $Root 'external/benchmark-resolved-commit.txt') -Value $Commit -Encoding utf8
Write-Host "Clone concluído. Commit: $Commit"
Write-Warning 'Não execute scripts do benchmark antes de auditar README, SKILL, LICENSE, dependências e scripts.'
