---
title: "OctoDoctor: Your Argo CD Anti-Pattern Guide, Now Executable"
description: "OctoDoctor is a free, read-only, open source binary that scans Argo CD manifests or a live cluster and turns 26 anti-patterns into an HTML, JSON and YAML report — with an agent skill and a CI gate built in."
summary: "Octopus Deploy packaged its Argo CD best-practice guides into executable checks. OctoDoctor reads Applications, ApplicationSets, AppProjects and cluster Secrets, never writes to them, and returns an exit code that turns the report into a pipeline gate. I walk through the two modes, the rules that matter, the `none → high → medium` adoption path, and the agent skill that treats exit 1 as a result instead of a failure."
date: 2026-11-11
draft: false
tags: ["argocd", "gitops", "kubernetes", "security", "open-source"]
categories: ["infrastructure"]
featureimage: "/img/blog/octodoctor-argocd-anti-patterns/cover.png"
featureimagecaption: "OctoDoctor inspects Argo CD application manifests like a scanner: the report is the diagnosis, the exit code is the gate."
---

Every Argo CD team I know has read a list of anti-patterns. Very few have a pipeline that stops when one of them shows up. That gap — between the document and the control — is what Octopus Deploy attacked with **OctoDoctor**, a free and open source utility that scans your Argo CD configuration and hands back a report of what is wrong.

If you have read [Top 30 Argo CD anti-patterns](https://octopus.com/blog/30-argo-cd-antipatterns-for-gitops), you know the problem: the rules are good, but nobody applies them. OctoDoctor is an attempt to close that gap — it packages the best practices Octopus had been publishing in guides and turns them into executable checks.

![OctoDoctor scanning a stack of Argo CD application manifests against a checklist](/img/blog/octodoctor-argocd-anti-patterns/cover.png)

## What it reads, and what it ignores

The scope is honestly narrow, and that is a feature. OctoDoctor does not look at your application code, does not evaluate images, and does not replace a policy engine. It reads **Applications, ApplicationSets, AppProjects**, the Argo CD ConfigMaps and Secrets, and cluster Secrets — and ignores everything else. You can point the binary at a repository that also contains other Kubernetes manifests without worrying.

And it is **read-only**. In both execution modes it only reads. You can run it against production without ceremony.

Octopus says the tool was tested on large installations — 100+ clusters and 20,000+ apps — and that its support team uses it as a discovery tool: instead of asking a customer to describe their Argo CD instance, they ask for the report. That detail says a lot about the intended use. The report is not a scoreboard; it is a common language for a conversation about configuration.

## One binary, two modes

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

### What lands on disk

The report lands in `octodoctor-output/`, inside the scanned directory:

```text
/path/to/argocd/manifests/
└── octodoctor-output/
    ├── index.html     # open this in a browser
    ├── report.json
    └── report.yaml
```

The HTML report lists at most `--limit` files per rule, so it does not become a wall. The JSON and YAML files contain **every** file, and are the right choice for scripts. I like this split: the human gets a curated view, the machine gets the whole truth.

## The exit code is the contract

The most useful piece of the design is the output contract. OctoDoctor returns `1` when at least one rule fails and `0` otherwise. That turns it into a pipeline gate with no wrapper:

```bash
# First adoption: observe only, always exit 0
./octodoctor -d ./gitops --fail-on none

# Later: block only high severity failures
./octodoctor -d ./gitops --fail-on high
```

The progression `none` → `high` → `medium` is the right way to introduce a tool like this into a repository that already carries debt. You start by measuring, not by blocking. A team that turns on `--fail-on medium` on day one learns to hate the tool by day three; a team that reads the report first, fixes the two rules that hurt the most, and then raises the bar keeps the tool.

## Rules worth reading

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

## The agent skill

Along with the binary, the project ships a skill called `octodoctor-report`. It uses `octodoctor` from your `PATH` if it is there; if not, it downloads the latest release into a temporary directory and verifies the checksum. It only needs `curl` and `tar`.

```bash
# With the skills CLI
npx skills add OctopusDeploy/octodoctor-argocd --skill octodoctor-report

# Or with the GitHub CLI (gh skill is in preview)
gh skill install OctopusDeploy/octodoctor-argocd octodoctor-report --agent claude-code
```

After that, the interaction is plain language: *"check the Argo CD manifests in ./gitops against best practices"* or *"audit the Argo CD installation in my production cluster"*. The agent picks the mode, runs the tool, and replies with the number of failed rules, the list ordered by severity, and the path to `index.html`.

Two implementation details deserve praise. First: the skill treats exit code `1` as a **normal result**, not an error — that is exactly the right behavior, and it is where many agent integrations with linting tools go wrong. An agent that reads a non-zero exit as a crash will either retry forever or apologize to you instead of showing the report. Second: the agent only edits manifests to fix the failures **if you ask it to**. A scanner that silently rewrites your GitOps repository is a different product with a different risk profile.

## Where this fits next to Argo CD itself

If you operate Argo CD, it is worth comparing this kind of static verification with recent changes in Argo CD itself. In [Argo CD 3.6](/en/blog/argocd-3-6/), Server-Side Diff started doing a real dry-run against the kube-apiserver to decide whether something is `Synced` — more precision at runtime. OctoDoctor attacks the layer above: the configuration that produced that state. And if you run ApplicationSets at scale, the [dedicated ApplicationSet UI in Argo CD 3.5](/en/blog/argocd-appset-ui/) helps you see what the tool is going to report.

That division of labor is the useful part. Argo CD tells you whether the cluster matches the repository. OctoDoctor tells you whether the repository deserves to be matched.

## Getting started

The shortest path is to run without blocking:

```bash
./octodoctor -d ./gitops --fail-on none
# open ./gitops/octodoctor-output/index.html
```

Read the report with your team, pick the two or three rules that hurt the most, fix them, and only then move to `--fail-on high`. If you want the agent route instead, install the `octodoctor-report` skill and ask for the audit in plain language — the first run downloads and verifies the binary for you.

The goal is not to reach zero findings. It is to make the decision visible: every failing rule is now a line in a report you can argue with, instead of a convention nobody checked. That is what separates a best practice from a control — the control is what happens when someone tries to go against it.

At EF-TECH, we operate Kubernetes clusters with Argo CD and help teams put guardrails around GitOps pipelines without slowing delivery. [Contact us](/en/contato/) if you want to review your Argo CD configuration. For more articles like this, visit our [blog](/en/blog/).

## Links and References

- **OctoDoctor: check your Argo CD cluster for best practices** — [octopus.com/blog/octodoctor-for-argocd](https://octopus.com/blog/octodoctor-for-argocd)
- **OctoDoctor documentation** — [octodoctor-argocd.readthedocs.io](https://octodoctor-argocd.readthedocs.io/)
- **OctoDoctor repository** — [github.com/OctopusDeploy/octodoctor-argocd](https://github.com/OctopusDeploy/octodoctor-argocd)
- **OctoDoctor releases (binaries and checksums)** — [github.com/OctopusDeploy/octodoctor-argocd/releases](https://github.com/OctopusDeploy/octodoctor-argocd/releases)
- **Top 30 Argo CD anti-patterns** — [octopus.com/blog/30-argo-cd-antipatterns-for-gitops](https://octopus.com/blog/30-argo-cd-antipatterns-for-gitops)

### Where these notes came from

The announcement was captured in the 2026-11-11 daily note, from a post on X (Twitter). Original link and resolved destination:

- `https://t.co/Exv4ar4B0y` → [octopus.com/blog/octodoctor-for-argocd](https://octopus.com/blog/octodoctor-for-argocd)
