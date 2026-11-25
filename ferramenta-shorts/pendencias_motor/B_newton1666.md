# B newton1666 - FERRAMENTA
- A palavra "maçã" vira "maca" na normalizacao (_nz) e casa com `\bmaca\b` (ferramenta de hospital, mkvideo.py linha ~164): as cenas que falam de maçã (b0, b9) ganham interior "hospital" + 3 macas (kit/maca) em volta. Qualquer roteiro com "maçã" sofre o mesmo.
- Correcao sugerida: no regex usar a palavra com acento original ou excluir "maca" quando a frase tem "maçã" (comparar antes da normalizacao).
- Contorno no roteiro: "set": "loc_campo" nas cenas b0 e b9 e "moveis": [] para tirar as macas.
