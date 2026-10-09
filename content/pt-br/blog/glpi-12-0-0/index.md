---
title: "GLPI 12.0.0: Lançamento Oficial da Nova Versão Major e Distribuição Cloud-Native da EF-TECH"
description: "O GLPI 12.0.0 foi lançado oficialmente. A EF-TECH disponibiliza as imagens Docker unprivileged e o Helm chart 2.12.0 com subcharts Valkey e MariaDB, nova Base de Conhecimento, Gerenciador de Sessões, Modo Sudo e alta disponibilidade."
summary: "O GLPI 12.0.0 chegou em 7 de outubro de 2026 como a nova versão major estável do principal ITSM open source do mercado. A distribuição cloud-native da EF-TECH (eftechcombr/glpi) já está disponível com o Helm chart glpi-2.12.0 e imagens Docker em Alpine unprivileged. Conheça a nova Base de Conhecimento reescrita do zero, o Gerenciador de Sessões ativas, a autenticação Step-Up (Modo Sudo), OLAs por grupo, o ciclo de vida com o EOL do GLPI 10 e o guia prático de migração e deploy."
date: 2026-10-09
draft: false
tags: ["glpi", "docker", "kubernetes", "helm", "cloud-native", "itsm"]
categories: ["infraestrutura"]
featureimage: "cover.png"
featureimagecaption: "GLPI 12.0.0 — Lançamento oficial da versão major e distribuição cloud-native com Docker e Kubernetes pela EF-TECH"
---

