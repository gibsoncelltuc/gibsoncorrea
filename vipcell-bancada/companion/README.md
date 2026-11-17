# Vipcell Bancada — companion de PC

Programa de bancada que roda no Windows do técnico e executa reparo/atualização
com **ferramentas e firmware oficiais**, pelo protocolo aberto **fastboot** — o
mesmo caminho que o LMSA da Motorola usa por baixo.

Sem bypass de conta/FRP, sem firmware pirata, sem "auth crackeado".

## O que já funciona (motor + travas de segurança, testado sem celular)

- **Detecção** de modo por VID:PID (fastboot, BROM, EDL, Download, Preloader…).
- **Recuperar Moto brickado** a partir do firmware **oficial** extraído:
  lê o `flashfile.xml`/`servicefile.xml` do pacote e monta o mesmo plano de
  comandos fastboot da Motorola.

### Travas contra "cliquei no botão errado"

1. **Prévia por padrão (dry-run):** mostra todo o plano; só grava com `--run`.
2. **Checagem de modelo:** compara `getvar product` do aparelho com o modelo do
   firmware e **recusa** gravar firmware de outro aparelho (`--force` para ignorar).
3. **Sem apagar dados por padrão:** os passos de `erase userdata/metadata` só
   entram com `--wipe`.
4. **Arquivo faltando = não grava:** confere que toda imagem citada existe.
5. **Fail-safe:** operação desconhecida no XML **aborta** o plano.
6. **Para na primeira falha** de gravação, para não piorar o aparelho.

## Requisitos (no PC do técnico)

- Python 3.9+
- **platform-tools** da Google (`fastboot` no PATH) — https://developer.android.com/tools/releases/platform-tools
- Drivers do fabricante
- `pyusb` (opcional, melhora a detecção dos modos baixos): `pip install pyusb`

## Uso

```bash
# identificar o aparelho conectado
python -m vipbench.cli detectar

# descobrir qual firmware oficial pegar (lê o modelo + avisa do anti-rollback)
python -m vipbench.cli firmware

# ver o PLANO de recuperação (não grava nada)
python -m vipbench.cli recuperar-moto C:\firmware\moto_g56_oficial

# executar de verdade (preserva dados do cliente)
python -m vipbench.cli recuperar-moto C:\firmware\moto_g56_oficial --run

# executar apagando dados (só se o cliente autorizou)
python -m vipbench.cli recuperar-moto C:\firmware\moto_g56_oficial --run --wipe
```

O firmware **oficial** vem do LMSA ou de `mirrors.lolinet.com/firmware/moto`.
Este programa não baixa firmware de fonte não oficial.

## Testes

```bash
python tests/test_moto.py
```

## Limite honesto

Isto grava quando o aparelho **chega no fastboot**. Se for dead boot total (só
BROM) e o chip novo exigir auth MediaTek, o caminho seguro é o LMSA oficial —
este programa **não** usa auth/DA crackeado de fórum (é o que mata o aparelho).
