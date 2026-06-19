---
type: doc
name: tooling
description: Scripts, IDE settings, automation, and developer productivity tips
category: tooling
generated: 2026-06-19
status: filled
scaffoldVersion: "2.0.0"
---

## Tooling & Productivity Guide

The EF-TECH website requires minimal tooling — Hugo CLI and Git are the primary tools. The Blowfish theme is managed as a git submodule. CI/CD is fully automated via GitHub Actions and Cloudflare Pages. No package manager (npm, yarn) or build tool beyond Hugo is needed for the project itself.

## Required Tooling

- **Hugo Extended v0.163.3+** — Static site generator. Install from [gohugo.io](https://gohugo.io/installation/). Must be the extended edition for SCSS/image processing.
- **Git** — Version control, required for submodule management
- **A Markdown editor** — Any text editor or IDE with Markdown support (VS Code, Neovim, etc.)

## Recommended Automation

```bash
# Local development with hot reload + drafts
hugo server -D

# Production build (mimics CI/CD)
hugo --gc --minify

# Update Blowfish theme to latest
git submodule update --remote themes/blowfish
git add themes/blowfish
git commit -m "chore: update blowfish theme"

# Create new blog post from archetype
hugo new content/pt-br/blog/my-post.md

# Create new service page
hugo new content/pt-br/servicos/new-service.md

# Clean build artifacts
rm -rf public resources/_gen
```

## IDE / Editor Setup

- **VS Code**: Install the "Hugo Language and Syntax Support" extension and "TOML" extension
- **Front Matter snippet**: Use the archetype at `archetypes/default.md` as a template for new content
- **Preview**: Use `hugo server -D` for live preview with drafts enabled

## Productivity Tips

- Use `hugo server -D --disableFastRender` for more accurate live preview (disables fast render mode)
- Pin Hugo version with a version manager (e.g., `asdf`, `homebrew`) to match CI (v0.163.3)
- Use `hugo --watch` in development for automatic rebuilds on file change
- Cloudflare Pages dashboard provides deploy previews for PRs — use for visual review before merging
- Keep `themes/blowfish/` clean — never edit files inside the submodule directly; use `layouts/` for overrides
