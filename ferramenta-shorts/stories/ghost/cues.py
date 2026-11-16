playful(F(0), F(106), 124); drone(F(106), F(275), 49); drone(F(196), F(343), 55)
march(F(343), F(639), 104); playful(F(639), F(823), 112); drone(F(823), F(1028), 52)
heartbeat(F(1028), F(1169), 84, 0.9); drone(F(1028), F(1169), 46); drone(F(1169), F(1389), 49)
march(F(1231), F(1389), 100); harp(F(1389), F(1578)); playful(F(1578), F(1692), 132); harp(F(1692), F(1792))
#--SFX--
def hiss(t0, t1, g=0.35):
    d = t1 - t0; x = hpf(lpf(noise(d), 6000), 1500); e = np.minimum(1, tt(d) / 0.15) * np.minimum(1, (d - tt(d)) / 0.3); place(sfx, (x * e).astype(np.float32), t0, g)
def engine(t0, t1, g=0.25, f=48):
    d = t1 - t0; x = tt(d); s = np.sin(2 * np.pi * f * x) + 0.6 * np.sin(2 * np.pi * f * 2.02 * x) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * x)); s = lpf(s.astype(np.float32), 400); place(sfx, s * np.minimum(1, x / 0.4) * np.minimum(1, (d - x) / 0.4), t0, g)
def blare(t, g=0.5):
    d = 0.6; x = tt(d); s = (np.sin(2 * np.pi * 220 * x) + 0.5 * np.sin(2 * np.pi * 330 * x) + 0.3 * np.sin(2 * np.pi * 440 * x)) * np.minimum(1, x / 0.03) * np.exp(-x * 3); place(sfx, s.astype(np.float32), t, g)
def pop(t, g=0.5): x = tt(0.2); place(sfx, (np.sin(2 * np.pi * np.cumsum(500 * np.exp(-x * 18) + 90) / SR) * np.exp(-x * 16)).astype(np.float32), t, g)
whoosh(F(0), 0.4, 0.4); ding(F(38), 0.5, 1175); whoosh(F(106), 0.5, 0.4); birds(F(0), F(106), 6, 0.08)
sting(F(199) - 0.2, 0.5); whoosh(F(196), 0.4, 0.35); whoosh(F(275), 0.4, 0.4)
whoosh(F(343), 0.4, 0.4); steps(F(343), F(446), 0.28, 0.22); ding(F(401), 0.6, 1568); whoosh(F(446), 0.4, 0.4)
steps(F(450), F(518), 0.3, 0.2); paper(F(530), 0.4); paper(F(560), 0.4); whoosh(F(518), 0.4, 0.4)
whoosh(F(592), 0.4, 0.4); pop(F(600), 0.5); whoosh(F(639), 0.4, 0.4)
engine(F(639), F(758), 0.2, 52); whoosh(F(706), 0.4, 0.4)
hiss(F(823), F(900), 0.4); [pop(F(905) + i * 0.1, 0.5) for i in range(3)]; ding(F(930), 0.6, 1320); whoosh(F(952), 0.4, 0.4)
thump(F(960), 0.4); [thump(F(965) + i * 0.4, 0.3) for i in range(6)]
blare(F(758), 0.5); blare(F(780), 0.4); engine(F(758), F(822), 0.15, 44)
engine(F(1028), F(1168), 0.28, 41); [blare(F(1032) + i * 0.7, 0.45) for i in range(8)]; steps(F(1028), F(1168), 0.26, 0.28)
whoosh(F(1169), 0.5, 0.4); sting(F(1180), 0.6); ding(F(1236), 0.5, 1047)
engine(F(1231), F(1300), 0.2, 50); steps(F(1231), F(1300), 0.27, 0.25)
sting(F(1305), 0.5); whoosh(F(1389), 0.5, 0.4); steps(F(1395), F(1458), 0.3, 0.25); sea(F(1389), F(1458), 0.2)
whoosh(F(1459), 0.5, 0.4); [ding(F(1465) + i * 0.4, 0.4, 880 * (1 + (i % 4) * 0.12)) for i in range(9)]
whoosh(F(1578), 0.5, 0.4); pop(F(1590), 0.4); hiss(F(1600), F(1640), 0.3); whoosh(F(1692), 0.5, 0.4)
ding(F(1716), 0.6, 988); sparkle = [ding(F(1745) + i * 0.08, 0.35, 1320 * (1 + i * 0.25)) for i in range(4)]; birds(F(1730), F(1792), 5, 0.07)
