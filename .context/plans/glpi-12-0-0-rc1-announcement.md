---
status: active
generated: 2026-09-08
agents:
  - type: "documentation-writer"
    role: "Draft clear, comprehensive announcement blog posts in PT-BR and EN"
  - type: "frontend-specialist"
    role: "Generate cover PNG image and integrate media into Hugo posts"
  - type: "devops-specialist"
    role: "Validate Hugo build, link checks, and prepare git branch and PR"
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

# GLPI 12.0.0-rc1 Blog Post Announcement Plan

> Create EN and PT-BR blog posts for GLPI 12.0.0-rc1 release, generate PNG cover image, validate with Hugo, and prepare PR.

## Task Snapshot
- **Primary goal:** Publish announcement blog posts in Portuguese (`content/pt-br/blog/glpi-12-0-0-rc1.md`) and English (`content/en/blog/glpi-12-0-0-rc1.md`) covering GLPI 12.0.0-rc1 / Helm Chart 2.12.0 from EF-TECH, with a generated featured PNG image and validated links.
- **Success signal:** Clean Hugo production build (`hugo --gc --minify`), no broken images or links, both language versions published, and a clean Git commit / PR ready.
- **Key references:**
  - [Documentation Index](../docs/README.md)
  - [Agent Handbook](../agents/README.md)
  - [Plans Index](./README.md)
  - [GitHub Release eftechcombr/glpi](https://github.com/eftechcombr/glpi/releases/tag/v12.0.0-rc1)

## Codebase Context
- **Hugo Site:** Multilingual setup with `pt-br` as default and `en` language section.
- **Blog Post Location:** `content/pt-br/blog/` and `content/en/blog/`.
- **Assets:** `static/img/blog/glpi-12-0-0-rc1/cover.png` generated via Python PIL script.

## Agent Lineup
| Agent | Role in this plan | Playbook | First responsibility focus |
| --- | --- | --- | --- |
| Documentation Writer | Technical content creation | [Documentation Writer](../agents/documentation-writer.md) | Draft accurate, engaging release notes in PT-BR and EN |
| Frontend Specialist | Media & Image generation | [Frontend Specialist](../agents/frontend-specialist.md) | Design and generate cover PNG image matching site theme |
| DevOps Specialist | Build & verification | [Devops Specialist](../agents/devops-specialist.md) | Validate Hugo build, verify links, manage git PR |

## Documentation Touchpoints
| Guide | File | Primary Inputs |
| --- | --- | --- |
| Project Overview | [project-overview.md](../docs/project-overview.md) | Site structure, multilingual content mapping |
| Development Workflow | [development-workflow.md](../docs/development-workflow.md) | Hugo commands, link trailing slash requirements, PR process |

## Working Phases

### Phase 1 — Discovery & Alignment
> **Primary Agent:** `documentation-writer` - [Playbook](../agents/documentation-writer.md)

**Objective:** Inspect release details from `eftechcombr/glpi`, analyze existing blog post patterns (`glpi-11-0-8.md`), and prepare structured content outline.

**Tasks**
| # | Task | Agent | Status | Deliverable |
|---|------|-------|--------|-------------|
| 1.1 | Analyze GLPI 12.0.0-rc1 release notes and PR details | `documentation-writer` | completed | Content outline |
| 1.2 | Design cover image concept and specifications | `frontend-specialist` | completed | Python PIL generation script |

---

### Phase 2 — Implementation & Iteration
> **Primary Agent:** `documentation-writer` - [Playbook](../agents/documentation-writer.md)

**Objective:** Generate PNG cover image and author comprehensive blog posts in PT-BR and EN with proper frontmatter, code snippets, and internal links.

**Tasks**
| # | Task | Agent | Status | Deliverable |
|---|------|-------|--------|-------------|
| 2.1 | Generate 1200x630 cover PNG at `static/img/blog/glpi-12-0-0-rc1/cover.png` | `frontend-specialist` | pending | Cover image PNG |
| 2.2 | Write `content/pt-br/blog/glpi-12-0-0-rc1.md` | `documentation-writer` | pending | Portuguese blog post |
| 2.3 | Write `content/en/blog/glpi-12-0-0-rc1.md` | `documentation-writer` | pending | English blog post |

---

### Phase 3 — Validation & Handoff
> **Primary Agent:** `devops-specialist` - [Playbook](../agents/devops-specialist.md)

**Objective:** Validate Hugo build, verify all links and image paths, commit changes, create PR and monitor checks.

**Tasks**
| # | Task | Agent | Status | Deliverable |
|---|------|-------|--------|-------------|
| 3.1 | Test build with `hugo --gc --minify` | `devops-specialist` | pending | Build verification |
| 3.2 | Check image rendering and link integrity | `devops-specialist` | pending | No 404 or broken links |
| 3.3 | Create git branch, commit, push, create PR and verify CI | `devops-specialist` | pending | Merged or approved PR |
