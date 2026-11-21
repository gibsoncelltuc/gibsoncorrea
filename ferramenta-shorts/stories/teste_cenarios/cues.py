_W = lambda i: _WORDS[min(i, len(_WORDS) - 1)]['s'] * 30   # frame da palavra i
_A = [0] + [int(_W(i) - 3) for i in [10, 21, 32, 40]] + [FR]
playful(F(_A[0]), F(_A[5]), 122)
#--SFX--
whoosh(F(_A[0]), 0.4, 0.35)
gibber(F(_A[0] + int((_A[1] - _A[0]) * 0.2)), 4, 230, 0.12); gibber(F(_A[0] + int((_A[1] - _A[0]) * 0.58)), 4, 170, 0.12)
whoosh(F(_A[1]), 0.4, 0.35)
gibber(F(_A[1] + int((_A[2] - _A[1]) * 0.2)), 4, 200, 0.12); gibber(F(_A[1] + int((_A[2] - _A[1]) * 0.58)), 4, 290, 0.12)
whoosh(F(_A[2]), 0.4, 0.35)
whoosh(F(_A[3]), 0.4, 0.35)
gibber(F(_A[3] + int((_A[4] - _A[3]) * 0.2)), 4, 230, 0.12); gibber(F(_A[3] + int((_A[4] - _A[3]) * 0.58)), 4, 170, 0.12)
whoosh(F(_A[4]), 0.4, 0.35)
gibber(F(_A[4] + int((_A[5] - _A[4]) * 0.2)), 4, 200, 0.12); gibber(F(_A[4] + int((_A[5] - _A[4]) * 0.58)), 4, 290, 0.12)
sting(F(int(_W(9))))
tick(F(int(_W(37))))
