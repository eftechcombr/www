---
title: "MCP-GLPI: integre assistentes de IA com o GLPI via Model Context Protocol"
description: "Conheça o mcp-glpi, um servidor MCP que expõe todo o ecossistema GLPI — tickets, ativos, usuários, KB e muito mais — para assistentes de IA como Claude, Cline e VS Code."
summary: "A EF-TECH lança o mcp-glpi, um servidor MCP (Model Context Protocol) que permite que assistentes de IA interajam diretamente com o GLPI via 84 ferramentas e 9 recursos, cobrindo tickets, ativos, problemas, mudanças, base de conhecimento, contratos e muito mais."
date: 2026-07-10
draft: false
tags: ["glpi", "mcp", "ia", "model-context-protocol", "open-source", "typescript"]
categories: ["infraestrutura"]
featureimage: "/img/blog/mcp-glpi/featured.svg"
featureimagecaption: "Diagrama conceitual do MCP-GLPI integrando assistentes de IA ao GLPI"
---

A EF-TECH tem o prazer de anunciar o **mcp-glpi**, um servidor open-source que implementa o [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) para expor todo o ecossistema GLPI a assistentes de IA como Claude, Cline, GitHub Copilot e qualquer outro cliente compatível com MCP.

![MCP-GLPI: integração entre IA e GLPI](/img/blog/mcp-glpi/featured.svg)

## O que é o MCP-GLPI?

O MCP (Model Context Protocol) é um protocolo aberto padronizado pela Anthropic que permite que assistentes de IA se conectem a sistemas externos de forma segura e estruturada. O **mcp-glpi** é a ponte entre esse protocolo e o GLPI — o software livre de gestão de serviços de TI (ITSM) mais utilizado no Brasil.

Com ele, você pode pedir em linguagem natural para um assistente de IA:

- "Liste os tickets abertos de alta urgência"
- "Crie um chamado informando que o servidor de banco está com 95% de uso de CPU"
- "Mostre os dados do computador do João"
- "Qual o total de ativos no inventário?"
- "Adicione um acompanhamento no ticket #42 informando que o problema foi resolvido"

Tudo isso sem sair do seu assistente de IA favorito.

## Principais funcionalidades

O servidor expõe **84 ferramentas MCP** e **9 recursos** organizados nas seguintes categorias:

### Gestão de Tickets (ITIL completo)

| Área | Ferramentas |
|---|---|
| Leitura | Listar, obter detalhes, timeline, acompanhamentos, tarefas, soluções, validações, documentos, satisfação, tickets em atraso (SLA) |
| Escrita | Criar, atualizar, deletar, adicionar acompanhamento, adicionar tarefa com apontamento de horas, adicionar solução, atribuir ticket, vincular tickets, solicitar validação, aprovar/recusar validação, anexar documento |

### Problemas e Mudanças

- Listar, obter, criar e atualizar problemas
- Listar, obter, criar e atualizar mudanças

### Gestão de Ativos

- **Computadores**: listar, obter (com software, portas de rede, conexões, documentos), criar, atualizar e deletar
- **Softwares**: listar, obter e criar
- **Equipamentos de rede**: listar, obter e criar
- **Impressoras**: listar, obter e criar
- **Monitores**: listar, obter e criar
- **Telefones**: listar, obter e criar

### Base de Conhecimento, Contratos, Fornecedores e Locais

- Listar, obter e criar artigos na base de conhecimento (com busca textual)
- Listar, obter e criar contratos, fornecedores, locais e projetos

### Usuários, Grupos e Categorias

- Listar usuários, buscar por login, criar usuário
- Listar e criar grupos, adicionar usuário a grupo
- Listar categorias de tickets
- Listar entidades

### Estatísticas e Introspecção

- Contagem de tickets por status (com filtro por entidade/período)
- Totais de ativos por tipo
- Distribuição de tickets por status, categoria, técnico, entidade ou mês
- Catálogo de campos pesquisáveis
- Informações da sessão ativa

### Recursos (Resources)

Além das ferramentas, o servidor expõe recursos no formato `glpi://`:

- `glpi://tickets/open` — tickets abertos
- `glpi://tickets/recent` — tickets recentes
- `glpi://problems/open` — problemas abertos
- `glpi://changes/pending` — mudanças pendentes
- `glpi://computers` — computadores
- `glpi://groups` — grupos
- `glpi://categories` — categorias
- `glpi://stats/tickets` — estatísticas de tickets
- `glpi://stats/assets` — estatísticas de ativos

