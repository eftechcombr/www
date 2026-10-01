---
title: "GLPI 11.0.11: Release de Segurança, Correção de Plugins e Novos Recursos no eftechcombr/glpi"
description: "A EF-TECH publicou as imagens Docker e os Helm charts do GLPI 11.0.11, uma release crítica de segurança que substitui a 11.0.10, corrige 6 vulnerabilidades de alta severidade e traz suporte a templates customizados de Nginx e conexões MySQL com SSL."
summary: "O GLPI 11.0.11 foi lançado em 1º de outubro de 2026 como um security release essencial que corrige 6 vulnerabilidades de alta severidade e substitui imediatamente a versão 11.0.10, resolvendo uma regressão no sistema de plugins. A distribuição da EF-TECH (eftechcombr/glpi) já está disponível em contêineres Docker e Helm chart, trazendo novidades como templates customizados para o Nginx (PR #209) e suporte a conexões seguras com MySQL/MariaDB via SSL (PR #207)."
date: 2026-10-01
draft: false
tags: ["glpi", "docker", "kubernetes", "helm", "cloud-native", "seguranca"]
categories: ["infraestrutura"]
featureimage: "cover.png"
featureimagecaption: "GLPI 11.0.11 — Imagens Docker e Helm charts com correções críticas de segurança e melhorias operacionais pela EF-TECH"
---

