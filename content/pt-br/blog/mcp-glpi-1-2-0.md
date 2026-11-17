---
title: "mcp-glpi v1.2.0: High-Level API v3.0 do GLPI como padrão, com compatibilidade v2.x"
description: "O mcp-glpi v1.2.0 (npm 3.5.0) passa a usar a High-Level API v3.0 do GLPI 12 por padrão, adiciona a variável GLPI_API_VERSION, corrige caminhos de itemtype e limpeza de sessão, e publica imagens multi-arch no GHCR."
summary: "Publicado em 14 de novembro de 2026, o mcp-glpi v1.2.0 (pacote 3.5.0) muda o alvo padrão da High-Level API do GLPI de v2.3 para v3.0 no GLPI 12, mantendo compatibilidade com v2.x. A versão adiciona a variável de ambiente GLPI_API_VERSION e o parâmetro api_version em glpi_configure_connection, informa a versão resolvida em glpi_connection_status, corrige os caminhos dos itemtypes SoftwareLicense e Project, ajusta os smoke tests para os formatos de equipe de v3.0 e v2.x, deixa de chamar a rota /logout não suportada em killSession e publica imagens multi-arch no GHCR."
date: 2026-11-14
draft: false
tags: ["glpi", "mcp", "ia", "model-context-protocol", "open-source", "docker"]
categories: ["infraestrutura"]
featureimage: "/img/blog/mcp-glpi/featured.png"
featureimagecaption: "Integração entre assistentes de IA, MCP e GLPI"
---

