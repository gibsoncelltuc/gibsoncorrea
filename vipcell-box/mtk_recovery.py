# -*- coding: utf-8 -*-
"""
Vipcell Box - modulo de recuperacao MediaTek (dead boot / brick).

NAO reimplementa o flasher. Pilota o mtkclient (open-source, bkerler),
que e o motor testado para BootROM/Preloader MediaTek. Fornece:

  - localizar o mtkclient instalado no PC
  - comandos SEGUROS (leitura): info da GPT, backup de particoes criticas
  - comando AVANCADO (escrita): restaurar preloader/lk/boot/vbmeta a partir
    de uma pasta de firmware que o tecnico baixou (nunca embutido aqui)

Tudo roda como subprocesso e devolve a saida linha a linha para a janela.

Aviso honesto: chips MediaTek novos (Dimensity 7060 do Moto G56, e a serie
70/80/90 em geral) podem ter protecao de BootROM (SLA/DAA) que o mtkclient
ainda nao contorna. Se o mtkclient nao "handshake", a recuperacao livre
pode nao ser possivel nesse chip - isso nao e defeito deste programa.
"""
import os
import sys
import shutil
import subprocess

# Particoes que costumam morrer num "dead boot" MediaTek e que um backup
# deve salvar antes de qualquer escrita. userdata NAO entra (enorme).
CRITICAS = ["preloader", "pgpt", "sgpt", "boot", "lk", "lk1", "lk2", "dtbo",
            "vbmeta", "vbmeta_system", "vbmeta_vendor", "md1img", "logo", "tee1", "tee2"]

# Ordem tipica de regravacao para reviver o boot (as que existirem no firmware).
RESTAURO = ["preloader", "pgpt", "lk", "lk1", "lk2", "boot", "dtbo",
            "vbmeta", "vbmeta_system", "vbmeta_vendor", "md1img", "tee1", "tee2"]

def find_mtk():
    """Devolve o comando base para rodar o mtkclient, ou None.
    Procura: comando 'mtk' no PATH, modulo python instalado, ou mtk.py local."""
    if shutil.which("mtk"):
        return ["mtk"]
    # modulo instalado via pip (pip install mtkclient). Nao vale rodando como
    # .exe empacotado: sys.executable seria o proprio exe.
    if not getattr(sys, "frozen", False):
        try:
            import importlib.util
            if importlib.util.find_spec("mtkclient"):
                return [sys.executable, "-m", "mtkclient.mtk"]
        except Exception:
            pass
    for base in (os.path.dirname(os.path.abspath(__file__)), os.getcwd()):
        for cand in ("mtk.py", os.path.join("mtkclient", "mtk.py")):
            p = os.path.join(base, cand)
            if os.path.isfile(p):
                return [sys.executable, p]
    return None

def available():
    return find_mtk() is not None

def install_hint():
    return ("mtkclient nao encontrado. No Windows:\n"
            "  pip install mtkclient\n"
            "ou baixe de github.com/bkerler/mtkclient e deixe a pasta ao lado do programa.\n"
            "Instale tambem o driver MediaTek e, se preciso, troque a porta para WinUSB (Zadig).")

def _run_stream(args, on_line, cwd=None):
    """Roda mtkclient com os args dados, enviando cada linha a on_line.
    Devolve o codigo de saida (0 = ok). Nunca levanta; reporta por on_line."""
    base = find_mtk()
    if base is None:
        on_line(install_hint())
        return 127
    cmd = base + args
    on_line("> " + " ".join(cmd))
    try:
        p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, text=True, bufsize=1)
    except Exception as e:
        on_line("Falha ao iniciar o mtkclient: %s" % e)
        return 1
    try:
        for line in iter(p.stdout.readline, ""):
            on_line(line.rstrip("\n"))
    except Exception as e:
        on_line("Erro lendo saida: %s" % e)
    p.wait()
    on_line("[mtkclient terminou com codigo %s]" % p.returncode)
    return p.returncode

# ---- acoes SEGURAS (somente leitura) ----
def info(on_line):
    """Le a tabela de particoes (GPT). Nao escreve nada."""
    return _run_stream(["printgpt"], on_line)

def backup(dest_dir, on_line):
    """Salva as particoes criticas em dest_dir antes de qualquer escrita."""
    os.makedirs(dest_dir, exist_ok=True)
    rc_any = 1
    for part in CRITICAS:
        out = os.path.join(dest_dir, part + ".bin")
        on_line("\n-- backup %s --" % part)
        rc = _run_stream(["r", part, out], on_line)
        if rc == 0:
            rc_any = 0
    on_line("\nBackup concluido em: %s" % dest_dir)
    return rc_any

# ---- acao AVANCADA (escrita) ----
def restore_from_folder(fw_dir, on_line, confirm=False):
    """Regrava as particoes de boot a partir de uma pasta de firmware.
    Procura arquivos <particao>.img/.bin em fw_dir. So escreve o que achar.
    Exige confirm=True (a janela pede confirmacao explicita antes)."""
    if not confirm:
        on_line("Escrita cancelada: confirmacao nao dada.")
        return 1
    if not os.path.isdir(fw_dir):
        on_line("Pasta de firmware invalida: %s" % fw_dir)
        return 1
    achados = []
    for part in RESTAURO:
        for ext in (".img", ".bin"):
            f = os.path.join(fw_dir, part + ext)
            if os.path.isfile(f):
                achados.append((part, f)); break
    if not achados:
        on_line("Nenhum arquivo de particao reconhecido em %s.\n"
                "Esperado: preloader.bin, lk.img, boot.img, vbmeta.img, etc." % fw_dir)
        return 1
    on_line("Vou gravar, nesta ordem: " + ", ".join(p for p, _ in achados))
    rc_any = 1
    for part, f in achados:
        on_line("\n-- gravando %s <- %s --" % (part, os.path.basename(f)))
        rc = _run_stream(["w", part, f], on_line)
        if rc == 0:
            rc_any = 0
        else:
            on_line("!! falha ao gravar %s - parando por seguranca." % part)
            break
    on_line("\nSe o preloader e o lk gravaram, tente ligar segurando as teclas de boot.")
    return rc_any
