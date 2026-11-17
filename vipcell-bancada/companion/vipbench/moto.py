"""Motor de recuperação Motorola por fastboot, a partir do firmware OFICIAL.

Um pacote de firmware oficial da Motorola traz um `flashfile.xml` (ou
`servicefile.xml`) que lista, passo a passo, os comandos fastboot que a
própria Motorola executa. Este módulo lê esse XML e monta o MESMO plano,
sem inventar nada — é o que o LMSA faz por baixo.

As travas de segurança (o ponto central): nada é executado às cegas.
  * Operações desconhecidas ABORTAM o plano (fail-safe).
  * Passos destrutivos (apagar userdata/metadata) ficam separados e só
    entram com wipe=True.
  * Todo filename referenciado tem de existir na pasta do firmware.
  * O modelo do firmware é comparado com o `getvar product` do aparelho
    antes de gravar (feito no runner), para não gravar firmware de outro
    aparelho — a causa nº 1 de brick por descuido.
"""

from __future__ import annotations

import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

# Operações que sabemos executar com segurança. Qualquer coisa fora disto
# faz o plano parar, em vez de rodar um comando que não entendemos.
KNOWN_OPS = {"getvar", "oem", "flash", "erase", "reboot", "reboot-bootloader",
             "reboot-fastboot", "continue"}

# Partições cuja escrita/apagamento apaga dados do cliente.
DESTRUCTIVE_PARTITIONS = {"userdata", "metadata", "carrier", "ddr"}

# Partições lógicas (super dinâmico): em alguns modelos precisam do fastbootd.
LOGICAL_PARTITIONS = {"super", "system", "system_ext", "vendor", "product",
                      "odm", "vendor_dlkm", "system_dlkm", "system_a", "vendor_a"}

# Trechos que a saída do fastboot traz quando o firmware é mais antigo que o
# aparelho (anti-rollback). Serve para dar uma mensagem clara em vez do erro cru.
ROLLBACK_MARKERS = (
    "preflash validation failed",
    "security version downgrade",
    "version downgraded",
    "anti-rollback",
    "img antirollback",
    "failed to validate",
)

FLASHFILE_NAMES = ("flashfile.xml", "servicefile.xml")


@dataclass
class Step:
    op: str
    partition: str = ""
    filename: str = ""
    var: str = ""
    destructive: bool = False

    def as_fastboot(self) -> list[str]:
        """Devolve os argumentos fastboot deste passo (sem o binário)."""
        if self.op == "getvar":
            return ["getvar", self.var or "all"]
        if self.op == "oem":
            return ["oem", self.var]
        if self.op == "flash":
            return ["flash", self.partition, self.filename]
        if self.op == "erase":
            return ["erase", self.partition]
        if self.op == "reboot-bootloader":
            return ["reboot-bootloader"]
        if self.op == "reboot-fastboot":
            return ["reboot", "fastboot"]
        if self.op == "reboot":
            return ["reboot"]
        if self.op == "continue":
            return ["continue"]
        raise ValueError(f"operação sem mapeamento: {self.op}")


@dataclass
class FlashPlan:
    model: str = ""
    version: str = ""
    steps: list[Step] = field(default_factory=list)
    source: str = ""

    @property
    def safe_steps(self) -> list[Step]:
        return [s for s in self.steps if not s.destructive]

    @property
    def destructive_steps(self) -> list[Step]:
        return [s for s in self.steps if s.destructive]


class PlanError(Exception):
    pass


def find_flashfile(firmware_dir: str) -> str:
    for name in FLASHFILE_NAMES:
        p = os.path.join(firmware_dir, name)
        if os.path.isfile(p):
            return p
    raise PlanError(
        "Não achei flashfile.xml nem servicefile.xml na pasta do firmware. "
        "Confirme que você extraiu o firmware OFICIAL completo da Motorola."
    )


def _is_destructive(op: str, partition: str) -> bool:
    if op == "erase" and partition in DESTRUCTIVE_PARTITIONS:
        return True
    if op == "flash" and partition in DESTRUCTIVE_PARTITIONS:
        return True
    return False


def parse_flashfile(path: str) -> FlashPlan:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        raise PlanError(f"flashfile.xml inválido: {e}")

    plan = FlashPlan(source=path)

    header = root.find(".//header")
    if header is not None:
        pm = header.find("phone_model")
        if pm is not None:
            plan.model = (pm.get("model") or pm.get("name") or "").strip()
        sv = header.find("software_version")
        if sv is not None:
            plan.version = (sv.get("version") or "").strip()

    steps_nodes = root.findall(".//step")
    if not steps_nodes:
        raise PlanError("O flashfile.xml não tem passos (<step>). Firmware incompleto?")

    for node in steps_nodes:
        op = (node.get("operation") or "").strip().lower()
        if op not in KNOWN_OPS:
            # Fail-safe: não executamos o que não entendemos.
            raise PlanError(
                f"Operação desconhecida no flashfile: '{op}'. "
                "Por segurança o plano foi interrompido — não vou rodar um comando que não reconheço."
            )
        partition = (node.get("partition") or "").strip()
        filename = (node.get("filename") or "").strip()
        var = (node.get("var") or "").strip()
        plan.steps.append(
            Step(
                op=op,
                partition=partition,
                filename=filename,
                var=var,
                destructive=_is_destructive(op, partition),
            )
        )
    return plan


def validate_files(plan: FlashPlan, firmware_dir: str) -> list[str]:
    """Confere que todo arquivo citado existe. Devolve a lista de faltantes."""
    missing = []
    for s in plan.steps:
        if s.op == "flash" and s.filename:
            if not os.path.isfile(os.path.join(firmware_dir, s.filename)):
                missing.append(s.filename)
    return missing


def is_rollback_failure(output: str) -> bool:
    """True se a saída do fastboot indicar firmware mais antigo (anti-rollback)."""
    low = (output or "").lower()
    return any(m in low for m in ROLLBACK_MARKERS)


def needs_fastbootd(plan: FlashPlan) -> bool:
    """True se o plano grava partição lógica (super) — pode exigir fastbootd."""
    has_logical = any(s.op == "flash" and s.partition in LOGICAL_PARTITIONS
                      for s in plan.steps)
    switches = any(s.op == "reboot-fastboot" for s in plan.steps)
    return has_logical and not switches


def build_command_list(plan: FlashPlan, wipe: bool) -> list[Step]:
    """Monta a sequência final respeitando a trava de wipe.

    Sem wipe (padrão): pula passos destrutivos, preservando dados do cliente.
    Com wipe: mantém a ordem original do flashfile.
    """
    if wipe:
        return list(plan.steps)
    return [s for s in plan.steps if not s.destructive]