O GLPI 12 passou a expor a **High-Level API v3.0**, e o servidor MCP que conecta assistentes de IA ao GLPI precisou acompanhar. Em 14 de novembro de 2026, a EF-TECH publicou o [mcp-glpi v1.2.0](https://github.com/eftechcombr/mcp-glpi/releases/tag/v1.2.0) (versão **3.5.0** do pacote) — uma entrega que torna a API v3.0 o alvo padrão, mantém o funcionamento com v2.x em instalações mais antigas e corrige os bugs de compatibilidade encontrados no caminho.

![Integração entre assistentes de IA, MCP e GLPI](/img/blog/mcp-glpi/featured.png)

## O release em resumo

| Item | Valor |
| --- | --- |
| Release no GitHub | [`v1.2.0`](https://github.com/eftechcombr/mcp-glpi/releases/tag/v1.2.0) |
| Versão do pacote | `3.5.0` |
| Pull request | [PR #12](https://github.com/eftechcombr/mcp-glpi/pull/12) — `feat(api): prefer GLPI High-Level API v3.0 with v2.x compatibility` |
| Commit de merge | [`13b1dc3`](https://github.com/eftechcombr/mcp-glpi/commit/13b1dc3) |
| Commit do version bump | [`a31778a`](https://github.com/eftechcombr/mcp-glpi/commit/a31778a) |
| Imagem de contêiner | `ghcr.io/eftechcombr/mcp-glpi:1.2.0` (também `1.2`, `3.5.0`, `latest`) |
| Plataformas | `linux/amd64`, `linux/arm64` |

O servidor continua expondo a mesma superfície de ferramentas — **mais de 84 ferramentas MCP** cobrindo tickets, problemas, mudanças, ativos, base de conhecimento, contratos, fornecedores, locais, projetos, usuários, grupos, categorias, entidades, documentos, busca e estatísticas — com autenticação OAuth2, busca multicritério em RSQL, mapeamento dinâmico de campos, resolução de chaves estrangeiras, validação com Zod e anotações de segurança do MCP. O que muda nesta versão é o contrato de API por baixo dessas ferramentas.

## Por que a versão da API se tornou configurável

Até então, o mcp-glpi tinha como alvo a **High-Level API v2.3** do GLPI. Esse era o caminho estável enquanto o GLPI 11 era a versão predominante em produção. O GLPI 12 expõe a **v3.0**, então manter `v2.3` fixo como padrão significaria escolher entre não aproveitar a nova API no GLPI 12 ou quebrar de uma vez todas as instalações em GLPI 11.

A v1.2.0 resolve isso com um alvo configurável:

| Configuração | Onde | Padrão | Função |
| --- | --- | --- | --- |
| `GLPI_API_VERSION` | Variável de ambiente | `3.0` | Define a versão da High-Level API usada pelo processo do servidor |
| `api_version` | Parâmetro da ferramenta `glpi_configure_connection` | `3.0` | Define a versão da API por sessão no modo HTTP multi-tenant |
| `apiVersion` | Resposta de `glpi_connection_status` | — | Informa a versão resolvida em uso |

O valor passa por `normalizeApiVersion`, que valida e normaliza a entrada antes de qualquer requisição. Isso importa porque um erro de digitação em uma variável de ambiente precisa falhar de forma explícita, e não cair silenciosamente em outra superfície de API. Os alvos suportados são `3.0` para o GLPI 12 e `2.3` / `2` para a linha v2.x.

Em uma configuração stdio, a versão é apenas mais uma variável de ambiente:

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
        "GLPI_CLIENT_ID": "seu_client_id",
        "GLPI_API_VERSION": "3.0"
      }
    }
  }
}
```

No modo multi-tenant com Streamable HTTP, em que `GLPI_URL` fica vazio e cada cliente traz a própria conexão, a mesma escolha é passada para `glpi_configure_connection` como `api_version`. Depois de conectar, chame `glpi_connection_status` e confira o campo `apiVersion` para confirmar qual superfície a sessão está usando.

```json
{
  "GLPI_URL": "https://glpi.example.com",
  "auth_method": "password",
  "username": "seu_usuario",
  "password": "sua_senha",
  "client_id": "seu_client_id",
  "api_version": "3.0"
}
```

O trecho acima representa o formato dos argumentos de `glpi_configure_connection`, não um arquivo em disco. As credenciais permanecem em memória durante a sessão e são descartadas quando ela termina ou expira.

## Correções de compatibilidade na v1.2.0

Trocar a versão padrão da API é o destaque, mas a versão também corrige quebras concretas encontradas ao testar as duas gerações de API.

### Caminhos de itemtype: `SoftwareLicense` e `Project`

O `ITEMTYPE_PATH_MAP` traduz itemtypes do MCP para caminhos REST do GLPI. Duas entradas estavam erradas e foram corrigidas:

| Itemtype | Caminho antes | Caminho agora |
| --- | --- | --- |
| `SoftwareLicense` | caminho incorreto | `Management/License` |
| `Project` | caminho incorreto | `Project` |

Essas duas ferramentas não alcançavam os recursos de forma confiável porque as requisições eram montadas com caminhos que não existem na API. Com o mapa corrigido, as operações de licença de software e de projeto passam a resolver para `Management/License` e `Project`, respectivamente.

### Formato de equipes em `scripts/smoke.ts`

A suíte de smoke tests cria e inspeciona a composição de equipes, e a chave de resposta muda entre as gerações da API: a **v3.0** retorna `UserTeamMember`, enquanto a **v2.x** retorna `TeamMember`. A checagem antiga assumia um único formato e passou a falhar assim que o padrão mudou. O `scripts/smoke.ts` agora ramifica pela versão de API configurada e valida o formato correto para cada uma, mantendo o gate de release útil tanto para alvos GLPI 11 quanto GLPI 12.

## Limpeza de sessão sem `/logout`

O `killSession()` chamava uma rota `/logout` que a API não suporta, gerando erros no encerramento. Agora ele limpa o token bearer local e finaliza de forma limpa, sem fingir que o servidor consegue invalidar a sessão remotamente. O efeito prático é um log mais silencioso e um caminho de encerramento previsível para processos stdio e para sessões HTTP expiradas.

## Verificação e pipeline de release

A versão foi validada de ponta a ponta antes da publicação:

| Verificação | Resultado |
| --- | --- |
| `bun run lint` | Aprovado |
| `bun run build` | Aprovado |
| `bun test` | 24/24 testes aprovados |
| GitHub Actions | Build e push da imagem Docker no GHCR para `v1.2.0` |

O workflow de contêiner publicou um manifesto multi-arch para `linux/amd64` e `linux/arm64`, então a mesma tag funciona em servidores x86 padrão, notebooks com Apple Silicon e nós Kubernetes arm64.

## Baixando a imagem

```bash
docker pull ghcr.io/eftechcombr/mcp-glpi:1.2.0
# ou acompanhe a linha de release / versão do pacote / latest
docker pull ghcr.io/eftechcombr/mcp-glpi:1.2
docker pull ghcr.io/eftechcombr/mcp-glpi:3.5.0
docker pull ghcr.io/eftechcombr/mcp-glpi:latest
```

Execute com a versão da API explícita, mesmo sendo `3.0` o padrão — isso documenta o alvo e sobrevive a mudanças futuras de default:

```bash
docker run -i --rm \
  -e GLPI_URL="https://glpi.example.com" \
  -e GLPI_AUTH_METHOD="password" \
  -e GLPI_USERNAME="seu_usuario" \
  -e GLPI_PASSWORD="sua_senha" \
  -e GLPI_CLIENT_ID="seu_client_id" \
  -e GLPI_API_VERSION="3.0" \
  ghcr.io/eftechcombr/mcp-glpi:1.2.0
```

Mantenha o `-i` e não adicione `-t`: um TTY pode corromper o fluxo JSON-RPC do stdio. A imagem executa com o usuário não-root `bunuser:1001` sobre `oven/bun:1-alpine`.

## Atualizando a partir da 3.4

A principal mudança de comportamento é o alvo padrão: **`GLPI_API_VERSION` agora tem `3.0` como valor padrão**, em vez de `v2.3`.

1. **No GLPI 12**, atualize e mantenha o padrão. Nenhuma configuração extra é necessária.
2. **No GLPI 11 ou em qualquer instância sem a API v3.0**, fixe o comportamento antigo explicitamente:

   ```bash
   GLPI_API_VERSION=2.3
   ```

   `GLPI_API_VERSION=2` também é aceito para a linha v2.x. No modo HTTP multi-tenant, passe `api_version: "2.3"` para `glpi_configure_connection`.
3. **Confirme depois de conectar** com `glpi_connection_status`; o campo `apiVersion` mostra o alvo resolvido.
4. **Atualize a tag do contêiner** para `1.2.0`, `1.2`, `3.5.0` ou `latest`, e mantenha o `-i` nas configurações do cliente MCP.

Nada mais na configuração do cliente precisa mudar. As correções de mapeamento de itemtype e dos smoke tests são internas, e a limpeza do `killSession()` apenas remove uma chamada não suportada.

## Links úteis

- [Release v1.2.0 no GitHub](https://github.com/eftechcombr/mcp-glpi/releases/tag/v1.2.0)
- [Pull request #12](https://github.com/eftechcombr/mcp-glpi/pull/12)
- [Commit `13b1dc3`](https://github.com/eftechcombr/mcp-glpi/commit/13b1dc3) e [commit `a31778a`](https://github.com/eftechcombr/mcp-glpi/commit/a31778a)
- [Pacote `mcp-glpi` no npm](https://www.npmjs.com/package/mcp-glpi)
- [Imagem de contêiner no GHCR](https://github.com/eftechcombr/mcp-glpi/pkgs/container/mcp-glpi)
- [Projeto GLPI](https://glpi-project.org/) e [documentação da High-Level API do GLPI](https://glpi-user-documentation.readthedocs.io/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Página do produto GLPI da EF-TECH](/pt-br/produtos/glpi/)

---

Na **EF-TECH**, trabalhamos com GLPI, cloud computing e infraestrutura de TI — de imagens de contêiner e Helm charts a integrações como o mcp-glpi. [Entre em contato](/pt-br/contato/) para conversar sobre rodar o GLPI 12 com assistentes de IA no seu ambiente.
