_W = lambda i: _WORDS[min(i, len(_WORDS) - 1)]['s'] * 30   # frame da palavra i
_A = [0] + [int(_W(i) - 3) for i in [5, 11, 18]] + [FR]
playful(F(_A[0]), F(_A[4]), 122)
#--SFX--
whoosh(F(_A[0]), 0.4, 0.35)
ding(F(int(_W(0) - 2)), 0.5, 988)
ding(F(_A[0] + 15))
whoosh(F(_A[1]), 0.4, 0.35)
ding(F(int(_W(5) - 2)), 0.5, 1175)
whoosh(F(_A[2]), 0.4, 0.35)
ding(F(int(_W(11) - 2)), 0.5, 880)
tick(F(_A[2] + 10))
tick(F(_A[2] + 40))
whoosh(F(_A[3]), 0.4, 0.35)
ding(F(int(_W(18) - 2)), 0.5, 1319)
gibber(F(_A[3] + int((_A[4] - _A[3]) * 0.2)), 4, 230, 0.12); gibber(F(_A[3] + int((_A[4] - _A[3]) * 0.58)), 4, 170, 0.12)
ding(F(_A[3] + 20))
sting(F(_A[3] + 30))
