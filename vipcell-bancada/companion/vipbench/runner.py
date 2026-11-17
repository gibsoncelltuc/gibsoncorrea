"""Camada que fala com os binários externos (fastboot) e com a USB.

Fica isolada de propósito: o motor (moto.py) monta o plano e os testes
verificam o plano sem precisar de celular. Aqui mora a parte que só funciona
no PC do técnico, com aparelho conectado.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass


class ToolMissing(Exception):
    pass


def _fastboot_bin(explicit: str | None = None) -> str:
    cand = explicit or shutil.which("fastboot")
    if not cand:
        raise ToolMissing(
            "fastboot não encontrado. Instale o platform-tools (Google) e deixe no PATH, "
            "ou aponte com --fastboot C:\\caminho\\fastboot.exe"
        )
    return cand


@dataclass
class CmdResult:
    args: list[str]
    code: int
    out: str
    err: str

    @property
    def ok(self) -> bool:
        return self.code == 0


def run_fastboot(fb_args: list[str], fastboot: str | None = None, timeout: int = 300) -> CmdResult:
    binp = _fastboot_bin(fastboot)
    proc = subprocess.run(
        [binp, *fb_args],
        capture_output=True, text=True, timeout=timeout,
    )
    # fastboot escreve quase tudo em stderr
    return CmdResult([binp, *fb_args], proc.returncode, proc.stdout, proc.stderr)


def fastboot_devices(fastboot: str | None = None) -> list[str]:
    res = run_fastboot(["devices"], fastboot)
    serials = []
    for line in (res.out + res.err).splitlines():
        line = line.strip()
        if line and "fastboot" in line:
            serials.append(line.split()[0])
    return serials


def getvar(var: str, fastboot: str | None = None) -> str:
    """Lê uma variável do aparelho em fastboot (ex. product, unlocked)."""
    res = run_fastboot(["getvar", var], fastboot, timeout=20)
    for line in (res.err + res.out).splitlines():
        line = line.strip()
        if line.lower().startswith(f"{var}:".lower()):
            return line.split(":", 1)[1].strip()
    return ""


def detect_usb_modes():
    """Detecta modos de baixo nível (BROM/EDL/Download) lendo a USB via pyusb.

    pyusb é opcional; se não estiver instalado, devolve lista vazia e a
    detecção recai sobre `fastboot devices` / `adb devices`.
    """
    try:
        import usb.core  # type: ignore
    except Exception:
        return []
    from .usbids import lookup, vendor_name
    found = []
    for dev in usb.core.find(find_all=True):
        info = lookup(dev.idVendor, dev.idProduct)
        if info:
            modo, rotulo, plataforma = info
            found.append({
                "vid": dev.idVendor, "pid": dev.idProduct,
                "modo": modo, "porta": rotulo, "plataforma": plataforma,
                "fabricante": vendor_name(dev.idVendor),
            })
    return found
