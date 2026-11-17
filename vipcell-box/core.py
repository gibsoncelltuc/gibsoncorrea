# -*- coding: utf-8 -*-
"""
Vipcell Box - nucleo de deteccao (somente leitura).
Compartilhado pela interface grafica (vipcell_box.py) e pela versao de
linha de comando (detector.py). Nao grava nada no aparelho.
"""
import shutil
import subprocess

try:
    import usb.core
    import usb.util
    HAVE_USB = True
except Exception:
    HAVE_USB = False

# (vid, pid) -> (modo, plataforma, acao).  pid 0xFFFF casa qualquer produto do fabricante.
KNOWN = {
    (0x05C6, 0x9008): ("Qualcomm EDL (9008)", "Qualcomm", "QFIL / edl: gravar com firehose do chip"),
    (0x05C6, 0x9006): ("Qualcomm Diag (9006)", "Qualcomm", "Modo diag - intermediario"),
    (0x05C6, 0x900E): ("Qualcomm Diag (900E)", "Qualcomm", "Modo diag"),
    (0x05C6, 0x676C): ("Qualcomm Download", "Qualcomm", "Modo download Qualcomm"),
    (0x0E8D, 0x0003): ("MediaTek BROM (BootROM)", "MediaTek", "mtkclient / SP Flash Tool (Download)"),
    (0x0E8D, 0x2000): ("MediaTek Preloader", "MediaTek", "SP Flash Tool / mtkclient"),
    (0x0E8D, 0x2001): ("MediaTek Preloader (DA)", "MediaTek", "SP Flash Tool / mtkclient"),
    (0x0E8D, 0x20FF): ("MediaTek BROM (preloader off)", "MediaTek", "mtkclient em bootrom"),
    (0x04E8, 0x685D): ("Samsung Download (Odin)", "Samsung", "Odin / Heimdall: gravar .tar.md5"),
    (0x04E8, 0x6860): ("Samsung MTP (ligado)", "Samsung", "Aparelho ligado - use ADB"),
    (0x04E8, 0x685E): ("Samsung Modem/Download", "Samsung", "Odin / Heimdall"),
    (0x1782, 0x4D00): ("Unisoc/SPRD Diag", "Unisoc", "SPD Upgrade / Research Download (pac)"),
    (0x1782, 0x3D00): ("Unisoc/SPRD Download", "Unisoc", "SPD Upgrade Tool"),
    (0x18D1, 0xD00D): ("Fastboot (Google/Android)", "Android", "fastboot getvar"),
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

def _run(cmd, timeout=8):
    if shutil.which(cmd[0]) is None:
        return None
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return (p.stdout or "") + (p.stderr or "")
    except Exception:
        return None

def read_adb():
    out = _run(["adb", "devices"])
    if not out:
        return None
    if "\tunauthorized" in out:
        return {"fonte": "ADB", "Modo": "ADB (nao autorizado)",
                "Aviso": "Aceite 'Permitir depuracao USB' na tela do aparelho."}
    if "\tdevice" not in out:
        return None
    rot = [("ro.product.manufacturer", "Marca"), ("ro.product.model", "Modelo"),
           ("ro.product.device", "Codinome"), ("ro.board.platform", "Plataforma"),
           ("ro.product.cpu.abi", "Arquitetura"), ("ro.hardware", "Chipset"),
           ("ro.build.version.release", "Android"), ("ro.build.version.security_patch", "Patch")]
    info = {"fonte": "ADB", "Modo": "ADB (sistema ligado)"}
    for prop, label in rot:
        r = _run(["adb", "shell", "getprop", prop])
        if r and r.strip():
            info[label] = r.strip()
    return info

def read_fastboot():
    out = _run(["fastboot", "devices"])
    if not out or "fastboot" not in out.lower():
        return None
    info = {"fonte": "Fastboot", "Modo": "Fastboot / Bootloader"}
    rot = [("product", "Modelo"), ("variant", "Variante"), ("cpu-abi", "Arquitetura"),
           ("unlocked", "Bootloader"), ("secure", "Secure"), ("version-bootloader", "Bootloader ver"),
           ("serialno", "Serial"), ("current-slot", "Slot")]
    for var, label in rot:
        r = _run(["fastboot", "getvar", var])
        if r:
            for line in r.splitlines():
                if line.lower().startswith(var):
                    val = line.split(":", 1)[-1].strip()
                    if val:
                        info[label] = val
                    break
    return info

def scan_usb():
    achados = []
    if not HAVE_USB:
        return achados
    try:
        devs = list(usb.core.find(find_all=True))
    except Exception as e:
        return [{"fonte": "USB", "Erro": "Backend libusb ausente? %s" % e}]
    for d in devs:
        vid, pid = d.idVendor, d.idProduct
        trio = KNOWN.get((vid, pid)) or KNOWN.get((vid, 0xFFFF))
        if trio is None and vid not in VENDOR:
            continue
        modo, plat, acao = trio if trio else ("USB do fabricante (modo nao mapeado)",
                                              VENDOR.get(vid, "?"), "Confirme o modo pelas teclas")
        prod = None
        try:
            prod = usb.util.get_string(d, d.iProduct) if d.iProduct else None
        except Exception:
            pass
        item = {"fonte": "USB", "USB": "%04X:%04X" % (vid, pid), "Modo": modo,
                "Plataforma": plat, "Fabricante": VENDOR.get(vid, "Desconhecido"),
                "O que fazer": acao}
        if prod:
            item["USB diz"] = prod
        achados.append(item)
    return achados

def detect():
    """Retorna (paineis, avisos). paineis = lista de dicts ordenados."""
    paineis = []
    for fn in (read_adb, read_fastboot):
        r = fn()
        if r:
            paineis.append(r)
    paineis.extend(scan_usb())
    avisos = []
    if not HAVE_USB:
        avisos.append("pyusb nao instalado - modos EDL/BROM/SPD nao serao vistos (pip install pyusb).")
    if shutil.which("adb") is None and shutil.which("fastboot") is None:
        avisos.append("platform-tools (adb/fastboot) fora do PATH - sem marca/modelo/CPU ricos.")
    return paineis, avisos
