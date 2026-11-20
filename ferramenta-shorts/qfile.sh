#!/usr/bin/env bash
# Qual fila esta maquina le (pelo branch): sessao A -> fila_sessao_A.txt | sessao B -> fila_sessao_B.txt | principal -> queue.txt
cd "$(dirname "$0")"
case "$(git -C .. rev-parse --abbrev-ref HEAD 2>/dev/null)" in
  *prod-a*) echo fila_sessao_A.txt;; *prod-b*) echo fila_sessao_B.txt;; *) echo queue.txt;; esac
