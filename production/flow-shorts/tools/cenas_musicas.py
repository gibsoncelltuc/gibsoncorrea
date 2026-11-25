# Cenas por música: 6 clipes de 10 s. Cada clipe: personagens (<=3), cenário, câmera, imagem inicial,
# keys = [(palavra cantada, ação na tela, ocorrência opcional)] -> o tempo exato vem do alinhamento da música.
MEADOW = "a sunny flowery meadow with a soft round wooden dance stage, pastel balloons and a clear blue sky in the background"
CENAS = {
1: [
 dict(chars=["Bento","Luna","Tico"], setting=MEADOW, cam="wide-medium shot, eye level, very slow gentle push-in",
      img="Bento stands at the center of the stage with his two floppy ears hanging down, Luna on his left and Tico on his right, all three smiling and ready to dance, feet on the ground",
      keys=[("pezinho","Bento lifts one foot a little and taps it softly on the stage"),("gira","Bento turns slowly once in place, Luna and Tico sway"),("amiguinho","Bento waves to Luna and Tico, who smile and wave back")]),
 dict(chars=["Bento","Pipo"], setting=MEADOW, cam="medium shot, eye level, slow gentle drift to the right",
      img="Bento and little Pipo face the camera side by side on the stage, Bento's weight on his back foot, ready to step",
      keys=[("frente","Bento takes one slow small step forward"),("trás","Bento takes one slow small step back"),("contente","Bento smiles widely, his floppy ears sway gently"),("mais","Pipo hops once happily next to him"),("pezinho","Bento taps one foot softly",2)]),
 dict(chars=["Luna","Tico","Pipo"], setting=MEADOW, cam="medium shot, eye level, slow gentle push-in",
      img="Luna, Tico and Pipo stand in a row on the stage, smiling, Luna in the middle",
      keys=[("gira","Luna turns slowly once in place with a happy smile"),("dança","Tico sways side to side",1),("palma","all three give one small clap together"),("parar","they keep swaying happily, nobody stops")]),
 dict(chars=["Bento","Tico","Pipo"], setting=MEADOW, cam="medium-wide shot, eye level, very slow orbit to the left",
      img="Bento in the center with Tico and Pipo beside him, all three mid-dance with big smiles, feet on the ground",
      keys=[("pé","Bento stomps one foot softly",2),("dançar","Tico and Pipo sway happily",1),("pá","all three clap once softly"),("mundo","everyone turns slowly toward the camera")]),
 dict(chars=["Bento"], setting=MEADOW, cam="close-up on Bento from the chest up, eye level, very slow push-in",
      img="Bento alone, centered, looking at the camera with a sweet smile, both floppy ears hanging down beside his cheeks",
      keys=[("ninguém","Bento tilts his head sweetly side to side"),("pezinho","Bento taps one foot, only his shoulders move a little"),("carinho","Bento puts both paws softly near his chest with a warm smile"),("devagarinho","Bento turns his head slowly to the left then back")]),
 dict(chars=["Bento","Luna","Tico"], setting=MEADOW, cam="wide shot, eye level, slow pull-back at the end",
      img="Bento, Luna and Tico stand together in the center of the stage, arms relaxed, smiling at the camera",
      keys=[("pezinho","Bento taps one foot"),("carinho","all three clap once softly"),("devagarinho","all three turn slowly once"),("amiguinho","all three wave at the camera and hold a happy final pose")]),
],
}
