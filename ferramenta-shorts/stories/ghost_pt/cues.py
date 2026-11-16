playful(FE(0), FE(106), 124); drone(FE(106), FE(275), 49); drone(FE(196), FE(343), 55)
march(FE(343), FE(639), 104); playful(FE(639), FE(823), 112); drone(FE(823), FE(1028), 52)
heartbeat(FE(1028), FE(1169), 84, 0.9); drone(FE(1028), FE(1169), 46); drone(FE(1169), FE(1389), 49)
march(FE(1231), FE(1389), 100); harp(FE(1389), FE(1578)); playful(FE(1578), FE(1692), 132); harp(FE(1692), FE(1792))
#--SFX--
def hiss(t0, t1, g=0.35):
    d = t1 - t0; x = hpf(lpf(noise(d), 6000), 1500); e = np.minimum(1, tt(d) / 0.15) * np.minimum(1, (d - tt(d)) / 0.3); place(sfx, (x * e).astype(np.float32), t0, g)
def engine(t0, t1, g=0.25, f=48):
    d = t1 - t0; x = tt(d); s = np.sin(2 * np.pi * f * x) + 0.6 * np.sin(2 * np.pi * f * 2.02 * x) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * x)); s = lpf(s.astype(np.float32), 400); place(sfx, s * np.minimum(1, x / 0.4) * np.minimum(1, (d - x) / 0.4), t0, g)
def blare(t, g=0.5):
    d = 0.6; x = tt(d); s = (np.sin(2 * np.pi * 220 * x) + 0.5 * np.sin(2 * np.pi * 330 * x) + 0.3 * np.sin(2 * np.pi * 440 * x)) * np.minimum(1, x / 0.03) * np.exp(-x * 3); place(sfx, s.astype(np.float32), t, g)
def pop(t, g=0.5): x = tt(0.2); place(sfx, (np.sin(2 * np.pi * np.cumsum(500 * np.exp(-x * 18) + 90) / SR) * np.exp(-x * 16)).astype(np.float32), t, g)
whoosh(FE(0), 0.4, 0.4); ding(FE(38), 0.5, 1175); whoosh(FE(106), 0.5, 0.4); birds(FE(0), FE(106), 6, 0.08)
sting(FE(199) - 0.2, 0.5); whoosh(FE(196), 0.4, 0.35); whoosh(FE(275), 0.4, 0.4)
whoosh(FE(343), 0.4, 0.4); steps(FE(343), FE(446), 0.28, 0.22); ding(FE(401), 0.6, 1568); whoosh(FE(446), 0.4, 0.4)
steps(FE(450), FE(518), 0.3, 0.2); paper(FE(530), 0.4); paper(FE(560), 0.4); whoosh(FE(518), 0.4, 0.4)
whoosh(FE(592), 0.4, 0.4); pop(FE(600), 0.5); whoosh(FE(639), 0.4, 0.4)
engine(FE(639), FE(758), 0.2, 52); whoosh(FE(706), 0.4, 0.4)
hiss(FE(823), FE(900), 0.4); [pop(FE(905) + i * 0.1, 0.5) for i in range(3)]; ding(FE(930), 0.6, 1320); whoosh(FE(952), 0.4, 0.4)
thump(FE(960), 0.4); [thump(FE(965) + i * 0.4, 0.3) for i in range(6)]
blare(FE(758), 0.5); blare(FE(780), 0.4); engine(FE(758), FE(822), 0.15, 44)
engine(FE(1028), FE(1168), 0.28, 41); [blare(FE(1032) + i * 0.7, 0.45) for i in range(8)]; steps(FE(1028), FE(1168), 0.26, 0.28)
whoosh(FE(1169), 0.5, 0.4); sting(FE(1180), 0.6); ding(FE(1236), 0.5, 1047)
engine(FE(1231), FE(1300), 0.2, 50); steps(FE(1231), FE(1300), 0.27, 0.25)
sting(FE(1305), 0.5); whoosh(FE(1389), 0.5, 0.4); steps(FE(1395), FE(1458), 0.3, 0.25); sea(FE(1389), FE(1458), 0.2)
whoosh(FE(1459), 0.5, 0.4); [ding(FE(1465) + i * 0.4, 0.4, 880 * (1 + (i % 4) * 0.12)) for i in range(9)]
whoosh(FE(1578), 0.5, 0.4); pop(FE(1590), 0.4); hiss(FE(1600), FE(1640), 0.3); whoosh(FE(1692), 0.5, 0.4)
ding(FE(1716), 0.6, 988); sparkle = [ding(FE(1745) + i * 0.08, 0.35, 1320 * (1 + i * 0.25)) for i in range(4)]; birds(FE(1730), FE(1792), 5, 0.07)
