---
title: "WireGuard"
description: "WireGuard - VPN corporativa containerizada e segura com deploy otimizado pela EF-TECH"
summary: "WireGuard e uma VPN corporativa moderna, containerizada e segura. A EF-TECH oferece deploy via Docker com Alpine Linux, health check automatizado, gerenciamento de chaves e monitoramento pronto para producao."
date: 2026-06-19
tags: ["wireguard", "vpn", "docker", "seguranca", "rede"]
categories: ["produtos"]
---
## WireGuard

WireGuard e um protocolo VPN moderno e eficiente que combina criptografia de ultima geracao com alto desempenho. A EF-TECH oferece uma solucao containerizada e leve do WireGuard construida sobre Alpine Linux (~50MB), projetada para ambientes corporativos que exigem seguranca, simplicidade e confiabilidade. O projeto e mantido pela nossa equipe no [GitHub](https://github.com/eftechcombr/wireguard) com imagens disponiveis no GitHub Container Registry (ghcr.io).

### VPN Corporativa WireGuard

A solucao WireGuard da EF-TECH foi desenvolvida para atender as demandas de conectividade segura em ambientes corporativos:

- Alto desempenho com baixa latencia
- Criptografia moderna baseada em Curve25519, ChaCha20 e Poly1305
- Configuracao simples e gerenciamento simplificado de chaves
- Conexao stateful com autenticacao mutua
- Roteamento eficiente com suporte a split tunneling
- Ideal para acesso remoto e interconexao de redes

### Deploy Containerizado

O deploy containerizado do WireGuard pela EF-TECH garante leveza e portabilidade para qualquer ambiente:

- Imagem Docker baseada em Alpine Linux (~50MB)
- Container com reinicializacao automatica (restart: unless-stopped)
- Capacidades NET_ADMIN e SYS_MODULE para gerenciamento de rede e kernel
- Configuracoes de sysctl otimizadas (ip_forward, ipv6.conf.all.forwarding)
- Graceful shutdown com tratamento de sinais (SIGTERM, SIGINT)
- Deploy simplificado via Docker Compose
- Portas expostas: 51820/udp (VPN) e 8080/tcp (health check)
- Volumes persistentes para configuracao (./etc/:/etc/wireguard/)
- Variaveis de ambiente: WG_CONF, WG_PRIVATE_KEY, WG_PUBLIC_KEY, WG_INTERFACE, PUID, PGID, TZ, SERVERURL, SERVERPORT, INTERNAL_SUBNET, PEERDNS

### Monitoramento e Health Check

A solucao inclui monitoramento integrado para garantir a disponibilidade continua do servico:

- Endpoint HTTP na porta 8080 para verificacao de saude
- Retorna HTTP 200 quando o servico esta operacional
- Retorna HTTP 503 quando o servico esta indisponivel
- Script Python wireguard_healthcheck.py como servidor de health check
- Ideal para integracao com orquestradores e sistemas de monitoramento
- Pronto para ambientes de producao com requisitos de alta disponibilidade

### Gerenciamento de Chaves

O gerenciamento de chaves e automatizado para simplificar a operacao e aumentar a seguranca:

- Geracao automatica de chave privada via `wg genkey`
- Derivacao automatica de chave publica via `wg pubkey`
- Chaves armazenadas em arquivos persistentes: etc/privatekey e etc/publickey
- Configuracao da interface armazenada em etc/wg0.conf
- Suporte a definicao manual de chaves via variaveis de ambiente (WG_PRIVATE_KEY, WG_PUBLIC_KEY)
- Arquitetura que permite rotacao de chaves sem interrupcao do servico

### Repositorio

O codigo fonte, Dockerfile, docker-compose.yml e documentacao completa estao disponiveis no repositorio oficial:

- Repositorio: https://github.com/eftechcombr/wireguard
- Imagens disponiveis em ghcr.io
- Docker Compose com cap_add, sysctls, volumes e portas configuradas
- Scripts de entrada (entrypoint.sh) e health check (wireguard_healthcheck.py)
- Licenca de codigo aberto para uso corporativo

---

Interessado em WireGuard para sua empresa? [Entre em contato](/pt-br/contato/) para uma consultoria personalizada.
