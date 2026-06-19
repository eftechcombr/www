---
title: "GLPI"
description: "GLPI - software livre de gestao de ativos de TI e service desk ITIL com deploy containerizado pela EF-TECH"
summary: "GLPI e um software livre de gestao de ativos de TI e service desk ITIL. A EF-TECH oferece deploy containerizado via Docker e Kubernetes com Helm chart, hosting gerenciado e suporte dedicado."
date: 2026-06-19
tags: ["glpi", "service-desk", "itil", "inventario", "kubernetes"]
categories: ["produtos"]
---
## GLPI

GLPI (Gestionnaire Libre de Parc Informatique) e um software livre de gestao de ativos de TI e service desk ITIL. Como solucao open source, oferece recursos para inventario de hardware e software, abertura e controle de chamados, rastreamento de licencas e auditoria de software. O projeto e mantido pela comunidade no [GitHub](https://github.com/glpi-project/glpi) e distribuido sob licenca GPL-3.0. A EF-TECH especializa-se no deploy containerizado e no hosting gerenciado do GLPI, levando a versatilidade do software livre para ambientes de producao robustos e seguros.

### Service Desk ITIL

O GLPI implementa os processos ITIL para service desk, permitindo centralizar e organizar todo o atendimento de TI:

- Gestao de incidentes e problemas
- Gestao de mudancas
- Acordos de Nivel de Servico (SLA) e escalonamento
- Base de conhecimento (knowledge base)
- Catalogo de servicos
- Formularios de solicitacao de servico (service catalog)

### Gestao de Ativos e Inventario

A gestao de ativos do GLPI mantem o inventario de TI sempre atualizado e rastreavel:

- Inventario automatico de hardware via agentes
- Descoberta de rede (network discovery)
- Rastreamento de equipamentos por localizacao, usuario e estado
- Gestao do ciclo de vida de ativos
- Integracao com ferramentas de inventario (OCS Inventory, FusionInventory)

### Rastreamento de Licencas e Auditoria de Software

O GLPI ajuda a manter a conformidade de licencas e contratos de software:

- Controle de licencas de software e compliance
- Auditoria de software instalado
- Alertas de vencimento de licencas
- Gestao de contratos e garantias
- Relatorios de conformidade

### Deploy Containerizado pela EF-TECH

A EF-TECH entrega o GLPI pronto para producao com imagens Docker e Helm charts mantidos pela nossa equipe:

- Imagens Docker oficiais: `eftechcombr/glpi` no Docker Hub
- GLPI 11.0.7 com PHP 8.4 e Nginx
- Deploy via Docker Compose para ambientes locais e de teste
- Deploy via Kubernetes com Helm chart
- Helm chart repository: `helm repo add eftechcombr https://eftechcombr.github.io/glpi/`
- Instalacao simples: `helm install my-glpi eftechcombr/glpi`
- Arquitetura com PHP-FPM, Nginx, MariaDB e Redis
- Suporte a Ingress, Persistent Volumes e auto-scaling no Kubernetes
- Repositorio: https://github.com/eftechcombr/glpi

### Hosting e Suporte Gerenciado

Para quem prefere focar no negocio, a EF-TECH oferece hosting gerenciado completo do GLPI:

- Hosting gerenciado com monitoramento 24/7
- Portal de suporte disponivel em https://glpi.eftech.com.br
- Backup automatizado e disaster recovery
- Atualizacoes e patching gerenciados
- Suporte tecnico dedicado
- Configuracao personalizada de fluxos de trabalho e categorias

---

Interessado em GLPI para sua empresa? [Entre em contato](/pt-br/contato/) para uma consultoria personalizada.
