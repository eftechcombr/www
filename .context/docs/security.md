---
type: doc
name: security
description: Security policies, authentication, secrets management, and compliance requirements
category: security
generated: 2026-06-19
status: filled
scaffoldVersion: "2.0.0"
---

## Security & Compliance Notes

As a static website with no server-side logic, database, or authentication, the EF-TECH website has a relatively small attack surface. Security considerations focus on build-time integrity, content safety, CDN configuration, and protecting deployment credentials. The site's static nature inherently mitigates common web vulnerabilities (SQL injection, XSS via server-side rendering, session hijacking).

## Authentication & Authorization

- **No user authentication**: The site is fully public — no login, user accounts, or sessions
- **Deployment auth**: Cloudflare Pages uses GitHub OAuth integration; GitHub Actions uses `GITHUB_TOKEN` with scoped permissions (`contents: read`, `pages: write`, `id-token: write`)
- **Git access**: Repository access controlled via GitHub organisation permissions (`eftechcombr`)

## Secrets & Sensitive Data

- **No secrets in the repository**: The site contains no API keys, passwords, or credentials
- **Analytics/verification tokens**: Google Analytics, Firebase, Fathom, Umami, and verification IDs are commented out in `config/_default/params.toml` — enable only with environment-specific configuration
- **Cloudflare Pages env vars**: `HUGO_VERSION` is the only configured environment variable — no secrets stored
- **`.gitignore`**: Ensure `public/`, `resources/_gen/`, and other build artifacts are not committed

## Compliance & Policies

- **LGPD (Lei Geral de Proteção de Dados)**: As a Brazilian company website, LGPD compliance is relevant — the site currently does not collect personal data (no forms with server-side processing, no analytics enabled). If analytics or contact forms are added, LGPD compliance measures (cookie consent, privacy policy, data processing notices) must be implemented.
- **Content accuracy**: All marketing claims about cloud services should be accurate and verifiable

## Incident Response

- **Deploy rollback**: Cloudflare Pages supports instant rollback to previous deployments via dashboard. GitHub Pages requires reverting the commit and redeploying.
- **Compromised tokens**: Rotate GitHub tokens and Cloudflare API keys via respective admin dashboards
- **Content defacement**: Revert malicious commits via `git revert` and force redeploy. Review GitHub access logs for unauthorised commits.
- **Broken site**: CI catches build errors before deploy. If a bad deploy occurs, rollback via Cloudflare Pages dashboard.
