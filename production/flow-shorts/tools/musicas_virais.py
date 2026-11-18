#!/usr/bin/env python3
"""As 10 canções originais de 60 s (estudo de bastidores). Uso: musicas_virais.py <n 1..10> <seed> <saida.json>
Aplica os padrões do estudo: gancho na batida 1, refrão curto repetido, pergunta e resposta, gesto, mudança de tom no último refrão."""
import json, sys

BASE_CAPTION = ("Gentle cheerful Brazilian nursery-rhyme style children's song for babies and toddlers up to 5 years old, sweet and soft, extremely catchy singalong, "
                "warm friendly adult male lead vocal with a sweet kids choir answering the hook, bright and playful but calm and cute, clean polished mix, "
                "the hook starts right on the first beat with no intro, every section lasts exactly 4 bars, short repeated chorus, simple melody in small steps, "
                "call and response with the kids choir, the last chorus goes up by a whole step (key change), clear Portuguese pronunciation of every word")


def S(chorus, v1, v2, bridge, extra=False):
    secs = [("Chorus", chorus), ("Verse 1", v1), ("Chorus", chorus), ("Verse 2", v2), ("Bridge", bridge), ("Chorus", chorus)]
    if extra:
        secs.append(("Final Chorus", chorus))
    return "\n\n".join(f"[{t}]\n{x.strip()}" for t, x in secs)


