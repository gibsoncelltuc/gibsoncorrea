# -*- coding: utf-8 -*-
"""
Vipcell Box - aplicativo de bancada (Windows).
Janela que detecta o aparelho ao plugar e mostra modo / marca / modelo /
CPU / arquitetura, no estilo do painel de deteccao da Chimera.
SOMENTE LEITURA: nao grava, nao remove conta/FRP, nao brica.

Rodar:   python vipcell_box.py
Gerar .exe (no Windows):  build_exe.bat
"""
import threading
import queue
import tkinter as tk
from tkinter import ttk

import core

BG = "#0A0F0D"; PANEL = "#111A16"; LINE = "#223029"; INK = "#E8F1EC"
MUT = "#8CA398"; BRAND = "#23C277"; CYAN = "#36B5C9"; WARN = "#E7A54B"; BAD = "#F06A5B"

MODE_COLOR = {"ADB": BRAND, "Fastboot": CYAN, "Qualcomm": CYAN, "MediaTek": BRAND,
              "Samsung": "#9D8CF0", "Unisoc": WARN}

def mode_color(painel):
    txt = (painel.get("Modo", "") + painel.get("Plataforma", "") + painel.get("fonte", ""))
    for k, c in MODE_COLOR.items():
        if k.lower() in txt.lower():
            return c
    return MUT

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vipcell Box - Bancada")
        self.configure(bg=BG)
        self.geometry("760x560")
        self.minsize(560, 420)
        self._q = queue.Queue()
        self._last = None
        self._build()
        self.after(200, self._poll_queue)
        self._tick()

    def _build(self):
        top = tk.Frame(self, bg=PANEL, height=58)
        top.pack(fill="x"); top.pack_propagate(False)
        logo = tk.Canvas(top, width=34, height=34, bg=PANEL, highlightthickness=0)
        logo.create_oval(2, 2, 32, 32, fill=BRAND, outline="")
        logo.create_text(17, 17, text="V", fill=BG, font=("Segoe UI", 15, "bold"))
        logo.pack(side="left", padx=(16, 10), pady=12)
        tk.Label(top, text="Vipcell Box", bg=PANEL, fg=INK,
                 font=("Segoe UI Semibold", 15)).pack(side="left", pady=12)
        tk.Label(top, text="bancada - identificacao (somente leitura)", bg=PANEL, fg=MUT,
                 font=("Segoe UI", 9)).pack(side="left", padx=8)
        self.state_dot = tk.Canvas(top, width=12, height=12, bg=PANEL, highlightthickness=0)
        self.state_dot.pack(side="right", padx=(0, 16))
        self._dot = self.state_dot.create_oval(2, 2, 10, 10, fill=MUT, outline="")
        self.state_lbl = tk.Label(top, text="procurando...", bg=PANEL, fg=MUT, font=("Segoe UI", 9))
        self.state_lbl.pack(side="right", padx=6)

        body = tk.Frame(self, bg=BG); body.pack(fill="both", expand=True, padx=14, pady=12)
        self.canvas = tk.Canvas(body, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(body, orient="vertical", command=self.canvas.yview)
        self.holder = tk.Frame(self.canvas, bg=BG)
        self.holder.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.holder, anchor="nw", width=720)
        self.canvas.configure(yscrollcommand=sb.set)
        self.canvas.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")

        foot = tk.Frame(self, bg=PANEL, height=38); foot.pack(fill="x"); foot.pack_propagate(False)
        tk.Label(foot, text="So LE o aparelho. Nao grava, nao remove conta, nao brica.",
                 bg=PANEL, fg=MUT, font=("Segoe UI", 8)).pack(side="left", padx=16)
        tk.Button(foot, text="Atualizar agora", command=self._tick, bg=BRAND, fg=BG,
                  relief="flat", font=("Segoe UI Semibold", 9), padx=12,
                  activebackground=CYAN, cursor="hand2").pack(side="right", padx=14, pady=6)

    def _card(self, painel):
        c = tk.Frame(self.holder, bg=PANEL, highlightbackground=LINE, highlightthickness=1)
        c.pack(fill="x", pady=6)
        bar = tk.Frame(c, bg=mode_color(painel), width=4)
        bar.pack(side="left", fill="y")
        inner = tk.Frame(c, bg=PANEL); inner.pack(side="left", fill="both", expand=True, padx=14, pady=12)
        head = painel.get("Modo", painel.get("fonte", "Aparelho"))
        tk.Label(inner, text=head, bg=PANEL, fg=mode_color(painel),
                 font=("Segoe UI Semibold", 13), anchor="w").pack(fill="x")
        grid = tk.Frame(inner, bg=PANEL); grid.pack(fill="x", pady=(6, 0))
        skip = {"fonte", "Modo"}
        row = 0
        for k, v in painel.items():
            if k in skip:
                continue
            fg = BAD if k in ("Erro",) else WARN if k in ("Aviso",) else INK
            tk.Label(grid, text=k, bg=PANEL, fg=MUT, font=("Segoe UI", 9), anchor="w",
                     width=14).grid(row=row, column=0, sticky="w", pady=1)
            tk.Label(grid, text=str(v), bg=PANEL, fg=fg, font=("Consolas", 10),
                     anchor="w", justify="left", wraplength=560).grid(row=row, column=1, sticky="w", pady=1)
            row += 1

    def _empty(self, avisos):
        c = tk.Frame(self.holder, bg=PANEL, highlightbackground=LINE, highlightthickness=1)
        c.pack(fill="x", pady=6)
        tk.Label(c, text="Nenhum aparelho detectado", bg=PANEL, fg=MUT,
                 font=("Segoe UI Semibold", 12)).pack(anchor="w", padx=16, pady=(14, 2))
        tk.Label(c, text="Plugue o cabo e confira o driver / modo. Em EDL/BROM, troque o driver\n"
                          "da porta para WinUSB (Zadig) para o programa enxergar.",
                 bg=PANEL, fg=MUT, font=("Segoe UI", 9), justify="left").pack(anchor="w", padx=16, pady=(0, 14))
        for a in avisos:
            tk.Label(self.holder, text="- " + a, bg=BG, fg=WARN, font=("Segoe UI", 9),
                     anchor="w", justify="left", wraplength=700).pack(fill="x", padx=4, pady=1)

    def _render(self, paineis, avisos):
        sig = str(paineis)
        if sig == self._last:
            return
        self._last = sig
        for w in self.holder.winfo_children():
            w.destroy()
        on = len(paineis) > 0
        self.state_dot.itemconfig(self._dot, fill=BRAND if on else MUT)
        self.state_lbl.config(text=("aparelho conectado" if on else "procurando..."),
                              fg=INK if on else MUT)
        if not paineis:
            self._empty(avisos)
        else:
            for p in paineis:
                self._card(p)
            for a in avisos:
                tk.Label(self.holder, text="- " + a, bg=BG, fg=WARN, font=("Segoe UI", 8),
                         anchor="w", justify="left", wraplength=700).pack(fill="x", padx=4, pady=1)

    def _worker(self):
        try:
            paineis, avisos = core.detect()
            self._q.put((paineis, avisos))
        except Exception as e:
            self._q.put(([], ["Falha na deteccao: %s" % e]))

    def _tick(self):
        threading.Thread(target=self._worker, daemon=True).start()
        self.after(2000, self._tick)

    def _poll_queue(self):
        try:
            while True:
                paineis, avisos = self._q.get_nowait()
                self._render(paineis, avisos)
        except queue.Empty:
            pass
        self.after(200, self._poll_queue)

if __name__ == "__main__":
    App().mainloop()
