---
type: agent
name: Test Writer
description: Write comprehensive unit and integration tests
agentType: test-writer
phases: [E, V]
generated: 2026-06-19
status: filled
scaffoldVersion: "2.0.0"
---

# Test Writer

## Testing Framework & Conventions

This is a Hugo static site — there are **no traditional test frameworks** (no Jest, no unit tests). Testing is done through CI build validation and automated link checking. The "test suite" consists of:

1. **Hugo build** (`hugo --gc --minify`) — validates that the site compiles without errors
2. **lychee link checker** — validates all internal and external links in generated HTML
3. **Manual visual review** — developer runs `hugo server -D` and verifies rendering

## Test File Organization

No test files exist. CI workflows in `.github/workflows/` serve as the test infrastructure:

- `.github/workflows/ci.yml` — Runs on PRs: Hugo build + lychee link check
- `.github/workflows/pages.yml` — Runs on push to main: Hugo build + GitHub Pages deploy

## Mocking Strategies

Not applicable — no runtime code to mock. Hugo processes everything at build time.

## Coverage Requirements

- **Build coverage**: 100% — every PR must build successfully
- **Link coverage**: 100% — lychee checks all links in `public/**/*.html`
- **Visual coverage**: Manual — developers should visually verify changes before merging

## CI/CD Integration

The CI pipeline (`.github/workflows/ci.yml`) acts as the test runner:

```yaml
steps:
  - uses: actions/checkout@v4
    with:
      submodules: true
      fetch-depth: 0
  - uses: peaceiris/actions-hugo@v3
    with:
      hugo-version: '0.163.3'
      extended: true
  - run: hugo --gc --minify
  - uses: lycheeverse/lychee-action@v2
    with:
      args: --verbose --no-progress public/**/*.html
      fail: true
```

## Best Practices for Content "Testing"

- Always run `hugo --gc --minify` locally before creating a PR
- Use `hugo server -D` to visually verify changes
- Check for broken internal links manually (use trailing slashes: `/contato/`)
- Verify front matter is valid TOML (no syntax errors)
- Test both light and dark appearance modes after visual changes
- If adding new content, ensure it appears in the correct menu and taxonomy