SONGS = {
 1: dict(titulo='Pé, Pé, Bate o Pezinho!', slug='pe-pe-bate-o-pezinho', bpm=112, key='C major',
         inst='bouncy ukulele strums, soft stomping foot percussion, gentle hand claps, bright glockenspiel, round soft bass',
         lyr=S('Pé, pé, bate o pezinho,\npá, pá, com muito carinho,\ngira, gira, devagarinho,\ndança com o seu amiguinho!', 'Um pezinho vai pra frente,\noutro pezinho vai pra trás,\ntodo mundo está contente,\ndançando e pedindo mais!', 'Bate palma, bate o pé,\ndança, dança, sem parar,\nbate o pé, bate o pé,\nvem comigo, vem dançar!', 'Pé, pé, pá, pá,\ntodo mundo vai dançar,\npé, pé, pá, pá,\nninguém quer parar!', True)),
 2: dict(titulo='Quem Faz Assim?', slug='quem-faz-assim', bpm=100, key='G major',
         inst='playful acoustic guitar, soft hand claps, shaker, xylophone, light bass, cute animal sound-like vocal ad-libs',
         lyr=S('Quem faz assim? Mi-au, mi-au!\nQuem faz assim? Au-au, au-au!\nÉ o gatinho, é o cachorrinho,\ncada um com seu jeitinho!', 'Quá, quá, quá, faz o patinho,\npiu, piu, piu, faz o pintinho,\nmuuu, muuu, faz a vaquinha,\ncó, có, có, faz a galinha!', 'Oinc, oinc, faz o porquinho,\nploc, ploc, faz o sapinho,\ngrrr, grrr, faz o leãozinho,\ne eu faço, eu faço um carinho!', 'Mi-au, mi-au, au-au, au-au,\npiu, piu, muuu, muuu, muuu,\nquá, quá, quá, que festa que eu vi,\nos bichinhos estão aqui!', False)),
 3: dict(titulo='Cores do Arco-Íris', slug='cores-do-arco-iris', bpm=104, key='C major',
         inst='bright marimba, plucked guitar, soft hand claps, glockenspiel melody, warm bass',
         lyr=S('Vermelho, laranja, amarelo, que cor!\nVerde, azul, anil, violeta, que amor!\nArco-íris, arco-íris, no céu a brilhar,\npintando a alegria no ar!', 'Vermelha é a maçã,\namarelo é o sol da manhã,\nverde é a folhinha no jardim,\ne azul é o céu sem fim!', 'Violeta é a florzinha,\nanil é a noitinha,\nlaranja é a cenourinha,\ne o arco-íris é a rainha!', 'Olha só quanta cor,\nvamos cantar com amor,\ntodo mundo canta junto,\ncada cor tem seu assunto!', False)),
 4: dict(titulo='Abraça, Abraça, Abraça!', slug='abraca-abraca-abraca', bpm=108, key='F major',
         inst='warm acoustic guitar, soft piano chords, gentle hand claps, light shaker, gentle bass, sweet kids choir',
         lyr=S('Abraça, abraça, abraça quem tá perto,\num abraço apertado deixa o dia mais esperto,\nabraça, abraça, abraça de verdade,\nabraço é amizade, abraço é felicidade!', 'Abraça a mamãe, abraça o papai,\no amor é tão grande que nunca se vai,\nabraça o amiguinho, abraça o irmãozinho,\nquem abraça ganha um sorrisinho!', 'Um abraço de urso, forte e quentinho,\num abraço de coala, bem devagarinho,\num abraço de polvo, cheio de bracinhos,\ntodo mundo fica felizinho!', 'Um, dois, três, abraço,\nfica pertinho, no meu laço,\num, dois, três, abraço,\neu te dou um grande abraço!', True)),
 5: dict(titulo='Pop-Pop, Banho de Bolhas!', slug='pop-pop-banho-de-bolhas', bpm=120, key='G major',
         inst='bubbly soft plucks, cute popping sounds, ukulele, gentle hand claps, bouncy soft bass, sparkly glockenspiel',
         lyr=S('Pop, pop, pop, as bolhinhas vão estourar,\npop, pop, pop, é hora de se ensaboar,\nesfrega o bracinho, esfrega o pezinho,\npop, pop, pop, fico limpinho!', 'Sabonete na mão, cheirinho de flor,\nespuma na cabeça, que coisa de amor,\nesfrega a barriguinha, que cosquinha,\npop, pop, pop, que bolhinha!', 'Água morninha, que gostosa que é,\nenxágua o corpinho, da cabeça ao pé,\npop, pop, pop, quanta espuma,\ntchau, sujeira, não sobra nenhuma!', 'Bolhinha pra lá, bolhinha pra cá,\npop, pop, pop, quem vai pegar,\nbolhinha pra cá, bolhinha pra lá,\npop, pop, pop, quem vai estourar!', True)),
 6: dict(titulo='Ma-Ma, Pa-Pa!', slug='ma-ma-pa-pa', bpm=100, key='C major',
         inst='gentle music-box and glockenspiel, soft ukulele, light hand claps, warm bass, tender and happy baby-friendly feel',
         lyr=S('Ma-ma, pa-pa, ma-ma, pa-pa,\na primeira palavrinha vai chegar,\nma-ma, pa-pa, ma-ma, pa-pa,\no bebê já sabe chamar!', 'Quem me abraça de manhã? É a mamãe, minha fã,\nquem me leva pra brincar? É o papai, vem me pegar,\nma-ma, ma-ma, pa-pa, pa-pa,\nque alegria vai chegar!', 'Eu tento falar, eu tento falar,\nma-ma, pa-pa, vou conseguir chamar,\na mamãe sorri, o papai também,\nma-ma, pa-pa, que alegria que vem!', 'Ma-ma, pa-pa, ma-ma, pa-pa,\neu te amo, mamãe,\neu te amo, papai,\no amor nunca sai!', False)),
 7: dict(titulo='Bom Dia, Sol!', slug='bom-dia-sol', bpm=112, key='D major',
         inst='sunny acoustic guitar strums, soft hand claps, bright glockenspiel, gentle whistle, upbeat soft bass, morning energy',
         lyr=S('Bom dia, sol, bom dia, céu,\nque bom, que bom, o dia nasceu,\nestica, estica o corpinho,\nbom dia, sol, com carinho!', 'Os braços pra cima, bem alto, bem alto,\ndepois pra baixo, num salto,\ngira a cabecinha, devagarinho,\ne dá um sorriso bonitinho!', 'Escovo os dentinhos, lavo o rostinho,\ntomo o café bem quentinho,\ncalço o tênis, vou pro jardim,\nbom dia pra você e pra mim!', 'Sol, sol, sol, sol, bom dia, bom dia,\nsol, sol, sol, sol, que alegria!', True)),
 8: dict(titulo='Só Mais Cinco Minutinhos!', slug='so-mais-cinco-minutinhos', bpm=120, key='F major',
         inst='funny bouncy soft bass, playful ukulele, hand claps, quirky xylophone, cute call and response, kids choir saying the hook',
         lyr=S('Só mais cinco minutinhos, só mais um,\njá é hora de dormir? Nenhum!\nSó mais cinco minutinhos, por favor,\ntá bom, tá bom, eu vou, meu amor!', 'Escovei os dentes, vesti o pijama,\nquero só mais uma historinha na cama,\nquero só mais um beijinho,\ne um abraço bem apertadinho!', 'A mamãe disse: já chega, filhinho,\no papai disse: vem, amiguinho,\na lua já brilha, o sono já vem,\neu bocejo, aaaah, que sono bem!', 'Cinco, quatro, três, dois, um,\nshhh, não faço mais nenhum,\ncinco, quatro, três, dois, um,\nshhh, boa noite, bom sonho a cada um!', True)),
 9: dict(titulo='Parabéns, Que Festa!', slug='parabens-que-festa', bpm=116, key="G major",
         inst='cheerful birthday nursery-rhyme feel, ukulele and glockenspiel, soft hand claps, little party horn sounds, sweet kids choir',
         lyr=S('Parabéns, parabéns, vamos cantar,\nbate palma, vem dançar,\nhoje é dia de festa, vem pular,\no aniversariante vai brilhar!', 'Tem bolo de chocolate, tem brigadeiro,\ntem balão e confete o dia inteiro,\ntem doce, tem pipoca, tem alegria,\na festa é boa, é de noite e de dia!', 'Sopra a velinha, faz um pedido,\no desejo é lindo e vai ser cumprido,\num, dois, três, sopra com vontade,\nfeliz aniversário, felicidade!', 'Palma, palma, palma, palma,\ntoda a turma bate palma,\npula, pula, pula, pula,\ntoda a turma faz bagunça!', True)),
 10: dict(titulo='Tchu-Tchu, Trenzinho!', slug='tchu-tchu-trenzinho', bpm=108, key='C major',
         inst='gentle chugging train rhythm with shaker and brushes, ukulele, little train whistle sounds, hand claps, soft bouncy bass, glockenspiel',
         lyr=S('Tchu-tchu, lá vem o trenzinho,\npiiii! Apita pelo caminho,\ntchu-tchu, vagãozinho por vagãozinho,\ntodo mundo a bordo, vamos juntinhos!', 'O vagão vermelho vem primeiro,\no azul vem logo, ligeiro,\no amarelo vem animado,\ne o verde chega, e fica ao lado!', 'O trenzinho passa na ponte,\no trenzinho passa no monte,\nentra no túnel, escuro e bem curtinho,\ne sai do outro lado, bem pertinho!', 'Tchu, tchu, tchu, tchu, chegou,\npiiii, piiii, o trem apitou,\ntchu, tchu, tchu, tchu, chegamos,\npiiii, piiii, todos cantamos!', True)),
}


def build(n, seed):
    s = SONGS[n]
    return {"lm_model": "acestep-5Hz-lm-1.7B-Q8_0.gguf", "synth_model": "acestep-v15-turbo-Q8_0.gguf",
            "caption": f"{BASE_CAPTION}, {s['inst']}", "lyrics": s["lyr"], "duration": 60, "bpm": s["bpm"],
            "vocal_language": "pt", "keyscale": s["key"], "timesignature": "4", "inference_steps": 8,
            "guidance_scale": 1.0, "shift": 3.0, "seed": seed}


if __name__ == "__main__":
    json.dump(build(int(sys.argv[1]), int(sys.argv[2])), open(sys.argv[3], "w"), ensure_ascii=False, indent=2)
