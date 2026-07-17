---
title: "Argo CD 3.5 Ships a Dedicated ApplicationSet UI: Managing GitOps at Scale"
description: "Argo CD v3.5 introduces a first-class ApplicationSet UI with resource trees, health status, editable preview, and owner badges. A deep dive into what changes for GitOps teams."
summary: "Argo CD v3.5 ships a dedicated ApplicationSet UI after a long-running community request. The new interface includes list pages with search and filters, a resource tree showing parent-child relationships between ApplicationSets and generated Applications, first-class health status, an editable YAML preview mode, and owner badges for traceability. An overview of the features and limitations."
date: 2026-07-17
draft: false
tags: ["argocd", "kubernetes", "gitops", "applicationset"]
categories: ["infrastructure"]
---

Argo CD has long been celebrated for its user interface — resource trees, real-time sync status, clean diff views — which made GitOps accessible to teams that do not live in YAML. ApplicationSets, however, fit awkwardly into that picture. Until now.

With version 3.5, Argo CD ships a first-class ApplicationSet UI, addressing a feature request that accumulated 189 thumbs-up reactions. This article walks through what is shipping and why it matters for teams managing GitOps at scale.

## The ApplicationSet visibility gap

ApplicationSets are a factory pattern for Applications. You write a single resource that says "for every cluster matching this label, generate an Application from this template," and the controller produces N child Applications. A single ApplicationSet can fan out across dozens of clusters and hundreds of repositories.

Before 3.5, operators had two options to inspect ApplicationSets: use `kubectl` or `argocd appset` on the CLI, or wrap the ApplicationSet inside an App-of-Apps and browse through the parent Application's resource tree. Neither approach is ideal for production environments running tens or hundreds of ApplicationSets.

## What the new UI brings

The new interface is accessible via the `/applicationsets` route and a dedicated navigation bar item.

### List page with familiar controls

The ApplicationSet list page mirrors the Application list — substring search, filters, a health-summary pie chart, and toggleable layouts. RBAC policies are enforced exactly as on the CLI.

### Resource tree showing the family tree

Each ApplicationSet is displayed as a root node with every generated child Application as a downstream node. Clicking a child jumps directly to its details page, making it straightforward to trace the relationship between a generator template and its deployed instances.

### Health as a first-class field

The ApplicationSet controller now writes `status.health` derived from status conditions, with three possible states: Healthy, Degraded, and Progressing. Conditions are exposed through the UI, giving operators the same health awareness they already have for individual Applications.

### Slide-out panel

Clicking an ApplicationSet node or its Details button opens a slide-out panel with four tabs: Summary, Manifest, Events, and Preview.

### ApplicationSet Preview

The Preview tab mirrors `argocd appset generate` directly in the browser. You can edit the ApplicationSet spec YAML, change generators, and re-run the preview. Three views are available: LIVE APPS (current state), DIFF (what would change), and DESIRED APPS (generated output).

### App-of-AppSet preview

For teams using the App-of-Apps pattern, the preview also works from the parent Application, showing which child Applications would change on the next sync.

### Owner badges and synthetic root node

Child Applications display an owner badge with the parent ApplicationSet name. A toggle-able synthetic root node icon can also be added to child Application resource trees for additional context.

## Limitations to keep in mind

The ApplicationSet UI is read-only in this alpha phase. Create, update, and delete operations still flow through Git, preserving the Git-as-source-of-truth model. The feature ships as alpha in 3.5, so look and behavior may change before reaching stable.

Availability: Argo CD 3.5 release candidate ships June 16, 2026, with general availability on August 4, 2026.

## Practical implications for GitOps teams

For organizations managing multi-cluster deployments with ApplicationSets, the new UI closes a significant observability gap. Operators no longer need to switch between CLI and UI to understand the state of their ApplicationSets. The resource tree visualization makes it immediately clear which Applications a given generator produced and whether those Applications are healthy.

The Preview feature is particularly valuable for teams experimenting with new generators or templates. Being able to iterate on the ApplicationSet spec and see the live diff before committing to Git reduces the feedback loop from minutes to seconds.

## Conclusion

Argo CD 3.5's ApplicationSet UI is a milestone for the project. It brings ApplicationSets out of the YAML-only realm and into the visual interface that made Argo CD popular in the first place. While the alpha release is read-only, the foundation is solid and addresses the most pressing visibility needs for ApplicationSet operators.

At EF-TECH, we help companies implement and manage GitOps workflows with Argo CD at scale. [Contact us](/en/contato/).
