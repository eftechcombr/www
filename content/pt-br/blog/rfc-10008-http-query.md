---
title: "Entendendo a RFC 10008: O Método HTTP QUERY"
description: "Uma análise aprofundada sobre a RFC 10008, que introduz o método HTTP QUERY como uma alternativa segura e idempotente para consultas com grande volume de dados."
summary: "A RFC 10008 padroniza o método HTTP QUERY, preenchendo uma lacuna antiga entre GET e POST. Ele permite requisições seguras e idempotentes com parâmetros no corpo da requisição, resolvendo limites de tamanho de URIs e mantendo os benefícios de cache e retransmissão."
date: 2026-07-09
draft: false
tags: ["http", "rfc", "desenvolvimento-web", "api", "arquitetura"]
categories: ["arquitetura"]
---

A IETF publicou oficialmente a **RFC 10008**, padronizando o método de requisição **HTTP QUERY**. Esta especificação define uma nova maneira padronizada de executar consultas seguras e idempotentes contendo parâmetros de consulta complexos ou volumosos dentro do corpo da requisição (request body).

Por anos, desenvolvedores enfrentaram dilemas ao escolher entre `GET` e `POST` para endpoints de busca e consulta. A RFC 10008 preenche essa lacuna de maneira nativa, oferecendo uma solução limpa e idiomática para o design de APIs modernas.

Abaixo, apresentamos uma análise completa do método HTTP QUERY, por que ele é importante e como utilizá-lo.

---

## O Problema Histórico: GET vs. POST

Tradicionalmente, as APIs web tinham duas opções principais para recuperar dados:

1. **HTTP GET**: Excelente para recuperação de recursos porque é seguro (não altera o estado do servidor) e idempotente (pode ser repetido sem efeitos colaterais). No entanto, os parâmetros do `GET` precisam ser codificados na URI. Quando uma consulta possui parâmetros complexos (como filtros JSON aninhados, queries SQL brutas ou termos de busca muito longos), a URI pode rapidamente exceder os limites de tamanho (geralmente recomenda-se suporte a pelo menos 8000 octetos, mas as restrições variam em proxies e navegadores). Além disso, URIs são frequentemente gravadas em logs de texto simples, gerando riscos de segurança para dados confidenciais de consulta.
2. **HTTP POST**: Permite enviar parâmetros no corpo da requisição, contornando limitações de tamanho da URI e riscos de logging. No entanto, o `POST` não é semanticamente seguro ou idempotente por padrão. Caches, proxies e navegadores não podem repetir automaticamente requisições `POST` malsucedidas nem podem realizar o cache de seus resultados facilmente.

### A Solução com o Método QUERY

O método `QUERY` funciona como uma ponte entre os dois. Assim como no `POST`, a entrada para a operação de consulta é passada no corpo da requisição (conteúdo da query) e não na URI. E assim como no `GET`, o método é explicitamente **seguro** e **idempotente**, permitindo que recursos como cache e retransmissões automáticas operem de forma nativa.

---

## Comparativo de Propriedades dos Métodos

A tabela abaixo resume como o `QUERY` se compara ao `GET` e ao `POST` (adaptada da especificação oficial da RFC):

| Propriedade | GET | QUERY | POST |
| :--- | :--- | :--- | :--- |
| **Seguro (Safe)** | Sim | Sim | Potencialmente Não |
| **Idempotente** | Sim | Sim | Potencialmente Não |
| **URI para a Query em si** | Sim (por definição) | Opcional (header `Location`) | Não |
| **URI para o Resultado** | Opcional (`Content-Location`) | Opcional (`Content-Location`) | Opcional (`Content-Location`) |
| **Cacheável** | Sim | Sim | Sim, mas apenas para GET/HEAD futuros |
| **Corpo da Requisição** | Sem semântica definida | Esperado (segundo regras do recurso) | Esperado (segundo regras do recurso) |

---

## Exemplos Práticos

Vejamos como uma consulta longa é transformada dos antigos formatos `GET` ou `POST` para o novo método `QUERY`.

### O padrão antigo e verboso com GET:
Se os parâmetros forem muito grandes, este formato é ineficiente para processar, corre o risco de ser truncado e expõe informações confidenciais nos logs do servidor:

```http
GET /feed?q=foo&limit=10&sort=-published&filter=conteudo-de-filtro-aninhado-altamente-especifico HTTP/1.1
Host: example.org
```

### O contorno comum com POST:
Embora proteja contra logs e truncamento, intermediários de rede não podem presumir que esta requisição é segura ou idempotente:

```http
POST /feed HTTP/1.1
Host: example.org
Content-Type: application/x-www-form-urlencoded

q=foo&limit=10&sort=-published
```

