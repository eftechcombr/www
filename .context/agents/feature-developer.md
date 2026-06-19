---
type: agent
name: Feature Developer
description: Implement new features according to specifications
agentType: feature-developer
phases: [P, E]
generated: 2026-06-19
status: filled
scaffoldVersion: "2.0.0"
---

# Feature Developer

## Feature Development Workflow

1. **Plan the feature**: Determine if it requires new content, config changes, or layout overrides
2. **Create content**: Add Markdown files in `content/pt-br/` using `hugo new` or manually
3. **Update config**: Modify `config/_default/*.toml` as needed (menus, params, taxonomies)
4. **Layout overrides**: If custom templates are needed, create files in `layouts/` (not in theme)
5. **Test locally**: Run `hugo server -D` and verify the feature works
6. **Build check**: Run `hugo --gc --minify` to verify production build
7. **Create PR**: Push branch, open PR, ensure CI passes (build + link check)

## Code Organization Patterns

- **New pages**: Markdown files in `content/pt-br/` with appropriate front matter
- **New sections**: Create directory in `content/pt-br/` with `_index.md` as section landing
- **Menu items**: Add entries in `config/_default/menus.pt-br.toml` with sequential weights
- **Custom layouts**: Override theme templates by creating matching files in `layouts/`
- **Static assets**: Place in `static/` for direct serving, `assets/` for Hugo Pipes processing
- **Data files**: Use `data/` for structured data accessible in templates

## Integration Points for New Features

- **Navigation**: `menus.pt-br.toml` — add menu entries
- **Taxonomy**: `hugo.toml [taxonomies]` — define new taxonomies
- **Outputs**: `hugo.toml [outputs]` — add output formats (HTML, RSS, JSON)
- **Theme features**: `params.toml` — enable/disable Blowfish features (search, breadcrumbs, etc.)
- **Homepage layout**: `params.toml [homepage]` — configure hero, recent items, card view

## Testing Requirements for New Code

- Hugo build succeeds: `hugo --gc --minify`
- Link check passes (lychee in CI)
- Visual review: `hugo server -D` — verify rendering on desktop and mobile
- Front matter: All required fields present and valid TOML
- Menu: New pages appear in navigation if intended

## Documentation Expectations

- Update `README.md` if project structure changes
- Add new sections to `.context/docs/` if architectural changes are made
- Update `menus.pt-br.toml` when adding navigable pages
- Document any new config parameters in `.context/docs/architecture.md`
