---
title: "WireGuard Container 1.0.20260223: Go Health Check, Alpine 3.24, OTLP Peer Logging, and Release-Driven Builds"
description: "EF-TECH's containerized WireGuard image reaches 1.0.20260223 — the largest update since v1.0.20250521. The Python health check is replaced by a static Go binary with stdout and OpenTelemetry peer logging, Alpine moves to 3.24, and CI builds now run strictly on releases or manual dispatch."
summary: "Release 1.0.20260223 of eftechcombr/wireguard drops the Python runtime in favor of a compiled Go health check server, upgrades to Alpine 3.24 and Go 1.27.4, adds structured JSON and OTLP/HTTP peer logging, pins iptables, hardens entrypoint.sh, and switches CI/CD to release-driven multi-arch builds for linux/amd64 and linux/arm64."
date: 2026-11-13
draft: false
tags: ["wireguard", "docker", "vpn", "go", "opentelemetry", "alpine", "ci-cd"]
categories: ["infrastructure"]
---

On November 13, 2026, we published [`eftechcombr/wireguard` **1.0.20260223**](https://github.com/eftechcombr/wireguard/releases/tag/1.0.20260223) — the first release since `v1.0.20250521`, and by far the largest change set in the project's history. It is also the first image built by the new release-driven pipeline introduced in [PR #70](https://github.com/eftechcombr/wireguard/pull/70).

At its core, this release transforms the container from a bash-and-Python wrapper around `wg-quick` into a slimmer, observable, multi-stage **Alpine 3.24** appliance powered by a static **Go 1.27.4** binary for health checks and OpenTelemetry peer logging.

---

## Release Highlights at a Glance

| Area | What Changed | Pull Request |
| --- | --- | --- |
| **Health check rewrite** | Replaced `wireguard_healthcheck.py` with `main.go` and unit tests (`main_test.go`), removing Python from the runtime image | [#54](https://github.com/eftechcombr/wireguard/pull/54) |
| **Base image & toolchain** | Multi-stage build on `golang:1.27.4-alpine3.24` and runtime on `alpine:3.24` | [#54](https://github.com/eftechcombr/wireguard/pull/54), [#69](https://github.com/eftechcombr/wireguard/pull/69) |
| **Security & hardening** | Fixed health check bug, hardened `entrypoint.sh` (`set -eo pipefail`), optimized `Dockerfile`, pinned CI checkouts | [#52](https://github.com/eftechcombr/wireguard/pull/52) |
| **Observability** | Structured JSON peer logging to stdout and OTLP/HTTP export, plus OTel log dependency compatibility fix | [#59](https://github.com/eftechcombr/wireguard/pull/59), [#68](https://github.com/eftechcombr/wireguard/pull/68) |
| **Reproducibility & quality** | Pinned `iptables` (`~1.8.13`) alongside `wireguard-tools` (`~1.0.20260223`) and resolved DeepSource findings | [#55](https://github.com/eftechcombr/wireguard/pull/55) |
| **CI/CD pipeline** | Removed `dev` branch builds; Docker images now publish only on release published or manual `workflow_dispatch` (`linux/amd64` + `linux/arm64`) | [#70](https://github.com/eftechcombr/wireguard/pull/70) |
| **Repo hygiene & docs** | `README.md` overhaul, Helm chart migrated to its own repository, `docker-compose.yml` updated, Dependabot catch-up | [#41](https://github.com/eftechcombr/wireguard/pull/41), [#43](https://github.com/eftechcombr/wireguard/pull/43), [#46](https://github.com/eftechcombr/wireguard/pull/46) |

---

## 1. Dropping Python: Health Check Rewritten in Go

Previously, the container relied on a Python 3 standard-library HTTP server (`wireguard_healthcheck.py`) just to serve port `8080/TCP` and read `/sys/class/net/wg0/carrier`. Carrying the Python runtime inside a minimal Alpine VPN container added unnecessary image weight and maintenance surface.

In [PR #54](https://github.com/eftechcombr/wireguard/pull/54), the health check server was rewritten in Go (`main.go`) with unit tests (`main_test.go`) and compiled statically with `CGO_ENABLED=0` in a multi-stage `Dockerfile`:

- **Zero runtime interpreter:** Only the compiled `/wireguard_healthcheck` binary lands in the final `alpine:3.24` image.
- **Same HTTP contract on `8080/TCP`:** Responds to `GET` and `HEAD` requests with **`200 OK`** when `/sys/class/net/<iface>/carrier` reads `1`, and **`503 Service Unavailable`** otherwise (non-`GET`/`HEAD` methods return `405 Method Not Allowed`).
- **Configurable interface and port:** Honors `WG_INTERFACE` (default `wg0`) and `HEALTHCHECK_PORT` / `PORT` (default `8080`).

> **Upgrade note for health probes:** Because the runtime image no longer includes `curl`, the updated `docker-compose.yml` switches the built-in Docker healthcheck to BusyBox `wget`:
> `wget -q --spider http://localhost:8080 || exit 1`.
> If you have custom Compose overrides or scripts calling `curl` inside the container, switch them to `wget` or use native Kubernetes HTTP `livenessProbe` / `readinessProbe` on port `8080`.

---

## 2. Alpine 3.24, Go 1.27.4, and Pinned Packages

The `Dockerfile` now separates build and runtime cleanly:

1. **Builder stage:** `golang:1.27.4-alpine3.24` ([PR #69](https://github.com/eftechcombr/wireguard/pull/69)) downloads modules, runs the build with `-ldflags="-s -w"`, and outputs `/wireguard_healthcheck`.
2. **Runtime stage:** `alpine:3.24` installs only `wireguard-tools=~1.0.20260223` and `iptables=~1.8.13` ([PR #55](https://github.com/eftechcombr/wireguard/pull/55)) via `apk add --no-cache`.

Pinning both `wireguard-tools` and `iptables` avoids surprise package drift between builds, while [PR #55](https://github.com/eftechcombr/wireguard/pull/55) also cleared outstanding DeepSource code quality issues across the repository.

---

## 3. Security Pass and Hardened Entrypoint

[PR #52](https://github.com/eftechcombr/wireguard/pull/52) focused on tightening both runtime behavior and the build pipeline:

- **Health check bug fix:** Resolved issues in status reporting before the Go rewrite landed.
- **Hardened `entrypoint.sh`:** Enabled `set -eo pipefail` and guarded teardown (`wg-quick down wg0 || true`) on `SIGTERM`, `SIGINT`, and `SIGQUIT` so signal handling remains clean even if the interface was already down.
- **Optimized `Dockerfile` and pinned CI checkouts:** Reduced unnecessary layers and locked GitHub Actions checkouts to controlled versions.

---

## 4. Structured Peer Logging to Stdout and OpenTelemetry (OTLP)

One of the most practical operational upgrades in `1.0.20260223` is built-in peer observability ([PR #59](https://github.com/eftechcombr/wireguard/pull/59), followed by the OTel log dependency compatibility fix in [PR #68](https://github.com/eftechcombr/wireguard/pull/68) and Dependabot bumps for `golang.org/x/net`, `google.golang.org/grpc`, and `go.opentelemetry.io/otel/trace`).

The Go service writes structured JSON logs (`log/slog`) to `stdout` for:

- **HTTP health-check requests** (method, path, status, duration)
- **Newly observed peer handshakes** (public key, endpoint, allowed IPs, latest handshake timestamp in Unix seconds)
- **Peer traffic-counter changes** (public key, endpoint, RX/TX deltas)

Because WireGuard is stateless at the session layer and does not emit an explicit "peer disconnected" event, the monitor polls WireGuard state on a configurable interval (`WG_LOG_INTERVAL`, defaulting to `5s`) and reports handshakes and traffic-counter changes instead.

### Exporting Logs via OTLP/HTTP

By default, logs go to `stdout` only. Set an OTLP/HTTP endpoint and the exact same structured logs are exported to your OpenTelemetry Collector alongside `stdout`:

```sh
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318 docker compose up -d
```

You can also target logs exclusively with `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`, customize `OTEL_SERVICE_NAME` (defaults to `wireguard`), and pass standard OpenTelemetry headers, timeout, and resource attributes (`OTEL_EXPORTER_OTLP_HEADERS`, `OTEL_EXPORTER_OTLP_LOGS_HEADERS`, `OTEL_EXPORTER_OTLP_TIMEOUT`, `OTEL_RESOURCE_ATTRIBUTES`).

---

## 5. Release-Driven Multi-Arch CI/CD and Repo Hygiene

Previously, the repository maintained separate workflows for `dev` and `latest` branches across Docker Hub and GHCR, plus a Helm chart releaser workflow. Several cleanup PRs streamlined that setup:

- **Helm chart decoupled ([PR #43](https://github.com/eftechcombr/wireguard/pull/43)):** The Helm chart was migrated to its own dedicated repository, keeping `eftechcombr/wireguard` focused purely on the container image.
- **Release-driven builds ([PR #70](https://github.com/eftechcombr/wireguard/pull/70)):** The `dev` image workflow was retired. Container images now build and publish **only** when a GitHub release is published or triggered via manual dispatch, targeting **`linux/amd64`** and **`linux/arm64`**.
- **Comprehensive documentation overhaul ([PR #46](https://github.com/eftechcombr/wireguard/pull/46)) and `docker-compose.yml` update ([PR #41](https://github.com/eftechcombr/wireguard/pull/41)):** Synced the README, architecture diagram, file layout, and Compose variables with the Go runtime.
- **Toolchain & GitHub Actions updates:** Dependabot brought the workflows up to `actions/checkout` v7, `docker/build-push-action` v7, `docker/login-action` v4, `docker/metadata-action` v6, `docker/setup-qemu-action` v4, `docker/setup-buildx-action` v4, `peter-evans/create-pull-request` v8, and `helm/chart-releaser-action` 1.9.0.

---

## Pulling and Running `1.0.20260223`

Pull the pinned release tag (recommended for production) or `latest` from GitHub Container Registry:

```sh
docker pull ghcr.io/eftechcombr/wireguard:1.0.20260223
# or
docker pull ghcr.io/eftechcombr/wireguard:latest
```

Images are also published on Docker Hub as `eftechcombr/wireguard`, built for both `linux/amd64` and `linux/arm64`.

### Operational Baseline (Docker Compose)

Keep the minimal runtime requirements in mind when deploying:

- **Ports:** `51820/UDP` (WireGuard VPN) and `8080/TCP` (HTTP health check)
- **Capability:** `NET_ADMIN`
- **Sysctl:** `net.ipv4.ip_forward=1`
- **Device & volume:** `/dev/net/tun` passed into the container and `./etc:/etc/wireguard:ro` mounted read-only

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

Verify the tunnel, logs, and health endpoint after startup:

```sh
docker compose up -d
docker exec wireguard wg show
docker logs -f wireguard
curl -i http://localhost:8080
```

---

Learn more about our [WireGuard enterprise VPN offering](/en/produtos/wireguard/), explore more infrastructure articles on our [blog](/en/blog/), or [contact us](/en/contato/) if you want help rolling out containerized WireGuard with centralized OpenTelemetry observability.

## Links and References

- **Release `1.0.20260223`** — [github.com/eftechcombr/wireguard/releases/tag/1.0.20260223](https://github.com/eftechcombr/wireguard/releases/tag/1.0.20260223)
- **Full Changelog (`v1.0.20250521...1.0.20260223`)** — [github.com/eftechcombr/wireguard/compare/v1.0.20250521...1.0.20260223](https://github.com/eftechcombr/wireguard/compare/v1.0.20250521...1.0.20260223)
- **GitHub Repository** — [github.com/eftechcombr/wireguard](https://github.com/eftechcombr/wireguard)
- **GHCR Package** — [github.com/eftechcombr/wireguard/pkgs/container/wireguard](https://github.com/eftechcombr/wireguard/pkgs/container/wireguard)
- **Docker Hub** — [hub.docker.com/r/eftechcombr/wireguard](https://hub.docker.com/r/eftechcombr/wireguard)
- **Key Pull Requests:** [#41](https://github.com/eftechcombr/wireguard/pull/41) (Compose), [#43](https://github.com/eftechcombr/wireguard/pull/43) (Helm migration), [#46](https://github.com/eftechcombr/wireguard/pull/46) (README overhaul), [#52](https://github.com/eftechcombr/wireguard/pull/52) (security pass), [#54](https://github.com/eftechcombr/wireguard/pull/54) (Go health check), [#55](https://github.com/eftechcombr/wireguard/pull/55) (`iptables` pin & DeepSource), [#59](https://github.com/eftechcombr/wireguard/pull/59) (stdout & OTLP peer logging), [#68](https://github.com/eftechcombr/wireguard/pull/68) (OTel log fix), [#69](https://github.com/eftechcombr/wireguard/pull/69) (Go 1.27.4 & Alpine 3.24), [#70](https://github.com/eftechcombr/wireguard/pull/70) (release-driven CI/CD)

### Where these notes came from

This post is based on the **2026-11-13** daily note (`daily/2026-11-13-Fri.md`), the companion `Wireguard` (`Wireguard.md`) architecture note, and the published GitHub release `1.0.20260223`:

- `https://github.com/eftechcombr/wireguard/releases/tag/1.0.20260223` — release notes and PR list
- `https://github.com/eftechcombr/wireguard/compare/v1.0.20250521...1.0.20260223` — full commit diff since `v1.0.20250521`
- `https://github.com/eftechcombr/wireguard` — source repository (`Dockerfile`, `main.go`, `entrypoint.sh`, `docker-compose.yml`, `README.md`)
