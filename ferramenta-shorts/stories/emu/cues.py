playful(F(0), F(312), 118); march(F(312), F(446), 104); drone(F(446), F(502), 49); playful(F(502), F(742), 138)
playful(F(742), F(972), 150); drone(F(972), F(1134), 47); drone(F(1134), F(1195), 41); playful(F(1195), F(1333), 126)
march(F(1333), F(1449), 108); playful(F(1449), F(1525), 140); harp(F(1525), F(1752)); playful(F(1752), F(1867), 116)
#--SFX--
def engine(t0, t1, g=0.25, f=48):
    d = t1 - t0; x = tt(d); s = np.sin(2 * np.pi * f * x) + 0.6 * np.sin(2 * np.pi * f * 2.02 * x) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * x)); s = lpf(s.astype(np.float32), 400); place(sfx, s * np.minimum(1, x / 0.4) * np.minimum(1, (d - x) / 0.4), t0, g)
def boom(t, g=0.5):
    d = 0.5; x = tt(d); s = np.sin(2 * np.pi * np.cumsum(120 * np.exp(-x * 6) + 55) / SR) * np.exp(-x * 6) * (1 + 0.2 * np.sin(2 * np.pi * 30 * x)); place(sfx, s.astype(np.float32), t, g)
def mg(t, n=10, g=0.5):
    for i in range(n): d = 0.12; x = tt(d); s = lpf(noise(d), 3500) * np.exp(-x * 45) + np.sin(2 * np.pi * 90 * x) * np.exp(-x * 30); place(sfx, s.astype(np.float32), t + i * 0.075, g)
def hoot(t, g=0.4):
    d = 0.35; x = tt(d); fr = 160 + 40 * np.sin(2 * np.pi * 12 * x); s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.minimum(1, x / 0.02) * np.exp(-x * 5); place(sfx, lpf(s.astype(np.float32), 600), t, g)
def laugh(t0, t1, g=0.3):
    t = t0; k = 0
    while t < t1: d = 0.13; x = tt(d); s = np.sin(2 * np.pi * np.cumsum(260 + 60 * (k % 3)) / SR if False else 2 * np.pi * (250 + 50 * (k % 3)) * x) * np.exp(-x * 14); place(sfx, s.astype(np.float32), t, g); t += 0.2; k += 1
whoosh(F(0), 0.4, 0.4); birds(F(0), F(500), 12, 0.09); ding(F(38), 0.5, 1175); whoosh(F(45), 0.4, 0.4); sting(F(80), 0.55); ding(F(96), 0.5, 988)
whoosh(F(121), 0.5, 0.4); [hoot(F(150) + i * 0.9, 0.3) for i in range(8)]; whoosh(F(237), 0.4, 0.35); sting(F(250), 0.4)
whoosh(F(312), 0.4, 0.4); steps(F(312), F(445), 0.28, 0.24); ding(F(358), 0.5, 880); ding(F(393), 0.5, 1047)
hoot(F(446), 0.45); hoot(F(470), 0.4); whoosh(F(502), 0.5, 0.45); steps(F(502), F(593), 0.14, 0.3)
mg(F(640), 14, 0.5); mg(F(700), 14, 0.5); steps(F(600), F(740), 0.12, 0.25); [hoot(F(620) + i * 0.7, 0.3) for i in range(6)]
whoosh(F(742), 0.5, 0.4); engine(F(742), F(971), 0.28, 46); mg(F(770), 12, 0.35); mg(F(830), 12, 0.35); [boom(F(850) + i * 0.38, 0.25) for i in range(10)]
sting(F(972), 0.5); [mg(F(1000) + i * 1.1, 8, 0.3) for i in range(4)]; ding(F(1040), 0.4, 740)
whoosh(F(1134), 0.4, 0.4); engine(F(1134), F(1194), 0.2, 40); laugh(F(1210), F(1330), 0.35); whoosh(F(1195), 0.4, 0.4)
whoosh(F(1333), 0.4, 0.4); mg(F(1380), 10, 0.4); mg(F(1400), 8, 0.4); steps(F(1449), F(1524), 0.13, 0.3); sting(F(1470), 0.55)
whoosh(F(1525), 0.4, 0.4); [ding(F(1555) + i * 0.25, 0.4, 1568 + 100 * (i % 3)) for i in range(5)]
whoosh(F(1629), 0.5, 0.4); thump(F(1665), 0.5); whoosh(F(1752), 0.4, 0.4); ding(F(1760), 0.6, 880); ding(F(1816), 0.6, 1320); hoot(F(1832), 0.5)
sparkle = [ding(F(1835) + i * 0.08, 0.35, 1320 * (1 + i * 0.25)) for i in range(4)]; birds(F(1780), F(1867), 5, 0.07)
