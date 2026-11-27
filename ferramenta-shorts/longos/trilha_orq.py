# TRILHA ORQUESTRAL composta por codigo (MIDI -> FluidSynth + FluidR3_GM, sons livres): cordas, contrabaixo, trompas,
# coral, timpanos e taiko; "impactos" (golpe de timpano + prato + metais) nos tempos pedidos; crescendo nos ultimos blocos.
# gerar(wav, total_s, impactos=[t...], blocos=[t...], humor='epico'|'misterio', bpm=92)
import mido, subprocess, os, random
SF = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
def gerar(wav, total, impactos=(), blocos=(), humor='epico', bpm=92):
    random.seed(4); mid = mido.MidiFile(ticks_per_beat=480); tpb = 480; spb = 60 / bpm
    def tk(s): return int(s / spb * tpb)
    ev = []   # (tick, msg)
    def nota(ch, n, t0, dur, vel):
        ev.append((tk(t0), mido.Message('note_on', channel=ch, note=n, velocity=max(1, min(127, int(vel))))))
        ev.append((tk(t0 + dur), mido.Message('note_off', channel=ch, note=n, velocity=0)))
    progs = {0: 48, 1: 43, 2: 60, 3: 52, 4: 47, 5: 116, 6: 49, 7: 57}   # cordas, contrabaixo, trompa, coral, timpano, taiko, cordas2, trombone
    for ch, p in progs.items(): ev.append((0, mido.Message('program_change', channel=ch, program=p)))
    ev.append((0, mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm))))
    if humor == 'misterio': prog = [(45, [57, 60, 64]), (41, [57, 60, 65]), (43, [55, 59, 62]), (40, [55, 59, 64])]   # Am F G Em
    else: prog = [(38, [57, 62, 65]), (34, [58, 62, 65]), (41, [57, 60, 65]), (36, [55, 60, 64])]                     # Dm Bb F C (epico)
    compasso = 4 * spb * 2; t = 0.0; i = 0
    while t < total:
        intens = min(1, .45 + .55 * t / max(1, total))   # cresce ao longo do video
        baixo, acorde = prog[i % 4]
        nota(1, baixo, t, compasso * .98, 70 + 30 * intens)                                       # contrabaixo
        for n in acorde: nota(0, n, t, compasso * .98, 45 + 40 * intens); nota(6, n + 12, t, compasso * .98, 30 + 35 * intens)   # cordas
        if intens > .55:
            for n in acorde[:2]: nota(3, n, t, compasso * .98, 30 + 40 * intens)                    # coral
        # ostinato ritmico das cordas graves (pulso de trailer)
        for k in range(16): nota(1, baixo + 12, t + k * spb / 2, spb * .4, (55 if k % 4 else 80) * intens)
        # taiko a cada tempo forte quando o video esquenta
        if intens > .5:
            for k in range(0, 8, 2): nota(5, 60, t + k * spb, spb * .5, 70 + 40 * intens)
        # trompas: tema heroico a cada 2 compassos
        if i % 2 == 0: 
            for k, n in enumerate([acorde[0] - 12 + 12, acorde[1], acorde[2], acorde[1]]): nota(2, n, t + k * spb * 2, spb * 1.9, 55 + 45 * intens)
        t += compasso; i += 1
    for tb in blocos: nota(4, 41, tb, spb, 100); nota(5, 60, tb, spb, 110)                              # timpano na entrada de cada bloco
    for ti in impactos:                                                                                    # IMPACTO: timpano + prato + metais
        for k, dt in enumerate((0, .12, .24)): nota(4, 38 + k * 3, ti + dt, spb, 127)
        ev.append((tk(ti), mido.Message('note_on', channel=9, note=49, velocity=120))); ev.append((tk(ti + 2), mido.Message('note_off', channel=9, note=49, velocity=0)))
        for n in (50, 57, 62): nota(7, n, ti, spb * 2, 118); nota(2, n + 12, ti, spb * 2, 110)
    tr = mido.MidiTrack(); mid.tracks.append(tr); ev.sort(key=lambda e: (e[0], 0 if e[1].type == 'note_off' else 1)); last = 0
    for tick, msg in ev: msg.time = tick - last; last = tick; tr.append(msg)
    mf = wav[:-4] + '.mid'; mid.save(mf)
    subprocess.run(['fluidsynth', '-ni', '-g', '0.9', '-r', '48000', '-F', wav, SF, mf], check=True, capture_output=True)
    return wav
