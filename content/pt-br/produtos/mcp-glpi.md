---
title: "mcp-glpi"
description: "mcp-glpi v3.4: servidor MCP para conectar assistentes de IA ao GLPI com OAuth2, 88 ferramentas e suporte a GLPI 11 e 12."
summary: "Conecte assistentes de IA ao GLPI com 88 ferramentas para tickets, ITIL, ativos, busca RSQL e estatísticas. A EF-TECH apoia avaliação, implantação e operação."
date: 2026-10-14
tags: ["mcp-glpi", "glpi", "mcp", "ia", "service-desk", "open-source"]
categories: ["produtos"]
---
## mcp-glpi

O **mcp-glpi v3.4** é um servidor do [Model Context Protocol (MCP)](https://modelcontextprotocol.org/) que conecta assistentes de IA compatíveis ao GLPI. Ele é baseado no projeto upstream [GMS64260/mcp-glpi](https://github.com/GMS64260/mcp-glpi) e expõe ferramentas padronizadas para consultar e operar tickets, ativos, problemas, mudanças e outros recursos do GLPI.

O projeto utiliza o caminho estável da **High-Level API v2.3**, compatível com GLPI 11 e GLPI 12. A EF-TECH pode apoiar a avaliação do caso de uso, a implantação e a operação da integração, de acordo com o ambiente e os requisitos da organização.

### Cobertura para service desk e operações

São **88 ferramentas MCP** para as principais áreas operacionais do GLPI:

- Tickets, acompanhamentos, tarefas, soluções, validações e SLA
- Problemas e mudanças
- Computadores, softwares, equipamentos de rede, impressoras, monitores e telefones
- Base de conhecimento, contratos, fornecedores, locais e projetos
- Usuários, grupos, categorias, entidades e documentos
- Busca multicritério, contagens e estatísticas

As ferramentas de tickets incluem timeline cronológica, atribuição a usuários ou grupos, vínculo entre tickets, solicitações de validação e ciclo de vida de tarefas com apontamento de horas. Isso permite usar assistentes de IA para consultar contexto operacional e executar ações no GLPI, respeitando as permissões e a configuração da instância.

### Busca e visibilidade operacional

A busca multicritério aceita filtros RSQL com operadores `AND`, `OR`, `AND NOT` e `OR NOT`, além de seleção de campos, paginação, busca de todos os resultados e uma consulta dedicada de contagem. O mapeamento dinâmico dos campos pesquisáveis ajuda a manter a integração válida entre versões do GLPI. A busca de tickets possui parâmetros diretos para status, responsável, solicitante e período.

O servidor também pode apresentar estatísticas por status, categoria, técnico, entidade ou mês, totais de ativos por tipo e tickets cujo prazo de SLA foi ultrapassado. Nas respostas de detalhe, chaves estrangeiras podem retornar tanto o ID quanto o nome legível relacionado.

### Segurança e autenticação OAuth2

As ferramentas incluem anotações MCP de segurança para distinguir operações de leitura e alteração. Listagens, consultas, buscas, contagens e estatísticas recebem `readOnlyHint`; operações de atualização, exclusão, definição e atribuição recebem `destructiveHint`. As ferramentas de tickets também usam validação de entrada em tempo de execução com Zod e retornam erros `InvalidParams` estruturados quando os parâmetros são inválidos.

O mcp-glpi v3 usa OAuth2 com `password`, `client_credentials` ou token `bearer`. A autenticação baseada em `app_token` e `user_token` da API v2 **não é suportada na v3**. É necessário configurar no GLPI um cliente OAuth2 com o grant apropriado e fornecer as credenciais por variáveis de ambiente ou pela configuração da sessão HTTP. Consulte o README do projeto para a tabela completa de variáveis e os requisitos de cada método.

### Transporte: stdio ou Streamable HTTP

No modo **stdio**, o cliente MCP inicia o servidor como subprocesso e troca mensagens pelo stdin/stdout. É o modo adequado para integrações locais ou um container iniciado pelo próprio cliente. Com Docker, mantenha `-i` para preservar o stdin e **não use `-t`**, pois um TTY pode corromper o fluxo do protocolo:

```bash
docker pull ghcr.io/eftechcombr/mcp-glpi:latest
docker run -i --rm --env-file /caminho/absoluto/.env \
  ghcr.io/eftechcombr/mcp-glpi:latest
```

No modo **Streamable HTTP**, o servidor atende conexões de rede. Configure `MCP_TRANSPORT=http` e publique a porta do serviço:

```bash
docker run -d --name mcp-glpi-http -p 3000:3000 \
  -e MCP_TRANSPORT=http -e PORT=3000 \
  ghcr.io/eftechcombr/mcp-glpi:latest
```

O endpoint MCP padrão é `/mcp`; `/health` e `/` fornecem endpoints de saúde. Em um proxy reverso, o caminho `/mcp` precisa encaminhar o streaming sem buffering de SSE.

O Streamable HTTP pode operar em dois modelos:

- **Single-tenant:** `GLPI_URL` e as variáveis de autenticação definem uma instância para as sessões.
- **Multi-tenant:** `GLPI_URL` fica sem definição e cada sessão configura sua própria conexão com `glpi_configure_connection`. As credenciais ficam somente em memória e são removidas quando a sessão termina ou expira.

No modo multi-tenant, o cliente consulta `glpi_connection_status`, chama `glpi_configure_connection` com a URL, o método OAuth2 e as credenciais correspondentes, e então usa as ferramentas normalmente.

### Como a EF-TECH pode apoiar

A EF-TECH pode apoiar a avaliação do uso de IA no service desk, a configuração do GLPI e do cliente MCP, a execução containerizada e a operação do serviço. O escopo é definido conforme a arquitetura, as permissões e os requisitos de segurança do ambiente.

Consulte o [repositório do mcp-glpi no GitHub](https://github.com/eftechcombr/mcp-glpi) e o [projeto upstream](https://github.com/GMS64260/mcp-glpi) para a configuração completa, o catálogo de ferramentas e os detalhes de desenvolvimento.

---

Quer conectar IA ao GLPI da sua empresa? [Entre em contato](/pt-br/contato/) para conversar com nossa equipe.
