# Contexto da conversa (16/11/2026) — pedidos do usuário, em ordem, com as palavras dele resumidas

Cole este arquivo junto com o LEIA-PRIMEIRO_HANDOFF_2026-11-16.md na nova sessão.

## Origem
O usuário (Gibson, fala português) produzia vídeos curtos de guerras estranhas/curiosidades (estilo Ricks Clips) numa sessão do Claude Code web (nuvem, 4 núcleos, 15 GB, reinicia ~a cada 1 h). Trouxe a ferramenta num zip (`ferramenta-shorts`) para continuar no PC dele (Windows, 2 núcleos, sem GPU). Vídeos já entregues antes em PT: Emus, Exército de Balões, Balde (+ Onoda enviado). Zip deste trabalho não trouxe os vídeos (muito grandes).

## Pedidos e decisões
1. "Retome as atividades, faça os vídeos usando a ferramenta." → ferramenta instalada e corrigida para Windows; Karansebes v1 renderizado e entregue.
2. Feedback do v1 ("ficou bom, mas…"): faltou personagem (a "infantaria" eram 2 bonecos); câmera nunca abriu (sempre close); movimentos de câmera fracos/básicos; palavras-chave da narração devem disparar animação/movimento; câmera e animação estão ligadas e precisam evoluir muito. → implementado o diretor automático (planos abertos, multidão, efeitos por palavra) e aprovado o plano antes.
3. Esclarecimento: o render é todo local (HTML/Three.js rodando em Chromium headless por software + ffmpeg); não usa Remotion neste motor.
4. Reclamação: render do v2 "demorando desde de manhã". → medido: ~3 quadros/min com PC sobrecarregado; PC com RAM esgotada e processos antigos consumindo CPU; render do v2 foi interrompido.
5. Pedido principal atual: achar otimização significativa para que **um short de 1 min (1.500–2.500 quadros, 30 fps, 1080x1920, qualidade alta) passe por TODAS as verificações e fique pronto em ≤ 40 min (máx. 1 h)**, de preferência na nuvem (sem usar o PC dele). Hipótese do usuário: o QA pesa mais que o render — confirmada em parte (QA levou ~2 h).
6. Resultado do benchmark: 24,9 s/quadro a 1080 vs 23,9 s/quadro a 720 → custo NÃO é por pixel; é custo fixo por quadro. Próximos passos: GPU real na nuvem, perfilar um quadro, QA com menos quadros.
7. Redes sociais: publicar os mesmos vídeos no YouTube (Shorts), TikTok (conta já criada) e Instagram (Reels), com o mesmo nome de perfil nos três. O usuário quer saber se "uma rede conectada na outra" impulsiona. Resposta dada no handoff §6: reaproveitar o mesmo vídeo é válido e multiplica chances, mas cada plataforma tem alcance independente; criação de contas/uploads é feita por ele.
8. A conta Claude dele chegou a 99% do limite semanal → este pacote para continuar em outra conta.
9. Requisito de robustez: a sessão de nuvem reinicia ~1 h; o sistema deve **continuar exatamente de onde parou** sem perder processo. → `run_queue.sh` + render por quadros faltantes + checkpoints (ver handoff §5; checkpoints por etapa ainda a implementar).

## Regras do usuário a respeitar
- Responder em português, curto, honesto sobre limites; mostrar o que foi feito/falta.
- Verificar quadros (folha de contato) antes de entregar; nunca afrouxar o gate de estilo.
- Enviar arquivos prontos de imediato.
- Disco C: cheio: tudo pesado no D:.
- Sem chaves/pagamentos feitos por mim; só licença comercial.

## Estado dos arquivos
- Ferramenta: `ferramenta-shorts/` (este zip). v1 do Karansebes e prévia (`sb.jpg`) só existem no PC dele (D:\PopcornPop_ferramenta\ferramenta-shorts\out\karansebes_v1 e sb.jpg).
- Karansebes v2 (com diretor) ainda NÃO renderizado.
