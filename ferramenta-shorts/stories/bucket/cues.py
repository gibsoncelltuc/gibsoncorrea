playful(F(0), F(137), 112); drone(F(137), F(311), 49); march(F(311), F(697), 108); playful(F(697), F(926), 148); march(F(926), F(1084), 104); harp(F(1084), F(1244)); drone(F(1244), F(1312), 44); playful(F(1312), F(1418), 120)
#--SFX--
def clang(t, g=0.5):
    x = tt(0.6); place(sfx, ((np.sin(2 * np.pi * 1800 * x) + 0.6 * np.sin(2 * np.pi * 2750 * x) + 0.3 * np.sin(2 * np.pi * 4100 * x)) * np.exp(-x * 8)).astype(np.float32), t, g)
def hooves(t0, t1, g=0.35):
    t = t0
    while t < t1: place(sfx, (lpf(noise(0.06), 700) * np.exp(-tt(0.06) * 50)).astype(np.float32), t, g); place(sfx, (lpf(noise(0.06), 700) * np.exp(-tt(0.06) * 50)).astype(np.float32), t + 0.09, g * 0.7); t += 0.22
def horn(t, d=0.8, g=0.4):
    x = tt(d); s = (np.sin(2 * np.pi * 330 * x) + 0.5 * np.sin(2 * np.pi * 495 * x)) * np.minimum(1, x / 0.05) * np.minimum(1, (d - x) / 0.2); place(sfx, s.astype(np.float32), t, g)
def clunk(t, g=0.5): x = tt(0.3); place(sfx, ((np.sin(2 * np.pi * 220 * x) + lpf(noise(0.3), 1200) * 0.6) * np.exp(-x * 12)).astype(np.float32), t, g)
whoosh(F(0), 0.4, 0.4); ding(F(6), 0.5, 988); whoosh(F(46), 0.4, 0.4); ding(F(60), 0.5, 740); steps(F(137), F(225), 0.45, 0.2); sting(F(226), 0.5); clunk(F(250), 0.5)
whoosh(F(311), 0.4, 0.4); sting(F(320), 0.4); ding(F(407), 0.6, 523); whoosh(F(467), 0.4, 0.4); steps(F(467), F(575), 0.3, 0.3); horn(F(467), 0.8, 0.4)
horn(F(576), 1.0, 0.45); whoosh(F(649), 0.4, 0.35); horn(F(697) - 0.3, 0.8, 0.5); hooves(F(697), F(796), 0.4); [clang(F(740) + i * 0.3, 0.45) for i in range(8)]
whoosh(F(797), 0.4, 0.4); steps(F(797), F(880), 0.18, 0.3); ding(F(822), 0.6, 1175); steps(F(926), F(1002), 0.3, 0.3); horn(F(926), 0.8, 0.4); ding(F(1003), 0.5, 988)
whoosh(F(1084), 0.4, 0.4); ding(F(1123), 0.5, 1175); whoosh(F(1172), 0.4, 0.4); sting(F(1180), 0.4); whoosh(F(1244), 0.4, 0.4); sting(F(1250), 0.5)
whoosh(F(1312), 0.4, 0.4); ding(F(1375), 0.7, 880); clunk(F(1380), 0.5); sparkle = [ding(F(1390) + i * 0.08, 0.35, 1320 * (1 + i * 0.25)) for i in range(4)]
