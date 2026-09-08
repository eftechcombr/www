---
title: "GLPI 12.0.0-rc1 e Helm Chart 2.12.0: modernização de subcharts, hardening e alta disponibilidade"
description: "A EF-TECH anuncia o lançamento do GLPI 12.0.0-rc1 e Helm Chart 2.12.0. Conheça as novidades: subchart Valkey, PDB, HPA, backup para S3 e hardening com readOnlyRootFilesystem."
summary: "A EF-TECH disponibiliza as imagens Docker do GLPI 12.0.0-rc1 e a versão 2.12.0 do Helm Chart, trazendo subchart Valkey, suporte a cache externo, PDB/HPA para php-fpm e nginx, backup S3 e hardening de segurança."
date: 2026-09-06
draft: false
tags: ["glpi", "docker", "kubernetes", "helm", "cloud-native", "seguranca"]
categories: ["infraestrutura"]
featureimage: "/img/blog/glpi-12-0-0-rc1/cover.png"
featureimagecaption: "GLPI 12.0.0-rc1 e Helm Chart 2.12.0 da EF-TECH"
---

A EF-TECH tem o orgulho de anunciar o lançamento do **GLPI 12.0.0-rc1** (Release Candidate) e a nova versão **2.12.0 do nosso Helm Chart**. Esta atualização representa um marco arquitetural importante na evolução da distribuição cloud-native do GLPI mantida pela EF-TECH, introduzindo modernização completa de dependências, suporte a cache Valkey, escalabilidade horizontal, rotinas automatizadas de backup em S3 e reforços substanciais de segurança para clusters Kubernetes corporativos.

![GLPI 12.0.0-rc1 e Helm Chart 2.12.0](/img/blog/glpi-12-0-0-rc1/cover.png)

Como se trata de um **Release Candidate**, esta versão é ideal para times que desejam validar o novo ciclo do GLPI 12, testar novos recursos em ambientes de homologação e homologar fluxos de migração antes da versão final de produção.

---

## Principais Novidades e Melhorias

### 1. Modernização de Subcharts: Valkey e MariaDB

Para acompanhar a evolução do ecossistema open-source e garantir compatibilidade a longo prazo, o Helm Chart agora adota subcharts independentes e modernos:

- **Subchart Valkey (`helmforge/valkey`)**: substituímos o subchart inline de Redis pelo **Valkey**, fork de código aberto sob governança da Linux Foundation. O Valkey oferece alto desempenho para sessões e cache do GLPI com total aderência aos padrões abertos.
- **Subchart MariaDB (`helmforge/mariadb`)**: substituímos o MariaDB inline por um subchart dedicado e atualizado do `helmforge/mariadb`.
- **Suporte a `externalCache`**: agora é possível apontar o GLPI diretamente para clusters externos de Valkey ou Redis gerenciados (como AWS ElastiCache, Azure Redis ou instâncias dedicadas) através de configurações explícitas no `values.yaml`.

### 2. Alta Disponibilidade e Escalabilidade (PDB e HPA)

Para ambientes de missão crítica que necessitam de tolerância a falhas e escalabilidade dinâmica:

- **PodDisruptionBudget (PDB)**: suporte opcional a PDB tanto para os pods de `php-fpm` quanto para o `nginx`. Garante que durante manutenções programadas de nós (como upgrades de cluster e drenagem de nós com `kubectl drain`), um número mínimo de réplicas permaneça saudável e disponível.
- **HorizontalPodAutoscaler (HPA)**: suporte opcional a HPA v2 para autoescalonamento dinâmico de réplicas de `php-fpm` e `nginx` baseado no consumo real de CPU e memória.
- **`priorityClassName` para Pods GLPI**: atribuição de classes de prioridade aos pods do GLPI, garantindo que o Kubernetes priorize o agendamento e a retenção do serviço de chamados frente a workloads não críticos.

### 3. Hardening de Segurança Avançado

A segurança é um dos pilares do trabalho da EF-TECH com contêineres e Kubernetes:

- **Hardening com `readOnlyRootFilesystem`**: adicionamos suporte opcional para montar o sistema de arquivos raiz como somente leitura (`readOnlyRootFilesystem: true`), empiricamente verificado e compatível com as necessidades de escrita temporária do GLPI através de volumes efêmeros.
- **Isolamento do Nginx**: removemos montagens de volume desnecessárias e variáveis com credenciais de banco de dados do contêiner do Nginx, respeitando estritamente o princípio do menor privilégio.
- **Gestão de Segredos de Banco de Dados**: a senha `MARIADB_PASSWORD` agora é lida diretamente da Secret gerada pelo subchart MariaDB.
- **Suporte a `existingSecret` para `externalDatabase`**: ao utilizar bancos de dados externos, você pode referenciar uma Secret preexistente com validação *fast-fail* — se a Secret ou a chave não existirem, a renderização do chart falha imediatamente, evitando deploys inconsistentes.

