_W = lambda i: _WORDS[min(i, len(_WORDS) - 1)]['s'] * 30   # frame da palavra i
_A = [0] + [int(_W(i) - 3) for i in [8, 14, 22, 31, 40]] + [FR]
playful(F(_A[0]), F(_A[6]), 122)
#--SFX--
whoosh(F(_A[0]), 0.4, 0.35)
birds(F(_A[0]), F(_A[1]), 6, 0.08)
steps(F(_A[0]), F(_A[1]), 0.12, 0.3)
whoosh(F(_A[1]), 0.4, 0.35)
birds(F(_A[1]), F(_A[2]), 6, 0.08)
whoosh(F(_A[2]), 0.4, 0.35)
birds(F(_A[2]), F(_A[3]), 6, 0.08)
whoosh(F(_A[3]), 0.4, 0.35)
birds(F(_A[3]), F(_A[4]), 6, 0.08)
whoosh(F(_A[4]), 0.4, 0.35)
birds(F(_A[4]), F(_A[5]), 6, 0.08)
whoosh(F(_A[5]), 0.4, 0.35)
birds(F(_A[5]), F(_A[6]), 6, 0.08)
