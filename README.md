# Python Data Integrity & File Monitoring Lab

Laboratório educacional em Python voltado para o estudo prático de **integridade de arquivos**, **codificação simétrica em ambiente controlado** e **monitoramento contínuo de alterações em diretórios locais** utilizando hashes criptográficos SHA-256.

> **Aviso Educacional:** Todos os scripts deste repositório foram projetados exclusivamente para fins de estudo e auditoria em ambiente controlado, operando estritamente sobre a pasta local `./sandbox_files`.

## Estrutura do Projeto

```text
Python-Data-Integrity-Lab/
├── README.md
├── .gitignore
├── docs/
│   └── SECURITY_GUIDELINES.md
├── sandbox_files/
│   ├── documento_financeiro.txt
│   └── notas_projeto.txt
└── scripts/
    ├── directory_watcher.py
    └── file_cipher_demo.py
```

## Componentes

- **`sandbox_files/`**: Diretório isolado contendo arquivos de texto fictícios utilizados nos testes de integridade e codificação.
- **`scripts/file_cipher_demo.py`**: Utilitário educacional que aplica codificação simétrica via `cryptography.fernet.Fernet` (com fallback automático em Base64 caso a biblioteca `cryptography` não esteja instalada) exclusivamente nos arquivos de teste dentro de `./sandbox_files`, gera a chave local `chave.key`, registra um resumo em `NOTA_INFORMATIVA.txt` e restaura os arquivos originais com a flag `--restore`.
- **`scripts/directory_watcher.py`**: Monitor de integridade que calcula hashes SHA-256 dos arquivos em `./sandbox_files` usando apenas a biblioteca padrão do Python (`os`, `hashlib` e `time`), emitindo um alerta de auditoria ao identificar modificações rápidas em lote.
- **`docs/SECURITY_GUIDELINES.md`**: Guia técnico com boas práticas de proteção de endpoints, controle de acesso, firewall de saída, estratégia de backup 3-2-1 e autenticação multifator (MFA).

## Pré-requisitos

- Python 3.9+
- (Opcional) Biblioteca `cryptography` para utilizar `Fernet`:
  ```bash
  pip install cryptography
  ```
  Caso `cryptography` não esteja instalada, `file_cipher_demo.py` utiliza automaticamente o modo de fallback em Base64.

## Como Executar o Laboratório

### 1. Iniciar o monitor de integridade (Terminal 1)

```bash
python scripts/directory_watcher.py
```

Parâmetros opcionais:
- `--interval 1.0`: intervalo de verificação em segundos.
- `--window 10.0`: janela de tempo (em segundos) para correlação de eventos em lote.
- `--threshold 2`: número mínimo de eventos na janela para disparar o alerta de auditoria.

### 2. Executar o teste de codificação controlada (Terminal 2)

Para codificar os arquivos de teste em `./sandbox_files`:

```bash
python scripts/file_cipher_demo.py
```

Para restaurar os arquivos originais:

```bash
python scripts/file_cipher_demo.py --restore
```

## Boas Práticas e Defesa

Consulte o documento [docs/SECURITY_GUIDELINES.md](docs/SECURITY_GUIDELINES.md) para diretrizes completas de proteção de endpoints e resposta a alterações anômalas em sistemas de arquivos.
