---
type: doc
name: architecture
description: System architecture, layers, patterns, and design decisions
category: architecture
generated: 2026-06-19
status: filled
scaffoldVersion: "2.0.0"
---

## Architecture Notes

The EF-TECH website is a statically generated site built with Hugo and the Blowfish theme. There is no server-side application logic — the architecture is a build-time pipeline that transforms Markdown content and TOML configuration into static HTML, CSS, JS, and JSON assets, which are then served by a CDN (Cloudflare Pages). This design was chosen for its simplicity, speed, security, and low operational overhead, which aligns with EF-TECH's cloud consulting brand.

## System Architecture Overview

The system is a **static site monolith** — a single Hugo project that compiles all pages at build time. The build pipeline runs on push to `main`, producing a `public/` directory that is deployed to Cloudflare Pages (and optionally GitHub Pages). There are no microservices, databases, or runtime API calls. Client-side interactivity (search, theme switching, code copy, mobile nav) is provided by the Blowfish theme's bundled JavaScript.

Request flow:

```
Visitor → Cloudflare CDN → Static HTML (public/) → Blowfish JS (search, theme toggle)
```

Build flow:

```
Git push (main) → Cloudflare Pages / GitHub Actions → hugo --gc --minify → public/ → CDN
```

## Architectural Layers

- **Configuration Layer**: Hugo site config and theme parameters (`config/_default/`)
- **Content Layer**: Markdown pages with TOML front matter (`content/pt-br/`)
- **Theme Layer**: Blowfish templates, layouts, assets, and JS libraries (`themes/blowfish/`)
- **Static Assets**: Images and files served as-is (`static/`, `assets/`)
- **Build Output**: Generated static site (`public/`)
- **CI/CD Layer**: GitHub Actions workflows for build validation and deployment (`.github/workflows/`)

> See [`codebase-map.json`](./codebase-map.json) for complete symbol counts and dependency graphs.

## Detected Design Patterns

| Pattern | Confidence | Locations | Description |
|---------|------------|-----------|-------------|
| Static Site Generation | 100% | `hugo.toml`, `content/` | Hugo compiles Markdown to static HTML at build time |
| GitOps Deploy | 100% | `.github/workflows/pages.yml`, Cloudflare Pages | Push to `main` triggers automatic build and deploy |
| Theme Submodule | 100% | `.gitmodules`, `themes/blowfish/` | Theme managed as git submodule for isolated updates |
| Configuration-Driven UI | 90% | `config/_default/params.toml` | Theme appearance and behaviour controlled via TOML params |
| Content-as-Data | 85% | `content/pt-br/` with front matter | Markdown files with TOML metadata drive page structure |
| Taxonomy System | 80% | `hugo.toml [taxonomies]` | Tags, categories, authors, and series for content organisation |

## Entry Points

- [`config/_default/hugo.toml`](../../config/_default/hugo.toml) — Main Hugo configuration
- [`content/pt-br/_index.md`](../../content/pt-br/_index.md) — Homepage content
- [`config/_default/menus.pt-br.toml`](../../config/_default/menus.pt-br.toml) — Navigation menu definition
- [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) — CI pipeline
- [`.github/workflows/pages.yml`](../../.github/workflows/pages.yml) — Deploy pipeline

## Public API

This is a static website with no API. The public-facing endpoints are HTTP routes serving static files:

| Route | Type | Source |
|-------|------|--------|
| `/` | HTML | `content/pt-br/_index.md` |
| `/servicos/` | HTML | `content/pt-br/servicos/_index.md` |
| `/servicos/cloud-computing/` | HTML | `content/pt-br/servicos/cloud-computing.md` |
| `/servicos/seguranca/` | HTML | `content/pt-br/servicos/seguranca.md` |
| `/sobre/` | HTML | `content/pt-br/sobre.md` |
| `/blog/` | HTML | `content/pt-br/blog/_index.md` |
| `/contato/` | HTML | `content/pt-br/contato.md` |
| `/index.xml` | RSS | Hugo RSS output |
| `/index.json` | JSON | Hugo JSON output (search index) |
| `/sitemap.xml` | XML | Hugo sitemap |

## External Service Dependencies

- **Cloudflare Pages** — Primary hosting and CDN. Build command: `hugo --gc --minify`. Output: `public/`. Env: `HUGO_VERSION=0.163.3`
- **GitHub Pages** — Secondary hosting via GitHub Actions (`actions/deploy-pages@v4`)
- **GitHub Actions** — CI/CD runner for build validation and link checking
- **lychee** — Link checker (via `lycheeverse/lychee-action@v2`) — validates all links in generated HTML
- **GLPI** (`glpi.eftech.com.br`) — External support portal linked in footer menu

## Key Decisions & Trade-offs

- **Hugo over other SSGs**: Chosen for build speed, Go binary distribution, and rich theme ecosystem. Trade-off: less flexible than JS-based SSGs for dynamic features.
- **Blowfish theme**: Selected for modern design, Tailwind CSS, built-in search, and multi-language support. Trade-off: large theme with bundled JS libraries increases complexity.
- **Git submodule for theme**: Allows independent theme updates without forking. Trade-off: requires `--recurse-submodules` on clone.
- **Cloudflare Pages + GitHub Pages**: Dual deploy paths for redundancy. Trade-off: two deployment configurations to maintain.
- **No backend/database**: Maximum simplicity and security. Trade-off: no dynamic features like server-side forms or CMS.

## Risks & Constraints

- Hugo version must be pinned at v0.163.3 to match CI and Cloudflare Pages build environment
- Theme updates require manual `git submodule update --remote` and testing
- No server-side functionality — contact form and dynamic features require external services
- Content is Portuguese-only (pt-br); adding languages requires new content directories and config

## Top Directories Snapshot

- `config/_default/` — 6 files (TOML configuration)
- `content/pt-br/` — 7 files (Markdown content)
- `themes/blowfish/` — Theme submodule (hundreds of files)
- `assets/img/` — 1 file (logo)
- `static/` — Static assets
- `.github/workflows/` — 2 files (CI + deploy YAML)
- `archetypes/` — 1 file (default template)
- `public/` — Build output (generated, not in git)

## Related Resources

- [Project Overview](./project-overview.md)
- [Data Flow & Integrations](./data-flow.md)
- [Development Workflow](./development-workflow.md)
- [Tooling & Productivity Guide](./tooling.md)
- [Blowfish Theme Docs](https://blowfish.page/docs/)
- [Hugo Docs](https://gohugo.io/documentation/)
