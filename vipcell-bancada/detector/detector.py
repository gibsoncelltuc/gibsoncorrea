#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vipcell Bancada - Detector de aparelho (somente leitura / read-only)
===================================================================

O que faz: ao plugar um celular no PC, identifica em que MODO ele esta
(ADB, fastboot, Qualcomm EDL 9008, MediaTek BROM/Preloader, Samsung
Download/Odin, Unisoc SPD) lendo o identificador USB (VID/PID), e puxa
marca / modelo / CPU / arquitetura onde o modo permite (adb getprop,
fastboot getvar). Nao grava NADA no aparelho. Nao tem como brickar.

Isto NAO remove conta/FRP e nao faz flash. E so o painel de identificacao,
no estilo da deteccao da Chimera.

Como rodar (Windows, com Python 3.9+):
    pip install pyusb
    python detector.py
    python detector.py --watch      (fica vigiando, detecta ao plugar)

Para a leitura rica (marca/modelo/CPU) em ADB/fastboot, tenha o
platform-tools da Google no PATH (adb.exe / fastboot.exe). Para os modos
baixos (EDL/BROM/SPD) instale o driver da marca; no Windows o pyusb
precisa do backend libusb (Zadig troca o driver para WinUSB quando a
leitura USB nao funcionar).
"""

import sys
import time
import shutil
import argparse
import subprocess

try:
    import usb.core
    import usb.util
    HAVE_USB = True
except Exception:
    HAVE_USB = False

# --------------------------------------------------------------------------
# Tabela de modos conhecidos por VID/PID.
# Fontes: identificadores publicos de bootrom/diag de cada plataforma.
# (vid, pid) -> (nome do modo, familia/plataforma, acao sugerida)
# Use 0xFFFF em pid para casar qualquer produto do mesmo fabricante.
# --------------------------------------------------------------------------
KNOWN = {
    (0x05C6, 0x9008): ("Qualcomm EDL (9008)", "Qualcomm", "QFIL / edl: gravar com firehose do chip"),
    (0x05C6, 0x9006): ("Qualcomm Diag (9006)", "Qualcomm", "Modo diag - normalmente intermediario"),
    (0x05C6, 0x900E): ("Qualcomm Diag (900E)", "Qualcomm", "Modo diag"),
    (0x05C6, 0x676C): ("Qualcomm Download", "Qualcomm", "Modo download Qualcomm"),
    (0x0E8D, 0x0003): ("MediaTek BROM (BootROM)", "MediaTek", "mtkclient / SP Flash Tool (Download)"),
    (0x0E8D, 0x2000): ("MediaTek Preloader", "MediaTek", "SP Flash Tool / mtkclient"),
    (0x0E8D, 0x2001): ("MediaTek Preloader (DA)", "MediaTek", "SP Flash Tool / mtkclient"),
    (0x0E8D, 0x20FF): ("MediaTek BROM (preloader off)", "MediaTek", "mtkclient em bootrom"),
    (0x04E8, 0x685D): ("Samsung Download (Odin)", "Samsung Exynos/Snapdragon", "Odin / Heimdall: gravar .tar.md5"),
    (0x04E8, 0x6860): ("Samsung MTP (sistema ligado)", "Samsung", "Aparelho ligado - use ADB"),
    (0x04E8, 0x685E): ("Samsung Modem/Download", "Samsung", "Odin / Heimdall"),
    (0x1782, 0x4D00): ("Unisoc/SPRD Diag", "Unisoc", "SPD Upgrade / Research Download (pac)"),
    (0x1782, 0x3D00): ("Unisoc/SPRD Download", "Unisoc", "SPD Upgrade Tool"),
    (0x18D1, 0xD00D): ("Fastboot (Google/Android)", "Android", "fastboot: ver abaixo a leitura getvar"),
    (0x2717, 0xFFFF): ("Xiaomi (fastboot/adb)", "Xiaomi", "fastboot getvar / adb getprop"),
    (0x22B8, 0xFFFF): ("Motorola (fastboot/adb)", "Motorola", "fastboot getvar / LMSA Rescue"),
    (0x2A70, 0xFFFF): ("OnePlus/Oppo/Realme", "BBK/Realme", "fastboot / EDL conforme chip"),
    (0x22D9, 0xFFFF): ("Oppo/Realme", "Realme", "fastboot / EDL conforme chip"),
    (0x201E, 0xFFFF): ("Infinix/Transsion", "Infinix", "MediaTek: SP Flash Tool / mtkclient"),
}

VENDOR = {
    0x05C6: "Qualcomm", 0x0E8D: "MediaTek", 0x04E8: "Samsung", 0x1782: "Unisoc/Spreadtrum",
    0x18D1: "Google", 0x2717: "Xiaomi", 0x22B8: "Motorola", 0x2A70: "BBK (OnePlus/Oppo/Realme)",
    0x22D9: "Oppo", 0x201E: "Transsion (Infinix/Tecno)", 0x1004: "LG", 0x12D1: "Huawei",
}

C = {"g": "\033[92m", "c": "\033[96m", "y": "\033[93m", "r": "\033[91m",
     "b": "\033[1m", "d": "\033[2m", "x": "\033[0m"}
def paint(s, k):
    if not sys.stdout.isatty():
        return s
    return C.get(k, "") + s + C["x"]

def run(cmd, timeout=8):
    """Roda um binario externo (adb/fastboot) e devolve a saida, ou None."""
    exe = cmd[0]
    if shutil.which(exe) is None:
        return None
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return (p.stdout or "") + (p.stderr or "")
    except Exception:
        return None

# --------------------------------------------------------------------------
# Leitura rica via platform-tools (quando disponivel)
# --------------------------------------------------------------------------
def read_adb():
    out = run(["adb", "devices"])
    if not out or "\tdevice" not in out and "\tunauthorized" not in out:
        return None
    if "\tunauthorized" in out:
        return {"modo": "ADB (nao autorizado)", "aviso": "Aceite 'Permitir depuracao USB' na tela do aparelho."}
    props = ["ro.product.manufacturer", "ro.product.brand", "ro.product.model",
             "ro.product.device", "ro.board.platform", "ro.product.cpu.abi",
             "ro.hardware", "ro.build.version.release", "ro.build.version.security_patch"]
    info = {"modo": "ADB (sistema ligado)"}
    for p in props:
        r = run(["adb", "shell", "getprop", p])
        if r:
            v = r.strip()
            if v:
                info[p.split(".")[-1]] = v
    return info

def read_fastboot():
    out = run(["fastboot", "devices"])
    if not out or "fastboot" not in out.lower():
        return None
    info = {"modo": "Fastboot / Bootloader"}
    for var in ["product", "variant", "cpu-abi", "secure", "unlocked", "hw-revision",
                "version-bootloader", "serialno", "current-slot"]:
        r = run(["fastboot", "getvar", var])
        if r:
            for line in r.splitlines():
                if line.lower().startswith(var):
                    val = line.split(":", 1)[-1].strip()
                    if val and val != "":
                        info[var] = val
                    break
    return info

# --------------------------------------------------------------------------
# Enumeracao USB dos modos baixos (pyusb)
# --------------------------------------------------------------------------
def scan_usb():
    achados = []
    if not HAVE_USB:
        return achados
    try:
        devs = list(usb.core.find(find_all=True))
    except Exception as e:
        return [{"erro": "Nao consegui ler o USB (backend libusb ausente?): %s" % e}]
    for d in devs:
        vid, pid = d.idVendor, d.idProduct
        modo = plataforma = acao = None
        if (vid, pid) in KNOWN:
            modo, plataforma, acao = KNOWN[(vid, pid)]
        elif (vid, 0xFFFF) in KNOWN:
            modo, plataforma, acao = KNOWN[(vid, 0xFFFF)]
        if modo is None and vid not in VENDOR:
            continue  # ignora mouse/teclado/hub
        fab = VENDOR.get(vid, "Desconhecido")
        nome = prod = None
        try:
            nome = usb.util.get_string(d, d.iManufacturer) if d.iManufacturer else None
            prod = usb.util.get_string(d, d.iProduct) if d.iProduct else None
        except Exception:
            pass
        achados.append({
            "vid": "%04X" % vid, "pid": "%04X" % pid, "fabricante": fab,
            "modo": modo or "USB do fabricante (modo nao mapeado)",
            "plataforma": plataforma or fab, "acao": acao or "Confirme o modo pelas teclas",
            "usb_fab": nome, "usb_prod": prod,
        })
    return achados

# --------------------------------------------------------------------------
# Relatorio
# --------------------------------------------------------------------------
def kv(label, value):
    print("   %-14s %s" % (label + ":", paint(str(value), "b")))

def report():
    print(paint("\n== Vipcell Bancada - Detector (somente leitura) ==", "g"))
    achou = False

    adb = read_adb()
    if adb:
        achou = True
        print(paint("\n[ ADB ]", "c"))
        kv("Modo", adb.get("modo"))
        for k in ["manufacturer", "brand", "model", "device", "platform", "abi", "hardware", "release", "security_patch"]:
            if k in adb: kv(k, adb[k])
        if "aviso" in adb: print("   " + paint(adb["aviso"], "y"))

    fb = read_fastboot()
    if fb:
        achou = True
        print(paint("\n[ Fastboot ]", "c"))
        for k, v in fb.items():
            kv(k, v)

    usb_list = scan_usb()
    for u in usb_list:
        if "erro" in u:
            print("\n" + paint(u["erro"], "y")); continue
        achou = True
        print(paint("\n[ USB %s:%s ]" % (u["vid"], u["pid"]), "c"))
        kv("Modo", u["modo"])
        kv("Plataforma", u["plataforma"])
        kv("Fabricante", u["fabricante"])
        if u.get("usb_prod"): kv("USB diz", u["usb_prod"])
        kv("O que fazer", u["acao"])

    if not HAVE_USB:
        print("\n" + paint("pyusb nao instalado: modos EDL/BROM/SPD nao serao vistos. Rode: pip install pyusb", "y"))
    if shutil.which("adb") is None and shutil.which("fastboot") is None:
        print(paint("platform-tools (adb/fastboot) nao esta no PATH: sem leitura rica de marca/modelo/CPU.", "y"))
    if not achou:
        print("\n" + paint("Nenhum aparelho detectado. Plugue o cabo e confira o driver/modo.", "y"))
    print(paint("\nLembrete: este detector so LE o aparelho. Nao grava, nao remove conta, nao brica.\n", "d"))

def main():
    ap = argparse.ArgumentParser(description="Detector de aparelho Vipcell (read-only).")
    ap.add_argument("--watch", action="store_true", help="vigia e re-detecta a cada 2s")
    a = ap.parse_args()
    if a.watch:
        print("Vigiando USB... (Ctrl+C para sair)")
        try:
            while True:
                report(); time.sleep(2)
        except KeyboardInterrupt:
            print("\nencerrado.")
    else:
        report()

if __name__ == "__main__":
    main()
