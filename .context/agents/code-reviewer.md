---
type: agent
name: Code Reviewer
description: Review code changes for quality, style, and best practices
agentType: code-reviewer
phases: [R, V]
generated: 2026-06-19
status: filled
scaffoldVersion: "2.0.0"
---

# Code Reviewer

## Code Review Checklist

### Content Changes (Markdown)
- [ ] Front matter TOML is valid and complete (title, description, date if applicable)
- [ ] Markdown is well-formatted and renders correctly
- [ ] Internal links use correct paths with trailing slashes (e.g., `/servicos/`)
- [ ] Images are in the correct directory (`assets/` for Hugo Pipes, `static/` for direct)
- [ ] No broken external links
- [ ] Content is in Portuguese (pt-br)
- [ ] Tags and categories are appropriate

### Configuration Changes (TOML)
- [ ] Hugo build succeeds: `hugo --gc --minify`
- [ ] No commented-out config left behind (unless intentionally disabled)
- [ ] Theme parameters match Blowfish documentation
- [ ] Menu weights are sequential and consistent

### Theme/Submodule Changes
- [ ] Submodule updated to a specific commit (not just latest)
- [ ] Full site tested locally after update
- [ ] No visual regressions
- [ ] No files in `themes/blowfish/` modified directly

### CI/CD Changes
- [ ] Hugo version matches v0.163.3
- [ ] Permissions are scoped correctly
- [ ] Build and link check steps preserved

## Common Patterns to Look For

- **Hardcoded values** that should be configurable in `params.toml`
- **Missing front matter** fields (especially `title` and `description` for SEO)
- **Inconsistent date formats** — should be `YYYY-MM-DD`
- **Missing trailing slashes** on internal links (breaks lychee)
- **Draft content** left as `draft: true` when intended for production

## Security Considerations

- No secrets, API keys, or credentials in config or content
- No inline JavaScript in Markdown content
- `goldmark.renderer.unsafe = true` is set — ensure no untrusted content is rendered
- External links should point to legitimate domains

## Performance Best Practices

- Images should be optimised and in `assets/` for Hugo Pipes processing
- `--minify` flag used in production builds
- `--gc` flag used to clean up resources
- No unnecessarily large images in `static/`

## Testing Requirements

- Hugo build must pass: `hugo --gc --minify`
- Link check must pass (lychee in CI)
- Visual review recommended for layout/theme changes
