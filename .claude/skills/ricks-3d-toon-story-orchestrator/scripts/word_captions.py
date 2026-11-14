#!/usr/bin/env python3
"""Convert real word timestamps JSON into readable 1–2 word SRT captions."""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def stamp(seconds: float) -> str:
    millis = max(0, round(seconds * 1000))
    hours, remainder = divmod(millis, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, ms = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON com {words:[{text,start,end}]}")
    parser.add_argument("output", type=Path, help="Arquivo .srt de saída")
    parser.add_argument("--max-words", type=int, choices=(1, 2), default=2)
    parser.add_argument("--max-gap", type=float, default=0.16, help="Gap máximo para agrupar palavras")
    parser.add_argument("--min-duration", type=float, default=0.12)
    args = parser.parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    words = payload.get("words")
    if not isinstance(words, list) or not words:
        raise SystemExit("O JSON precisa ter uma lista 'words' não vazia")

    normalized = []
    previous_end = -1.0
    for i, word in enumerate(words, 1):
        text = str(word.get("text", "")).strip()
        start = float(word["start"])
        end = float(word["end"])
        if not text or end <= start:
            raise SystemExit(f"Palavra {i} tem texto vazio ou timestamps inválidos")
        if start < previous_end - 0.01:
            raise SystemExit(f"Palavra {i} se sobrepõe à anterior; corrija o alinhamento")
        normalized.append({"text": text, "start": start, "end": end})
        previous_end = end

    groups = []
    current = []
    for word in normalized:
        if current:
            gap = word["start"] - current[-1]["end"]
            if len(current) >= args.max_words or gap > args.max_gap:
                groups.append(current)
                current = []
        current.append(word)
    if current:
        groups.append(current)

    lines = []
    for index, group in enumerate(groups, 1):
        start = group[0]["start"]
        end = max(group[-1]["end"], start + args.min_duration)
        text = " ".join(item["text"] for item in group)
        lines.extend([str(index), f"{stamp(start)} --> {stamp(end)}", text, ""])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Geradas {len(groups)} legendas em {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