A **EF-TECH** anuncia hoje, 9 de outubro de 2026, a disponibilização oficial da versão **v12.0.0** da sua distribuição cloud-native para o GLPI no repositório [eftechcombr/glpi](https://github.com/eftechcombr/glpi) (PR #214). O lançamento acompanha a publicação oficial do **GLPI 12.0.0** pelo time upstream do [glpi-project/glpi](https://github.com/glpi-project/glpi) em 7 de outubro de 2026 — que atinge o status de General Availability (GA) estável após três rodadas de testes rigorosos nos Release Candidates (rc1, rc2 e rc3).

Com esta nova versão, fornecemos o novo **Helm chart `glpi-2.12.0`** (com `appVersion: "12.0.0"`) no repositório oficial de charts da EF-TECH, além das imagens de contêiner **`eftechcombr/glpi:php-fpm-12.0.0`** e **`eftechcombr/glpi:nginx-12.0.0`**.

![GLPI 12.0.0](cover.png)

---

## O que há de novo no GLPI 12.0.0 Upstream

O GLPI 12.0.0 representa um salto arquitetural no gerenciamento de serviços de TI (ITSM) e gestão de ativos de TI (ITAM), combinando uma experiência de usuário renovada com controles corporativos aprofundados de governança e segurança.

### 1. Base de Conhecimento Totalmente Reescrita (Knowledge Base Rework)

A Base de Conhecimento recebeu uma reconstrução completa do zero em seu frontend. A nova interface oferece:
- Navegação em árvore e categorização visual intuitiva, reduzindo o tempo de resolução de chamados pelo próprio usuário no catálogo de autoatendimento.
- Busca instantânea inteligente com filtros aprimorados e destaque de termos.
- Visualização limpa e responsiva para artigos técnicos, procedimentos operacionais padrão (SOP) e perguntas frequentes (FAQ).
- Mecanismo modernizado para inserção e renderização de mídias, anexos e códigos técnicos.

### 2. Gerenciador de Sessões Ativas (Session Management)

Para atender a exigências de auditoria de segurança e conformidade (como ISO 27001 e LGPD), o GLPI 12 introduz um controle centralizado de sessões ativas:
- Visibilidade completa de conexões por usuário: endereço IP de origem, dispositivo/navegador (*User-Agent*), data de início e última atividade registrada.
- Capacidade de encerramento remoto de sessões específicas ou em massa por administradores de sistema caso um token ou credencial seja comprometido.
- Autoinspeção para os próprios operadores, permitindo desconectar dispositivos esquecidos conectados em outros pontos de acesso.

### 3. Step-Up Authentication e Modo Sudo

Ações administrativas altamente sensíveis — como alteração de privilégios de perfis, exclusão massiva de ativos de infraestrutura ou configuração de autenticação externa (LDAP/SAML/OAuth) — agora contam com o **Modo Sudo / Step-Up Authentication**:
- O operador é desafiado a revalidar suas credenciais (ou segundo fator de autenticação) antes de prosseguir com alterações críticas.
- Essa camada de defesa em profundidade impede que sessões administrativas deixadas abertas em estações de trabalho sejam exploradas indevidamente por terceiros.

### 4. Acordos de Nível Operacional por Grupo (Group-managed OLAs)

No gerenciamento avançado de tickets e SLAs, os Acordos de Nível Operacional (OLA - *Operational Level Agreements*) definem os prazos de resposta e resolução entre equipes internas de suporte:
- O GLPI 12 adiciona suporte nativo a múltiplos OLAs diretamente atrelados a grupos técnicos de atendimento (e.g., redes, infraestrutura, desenvolvimento).
- Permite escalonamento e transição de prazos em cascata conforme o chamado transita entre diferentes squads e níveis de atendimento.

### 5. Acessibilidade Aprofundada (RGAA & RAWeb)

Este é o primeiro ciclo completo do GLPI projetado em estrita conformidade com os padrões de acessibilidade web internacionais (WCAG) e normas de referência como o **RGAA** (Référentiel Général d'Amélioration de l'Accessibilité) e **RAWeb**:
- Navegação fluida via teclado em todas as telas principais de tickets, inventário e relatórios.
- Contraste visual balanceado e compatibilidade total com leitores de tela assistivos.

### 6. Hardening de Segurança no Core

O núcleo do GLPI recebeu um ciclo intensivo de endurecimento de segurança:
- Prevenção reforçada contra injeções SQL (*SQL Injection*) e ataques de falsificação de requisições entre sites (*CSRF*).
- Validação estrita de tipos e sanitização aprofundada de inputs em todas as APIs internas e endpoints de processamento de formulários.

### 7. Nova Documentação Oficial de Usuários

A documentação para operadores e usuários finais foi totalmente reestruturada e republicada no portal [help.glpi-project.org](https://help.glpi-project.org), trazendo tutoriais passo a passo, boas práticas de ITSM e guias visuais atualizados.

### 8. Fim de Vida da Linha GLPI 10 (End-of-Life)

Um comunicado crucial para equipes de operações e infraestrutura: **o ciclo de vida do GLPI 10.x foi oficialmente encerrado**. 
- O **GLPI 10.0.28** é a versão final desta linha. 
- A partir de agora, a linha 10.x **não receberá mais correções de bugs**.
- As organizações que ainda operam no GLPI 10 devem planejar com urgência a homologação e migração para as versões mantidas (linhas 11.x e 12.x).

---

## Destaques da Distribuição Cloud-Native da EF-TECH

O projeto open source [eftechcombr/glpi](https://github.com/eftechcombr/glpi) empacota o GLPI com foco em arquiteturas em nuvem resilientes, seguras e prontas para produção no Kubernetes e Docker.

Na versão **12.0.0** e no Helm chart **`glpi-2.12.0`**, destacam-se os seguintes recursos:

| Recurso | Detalhes Técnicos |
|---|---|
| **Imagens Unprivileged (Non-Root)** | Contêineres baseados em Alpine Linux executando PHP-FPM e Nginx como usuário sem privilégios (UID 10001 / GID 10001). |
| **Subchart Valkey (`helmforge/valkey`)** | Substituição moderna do Redis inline pelo subchart dedicado Valkey, com suporte à configuração `externalCache` para clusters gerenciados externos. |
| **Subchart MariaDB (`helmforge/mariadb`)** | Banco de dados desacoplado via subchart dedicado com leitura de senhas via Secrets dinâmicas e suporte a `externalDatabase` com `existingSecret`. |
| **Templates Nginx Customizáveis** | Suporte à injeção de `nginx.conf.template` customizado via ConfigMap (PR #209), permitindo desativar facilmente o listener IPv6 em clusters que não possuem suporte de rede. |
| **Conexões de Banco com SSL/TLS** | Suporte nativo a conexões seguras criptografadas via SSL (`GLPI_DB_SSL`, `GLPI_DB_SSL_CA`, `GLPI_DB_SSL_VERIFY`) compatível com AWS Aurora, Cloud SQL e Azure MySQL (PR #207). |
| **Alta Disponibilidade (HA)** | Suporte completo a PodDisruptionBudget (PDB) e HorizontalPodAutoscaler (HPA) para absorver picos de tráfego de service desks corporativos. |
| **Hardening de Pods** | Suporte a `readOnlyRootFilesystem`, `priorityClassName`, *securityContext* estrito e perfis padronizados de recursos (`resourcesPreset`). |
| **Confiabilidade Operacional** | CronJob de manutenção (`bin/console glpi:cron`) com verificação prévia de prontidão do banco e CronJob automatizado para backup de arquivos em buckets S3 compatíveis. |

---

## Como Instalar ou Atualizar

### 1. Implantação no Kubernetes com Helm Chart

O Helm chart da EF-TECH é a forma recomendada de executar o GLPI em ambientes Kubernetes corporativos.

#### Passo 1: Adicionar o Repositório de Charts

```bash
# Adicionar o repositório oficial de charts da EF-TECH
helm repo add eftech https://eftechcombr.github.io/glpi/charts
helm repo update
```

#### Passo 2: Criar o Arquivo de Configuração (`values.yaml`)

Crie um arquivo `values.yaml` com a configuração recomendada para o GLPI 12.0.0:

```yaml
# values.yaml para GLPI 12.0.0 em produção
replicaCount: 2

image:
  repository: eftechcombr/glpi
  tag: "php-fpm-12.0.0"
  pullPolicy: IfNotPresent

nginx:
  enabled: true
  image:
    repository: eftechcombr/glpi
    tag: "nginx-12.0.0"
  resourcesPreset: "small"

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 8
  targetCPUUtilizationPercentage: 75
  targetMemoryUtilizationPercentage: 80

podDisruptionBudget:
  enabled: true
  minAvailable: 1

securityContext:
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 10001

# Subchart Valkey ativado para sessões e cache de alta performance
valkey:
  enabled: true

# Subchart MariaDB ativado para persistência interna
mariadb:
  enabled: true
  auth:
    database: glpi
    username: glpi

cron:
  enabled: true
  schedule: "*/5 * * * *"
```

#### Passo 3: Executar a Instalação ou Atualização

```bash
helm upgrade --install glpi eftech/glpi \
  --namespace glpi \
  --create-namespace \
  --version 2.12.0 \
  -f values.yaml
```

---

### 2. Implantação com Docker Compose

Para equipes que utilizam Docker standalone em servidores dedicados ou máquinas virtuais, segue o manifesto completo com PHP-FPM, Nginx, MariaDB e Valkey:

```yaml
# docker-compose.yml
services:
  glpi-db:
    image: mariadb:11.4
    restart: unless-stopped
    environment:
      - MARIADB_ROOT_PASSWORD=sua_senha_root_segura
      - MARIADB_DATABASE=glpi
      - MARIADB_USER=glpi
      - MARIADB_PASSWORD=sua_senha_glpi_segura
    volumes:
      - db_data:/var/lib/mysql
    networks:
      - glpi-net

  glpi-cache:
    image: valkey/valkey:8.0-alpine
    restart: unless-stopped
    networks:
      - glpi-net

  glpi-fpm:
    image: eftechcombr/glpi:php-fpm-12.0.0
    restart: unless-stopped
    environment:
      - GLPI_DB_HOST=glpi-db
      - GLPI_DB_NAME=glpi
      - GLPI_DB_USER=glpi
      - GLPI_DB_PASSWORD=sua_senha_glpi_segura
      - GLPI_DB_SSL=false
    volumes:
      - glpi_files:/var/www/glpi/files
      - glpi_plugins:/var/www/glpi/marketplace
    depends_on:
      - glpi-db
      - glpi-cache
    networks:
      - glpi-net

  glpi-nginx:
    image: eftechcombr/glpi:nginx-12.0.0
    restart: unless-stopped
    ports:
      - "8080:80"
    environment:
      - GLPI_PHPFPM_HOST=glpi-fpm
      - GLPI_PHPFPM_PORT=9000
    depends_on:
      - glpi-fpm
    networks:
      - glpi-net

volumes:
  db_data:
  glpi_files:
  glpi_plugins:

networks:
  glpi-net:
    driver: bridge
```

Para subir o ambiente:

```bash
docker compose up -d
```

---

## Guia de Migração: Do GLPI 10.x / 11.x para o GLPI 12.0.0

A transição para uma nova versão major exige planejamento para garantir integridade dos dados e continuidade operacional:

1. **Backup Completo de Segurança (Mandatório):**
   - Realize o dump consistente da base de dados MariaDB/MySQL (`mysqldump --single-transaction --quick glpi > backup_glpi_pre12.sql`).
   - Efetue o backup integral do diretório de arquivos (`/var/www/glpi/files/`).
2. **Homologação Prévia de Plugins:**
   - Como o GLPI 12 reformulou subsistemas e a interface da Base de Conhecimento, certifique-se de que os plugins utilizados pela sua equipe já possuem versões compatíveis lançadas pelos desenvolvedores no Marketplace.
3. **Execução da Atualização do Schema:**
   - Em contêineres, o script de entrypoint realiza a verificação de compatibilidade. Se preferir rodar manualmente via CLI:
     ```bash
     php bin/console db:update
     ```
4. **Otimização e Cache:**
   - Limpe e reconstrua o cache de aplicação com o comando:
     ```bash
     php bin/console cache:clear
     ```

---

## Links e Referências Oficiais

- [Repositório eftechcombr/glpi no GitHub](https://github.com/eftechcombr/glpi)
- [Releases e Changelog do eftechcombr/glpi](https://github.com/eftechcombr/glpi/releases)
- [Repositório Oficial de Helm Charts da EF-TECH](https://eftechcombr.github.io/glpi/)
- [GLPI no Artifact Hub](https://artifacthub.io/packages/helm/eftech/glpi)
- [Notas da Release Upstream GLPI 12.0.0](https://github.com/glpi-project/glpi/releases/tag/12.0.0)
- [Nova Documentação de Ajuda do GLPI](https://help.glpi-project.org)

---

A **EF-TECH** é especializada em arquitetura de nuvem, Kubernetes e engenharia de confiabilidade de plataformas (SRE). Implementamos, migramos e sustentamos infraestruturas GLPI com alta disponibilidade, conformidade de segurança e automação GitOps.

Para suporte na migração do seu ambiente ou implantação em cluster Kubernetes corporativo, [entre em contato conosco](/pt-br/contato/). Conheça também nossa [solução corporativa GLPI](/pt-br/produtos/glpi/) e acompanhe outros artigos técnicos em nosso [blog](/pt-br/blog/).
