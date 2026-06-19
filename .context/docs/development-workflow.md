---
type: doc
name: development-workflow
description: Day-to-day engineering processes, branching, and contribution guidelines
category: workflow
generated: 2026-06-19
status: filled
scaffoldVersion: "2.0.0"
---

## Development Workflow

The EF-TECH website follows a GitOps workflow: content and configuration changes are committed to Git, pushed to `main`, and automatically built and deployed by Cloudflare Pages and GitHub Actions. Day-to-day work involves writing Markdown content, adjusting TOML configuration, occasionally updating the Blowfish theme submodule, and verifying changes locally with Hugo's dev server before pushing.

## Branching & Releases

- **Trunk-based**: All changes merge to `main` — no long-lived feature branches
- **Production branch**: `main` — every push to `main` triggers deploy
- **Pull requests**: CI workflow (`ci.yml`) runs on PRs — build check + link checker
- **Releases**: No formal release tagging — deployment is continuous on push to `main`
- **Theme updates**: Periodic `git submodule update --remote themes/blowfish` followed by testing and commit

## Local Development

```bash
# Clone with theme submodule
git clone --recurse-submodules https://github.com/eftechcombr/www.git
cd www

# Start local dev server (includes drafts)
hugo server -D

# Build for production
hugo --gc --minify

# Update Blowfish theme
git submodule update --remote themes/blowfish
git add themes/blowfish
git commit -m "chore: update blowfish theme"

# Create new content from archetype
hugo new content/pt-br/blog/my-post.md
```

Local server: `http://localhost:1313/`

## Code Review Expectations

- All changes should go through a PR with CI passing (build + link check)
- Content changes: verify Markdown renders correctly, front matter is valid TOML, internal links work
- Config changes: verify Hugo build succeeds locally before pushing
- Theme updates: test the full site locally after submodule update — check for visual regressions
- Follow Conventional Commits (e.g., `feat(content): add new service page`, `fix(config): correct menu weight`)
- See `AGENTS.md` for agent collaboration tips and `CONTRIBUTING.md` for contribution guidelines

## Onboarding Tasks

1. Clone the repo with `--recurse-submodules`
2. Install Hugo v0.163.3+ (extended)
3. Run `hugo server -D` and verify the site loads
4. Read `README.md` for project overview and structure
5. Explore `config/_default/` to understand site configuration
6. Explore `content/pt-br/` to understand content organisation
7. Review `.github/workflows/` for CI/CD pipeline
8. Check the [Blowfish docs](https://blowfish.page/docs/) for theme customisation options
