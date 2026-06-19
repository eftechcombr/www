---
slug: deployment
category: operations
generatedAt: 2026-06-19
relevantFiles:
  - .github/workflows/ci.yml
  - .github/workflows/pages.yml
---

# How do I deploy this project?

## Deployment

The EF-TECH website uses a GitOps deployment model. Pushing to the `main` branch triggers automatic builds and deploys.

### Cloudflare Pages (Primary)

| Setting | Value |
|---|---|
| Framework preset | Hugo |
| Build command | `hugo --gc --minify` |
| Output directory | `public` |
| Env var | `HUGO_VERSION=0.163.3` |
| Production branch | `main` |

1. Push to `main` branch
2. Cloudflare Pages detects the push via webhook
3. Build: `hugo --gc --minify`
4. Deploy automatic to `www.eftech.com.br`

### GitHub Pages (Secondary)

Defined in `.github/workflows/pages.yml`:

1. Triggered on push to `main` or manual `workflow_dispatch`
2. Install Hugo CLI v0.163.3
3. Checkout with `submodules: recursive`
4. Build: `hugo --gc --minify`
5. Upload artifact and deploy via `actions/deploy-pages@v4`

### CI Pipeline

Defined in `.github/workflows/ci.yml` — runs on every pull request:

1. Checkout with submodules
2. Setup Hugo v0.163.3 (extended)
3. Build: `hugo --gc --minify`
4. Link check: `lychee --verbose --no-progress public/**/*.html`

CI must pass before a PR can be merged.
