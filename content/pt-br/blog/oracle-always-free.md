---
title: "Oracle Cloud Always Free: recursos gratuitos para sempre"
description: "Conheça todos os recursos do Oracle Cloud Infrastructure (OCI) disponíveis gratuitamente por tempo ilimitado — compute, banco de dados, armazenamento e rede."
summary: "O Oracle Cloud Infrastructure (OCI) oferece um conjunto generoso de recursos Always Free que incluem instâncias AMD e ARM, banco de dados autônomo, 200 GB de block storage, load balancer e muito mais. Veja tudo que você pode provisionar sem pagar nada."
date: 2026-06-19
draft: false
tags: ["oracle", "oci", "cloud-computing", "infraestrutura"]
categories: ["cloud-computing"]
---

O Oracle Cloud Infrastructure (OCI) oferece um dos programas **Always Free** mais generosos entre os grandes provedores de nuvem. Diferente de trials que expiram após 30 ou 90 dias, os recursos do Always Free estão disponíveis **por tempo ilimitado** na região *home* da sua conta.

Se você está começando um projeto pessoal, fazendo provas de conceito ou estudando cloud computing, este guia detalha todos os recursos que você pode usar sem custo.

## Compute

O OCI oferece duas opções de instâncias Always Free:

### VM.Standard.E2.1.Micro (AMD)

- **Processador:** 1/8 de um OCPU AMD (com burst)
- **Memória:** 1 GB
- **Rede:** 1 VNIC com 1 IP público, até 50 Mbps (internet) ou 480 Mbps (tráfego interno na região)
- **Imagens:** Oracle Linux, Oracle Linux Cloud Developer, Ubuntu, CentOS
- **Limite:** até 2 instâncias por conta

### VM.Standard.A1.Flex (ARM — Ampere)

- **Processador:** até 2 OCPUs no total (configurável: 1 instância com 2 OCPUs ou 2 instâncias com 1 OCPU cada)
- **Memória:** até 12 GB no total
- **Rede:** largura de banda e VNICs escalam com o número de OCPUs
- **Imagens:** Oracle Linux, Oracle Linux Cloud Developer, Ubuntu
- **Limite:** 1.500 horas OCPU e 9.000 GB-hora por mês

> ⚠️ **Instâncias ociosas podem ser recuperadas.** Se por 7 dias consecutivos o uso de CPU for inferior a 20%, rede inferior a 20% e memória inferior a 20% (A1 apenas), a Oracle pode desligar a instância.

## Armazenamento

### Block Volume

- **200 GB** totais combinados entre boot volumes e block volumes
- **5 backups** de volume simultâneos
- O boot volume padrão de cada instância consome 50 GB desse total
- Volumes Always Free devem ser criados na região *home*

### Object Storage

- **20 GB** combinados entre Standard, Infrequent Access e Archive
- **50.000 requisições** por mês à API de Object Storage

## Banco de Dados

### Oracle Autonomous AI Database

- **2 instâncias** Always Free por tenancy
- **1 OCPU** e **20 GB de armazenamento** por instância
- Workloads suportadas: Transaction Processing, JSON Database, APEX Application Development e Lakehouse
- **20 sessões** simultâneas por banco

### Oracle NoSQL Database

- Até **133 milhões de leituras** por mês
- Até **133 milhões de escritas** por mês
- **3 tabelas** com **25 GB** cada

### Oracle MySQL HeatWave

- **1 DB system** standalone com HeatWave
- **50 GB** de armazenamento para dados + **50 GB** para backups

## Rede

### Virtual Cloud Network (VCN)

- Até **2 VCNs** por tenancy (contas Free Tier)
- Suporte a IPv4 e IPv6

### Load Balancer

- **1 Load Balancer Flexible** (10 Mbps mín/máx) — contas criadas a partir de 15/12/2020
- Contas anteriores: 1 Load Balancer Micro (10 Mbps)
- Suporte a até 16 listeners e 1.024 backends

### Network Load Balancer

- **1 NLB** Always Free
- Até 50 listeners, 50 backend sets, 1.024 backends no total

### Site-to-Site VPN

- Até **50 conexões IPSec**

### VCN Flow Logs

- **10 GB por mês** de logs compartilhados com o serviço de Logging

## Observability & Management

- **Monitoring:** 500 milhões de pontos de ingestão + 1 bilhão de pontos de consulta
- **Application Performance Monitoring:** 1.000 eventos de tracing e 10 execuções de Synthetic Monitor por hora
- **Connector Hub:** 2 conectores Always Free
- **Notifications:** 1 milhão de notificações HTTPS e 1.000 e-mails por mês
- **Logging:** incluído, compartilha os 10 GB mensais com VCN Flow Logs
- **Console Dashboards:** 100 dashboards por tenancy
- **Email Delivery:** 3.000 e-mails por mês
- **Fleet Application Management:** gerenciamento de lifecycle dos primeiros 25 recursos por mês

## Segurança

- **Vault:** chaves criptográficas por software (ilimitadas) + 20 versões de chaves HSM + 150 secrets
- **Bastion:** acesso SSH restrito e temporário — **gratuito** para todos os tipos de conta

## Outros Serviços

- **Certificates:** 5 CAs e 150 certificados
- **Cluster Placement Groups:** 10 a 50 grupos por região
- **Resource Manager:** 100 stacks, 100 templates, 100 configuration source providers, 2 jobs simultâneos
- **Outbound Data Transfer:** **10 TB por mês** de tráfego de saída

## Dicas Importantes

1. **Região *home* é obrigatória:** recursos Always Free como block volume e instâncias só são gratuitos na região *home* da sua conta.
2. **Monitore seus limites:** acesse **Governance & Administration → Limits, Quotas and Usage** no Console OCI para ver seus limites atuais.
3. **Upgrade não cancela o Always Free:** se você fizer upgrade para conta paga, os recursos Always Free continuam gratuitos — você paga apenas pelo que usar além dos limites.
4. **Instâncias ociosas são recuperadas:** mantenha suas instâncias com atividade mínima para evitar perda.
5. **Use Resource Manager para provisionamento rápido:** o OCI templates permitem criar todo o conjunto Always Free em poucos minutos via Terraform.

## Conclusão

O Oracle Cloud Always Free é uma excelente opção para projetos pessoais, laboratórios de estudo e provas de conceito. Com instâncias AMD e ARM, banco de dados autônomo, 200 GB de armazenamento e 10 TB de transferência mensal, você tem poder computacional suficiente para rodar aplicações reais sem se preocupar com cobranças.

Na **EF-TECH**, temos experiência em projetos na Oracle Cloud e podemos ajudar sua empresa a planejar e executar migrações para o OCI com foco em economia e boas práticas. [Entre em contato](/pt-br/contato/) para saber mais.
