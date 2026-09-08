---
title: "GLPI 12.0.0-rc1 and Helm Chart 2.12.0: Subchart Modernization, Security Hardening, and High Availability"
description: "EF-TECH announces the release of GLPI 12.0.0-rc1 and Helm Chart 2.12.0. Discover key updates: Valkey subchart, PDB, HPA, S3 backup, and readOnlyRootFilesystem hardening."
summary: "EF-TECH releases Docker images for GLPI 12.0.0-rc1 and Helm Chart 2.12.0, introducing Valkey subchart support, external cache options, PDB/HPA for php-fpm and nginx, S3 backup CronJob, and enterprise security hardening."
date: 2026-09-06
draft: false
tags: ["glpi", "docker", "kubernetes", "helm", "cloud-native", "security"]
categories: ["infrastructure"]
featureimage: "/img/blog/glpi-12-0-0-rc1/cover.png"
featureimagecaption: "GLPI 12.0.0-rc1 and Helm Chart 2.12.0 from EF-TECH"
---

EF-TECH is excited to announce the release of **GLPI 12.0.0-rc1** (Release Candidate) alongside **Helm Chart version 2.12.0**. This release marks a significant architectural milestone in the evolution of EF-TECH's cloud-native GLPI distribution, bringing subchart modernization, native Valkey cache support, horizontal scalability, automated S3 backups, and enterprise-grade security hardening for Kubernetes clusters.

![GLPI 12.0.0-rc1 and Helm Chart 2.12.0](/img/blog/glpi-12-0-0-rc1/cover.png)

As a **Release Candidate**, this pre-release is designed for teams wanting to evaluate GLPI 12's upcoming capabilities, test new features in staging environments, and validate database and configuration migration paths ahead of the general availability release.

---

## Key Updates and New Features

### 1. Subchart Modernization: Valkey and MariaDB

To stay aligned with current open-source standards and ensure dependable lifecycle management:

- **Valkey Subchart (`helmforge/valkey`)**: Replaced the previous inline Redis subchart with **Valkey**, the high-performance open-source in-memory data store hosted under the Linux Foundation. Valkey handles GLPI session caching and background state efficiently.
- **MariaDB Subchart (`helmforge/mariadb`)**: Replaced inline MariaDB with the modernized and dedicated `helmforge/mariadb` subchart.
- **External Cache Configuration (`externalCache`)**: Added direct configuration parameters for teams deploying against managed cache clusters (such as AWS ElastiCache, Azure Redis, or independent Valkey/Redis instances).

### 2. High Availability and Scalability (PDB and HPA)

To ensure enterprise-grade resilience and smooth traffic handling under heavy loads:

- **PodDisruptionBudget (PDB)**: Added optional PDB configurations for both `php-fpm` and `nginx` pods. This guarantees minimum available replicas during voluntary disruptions like node drains, cluster maintenance, or node pool upgrades.
- **HorizontalPodAutoscaler (HPA)**: Added optional HPA v2 autoscaling support for `php-fpm` and `nginx`, automatically adjusting pod replicas according to CPU and memory utilization thresholds.
- **Workload Scheduling with `priorityClassName`**: Added `priorityClassName` support for GLPI-owned pods, ensuring Kubernetes prioritizes GLPI workload scheduling and prevents preemption by lower-priority workloads.

### 3. Security Hardening and Least Privilege

Security in Kubernetes environments is a core focus at EF-TECH:

- **Root Filesystem Hardening (`readOnlyRootFilesystem`)**: Added optional `readOnlyRootFilesystem: true` hardening, empirically tested and verified for GLPI's runtime needs using appropriate ephemeral volume mounts for temporary paths.
- **Nginx Attack Surface Reduction**: Removed unused volume mounts and database secrets from the Nginx container, strictly following the principle of least privilege.
- **Secret Separation for Databases**: The database password (`MARIADB_PASSWORD`) is now retrieved directly from the MariaDB subchart's Secret.
- **Existing Secret Support for External Databases**: When connecting to an `externalDatabase`, you can supply an `existingSecret` with fast-fail validation to ensure misconfigurations are detected before pods attempt to boot.

