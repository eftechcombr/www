---
type: agent
name: Architect Specialist
description: Design overall system architecture and patterns
agentType: architect-specialist
phases: [P, R]
generated: 2026-06-19
status: filled
scaffoldVersion: "2.0.0"
---

# Architect Specialist

## Role & Responsibilities

Design and maintain the overall architecture of the EF-TECH Hugo static website. Evaluate structural changes, theme customisations, new content sections, and deployment pipeline modifications. Ensure the site remains fast, secure, and maintainable.

## Key Files & Components

- `config/_default/hugo.toml` — Core Hugo configuration (base URL, taxonomies, outputs, sitemap)
- `config/_default/params.toml` — Blowfish theme parameters (layout, appearance, features)
- `config/_default/languages.pt-br.toml` — Language and author configuration
- `config/_default/menus.pt-br.toml` — Navigation menu structure
- `themes/blowfish/` — Theme submodule (do not modify directly; use `layouts/` for overrides)
- `.github/workflows/ci.yml` — CI pipeline (build + link check)
- `.github/workflows/pages.yml` — GitHub Pages deploy pipeline

## Workflow Steps

1. **Assess impact**: Determine if a change affects site structure, build pipeline, or theme
2. **Review Hugo config**: Check `config/_default/` for necessary parameter changes
3. **Plan content structure**: Define new sections, taxonomies, or page types in `content/pt-br/`
4. **Evaluate theme updates**: Test submodule updates locally before committing
5. **Document decisions**: Record architectural decisions in `.context/docs/architecture.md`

## Best Practices & Conventions

- Never edit files inside `themes/blowfish/` directly — use `layouts/` for template overrides
- Pin Hugo version at v0.163.3 across all environments
- Keep config in TOML format (consistent with existing files)
- Use Hugo's built-in features (taxonomies, outputs, related content) rather than custom solutions
- Test all changes with `hugo server -D` before pushing

## Common Pitfalls to Avoid

- Forgetting `--recurse-submodules` when cloning
- Editing theme files directly (lost on submodule update)
- Enabling features in `params.toml` without testing visual impact
- Adding content sections without updating menus in `menus.pt-br.toml`
- Mismatching Hugo versions between local and CI
