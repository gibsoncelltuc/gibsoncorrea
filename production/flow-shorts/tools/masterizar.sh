#!/usr/bin/env bash
# Acabamento: normaliza volume para -14 LUFS (padrão YouTube) com pico máximo -1,5 dB, mp3 320k. Uso: masterizar.sh entrada.mp3 saida.mp3
ffmpeg -y -loglevel error -i "$1" -af "loudnorm=I=-14:TP=-1.5:LRA=7" -ar 44100 -b:a 320k "$2"
