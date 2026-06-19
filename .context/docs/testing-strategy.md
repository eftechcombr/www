---
type: doc
name: testing-strategy
description: Test frameworks, patterns, coverage requirements, and quality gates
category: testing
generated: 2026-06-19
status: filled
scaffoldVersion: "2.0.0"
---

## Testing Strategy

As a Hugo static site, the EF-TECH website does not use traditional unit/integration test frameworks. Quality is maintained through CI build validation, automated link checking, and manual visual review. The CI pipeline ensures every pull request builds successfully and contains no broken links before it can be merged.

## Test Types

- **Build validation**: Hugo build (`hugo --gc --minify`) runs in CI on every PR — if the build fails, the PR is blocked
- **Link checking**: `lychee` (via `lycheeverse/lychee-action@v2`) checks all links in generated HTML files (`public/**/*.html`)
- **Visual review**: Manual — developers run `hugo server -D` locally and verify pages render correctly before creating PRs
- **Content review**: Manual — verify Markdown front matter, content accuracy, and internal links

## Running Tests

```bash
# Local build test (mimics CI)
hugo --gc --minify

# Local dev server for visual review
hugo server -D

# CI runs automatically on PRs:
# 1. hugo --gc --minify
# 2. lychee --verbose --no-progress public/**/*.html
```

## Quality Gates

- **Hugo build must succeed**: Any build error blocks the PR
- **No broken links**: lychee link checker must pass — all internal and external links must resolve
- **Hugo version pinned**: CI uses v0.163.3 to match production environment
- **Submodules required**: CI checks out with `submodules: true` — missing theme will cause build failure

## Troubleshooting

- **Build fails locally but not CI**: Ensure Hugo version matches (v0.163.3 extended). Check `hugo version`.
- **lychee false positives**: External links may be temporarily down — re-run CI or mark with `--exclude` if known to be flaky
- **Theme not found**: Run `git submodule update --init --recursive` to initialise Blowfish theme
- **Missing images**: Ensure images are in `assets/` (for Hugo Pipes) or `static/` (for direct serving)
