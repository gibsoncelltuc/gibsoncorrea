# Vipcell Box — programa de bancada (Windows)

Aplicativo de computador (janela) que **identifica o aparelho ao plugar**: o modo em que
ele está e o que é (marca / modelo / CPU / arquitetura), no estilo do painel de detecção
da Chimera. **Somente leitura** — não grava, não remove conta/FRP, não tem como brickar.

É um programa separado da ferramenta da loja. Este aqui é desktop, nativo, com acesso ao USB.

## Abrir rápido (sem gerar .exe)

1. Instale o **Python 3.9+** (marque *Add Python to PATH*).
2. No Prompt de Comando, dentro desta pasta:
   ```
   pip install pyusb
   python vipcell_box.py
   ```

## Gerar o executável (VipcellBox.exe)

Na pasta, dê dois cliques em **`build_exe.bat`** (ou rode no Prompt). Ele instala o
necessário e cria **`dist\VipcellBox.exe`** — um programa único, que você instala/copia
pra qualquer PC e abre com dois cliques.

## Para a leitura completa

- **platform-tools** da Google (adb.exe / fastboot.exe) no PATH → marca/modelo/CPU ricos.
- **Driver da marca** instalado (Samsung USB, Qualcomm 9008, MediaTek VCOM, Unisoc).
- Se o modo baixo (EDL/BROM/SPD) não aparecer, use o **Zadig** para trocar o driver
  daquela porta para **WinUSB** (o acesso USB do Python precisa disso).

## Arquivos

| Arquivo | O que é |
|---|---|
| `vipcell_box.py` | o programa (janela) |
| `detector.py` | a mesma detecção, versão de terminal |
| `core.py` | núcleo de detecção (compartilhado) |
| `mtk_recovery.py` | recuperação MediaTek (dead boot) pilotando o mtkclient |
| `RECUPERAR-G56.md` | passo a passo do Moto G56 (Dimensity 7060) |
| `build_exe.bat` | gera o `VipcellBox.exe` |
| `requirements.txt` | dependências (pyusb) |

## Recuperação MediaTek (dead boot)

Quando a Box detecta um MediaTek em BROM/Preloader, o card mostra 3 botões: **ler info**
(seguro), **backup** (seguro) e **restaurar boot** (grava do firmware que você baixou). O
motor é o **mtkclient** — instale com `pip install mtkclient`. Para usar a recuperação,
rode pela versão Python (`python vipcell_box.py`), porque o `.exe` empacotado não hospeda o
mtkclient. Passo a passo do G56 em `RECUPERAR-G56.md`. **Nada de firmware vem embutido.**

## O que reconhece

ADB · Fastboot/Bootloader · Qualcomm EDL 9008 · MediaTek BROM/Preloader ·
Samsung Download/Odin · Unisoc SPD — por VID/PID, com marca/modelo/CPU onde o modo permite.

## Honesto

Isto é o **detector** (seguro, só lê). Gravar firmware é outro passo, com risco real, e não
entra neste programa. A tabela de IDs a gente amplia conforme os aparelhos que você atende.
