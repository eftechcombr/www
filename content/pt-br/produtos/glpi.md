---
title: "GLPI"
description: "GLPI - software livre de gestão de ativos de TI e service desk ITIL com deploy containerizado pela EF-TECH"
summary: "GLPI é um software livre de gestão de ativos de TI e service desk ITIL. A EF-TECH oferece deploy containerizado via Docker e Kubernetes com Helm chart, hosting gerenciado e suporte dedicado."
date: 2026-06-19
tags: ["glpi", "service-desk", "itil", "inventario", "kubernetes"]
categories: ["produtos"]
---
## GLPI

GLPI (Gestionnaire Libre de Parc Informatique) é um software livre de gestão de ativos de TI e service desk ITIL. Como solução open source, oferece recursos para inventário de hardware e software, abertura e controle de chamados, rastreamento de licenças e auditoria de software. O projeto é mantido pela comunidade no [GitHub](https://github.com/glpi-project/glpi) e distribuído sob licença GPL-3.0. A EF-TECH especializa-se no deploy containerizado e no hosting gerenciado do GLPI, levando a versatilidade do software livre para ambientes de produção robustos e seguros.

### Service Desk ITIL

O GLPI implementa os processos ITIL para service desk, permitindo centralizar e organizar todo o atendimento de TI:

- Gestão de incidentes e problemas
- Gestão de mudanças
- Acordos de Nível de Serviço (SLA) e escalonamento
- Base de conhecimento (knowledge base)
- Catálogo de serviços
- Formulários de solicitação de serviço (service catalog)

### Gestão de Ativos e Inventário

A gestão de ativos do GLPI mantém o inventário de TI sempre atualizado e rastreável:

- Inventário automático de hardware via agentes
- Descoberta de rede (network discovery)
- Rastreamento de equipamentos por localização, usuário e estado
- Gestão do ciclo de vida de ativos
- Integração com ferramentas de inventário (OCS Inventory, FusionInventory)

### Rastreamento de Licenças e Auditoria de Software

O GLPI ajuda a manter a conformidade de licenças e contratos de software:

- Controle de licenças de software e compliance
- Auditoria de software instalado
- Alertas de vencimento de licenças
- Gestão de contratos e garantias
- Relatórios de conformidade

### Deploy Containerizado pela EF-TECH

A EF-TECH entrega o GLPI pronto para produção com imagens Docker e Helm charts mantidos pela nossa equipe:

- Imagens Docker oficiais: `eftechcombr/glpi` no Docker Hub
- GLPI 11.0.7 com PHP 8.4 e Nginx
- Deploy via Docker Compose para ambientes locais e de teste
- Deploy via Kubernetes com Helm chart
- Helm chart repository: `helm repo add eftechcombr https://eftechcombr.github.io/glpi/`
- Instalação simples: `helm install my-glpi eftechcombr/glpi`
- Arquitetura com PHP-FPM, Nginx, MariaDB e Redis
- Suporte a Ingress, Persistent Volumes e auto-scaling no Kubernetes
- Repositorio: https://github.com/eftechcombr/glpi

### Hosting e Suporte Gerenciado

Para quem prefere focar no negocio, a EF-TECH oferece hosting gerenciado completo do GLPI:

- Hosting gerenciado com monitoramento 24/7
- Portal de suporte disponivel em https://glpi.eftech.com.br
- Backup automatizado e disaster recovery
- Atualizações e patching gerenciados
- Suporte técnico dedicado
- Configuração personalizada de fluxos de trabalho e categorias

---

Interessado em GLPI para sua empresa? [Entre em contato](/pt-br/contato/) para uma consultoria personalizada.