### 4. Operational Reliability and S3 Backup

- **Files Backup CronJob to S3-Compatible Storage**: Added a dedicated CronJob to automatically back up uploaded GLPI files and attachments (`/var/lib/glpi/files`) to S3-compatible storage (AWS S3, MinIO, Cloudflare R2, or Ceph).
- **Readiness-Gated Maintenance CronJob**: The maintenance CronJob now actively checks and waits for GLPI application and database readiness, preventing spurious errors during pod rollout or restarts.
- **Resource Presets (`resourcesPreset`)**: Added Bitnami-style resource tiers (`nano`, `micro`, `small`, `medium`, `large`, `xlarge`) to simplify pod resource allocations based on organizational workload requirements.
- **Chart Reorganization & Artifact Hub Compliance**: Chart files have been cleanly reorganized under the standard `helm/` directory structure, resolving all Artifact Hub metadata validations.

---

## Component Matrix

| Componente | Version | Source / Catalog |
|---|---|---|
| GLPI (Application) | `12.0.0-rc1` | [ghcr.io/eftechcombr/glpi](https://github.com/eftechcombr/glpi/packages) |
| Helm Chart | `2.12.0` | [eftech/glpi](https://github.com/eftechcombr/glpi/releases/tag/glpi-2.12.0) |
| Default Cache | Valkey | `helmforge/valkey` |
| Default Database | MariaDB | `helmforge/mariadb` |

---

## Installation and Upgrade Guide

### Upgrading via Helm Chart

Add or update the official EF-TECH Helm repository and run the upgrade:

```bash
# Add or update the EF-TECH Helm repository
helm repo add eftech https://eftechcombr.github.io/glpi/charts
helm repo update

# Install or upgrade to version 2.12.0
helm upgrade --install glpi eftech/glpi \
  --namespace glpi \
  --create-namespace \
  --version 2.12.0
```

### Example `values.yaml` Configuration

Here is an example demonstrating the new high availability, hardening, and resource preset options:

```yaml
# Standardized resource tier
resourcesPreset: "medium"

# Filesystem security hardening
securityContext:
  readOnlyRootFilesystem: true

# High availability with PodDisruptionBudget
podDisruptionBudget:
  enabled: true
  minAvailable: 1

# Horizontal Pod Autoscaling (HPA)
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 8
  targetCPUUtilizationPercentage: 75
  targetMemoryUtilizationPercentage: 80

# Kubernetes scheduling priority
priorityClassName: "system-cluster-critical"

# Modernized Valkey cache
valkey:
  enabled: true

# S3-compatible files backup
backup:
  files:
    enabled: true
    schedule: "0 2 * * *"  # Daily at 02:00 UTC
    s3:
      endpoint: "https://s3.amazonaws.com"
      bucket: "my-glpi-backup-bucket"
      region: "us-east-1"
      existingSecret: "s3-backup-credentials"
```

### Upgrading via Docker

If running standalone containers with Docker or Docker Compose:

```bash
docker pull ghcr.io/eftechcombr/glpi:12.0.0-rc1
```

---

## Useful Links

- [Official EF-TECH GLPI Repository on GitHub](https://github.com/eftechcombr/glpi)
- [GLPI 12.0.0-rc1 Release Notes](https://github.com/eftechcombr/glpi/releases/tag/v12.0.0-rc1)
- [Helm Chart 2.12.0 Release](https://github.com/eftechcombr/glpi/releases/tag/glpi-2.12.0)
- [Docker Image Packages and Releases](https://github.com/eftechcombr/glpi/packages)

---

## Enterprise Support & Consulting

**EF-TECH** specializes in architecting, deploying, and maintaining high-performance ITSM and Service Desk platforms on Kubernetes. We provide enterprise support, migration assistance, and continuous maintenance for containerized GLPI deployments.

Preparing for GLPI 12 or looking to modernize your ITSM infrastructure? [Contact our team](/en/contato/) to speak with an infrastructure specialist.
