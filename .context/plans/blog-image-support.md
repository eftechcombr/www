---
status: draft
generated: 2026-06-22
agents:
  - type: "architect-specialist"
    role: "Design image integration strategy and choose between flat files vs page bundles"
  - type: "frontend-specialist"
    role: "Configure Hugo/Blowfish theme settings for hero images and featured images"
  - type: "feature-developer"
    role: "Implement changes: archetype update, image directories, config changes"
  - type: "code-reviewer"
    role: "Review all changes for correctness and Hugo best practices"
  - type: "documentation-writer"
    role: "Document the image convention in .context/docs/ and AGENTS.md"
  - type: "performance-optimizer"
    role: "Verify image optimization settings and responsive image generation"
docs:
  - "project-overview.md"
  - "architecture.md"
  - "development-workflow.md"
  - "glossary.md"
phases:
  - id: "phase-1"
    name: "Design & Config"
    prevc: "P"
    agent: "architect-specialist"
  - id: "phase-2"
    name: "Implementation"
    prevc: "E"
    agent: "feature-developer"
  - id: "phase-3"
    name: "Verification"
    prevc: "V"
    agent: "frontend-specialist"
---

# Suporte a imagens nos posts do blog Plan

> Adicionar suporte completo a imagens nos posts do blog usando o tema Blowfish: featured images, hero images, imagens inline com processamento responsivo, e estrutura de diretórios padronizada

## Task Snapshot
- **Primary goal:** Permitir que autores de posts do blog adicionem imagens (featured/hero/inline) seguindo uma convenção clara, aproveitando as funcionalidades nativas do tema Blowfish.
- **Success signal:** Qualquer post novo pode incluir `featureimage` no front matter e imagens Markdown no corpo; o build `hugo --gc --minify` passa sem erros; a listagem de blog mostra thumbnails.
- **Key references:**
  - [Documentation Index](../docs/README.md)
  - [Agent Handbook](../agents/README.md)
  - [Plans Index](./README.md)

## Codebase Context
- **Stack:** Hugo + Blowfish theme
- **Posts:** 4 posts em `/content/{en,pt-br}/blog/` como arquivos `.md` flat (sem page bundles)
- **Config:** `showHero = false` em params.toml, `disableImageOptimization = false`
- **Imagens existentes:** Apenas `assets/img/logo.png` e `static/img/logo.png`

## Abordagem Escolhida: Flat files com `static/img/blog/`

Por que **não** page bundles:
- Menos disruptivo: não requer migrar os 4 posts existentes
- Simplicidade: autores continuam editando um único `.md`
- O tema Blowfish processa imagens em Markdown via `render-image.html` (responsive, lazy loading, zoom) independentemente de page bundle
- `featureimage` no front matter funciona com caminhos em `static/` ou `assets/`

Estrutura de diretórios para imagens:
```
static/
  img/
    blog/
      <post-slug>/
        hero.jpg         # Featured image (opcional)
        image-01.png     # Imagens inline do post
```

## Agent Lineup
| Agent | Role in this plan | First responsibility focus |
|-------|-------------------|---------------------------|
| Architect Specialist | Definir estratégia de imagens e estrutura de diretórios | Escolher flat vs page bundle, definir convenção |
| Feature Developer | Implementar todas as mudanças no código | Atualizar params.toml, archetype, criar diretórios |
| Frontend Specialist | Validar configuração do tema e renderização | Verificar hero images e responsividade |
| Code Reviewer | Revisar qualidade e boas práticas | Garantir que `hugo --gc --minify` passa |
| Documentation Writer | Documentar a convenção adotada | Atualizar .context/docs/ e AGENTS.md |
| Performance Optimizer | Verificar otimização de imagens | Confirmar `disableImageOptimization = false` e srcset gerado |

## Documentation Touchpoints
| Guide | File | What to update |
|-------|------|----------------|
| Development Workflow | [development-workflow.md](../docs/development-workflow.md) | Adicionar seção "Adding images to blog posts" |
| Project Overview | [project-overview.md](../docs/project-overview.md) | Mencionar suporte a imagens nos posts |
| Architecture Notes | [architecture.md](../docs/architecture.md) | Documentar estrutura `static/img/blog/` |
| Glossary | [glossary.md](../docs/glossary.md) | Adicionar termos: featured image, hero image, page bundle, srcset |

## Working Phases

### Phase 1 — Design & Config (Plan)
> **Primary Agent:** `architect-specialist`

