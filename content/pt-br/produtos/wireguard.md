---
title: "WireGuard"
description: "WireGuard - VPN corporativa containerizada e segura com deploy otimizado pela EF-TECH"
summary: "WireGuard é uma VPN corporativa moderna, containerizada e segura. A EF-TECH oferece deploy via Docker com Alpine Linux, health check automatizado, gerenciamento de chaves e monitoramento pronto para produção."
date: 2026-06-19
tags: ["wireguard", "vpn", "docker", "seguranca", "rede"]
categories: ["produtos"]
---
## WireGuard

WireGuard é um protocolo VPN moderno e eficiente que combina criptografia de última geração com alto desempenho. A EF-TECH oferece uma solução containerizada e leve do WireGuard construída sobre Alpine Linux (~50MB), projetada para ambientes corporativos que exigem segurança, simplicidade e confiabilidade. O projeto é mantido pela nossa equipe no [GitHub](https://github.com/eftechcombr/wireguard) com imagens disponíveis no GitHub Container Registry (ghcr.io).

### VPN Corporativa WireGuard

A solução WireGuard da EF-TECH foi desenvolvida para atender as demandas de conectividade segura em ambientes corporativos:

- Alto desempenho com baixa latencia
- Criptografia moderna baseada em Curve25519, ChaCha20 e Poly1305
- Configuração simples e gerenciamento simplificado de chaves
- Conexão stateful com autenticação mútua
- Roteamento eficiente com suporte a split tunneling
- Ideal para acesso remoto e interconexão de redes

### Deploy Containerizado

O deploy containerizado do WireGuard pela EF-TECH garante leveza e portabilidade para qualquer ambiente:

- Imagem Docker baseada em Alpine Linux (~50MB)
- Container com reinicialização automática (restart: unless-stopped)
- Capacidades NET_ADMIN e SYS_MODULE para gerenciamento de rede e kernel
- Configurações de sysctl otimizadas (ip_forward, ipv6.conf.all.forwarding)
- Graceful shutdown com tratamento de sinais (SIGTERM, SIGINT)
- Deploy simplificado via Docker Compose
- Portas expostas: 51820/udp (VPN) e 8080/tcp (health check)
- Volumes persistentes para configuração (./etc/:/etc/wireguard/)
- Variaveis de ambiente: WG_CONF, WG_PRIVATE_KEY, WG_PUBLIC_KEY, WG_INTERFACE, PUID, PGID, TZ, SERVERURL, SERVERPORT, INTERNAL_SUBNET, PEERDNS

### Monitoramento e Health Check

A solução inclui monitoramento integrado para garantir a disponibilidade contínua do serviço:

- Endpoint HTTP na porta 8080 para verificação de saúde
- Retorna HTTP 200 quando o servico esta operacional
- Retorna HTTP 503 quando o servico esta indisponivel
- Script Python wireguard_healthcheck.py como servidor de health check
- Ideal para integração com orquestradores e sistemas de monitoramento
- Pronto para ambientes de produção com requisitos de alta disponibilidade

### Gerenciamento de Chaves

O gerenciamento de chaves é automatizado para simplificar a operação e aumentar a segurança:

- Geração automática de chave privada via `wg genkey`
- Derivação automática de chave pública via `wg pubkey`
- Chaves armazenadas em arquivos persistentes: etc/privatekey e etc/publickey
- Configuração da interface armazenada em etc/wg0.conf
- Suporte a definição manual de chaves via variáveis de ambiente (WG_PRIVATE_KEY, WG_PUBLIC_KEY)
- Arquitetura que permite rotação de chaves sem interrupção do serviço

### Repositorio

O código fonte, Dockerfile, docker-compose.yml e documentação completa estão disponíveis no repositório oficial:

- Repositorio: https://github.com/eftechcombr/wireguard
- Imagens disponiveis em ghcr.io
- Docker Compose com cap_add, sysctls, volumes e portas configuradas
- Scripts de entrada (entrypoint.sh) e health check (wireguard_healthcheck.py)
- Licença de código aberto para uso corporativo

---

Interessado em WireGuard para sua empresa? [Entre em contato](/pt-br/contato/) para uma consultoria personalizada.
