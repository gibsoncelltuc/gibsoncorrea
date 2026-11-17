import importlib, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
total = ok = 0
for mod in ("tests.test_moto", "tests.test_firmware"):
    m = importlib.import_module(mod)
    for name in sorted(n for n in dir(m) if n.startswith("test_")):
        total += 1
        try:
            getattr(m, name)(); ok += 1; print(f"  ok   {mod}.{name}")
        except Exception as e:
            print(f"  FALHOU {mod}.{name}: {e}")
print(f"\n{ok}/{total} testes passaram")
sys.exit(0 if ok == total else 1)
