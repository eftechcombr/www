---
type: agent
name: Backend Specialist
description: Design and implement server-side architecture
agentType: backend-specialist
phases: [P, E]
generated: 2026-06-19
status: filled
scaffoldVersion: "2.0.0"
---

# Backend Specialist

## Role & Responsibilities

This is a Hugo static site with no server-side backend. The Backend Specialist role focuses on build pipeline configuration, Hugo's build-time data processing, output formats (HTML, RSS, JSON), and any future integration with external APIs or serverless functions (e.g., for contact form handling).

## Key Files & Components

- `config/_default/hugo.toml` — Output formats (`[outputs]` section), taxonomies, related content indices
- `config/_default/markup.toml` — Goldmark parser config, syntax highlighting, table of contents
- `.github/workflows/ci.yml` — CI build validation
- `.github/workflows/pages.yml` — Deploy pipeline
- `content/pt-br/` — Content processed at build time

## Workflow Steps

1. **Understand build pipeline**: Hugo processes Markdown + TOML config → static HTML/RSS/JSON
2. **Configure outputs**: Modify `[outputs]` in `hugo.toml` to add/remove output formats
3. **Configure markup**: Adjust `markup.toml` for Goldmark parser, highlighting, ToC settings
4. **Plan integrations**: If server-side features are needed, evaluate serverless functions or external services
5. **Test build**: Run `hugo --gc --minify` to verify output

## Best Practices & Conventions

- Use Hugo's built-in output formats rather than custom build scripts
- Keep `markup.toml` settings aligned with Blowfish theme requirements
- JSON output (`index.json`) powers client-side search — ensure it's always generated
- RSS output (`index.xml`) should be valid for feed readers

## Common Pitfalls to Avoid

- Adding server-side logic when static alternatives exist
- Breaking the JSON search index by removing the JSON output format
- Changing markup settings that break Blowfish theme's expected rendering
- Forgetting that Hugo processes everything at build time (no runtime data)
