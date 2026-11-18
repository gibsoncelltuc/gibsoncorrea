# Referências para modelar no Blender (objeto real: carro, avião, prédio, aparelho, roupa de profissão...)

Quando o roteiro pede um objeto REAL que não existe na biblioteca (a folha 2 lista em "PARA O BLENDER" como FALTA), faça nesta ordem:

1. **Pesquisar**: use a busca na internet (WebSearch) com o nome exato + "side view", "front view", "dimensions". Abra 2–3 páginas confiáveis (fabricante, Wikipédia, museu) com WebFetch e anote o que importa para o desenho. Se conseguir baixar imagem (`curl -L -o referencias/<nome>/frente.jpg <url>` de página pública), guarde em `referencias/<nome>/` e ABRA a imagem (Read) para olhar. Não dá para baixar de todo site; se não der, vale a descrição escrita.
2. **Ficha** `referencias/<nome>/FICHA.md` (copie o modelo abaixo): medidas reais, silhueta, 3 a 5 partes que tornam o objeto reconhecível, cores, o que se mexe (roda, hélice).
3. **Modelar** em `blender/objetos_<sessao>.py` com `blender/formas.py`, seguindo a ficha: primeiro o volume principal (torno/bola esticada/caixa chanfrada), depois as partes marcantes, depois detalhes. Estilo cartunesco: proporção um pouco exagerada, cores chapadas, nada de textura fotográfica.
4. **Conferir** com `blender -b --python blender/foto.py -- /tmp/f.png web/assets/library/kit/<nome>.glb` e comparar com a referência: alguém que nunca viu a ficha reconhece o objeto? Se não, refaça as partes marcantes.
5. **Cadastrar** em `obj_dict.d/<sessao>.json`, rodar `python3 capacidades.py`, commit + push (glb, script, ficha).

## Modelo de FICHA.md
```
Objeto: <nome real e ano>
Fontes: <links consultados>
Medidas reais: comprimento x largura x altura (m)  -> no vídeo: altura ~<m> (personagem tem ~2 m)
Silhueta em uma frase: <ex.: cunha baixa de aço, teto reto, sem curvas>
Partes que identificam (em ordem de importância): 1) ... 2) ... 3) ...
Cores: principal #...., detalhe #...., vidro #....
Partes móveis: rodas / hélice / porta
Não esquecer: <o detalhe que todo mundo lembra>
```
Pessoa real ou marca: desenhe o objeto de forma reconhecível, sem copiar logotipo; pessoa real só como caricatura pelos traços gerais (ver `FIGURINOS_FAMOSOS.md`).
