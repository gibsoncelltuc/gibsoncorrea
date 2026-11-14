#!/usr/bin/env python3
"""Validate the basic timing and format contracts of a production folder."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path


def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError(f"Arquivo ausente: {path}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido em {path}: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path, help="Pasta com production.json e shots.json")
    parser.add_argument("--tolerance", type=float, default=0.08, help="Tolerância em segundos para a duração")
    args = parser.parse_args()
    folder = args.folder

    try:
        production = load_json(folder / "production.json")
        shot_data = load_json(folder / "shots.json")
    except ValueError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []

    for key in ("title", "width", "height", "fps", "durationSeconds", "format"):
        if key not in production:
            errors.append(f"production.json sem campo obrigatório: {key}")

    try:
        width = int(production["width"])
        height = int(production["height"])
        fps = float(production["fps"])
        duration = float(production["durationSeconds"])
        if width <= 0 or height <= 0 or fps <= 0 or duration <= 0:
            errors.append("width, height, fps e durationSeconds devem ser positivos")
    except (KeyError, TypeError, ValueError):
        width = height = 0
        fps = duration = 0
        errors.append("Resolução, fps ou duração inválidos")

    if width and height:
        ratio = width / height
        if abs(ratio - 9 / 16) < 0.02:
            orientation = "vertical 9:16"
        elif abs(ratio - 16 / 9) < 0.02:
            orientation = "horizontal 16:9"
        else:
            orientation = f"proporção personalizada ({ratio:.3f})"
        print(f"Formato: {width}x{height} @ {fps:g} fps — {orientation}")

    shots = shot_data.get("shots")
    if not isinstance(shots, list) or not shots:
        errors.append("shots.json precisa conter uma lista não vazia em 'shots'")
        shots = []

    parsed = []
    for index, shot in enumerate(shots, start=1):
        try:
            shot_id = str(shot.get("id", f"shot-{index}"))
            start = float(shot["start"])
            end = float(shot["end"])
            if end <= start:
                errors.append(f"{shot_id}: end precisa ser maior que start")
            parsed.append((start, end, shot_id))
            for field in ("purpose", "camera", "action"):
                if field not in shot:
                    warnings.append(f"{shot_id}: campo recomendado ausente: {field}")
        except (KeyError, TypeError, ValueError):
            errors.append(f"Plano {index}: timecodes inválidos")

    parsed.sort(key=lambda x: x[0])
    if parsed:
        if parsed[0][0] > args.tolerance:
            warnings.append(f"Timeline começa em {parsed[0][0]:.2f}s, não em 0s")
        for previous, current in zip(parsed, parsed[1:]):
            gap = current[0] - previous[1]
            if gap > args.tolerance:
                warnings.append(f"Lacuna entre {previous[2]} e {current[2]}: {gap:.2f}s")
            elif gap < -args.tolerance:
                errors.append(f"Sobreposição entre {previous[2]} e {current[2]}: {-gap:.2f}s")
        last_end = max(item[1] for item in parsed)
        if duration and abs(last_end - duration) > args.tolerance:
            warnings.append(f"Último plano termina em {last_end:.2f}s; projeto declara {duration:.2f}s")

    print(f"Planos: {len(shots)}")
    for warning in warnings:
        print(f"AVISO: {warning}")
    for error in errors:
        print(f"ERRO: {error}")

    if errors:
        print("Resultado: REPROVADO")
        return 1
    print("Resultado: APROVADO (com avisos, se houver)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
