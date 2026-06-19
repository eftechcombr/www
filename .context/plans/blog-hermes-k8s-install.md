---
status: filled
generated: 2026-06-19
agents:
  - type: "documentation-writer"
    role: "Write bilingual blog post content (en/pt-br) explaining how to install Hermes agent on Kubernetes"
  - type: "devops-specialist"
    role: "Review Kubernetes manifests for accuracy and best practices"
  - type: "code-reviewer"
    role: "Review blog post for technical accuracy and completeness"
docs:
  - "content/pt-br/blog/"
  - "content/en/blog/"
phases:
  - id: "phase-1"
    name: "Content Planning & Outline"
    prevc: "P"
    agent: "documentation-writer"
  - id: "phase-2"
    name: "Write Blog Post Content"
    prevc: "E"
    agent: "documentation-writer"
  - id: "phase-3"
    name: "Review & Build Verification"
    prevc: "V"
    agent: "code-reviewer"
---

# Blog Hermes K8s Install Plan

> Create a bilingual blog post (en/pt-br) teaching how to install the Hermes agent on Kubernetes. The post will walk through each Kubernetes resource from the manifests in `../iac/files/kubernetes/hermes`, explaining what each component does and how to deploy them with `kubectl`/`kustomize`. The post should include prerequisites, step-by-step instructions, configuration options, and verification steps.

## Task Snapshot
- **Primary goal:** Publish a technical blog post on eftech.com.br teaching users how to deploy the Hermes agent on Kubernetes
- **Success signal:** Blog post builds successfully with `hugo --gc --minify`, internal links use trailing slashes, and content is published in both pt-br and en
- **Key references:**
  - [Existing blog posts](../content/pt-br/blog/) for formatting conventions
  - [Kubernetes manifests](../../iac/files/kubernetes/hermes/) as technical reference

## Agent Lineup
| Agent | Role in this plan | Playbook | Focus |
| --- | --- | --- | --- |
| Documentation Writer | Write bilingual content (en/pt-br) | [Documentation Writer](../agents/documentation-writer.md) | Write clear, accurate, engaging technical blog posts |
| DevOps Specialist | Review Kubernetes accuracy | [DevOps Specialist](../agents/devops-specialist.md) | Validate k8s manifests, commands, and deployment steps |
| Code Reviewer | Quality assurance | [Code Reviewer](../agents/code-reviewer.md) | Verify technical accuracy and formatting |

## Working Phases

### Phase 1 — Content Planning & Outline (P)
> **Primary Agent:** `documentation-writer`

**Objective:** Define the structure and scope of the blog post for both languages.

**Tasks**

| # | Task | Agent | Status | Deliverable |
|---|------|-------|--------|-------------|
| 1.1 | Analyze Kubernetes manifests in `../iac/files/kubernetes/hermes` to understand each resource | `documentation-writer` | pending | Summary of each resource and its purpose |
| 1.2 | Review existing blog posts for format, tone, and structure conventions | `documentation-writer` | pending | Format reference notes |
| 1.3 | Create detailed outline for pt-br and en versions | `documentation-writer` | pending | Outline document |

**Proposed Outline:**
1. Introduction — what is Hermes agent and why run it on Kubernetes
2. Prerequisites — kubectl, kustomize, Kubernetes cluster, cert-manager, storage class
3. Step 1: Create the namespace
4. Step 2: ConfigMap configuration (environment variables)
5. Step 3: Secrets (external, via Reloader)
6. Step 4: PersistentVolumeClaim for data storage
7. Step 5: Deployment — container spec, probes, resource limits
8. Step 6: Services — Gateway, Dashboard, Webhook
9. Step 7: TLS certificate with cert-manager (Issuer)
10. Step 8: Ingress configuration (optional)
11. Apply everything with kustomize
12. Verification — health checks, logs, dashboard access
13. Conclusion + call to action

---

### Phase 2 — Write Blog Post Content (E)
> **Primary Agent:** `documentation-writer`

**Objective:** Write the full blog post in both Portuguese and English.

**Tasks**

| # | Task | Agent | Status | Deliverable |
|---|------|-------|--------|-------------|
| 2.1 | Write Portuguese version (`content/pt-br/blog/hermes-k8s-install.md`) | `documentation-writer` | pending | pt-br blog post markdown |
| 2.2 | Write English version (`content/en/blog/hermes-k8s-install.md`) | `documentation-writer` | pending | en blog post markdown |
| 2.3 | Verify both files follow front matter conventions and internal link format | `documentation-writer` | pending | Self-review |

**Content Requirements:**
- Front matter: `title`, `description`, `summary`, `date`, `draft: false`, `tags`, `categories`
- Tags: `hermes`, `kubernetes`, `k8s`, `devops`, `deploy` (pt-br: `hermes`, `kubernetes`, `k8s`, `devops`, `implantacao`)
- Categories: `devops` / `infraestrutura`
- Internal links must use trailing slashes (e.g., `/contato/`)
- Include code blocks with YAML snippets from the manifests
- Include kubectl/kustomize commands in code blocks
- End with CTA linking to `/contato/`

---

### Phase 3 — Review & Build Verification (V)
> **Primary Agent:** `code-reviewer`

**Objective:** Verify technical accuracy and ensure the site builds cleanly.

**Tasks**

| # | Task | Agent | Status | Deliverable |
|---|------|-------|--------|-------------|
| 3.1 | Verify Kubernetes commands and manifest references are accurate | `devops-specialist` | pending | Technical accuracy sign-off |
| 3.2 | Run `hugo --gc --minify` to verify build | `code-reviewer` | pending | Clean build output |
| 3.3 | Verify internal links use trailing slashes | `code-reviewer` | pending | Link check pass |
| 3.4 | Cross-link post in `.context/docs/README.md` if applicable | `documentation-writer` | pending | Updated index |

## Success Criteria
- `hugo --gc --minify` completes with zero errors
- Both pt-br and en versions render correctly on `hugo server -D`
- All internal links use trailing slashes
- Kubernetes manifests and commands are technically accurate
- Blog follows the same format and tone as existing posts

## Rollback
- If build fails: fix issues and re-run `hugo --gc --minify`
- If content is incorrect: edit the markdown files directly
- No production changes beyond content files
