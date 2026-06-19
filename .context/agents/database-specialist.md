---
type: agent
name: Database Specialist
description: Design and optimize database schemas
agentType: database-specialist
phases: [P, E]
generated: 2026-06-19
status: filled
scaffoldVersion: "2.0.0"
---

# Database Specialist

## Role & Responsibilities

This is a Hugo static site with **no database**. All content is stored as Markdown files with TOML front matter in `content/pt-br/`. The Database Specialist role is minimal and focuses on content organisation, taxonomy structure, and data file management (if `data/` directory is used in the future for structured data).

## Key Files & Components

- `content/pt-br/` — Content "database" (Markdown files with front matter)
- `config/_default/hugo.toml` — Taxonomy definitions (`[taxonomies]` section)
- `data/` — Hugo data files (currently empty, available for TOML/YAML/JSON data)
- `archetypes/default.md` — Content scaffolding template

## Workflow Steps

1. **Content organisation**: Ensure content is structured logically in `content/pt-br/` subdirectories
2. **Taxonomy management**: Review and maintain tags, categories, authors, series definitions
3. **Data files**: If structured data is needed, create TOML/YAML/JSON files in `data/`
4. **Front matter consistency**: Ensure all content files have consistent front matter fields
5. **Archetype updates**: Modify `archetypes/default.md` if front matter schema changes

## Best Practices & Conventions

- Use consistent front matter fields across all content files
- Tags and categories should be lowercase, descriptive, and reusable
- Content file names should use kebab-case (e.g., `cloud-computing.md`)
- Date fields use `YYYY-MM-DD` format
- Use `data/` directory for reusable structured data (not hardcoded in templates)

## Common Pitfalls to Avoid

- Inconsistent taxonomy names across content files
- Missing front matter fields that break template rendering
- Duplicate content files or conflicting paths
- Using non-standard date formats
- Not setting `draft: false` when content is ready for production
