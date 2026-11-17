"""Mapa de códigos USB (VID:PID) para modo de conexão.

Usado pela detecção automática: ao conectar o aparelho, o Windows expõe uma
porta com um VID:PID conhecido, e isso já diz em que modo o aparelho está.
Fonte: drivers oficiais e bases públicas de VID:PID.
"""

# (vid, pid) -> (modo, rótulo da porta, plataforma)
USB_MODES = {
    (0x05C6, 0x9008): ("edl",        "Qualcomm HS-USB QDLoader 9008", "qualcomm"),
    (0x18D1, 0x9008): ("edl",        "Qualcomm HS-USB QDLoader 9008", "qualcomm"),
    (0x0E8D, 0x0003): ("brom",       "MediaTek USB Port (BROM)",      "mediatek"),
    (0x0E8D, 0x2000): ("preloader",  "MediaTek USB VCOM (Preloader)", "mediatek"),
    (0x0E8D, 0x2001): ("preloader",  "MediaTek USB VCOM (Preloader)", "mediatek"),
    (0x04E8, 0x685D): ("download",   "Samsung Mobile USB (Download)", "samsung"),
    (0x1782, 0x4D00): ("unisoc",     "SPRD U2S Diag",                 "unisoc"),
    # fastboot / adb: VID do fabricante varia, o PID identifica o modo
    (0x18D1, 0xD00D): ("fastboot",   "Android Bootloader (fastboot)", "android"),
    (0x22B8, 0x2E80): ("fastboot",   "Motorola Fastboot",             "motorola"),
    (0x22B8, 0x2E76): ("fastboot",   "Motorola Fastboot",             "motorola"),
    (0x2717, 0xFF40): ("fastboot",   "Xiaomi Fastboot",               "xiaomi"),
    (0x18D1, 0x4EE7): ("adb",        "Android ADB",                   "android"),
}

# VIDs de fabricante, para reconhecer a marca mesmo quando o PID é desconhecido
VENDORS = {
    0x22B8: "Motorola",
    0x2717: "Xiaomi",
    0x04E8: "Samsung",
    0x2A70: "OnePlus/Oppo",
    0x18D1: "Google",
    0x0E8D: "MediaTek",
    0x05C6: "Qualcomm",
    0x1782: "Unisoc",
}


def lookup(vid: int, pid: int):
    """Retorna (modo, rotulo, plataforma) ou None se o par for desconhecido."""
    return USB_MODES.get((vid, pid))


def vendor_name(vid: int) -> str:
    return VENDORS.get(vid, f"VID 0x{vid:04X}")