### O novo Método QUERY:
Ao realizar uma requisição `QUERY`, obtemos o melhor dos dois mundos:

```http
QUERY /feed HTTP/1.1
Host: example.org
Content-Type: application/x-www-form-urlencoded
Accept: application/json

q=foo&limit=10&sort=-published
```

#### Resposta:
```http
HTTP/1.1 200 OK
Content-Type: application/json

[
  { "id": 1, "title": "Primeiro Resultado" },
  { "id": 2, "title": "Segundo Resultado" }
]
```

---

## Principais Características Técnicas da RFC 10008

### 1. O Cabeçalho `Accept-Query`
Os servidores podem anunciar suporte ao método `QUERY` e quais formatos aceitam através do cabeçalho de resposta `Accept-Query`. Ele utiliza a sintaxe moderna de "Campos Estruturados" (Structured Fields):

```http
Accept-Query: "application/jsonpath", application/sql;charset="UTF-8"
```

Os clientes podem descobrir o suporte por meio de uma requisição `OPTIONS` ou inspecionando o cabeçalho `Allow` em uma resposta `405 Method Not Allowed`:

```http
OPTIONS /contacts HTTP/1.1
Host: example.org

--- Resposta ---
HTTP/1.1 200 OK
Allow: GET, QUERY, OPTIONS, HEAD
```

### 2. Cache e Chaves de Cache (Cache Keys)
Fazer cache de requisições `QUERY` é inerentemente mais complexo do que fazer cache de requisições `GET` porque o cache precisa construir uma chave utilizando tanto a URI quanto o corpo da requisição (conteúdo da query), junto aos metadados associados.

Para melhorar a eficiência, os caches têm permissão para normalizar diferenças pequenas e semanticamente insignificantes nos corpos das requisições (como remover espaços em branco no JSON ou remover codificações de conteúdo específicas) antes de gerar a chave de cache.

### 3. Redirecionamento e Recursos Equivalentes
Ao processar um `QUERY`, o servidor pode atribuir uma URI para a própria definição de consulta ou para o resultado específico dela.

- **Campo de resposta `Location`**: Indica uma URI que representa a consulta em si. O cliente pode enviar uma requisição `GET` padrão para esta URI para repetir a busca sem precisar reenviar o corpo pesado da requisição.
- **Campo de resposta `Content-Location`**: Aponta para um recurso temporário contendo o resultado estático da consulta que acabou de ser realizada.

Por exemplo, o servidor pode responder com:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Location: /contacts/stored-queries/42
Content-Location: /contacts/stored-results/17
```

Os clientes podem, subsequentemente, enviar uma requisição `GET /contacts/stored-queries/42` para executar a mesma busca de forma simplificada.

---

## Considerações de Segurança

A RFC 10008 destaca várias vantagens e requisitos de segurança para os implementadores:

- **Prevenção de Vazamento em Logs**: Parâmetros de busca sensíveis (como IDs de usuários ou chaves de busca personalizadas) ficam contidos no corpo, evitando a exposição em logs de servidores e proxies em texto claro.
- **URIs de Recursos Temporários**: Se o servidor atribuir uma URI para a consulta (utilizando `Location` ou `Content-Location`), ele **deve** garantir que essa nova URI gerada não exponha partes confidenciais do corpo original da requisição.
- **Tratamento de CORS**: Navegadores que implementam Compartilhamento de Recursos de Origem Cruzada (CORS) farão uma requisição de "preflight" (`OPTIONS`) antes de um `QUERY`, uma vez que ele não pertence ao grupo de métodos isentos de preflight pelo CORS.

---

## Conclusão

A padronização do método `QUERY` representa um marco importante para a arquitetura RESTful. Ela elimina o abuso semântico do `POST` para buscas, resolve as limitações de tamanho e vazamentos de segurança do `GET`, e abre caminhos mais eficientes para otimizações de cache em servidores de API e intermediários de rede.

À medida que os frameworks web e proxies reversos começam a implementar suporte nativo para a RFC 10008, desenvolvedores devem considerar a adoção do `QUERY` para endpoints de filtragem, buscas complexas e relatórios que exijam grandes payloads.

Para ler a especificação técnica completa, consulte o padrão oficial:
- [RFC 10008: The HTTP QUERY Method](https://www.rfc-editor.org/info/rfc10008/)

Deseja modernizar a arquitetura das suas APIs ou aprimorar a observabilidade dos seus sistemas? Na EF-TECH, ajudamos empresas a desenhar arquiteturas de software escaláveis, eficientes e robustas. [Entre em contato](/pt-br/contato/).
