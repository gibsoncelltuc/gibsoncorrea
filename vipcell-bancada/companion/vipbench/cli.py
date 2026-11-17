"""Vipcell Bancada — companion de PC (linha de comando).

Comandos:
  detectar                 identifica o aparelho conectado e o modo
  recuperar-moto <pasta>   recupera Moto brickado com o firmware OFICIAL

Filosofia: plano primeiro, execução depois. Por padrão só MOSTRA o que vai
fazer (dry-run). Só grava de verdade com --run. Isso é a trava contra
"cliquei no botão errado".
"""

from __future__ import annotations

import argparse
import sys

from . import moto, runner


def _p(msg=""):
    print(msg, flush=True)


def cmd_detectar(args):
    _p("== Detecção ==")
    modos = runner.detect_usb_modes()
    if modos:
        for m in modos:
            _p(f"  [{m['modo'].upper()}] {m['fabricante']} · {m['porta']} "
               f"(VID:PID {m['vid']:04X}:{m['pid']:04X}) · plataforma {m['plataforma']}")
    else:
        _p("  (pyusb não instalado ou nenhum modo baixo detectado — tentando fastboot)")
    try:
        serials = runner.fastboot_devices(args.fastboot)
        if serials:
            for s in serials:
                prod = runner.getvar("product", args.fastboot)
                unlocked = runner.getvar("unlocked", args.fastboot)
                _p(f"  [FASTBOOT] serial {s} · product={prod or '?'} · unlocked={unlocked or '?'}")
        elif not modos:
            _p("  Nenhum aparelho encontrado. Confira driver, cabo e modo (fastboot/BROM).")
    except runner.ToolMissing as e:
        _p(f"  fastboot indisponível: {e}")
    return 0


def _match_product(firmware_model: str, device_product: str) -> bool:
    a = (firmware_model or "").strip().lower()
    b = (device_product or "").strip().lower()
    if not a or not b:
        return False
    return a == b or a in b or b in a


def cmd_recuperar_moto(args):
    fw = args.firmware_dir
    _p("== Recuperar Moto brickado (firmware oficial) ==")
    _p(f"Firmware: {fw}")

    try:
        path = moto.find_flashfile(fw)
        plan = moto.parse_flashfile(path)
    except moto.PlanError as e:
        _p(f"ERRO: {e}")
        return 2

    _p(f"Modelo do firmware: {plan.model or '(não informado no XML)'}  "
       f"versão: {plan.version or '?'}")
    _p(f"Fonte: {plan.source}")

    missing = moto.validate_files(plan, fw)
    if missing:
        _p("ERRO: arquivos citados no flashfile que NÃO estão na pasta:")
        for m in missing:
            _p(f"   - {m}")
        _p("Extraia o firmware completo. Não vou gravar com arquivo faltando.")
        return 2

    cmds = moto.build_command_list(plan, wipe=args.wipe)
    _p("")
    _p(f"Plano ({'COM wipe de dados' if args.wipe else 'SEM apagar dados do cliente'}):")
    for i, s in enumerate(cmds, 1):
        mark = "  (apaga dados)" if s.destructive else ""
        _p(f"  {i:3}. fastboot {' '.join(s.as_fastboot())}{mark}")
    if not args.wipe and plan.destructive_steps:
        _p(f"  ({len(plan.destructive_steps)} passos de apagar dados foram PULADOS; "
           f"use --wipe se o cliente autorizou perder os dados)")

    if not args.run:
        _p("")
        _p(">> Isto foi apenas a PRÉVIA (dry-run). Nada foi gravado.")
        _p(">> Para executar de verdade, rode de novo com  --run")
        return 0

    # Execução real — a partir daqui precisa de aparelho + fastboot.
    _p("")
    _p("== Execução ==")
    try:
        serials = runner.fastboot_devices(args.fastboot)
    except runner.ToolMissing as e:
        _p(f"ERRO: {e}")
        return 2
    if not serials:
        _p("ERRO: nenhum aparelho em fastboot. Coloque o Moto em fastboot (Vol − + Power) e conecte.")
        return 2

    product = runner.getvar("product", args.fastboot)
    _p(f"Aparelho: product={product or '?'}")
    if not _match_product(plan.model, product):
        if not args.force:
            _p(f"ERRO: o firmware é de '{plan.model}' e o aparelho diz '{product}'. "
               "NÃO vou gravar firmware de outro modelo (risco de brick). "
               "Se tiver certeza do modelo, repita com --force.")
            return 3
        _p("AVISO: modelo diferente, mas --force foi passado. Prosseguindo por sua conta.")

    for i, s in enumerate(cmds, 1):
        _p(f"[{i}/{len(cmds)}] fastboot {' '.join(s.as_fastboot())}")
        res = runner.run_fastboot(s.as_fastboot(), args.fastboot)
        tail = (res.err or res.out).strip().splitlines()[-1:] or [""]
        _p(f"      -> {'OK' if res.ok else 'FALHOU'} {tail[0]}")
        if not res.ok and s.op in ("flash", "erase"):
            _p("PAROU: um passo de gravação falhou. Não continuo para não deixar o aparelho pior.")
            _p("Verifique cabo/porta e, se o aparelho não entra em fastboot, use o caminho BROM/LMSA.")
            return 4
    _p("")
    _p("Concluído. Reinicie o aparelho; o primeiro boot pode levar alguns minutos.")
    return 0


def build_parser():
    ap = argparse.ArgumentParser(prog="vipbench", description="Vipcell Bancada — companion de PC")
    ap.add_argument("--fastboot", help="caminho do fastboot.exe (se não estiver no PATH)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("detectar", help="identifica o aparelho e o modo").set_defaults(func=cmd_detectar)

    r = sub.add_parser("recuperar-moto", help="recupera Moto brickado com firmware oficial")
    r.add_argument("firmware_dir", help="pasta do firmware OFICIAL extraído (com flashfile.xml)")
    r.add_argument("--run", action="store_true", help="executa de verdade (sem isto, só mostra o plano)")
    r.add_argument("--wipe", action="store_true", help="também apaga dados (userdata) — só se autorizado")
    r.add_argument("--force", action="store_true", help="ignora a checagem de modelo (perigoso)")
    r.set_defaults(func=cmd_recuperar_moto)
    return ap


def main(argv=None):
    ap = build_parser()
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
