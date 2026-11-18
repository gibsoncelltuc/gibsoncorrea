#!/usr/bin/env python3
"""As 10 canções originais de 60 s (estudo de bastidores). Uso: musicas_virais.py <n 1..10> <seed> <saida.json>
Aplica os padrões do estudo: gancho na batida 1, refrão curto repetido, pergunta e resposta, gesto, mudança de tom no último refrão."""
import json, sys

BASE_CAPTION = ("Cheerful Brazilian children's pop song, extremely catchy singalong earworm, warm friendly adult male lead vocal with a kids choir "
                "answering the hook, bright and playful, clean polished mix, the hook starts right on the first beat with no intro, every section lasts exactly 4 bars, "
                "short repeated chorus, simple melody in small steps, call and response with the kids choir, the last chorus goes up by a whole step (key change), "
                "clear Portuguese pronunciation of every word")


def S(chorus, v1, v2, bridge, extra=False):
    secs = [("Chorus", chorus), ("Verse 1", v1), ("Chorus", chorus), ("Verse 2", v2), ("Bridge", bridge), ("Chorus", chorus)]
    if extra:
        secs.append(("Final Chorus", chorus))
    return "\n\n".join(f"[{t}]\n{x.strip()}" for t, x in secs)


SONGS = {
 1: dict(titulo="Pé, Pé, Bate o Pezinho!", slug="pe-pe-bate-o-pezinho", bpm=112, key="C major",
         inst="bouncy ukulele strums, stomping foot percussion, hand claps on every beat, bright glockenspiel, round bass",
         lyr=S("""Pé, pé, bate o pezinho!
Pá, pá, bate a mãozinha!
Gira, gira, devagarinho,
e dança, dança, dança com a gente!""",
               """Um pé aqui, outro pé ali,
palminha pra lá, palminha pra cá,
quem tá dançando vai sorrir,
vem, vem, vem, vem brincar!""",
               """Bate o pé bem devagar,
bate o pé bem depressa,
bate, bate, bate, bate,
agora parou e respira!""",
               """Pé, pé, pá, pá!
Pé, pé, pá, pá!
Pé, pé, pá, pá!
Todo mundo junto, vai!""", True)),
 2: dict(titulo="Quem Faz Assim?", slug="quem-faz-assim", bpm=100, key="G major",
         inst="playful acoustic guitar, hand claps, shaker, xylophone, light bass, animal sound-like vocal ad-libs",
         lyr=S("""Quem faz assim? Miau, miau!
Quem faz assim? Au, au, au!
Quem faz assim? Muuu, muuu!
Adivinha, adivinha, quem é?""",
               """O gatinho faz miau, miau,
o cachorrinho faz au, au, au,
a vaquinha faz muuu, muuu,
e o patinho faz quá, quá, quá!""",
               """O pintinho faz piu, piu,
o sapinho faz ploc, ploc,
o porquinho faz oinc, oinc,
e o leãozinho faz grrr, grrr!""",
               """Piu, piu, miau, miau,
au, au, muuu, muuu,
quá, quá, ploc, ploc,
que festa de bichinhos!""")),
 3: dict(titulo="Cores do Arco-Íris", slug="cores-do-arco-iris", bpm=104, key="C major",
         inst="bright marimba, plucked guitar, soft hand claps, glockenspiel melody, warm bass",
         lyr=S("""Vermelho, laranja, amarelo e verde,
azul, anil, violeta,
arco-íris, arco-íris,
pintando o céu de alegria!""",
               """Vermelho é a maçã,
laranja é a laranja,
amarelo é o sol,
verde é a folhinha!""",
               """Azul é o céu,
anil é a noite,
violeta é a uva,
e o arco-íris tem todas!""",
               """Vermelho, laranja, amarelo,
verde, azul, violeta,
olha só quanta cor,
todo mundo canta junto!""")),
 4: dict(titulo="Abraça, Abraça, Abraça!", slug="abraca-abraca-abraca", bpm=108, key="F major",
         inst="warm acoustic guitar, soft piano chords, hand claps, light shaker, gentle bass, kids choir",
         lyr=S("""Abraça, abraça, abraça quem tá perto!
Um abraço apertado deixa o dia mais esperto!
Abraça, abraça, abraça de verdade,
abraço é amizade, abraço é felicidade!""",
               """Abraça a mamãe, abraça o papai,
abraça a vovó, e o vovô também,
abraça o amiguinho, abraça o irmãozinho,
quem abraça vai sorrir!""",
               """Um abraço de urso, bem forte e bem quentinho,
um abraço de coala, bem devagarinho,
um abraço de polvo, com muitos bracinhos,
abraça, abraça, abraça!""",
               """Um, dois, três, abraço!
Um, dois, três, abraço!
Um, dois, três, abraço!
Todo mundo abraça!""", True)),
 5: dict(titulo="Pop-Pop, Banho de Bolhas!", slug="pop-pop-banho-de-bolhas", bpm=120, key="G major",
         inst="bubbly synth plucks, popping percussion sounds, ukulele, hand claps, bouncy bass, sparkly glockenspiel",
         lyr=S("""Pop, pop, pop, as bolhinhas vão estourar!
Pop, pop, pop, é hora de se ensaboar!
Esfrega o bracinho, esfrega o pezinho,
pop, pop, pop, fico limpinho!""",
               """Sabonete na mão, cheirinho de flor,
espuma na cabeça, que coisa de amor,
esfrega a barriguinha, esfrega as orelhinhas,
pop, pop, pop, bolhinhas!""",
               """Água morninha, que gostosa que é,
enxágua o corpinho, da cabeça ao pé,
pop, pop, pop, quanta espuma,
tchau, tchau, sujeirinha!""",
               """Pop, pop, pop, pop, pop!
Pop, pop, pop, pop, pop!
Bolhinha pra lá, bolhinha pra cá,
pop!""", True)),
 6: dict(titulo="Ma-Ma, Pa-Pa!", slug="ma-ma-pa-pa", bpm=100, key="C major",
         inst="gentle music-box and glockenspiel, soft ukulele, light hand claps, warm bass, tender and happy baby-friendly feel",
         lyr=S("""Ma-ma, pa-pa, ma-ma, pa-pa!
A primeira palavrinha é de amor, tá?
Ma-ma, pa-pa, ma-ma, pa-pa!
O bebê já sabe chamar!""",
               """Quem é que me abraça? Ma-ma!
Quem é que me cuida? Pa-pa!
Quem me dá sorriso? Ma-ma!
Quem brinca comigo? Pa-pa!""",
               """Eu tento falar, eu tento falar,
ma-ma, pa-pa, eu sei falar!
A mamãe aplaude, o papai também,
ma-ma, pa-pa, que alegria!""",
               """Ma-ma! Pa-pa! Ma-ma! Pa-pa!
Ma-ma! Pa-pa! Ma-ma! Pa-pa!
Eu te amo, mamãe!
Eu te amo, papai!""")),
 7: dict(titulo="Bom Dia, Sol!", slug="bom-dia-sol", bpm=112, key="D major",
         inst="sunny acoustic guitar strums, hand claps, bright glockenspiel, whistle-like synth, upbeat bass, morning energy",
         lyr=S("""Bom dia, sol, bom dia, céu!
Eu acordei, que lindo é o dia!
Estica, estica, estica o corpinho,
bom dia, sol, bom dia!""",
               """Os braços pra cima, bem alto, bem alto,
depois pra baixo, bem baixinho,
gira a cabecinha, devagarinho,
e dá um grande sorriso!""",
               """Escovo os dentinhos, lavo o rostinho,
visto a roupinha, calço o tênis,
tomo o café da manhã,
e vou brincar no jardim!""",
               """Sol, sol, sol, sol!
Bom dia, bom dia!
Sol, sol, sol, sol!
Bom dia, bom dia!""", True)),
 8: dict(titulo="Só Mais Cinco Minutinhos!", slug="so-mais-cinco-minutinhos", bpm=120, key="F major",
         inst="funny bouncy bass, playful ukulele, hand claps, quirky xylophone, comedic call and response, kids choir shouting the hook",
         lyr=S("""Só mais cinco minutinhos, só mais um, só mais um!
Já é hora de dormir? Ah, não, não, não!
Só mais cinco minutinhos, só mais um, só mais um!
Tá bom, tá bom, tá bom, eu vou!""",
               """Escovei os dentes, vesti o pijama,
quero só mais uma historinha,
quero só mais um copo d'água,
quero só mais um abraço!""",
               """A mamãe disse: já chega, filhinho,
o papai disse: é hora, amiguinho,
a lua já brilha, o sono já vem,
eu bocejo, aaaah!""",
               """Cinco, quatro, três, dois, um...
Shhh... boa noite!
Cinco, quatro, três, dois, um...
Shhh... boa noite!""", True)),
 9: dict(titulo="Shhh, Boa Noite, Estrelinha", slug="shhh-boa-noite-estrelinha", bpm=96, key="G major",
         inst="soft music box, gentle acoustic guitar, warm pad, very soft hand percussion, slow lullaby feel, soothing whispered shh sounds, calm kids choir",
         lyr=S("""Shhh, shhh, boa noite, estrelinha,
shhh, shhh, a lua está chegando,
fecha o olhinho, respira devagarinho,
shhh, shhh, bons sonhos, meu bebê.""",
               """As estrelas piscam, lá no céu azul,
a lua balança, ninando o mundo,
o ursinho abraçado, a coberta quentinha,
shhh, shhh, que sono bom.""",
               """Os sonhos vão chegando, bem de mansinho,
com nuvens macias e estrelinhas,
a noite é de paz, a noite é de amor,
shhh, shhh, durma bem.""",
               """Lá, lá, lá, lá,
boa noite, boa noite,
lá, lá, lá, lá,
dorme, estrelinha.""")),
 10: dict(titulo="Tchu-Tchu, Trenzinho!", slug="tchu-tchu-trenzinho", bpm=108, key="C major",
          inst="chugging train rhythm with shaker and snare brushes, ukulele, whistle sounds, hand claps, bouncy bass, glockenspiel",
          lyr=S("""Tchu-tchu, lá vem o trenzinho!
Piiii! Apita pra todo mundo ir!
Tchu-tchu, vagãozinho por vagãozinho,
todo mundo a bordo, vamos sorrir!""",
                """O primeiro vagão é vermelho,
o segundo vagão é azul,
o terceiro vagão é amarelo,
e o quarto é verde também!""",
                """O trenzinho passa na ponte,
o trenzinho passa no túnel,
o trenzinho sobe a montanha,
e desce com muita alegria!""",
                """Tchu, tchu, tchu, tchu!
Piiii! Piiii!
Tchu, tchu, tchu, tchu!
Chegamos, chegamos!""", True)),
}


def build(n, seed):
    s = SONGS[n]
    return {"lm_model": "acestep-5Hz-lm-1.7B-Q8_0.gguf", "synth_model": "acestep-v15-turbo-Q8_0.gguf",
            "caption": f"{BASE_CAPTION}, {s['inst']}", "lyrics": s["lyr"], "duration": 60, "bpm": s["bpm"],
            "vocal_language": "pt", "keyscale": s["key"], "timesignature": "4", "inference_steps": 8,
            "guidance_scale": 1.0, "shift": 3.0, "seed": seed}


if __name__ == "__main__":
    json.dump(build(int(sys.argv[1]), int(sys.argv[2])), open(sys.argv[3], "w"), ensure_ascii=False, indent=2)