A EF-TECH disponibilizou hoje, 1º de outubro de 2026, as novas imagens Docker e versões do Helm chart para o **GLPI 11.0.11** no repositório [eftechcombr/glpi](https://github.com/eftechcombr/glpi). Esta atualização traz correções vitais de segurança publicadas pelo projeto upstream, soluciona uma regressão importante no ecossistema de plugins e incorpora melhorias operacionais desenvolvidas pela EF-TECH e pela comunidade de código aberto.

![GLPI 11.0.11](cover.png)

## Por que o GLPI 11.0.11 substitui a versão 11.0.10?

Uma informação fundamental para operadores e administradores de sistemas: **o GLPI 11.0.11 substitui imediatamente a versão 11.0.10**. 

Durante o ciclo de lançamento da versão 11.0.10, foi identificada uma regressão que afetava diretamente o carregamento e os ganchos (*hooks*) do sistema de plugins do GLPI. Para evitar impactos operacionais em ambientes que dependem de extensões ativas de inventário, autenticação ou automação, a equipe upstream do `glpi-project/glpi` publicou de imediato a versão 11.0.11.

> **Recomendação de atualização:** Se a sua organização estava planejando atualizar para a versão 11.0.10 ou ainda opera na linha 11.0.9 (ou anteriores), atualize diretamente para o **GLPI 11.0.11**. A versão 11.0.10 não deve ser utilizada em produção.

---

## Raio-X de Segurança: O Que Foi Corrigido

Classificado oficialmente como **Security Release**, o GLPI 11.0.11 mitiga um conjunto de vulnerabilidades severas que poderiam permitir desde o desvio de controles de acesso até a execução indevida de comandos e escalação de privilégios.

### Vulnerabilidades de Alta Severidade (High)

1. **Bypass de autorização em ações massivas (*Authorization bypass in massive actions*)**:
   Falha na validação de permissões contextuais ao executar ações em lote no GLPI, permitindo que operadores manipulem recursos além das atribuições de seu perfil.
2. **Escalação de privilégios via clonagem de usuários (*Privilege escalation via user cloning*)**:
   Brecha no fluxo de clonagem de contas que possibilitava herdar ou atribuir direitos administrativos superiores aos do usuário solicitante.
3. **Checagem inadequada de permissões na exclusão de usuários (*Improper rights checks in users deletion*)**:
   Ausência de checagem estrita de perfis no momento de purgar ou desativar contas de usuários no diretório.
4. **Injeção de SQL através do dropdown de atores em formulários (*SQL Injection through form actors dropdown*)**:
   Tratamento insuficiente de parâmetros recebidos via requisições HTTP nos seletores dinâmicos de atores de formulários, abrindo vetor para consultas SQL não autorizadas na base de dados.
5. **Modificação ou desativação de 2FA em usuários com privilégios mais altos (*2FA deactivation/modification on users with higher privileges*)**:
   Falha que permitia a usuários com permissões intermediárias desabilitar ou alterar o segundo fator de autenticação (MFA/2FA) de contas com nível hierárquico superior.
6. **XSS Refletido no widget de resultados de busca do dashboard (*Reflected XSS in the dashboard search result widget*)**:
   Injeção de scripts arbitrários no navegador de operadores através de parâmetros de busca não sanitizados renderizados no painel principal.

### Vulnerabilidades de Média Severidade (Medium)

- **Enumeração de nomes de usuários na funcionalidade de planejamento (*Users names enumeration via the planning feature*)**:
  Exposição de identificadores de operadores através de respostas inconsistentes em endpoints da agenda.
- **Falta de checagem de autorização no planejamento (*Missing authorization checks in the planning feature*)**:
  Permissão indevida para visualizar ou interagir com compromissos de terceiros sem a respectiva permissão de perfil.

A combinação de vetor SQL Injection com falhas de escalação de privilégios e manipulação de 2FA torna este upgrade indispensável.

---

## Novidades na Distribuição EF-TECH (`eftechcombr/glpi`)

Além de incorporar o código upstream corrigido (PR #211 por [@eduardofraga](https://github.com/eduardofraga)), o ecossistema de contêineres e Helm charts da EF-TECH traz aprimoramentos arquiteturais relevantes:

### 1. Template Customizável do Nginx e Controle de IPv6 (PR #209)

Uma contribuição valiosa de [@ohemelaar-dinum](https://github.com/ohemelaar-dinum) adicionou a flexibilidade de injetar um template de configuração customizado para o Nginx (`nginx.conf.template`).

Em ambientes corporativos ou clusters Kubernetes onde o suporte a IPv6 está intencionalmente desativado no kernel do host, o listener padrão `listen [::]:80;` causava erros recorrentes de inicialização:

```text
nginx: [emerg] bind() to [::]:80 failed (99: Cannot assign requested address)
```

Com o PR #209, agora é possível fornecer uma configuração customizada ou desabilitar o listener IPv6 de forma simples, garantindo compatibilidade universal de rede sem necessidade de construir uma imagem derivada.

#### Exemplo: Desabilitando o listener IPv6 via Volume Mount

Ao executar em contêiner ou via ConfigMap no Kubernetes, você pode montar o seu próprio template de virtualhost:

```nginx
# custom-nginx.conf.template
server {
    listen 80 default_server;
    # Listener IPv6 desativado para clusters sem suporte a IPv6
    # listen [::]:80 default_server;

    server_name _;
    root /var/www/glpi/public;

    location / {
        try_files $uri /index.php$is_args$args;
    }

    location ~ ^/index\.php$ {
        fastcgi_pass ${GLPI_PHPFPM_HOST}:${GLPI_PHPFPM_PORT};
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }
}
```

### 2. Suporte Nativo a Conexões MySQL/MariaDB com SSL/TLS (PR #207)

Consolidado no ciclo recente e totalmente compatível com o GLPI 11.0.11, o projeto agora oferece suporte nativo para conexões criptografadas com o banco de dados via SSL/TLS.

Essa funcionalidade é indispensável ao conectar o GLPI a bancos de dados gerenciados em nuvem (como **AWS RDS Aurora MySQL**, **Google Cloud SQL** ou **Azure Database for MySQL**), onde a imposição de conexões criptografadas (`REQUIRE SSL`) é uma política de segurança corporativa mandatória.

Parâmetros suportados nas variáveis de ambiente:
- `GLPI_DB_SSL`: ativação do modo SSL (`true` ou `false`).
- `GLPI_DB_SSL_CA`: caminho para o certificado da autoridade certificadora (CA).
- `GLPI_DB_SSL_VERIFY`: verificação rigorosa do certificado do servidor de banco.

---

## Como Atualizar ou Experimentar

### Atualização via Helm Chart (Kubernetes)

O repositório oficial de Helm charts da EF-TECH já conta com as definições atualizadas:

```bash
# 1. Adicione ou atualize o repositório Helm da EF-TECH
helm repo add eftech https://eftechcombr.github.io/glpi/
helm repo update

# 2. Atualize sua release existente para o GLPI 11.0.11
helm upgrade --install glpi eftech/glpi \
  --namespace glpi \
  --create-namespace \
  --version 2.11.7
```

### Execução via Docker Standalone / Docker Compose

Para ambientes baseados em contêineres Docker independentes:

```bash
# Baixar a imagem estável 11.0.11
docker pull ghcr.io/eftechcombr/glpi:11.0.11
```

Exemplo básico de `docker-compose.yml` utilizando o GLPI 11.0.11 com MariaDB e Nginx:

```yaml
services:
  glpi-fpm:
    image: ghcr.io/eftechcombr/glpi:11.0.11
    restart: unless-stopped
    environment:
      - GLPI_DB_HOST=mariadb
      - GLPI_DB_NAME=glpi
      - GLPI_DB_USER=glpi
      - GLPI_DB_PASSWORD=secret_db_password
      - GLPI_DB_SSL=false
    volumes:
      - glpi_data:/var/www/glpi/files
      - glpi_marketplace:/var/www/glpi/marketplace

  glpi-nginx:
    image: ghcr.io/eftechcombr/glpi-nginx:11.0.11
    restart: unless-stopped
    ports:
      - "8080:80"
    environment:
      - GLPI_PHPFPM_HOST=glpi-fpm
      - GLPI_PHPFPM_PORT=9000
    depends_on:
      - glpi-fpm

volumes:
  glpi_data:
  glpi_marketplace:
```

---

## Links e Referências

- [Repositório eftechcombr/glpi no GitHub](https://github.com/eftechcombr/glpi)
- [Releases e Changelog do eftechcombr/glpi](https://github.com/eftechcombr/glpi/releases)
- [Notas da Release GLPI 11.0.11 Upstream](https://github.com/glpi-project/glpi/releases/tag/11.0.11)
- [GLPI no Artifact Hub](https://artifacthub.io/packages/helm/eftech/glpi)
- [Repositório de Helm Charts da EF-TECH](https://eftechcombr.github.io/glpi/)

---

Na **EF-TECH**, somos especialistas em Kubernetes, cloud computing e automação de infraestrutura. Projetamos, implantamos e operamos ambientes GLPI de alta performance com segurança, observabilidade e escalabilidade. [Entre em contato](/pt-br/contato/) para saber como podemos ajudar sua equipe. Para mais artigos como este, visite nosso [blog](/pt-br/blog/).
