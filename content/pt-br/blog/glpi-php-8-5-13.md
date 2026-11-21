---
title: "GLPI: imagem base atualizada para PHP 8.5.13"
description: "A distribuição de contêineres da EF-TECH para GLPI atualizou sua imagem PHP-FPM base para PHP 8.5.13 e zlib 1.4."
summary: "A imagem base usada na distribuição Docker do GLPI foi atualizada de PHP 8.5.12 para PHP 8.5.13, com zlib atualizado para 1.4-r0 no Alpine 3.24. A mudança mantém o GLPI 12.0.2 e as imagens de aplicação existentes."
date: 2026-11-21
draft: false
tags: ["glpi", "docker", "php", "infraestrutura"]
categories: ["infraestrutura"]
---

A imagem base PHP da distribuição de [GLPI da EF-TECH](https://github.com/eftechcombr/glpi) foi atualizada para **PHP 8.5.13**, substituindo a versão 8.5.12. A alteração foi publicada no repositório em 21 de novembro de 2026.

## O que mudou

A atualização está no `docker/php/Dockerfile.base` e contempla:

- Imagem `php:8.5.13-fpm-alpine3.24` no lugar de `php:8.5.12-fpm-alpine3.24`.
- Pacote de desenvolvimento `zlib-dev` atualizado de `1.3.2-r1` para `1.4-r0`, conforme a versão disponível no Alpine 3.24.

Essa imagem base fornece o ambiente PHP-FPM sobre o qual a imagem da aplicação é construída. A mudança não altera a versão do GLPI: a configuração da aplicação continua apontando para **GLPI 12.0.2**. Também não houve alteração na versão do Nginx.

## O que fazer ao atualizar

Quem consome as imagens publicadas deve conferir as tags disponíveis no [repositório de releases](https://github.com/eftechcombr/glpi/releases) e seguir o processo normal de atualização do ambiente. Quem constrói as imagens localmente pode reconstruir a imagem PHP-FPM para incorporar a nova base.

Antes de aplicar atualizações em produção, mantenha os backups do banco de dados e dos arquivos do GLPI em dia e valide a implantação em um ambiente de homologação.

## Referências

- [Repositório EF-TECH GLPI](https://github.com/eftechcombr/glpi)
- [Alteração da imagem base PHP para 8.5.13](https://github.com/eftechcombr/glpi/commit/80a94b030b60eb0f4f69a9ff2273433d96d6ca0b)
- [Produto GLPI da EF-TECH](/pt-br/produtos/glpi/)
