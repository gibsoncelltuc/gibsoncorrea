# Detector de aparelho — Vipcell Bancada

Painel de identificação no estilo da detecção da Chimera: pluga o celular, ele diz
**em que modo está** e **o que é** (marca / modelo / CPU / arquitetura). **Somente leitura** —
não grava nada, não remove conta/FRP, não tem como brickar.

## Rodar no Windows

1. Instale o **Python 3.9+** (marque "Add Python to PATH" no instalador).
2. Abra o Prompt de Comando e instale a biblioteca USB:
   ```
   pip install pyusb
   ```
3. Para marca/modelo/CPU completos, baixe o **platform-tools** da Google
   (adb/fastboot) e deixe a pasta no PATH.
4. Instale o **driver da marca** do aparelho (Samsung USB, Qualcomm 9008,
   MediaTek VCOM, etc.). Se o modo baixo (EDL/BROM/SPD) não aparecer, use o
   **Zadig** para trocar o driver daquela porta para **WinUSB** (o pyusb precisa disso).
5. Rode:
   ```
   python detector.py
   ```
   ou, para ficar vigiando e detectar assim que plugar:
   ```
   python detector.py --watch
   ```

## O que ele reconhece

| Modo | Como aparece | Plataforma |
|---|---|---|
| ADB (ligado) | `adb devices` | marca/modelo/CPU completos |
| Fastboot / Bootloader | `fastboot getvar` | product, variant, cpu-abi, unlocked |
| Qualcomm EDL | USB `05C6:9008` | Qualcomm (QFIL / edl) |
| MediaTek BROM/Preloader | USB `0E8D:xxxx` | MediaTek (mtkclient / SP Flash) |
| Samsung Download/Odin | USB `04E8:685D` | Samsung (Odin / Heimdall) |
| Unisoc SPD | USB `1782:4D00` | Unisoc (SPD Upgrade) |

## Limites honestos

- **Identifica com segurança** o modo e os IDs. Em ADB/fastboot, puxa marca/modelo/CPU
  ricos. Em EDL/BROM/SPD, identifica a plataforma e o chip; o **modelo exato** nesses
  modos costuma depender do firmware, igual nas ferramentas pagas.
- Isto é um **detector**, não um gravador. Flash de firmware é outro passo, com risco real,
  e não entra aqui.
