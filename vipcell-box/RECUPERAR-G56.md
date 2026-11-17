# Recuperar o Moto G56 (dead boot) — passo a passo

**Aparelho:** Moto G56 5G · **Chip:** MediaTek **Dimensity 7060** (6 nm) · **Modo que ele entra:** MediaTek (BROM/Preloader).

> **Leia antes:** o Dimensity 7060 é um chip **novo (2025)**. O mtkclient (ferramenta
> livre) pode **ainda não ter o payload** que vence a proteção de BootROM (SLA/DAA) desse
> chip. Se no passo 3 o mtkclient **não fizer o "handshake"**, a recuperação livre não é
> possível nesse chip hoje — não é defeito do programa. Nesse caso o caminho é firmware
> oficial pela Motorola (LMSA Rescue) quando o aparelho voltar a ser visto, ou uma box
> comercial que já tenha o loader do 7060.

## O que você precisa no PC (Windows)

1. **Python 3.9+** no PATH.
2. **mtkclient**: `pip install mtkclient` (ou baixar de `github.com/bkerler/mtkclient`).
3. **Driver**: MediaTek USB VCOM + o backend **libusb**. Se a porta MediaTek não for
   vista pelo Python, abra o **Zadig** e troque o driver daquela porta para **WinUSB**.
4. **Firmware oficial do G56** (modelo exato, ex. XT2529): baixe de fonte oficial /
   mirror confiável (lolinet/Motorola). Extraia os arquivos de partição.

## Importante: use o programa pela versão Python para a recuperação

A detecção funciona no `.exe`. Mas para **pilotar o mtkclient**, rode a Vipcell Box pela
versão Python (o `.exe` empacotado não hospeda o mtkclient como módulo):

```
pip install pyusb mtkclient
python vipcell_box.py
```

## Passo a passo

1. **Desligue** o G56. Segure **Volume −** (ou Vol + conforme responder) e **plugue o cabo**
   com ele desligado, para entrar em **BROM/Preloader**. No Gerenciador de Dispositivos
   deve surgir a porta MediaTek. A Vipcell Box mostra o card **MediaTek BROM**.
2. **Botão 1 — Ler info (seguro):** confirma que o mtkclient conversa com o chip e lê a
   tabela de partições. **Se travar em "handshake"/"preloader", é o limite do 7060** (veja o
   aviso lá em cima).
3. **Botão 2 — Backup de segurança:** salva preloader, boot, lk, vbmeta e outras críticas
   numa pasta. **Faça sempre antes de gravar.**
4. **Botão 3 — Restaurar boot (avançado):** aponte a **pasta do firmware** do G56. O
   programa grava, na ordem: `preloader → lk → boot → dtbo → vbmeta`. Nomes esperados:
   `preloader.bin`, `lk.img`, `boot.img`, `vbmeta.img`, etc.
5. Terminado, **desplugue**, segure as teclas de boot e tente ligar.

## Comando manual (se preferir o terminal)

```
mtk printgpt                       # ler (seguro)
mtk r preloader preloader_bkp.bin  # backup de uma particao
mtk w preloader preloader.bin      # gravar (do firmware oficial)
mtk w lk lk.img
mtk w boot boot.img
```

## Honesto, de novo

- O programa **não grava firmware que não exista no seu PC** — nada vem embutido.
- O motor é o **mtkclient**; a Vipcell Box organiza e transmite a saída dele.
- Em chip novo com BootROM protegido, a ferramenta livre **pode não entrar** — e aí nenhum
  clone grátis resolve; é firmware oficial ou box comercial com o loader do chip.
