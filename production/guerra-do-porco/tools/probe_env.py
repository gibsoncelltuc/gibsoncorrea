#!/usr/bin/env python3
"""Fase 0 — auditoria do ambiente (perfil v3.1 §2 + V2 Fase 0). Gera env_report.json e environment-report.md."""
import json, os, subprocess, shutil, platform, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def sh(c):
    try: return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=25).stdout.strip()
    except Exception as e: return f"erro: {e}"
R = {
 "uname": sh("uname -a"), "cpus": int(sh("nproc") or 0), "mem": sh("free -h | sed -n 2p"), "disk": sh("df -h /home | tail -1"),
 "python": sys.version.split()[0], "pillow_numpy": sh("python3 -c \"import PIL,numpy;print(PIL.__version__,numpy.__version__)\""),
 "node": sh("node --version"), "npm": sh("npm --version"), "ffmpeg": sh("ffmpeg -version | head -1"),
 "chromium": sh("ls /opt/pw-browsers 2>/dev/null | tr '\\n' ' '"), "blender": sh("blender --version 2>&1 | head -1") if shutil.which("blender") else "ausente",
 "gpu": "ausente (nvidia-smi não encontrado)" if not shutil.which("nvidia-smi") else sh("nvidia-smi | head -3"),
 "remotion": sh(f"cd {ROOT} && npx remotion versions 2>/dev/null | grep -m1 'On version'"),
 "network": {"tts_edge": "acessível via HTTPS_PROXY (edge-tts com proxy=...)", "npm_registry": "ok", "pypi": "ok",
             "github.com": "403 (app sem acesso ao repositório / benchmark não clonável)", "nps.gov": "bloqueado (ENOTFOUND)", "historylink.org": "bloqueado (ENOTFOUND)"},
}
cpu = R["cpus"]
R["route"] = "Rota B (V2 principal): Remotion + Three.js/R3F, WebGL via SwiftShader (--gl=swangle), frames em disco + FFmpeg. Rota A (Pillow) disponível como fallback; Blender ausente → Rota C descartada."
R["render_budget"] = {"preview": "540x960 @30fps (≈0,2 s/frame com 4 abas)", "final_1080": "≈0,5 s/frame medido na produção anterior"}
json.dump(R, open(f"{ROOT}/env_report.json", "w"), indent=1, ensure_ascii=False)
open(f"{ROOT}/environment-report.md", "w", encoding="utf-8").write("# Environment report\n\n" + "\n".join(f"- **{k}**: {v}" for k, v in R.items() if not isinstance(v, dict)) + "\n\n## Rede\n" + "\n".join(f"- {k}: {v}" for k, v in R["network"].items()) + "\n")
print(R["route"])
