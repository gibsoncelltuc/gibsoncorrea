# -*- coding: utf-8 -*-
"""
Vipcell Box - aplicativo de bancada (Windows).
Janela que detecta o aparelho ao plugar e mostra modo / marca / modelo /
CPU / arquitetura, no estilo do painel de deteccao da Chimera.
SOMENTE LEITURA: nao grava, nao remove conta/FRP, nao brica.

Rodar:   python vipcell_box.py
Gerar .exe (no Windows):  build_exe.bat
"""
import os
import time
import threading
import queue
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import core
import mtk_recovery

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
        self._logq = queue.Queue()
        self._last = None
        self._busy = False
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

        # console de recuperacao (saida do mtkclient)
        con = tk.Frame(self, bg=PANEL, highlightbackground=LINE, highlightthickness=1)
        con.pack(fill="x", padx=14, pady=(0, 8))
        hd = tk.Frame(con, bg=PANEL); hd.pack(fill="x", padx=10, pady=(6, 0))
        tk.Label(hd, text="Console de recuperacao", bg=PANEL, fg=MUT,
                 font=("Segoe UI", 8, "bold")).pack(side="left")
        tk.Button(hd, text="limpar", command=lambda: self._clear_console(), bg=PANEL, fg=MUT,
                  relief="flat", font=("Segoe UI", 8), cursor="hand2").pack(side="right")
        self.console = tk.Text(con, height=7, bg="#0C120F", fg="#B9CfC4", insertbackground=INK,
                               font=("Consolas", 9), relief="flat", wrap="word", state="disabled")
        self.console.pack(fill="x", padx=10, pady=(2, 8))
        self._log("Pronto. Plugue o aparelho. Para MediaTek em dead boot, use os botoes do card.")

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
        texto = (painel.get("Modo", "") + painel.get("Plataforma", "")).lower()
        if "mediatek" in texto or "brom" in texto or "preloader" in texto:
            self._mtk_buttons(inner)

    def _mtk_buttons(self, parent):
        box = tk.Frame(parent, bg=PANEL); box.pack(fill="x", pady=(10, 0))
        tk.Label(box, text="Recuperacao MediaTek (dead boot) - via mtkclient",
                 bg=PANEL, fg=CYAN, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 4))
        bar = tk.Frame(box, bg=PANEL); bar.pack(fill="x")
        def mk(txt, cmd, bg=LINE, fg=INK):
            b = tk.Button(bar, text=txt, command=cmd, bg=bg, fg=fg, relief="flat",
                          font=("Segoe UI", 9), padx=10, pady=4, cursor="hand2",
                          activebackground=CYAN)
            b.pack(side="left", padx=(0, 6)); return b
        mk("1. Ler info (seguro)", self._mtk_info)
        mk("2. Backup de seguranca", self._mtk_backup)
        mk("3. Restaurar boot (avancado)", self._mtk_restore, bg="#3A2412", fg=WARN)
        tk.Label(box, text="Faca 1 e 2 antes do 3. Restaurar exige a pasta do firmware oficial do modelo.",
                 bg=PANEL, fg=MUT, font=("Segoe UI", 8), wraplength=640,
                 justify="left").pack(anchor="w", pady=(4, 0))

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

    # ---------- console / log ----------
    def _log(self, text):
        self.console.config(state="normal")
        self.console.insert("end", text + "\n")
        self.console.see("end")
        self.console.config(state="disabled")

    def _log_ts(self, text):
        self._logq.put(text)

    def _clear_console(self):
        self.console.config(state="normal"); self.console.delete("1.0", "end"); self.console.config(state="disabled")

    # ---------- acoes MediaTek ----------
    def _guard(self):
        if not mtk_recovery.available():
            self._log(mtk_recovery.install_hint()); return False
        if self._busy:
            self._log("Aguarde: ja existe uma operacao em andamento."); return False
        return True

    def _spawn(self, fn):
        self._busy = True
        def wrap():
            try:
                fn()
            except Exception as e:
                self._log_ts("Erro: %s" % e)
            finally:
                self._busy = False
                self._log_ts("--- fim ---")
        threading.Thread(target=wrap, daemon=True).start()

    def _mtk_info(self):
        if not self._guard():
            return
        self._log("Lendo tabela de particoes (printgpt)... nao escreve nada.")
        self._spawn(lambda: mtk_recovery.info(self._log_ts))

    def _mtk_backup(self):
        if not self._guard():
            return
        d = filedialog.askdirectory(title="Pasta para salvar o backup")
        if not d:
            return
        dest = os.path.join(d, "vipcell_backup_%s" % time.strftime("%Y%m%d_%H%M%S"))
        self._log("Backup das particoes criticas em: %s" % dest)
        self._spawn(lambda: mtk_recovery.backup(dest, self._log_ts))

    def _mtk_restore(self):
        if not self._guard():
            return
        d = filedialog.askdirectory(title="Pasta do firmware oficial (preloader.bin, lk.img, boot.img...)")
        if not d:
            return
        ok = messagebox.askyesno("Confirmar gravacao",
            "Vou GRAVAR particoes de boot no aparelho a partir de:\n%s\n\n"
            "Isso e irreversivel e pode piorar o brick se o firmware for do modelo errado.\n"
            "Fez o backup (botao 2)? Deseja continuar?" % d)
        if not ok:
            self._log("Restauro cancelado pelo operador.")
            return
        self._log("Restaurando boot a partir de: %s" % d)
        self._spawn(lambda: mtk_recovery.restore_from_folder(d, self._log_ts, confirm=True))

    def _worker(self):
        try:
            paineis, avisos = core.detect()
            self._q.put((paineis, avisos))
        except Exception as e:
            self._q.put(([], ["Falha na deteccao: %s" % e]))

    def _tick(self):
        if not self._busy:   # nao varrer durante uma operacao do mtkclient (disputa de porta)
            threading.Thread(target=self._worker, daemon=True).start()
        self.after(2000, self._tick)

    def _poll_queue(self):
        try:
            while True:
                paineis, avisos = self._q.get_nowait()
                self._render(paineis, avisos)
        except queue.Empty:
            pass
        try:
            while True:
                self._log(self._logq.get_nowait())
        except queue.Empty:
            pass
        self.after(200, self._poll_queue)

if __name__ == "__main__":
    App().mainloop()