**Objective:** Definir a estratégia de imagens e preparar a configuração do Hugo/Blowfish.

**Tasks**

| # | Task | Agent | Status | Deliverable |
|---|------|-------|--------|-------------|
| 1.1 | Decidir entre flat files vs page bundles | `architect-specialist` | pending | Decisão documentada no plano |
| 1.2 | Atualizar `config/_default/params.toml`: ativar hero images | `architect-specialist` | pending | `showHero = true`, `heroStyle = "basic"` |
| 1.3 | Criar diretório `static/img/blog/` | `architect-specialist` | pending | Diretório criado |
| 1.4 | Adicionar `defaultFeaturedImage` em params.toml | `architect-specialist` | pending | Fallback visual para posts sem imagem |
| 1.5 | Revisar configuração de otimização de imagens | `architect-specialist` | pending | Confirmar `disableImageOptimization = false` |

**Commit Checkpoint:** `git commit -m "feat(config): enable hero images and add default featured image"`

---

### Phase 2 — Implementation (Execute)
> **Primary Agent:** `feature-developer`

**Objective:** Implementar todas as mudanças no código e preparar exemplos.

**Tasks**

| # | Task | Agent | Status | Deliverable |
|---|------|-------|--------|-------------|
| 2.1 | Atualizar `archetypes/default.md` com campos de imagem no front matter | `feature-developer` | pending | `featureimage`, `featureimagecaption`, `showHero` no template |
| 2.2 | Adicionar `defaultFeaturedImage` em params.toml | `feature-developer` | pending | Config apontando para logo como fallback |
| 2.3 | Ativar hero images: `showHero = true`, `heroStyle = "basic"` | `feature-developer` | pending | params.toml atualizado |
| 2.4 | Exemplificar num post existente: adicionar `featureimage` a `oracle-always-free` | `feature-developer` | pending | Post com imagem de exemplo |
| 2.5 | Documentar convenção em `.context/docs/development-workflow.md` | `documentation-writer` | pending | Seção "Adding images" |
| 2.6 | Atualizar `AGENTS.md` com a nova convenção | `documentation-writer` | pending | Repo map atualizado |

**Commit Checkpoint:** `git commit -m "feat(blog): add image support with featured images and hero style"`

---

### Phase 3 — Verification (Verify)
> **Primary Agent:** `frontend-specialist`

**Objective:** Verificar que o build passa, as imagens renderizam corretamente e a convenção está documentada.

**Tasks**

| # | Task | Agent | Status | Deliverable |
|---|------|-------|--------|-------------|
| 3.1 | Executar `hugo --gc --minify` e verificar se passa sem erros | `frontend-specialist` | pending | Build bem-sucedido |
| 3.2 | Revisar visualmente no `hugo server -D` | `frontend-specialist` | pending | Hero image visível, thumbnail na listagem |
| 3.3 | Verificar links internos com lychee (se aplicável) | `frontend-specialist` | pending | Sem broken links |
| 3.4 | Revisão de código pelo `code-reviewer` | `code-reviewer` | pending | PR aprovado |
| 3.5 | Verificar documentação gerada | `documentation-writer` | pending | Docs completos e cross-linkados |

**Commit Checkpoint:** `git commit -m "chore(blog): finalize image support with verification"`

## Rollback Plan

### Rollback Triggers
- Build falha com erro relacionado a imagens
- Hero images quebram layout em dispositivos móveis
- Performance degradada (LCP/Lighthouse)

### Rollback Procedures
#### Phase 1 Rollback
- Action: Reverter params.toml para o estado original
- Data Impact: Nenhum
- Estimated Time: < 5 min

#### Phase 2 Rollback
- Action: Reverter commits com `git revert`
- Data Impact: Nenhum (só arquivos de configuração e docs)
- Estimated Time: < 10 min

## Evidence & Follow-up

### Artifacts to Collect
- Log de `hugo --gc --minify` bem-sucedido
- Screenshot do post com hero image
- Screenshot da listagem do blog com thumbnail

### Success Metrics
- `hugo --gc --minify` executa sem erros
- Post `oracle-always-free` exibe hero image no topo
- Blog listing mostra thumbnail para posts com `featureimage`
- Autores conseguem adicionar imagens em Markdown com processamento responsivo

### Follow-up Actions
| Action | Owner (Agent) | Due |
|--------|---------------|-----|
| Adicionar imagens reais aos posts existentes | `feature-developer` | Post-workflow |
| Considerar conversão futura para page bundles | `architect-specialist` | Próximo roadmap |
