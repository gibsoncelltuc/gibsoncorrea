_W = lambda i: _WORDS[min(i, len(_WORDS) - 1)]['s'] * 30   # frame da palavra i
_A = [0] + [int(_W(i) - 3) for i in [9, 19, 28]] + [FR]
playful(F(_A[0]), F(_A[4]), 122)
#--SFX--
whoosh(F(_A[0]), 0.4, 0.35)
birds(F(_A[0]), F(_A[1]), 6, 0.08)
ding(F(int(_W(0) - 2)), 0.5, 988)
whoosh(F(_A[1]), 0.4, 0.35)
birds(F(_A[1]), F(_A[2]), 6, 0.08)
ding(F(int(_W(9) - 2)), 0.5, 1175)
whoosh(F(_A[2]), 0.4, 0.35)
birds(F(_A[2]), F(_A[3]), 6, 0.08)
whoosh(F(_A[3]), 0.4, 0.35)
birds(F(_A[3]), F(_A[4]), 6, 0.08)
ding(F(int(_W(28) - 2)), 0.5, 1319)
