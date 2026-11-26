# Diretrizes Técnicas de Segurança e Proteção de Endpoints

Este guia reúne boas práticas fundamentais para proteger endpoints corporativos e ambientes de desenvolvimento contra alterações não autorizadas de arquivos, comprometimento de credenciais e exfiltração de dados.

---

## 1. Proteção de Endpoints (EDR, Hardening e Monitoramento de Integridade)

- **Monitoramento de Integridade de Arquivos (FIM):** Acompanhe hashes criptográficos (como SHA-256) de diretórios críticos e correlacione eventos em janelas curtas para detectar modificações em massa rapidamente.
- **Soluções EDR/EPP Atualizadas:** Mantenha sensores de detecção e resposta em endpoints ativos, com proteção contra adulteração (*tamper protection*) e envio contínuo de telemetria para um SIEM centralizado.
- **Gestão de Patches e Hardening:** Aplique atualizações de sistema operacional e bibliotecas com SLA definido, desative serviços e portas desnecessárias e habilite proteção de memória e controle de execução de aplicações (*Application Allowlisting*).
- **Isolamento Rápido:** Defina playbooks claros para isolar imediatamente um host da rede caso alertas de alterações anômalas em lote sejam confirmados.

---

## 2. Controle de Acesso e Princípio do Menor Privilégio

- **Menor Privilégio (Least Privilege):** Conceda a usuários, scripts e contas de serviço apenas as permissões estritamente necessárias sobre diretórios e recursos.
- **Separação de Contas Administrativas:** Evite o uso diário de contas com privilégios elevados (Administrador/root). Utilize elevação sob demanda (*Just-In-Time Access*) com registro de auditoria.
- **Permissões Granulares em Arquivos (ACLs):** Restrinja permissão de escrita em compartilhamentos de rede e pastas sensíveis; mantenha diretórios de configuração e binários em modo somente leitura para usuários comuns.
- **Revisão Periódica de Acessos:** Audite regularmente contas inativas, tokens de API, chaves SSH e permissões de grupos, revogando acessos obsoletos imediatamente.

---

## 3. Firewall de Saída (Egress Filtering) e Segmentação de Rede

- **Filtragem de Tráfego de Saída:** Além de controlar conexões de entrada, configure regras restritivas de saída (*default-deny* quando viável), liberando apenas portas, protocolos e destinos explicitamente necessários.
- **Proxy e Inspeção de DNS:** Centralize a resolução DNS e o tráfego HTTP/HTTPS por meio de proxies autenticados com listas de bloqueio e detecção de domínios recém-registrados ou suspeitos.
- **Segmentação de Rede (Microsegmentação):** Separe estações de trabalho, servidores de aplicação, bancos de dados e infraestrutura de backup em VLANs/sub-redes distintas, impedindo movimentação lateral livre.
- **Logs de Fluxo:** Registre tentativas bloqueadas de conexão de saída para identificar precocemente processos tentando se comunicar com destinos não autorizados.

---

## 4. Estratégia de Backups 3-2-1 (com Imutabilidade)

Para garantir a recuperação confiável dos dados diante de falhas de hardware, erros operacionais ou incidentes de integridade, adote a regra **3-2-1** (e sua evolução **3-2-1-1-0**):

- **3 cópias dos dados:** 1 cópia de produção e pelo menos 2 cópias de backup.
- **2 mídias ou plataformas distintas:** Por exemplo, armazenamento local em servidor dedicado/NAS e armazenamento em nuvem em conta isolada.
- **1 cópia externa (off-site) e isolada/imutável:** Mantenha ao menos uma cópia fora da rede principal, protegida com *WORM* (*Write Once, Read Many*) ou *Object Lock* e credenciais independentes do diretório principal.
- **Testes Regulares de Restauração:** Valide periodicamente os backups com simulações reais de restauração, aferindo RPO (*Recovery Point Objective*) e RTO (*Recovery Time Objective*) com zero erros verificados.

---

## 5. Autenticação Multifator (MFA)

- **Obrigatoriedade Universal:** Exija MFA para todos os acessos a VPNs, painéis de nuvem, repositórios Git, consoles de backup, e-mail corporativo e acessos administrativos (SSH/RDP).
- **Preferência por Fatores Resistentes a Phishing:** Priorize chaves de segurança FIDO2/WebAuthn ou passkeys vinculadas a hardware em vez de códigos via SMS, que são suscetíveis a *SIM swapping* e interceptação.
- **Proteção contra Fadiga de MFA:** Caso utilize notificações push, habilite *number matching*, exibição de contexto geográfico/aplicação e bloqueio após múltiplas tentativas negadas.
- **Gestão Segura de Códigos de Recuperação:** Armazene códigos de recuperação em cofres de senhas corporativos com auditoria de acesso e nunca em texto plano no repositório ou na estação de trabalho.

---

## Checklist Resumido de Auditoria

| Pilar | Verificação Essencial |
| :--- | :--- |
| **Endpoint & FIM** | Monitoramento de hashes ativo e alertas centralizados? |
| **Acesso** | Contas seguem o princípio do menor privilégio e ACLs restritivas? |
| **Rede (Saída)** | Firewall de saída restringe destinos e registra bloqueios? |
| **Backup 3-2-1** | Existe cópia off-site imutável testada recentemente? |
| **MFA** | Todos os acessos críticos exigem segundo fator forte (FIDO2/TOTP)? |
