---
title: "Guardrails Outside the Box: OctoDoctor Audits Your Argo CD, OpenShell Isolates Your Agents"
description: "OctoDoctor is a free, read-only, open source binary that scans Argo CD manifests or live clusters and turns 26 anti-patterns into an HTML, JSON and YAML report — with an agent skill and a CI gate built in. That same week, CNCF announced OpenShell in the Sandbox, with per-agent sandboxes, per-request policy and credentials the model never sees."
summary: "Two tools released during KubeCon NA 2026 week attack the same problem from opposite sides: OctoDoctor moves Argo CD configuration review outside the cluster, as a read-only scanner that fails your pipeline; OpenShell moves agent control outside the sandbox, into a supervisor that decides what each binary may do. In both cases, the guardrail lives outside the thing it governs."
date: 2026-11-11
draft: false
tags: ["argocd", "gitops", "kubernetes", "ai-agents", "security", "cncf", "open-source"]
categories: ["infrastructure"]
featureimage: "/img/blog/guardrails-argocd-openshell-agents/cover.png"
featureimagecaption: "On the left, OctoDoctor reading Argo CD configuration; on the right, OpenShell keeping the agent and the key behind a supervisor."
---

Two announcements landed in my feed on the same day and, at first glance, they have nothing in common. The first: Octopus Deploy shipped **OctoDoctor**, a free and open source utility that scans your Argo CD configuration and hands back a report of what is wrong. The second: **OpenShell**, the secure runtime for AI agents started by NVIDIA, entered the CNCF Sandbox — and was one of the foundation's highlights at KubeCon NA 2026.

One is about GitOps YAML. The other is about agents that run shells and hold real credentials. What connects them is the design: **in both cases, the control mechanism sits outside the thing being controlled**. OctoDoctor reads your manifests and never writes to them. OpenShell keeps the supervisor outside the sandbox and the API key out of the agent's reach.

That is the difference between documenting a best practice and making the pipeline stop when it is violated.

![OctoDoctor auditing an Argo CD cluster and OpenShell isolating an agent behind a supervisor](/img/blog/guardrails-argocd-openshell-agents/cover.png)

## OctoDoctor: the anti-pattern guide became an executable