### 4. Confiabilidade Operacional e Backup S3

- **Backup Automatizado de Arquivos para S3**: introduzimos um CronJob dedicado para backup periódico dos documentos e anexos do GLPI (`/var/lib/glpi/files`) diretamente para buckets S3 compatíveis (AWS S3, MinIO, Cloudflare R2 ou Ceph).
- **Gating de Prontidão no CronJob de Manutenção**: o CronJob responsável pelas tarefas rotineiras do GLPI agora aguarda ativamente a prontidão do GLPI e do banco de dados antes de disparar os comandos, eliminando falhas transitórias durante reinicializações.
- **Presets de Recursos (`resourcesPreset`)**: inclusão de níveis padronizados de recursos estilo Bitnami (`nano`, `micro`, `small`, `medium`, `large`, `xlarge`), facilitando o dimensionamento correto de CPU e memória para cada porte de organização.
- **Estrutura Helm e Artifact Hub**: reorganização de todos os templates do chart no diretório padronizado `helm/` e conformidade completa com os requisitos de validação do Artifact Hub.

---

## Matriz de Versões

| Componente | Versão | Origem / Catálogo |
|---|---|---|
| GLPI (Aplicação) | `12.0.0-rc1` | [ghcr.io/eftechcombr/glpi](https://github.com/eftechcombr/glpi/packages) |
| Helm Chart | `2.12.0` | [eftech/glpi](https://github.com/eftechcombr/glpi/releases/tag/glpi-2.12.0) |
| Cache padrão | Valkey | `helmforge/valkey` |
| Banco padrão | MariaDB | `helmforge/mariadb` |

---

## Como Instalar e Atualizar

### Atualização via Helm Chart

Adicione o repositório oficial de charts da EF-TECH (ou atualize seu catálogo) e execute a instalação ou upgrade:

```bash
# Adicionar ou atualizar o repositório Helm da EF-TECH
helm repo add eftech https://eftechcombr.github.io/glpi/charts
helm repo update

# Instalar ou atualizar para a versão 2.12.0
helm upgrade --install glpi eftech/glpi \
  --namespace glpi \
  --create-namespace \
  --version 2.12.0
```

### Exemplo de Configuração (`values.yaml`)

Abaixo está um exemplo prático demonstrando o uso dos novos recursos de alta disponibilidade, hardening e presets de recursos:

```yaml
# Definir preset de recursos padronizado
resourcesPreset: "medium"

# Hardening do sistema de arquivos
securityContext:
  readOnlyRootFilesystem: true

# Alta disponibilidade com PDB
podDisruptionBudget:
  enabled: true
  minAvailable: 1

# Autoescalonamento horizontal (HPA)
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 8
  targetCPUUtilizationPercentage: 75
  targetMemoryUtilizationPercentage: 80

# Prioridade no agendamento Kubernetes
priorityClassName: "system-cluster-critical"

# Subchart Valkey ativado por padrão
valkey:
  enabled: true

# Backup automatizado para storage S3 compatível
backup:
  files:
    enabled: true
    schedule: "0 2 * * *"  # Todos os dias às 02:00
    s3:
      endpoint: "https://s3.amazonaws.com"
      bucket: "meu-bucket-glpi-backups"
      region: "us-east-1"
      existingSecret: "s3-backup-credentials"
```

### Imagem Docker Standalone

Se você opera o GLPI diretamente no Docker ou Docker Compose:

```bash
docker pull ghcr.io/eftechcombr/glpi:12.0.0-rc1
```

---

## Links e Referências

- [Repositório Oficial do Projeto GLPI](https://github.com/glpi-project/glpi)
- [Repositório Oficial EF-TECH GLPI no GitHub](https://github.com/eftechcombr/glpi)
- [Release GLPI 12.0.0-rc1](https://github.com/eftechcombr/glpi/releases/tag/v12.0.0-rc1)
- [Release Helm Chart 2.12.0](https://github.com/eftechcombr/glpi/releases/tag/glpi-2.12.0)
- [Catálogo de Imagens e Pacotes](https://github.com/eftechcombr/glpi/packages)

---

## Suporte e Consultoria Especializada

A **EF-TECH** é referência em arquiteturas de Service Desk, ITSM e automação de infraestrutura. Projetamos, implantamos e mantemos ambientes GLPI em Kubernetes de alta performance com observabilidade, segurança e escalabilidade garantidas.

Precisa de apoio para planejar o ciclo de homologação do GLPI 12 ou modernizar a infraestrutura da sua empresa? [Entre em contato com nossos especialistas](/pt-br/contato/).
