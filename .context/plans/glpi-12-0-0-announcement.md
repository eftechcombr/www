---
status: active
generated: 2026-10-09
agents:
  - type: "documentation-writer"
    role: "Draft comprehensive GLPI 12.0.0 official release announcement posts in PT-BR and EN"
  - type: "frontend-specialist"
    role: "Generate cover PNG image and integrate media into Hugo posts"
  - type: "devops-specialist"
    role: "Validate Hugo build, link checks, and manage git branch and PR"
docs:
  - "project-overview.md"
  - "architecture.md"
  - "development-workflow.md"
phases:
  - id: "phase-1"
    name: "Discovery & Alignment"
    prevc: "P"
    agent: "documentation-writer"
  - id: "phase-2"
    name: "Implementation & Iteration"
    prevc: "E"
    agent: "documentation-writer"
  - id: "phase-3"
    name: "Validation & Handoff"
    prevc: "V"
    agent: "devops-specialist"
---

# GLPI 12.0.0 Official Release and EF-TECH Distribution Post Plan

> Write blog posts in Portuguese and English announcing the official release of GLPI 12.0.0 and EF-TECH Helm chart 2.12.0 / Docker containers, generate cover image, validate build, and create PR.

## Task Snapshot
- **Primary goal:** Publish announcement blog posts in Portuguese (`content/pt-br/blog/glpi-12-0-0/index.md`) and English (`content/en/blog/glpi-12-0-0/index.md`) announcing the official release of GLPI 12.0.0 by `glpi-project/glpi` and EF-TECH distribution `v12.0.0` (PR #214), Helm chart `glpi-2.12.0` (appVersion: "12.0.0"), Docker images `eftechcombr/glpi:php-fpm-12.0.0` and `eftechcombr/glpi:nginx-12.0.0`, with cover PNG image and validated links.
- **Success signal:** Clean Hugo production build (`hugo --gc --minify`), 0 broken links with lychee, both language versions published, and a clean Git commit / PR created and merged.
- **Key references:**
  - [Documentation Index](../docs/README.md)
  - [Agent Handbook](../agents/README.md)
  - [Plans Index](./README.md)
  - [GitHub Repository eftechcombr/glpi](https://github.com/eftechcombr/glpi)
  - [Upstream GLPI Releases](https://github.com/glpi-project/glpi/releases)
  - [GLPI User Documentation](https://help.glpi-project.org)

## Codebase Context
- **Hugo Site:** Multilingual setup with `pt-br` as default and `en` language section.
- **Blog Post Locations:** `content/pt-br/blog/glpi-12-0-0/index.md` and `content/en/blog/glpi-12-0-0/index.md`.
- **Assets:** `static/img/blog/glpi-12-0-0/cover.png`, `content/pt-br/blog/glpi-12-0-0/cover.png`, and `content/en/blog/glpi-12-0-0/cover.png` generated via Python PIL script.

## Agent Lineup
| Agent | Role in this plan | Playbook | First responsibility focus |
| --- | --- | --- | --- |
| Documentation Writer | Technical content creation | [Documentation Writer](../agents/documentation-writer.md) | Draft accurate, engaging release posts in PT-BR and EN |
| Frontend Specialist | Media & Image generation | [Frontend Specialist](../agents/frontend-specialist.md) | Design and generate cover PNG image matching site theme |
| DevOps Specialist | Build & verification | [Devops Specialist](../agents/devops-specialist.md) | Validate Hugo build, verify links, manage git branch and PR |

## Documentation Touchpoints
| Guide | File | Primary Inputs |
| --- | --- | --- |
| Project Overview | [project-overview.md](../docs/project-overview.md) | Multilingual content structure, blog layout |
| Development Workflow | [development-workflow.md](../docs/development-workflow.md) | Hugo commands, link trailing slash requirements, PR process |

## Working Phases

### Phase 1 — Discovery & Alignment
> **Primary Agent:** `documentation-writer` - [Playbook](../agents/documentation-writer.md)

**Objective:** Inspect release details from `glpi-project/glpi` (released October 7, 2026 after 3 RCs) and `eftechcombr/glpi` (release `v12.0.0`, PR #214 merged October 9, 2026, chart `glpi-2.12.0`), structure post content and image generation script.

**Tasks**
| # | Task | Agent | Status | Deliverable |
|---|------|-------|--------|-------------|
| 1.1 | Analyze GLPI 12.0.0 features: Knowledge Base rewrite, Session Manager, Step-Up/Sudo mode, Group OLAs, Accessibility, Security, EOL of GLPI 10 | `documentation-writer` | completed | Content outline |
| 1.2 | Design cover image concept and specifications | `frontend-specialist` | completed | Python PIL generation script |

---

### Phase 2 — Implementation & Iteration
> **Primary Agent:** `documentation-writer` - [Playbook](../agents/documentation-writer.md)

**Objective:** Generate PNG cover image, author comprehensive blog posts in PT-BR and EN with proper frontmatter, upgrade guide, deployment examples, and internal links.

**Tasks**
| # | Task | Agent | Status | Deliverable |
|---|------|-------|--------|-------------|
| 2.1 | Generate 1200x630 cover PNG at `static/img/blog/glpi-12-0-0/cover.png` and content bundles | `frontend-specialist` | completed | Cover image PNG |
| 2.2 | Author `content/pt-br/blog/glpi-12-0-0/index.md` | `documentation-writer` | completed | Portuguese blog post |
| 2.3 | Author `content/en/blog/glpi-12-0-0/index.md` | `documentation-writer` | completed | English blog post |
| 2.4 | Update documentation indices in `.context/docs/README.md`, `.context/agents/README.md`, and `.context/plans/README.md` | `documentation-writer` | completed | Documentation updates |

---

### Phase 3 — Validation & Handoff
> **Primary Agent:** `devops-specialist` - [Playbook](../agents/devops-specialist.md)

**Objective:** Validate Hugo build, verify all links and image paths, commit changes, create PR and monitor checks.

**Tasks**
| # | Task | Agent | Status | Deliverable |
|---|------|-------|--------|-------------|
| 3.1 | Test build with `hugo --gc --minify` | `devops-specialist` | completed | Build verification |
| 3.2 | Check image rendering and link integrity with lychee | `devops-specialist` | completed | Verified assets |
| 3.3 | Create git branch, commit, push, create PR and verify CI | `devops-specialist` | completed | Pull Request |
