"""Localizador e baixador de firmware OFICIAL (Motorola).

Dois problemas reais que este módulo resolve:

1. Anti-rollback: se o firmware for mais antigo que o aparelho, o flash falha
   logo no começo ("Preflash validation failed"), e NÃO há bypass seguro.
   Então a regra é pegar firmware com versão/patch igual ou mais novo.

2. Achar o firmware certo do modelo exato. Aqui lemos o codinome e a versão
   direto do aparelho (fastboot getvar) e indicamos onde pegar o oficial.

O download é só de fonte OFICIAL que você aponta (LMSA, ou o mirror oficial
por codinome). O programa baixa e CONFERE o hash — não sai catando arquivo de
fórum (que é o que infecta PC e brica aparelho).
"""

from __future__ import annotations

import hashlib
import os
import urllib.request
from dataclasses import dataclass

from . import runner

# Fontes oficiais / mirrors de firmware assinado da Motorola.
OFFICIAL_SOURCES = [
    ("LMSA (Rescue and Smart Assistant)", "https://www.motorola.com/rescue",
     "Baixa o firmware oficial do modelo automaticamente. Caminho mais seguro."),
    ("Mirror oficial (lolinet)", "https://mirrors.lolinet.com/firmware/moto/",
     "Pasta por codinome; pegue a versão mais NOVA do canal da região (ex. retbr)."),
]


@dataclass
class DeviceInfo:
    product: str = ""          # codinome, ex. "fogo"
    version_bootloader: str = ""
    version_baseband: str = ""
    unlocked: str = ""
    current_slot: str = ""

    @property
    def known(self) -> bool:
        return bool(self.product)


def read_device(fastboot: str | None = None) -> DeviceInfo:
    """Lê os dados do aparelho em fastboot para guiar a escolha do firmware."""
    return DeviceInfo(
        product=runner.getvar("product", fastboot),
        version_bootloader=runner.getvar("version-bootloader", fastboot),
        version_baseband=runner.getvar("version-baseband", fastboot),
        unlocked=runner.getvar("unlocked", fastboot),
        current_slot=runner.getvar("current-slot", fastboot),
    )


def advise(info: DeviceInfo) -> list[str]:
    """Monta as orientações de qual firmware pegar, com o alerta de rollback."""
    out = []
    if info.known:
        out.append(f"Aparelho: codinome '{info.product}' · bootloader "
                   f"{info.version_bootloader or '?'} · slot {info.current_slot or '?'}")
    else:
        out.append("Não consegui ler o aparelho. Coloque em fastboot e conecte.")
    out.append("")
    out.append("REGRA DE OURO (anti-rollback): pegue o firmware com versão/patch de "
               "segurança IGUAL ou MAIS NOVO que o do aparelho. Firmware mais antigo "
               "falha no 1º passo (Preflash validation failed) e isso NÃO tem bypass seguro.")
    out.append("")
    out.append("Onde pegar o firmware OFICIAL deste modelo:")
    for nome, url, nota in OFFICIAL_SOURCES:
        slug = info.product or "<codinome>"
        link = url + (slug + "/" if "lolinet" in url and info.product else "")
        out.append(f"  • {nome}: {link}")
        out.append(f"      {nota}")
    out.append("")
    out.append("Depois de baixar, extraia a pasta (com flashfile.xml) e rode:")
    out.append("  python -m vipbench.cli recuperar-moto <pasta>   (prévia)")
    out.append("  python -m vipbench.cli recuperar-moto <pasta> --run")
    return out


def sha256_file(path: str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def download(url: str, dest: str, expected_sha256: str | None = None,
             progress=None) -> str:
    """Baixa de uma URL OFICIAL para `dest`, com retomada e verificação de hash.

    Levanta exceção se o hash informado não bater (arquivo corrompido ou trocado).
    """
    if not url.lower().startswith(("http://", "https://")):
        raise ValueError("URL inválida. Use o link oficial (http/https).")
    tmp = dest + ".part"
    start = os.path.getsize(tmp) if os.path.exists(tmp) else 0
    req = urllib.request.Request(url)
    if start:
        req.add_header("Range", f"bytes={start}-")
    with urllib.request.urlopen(req, timeout=60) as r, open(tmp, "ab") as f:
        total = int(r.headers.get("Content-Length", 0)) + start
        done = start
        while True:
            block = r.read(1 << 20)
            if not block:
                break
            f.write(block)
            done += len(block)
            if progress:
                progress(done, total)
    os.replace(tmp, dest)
    if expected_sha256:
        got = sha256_file(dest)
        if got.lower() != expected_sha256.lower():
            raise ValueError(f"Hash não confere! esperado {expected_sha256}, obtido {got}. "
                             "NÃO use este arquivo — pode estar corrompido ou adulterado.")
    return dest