If you have read [Top 30 Argo CD anti-patterns](https://octopus.com/blog/30-argo-cd-antipatterns-for-gitops), you know the problem: the rules are good, but nobody applies them. OctoDoctor is an attempt to close that gap — it packages the best practices Octopus had been publishing in guides and turns them into executable checks.

The scope is honestly narrow. It does not look at your application code, does not evaluate images, and does not replace a policy engine. It reads **Applications, ApplicationSets, AppProjects**, the Argo CD ConfigMaps and Secrets, and cluster Secrets — and ignores everything else. You can point the binary at a repository that also contains other Kubernetes manifests without worrying.

And it is **read-only**. In both execution modes it only reads. You can run it against production without ceremony.

Octopus says the tool was tested on large installations — 100+ clusters and 20,000+ apps — and that its support team uses it as a discovery tool: instead of asking a customer to describe their Argo CD instance, they ask for the report.

### Two modes, the same result

OctoDoctor is a single self-contained binary with no runtime dependencies. Installing it means downloading from the releases page, extracting, and putting it on your `PATH`:

```bash
tar -xzf octodoctor_<version>_linux_amd64.tar.gz
chmod +x octodoctor
./octodoctor --version
```

From there, there are two ways to analyze:

```bash
# 1. Manifests on disk (a GitOps repository checkout)
./octodoctor --directory /path/to/argocd/manifests

# 2. A live cluster: export and analyze in one step
./octodoctor --export --context production --namespace argocd
```

The relevant options:

| Flag | Default | What it does |
| --- | --- | --- |
| `-d, --directory` | current directory | Scans a directory for `.yaml`/`.yml` files |
| `-e, --export` | off | Exports manifests from a live cluster and analyzes them |
| `-c, --context` | current kubeconfig context | Context used for the export |
| `-n, --namespace` | `argocd` | Argo CD namespace for the export |
| `-l, --limit` | 5 | How many files to list per rule in the HTML report |
| `--fail-on` | `medium` | Lowest severity that makes the process exit with code 1: `high`, `medium` or `none` |

`--export` and `--directory` are mutually exclusive. With neither, it analyzes the current directory. Without `--export`, the context and namespace flags are ignored — and the log says so, which is a small detail that prevents a lot of confusion.

The report lands in `octodoctor-output/`, inside the scanned directory:

```text
/path/to/argocd/manifests/
└── octodoctor-output/
    ├── index.html     # open this in a browser
    ├── report.json
    └── report.yaml
```

The HTML report lists at most `--limit` files per rule, so it does not become a wall. The JSON and YAML files contain **every** file, and are the right choice for scripts.

### The part that matters: the exit code

The most useful piece of the design is the output contract. OctoDoctor returns `1` when at least one rule fails and `0` otherwise. That turns it into a pipeline gate with no wrapper:

```bash
# First adoption: observe only, always exit 0
./octodoctor -d ./gitops --fail-on none

# Later: block only high severity failures
./octodoctor -d ./gitops --fail-on high
```

The progression `none` → `high` → `medium` is the right way to introduce a tool like this into a repository that already carries debt. You start by measuring, not by blocking.

### Rules worth reading

The full list has 26 implemented rules, each with severity and per-rule documentation. A few that explain the kind of problem it catches:

| Rule | What it detects | Severity |
| --- | --- | --- |
| R01 | Application with `prune=true` **and** `allowEmpty=true` in its sync policy | High |
| R05 | AppProject with `sourceRepos: "*"` | High |
| R11 | Anonymous user access enabled in Argo CD | High |
| R17 | Parameter overrides on an Application | High |
| R30 | Image Updater without write-back to Git | High |
| R19 | Commit hash or branch name in `targetRevision` (anything other than `HEAD`) | Medium |
| R02 | Application without an automated sync policy | Medium |
| R15/R16 | Hardcoded Helm values or `kustomize` values | Medium |

R01 is the classic that deletes resources by accident when an Application renders empty. R05 and R11 are open doors. R19 is what breaks reproducibility: a `targetRevision` pointing at a branch means "the same commit" can produce different results tomorrow.

None of this replaces understanding your own environment. Octopus itself admits it cannot predict every existing configuration — if a rule fails and you know exactly why, that is expected. The report is the start of a conversation, not a verdict.

### The agent skill

Along with the binary, the project ships a skill called `octodoctor-report`. It uses `octodoctor` from your `PATH` if it is there; if not, it downloads the latest release into a temporary directory and verifies the checksum. It only needs `curl` and `tar`.

```bash
# With the skills CLI
npx skills add OctopusDeploy/octodoctor-argocd --skill octodoctor-report

# Or with the GitHub CLI (gh skill is in preview)
gh skill install OctopusDeploy/octodoctor-argocd octodoctor-report --agent claude-code
```

After that, the interaction is plain language: *"check the Argo CD manifests in ./gitops against best practices"* or *"audit the Argo CD installation in my production cluster"*. The agent picks the mode, runs the tool, and replies with the number of failed rules, the list ordered by severity, and the path to `index.html`.

Two implementation details deserve praise. First: the skill treats exit code `1` as a **normal result**, not an error — that is exactly the right behavior, and it is where many agent integrations with linting tools go wrong. Second: the agent only edits manifests to fix the failures **if you ask it to**.

If you operate Argo CD, it is worth comparing this kind of static verification with recent changes in Argo CD itself. In [Argo CD 3.6](/en/blog/argocd-3-6/), Server-Side Diff started doing a real dry-run against the kube-apiserver to decide whether something is `Synced` — more precision at runtime. OctoDoctor attacks the layer above: the configuration that produced that state. And if you run ApplicationSets at scale, the [dedicated ApplicationSet UI in Argo CD 3.5](/en/blog/argocd-appset-ui/) helps you see what the tool is going to report.

## OpenShell: the guardrail outside the sandbox

The second announcement belongs to a different risk category. An AI agent does more than call APIs: it runs shells, installs packages, reads files, and opens network connections. Often acting on text it read on the internet a minute earlier. As the [CNCF guide for platform engineers](https://www.cncf.io/blog/2026/11/11/openshell-on-kubernetes-a-guide-for-platform-engineers/) puts it: **every agent is untrusted code that holds real credentials**.

[OpenShell](https://github.com/NVIDIA/OpenShell) starts from a simple premise: if the control lives in the prompt, the control does not exist. It runs each agent in a sandbox and puts a **trusted supervisor outside the sandbox** to decide what the agent may reach. Policy is declared in YAML across four dimensions:

| Control | Mechanism | Practical effect |
| --- | --- | --- |
| **Filesystem** | Landlock | Limits read and write paths. In the demo, `/usr` and `/etc` are read-only; only `/sandbox`, `/tmp` and `/dev/null` are writable |
| **Process** | Non-root UID/GID, zero capabilities, seccomp | The agent is not born privileged — and cannot escalate |
| **Network** | Egress denied by default | Rules per binary, host, port and **HTTP method** |
| **Credentials** | Placeholder + swap at the supervisor | The agent never sees the real key; the supervisor injects it only at allowed endpoints |

The network line is the strongest argument. A Kubernetes `NetworkPolicy` can say "this Pod may reach `api.github.com` on 443". It **cannot** say "`curl` may read issues but not create them". OpenShell can — and it can change that rule on a running sandbox without a restart.

### How a sandbox is born on Kubernetes

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

In practice, the create command looks like this:

```bash
openshell sandbox create \
  --workspace demo \
  --name policy-demo \
  --from nicolaka/netshoot@sha256:<digest> \
  --no-auto-providers
```

Note the `@sha256:`. An image by tag is a moving dependency; by digest, it is not.

### Runtime policy, without a restart

Every outbound request from the agent goes through the supervisor, which checks destination, port, calling binary and the HTTP request before opening the connection. That is why the demo case works: `curl` starts out blocked, receives a policy that allows `GET` on `api.github.com`, and keeps getting `policy_denied` on a `POST /issues`.

```bash
openshell policy update <policy-file>   # loads a new version and waits for the sandbox to confirm
openshell logs policy-demo --source sandbox   # shows every allowed and denied request
```

The per-sandbox log, with source `sandbox`, is what turns policy into audit. Without it you have blocking; with it, you have evidence.

### Limits the documentation admits

Two points deserve attention before you put this in production:

- **No CRD yet.** Sandboxes can only be created through the gateway API, not through the Kubernetes API. There is an open issue for an `OpenShellSandbox` CRD and an operator ([openshell#1719](https://github.com/NVIDIA/OpenShell/issues/1719)).
- **One supervisor per agent** provides strong isolation, but may not scale well in large environments. The roadmap discusses flexible deployment options ([RFC 0018](https://github.com/NVIDIA/OpenShell/pull/4377)).

### OpenShell and Agent Substrate: two different problems

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

### Kyverno on top: admission

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

## The common pattern

Back to the two announcements. OctoDoctor takes a document — Argo CD best practices — and turns it into a check that breaks the build. OpenShell takes a prompt instruction — "do not access that" — and turns it into policy enforced by a process the model cannot reach.

In both cases the guardrail is **external, declarative and auditable**. In both cases there is an exit code or an admission event that says "no". And in both cases the tool is explicit about what it does not decide: OctoDoctor cannot tell whether a violation was intentional, and OpenShell leaves it to the platform team to decide which images run, how large a sandbox can get, which credentials each agent receives, and who may touch its RBAC.

That is what separates a best practice from a control. A best practice is what is written down. A control is what happens when someone tries to go against it.

## Getting started

For Argo CD, the shortest path is to run without blocking:

```bash
./octodoctor -d ./gitops --fail-on none
# open ./gitops/octodoctor-output/index.html
```

Read the report with your team, pick the two or three rules that hurt the most, fix them, and only then move to `--fail-on high`.

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

At EF-TECH, we operate Kubernetes clusters with Argo CD and help teams put guardrails around GitOps pipelines and AI workloads without slowing delivery. [Contact us](/en/contato/) if you want to review your Argo CD configuration or design the isolation for your agents. For more articles like this, visit our [blog](/en/blog/).

## Links and References

- **OctoDoctor: check your Argo CD cluster for best practices** — [octopus.com/blog/octodoctor-for-argocd](https://octopus.com/blog/octodoctor-for-argocd)
- **OctoDoctor documentation** — [octodoctor-argocd.readthedocs.io](https://octodoctor-argocd.readthedocs.io/)
- **OctoDoctor repository** — [github.com/OctopusDeploy/octodoctor-argocd](https://github.com/OctopusDeploy/octodoctor-argocd)
- **OctoDoctor releases (binaries and checksums)** — [github.com/OctopusDeploy/octodoctor-argocd/releases](https://github.com/OctopusDeploy/octodoctor-argocd/releases)
- **Top 30 Argo CD anti-patterns** — [octopus.com/blog/30-argo-cd-antipatterns-for-gitops](https://octopus.com/blog/30-argo-cd-antipatterns-for-gitops)
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

Both announcements were captured in the 2026-11-11 daily note, from posts on X (Twitter). Original links and resolved destinations:

- `https://t.co/Exv4ar4B0y` → [octopus.com/blog/octodoctor-for-argocd](https://octopus.com/blog/octodoctor-for-argocd)
- `https://t.co/QaFxfAGfYf` → [CNCF announcement](https://www.cncf.io/announcements/2026/11/10/cncf-hits-major-milestones-with-global-community-growth-record-industry-investment-and-a-new-generation-of-projects-to-build-ai-systems-in-production/)
- `https://t.co/vhJfyRjfMX` (post image) → [x.com/CloudNativeFdn/status/2120250399219188199](https://x.com/CloudNativeFdn/status/2120250399219188199)
