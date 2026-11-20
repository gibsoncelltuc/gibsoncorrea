playful(FE(0), FE(312), 118); march(FE(312), FE(446), 104); drone(FE(446), FE(502), 49); playful(FE(502), FE(742), 138)
playful(FE(742), FE(972), 150); drone(FE(972), FE(1134), 47); drone(FE(1134), FE(1195), 41); playful(FE(1195), FE(1333), 126)
march(FE(1333), FE(1449), 108); playful(FE(1449), FE(1525), 140); harp(FE(1525), FE(1752)); playful(FE(1752), FE(1867), 116)
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
whoosh(FE(0), 0.4, 0.4); birds(FE(0), FE(500), 12, 0.09); ding(FE(38), 0.5, 1175); whoosh(FE(45), 0.4, 0.4); sting(FE(80), 0.55); ding(FE(96), 0.5, 988)
whoosh(FE(121), 0.5, 0.4); [hoot(FE(150) + i * 0.9, 0.3) for i in range(8)]; whoosh(FE(237), 0.4, 0.35); sting(FE(250), 0.4)
whoosh(FE(312), 0.4, 0.4); steps(FE(312), FE(445), 0.28, 0.24); ding(FE(358), 0.5, 880); ding(FE(393), 0.5, 1047)
hoot(FE(446), 0.45); hoot(FE(470), 0.4); whoosh(FE(502), 0.5, 0.45); steps(FE(502), FE(593), 0.14, 0.3)
mg(FE(640), 14, 0.5); mg(FE(700), 14, 0.5); steps(FE(600), FE(740), 0.12, 0.25); [hoot(FE(620) + i * 0.7, 0.3) for i in range(6)]
whoosh(FE(742), 0.5, 0.4); engine(FE(742), FE(971), 0.28, 46); mg(FE(770), 12, 0.35); mg(FE(830), 12, 0.35); [boom(FE(850) + i * 0.38, 0.25) for i in range(10)]
sting(FE(972), 0.5); [mg(FE(1000) + i * 1.1, 8, 0.3) for i in range(4)]; ding(FE(1040), 0.4, 740)
whoosh(FE(1134), 0.4, 0.4); engine(FE(1134), FE(1194), 0.2, 40); laugh(FE(1210), FE(1330), 0.35); whoosh(FE(1195), 0.4, 0.4)
whoosh(FE(1333), 0.4, 0.4); mg(FE(1380), 10, 0.4); mg(FE(1400), 8, 0.4); steps(FE(1449), FE(1524), 0.13, 0.3); sting(FE(1470), 0.55)
whoosh(FE(1525), 0.4, 0.4); [ding(FE(1555) + i * 0.25, 0.4, 1568 + 100 * (i % 3)) for i in range(5)]
whoosh(FE(1629), 0.5, 0.4); thump(FE(1665), 0.5); whoosh(FE(1752), 0.4, 0.4); ding(FE(1760), 0.6, 880); ding(FE(1816), 0.6, 1320); hoot(FE(1832), 0.5)
sparkle = [ding(FE(1835) + i * 0.08, 0.35, 1320 * (1 + i * 0.25)) for i in range(4)]; birds(FE(1780), FE(1867), 5, 0.07)
