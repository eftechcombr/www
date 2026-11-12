---
title: "OpenShell: The Guardrail Lives Outside the Agent Sandbox"
description: "CNCF accepted OpenShell into the Sandbox at KubeCon NA 2026: one sandbox per agent, a trusted supervisor outside it, policy per request — including HTTP method — and credentials the model never sees."
summary: "OpenShell starts from the premise that control written in a prompt is not control. It runs each agent in a sandbox and keeps the supervisor outside, with YAML policy across filesystem, process, network and credentials. I walk through the eight-step Kubernetes control path, the NetworkPolicy-versus-L7 argument, the Kyverno admission layer on top, the comparison with Agent Substrate, and the limits the documentation admits."
date: 2026-11-11
draft: false
tags: ["ai-agents", "security", "kubernetes", "cncf", "open-source"]
categories: ["infrastructure"]
featureimage: "/img/blog/openshell-cncf-agent-sandbox/cover.png"
featureimagecaption: "The agent stays sealed inside the sandbox; the supervisor, the policy layers and the API key stay outside the glass."
---

An AI agent does more than call APIs: it runs shells, installs packages, reads files, and opens network connections. Often acting on text it read on the internet a minute earlier. As the [CNCF guide for platform engineers](https://www.cncf.io/blog/2026/11/11/openshell-on-kubernetes-a-guide-for-platform-engineers/) puts it: **every agent is untrusted code that holds real credentials**.

**OpenShell**, the secure runtime for AI agents started by NVIDIA, entered the CNCF Sandbox and was one of the foundation's highlights at KubeCon NA 2026. It starts from a simple premise: if the control lives in the prompt, the control does not exist. It runs each agent in a sandbox and puts a **trusted supervisor outside the sandbox** to decide what the agent may reach.

![A robot agent sealed inside a glass sandbox, with the supervisor and the API key outside the dome](/img/blog/openshell-cncf-agent-sandbox/cover.png)

## Where the control lives

The design decision is architectural, not procedural. A system prompt that says "do not touch production" is a suggestion the model may follow or ignore, and it is invisible to your audit trail. A supervisor outside the sandbox is a process the model cannot reach, cannot edit, and cannot talk its way past.

Policy is declared in YAML across four dimensions:

| Control | Mechanism | Practical effect |
| --- | --- | --- |
| **Filesystem** | Landlock | Limits read and write paths. In the demo, `/usr` and `/etc` are read-only; only `/sandbox`, `/tmp` and `/dev/null` are writable |
| **Process** | Non-root UID/GID, zero capabilities, seccomp | The agent is not born privileged — and cannot escalate |
| **Network** | Egress denied by default | Rules per binary, host, port and **HTTP method** |
| **Credentials** | Placeholder + swap at the supervisor | The agent never sees the real key; the supervisor injects it only at allowed endpoints |

### Why a NetworkPolicy is not enough

The network line is the strongest argument in the whole design, and the easiest one to underestimate.

A Kubernetes `NetworkPolicy` can say "this Pod may reach `api.github.com` on 443". It **cannot** say "`curl` may read issues but not create them". Both requests are the same destination, the same port and the same protocol; they differ only inside the TLS session, at the HTTP layer.

OpenShell can make that distinction — and it can change the rule on a running sandbox without a restart. That is the difference between network isolation and capability control.

## How a sandbox is born on Kubernetes

OpenShell does not bring its own scheduler. The Kubernetes backend uses [Agent Sandbox](https://agent-sandbox.sigs.k8s.io/), the `Sandbox` resource from `agents.x-k8s.io` maintained by SIG Apps. In practice, agents show up as Pods, Services, PVCs, Secrets and NetworkPolicies — objects you already know how to operate.

The control path, in short:

1. **Preparation.** A CNI that enforces both ingress and egress NetworkPolicy, the Agent Sandbox controller and CRDs, then the OpenShell gateway Helm chart.
2. **Creation.** `openshell sandbox create` talks to the gateway over mTLS. Clients never talk to the Kubernetes API directly.
3. **Recording.** The gateway authenticates the caller, resolves image, policy, providers and resources, and writes the sandbox record in the `Provisioning` phase. That record — not the Pod — is the source of truth.
4. **Network first.** The driver creates two NetworkPolicies in the namespace: workloads get no egress at all and ingress only from supervisors on 5500; and the supervisor side. Only then is the `Sandbox` resource created, already suspended.
5. **Workload.** Agent Sandbox creates the workload Pod and a PVC for `/sandbox`, with a scheduling gate holding the Pod back.
6. **Verification.** The driver reads the admitted Pod back and checks non-root UID/GID, no added capabilities, `RuntimeDefault` seccomp, no host namespaces, no ServiceAccount token, and the expected labels and volumes. If an admission webhook changed any of it, creation fails.
7. **Supervisor.** A supervisor Pod, a Service in front of the workload's port 5500, TLS and bootstrap Secrets, and a short-lived token. The workload never receives gateway credentials.
8. **Connection.** The supervisor authenticates with an identity tied to the namespace, the Sandbox UID, its own Pod UID and the runtime generation. Only then are the scheduling gates released. Inside the workload, filesystem, process, socket and DNS controls are applied **before** the agent's command starts.

The ordering is the interesting part. Network policy exists before the workload does. The workload is suspended until its identity is verified. The supervisor is trusted because it proved who it is, not because it lives in a privileged namespace.

### The create command

In practice, the create command looks like this:

```bash
openshell sandbox create \
  --workspace demo \
  --name policy-demo \
  --from nicolaka/netshoot@sha256:<digest> \
  --no-auto-providers
```

Note the `@sha256:`. An image by tag is a moving dependency; by digest, it is not. That single character is the difference between "we tested this image" and "we tested an image that had that name at the time".

## Runtime policy, without a restart

Every outbound request from the agent goes through the supervisor, which checks destination, port, calling binary and the HTTP request before opening the connection. That is why the demo case works: `curl` starts out blocked, receives a policy that allows `GET` on `api.github.com`, and keeps getting `policy_denied` on a `POST /issues`.

```bash
openshell policy update <policy-file>   # loads a new version and waits for the sandbox to confirm
openshell logs policy-demo --source sandbox   # shows every allowed and denied request
```

The per-sandbox log, with source `sandbox`, is what turns policy into audit. Without it you have blocking; with it, you have evidence. When the security team asks what the agent actually did last Tuesday, that log is the answer.

## Limits the documentation admits

Two points deserve attention before you put this in production:

- **No CRD yet.** Sandboxes can only be created through the gateway API, not through the Kubernetes API. There is an open issue for an `OpenShellSandbox` CRD and an operator ([openshell#1719](https://github.com/NVIDIA/OpenShell/issues/1719)).
- **One supervisor per agent** provides strong isolation, but may not scale well in large environments. The roadmap discusses flexible deployment options ([RFC 0018](https://github.com/NVIDIA/OpenShell/pull/4377)).

The absence of a CRD is the one that changes your operational model today: GitOps workflows that expect a Kubernetes object to reconcile do not apply yet. You create sandboxes through the gateway, and the gateway's record is the source of truth.

## OpenShell and Agent Substrate: two different problems

OpenShell and [Agent Substrate](https://github.com/agent-substrate/substrate) (Google) both entered the CNCF Sandbox in September 2026, two days apart, and it is easy to treat them as competitors. They answer different questions:

| | OpenShell | Agent Substrate |
| --- | --- | --- |
| Origin | NVIDIA | Google |
| Main question | **What may this agent do?** | **How do we run thousands of mostly idle agents cheaply?** |
| Unit of work | One sandbox per agent: a Sandbox, a workload Pod and a supervisor Pod | An actor: identity + snapshot, running in shared worker Pods |
| Kubernetes building block | Agent Sandbox (`agents.x-k8s.io`) | Its own `WorkerPool` CRD (`ate.dev`) |
| Isolation | Standard container + Landlock + seccomp (a stronger RuntimeClass is optional) | gVisor or Cloud Hypervisor required per actor |
| State | A `/sandbox` PVC that survives stop/start | RAM and filesystem snapshots in object storage |
| Scaling | HPA on the gateway (more than one replica needs external PostgreSQL) | HPA on the `WorkerPool`, which has a `/scale` subresource |
| Maturity | v0.1.x | Pre-1.0 |

The rule of thumb: **bursty, mostly idle agents, one per user, with cost per agent as the main metric → Substrate. Agents holding real credentials and reaching production systems, with a need for per-request control → OpenShell.** Large enterprises will likely want both, and there is ongoing work to let OpenShell accept pluggable isolation backends — including a Substrate backend.

## Kyverno on top: admission

OpenShell checks the Pod settings it depends on to stay safe. The rest belongs to the platform team — and that is where admission control comes in. The Nirmata demo shows seven Kyverno policies in `Enforce` mode, written in CEL:

| Control | Attempt | Result |
| --- | --- | --- |
| Pod security | A container with `privileged: true` | Denied: non-root, dropped capabilities and `allowPrivilegeEscalation: false` are mandatory |
| RBAC | A Role named `openshell-*` granting `*` on `*` | Denied: OpenShell RBAC rules may not contain wildcards |
| Network | A patch that allows all egress on the workloads NetworkPolicy | Denied: workloads may not have direct egress |
| Supply chain | The `nicolaka/netshoot:v0.13` image (tag) | Denied: sandbox images must use `sha256` digests |
| Resources | A Sandbox with no resources / asking for 8 CPU and 16Gi | Gets defaults (`100m` CPU) / denied above 4 CPU, 8Gi and 20Gi ephemeral |
| Credentials | `envFrom` with a Kubernetes Secret | Denied: use OpenShell providers instead of injecting Secrets |

The important detail: the policies look at the **request**, not the sender. Even a compromised gateway cannot push a privileged, unpinned or oversized sandbox through admission. But the gateway's ServiceAccount can still create Pods and NetworkPolicies directly in the namespace — in production, extend the policies to Pods and to any NetworkPolicy that selects OpenShell workloads.

And there is the hole admission control cannot cover by definition: a Deployment from your own team calling `api.openai.com` never goes through the gateway or a supervisor. For that case, kernel monitors such as [Runtime for Kyverno](https://github.com/nirmata/runtime) run as a DaemonSet, attach eBPF programs and report `exec`, file opens, network and DNS as `OpenReports`.

That is the honest boundary of this architecture. OpenShell governs what goes through it. Admission governs what can be created. Kernel telemetry is what remains for everything that never asks permission.

## Getting started

For OpenShell, the Nirmata demo brings everything up on a two-node kind cluster (Kubernetes 1.35, Cilium 1.20, Agent Sandbox v1.0.5, OpenShell 0.1.3, Kyverno 1.18.2):

```bash
git clone https://github.com/nirmata/demo-openshell
cd demo-openshell
./scripts/setup.sh && ./scripts/install-cli.sh && ./scripts/verify.sh
./scripts/demo.sh           # OpenShell L7 policy
./scripts/kyverno-demo.sh   # Kyverno admission policies
./scripts/cleanup.sh
```

You need Docker, kind, kubectl, Helm, curl, SSH and nc. It is the cheapest way I know to watch `policy_denied` actually happen before you bring this to the security team.

The point is not to make the agent harmless. It is to make its permissions explicit, small and revocable — and to keep the decision outside the reach of the thing being decided about.

At EF-TECH, we operate Kubernetes clusters and help teams design isolation for AI workloads without slowing delivery. [Contact us](/en/contato/) if you want to design the guardrails for your agents. For more articles like this, visit our [blog](/en/blog/).

## Links and References

- **CNCF announcement at KubeCon NA 2026 (OpenShell and Agent Substrate in the Sandbox)** — [cncf.io/announcements/2026/11/10/...](https://www.cncf.io/announcements/2026/11/10/cncf-hits-major-milestones-with-global-community-growth-record-industry-investment-and-a-new-generation-of-projects-to-build-ai-systems-in-production/)
- **OpenShell project page on CNCF** — [cncf.io/projects/openshell](https://www.cncf.io/projects/openshell/)
- **OpenShell on GitHub** — [github.com/NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell)
- **OpenShell documentation (architecture and Kubernetes setup)** — [docs.nvidia.com/openshell/latest](https://docs.nvidia.com/openshell/latest/)
- **OpenShell on Kubernetes: a guide for platform engineers** — [cncf.io/blog/2026/11/11/openshell-on-kubernetes-a-guide-for-platform-engineers](https://www.cncf.io/blog/2026/11/11/openshell-on-kubernetes-a-guide-for-platform-engineers/)
- **Agent Sandbox (SIG Apps)** — [agent-sandbox.sigs.k8s.io](https://agent-sandbox.sigs.k8s.io/)
- **Agent Substrate** — [github.com/agent-substrate/substrate](https://github.com/agent-substrate/substrate)
- **OpenShell on Kubernetes demo (Nirmata)** — [github.com/nirmata/demo-openshell](https://github.com/nirmata/demo-openshell)
- **Runtime for Kyverno (eBPF monitoring)** — [github.com/nirmata/runtime](https://github.com/nirmata/runtime)
- **KubeCon + CloudNativeCon North America 2026** — [events.linuxfoundation.org/kubecon-cloudnativecon-north-america](https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/)

### Where these notes came from

The announcement was captured in the 2026-11-11 daily note, from posts on X (Twitter). Original links and resolved destinations:

- `https://t.co/QaFxfAGfYf` → [CNCF announcement](https://www.cncf.io/announcements/2026/11/10/cncf-hits-major-milestones-with-global-community-growth-record-industry-investment-and-a-new-generation-of-projects-to-build-ai-systems-in-production/)
- `https://t.co/vhJfyRjfMX` (post image) → [x.com/CloudNativeFdn/status/2120250399219188199](https://x.com/CloudNativeFdn/status/2120250399219188199)
