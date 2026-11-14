---
title: "Apple container 1.7.1: Local Kubernetes Clusters in Lightweight macOS VMs"
description: "Apple's container CLI 1.7.1 ships container cluster: lightweight-VM-backed Kubernetes clusters on macOS with automatic kubeconfig setup, heterogeneous worker pools, --shared-image-store (and its security trade-offs), and custom CNI support."
summary: "With release 1.7.1, Apple's native container CLI adds mature local Kubernetes cluster management via container cluster. I walk through the quickstart, named per-branch clusters, heterogeneous worker topologies, node lifecycle isolation, local image sharing with --shared-image-store (including the root/pull-secret caveats), custom Cilium CNI manifests, and the other 1.7.1 runtime improvements."
date: 2026-11-13
draft: false
tags: ["kubernetes", "macos", "containers", "local-development", "cilium"]
categories: ["infrastructure"]
---

On November 6, 2026, Apple shipped [`container` 1.7.1](https://github.com/apple/container/releases/tag/1.7.1), bringing first-class local Kubernetes cluster support via `container cluster` directly into Apple's native macOS container runtime. Instead of running Docker Desktop or a separate Linux VM manager just to test manifests, you can spin up lightweight-VM-backed Kubernetes clusters from the same CLI you use to build and run containers — with automatic `~/.kube/config` registration so `kubectl` and the rest of your Kubernetes tooling work immediately.

## Why run Kubernetes on Apple `container`

Local Kubernetes on macOS usually means trading off startup speed, isolation, or compatibility with standard tools. `container cluster` hits a practical sweet spot:

- **Lightweight VMs per node.** Clusters run as lightweight virtual machines on macOS rather than nested containers inside a single shared Linux VM.
- **Zero kubeconfig wiring.** Creating a cluster automatically registers its context in `~/.kube/config`, so `kubectl`, `helm`, and GitOps CLIs work without extra flags or manual exports.
- **Concurrent, isolated clusters.** Spin up named clusters side by side — for example, one per feature branch or different Kubernetes node versions — without port or state collisions.
- **Direct local image sharing (opt-in).** Images built with `container build` can be consumed inside the cluster without pushing to a remote registry.

## Quickstart

Creating, inspecting, using, and tearing down a default cluster takes five commands:

```sh
# Create a cluster (defaults to "cluster-dev")
container cluster create

# List running clusters
container cluster list

# Verify with kubectl
kubectl cluster-info
kubectl get nodes

# Delete when done
container cluster delete
```

In `1.7.1`, `container cluster list` (and `container cluster ls`) shows one row per cluster by default. Pass `--nodes` when you want one row per node instead. Clusters created with versions earlier than `1.7.1` are not listed.

## Named clusters and concurrent environments

When you omit `--name`, `container cluster create` names the cluster `cluster-dev`. Passing `--name` lets you run multiple environments concurrently on the same Mac:

```sh
container cluster create --name feature-auth
container cluster create --name feature-payments

kubectl --context feature-auth get pods
kubectl config use-context feature-payments
```

For short-lived test runs, `--rm` removes the node containers automatically when they stop. Note that the cluster's stored configuration remains — so it appears as `stopped` in `container cluster list` until you run `container cluster delete --name <name>` or create a new cluster with the same name. Similarly, if a control plane node stops unexpectedly (for instance, after `container system stop`), the recovery path is to delete and recreate the cluster.

## Resource sizing and multi-node topologies

By default, a cluster uses **1/4 of your host CPUs (minimum 2)** and **1/4 of your host memory (minimum 2 GB)**, running a single node that serves as both control plane and worker.

You can override CPU and memory for the control plane (or single node) at creation time:

```sh
container cluster create --name high-resource --cpus 4 --memory 8g
```

To simulate realistic multi-node scheduling, pass `--workers`:

```sh
# Control plane plus 3 dedicated worker nodes
container cluster create --name my-cluster --workers 3
```

When `--workers` is greater than `0`, `container cluster` **taints the control-plane node automatically** so workloads schedule onto workers (`<cluster-name>-worker-<n>`), matching production behavior. Worker nodes share the control plane's `--node-image`.

New in `1.7.1`, you can also size worker pools explicitly — and even mix heterogeneous worker groups by repeating `--workers`:

```sh
# Control plane: 2 CPUs / 4 GB
# 2 heavy workers: 4 CPUs / 8 GB each
# 1 lighter worker: 2 CPUs / 4 GB
container cluster create --name my-cluster --cpus 2 --memory 4g \
  --workers count=2,cpus=4,memory=8g \
  --workers count=1,cpus=2,memory=4g
```

Inside a worker spec, `count` defaults to `1`, and omitted `cpus` or `memory` values fall back to the single-node defaults (1/4 of host resources, minimum 2 CPUs and 2 GB).

## Node lifecycle isolation in 1.7.1

Because each cluster node is backed by a container, older workflows risked breaking a cluster by accidentally stopping or deleting one of its nodes with regular `container` commands. Release `1.7.1` draws a clear boundary:

- `container list` hides cluster nodes, even when `--all` is passed. Use `container cluster list --nodes` to inspect them.
- High-level lifecycle commands — `container start`, `container stop`, `container kill`, and `container delete` — reject cluster node names as not found (while still processing any non-cluster containers passed in the same invocation).
- Read-only and diagnostic commands (`container inspect`, `container logs`, `container exec`, `container stats`, and `container clean`) still work when you target a cluster node by name.

To tear down nodes properly, always use `container cluster delete --name <cluster>`.

## Sharing local images (`--shared-image-store`)

Release `1.7.1` replaces the earlier `load-image` subcommand with `--shared-image-store` on cluster creation:

```sh
container cluster create --name test --shared-image-store
container build -t my-app:dev .
kubectl --context test run my-app --image=my-app:dev --image-pull-policy=Never
```

When enabled, cluster nodes copy image content for their platform directly from your local `container` image store on first use — no local registry container or `push` step required. Image names without a registry (like `my-app:dev`) resolve using your default `registry.domain` and appear inside Kubernetes under their `docker.io` form (for example, `docker.io/library/my-app:dev`).

Three operational details to keep in mind:

1. **All pull policies work**, including `imagePullPolicy: Never`.
2. **Rebuilding the same tag requires care.** If you rebuild `my-app:dev` without bumping the tag, `IfNotPresent` keeps the copy already cached on the node. Either use a new tag per build or set `imagePullPolicy: Always`.
3. **The flag is immutable per cluster.** Sharing is configured at `container cluster create` time; changing it later requires deleting and recreating the cluster.

### Security caveat: why sharing is off by default

The [official cluster documentation](https://github.com/apple/container/blob/1.7.1/docs/cluster.md) highlights two important security consequences of `--shared-image-store`:

- **Any root workload on a node can read your entire local image store.** Privileged pods or pods with a `hostPath` mount can access every image stored locally on your Mac via `container`, including private images you pulled using registry credentials.
- **Local names override registry pulls and bypass pull secrets.** If a local image matches the requested name, the node uses it *before* checking any remote registry, under every pull policy, and without validating the pod's `imagePullSecrets`. (Nodes still cannot modify, add, or delete images in your local store.)

Leave `--shared-image-store` off unless you actually need local-only images in that cluster, and avoid running untrusted manifests or third-party charts with privileged pods in a shared-store cluster.

## Node versions and custom CNIs (Cilium example)

By default, clusters boot `kindest/node:v1.35.5` and install `kindnet` for pod networking. You can pin a different Kubernetes version with `--node-image`:

```sh
container cluster create --node-image docker.io/kindest/node:v1.34.11
```

If you need NetworkPolicies, eBPF observability, or CNI parity with production, pass a plain Kubernetes manifest via `--cni`:

```sh
container cluster create --name my-cluster --cni ./my-cni.yaml
```

Note that `--cni` expects a rendered YAML manifest (the format `kubectl apply -f` consumes), not a Helm chart. For Cilium `1.20.1`, render the manifest with `helm template` first:

```sh
helm repo add cilium https://helm.cilium.io/
helm repo update
helm template cilium cilium/cilium \
  --version 1.20.1 \
  --namespace kube-system \
  --set ipam.mode=kubernetes > cilium.yaml

container cluster create --name cilium-demo --cni ./cilium.yaml
```

Setting `ipam.mode=kubernetes` is essential here: Cilium's default `cluster-pool` mode (`10.0.0.0/8`) overlaps with kubeadm's pod subnet and service CIDR on `container cluster` nodes. Once created, verify with:

```sh
kubectl --context cilium-demo get pods -n kube-system
kubectl --context cilium-demo get nodes -o wide
```

## Other 1.7.1 highlights worth knowing

Beyond `container cluster`, the `1.7.1` release includes several welcome runtime and quality-of-life updates on macOS:

- **Time Machine exclusions:** Image snapshots and container filesystems are now excluded from Time Machine backups automatically, preventing transient container layers from bloating local snapshots and external backup drives.
- **Updated kernel and Containerization:** Default Kata kernel moves to `4.3.1` (`vmlinux-6.18.56-208-debug`) alongside Containerization `0.54.0`.
- **Default DNS in `config.toml`:** Default DNS nameservers, search domains, and options can now be configured persistently in `config.toml`.
- **`cpuUtilization` in `container stats`:** Machine-readable formats (`JSON`, `YAML`, and `TOML`) now report `cpuUtilization`.
- **BuildKit fixes:** Resolves `container build` failures with newer BuildKit versions and missing context errors when steps require the full build context.

## Where it fits in a local workflow

`container cluster` does not try to replace a shared staging cluster, and it should not be confused with production parity for cloud-managed IAM or load balancers. Where it shines is the fast inner loop on Apple Silicon: validating Kubernetes manifests, testing Cilium policies locally, building an image with `container build` and running it in seconds, or keeping separate clusters per branch without paying a heavy VM tax.

At EF-TECH, we help engineering teams design fast, reproducible developer platforms and Kubernetes delivery pipelines. [Contact us](/en/contato/) if you want to streamline your local-to-production Kubernetes workflow, or browse more engineering notes on our [blog](/en/blog/).

## Links and References

- **Apple `container` Cluster Documentation (`1.7.1`)** — [github.com/apple/container/blob/1.7.1/docs/cluster.md](https://github.com/apple/container/blob/1.7.1/docs/cluster.md)
- **Apple `container` Release `1.7.1`** — [github.com/apple/container/releases/tag/1.7.1](https://github.com/apple/container/releases/tag/1.7.1)
- **Apple `container` GitHub Repository** — [github.com/apple/container](https://github.com/apple/container)

### Where these notes came from

These notes originated from the **2026-11-13** daily note (`daily/2026-11-13-Fri.md`), which flagged the release of Kubernetes support in Apple's `container` CLI via:

- `https://t.co/RkbfF72KEC` — short link resolving to `https://github.com/apple/container/blob/1.7.1/docs/cluster.md`
- `https://github.com/apple/container/releases/tag/1.7.1` — the `1.7.1` release notes published November 6, 2026
