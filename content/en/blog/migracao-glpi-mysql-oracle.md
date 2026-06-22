---
title: "Migrating GLPI Database: From StatefulSet to MySQL on Oracle Cloud"
description: "We migrated the GLPI database from a Kubernetes StatefulSet to Oracle Cloud's free MySQL instance. Check out the results with Grafana."
summary: "This weekend we migrated the GLPI database that was running on a Kubernetes StatefulSet to Oracle Cloud MySQL HeatWave (Always Free). Grafana monitoring is already showing the first results."
date: 2026-06-22
draft: false
tags: ["glpi", "mysql", "oracle-cloud", "kubernetes", "grafana", "migration", "observability"]
categories: ["infrastructure"]
---

This weekend we migrated the GLPI database — which previously operated inside a **StatefulSet on Kubernetes** — to **MySQL HeatWave** on Oracle Cloud, using the resources from the [Always Free](/en/blog/oracle-always-free/) program.

## The previous setup

EF-TECH's GLPI ran with its database on a Kubernetes StatefulSet with persistent storage via PVC. While functional, this model came with challenges:

- **Manual backup management** — no automated snapshot outside the cluster
- **Cluster resource consumption** — database CPU and memory competed with other workloads
- **MySQL maintenance** — version updates and tuning required manual pod intervention
- **Limited high availability** — the single-replica StatefulSet was a single point of failure

## The solution: Oracle MySQL HeatWave

Oracle Cloud offers a **MySQL HeatWave DB System** under the Always Free program with:

- **50 GB of storage** for data
- **50 GB additional** for automated backups
- **Managed standalone instance** — no worries about OS or MySQL maintenance
- **Automatic backups** — configurable retention at no additional cost

Additionally, by moving out of the Kubernetes cluster, we freed up resources for main workloads and eliminated the complexity of operating a stateful database inside Kubernetes.

## The migration process

The migration was planned for minimal impact:

1. **Provisioning** the MySQL HeatWave DB System on OCI (home region)
2. **Exporting** the database from the Kubernetes StatefulSet using `mysqldump`
3. **Importing** the data into the Oracle Cloud MySQL instance
4. **Updating the connection string** in the GLPI application (ConfigMap + environment variables)
5. **Redirecting traffic** and validating the data
6. **Decommissioning** the old StatefulSet

### Commands used

Exporting data from the StatefulSet:

```bash
kubectl exec -n glpi deployment/glpi-mysql -- \
  mysqldump --all-databases --single-transaction --quick \
  -u root -p"$MYSQL_ROOT_PASSWORD" > glpi-backup.sql
```

Importing into MySQL HeatWave:

```bash
mysql -h <oci-mysql-host> -u admin -p < glpi-backup.sql
```

Updating the configuration in the GLPI ConfigMap:

```bash
kubectl edit configmap glpi-config -n glpi
# Update: GLPI_DB_HOST, GLPI_DB_PORT, GLPI_DB_USER, GLPI_DB_PASSWORD
```

## Observability with Grafana

With the database now running outside the cluster, we took the opportunity to set up monitoring via **Grafana** with MySQL HeatWave metrics. The main dashboards include:

- **Active connections** — number of simultaneous connections to GLPI
- **Queries per second (QPS)** — query volume and load trends
- **Response time (latency)** — p95 and p99 of slowest queries
- **Storage usage** — database growth over time
- **Backups** — automated backup status and retention
- **Alerts** — notifications for connections above threshold, delayed replication, and disk space

![Grafana Dashboard - MySQL HeatWave](/img/blog/glpi-mysql-grafana.png)

## First results

After the first hours of operation, the results are already positive:

| Metric | Before (StatefulSet) | After (MySQL HeatWave) |
|---|---|---|
| Average query latency | ~12 ms | ~4 ms |
| Manual backup time | ~25 min | Automatic (zero effort) |
| Cluster resources freed | — | 2 vCPUs and 4 GB RAM |
| MySQL maintenance | Manual | Managed by Oracle |

## Next steps

Throughout this week we will closely monitor the Grafana metrics to:

1. Validate connection stability between GLPI (on Kubernetes) and MySQL (on OCI)
2. Adjust alert thresholds based on the operational baseline
3. Assess the need for tuning specific GLPI queries
4. Document the process for replication in other environments

---

Is GLPI running on your infrastructure and you want to migrate to a more sustainable model? **EF-TECH** has experience planning and executing database migrations safely with minimal downtime. [Contact us](/en/contato/) to talk.
