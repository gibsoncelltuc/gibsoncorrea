# B -> principal: velcro1941 (e qualquer roteiro que cite "microscopio")
- O motor poe sozinho `kit/microscopio` (modelo antigo: cilindro branco grosseiro) na cena b3 mesmo com `kit/microscopio_antigo` nos props e `"objetos": false` (aparece como overlay temporizado `asset: "kit/microscopio", a:..., b:...` no spec).
- Pedido: no mkvideo, nao inserir o overlay `kit/microscopio` quando a cena ja tem prop `kit/microscopio_antigo`; ou trocar o glb `kit/microscopio` pelo `microscopio_antigo` (ja modelado em blender/objetos_b2.py, web/assets/library/kit/microscopio_antigo.glb).
- Igual ao problema do celular/micro-ondas (resolvido com `"objetos": false` nas cenas, mas aqui nao basta).
