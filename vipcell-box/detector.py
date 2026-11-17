#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vipcell Box - versao linha de comando (sem janela).
Mesma deteccao do aplicativo, para quem prefere terminal ou script.
    python detector.py
    python detector.py --watch
"""
import sys
import time
import argparse
import core

def show():
    paineis, avisos = core.detect()
    print("\n== Vipcell Box - Detector (somente leitura) ==")
    if not paineis:
        print("\nNenhum aparelho detectado. Plugue o cabo e confira o driver/modo.")
    for p in paineis:
        print("\n[ %s ]" % p.get("Modo", p.get("fonte", "Aparelho")))
        for k, v in p.items():
            if k in ("fonte", "Modo"):
                continue
            print("   %-14s %s" % (k + ":", v))
    for a in avisos:
        print("\n! " + a)
    print("\nSo LE o aparelho. Nao grava, nao remove conta, nao brica.\n")

def main():
    ap = argparse.ArgumentParser(description="Detector Vipcell Box (read-only).")
    ap.add_argument("--watch", action="store_true", help="re-detecta a cada 2s")
    a = ap.parse_args()
    if a.watch:
        print("Vigiando USB... (Ctrl+C para sair)")
        try:
            while True:
                show(); time.sleep(2)
        except KeyboardInterrupt:
            print("\nencerrado.")
    else:
        show()

if __name__ == "__main__":
    main()
