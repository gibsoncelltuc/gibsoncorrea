playful(FE(0), FE(137), 112); drone(FE(137), FE(311), 49); march(FE(311), FE(697), 108); playful(FE(697), FE(926), 148); march(FE(926), FE(1084), 104); harp(FE(1084), FE(1244)); drone(FE(1244), FE(1312), 44); playful(FE(1312), FE(1418), 120)
#--SFX--
def clang(t, g=0.5):
    x = tt(0.6); place(sfx, ((np.sin(2 * np.pi * 1800 * x) + 0.6 * np.sin(2 * np.pi * 2750 * x) + 0.3 * np.sin(2 * np.pi * 4100 * x)) * np.exp(-x * 8)).astype(np.float32), t, g)
def hooves(t0, t1, g=0.35):
    t = t0
    while t < t1: place(sfx, (lpf(noise(0.06), 700) * np.exp(-tt(0.06) * 50)).astype(np.float32), t, g); place(sfx, (lpf(noise(0.06), 700) * np.exp(-tt(0.06) * 50)).astype(np.float32), t + 0.09, g * 0.7); t += 0.22
def horn(t, d=0.8, g=0.4):
    x = tt(d); s = (np.sin(2 * np.pi * 330 * x) + 0.5 * np.sin(2 * np.pi * 495 * x)) * np.minimum(1, x / 0.05) * np.minimum(1, (d - x) / 0.2); place(sfx, s.astype(np.float32), t, g)
def clunk(t, g=0.5): x = tt(0.3); place(sfx, ((np.sin(2 * np.pi * 220 * x) + lpf(noise(0.3), 1200) * 0.6) * np.exp(-x * 12)).astype(np.float32), t, g)
whoosh(FE(0), 0.4, 0.4); ding(FE(6), 0.5, 988); whoosh(FE(46), 0.4, 0.4); ding(FE(60), 0.5, 740); steps(FE(137), FE(225), 0.45, 0.2); sting(FE(226), 0.5); clunk(FE(250), 0.5)
whoosh(FE(311), 0.4, 0.4); sting(FE(320), 0.4); ding(FE(407), 0.6, 523); whoosh(FE(467), 0.4, 0.4); steps(FE(467), FE(575), 0.3, 0.3); horn(FE(467), 0.8, 0.4)
horn(FE(576), 1.0, 0.45); whoosh(FE(649), 0.4, 0.35); horn(FE(697) - 0.3, 0.8, 0.5); hooves(FE(697), FE(796), 0.4); [clang(FE(740) + i * 0.3, 0.45) for i in range(8)]
whoosh(FE(797), 0.4, 0.4); steps(FE(797), FE(880), 0.18, 0.3); ding(FE(822), 0.6, 1175); steps(FE(926), FE(1002), 0.3, 0.3); horn(FE(926), 0.8, 0.4); ding(FE(1003), 0.5, 988)
whoosh(FE(1084), 0.4, 0.4); ding(FE(1123), 0.5, 1175); whoosh(FE(1172), 0.4, 0.4); sting(FE(1180), 0.4); whoosh(FE(1244), 0.4, 0.4); sting(FE(1250), 0.5)
whoosh(FE(1312), 0.4, 0.4); ding(FE(1375), 0.7, 880); clunk(FE(1380), 0.5); sparkle = [ding(FE(1390) + i * 0.08, 0.35, 1320 * (1 + i * 0.25)) for i in range(4)]
