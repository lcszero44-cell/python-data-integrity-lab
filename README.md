# 🛡️ Simulação Educacional de Ameaças em Python & Defesa Cibernética (Blue Team Lab)

![Python](https://img.shields.io/badge/Python_3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Cryptography](https://img.shields.io/badge/Fernet_AES--128-0F172A?style=for-the-badge&logo=letsencrypt&logoColor=white)
![Blue Team](https://img.shields.io/badge/Endpoint_Defense_%26_EDR-0284C7?style=for-the-badge&logo=securityscorecard&logoColor=white)
![DIO Lab](https://img.shields.io/badge/DIO_Cybersecurity_Lab-E11D48?style=for-the-badge)

> **Aviso Ético e Legal (Disclaimer):** Todo o código, documentação e análise técnica deste repositório foram desenvolvidos exclusivamente para fins educacionais em ambiente controlado e isolado (`./sandbox_files`), visando compreender mecanismos de ameaças digitais para projetar defesas eficazes (Blue Team / EDR).

---

## 📌 Visão Geral do Desafio

Este repositório documenta os estudos práticos sobre o funcionamento interno de duas classes clássicas de ameaças digitais — **Ransomware** e **Keylogger** — implementadas de forma controlada e segura em **Python**, acompanhadas de um monitor defensivo comportamental (`scripts/directory_watcher.py`) e um guia completo de mitigação (`docs/SECURITY_GUIDELINES.md`).

### Objetivos Técnicos Cobertos
* **Criptografia Simétrica Aplicada (`cryptography.fernet`):** Implementação segura de rotina de cifragem e decifragem restrita à pasta de laboratório `./sandbox_files`, com geração de nota informativa (`AVISO_SIMULACAO.txt`).
* **Análise de Captura de Eventos e Exfiltração (`pynput` & `smtplib`):** Estudo arquitetural de como listeners de teclado capturam eventos de entrada, técnicas de execução em segundo plano (`.pyw` / processos sem console) e canais de envio via SMTP autenticado.
* **Detecção Comportamental (Blue Team / EDR):** Simulação em Python de detecção de alterações rápidas de hash SHA-256 em diretórios sensíveis.
* **Estratégias de Prevenção e Defesa:** Análise estruturada de Antivírus/EDR, Firewall de Egresso, Sandboxing, Backups 3-2-1 e Conscientização do Usuário.

---

## 🏗️ Arquitetura do Estudo (Vetor de Ataque vs. Camada de Defesa)

```mermaid
flowchart TB
    subgraph Lab["Ambiente Controlado (Sandbox Educacional)"]
        direction LR
        R["🔐 Módulo 1: Ransomware Simulado<br/>cryptography.fernet (AES-128-CBC + HMAC)<br/>Alvo restrito: ./sandbox_files/"]
        K["⌨️ Módulo 2: Keylogger (Estudo Arquitetural)<br/>pynput.keyboard Listener + smtplib TLS<br/>Registro local & exfiltração controlada"]
    end

    subgraph Defense["Camadas de Proteção & Mitigação (Blue Team)"]
        D1["🛡️ EDR / Monitor Comportamental<br/>Detecção de I/O em massa & hooking de API"]
        D2["🧱 Firewall de Egresso & DLP<br/>Bloqueio de SMTP/portas não autorizadas"]
        D3["📦 Sandboxing & Menor Privilégio<br/>Execução isolada e bloqueio de scripts"]
        D4["💾 Backup Imutável (Regra 3-2-1)<br/>Recuperação sem pagamento de resgate"]
    end

    R --> D1
    R --> D4
    K --> D2
    K --> D3