## Tecnologia

O mcp-glpi é construído com **TypeScript** e executado com **Bun**, oferecendo:

- **Autenticação OAuth2** com suporte a `password grant`, `client_credentials` e `bearer token`
- **Camada HTTP unificada** com reautenticação automática em 401, retry em 5xx/429 e timeouts configuráveis
- **Busca multicritério** com filtros RSQL (`AND`/`OR`/`AND NOT`/`OR NOT`), paginação e `fetch_all`
- **Mapeamento dinâmico de campos** — as traduções entre `field_id` e nome são cacheadas com TTL de 1 hora
- **Chaves estrangeiras resolvidas** — detalhes retornam o ID e o nome legível, sem necessidade de consultas adicionais
- **Validação de entrada em runtime** com Zod — erros claros em vez de falhas no GLPI
- **Anotações de segurança** — `readOnlyHint` em ferramentas de consulta, `destructiveHint` em operações de escrita/exclusão
- **Imagem Docker** baseada em `oven/bun:1-alpine`, executando como usuário não-root (`bunuser:1001`)

## Como usar

### Com Claude Desktop / Claude Code

Adicione ao seu `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "glpi": {
      "command": "bunx",
      "args": ["mcp-glpi"],
      "env": {
        "GLPI_URL": "https://glpi.sua-empresa.com",
        "GLPI_AUTH_METHOD": "password",
        "GLPI_USERNAME": "seu_usuario",
        "GLPI_PASSWORD": "sua_senha",
        "GLPI_CLIENT_ID": "seu_client_id"
      }
    }
  }
}
```

### Com Docker

```bash
docker pull ghcr.io/eftechcombr/mcp-glpi:1.0

docker run -i --rm \
  -e GLPI_URL="https://glpi.sua-empresa.com" \
  -e GLPI_AUTH_METHOD="password" \
  -e GLPI_USERNAME="seu_usuario" \
  -e GLPI_PASSWORD="sua_senha" \
  -e GLPI_CLIENT_ID="seu_client_id" \
  ghcr.io/eftechcombr/mcp-glpi:1.0
```

### Pré-requisitos

1. Uma instância do GLPI (versão 10 ou 11) com acesso à API
2. Um cliente OAuth2 configurado no GLPI (Setup → General → OAuth2 Client)
3. Um dos assistentes de IA compatíveis com MCP (Claude, Cline, Continue, etc.)

## Por que lançamos isso?

Na EF-TECH, trabalhamos diariamente com GLPI — seja na operação de service desk dos nossos clientes, seja no desenvolvimento de imagens Docker e Helm Charts para deploy containerizado.

Percebemos que os assistentes de IA estão cada vez mais presentes no dia a dia de times de TI, mas ainda falta uma conexão direta entre eles e as ferramentas de gestão. O mcp-glpi preenche exatamente essa lacuna: em vez de copiar e colar informações manualmente, o assistente de IA consulta e registra dados diretamente no GLPI.

## O que vem por aí?

O servidor já está funcional e em uso, mas temos vários planos para evolução:

- Suporte a workflow de aprovação de mudanças
- Ferramentas para relatórios personalizados
- Melhorias na cobertura de ativos (dispositivos de rede, baterias, etc.)
- Integração com mais assistentes e IDEs

## Contribua

O mcp-glpi é **open-source** sob licença MIT e está disponível no GitHub:

🔗 [https://github.com/eftechcombr/mcp-glpi](https://github.com/eftechcombr/mcp-glpi)

Contribuições são bem-vindas! Issues, pull requests e sugestões estão abertos para a comunidade.

## Links úteis

- [Repositório no GitHub](https://github.com/eftechcombr/mcp-glpi)
- [Pacote no NPM](https://www.npmjs.com/package/mcp-glpi)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [GLPI Project](https://glpi-project.org/)
- [Documentação da API GLPI](https://glpi-user-documentation.readthedocs.io/)

---

Na **EF-TECH**, somos especialistas em GLPI, cloud computing e infraestrutura de TI. Oferecemos suporte especializado para implantação, manutenção e integração do GLPI com ferramentas modernas. [Entre em contato](/pt-br/contato/) para saber como podemos ajudar sua equipe.
