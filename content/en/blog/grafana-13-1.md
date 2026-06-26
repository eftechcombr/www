---
title: "Grafana 13.1: What's new in observability as code, Grafana Assistant, and more"
description: "Grafana 13.1 ships Git Sync GA, Grafana Assistant expanded to 8 new data sources, section-level variables, redesigned query editor, and PDC additions."
summary: "Grafana 13.1 brings Git Sync to GA with signed commits, Grafana Assistant support for Oracle, MongoDB, Elasticsearch and more, section-scoped variables, a redesigned query editor, and three new PDC data sources. A practical overview for observability practitioners."
date: 2026-06-26
draft: false
tags: ["grafana", "observability", "monitoring", "devops"]
categories: ["infrastructure"]
---

Grafana Labs has released version 13.1, building on the foundation laid by Grafana 13 which brought Git Sync to general availability. This release is especially relevant for teams embracing observability as code, managing dynamic dashboards across multiple services, or connecting to on-premise data sources through secure tunnels.

Here is a breakdown of the key changes organized by area of interest.

## Git Sync: Observability as code matures

Git Sync, which reached GA in Grafana 13, continues to receive meaningful improvements in 13.1. For teams managing dashboards as code, this remains the centerpiece of the release.

### Dashboard import into provisioned folders (GA)

Dashboards can now be imported directly into folders managed by provisioning. This means you can define your folder structure through configuration files and have Git-synced dashboards land in the correct location automatically, without manual intervention.

### Root-level sync (GA)

Support for syncing from the repository root removes the need for specific directory structures. Simply configure the desired path and Grafana interprets your repository's natural layout.

### README.md rendering in Git Sync folders (public preview)

Folders synced via Git Sync now display the repository's `README.md` file directly inside Grafana. This enables inline documentation for each dashboard set, especially useful for teams maintaining multiple observability repositories.

### Signed commits with GPG, SSH, and S/MIME (GA)

Every change made through Git Sync can be digitally signed, ensuring traceability and compliance. Support covers GPG, SSH, and S/MIME, suiting teams from small setups to enterprise environments with strict auditing policies.

### GitHub App, GitLab, and BitBucket integration

Git Sync supports authentication via GitHub App (recommended for GitHub-based organizations), GitLab, BitBucket, and plain Git connections, covering most real-world scenarios.

## Grafana Assistant expands to 8 new data sources

The AI-powered assistant that helps users build queries and interpret metrics now supports eight additional data sources:

- **Snowflake** — cloud data warehouse
- **Oracle** — enterprise relational database
- **Elasticsearch** — log search and analytics
- **Dynatrace** — application performance monitoring
- **Honeycomb** — event-driven observability
- **Zabbix** — open source infrastructure monitoring
- **Jira** — project management and ticketing
- **MongoDB** — NoSQL database

### Availability

The Grafana Assistant comes **pre-installed with Grafana Enterprise** (no extra plugin required). OSS users can install it from the plugin catalog, which requires a Grafana Cloud account.

For organizations running mixed stacks, the addition of Oracle, Elasticsearch, and MongoDB means the assistant can now help across a broader range of backend technologies.

## Dashboarding improvements

The dashboard authoring and consumption experience received several updates in 13.1.

### Section-level variables (GA)

This is one of the most requested community features. Previously, variables like `$service` or `$environment` applied globally across the entire dashboard. Now you can define **variables scoped to rows and tabs**, allowing each dashboard section to have its own context.

Practical example: in a dashboard monitoring both production and staging side by side, you can have a different `$service` variable per row without conflicts.

### Redesigned query editor (public preview)

The query editor has been reworked for productivity:

- **Multi-select and bulk actions** — select multiple queries at once to edit, duplicate, or delete
- **Stacked view** — side-by-side visualization of open queries for easier comparison

For teams maintaining dashboards with dozens of panels, the time savings are substantial.

### Quick filters and data grouping (GA)

Quick filters let you apply ad-hoc filters without modifying underlying queries. Data grouping is now stable and works directly from the UI, simplifying the creation of aggregated views.

### Series visibility in time series legends

Time series chart legends now include per-series visibility controls. You can hide or show individual lines directly from the legend, useful in dashboards with multiple overlapping metrics.

### Enhanced nested tables

Nested tables received improvements in:

- **Configurable grouping** — define how data is grouped within each cell
- **Cell styling** — conditional formatting with colors and styles
- **Improved aggregations** — new aggregation functions for summarizing nested data

### Copy and paste panel styles (GA)

You can now copy style configuration from one panel and apply it to another, eliminating the need to manually reconfigure colors, thresholds, and formatting.

### Panel style presets (GA)

Grafana 13.1 includes curated style presets — combinations of colors, thresholds, and formatting for common panel types (bar charts, gauges, tables, etc.). This accelerates dashboard creation while maintaining visual consistency.

## PDC (Private Data Source Connect): new data sources

PDC, which enables secure encrypted tunnel connections to data sources on private networks, now supports three new types:

- **MQTT** — IoT (Internet of Things) protocol
- **GitHub** — GitHub API for repository metrics
- **IBM Db2** — IBM relational database

These additions extend PDC reach to IoT scenarios, DevOps integration, and legacy enterprise databases, all while keeping traffic encrypted between Grafana and the data source.

## Conclusion

Grafana 13.1 solidifies Git Sync as a mature tool for observability as code, expands the AI assistant to data sources widely used in enterprise environments, and delivers practical improvements for day-to-day dashboard work.

For Grafana Enterprise users, the highlight is the built-in Grafana Assistant with no additional plugins required. For OSS users, the Git Sync enhancements, section-level variables, and redesigned query editor are the strongest reasons to upgrade.

At EF-TECH, we help companies implement and manage Grafana observability solutions. [Contact us](/en/contato/).
