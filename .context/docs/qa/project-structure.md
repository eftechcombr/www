---
slug: project-structure
category: architecture
generatedAt: 2026-06-19
---

# How is the codebase organized?

## Project Structure

```
www/
├── config/_default/       # Hugo configuration (TOML)
│   ├── hugo.toml          # Core site config (base URL, taxonomies, outputs)
│   ├── params.toml        # Blowfish theme parameters
│   ├── markup.toml        # Goldmark parser + syntax highlighting
│   ├── languages.pt-br.toml  # Portuguese language config
│   ├── menus.pt-br.toml   # Navigation menu definition
│   └── module.toml        # Hugo module config (empty)
├── content/pt-br/         # Markdown content in Portuguese
│   ├── _index.md          # Landing page (hero layout)
│   ├── servicos/          # Service pages
│   │   ├── _index.md
│   │   ├── cloud-computing.md
│   │   └── seguranca.md
│   ├── sobre.md           # About page
│   ├── blog/              # Blog section
│   │   ├── _index.md
│   │   └── primeiro-post.md
│   └── contato.md         # Contact page
├── assets/img/            # Images for Hugo Pipes (logo)
├── static/                # Static files served as-is
├── themes/blowfish/       # Blowfish theme (git submodule)
├── archetypes/            # Content scaffolding templates
├── layouts/               # Custom layout overrides (empty)
├── data/                  # Hugo data files (empty)
├── i18n/                  # Translation files (empty)
├── public/                # Build output (generated, gitignored)
├── resources/             # Hugo resource cache (generated)
└── .github/workflows/     # CI (ci.yml) + Deploy (pages.yml)
```

## Key Directories

- **`config/_default/`** — All Hugo site configuration in TOML format
- **`content/pt-br/`** — Markdown content with TOML front matter (Portuguese)
- **`themes/blowfish/`** — Theme managed as git submodule from `nunocoracao/blowfish`
- **`assets/`** — Images processed by Hugo Pipes (optimisation, fingerprinting)
- **`layouts/`** — Override theme templates here (currently empty, theme defaults used)
