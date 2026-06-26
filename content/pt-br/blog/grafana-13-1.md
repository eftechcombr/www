---
title: "Grafana 13.1: Novidades em observability as code, Grafana Assistant e mais"
description: "A Grafana 13.1 chegou com Git Sync GA, Grafana Assistant expandido para 8 novas fontes de dados e melhorias significativas em dashboards. Confira o que muda."
summary: "A Grafana 13.1 traz Git Sync em GA com commits assinados, suporte do Grafana Assistant a bancos como Oracle e MongoDB, variáveis por seção, editor de queries reformulado e novos data sources no PDC. Um resumo prático para quem trabalha com observabilidade no dia a dia."
date: 2026-06-26
draft: false
tags: ["grafana", "observabilidade", "monitoramento", "devops"]
categories: ["infraestrutura"]
---

A Grafana Labs lançou a versão 13.1, dando continuidade ao ciclo iniciado com a Grafana 13, que trouxe o Git Sync como funcionalidade estável e disponível para todos. Esta versão é particularmente relevante para equipes que adotam observability as code, dependem de dashboards dinâmicos com múltiplos serviços ou precisam conectar fontes de dados on-premise de forma segura.

A seguir, um resumo das principais novidades organizadas por área de interesse.

## Git Sync: Observability as Code amadurece

O Git Sync, que atingiu GA (disponibilidade geral) na versão 13, continua recebendo melhorias importantes na 13.1. Para quem gerencia dashboards como código, esta é a funcionalidade central da release.

### Importação de dashboards em pastas provisionadas (GA)

Agora é possível importar dashboards diretamente para pastas gerenciadas por provisionamento. Na prática, isso significa que você pode definir a estrutura de pastas via arquivos de configuração e ter os dashboards sincronizados do Git já no local correto, sem intervenção manual.

### Sincronização no nível raiz (GA)

O suporte a sincronização a partir da raiz do repositório elimina a necessidade de estruturas de diretório específicas. Basta configurar o caminho desejado e o Grafana interpreta a organização natural do seu repositório.

### README.md em pastas Git Sync (public preview)

Pastas sincronizadas via Git Sync agora exibem o arquivo `README.md` do repositório diretamente no Grafana. Isso facilita a documentação in-line de cada conjunto de dashboards, especialmente em equipes que mantêm múltiplos repositórios de observabilidade.

### Commits assinados com GPG, SSH e S/MIME (GA)

Toda alteração feita via Git Sync pode ser assinada digitalmente, garantindo rastreabilidade e conformidade. O suporte cobre GPG, SSH e S/MIME, atendendo desde times pequenos até ambientes corporativos com políticas rigorosas de auditoria.

### Integração com GitHub App, GitLab, BitBucket

O Git Sync suporta autenticação via GitHub App (recomendado para organizações que usam GitHub), além de GitLab e BitBucket, e também conexão pura via Git. Isso cobre a maioria dos cenários de mercado.

## Grafana Assistant ganha 8 novos data sources

O assistente baseado em IA do Grafana, que ajuda na criação de queries e interpretação de métricas, foi expandido para suportar oito novas fontes de dados:

- **Snowflake** — data warehouse na nuvem
- **Oracle** — banco de dados relacional corporativo
- **Elasticsearch** — busca e análise de logs
- **Dynatrace** — monitoramento de performance de aplicações
- **Honeycomb** — observabilidade orientada a eventos
- **Zabbix** — monitoramento de infraestrutura open source
- **Jira** — gerenciamento de projetos e tickets
- **MongoDB** — banco NoSQL

### Disponibilidade

O Grafana Assistant vem **pré-instalado no Grafana Enterprise** (não requer plugin adicional). Para usuários da versão OSS, está disponível como plugin no catálogo, exigindo uma conta Grafana Cloud.

Para o mercado brasileiro, o suporte a Oracle, Zabbix e MongoDB é particularmente interessante, já que são tecnologias com presença significativa em ambientes corporativos e provedores de serviços por aqui.

## Melhorias em dashboards

A experiência de criação e uso de dashboards recebeu várias atualizações na 13.1.

### Variáveis por seção (GA)

Esta é uma das funcionalidades mais pedidas pela comunidade. Antes, variáveis como `$service` ou `$environment` tinham escopo global no dashboard. Agora é possível definir **variáveis no nível de linhas e abas**, permitindo que cada seção do dashboard tenha seu próprio contexto.

Exemplo prático: em um dashboard que monitora produção e homologação lado a lado, você pode ter uma variável `$service` diferente para cada linha, sem conflitos.

### Editor de queries reformulado (public preview)

O editor de queries foi redesenhado com foco em produtividade:

- **Seleção múltipla e ações em lote** — selecione várias queries de uma vez para editar, duplicar ou remover
- **Visão empilhada** — visualização lado a lado das queries abertas, facilitando a comparação

Para times que mantêm dashboards com dezenas de painéis, a economia de tempo é significativa.

### Filtros rápidos e agrupamento de dados (GA)

Os quick filters permitem aplicar filtros ad-hoc sem modificar as queries subjacentes. O agrupamento de dados agora é estável e funciona diretamente na interface, simplificando a criação de visões agregadas.

### Visibilidade de séries em legendas de séries temporais

A legenda dos gráficos de série temporal agora inclui um controle de visibilidade por série. Isso permite ocultar ou exibir linhas individualmente, útil em dashboards com múltiplas métricas sobrepostas.

### Tabelas aninhadas melhoradas

As tabelas aninhadas (nested tables) receberam melhorias em:

- **Agrupamento configurável** — defina como os dados são agrupados dentro de cada célula
- **Estilização de células** — formatação condicional com cores e estilos
- **Agregações aprimoradas** — novas funções de agregação para sumarizar dados aninhados

### Copiar e colar estilos de painel (GA)

Finalmente é possível copiar a configuração de estilo de um painel e aplicar em outro, sem precisar reconfigurar manualmente cores, thresholds e formatação.

### Presets de estilo de painel (GA)

O Grafana 13.1 inclui presets de estilo — combinações curadas de cores, thresholds e formatação para tipos comuns de painel (gráficos de barra, medidores, tabelas, etc.). Isso acelera a criação de dashboards com aparência consistente.

## PDC (Private Data Source Connect): novos data sources

O PDC, que permite conexões seguras via túnel criptografado para fontes de dados em redes privadas, ganhou suporte a três novos tipos:

- **MQTT** — protocolo IoT (Internet das Coisas)
- **GitHub** — API do GitHub para métricas de repositórios
- **IBM Db2** — banco de dados relacional da IBM

Essas adições ampliam o alcance do PDC para cenários de IoT, integração com DevOps e bancos corporativos legados, mantendo todo o tráfego criptografado entre o Grafana e a fonte de dados.

## Conclusão

A Grafana 13.1 consolida o Git Sync como ferramenta madura para observability as code, expande o alcance do assistente de IA para fontes de dados muito utilizadas no mercado brasileiro e entrega melhorias práticas no dia a dia de quem constrói e mantém dashboards.

Para quem utiliza Grafana Enterprise, o destaque fica com o Grafana Assistant já incluso, sem necessidade de plugins adicionais. Para usuários OSS, as melhorias em Git Sync, variáveis por seção e editor de queries são os motivos mais fortes para atualizar.

Na EF-TECH, ajudamos empresas a implementar e gerenciar soluções de observabilidade com Grafana. [Entre em contato](/pt-br/contato/).
