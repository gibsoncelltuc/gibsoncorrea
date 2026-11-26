_W = lambda i: _WORDS[min(i, len(_WORDS) - 1)]['s'] * 30   # frame da palavra i
_A = [0] + [int(_W(i) - 3) for i in [10, 21, 32, 40]] + [FR]
playful(F(_A[0]), F(_A[5]), 122)
#--SFX--
whoosh(F(_A[0]), 0.4, 0.35)
whoosh(F(_A[1]), 0.4, 0.35)
whoosh(F(_A[2]), 0.4, 0.35)
whoosh(F(_A[3]), 0.4, 0.35)
whoosh(F(_A[4]), 0.4, 0.35)
