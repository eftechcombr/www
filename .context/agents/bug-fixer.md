---
type: agent
name: Bug Fixer
description: Analyze bug reports and error messages
agentType: bug-fixer
phases: [E, V]
generated: 2026-06-19
status: filled
scaffoldVersion: "2.0.0"
---

# Bug Fixer

## Debugging Workflow

1. **Reproduce locally**: Clone with `--recurse-submodules`, run `hugo server -D`
2. **Check Hugo version**: Ensure v0.163.3 extended — mismatches cause subtle build errors
3. **Check build output**: Run `hugo --gc --minify` and read error messages carefully
4. **Check CI logs**: Review GitHub Actions output for build or link checker failures
5. **Isolate the issue**: Comment out recent changes or test with minimal content
6. **Fix and verify**: Apply fix, rebuild, run `hugo server -D`, verify visually

## Common Bug Patterns & Fixes

| Pattern | Cause | Fix |
|---------|-------|-----|
| Build fails: "theme not found" | Submodule not initialised | `git submodule update --init --recursive` |
| Build fails: template error | Invalid front matter TOML | Check for syntax errors in `+++`/`---` blocks |
| Broken links in CI | Incorrect internal link path | Use trailing slashes: `/contato/` not `/contato` |
| Missing images | Image in wrong directory | `assets/` for Hugo Pipes, `static/` for direct serving |
| Page not in menu | Menu weight or pageRef mismatch | Check `menus.pt-br.toml` matches content path |
| Blank page | `draft: true` in front matter | Use `hugo server -D` to see drafts, or set `draft: false` |
| Search not working | JSON output disabled | Ensure `[outputs] home = ["HTML", "RSS", "JSON"]` in `hugo.toml` |

## Logging & Error Handling

- Hugo outputs build errors to stderr — check terminal output
- lychee link checker outputs broken links with file and line references
- GitHub Actions logs are available in the Actions tab of the repository
- Cloudflare Pages build logs available in the Cloudflare dashboard

## Test Verification Steps

1. Run `hugo --gc --minify` — must succeed without errors
2. Run `hugo server -D` — verify the affected page renders correctly
3. Check internal links on the affected page
4. If CI was failing, push fix and verify CI passes

## Rollback Procedures

- **Git revert**: `git revert <commit-hash>` to undo the problematic change
- **Cloudflare Pages**: Roll back to previous deployment via dashboard
- **GitHub Pages**: Revert commit and redeploy via Actions
