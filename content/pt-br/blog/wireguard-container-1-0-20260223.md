---
title: "WireGuard Container 1.0.20260223: Health Check em Go, Alpine 3.24, Logs OTLP de Peers e Builds por Release"
description: "A imagem containerizada de WireGuard da EF-TECH chega à versão 1.0.20260223 — a maior atualização desde v1.0.20250521. O health check em Python dá lugar a um binário estático em Go com logs de peers em stdout e OpenTelemetry, o Alpine sobe para 3.24 e o CI agora publica apenas em releases ou dispatch manual."
summary: "O release 1.0.20260223 do eftechcombr/wireguard remove o runtime Python em favor de um servidor de health check compilado em Go, atualiza para Alpine 3.24 e Go 1.27.4, adiciona logs JSON estruturados e exportação OTLP/HTTP para peers, fixa a versão do iptables, endurece o entrypoint.sh e muda o CI/CD para builds multi-arch (linux/amd64 e linux/arm64) disparados por release."
date: 2026-11-13
draft: false
tags: ["wireguard", "docker", "vpn", "go", "opentelemetry", "alpine", "ci-cd"]
categories: ["infraestrutura"]
---

Em 13 de novembro de 2026 publicamos o release [**1.0.20260223** do `eftechcombr/wireguard`](https://github.com/eftechcombr/wireguard/releases/tag/1.0.20260223) — o primeiro desde a `v1.0.20250521` e, de longe, o maior conjunto de mudanças do projeto até aqui. Este também é o primeiro pacote construído pelo novo pipeline orientado a releases habilitado no [PR #70](https://github.com/eftechcombr/wireguard/pull/70).

Na prática, a atualização transforma o container de um wrapper em bash e Python em volta do `wg-quick` em um appliance mais enxuto e observável sobre **Alpine 3.24**, com um binário estático em **Go 1.27.4** cuidando do health check e da telemetria de peers via OpenTelemetry.

---

## Resumo das novidades

| Área | O que mudou | Pull Request |
| --- | --- | --- |
| **Reescrita do health check** | Substituição do `wireguard_healthcheck.py` por `main.go` e testes unitários (`main_test.go`), removendo o Python da imagem final | [#54](https://github.com/eftechcombr/wireguard/pull/54) |
| **Imagem base e toolchain** | Build multi-stage com `golang:1.27.4-alpine3.24` e runtime em `alpine:3.24` | [#54](https://github.com/eftechcombr/wireguard/pull/54), [#69](https://github.com/eftechcombr/wireguard/pull/69) |
| **Segurança e hardening** | Correção de bug no health check, `entrypoint.sh` endurecido (`set -eo pipefail`), `Dockerfile` otimizado e checkouts de CI fixados | [#52](https://github.com/eftechcombr/wireguard/pull/52) |
| **Observabilidade** | Logs JSON de peers em stdout e OTLP/HTTP, mais ajuste de compatibilidade nas dependências de log do OpenTelemetry | [#59](https://github.com/eftechcombr/wireguard/pull/59), [#68](https://github.com/eftechcombr/wireguard/pull/68) |
| **Reprodutibilidade e qualidade** | Versão do `iptables` fixada (`~1.8.13`) junto ao `wireguard-tools` (`~1.0.20260223`) e pendências do DeepSource resolvidas | [#55](https://github.com/eftechcombr/wireguard/pull/55) |
| **Pipeline de CI/CD** | Build de `dev` removido; imagens Docker agora são geradas apenas ao publicar release ou via `workflow_dispatch` manual (`linux/amd64` + `linux/arm64`) | [#70](https://github.com/eftechcombr/wireguard/pull/70) |
| **Documentação e organização** | Revisão completa do `README.md`, migração do Helm chart para outro repositório, atualização do `docker-compose.yml` e fila de Dependabot | [#41](https://github.com/eftechcombr/wireguard/pull/41), [#43](https://github.com/eftechcombr/wireguard/pull/43), [#46](https://github.com/eftechcombr/wireguard/pull/46) |

---

## 1. Adeus Python: health check reescrito em Go

Antes desta versão, o container carregava um runtime Python 3 inteiro apenas para rodar `wireguard_healthcheck.py`, um servidor HTTP simples escutando na porta `8080/TCP` e lendo `/sys/class/net/wg0/carrier`. Em um container de VPN minimalista, manter Python aumentava o tamanho da imagem e a superfície de manutenção sem necessidade.

No [PR #54](https://github.com/eftechcombr/wireguard/pull/54), o servidor de health check foi reescrito em Go (`main.go`) com testes unitários (`main_test.go`) e compilado de forma estática com `CGO_ENABLED=0` em um `Dockerfile` multi-stage:

- **Sem interpretador em runtime:** Apenas o binário `/wireguard_healthcheck` entra na imagem final baseada em `alpine:3.24`.
- **Mesmo contrato HTTP na porta `8080/TCP`:** Responde a `GET` e `HEAD` com **`200 OK`** quando `/sys/class/net/<interface>/carrier` retorna `1`, e **`503 Service Unavailable`** caso contrário (outros métodos recebem `405 Method Not Allowed`).
- **Interface e porta configuráveis:** Passa a respeitar `WG_INTERFACE` (padrão `wg0`) e `HEALTHCHECK_PORT` / `PORT` (padrão `8080`).

> **Nota de atualização para probes:** Como o `curl` também saiu da imagem de runtime, o `docker-compose.yml` atualizado passou a usar o `wget` do BusyBox no healthcheck nativo do Docker:
> `wget -q --spider http://localhost:8080 || exit 1`.
> Se você tiver scripts ou overrides chamando `curl` dentro do container, troque para `wget` ou aponte uma probe HTTP nativa do Kubernetes diretamente para a porta `8080`.

---

## 2. Alpine 3.24, Go 1.27.4 e pacotes fixados

O `Dockerfile` agora separa claramente compilação e execução:

1. **Estágio de build:** `golang:1.27.4-alpine3.24` ([PR #69](https://github.com/eftechcombr/wireguard/pull/69)) baixa os módulos, compila com `-ldflags="-s -w"` e gera `/wireguard_healthcheck`.
2. **Estágio final:** `alpine:3.24` instala somente `wireguard-tools=~1.0.20260223` e `iptables=~1.8.13` ([PR #55](https://github.com/eftechcombr/wireguard/pull/55)) com `apk add --no-cache`.

Fixar as versões de `wireguard-tools` e `iptables` evita surpresas entre builds consecutivos, enquanto o [PR #55](https://github.com/eftechcombr/wireguard/pull/55) aproveitou para zerar os apontamentos de qualidade do DeepSource no repositório.

---

## 3. Segurança e endurecimento do `entrypoint.sh`

O [PR #52](https://github.com/eftechcombr/wireguard/pull/52) fez uma varredura de segurança no runtime e nos workflows:

- **Correção no health check:** Ajustes no tratamento de estado antes da reescrita em Go.
- **`entrypoint.sh` mais resiliente:** Passou a usar `set -eo pipefail` e protegeu o encerramento da interface (`wg-quick down wg0 || true`) nos sinais `SIGTERM`, `SIGINT` e `SIGQUIT`, garantindo saída limpa mesmo se `wg0` já estiver fora do ar.
- **Otimização do `Dockerfile` e checkouts fixados:** Camadas enxutas e ações de CI fixadas por versão.

---

## 4. Logs estruturados de peers em stdout e OpenTelemetry (OTLP)

Um dos ganhos operacionais mais úteis da `1.0.20260223` é a observabilidade nativa de peers ([PR #59](https://github.com/eftechcombr/wireguard/pull/59), seguida pelo ajuste de compatibilidade das dependências de log do OpenTelemetry no [PR #68](https://github.com/eftechcombr/wireguard/pull/68) e atualizações do Dependabot para `golang.org/x/net`, `google.golang.org/grpc` e `go.opentelemetry.io/otel/trace`).

O serviço em Go emite logs JSON estruturados (`log/slog`) para `stdout` cobrindo:

- **Requisições HTTP no health check** (método, caminho, status, duração)
- **Novos handshakes de peers observados** (chave pública, endpoint, `AllowedIPs` e timestamp do último handshake em segundos Unix)
- **Variações nos contadores de tráfego dos peers** (chave pública, endpoint e variação de RX/TX)

Como o WireGuard não gera um evento explícito de desconexão de peer, o monitor consulta o estado da interface em intervalos configuráveis (`WG_LOG_INTERVAL`, padrão `5s`) e registra handshakes e movimentação de tráfego.

### Exportando logs via OTLP/HTTP

Sem configuração adicional, os logs ficam apenas em `stdout`. Ao definir um endpoint OTLP/HTTP, os mesmos eventos estruturados passam a ser enviados também para o seu OpenTelemetry Collector:

```sh
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318 docker compose up -d
```

Se quiser direcionar apenas o pipeline de logs, use `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`. O nome padrão do serviço (`OTEL_SERVICE_NAME`) é `wireguard`, e as variáveis padrão do OpenTelemetry para cabeçalhos, timeout e atributos de recurso (`OTEL_EXPORTER_OTLP_HEADERS`, `OTEL_EXPORTER_OTLP_LOGS_HEADERS`, `OTEL_EXPORTER_OTLP_TIMEOUT`, `OTEL_RESOURCE_ATTRIBUTES`) são suportadas.

---

## 5. CI/CD orientado a releases e organização do repositório

Antes, o repositório mantinha pipelines separados para as branches `dev` e `latest` no Docker Hub e no GHCR, além de um workflow de Helm chart no mesmo repo. Uma série de PRs simplificou essa estrutura:

- **Helm chart migrado ([PR #43](https://github.com/eftechcombr/wireguard/pull/43)):** O chart Helm foi movido para um repositório próprio, deixando o `eftechcombr/wireguard` focado exclusivamente na imagem de container.
- **Builds somente em release ou dispatch manual ([PR #70](https://github.com/eftechcombr/wireguard/pull/70)):** O build contínuo de `dev` foi removido. Agora as imagens Docker são compiladas e publicadas apenas quando um release é publicado no GitHub ou disparado manualmente, para **`linux/amd64`** e **`linux/arm64`**.
- **Documentação e Compose atualizados ([PR #46](https://github.com/eftechcombr/wireguard/pull/46) e [PR #41](https://github.com/eftechcombr/wireguard/pull/41)):** `README.md` totalmente revisado e `docker-compose.yml` alinhado com as novas variáveis de log e OTLP.
- **Atualizações de Actions via Dependabot:** Workflows atualizados para `actions/checkout` v7, `docker/build-push-action` v7, `docker/login-action` v4, `docker/metadata-action` v6, `docker/setup-qemu-action` v4, `docker/setup-buildx-action` v4, `peter-evans/create-pull-request` v8 e `helm/chart-releaser-action` 1.9.0.

---

## Como baixar e rodar a `1.0.20260223`

Baixe a tag fixa do release (recomendada para produção) ou `latest` no GitHub Container Registry:

```sh
docker pull ghcr.io/eftechcombr/wireguard:1.0.20260223
# ou
docker pull ghcr.io/eftechcombr/wireguard:latest
```

As imagens também seguem publicadas no Docker Hub (`eftechcombr/wireguard`), com suporte multi-arquitetura para `linux/amd64` e `linux/arm64`.

### Requisitos operacionais (Docker Compose)

No deploy, mantenha os parâmetros básicos esperados pelo container:

- **Portas:** `51820/UDP` (VPN WireGuard) e `8080/TCP` (health check HTTP)
- **Capability:** `NET_ADMIN`
- **Sysctl:** `net.ipv4.ip_forward=1`
- **Dispositivo e volume:** `/dev/net/tun` mapeado para o container e `./etc:/etc/wireguard:ro` montado como somente leitura

```yaml
services:
  wireguard:
    image: ghcr.io/eftechcombr/wireguard:1.0.20260223
    cap_add:
      - NET_ADMIN
    sysctls:
      - net.ipv4.ip_forward=1
    volumes:
      - /dev/net/tun:/dev/net/tun
      - ./etc:/etc/wireguard:ro
    ports:
      - "51820:51820/UDP"
      - "8080:8080/TCP"
    environment:
      WG_LOG_INTERVAL: ${WG_LOG_INTERVAL:-5s}
      OTEL_SERVICE_NAME: ${OTEL_SERVICE_NAME:-wireguard}
      OTEL_EXPORTER_OTLP_ENDPOINT: ${OTEL_EXPORTER_OTLP_ENDPOINT:-}
    healthcheck:
      test: ["CMD", "sh", "-c", "wget -q --spider http://localhost:8080 || exit 1"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
    restart: unless-stopped
```

Valide o túnel, os logs e o endpoint de health logo após subir o serviço:

```sh
docker compose up -d
docker exec wireguard wg show
docker logs -f wireguard
curl -i http://localhost:8080
```

---

Conheça mais detalhes na página do produto [WireGuard da EF-TECH](/pt-br/produtos/wireguard/), veja outros artigos técnicos no nosso [blog](/pt-br/blog/) ou [entre em contato](/pt-br/contato/) se quiser ajuda para implantar VPN corporativa em containers com observabilidade centralizada via OpenTelemetry.

## Links e Referências

- **Release `1.0.20260223`** — [github.com/eftechcombr/wireguard/releases/tag/1.0.20260223](https://github.com/eftechcombr/wireguard/releases/tag/1.0.20260223)
- **Changelog completo (`v1.0.20250521...1.0.20260223`)** — [github.com/eftechcombr/wireguard/compare/v1.0.20250521...1.0.20260223](https://github.com/eftechcombr/wireguard/compare/v1.0.20250521...1.0.20260223)
- **Repositório no GitHub** — [github.com/eftechcombr/wireguard](https://github.com/eftechcombr/wireguard)
- **Pacote no GHCR** — [github.com/eftechcombr/wireguard/pkgs/container/wireguard](https://github.com/eftechcombr/wireguard/pkgs/container/wireguard)
- **Docker Hub** — [hub.docker.com/r/eftechcombr/wireguard](https://hub.docker.com/r/eftechcombr/wireguard)
- **Principais Pull Requests:** [#41](https://github.com/eftechcombr/wireguard/pull/41) (Compose), [#43](https://github.com/eftechcombr/wireguard/pull/43) (migração do Helm), [#46](https://github.com/eftechcombr/wireguard/pull/46) (revisão do README), [#52](https://github.com/eftechcombr/wireguard/pull/52) (segurança), [#54](https://github.com/eftechcombr/wireguard/pull/54) (health check em Go), [#55](https://github.com/eftechcombr/wireguard/pull/55) (`iptables` fixado e DeepSource), [#59](https://github.com/eftechcombr/wireguard/pull/59) (logs de peers em stdout e OTLP), [#68](https://github.com/eftechcombr/wireguard/pull/68) (ajuste de dependência OTel), [#69](https://github.com/eftechcombr/wireguard/pull/69) (Go 1.27.4 e Alpine 3.24), [#70](https://github.com/eftechcombr/wireguard/pull/70) (CI/CD por release)

### Origem das notas

Este artigo foi construído a partir da nota diária de **2026-11-13** (`daily/2026-11-13-Fri.md`), da nota de arquitetura `Wireguard` (`Wireguard.md`) e do release publicado no GitHub (`1.0.20260223`):

- `https://github.com/eftechcombr/wireguard/releases/tag/1.0.20260223` — notas de release e lista de PRs
- `https://github.com/eftechcombr/wireguard/compare/v1.0.20250521...1.0.20260223` — comparação completa desde a `v1.0.20250521`
- `https://github.com/eftechcombr/wireguard` — repositório-fonte (`Dockerfile`, `main.go`, `entrypoint.sh`, `docker-compose.yml`, `README.md`)
