"""Testes do motor Motorola — rodam sem celular e sem fastboot."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vipbench import moto  # noqa: E402

FW = os.path.join(os.path.dirname(__file__), "fw_g56")
FW_INC = os.path.join(os.path.dirname(__file__), "fw_incompleto")
FW_BAD = os.path.join(os.path.dirname(__file__), "fw_perigoso")


def test_parse_lê_modelo_e_passos():
    plan = moto.parse_flashfile(moto.find_flashfile(FW))
    assert plan.model == "fogo"
    assert plan.version.startswith("fogo_g56")
    assert len(plan.steps) == 12


def test_passos_destrutivos_marcados():
    plan = moto.parse_flashfile(moto.find_flashfile(FW))
    destr = [s.partition for s in plan.destructive_steps]
    assert "userdata" in destr and "metadata" in destr


def test_sem_wipe_pula_destrutivos():
    plan = moto.parse_flashfile(moto.find_flashfile(FW))
    cmds = moto.build_command_list(plan, wipe=False)
    assert all(not s.destructive for s in cmds)
    assert not any(s.op == "erase" for s in cmds)


def test_com_wipe_mantém_ordem_original():
    plan = moto.parse_flashfile(moto.find_flashfile(FW))
    cmds = moto.build_command_list(plan, wipe=True)
    assert cmds == plan.steps


def test_comando_fastboot_correto():
    plan = moto.parse_flashfile(moto.find_flashfile(FW))
    flash_boot = next(s for s in plan.steps if s.op == "flash" and s.partition == "boot")
    assert flash_boot.as_fastboot() == ["flash", "boot", "boot.img"]


def test_arquivo_faltando_é_detectado():
    plan = moto.parse_flashfile(moto.find_flashfile(FW_INC))
    missing = moto.validate_files(plan, FW_INC)
    assert "boot.img" in missing and "super.img" in missing


def test_operação_desconhecida_aborta():
    try:
        moto.parse_flashfile(moto.find_flashfile(FW_BAD))
        assert False, "deveria ter abortado"
    except moto.PlanError as e:
        assert "desconhecida" in str(e).lower()


def test_pasta_sem_flashfile_aborta():
    try:
        moto.find_flashfile(os.path.dirname(__file__))
        assert False
    except moto.PlanError:
        pass


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    ok = 0
    for fn in fns:
        fn()
        print(f"  ok  {fn.__name__}")
        ok += 1
    print(f"\n{ok}/{len(fns)} testes passaram")
