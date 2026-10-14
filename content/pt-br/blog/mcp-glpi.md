---
title: "mcp-glpi 3.4: conecte assistentes de IA ao GLPI com MCP"
description: "Conheça o mcp-glpi 3.4, servidor MCP que conecta assistentes de IA ao GLPI com OAuth2, 88 ferramentas e transporte stdio ou Streamable HTTP."
summary: "O mcp-glpi 3.4 oferece uma ponte estruturada entre clientes compatíveis com Model Context Protocol e o GLPI, cobrindo tickets, ITIL, ativos, estatísticas, busca multicritério e conexões multi-tenant."
date: 2026-10-14
draft: false
tags: ["glpi", "mcp", "ia", "model-context-protocol", "open-source", "typescript"]
categories: ["infraestrutura"]
featureimage: "/img/blog/mcp-glpi/featured.png"
featureimagecaption: "Diagrama conceitual da integração entre assistentes de IA, MCP e GLPI"
---

Equipes de service desk e operações acumulam informações em tickets, ativos,
problemas, mudanças e na base de conhecimento. Quando um assistente de IA não
consegue consultar essas informações de forma estruturada, o trabalho acaba
envolvendo cópia e colagem, consultas manuais e alternância entre ferramentas.

O **mcp-glpi** resolve a conexão entre esses dois mundos. Ele é um servidor do
[Model Context Protocol (MCP)](https://modelcontextprotocol.io/) que expõe o
GLPI a clientes compatíveis, como Claude Desktop, Claude Code e Cline. Assim,
o assistente pode utilizar as ferramentas disponibilizadas pelo servidor para
consultar e operar dados do GLPI, respeitando os sinais de segurança definidos
em cada ferramenta.

## MCP em poucas palavras

MCP é um protocolo para conectar assistentes de IA a sistemas externos por meio
de ferramentas e recursos descritos de maneira padronizada. O cliente MCP se
conecta ao servidor, descobre o que está disponível e pode solicitar uma ação
ou consulta conforme a conversa.

No caso do mcp-glpi, o sistema externo é uma instância do GLPI. O servidor
traduz as chamadas das ferramentas para a High-Level API v2.3 do GLPI, caminho
mantido estável para compatibilidade com GLPI 11 e GLPI 12, conforme o README do
projeto.

## O que o mcp-glpi 3.4 oferece

### 88 ferramentas para o ecossistema GLPI

A versão 3.4 reúne **88 ferramentas MCP** para tickets, problemas, mudanças,
ativos, base de conhecimento, contratos, fornecedores, locais, projetos,
usuários, grupos, categorias, entidades, documentos, pesquisa, estatísticas e
gerenciamento da conexão.

Também há recursos no formato `glpi://`, como tickets abertos e recentes,
problemas abertos, mudanças pendentes, computadores, grupos, categorias e
estatísticas de tickets e ativos.

### Tickets e cobertura ITIL

O conjunto de ferramentas de tickets cobre tanto leitura quanto operações do
ciclo de atendimento:

- listagem, detalhes e busca de tickets;
- timeline cronológica com acompanhamentos, tarefas, soluções e validações;
- tarefas com apontamento de horas e gerenciamento do ciclo de vida;
- atribuição a usuário ou grupo e vínculo entre tickets;
- solicitação, aprovação e recusa de validações;
- documentos vinculados e resultado de pesquisa de satisfação;
- identificação de tickets cujo prazo de SLA já foi ultrapassado.

O servidor também oferece ferramentas para listar, consultar, criar e atualizar
problemas e mudanças.

### Ativos e informações operacionais

Para gestão de ativos, o mcp-glpi cobre computadores, softwares, equipamentos
de rede, impressoras, monitores e telefones. Detalhes de computadores podem
incluir softwares, portas de rede, conexões e documentos.

Há ainda cobertura para artigos da base de conhecimento, contratos,
fornecedores, locais, projetos, usuários, grupos, categorias e entidades.

### Busca multicritério e estatísticas

A busca genérica usa filtros RSQL com `AND`, `OR`, `AND NOT` e `OR NOT`, além de
paginação, `forcedisplay` e `fetch_all`. A ferramenta de busca de tickets
oferece parâmetros mais diretos, como status, responsável, solicitante e
período.

Para análises, o servidor disponibiliza:

- contagem de tickets por status, com filtros opcionais de entidade e período;
- totais de ativos por tipo;
- distribuição de tickets por status, categoria, técnico, entidade ou mês;
- catálogo dos campos pesquisáveis;
- informações da sessão ativa.

As chaves estrangeiras são resolvidas por padrão nas visualizações de detalhes:
além do ID, o retorno pode trazer o nome legível. Isso reduz a necessidade de
consultas adicionais para interpretar responsáveis, grupos e outros vínculos.

## Segurança e validação antes da execução

As ferramentas carregam anotações MCP que ajudam o cliente a distinguir tipos
de operação. Consultas, listagens, buscas, contagens e estatísticas recebem
`readOnlyHint`; operações de atualização, exclusão, definição e atribuição
recebem `destructiveHint`.

As ferramentas de tickets também validam entradas em tempo de execução com
Zod. Em vez de deixar um parâmetro inválido chegar ao GLPI e produzir uma falha
menos clara, o servidor pode retornar um erro `InvalidParams` estruturado.

Na autenticação, a versão 3 usa OAuth2. São suportados `password grant`,
`client_credentials` e token `bearer`; a autenticação `app_token`/`user_token`
da API v2 não é suportada no v3. O cliente OAuth2 precisa ser configurado no
GLPI em **Setup → General → OAuth2 Client**, com o grant type apropriado.

## Cenários de uso

Os recursos do mcp-glpi permitem cenários como:

- **Service desk:** localizar tickets por status, responsável, solicitante ou
  período e consultar a timeline completa antes de registrar um acompanhamento,
  tarefa ou solução.
- **Operações:** identificar tickets com SLA vencido, distribuir chamados por
  técnico ou entidade e consultar estatísticas por mês, status ou categoria.
- **Gestão de ativos:** consultar um computador com seus softwares, conexões e
  documentos, ou verificar os totais do inventário por tipo de ativo.
- **Gestão de mudanças e problemas:** consultar itens em andamento e usar as
  ferramentas de criação, atualização, validação e acompanhamento disponíveis
  no GLPI.
- **Conhecimento e atendimento:** buscar artigos da base de conhecimento e
  relacioná-los ao contexto de um atendimento, sem sair do cliente MCP.

Esses cenários descrevem o que as ferramentas permitem fazer; os dados e as
permissões efetivamente disponíveis continuam dependendo da instância do GLPI,
do perfil e da entidade usados na conexão.

## Configuração rápida com `bunx`

O servidor pode ser iniciado pelo cliente MCP com `bunx`. O exemplo abaixo usa
valores fictícios e não deve ser preenchido com credenciais no controle de
versão:

```json
{
  "mcpServers": {
    "glpi": {
      "command": "bunx",
      "args": ["mcp-glpi"],
      "env": {
        "GLPI_URL": "https://glpi.example.com",
        "GLPI_AUTH_METHOD": "password",
        "GLPI_USERNAME": "seu_usuario",
        "GLPI_PASSWORD": "sua_senha",
        "GLPI_CLIENT_ID": "seu_client_id"
      }
    }
  }
}
```

`GLPI_URL` deve ser a URL base sem barra final. Dependendo de
`GLPI_AUTH_METHOD`, são usadas as variáveis correspondentes para password
grant, client credentials ou bearer token. O README também documenta opções
como `GLPI_CLIENT_SECRET`, `GLPI_TIMEOUT_MS`, `GLPI_MAX_RETRIES`,
`GLPI_ENTITY_ID`, `GLPI_PROFILE_ID` e `GLPI_ENTITY_RECURSIVE`.

## Executando com Docker

Para usar a imagem publicada no GitHub Container Registry:

```bash
docker pull ghcr.io/eftechcombr/mcp-glpi:latest

docker run -i --rm \
  --env-file /caminho/absoluto/.env \
  ghcr.io/eftechcombr/mcp-glpi:latest
```

O `.env` deve conter a URL do GLPI e as credenciais OAuth2 correspondentes. O
servidor não precisa de dados persistentes em disco para a operação normal.
Além disso, a imagem executa com o usuário não-root `bunuser:1001`.

Ao configurar o Docker como processo iniciado por um cliente MCP, mantenha o
stdin aberto com **`-i`**. Não use **`-t`**: o TTY pode corromper o fluxo do
protocolo MCP stdio. Uma configuração equivalente no cliente é:

```json
{
  "mcpServers": {
    "glpi": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "--env-file", "/caminho/absoluto/.env",
        "ghcr.io/eftechcombr/mcp-glpi:latest"
      ]
    }
  }
}
```

O transporte **stdio** é apropriado quando o cliente inicia o servidor como um
subprocesso e troca mensagens JSON-RPC por entrada e saída padrão. Para um
servidor acessível pela rede, o mcp-glpi também oferece **Streamable HTTP**.

## Streamable HTTP e modo multi-tenant

Defina `MCP_TRANSPORT=http` para executar o servidor HTTP. As principais
variáveis desse modo são `HOST`, `PORT`, `MCP_PATH` e `SESSION_TTL_MS`; o
endpoint padrão é `/mcp` e há endpoints de saúde em `/health` e `/`.

Em modo single-tenant, `GLPI_URL` e as variáveis de autenticação são definidas
no ambiente do servidor. Em modo **multi-tenant**, `GLPI_URL` fica vazio e cada
cliente configura a própria conexão na sessão usando `glpi_configure_connection`.
As credenciais ficam apenas em memória, não são registradas em logs e são
revogadas quando a sessão termina ou expira.

Exemplo de conexão de um cliente MCP via HTTP:

```json
{
  "mcpServers": {
    "glpi": {
      "type": "streamable-http",
      "url": "https://glpi.example.com/mcp"
    }
  }
}
```

No modo multi-tenant, a sequência inicial documentada pelo projeto é consultar
`glpi_connection_status`, chamar `glpi_configure_connection` com a URL, o
método OAuth2 e as credenciais correspondentes, e então usar as ferramentas.
Se houver um proxy reverso, o README recomenda encaminhar o caminho MCP com o
buffering SSE desabilitado e propagar os cabeçalhos `Host` e `X-Forwarded-*`.

## Conclusão

O mcp-glpi 3.4 cria uma interface padronizada para que assistentes compatíveis
com MCP consultem e operem informações do GLPI. Com 88 ferramentas, cobertura
de tickets e ITIL, busca multicritério, estatísticas, validação de entrada,
anotações de segurança, OAuth2 e suporte a stdio ou Streamable HTTP multi-tenant,
ele atende desde uma configuração local até um serviço HTTP compartilhado por
sessões.

Consulte o [repositório oficial do mcp-glpi no GitHub](https://github.com/eftechcombr/mcp-glpi),
o [pacote no npm](https://www.npmjs.com/package/mcp-glpi), a
[documentação da High-Level API do GLPI](https://glpi-user-documentation.readthedocs.io/)
e a [documentação oficial do Model Context Protocol](https://modelcontextprotocol.io/)
para experimentar o projeto. Para conhecer o GLPI e as opções de implantação
da EF-TECH, veja também nossa página de [produto GLPI](/pt-br/produtos/glpi/).

Na EF-TECH, trabalhamos com GLPI, cloud computing e infraestrutura de TI. Se
você precisa avaliar esse tipo de integração no seu ambiente, [entre em
contato](/pt-br/contato/) para conversar com nossa equipe.
