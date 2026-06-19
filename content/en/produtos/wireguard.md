---
title: "WireGuard"
description: "WireGuard - containerized, secure corporate VPN with optimized deployment by EF-TECH"
summary: "WireGuard is a modern, containerized, and secure corporate VPN. EF-TECH offers deployment via Docker with Alpine Linux, automated health checks, key management, and production-ready monitoring."
date: 2026-06-19
tags: ["wireguard", "vpn", "docker", "security", "network"]
categories: ["produtos"]
---
## WireGuard

WireGuard is a modern, high-performance VPN protocol that combines cutting-edge encryption with exceptional speed. EF-TECH offers a lightweight, containerized WireGuard solution built on Alpine Linux (~50MB), designed for enterprise environments demanding security, simplicity, and reliability. The project is maintained by our team on [GitHub](https://github.com/eftechcombr/wireguard) with images available on GitHub Container Registry (ghcr.io).

### Enterprise WireGuard VPN

The EF-TECH WireGuard solution is designed to meet the connectivity demands of enterprise environments:

- High performance with low latency
- Modern encryption based on Curve25519, ChaCha20, and Poly1305
- Simple configuration and streamlined key management
- Stateful connection with mutual authentication
- Efficient routing with split tunneling support
- Ideal for remote access and network interconnection

### Containerized Deployment

EF-TECH's containerized WireGuard deployment ensures lightness and portability for any environment:

- Docker image based on Alpine Linux (~50MB)
- Container with automatic restart (restart: unless-stopped)
- NET_ADMIN and SYS_MODULE capabilities for network and kernel management
- Optimized sysctl settings (ip_forward, ipv6.conf.all.forwarding)
- Graceful shutdown with signal handling (SIGTERM, SIGINT)
- Simplified deployment via Docker Compose
- Exposed ports: 51820/udp (VPN) and 8080/tcp (health check)
- Persistent volumes for configuration (./etc/:/etc/wireguard/)
- Environment variables: WG_CONF, WG_PRIVATE_KEY, WG_PUBLIC_KEY, WG_INTERFACE, PUID, PGID, TZ, SERVERURL, SERVERPORT, INTERNAL_SUBNET, PEERDNS

### Monitoring and Health Check

The solution includes integrated monitoring to ensure continuous service availability:

- HTTP endpoint on port 8080 for health verification
- Returns HTTP 200 when the service is operational
- Returns HTTP 503 when the service is unavailable
- Python wireguard_healthcheck.py script as health check server
- Ideal for integration with orchestrators and monitoring systems
- Ready for production environments with high availability requirements

### Key Management

Key management is automated to simplify operations and increase security:

- Automatic private key generation via `wg genkey`
- Automatic public key derivation via `wg pubkey`
- Keys stored in persistent files: etc/privatekey and etc/publickey
- Interface configuration stored in etc/wg0.conf
- Support for manual key definition via environment variables (WG_PRIVATE_KEY, WG_PUBLIC_KEY)
- Architecture that allows key rotation without service interruption

### Repository

Source code, Dockerfile, docker-compose.yml, and full documentation are available in the official repository:

- Repository: https://github.com/eftechcombr/wireguard
- Images available on ghcr.io
- Docker Compose with cap_add, sysctls, volumes, and ports configured
- Entry scripts (entrypoint.sh) and health check (wireguard_healthcheck.py)
- Open-source license for enterprise use

---

Interested in WireGuard for your company? [Contact us](/en/contato/) for a personalized consultation.
