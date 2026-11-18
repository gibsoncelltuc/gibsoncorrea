_W = lambda i: _WORDS[min(i, len(_WORDS) - 1)]['s'] * 30   # frame da palavra i
_A = [0] + [int(_W(i) - 3) for i in [16, 32, 49, 65, 79]] + [FR]
playful(F(_A[0]), F(_A[6]), 122)
#--SFX--
whoosh(F(_A[0]), 0.4, 0.35)
gibber(F(_A[0] + int((_A[1] - _A[0]) * 0.2)), 4, 230, 0.12); gibber(F(_A[0] + int((_A[1] - _A[0]) * 0.58)), 4, 170, 0.12)
whoosh(F(_A[1]), 0.4, 0.35)
gibber(F(_A[1] + int((_A[2] - _A[1]) * 0.2)), 4, 200, 0.12); gibber(F(_A[1] + int((_A[2] - _A[1]) * 0.58)), 4, 290, 0.12)
whoosh(F(_A[2]), 0.4, 0.35)
gibber(F(_A[2] + int((_A[3] - _A[2]) * 0.25)), 5, 330, 0.1); gibber(F(_A[2] + int((_A[3] - _A[2]) * 0.6)), 5, 300, 0.1)
whoosh(F(_A[3]), 0.4, 0.35)
ding(F(int(_W(49) - 2)), 0.5, 1319)
gibber(F(_A[3] + int((_A[4] - _A[3]) * 0.2)), 4, 230, 0.12); gibber(F(_A[3] + int((_A[4] - _A[3]) * 0.58)), 4, 170, 0.12)
sting(F(_A[3] + 5))
whoosh(F(_A[4]), 0.4, 0.35)
whoosh(F(_A[5]), 0.4, 0.35)
gibber(F(_A[5] + int((_A[6] - _A[5]) * 0.2)), 4, 260, 0.12); gibber(F(_A[5] + int((_A[6] - _A[5]) * 0.58)), 4, 185, 0.12)
ding(F(int(_W(41))))
