---
type: doc
name: glossary
description: Project terminology, type definitions, domain entities, and business rules
category: glossary
generated: 2026-06-19
status: filled
scaffoldVersion: "2.0.0"
---

## Glossary & Domain Concepts

This glossary covers terminology specific to the EF-TECH website project, Hugo/Blowfish concepts, and EF-TECH's business domain (cloud computing services in Brazil).

## Type Definitions

No TypeScript or programming type definitions exist in this project. Data structures are defined via Hugo's front matter schema (TOML) and configuration files.

**Front Matter Schema** (TOML in each Markdown file):

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | yes | Page title |
| `description` | string | no | SEO meta description |
| `summary` | string | no | Summary for lists/cards |
| `date` | date | no | Publication date (YYYY-MM-DD) |
| `draft` | boolean | no | If true, excluded from production build |
| `tags` | array | no | Content tags for taxonomy |
| `categories` | array | no | Content categories for taxonomy |
| `author` | string | no | Author name for taxonomy |

## Enumerations

No exported enums. Configuration values use Blowfish theme's documented options:

- `colorScheme`: `blowfish`
- `defaultAppearance`: `light` | `dark`
- `homepage.layout`: `page` | `profile` | `hero` | `card` | `background` | `custom`
- `header.layout`: `basic` | `fixed` | `fixed-fill` | `fixed-gradient` | `fixed-fill-blur`

## Core Terms

- **Hugo** — Go-based static site generator (SSG) that compiles Markdown + templates into HTML
- **Blowfish** — Hugo theme (v2.103.0) by Nuno Coracao, built with Tailwind CSS
- **Front Matter** — TOML metadata at the top of Markdown files that configures page properties
- **Hugo Pipes** — Hugo's asset processing pipeline for image optimisation, CSS/JS bundling, fingerprinting
- **Taxonomy** — Hugo's content classification system (tags, categories, authors, series)
- **Archetype** — Template used by `hugo new` to scaffold new content files
- **GitOps** — Deployment model where Git pushes trigger automatic builds and deploys
- **Cloudflare Pages** — JAMstack hosting platform with automatic Git integration
- **lychee** — Rust-based link checker used in CI to validate links in generated HTML
- **Submodule** — Git mechanism for including the Blowfish theme as a nested repository

## Acronyms & Abbreviations

- **SSG** — Static Site Generator
- **CDN** — Content Delivery Network
- **CI/CD** — Continuous Integration / Continuous Deployment
- **GLPI** — Gestionnaire Libre de Parc Informatique (EF-TECH's support ticketing system)
- **LGPD** — Lei Geral de Proteção de Dados (Brazilian GDPR equivalent, relevant to EF-TECH's security services)
- **WAF** — Web Application Firewall
- **SIEM** — Security Information and Event Management
- **IaC** — Infrastructure as Code
- **RSS** — Really Simple Syndication
- **SEO** — Search Engine Optimisation

## Personas / Actors

- **Content Editor** — Writes and updates Markdown content in `content/pt-br/`. Needs basic Markdown and TOML knowledge.
- **Site Administrator** — Manages Hugo configuration, theme updates, and deployment settings. Needs Git and Hugo CLI skills.
- **Visitor** — End user browsing `www.eftech.com.br`. Experiences the static site via CDN with client-side search and theme switching.
- **CI/CD System** — GitHub Actions runner that builds the site and checks links on PRs and pushes.

## Domain Rules & Invariants

- Content language is Portuguese (pt-br) — `defaultContentLanguage = "pt-br"` in `hugo.toml`
- Hugo version must be v0.163.3 across local, CI, and Cloudflare Pages environments
- Theme is managed as a git submodule — `git clone --recurse-submodules` is required
- Draft content (`draft = true` in front matter) is excluded from production builds (`buildDrafts = false`)
- All content must pass the lychee link checker in CI before merging
- Internal links should use relative paths (e.g., `/contato/`, `/servicos/cloud-computing/`)
- Images for Hugo Pipes processing go in `assets/`; static images go in `static/`
