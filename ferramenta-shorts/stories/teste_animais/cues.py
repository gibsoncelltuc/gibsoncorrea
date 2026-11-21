_W = lambda i: _WORDS[min(i, len(_WORDS) - 1)]['s'] * 30   # frame da palavra i
_A = [0] + [int(_W(i) - 3) for i in [15, 26, 39]] + [FR]
playful(F(_A[0]), F(_A[4]), 122)
#--SFX--
whoosh(F(_A[0]), 0.4, 0.35)
birds(F(_A[0]), F(_A[1]), 6, 0.08)
whoosh(F(_A[1]), 0.4, 0.35)
birds(F(_A[1]), F(_A[2]), 6, 0.08)
whoosh(F(_A[2]), 0.4, 0.35)
birds(F(_A[2]), F(_A[3]), 6, 0.08)
whoosh(F(_A[3]), 0.4, 0.35)
birds(F(_A[3]), F(_A[4]), 6, 0.08)
thump(F(int(_W(23))))
thump(F(int(_W(30))))
gun(F(int(_W(40))))
thump(F(int(_W(44))))
gun(F(int(_W(40))))
thump(F(int(_W(46))))
