# Documentation Index

Welcome to the repository knowledge base. Start with the project overview, then dive into specific guides as needed.

**Blog Posts Reference**

The following blog posts have been added to the documentation index:
- [GLPI 12.0.0: Official Major Release and EF-TECH Cloud-Native Distribution](../../content/en/blog/glpi-12-0-0/index.md) (en) — Official release of GLPI 12.0.0, EF-TECH Helm chart 2.12.0 and unprivileged Docker images, rewritten Knowledge Base, Session Manager, and Sudo Mode
- [GLPI 12.0.0: Lançamento Oficial da Nova Versão Major e Distribuição Cloud-Native da EF-TECH](../../content/pt-br/blog/glpi-12-0-0/index.md) (pt-br) — Lançamento oficial do GLPI 12.0.0, Helm chart 2.12.0 e imagens Docker unprivileged da EF-TECH, nova Base de Conhecimento, Gerenciador de Sessões e Modo Sudo
- [GLPI 11.0.11: Security Release, Plugin Fixes, and New Features in eftechcombr/glpi](../../content/en/blog/glpi-11-0-11/index.md) (en) — EF-TECH release of GLPI 11.0.11 security release superseding 11.0.10, fixing 6 high vulnerabilities, custom Nginx config templates, and MySQL SSL support
- [GLPI 11.0.11: Release de Segurança, Correção de Plugins e Novos Recursos no eftechcombr/glpi](../../content/pt-br/blog/glpi-11-0-11/index.md) (pt-br) — Lançamento da EF-TECH do GLPI 11.0.11 corrigindo 6 vulnerabilidades de alta severidade, substituindo 11.0.10, templates customizados de Nginx e suporte a SSL no MySQL
- [GLPI 12.0.0-rc1 and Helm Chart 2.12.0: Subchart Modernization, Security Hardening, and High Availability](../../content/en/blog/glpi-12-0-0-rc1.md) (en) — EF-TECH release of GLPI 12.0.0-rc1 and Helm Chart 2.12.0 with Valkey subchart, PDB, HPA, S3 backup, and readOnlyRootFilesystem hardening
- [GLPI 12.0.0-rc1 e Helm Chart 2.12.0: modernização de subcharts, hardening e alta disponibilidade](../../content/pt-br/blog/glpi-12-0-0-rc1.md) (pt-br) — Lançamento da EF-TECH do GLPI 12.0.0-rc1 e Helm Chart 2.12.0 com subchart Valkey, PDB, HPA, backup S3 e hardening com readOnlyRootFilesystem
- [Understanding P99 and Tail Latency](../../content/en/blog/p99-tail-latency/index.md) (en) — Why the mean lies and how to eliminate tail latency bottlenecks in production
- [P99 e Latência de Cauda (Tail Latency)](../../content/pt-br/blog/p99-tail-latency/index.md) (pt-br) — Por que a média engana e como mitigar gargalos de latência de cauda em produção
- [Understanding RFC 10008: The HTTP QUERY Method](../../content/en/blog/rfc-10008-http-query.md) (en) — Standardizing HTTP QUERY as a safe and idempotent method with a body payload
- [Entendendo a RFC 10008: O Método HTTP QUERY](../../content/pt-br/blog/rfc-10008-http-query.md) (pt-br) — Padronizando o método HTTP QUERY como uma alternativa segura e idempotente com payload no corpo
- [Google SRE Principles: Evolution from Traditional Operations to Site Reliability Engineering](../../content/en/blog/google-sre-principles.md) (en) — Comprehensive overview of Google SRE principles from the SRE Book
- [Princípios SRE do Google: Evolução da Operações Tradicionais para a Engenharia de Confiabilidade de Sites](../../content/pt-br/blog/google-sre-principles.md) (pt-br) — Visão geral abrangente dos princípios SRE do Google, do Livro SRE

## Core Guides
- [Project Overview](./project-overview.md)
- [Architecture Notes](./architecture.md)
- [Development Workflow](./development-workflow.md)
- [Testing Strategy](./testing-strategy.md)
- [Glossary & Domain Concepts](./glossary.md)
- [Data Flow & Integrations](./data-flow.md)
- [Security & Compliance Notes](./security.md)
- [Tooling & Productivity Guide](./tooling.md)

## Repository Snapshot
- `archetypes/`
- `assets/`
- `config/`
- `content/`
- `data/`
- `i18n/`
- `layouts/`
- `public/`
- `README.md/`
- `resources/`
- `static/`
- `themes/`

## Document Map
| Guide | File | Primary Inputs |
| --- | --- | --- |
| Project Overview | `project-overview.md` | Roadmap, README, stakeholder notes |
| Architecture Notes | `architecture.md` | ADRs, service boundaries, dependency graphs |
| Development Workflow | `development-workflow.md` | Branching rules, CI config, contributing guide |
| Testing Strategy | `testing-strategy.md` | Test configs, CI gates, known flaky suites |
| Glossary & Domain Concepts | `glossary.md` | Business terminology, user personas, domain rules |
| Data Flow & Integrations | `data-flow.md` | System diagrams, integration specs, queue topics |
| Security & Compliance Notes | `security.md` | Auth model, secrets management, compliance requirements |
| Tooling & Productivity Guide | `tooling.md` | CLI scripts, IDE configs, automation workflows |

## Recent Blog Posts
- [Understanding P99 and Tail Latency](../../content/en/blog/p99-tail-latency/index.md) (en) — Why the mean lies and how to eliminate tail latency bottlenecks in production
- [P99 e Latência de Cauda (Tail Latency)](../../content/pt-br/blog/p99-tail-latency/index.md) (pt-br) — Por que a média engana e como mitigar gargalos de latência de cauda em produção
- [Understanding RFC 10008: The HTTP QUERY Method](../../content/en/blog/rfc-10008-http-query.md) (en) — Standardizing HTTP QUERY as a safe and idempotent method with a body payload
- [Entendendo a RFC 10008: O Método HTTP QUERY](../../content/pt-br/blog/rfc-10008-http-query.md) (pt-br) — Padronizando o método HTTP QUERY como uma alternativa segura e idempotente com payload no corpo
- [Understanding Site Reliability Engineering: Google's SRE Philosophy and Practices](../../content/en/blog/understanding-sre-google-sre-philosophy-practices.md) (en) — Deep dive into Google SRE principles: error budgets, progressive rollouts, and the engineering-first culture
- [Supabase agora é um app oficial do ChatGPT](../../content/pt-br/blog/supabase-chatgpt-app.md) (pt-br) — Supabase becomes official ChatGPT app with 29 integrated tools
- [Supabase Is Now an Official ChatGPT App](../../content/en/blog/supabase-chatgpt-app.md) (en) — English version of the same announcement
- [Google SRE Principles: Evolution from Traditional Operations to Site Reliability Engineering](./../../content/en/blog/google-sre-principles.md) (en) — Comprehensive overview of Google SRE principles from the SRE Book
- [Princípios SRE do Google: Evolução da Operações Tradicionais para a Engenharia de Confiabilidade de Sites](./../../content/pt-br/blog/google-sre-principles.md) (pt-br) — Visão geral abrangente dos princípios SRE do Google, do Livro SRE
