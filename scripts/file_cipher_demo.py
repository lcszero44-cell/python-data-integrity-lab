import os
import sys
from pathlib import Path

try:
    from cryptography.fernet import Fernet
    HAS_CRYPTOGRAPHY = True
except ImportError:
    import base64
    HAS_CRYPTOGRAPHY = False

SANDBOX_DIR = Path(__file__).resolve().parent.parent / "sandbox_files"
KEY_FILE = Path(__file__).resolve().parent.parent / "chave.key"
NOTICE_FILE = SANDBOX_DIR / "AVISO_SIMULACAO.txt"


def gerar_ou_carregar_chave() -> bytes:
    if KEY_FILE.exists():
        return KEY_FILE.read_bytes()
    chave = Fernet.generate_key() if HAS_CRYPTOGRAPHY else b"sandbox-demo-key-2026"
    KEY_FILE.write_bytes(chave)
    return chave


def cifrar_dados(dados: bytes, chave: bytes) -> bytes:
    if HAS_CRYPTOGRAPHY:
        return Fernet(chave).encrypt(dados)
    return base64.b64encode(dados)


def decifrar_dados(dados: bytes, chave: bytes) -> bytes:
    if HAS_CRYPTOGRAPHY:
        return Fernet(chave).decrypt(dados)
    return base64.b64decode(dados)


def processar_sandbox(modo_restaurar: bool = False) -> None:
    if not SANDBOX_DIR.exists():
        print(f"[ERRO] Diretório de laboratório não encontrado: {SANDBOX_DIR}")
        return

    chave = gerar_ou_carregar_chave()
    arquivos_alvo = [
        arq for arq in SANDBOX_DIR.iterdir()
        if arq.is_file() and arq.name != NOTICE_FILE.name
    ]

    for arquivo in arquivos_alvo:
        conteudo = arquivo.read_bytes()
        if modo_restaurar:
            resultado = decifrar_dados(conteudo, chave)
            arquivo.write_bytes(resultado)
            print(f"[RESTAURADO] {arquivo.name}")
        else:
            resultado = cifrar_dados(conteudo, chave)
            arquivo.write_bytes(resultado)
            print(f"[CODIFICADO] {arquivo.name}")

    if modo_restaurar:
        if NOTICE_FILE.exists():
            NOTICE_FILE.unlink()
        print("\n[OK] Todos os arquivos do sandbox foram restaurados com sucesso.")
    else:
        NOTICE_FILE.write_text(
            "SIMULACAO EDUCACIONAL DE LABORATORIO (DIO CYBERSECURITY)\n"
            "Os arquivos desta pasta sandbox foram codificados com Fernet.\n"
            "Execute 'python scripts/file_cipher_demo.py --restore' para restaurar.\n",
            encoding="utf-8",
        )
        print(f"\n[OK] Simulação concluída. Nota gerada em: {NOTICE_FILE.name}")


if __name__ == "__main__":
    restaurar = "--restore" in sys.argv
    processar_sandbox(modo_restaurar=restaurar)
