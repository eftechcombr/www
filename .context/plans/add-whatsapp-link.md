---
status: drafted
generated: 2026-06-19
agents:
  - type: "feature-developer"
    role: "Add WhatsApp link to contato pages and menus"
  - type: "frontend-specialist"
    role: "Add WhatsApp SVG icon to assets/icons/ for menu display"
  - type: "documentation-writer"
    role: "Update .context docs and cross-link new WhatsApp info"
docs:
  - "project-overview.md"
phases:
  - id: "phase-1"
    name: "Plan & Requirements"
    prevc: "P"
    agent: "feature-developer"
  - id: "phase-2"
    name: "Implementation"
    prevc: "E"
    agent: "frontend-specialist"
  - id: "phase-3"
    name: "Validation & Build"
    prevc: "V"
    agent: "feature-developer"
---

# Add WhatsApp link (55 85 98803-7625) to site Plan

> Add WhatsApp contact link to EF-TECH website contato pages (pt-br and en), header/footer menus, and enable WhatsApp sharing on articles. The WhatsApp number is 5585988037625.

## Task Snapshot
- **Primary goal:** Site visitors can reach EF-TECH via WhatsApp with one click from any page.
- **Success signal:** WhatsApp icon appears in the header menu, footer menu, and contato page on both languages; `hugo --gc --minify` builds without errors.
- **Key references:**
  - [Documentation Index](../docs/README.md)
  - [Blowfish theme docs](https://blowfish.page/docs/) — icon system, menus, sharingLinks

## Files to Modify

| File | Change |
|------|--------|
| `config/_default/menus.pt-br.toml` | Add WhatsApp entry in `[[main]]` (header) and `[[footer]]` |
| `config/_default/menus.en.toml` | Add WhatsApp entry in `[[main]]` (header) and `[[footer]]` |
| `config/_default/params.toml` | Uncomment `sharingLinks` and add `"whatsapp"` |
| `content/pt-br/contato.md` | Add WhatsApp link under "Redes Sociais" section |
| `content/en/contato.md` | Add WhatsApp link under "Social Media" section |
| `assets/icons/whatsapp.svg` | **New file** — WhatsApp SVG icon for menu `pre` parameter |

## Working Phases

### Phase 1 — Plan & Requirements
> **Primary Agent:** `feature-developer`

**Objective:** Define exact markup, icon source, and URL format.

**Tasks**

| # | Task | Agent | Status | Deliverable |
|---|------|-------|--------|-------------|
| 1.1 | Confirm WhatsApp link format: `https://wa.me/5585988037625` | `feature-developer` | pending | Accepted URL format |
| 1.2 | Locate WhatsApp SVG icon to place at `assets/icons/whatsapp.svg` | `frontend-specialist` | pending | SVG file prepared |
| 1.3 | Confirm icon name for menu `pre` parameter is `"whatsapp"` | `feature-developer` | pending | Config-ready |

**Commit Checkpoint**
- `git commit -m "feat(plan): add WhatsApp link plan after phase 1"`

---

### Phase 2 — Implementation
> **Primary Agent:** `frontend-specialist`

**Objective:** Apply all file changes.

**Tasks**

| # | Task | Agent | Status | Deliverable |
|---|------|-------|--------|-------------|
| 2.1 | Create `assets/icons/whatsapp.svg` with WhatsApp brand SVG | `frontend-specialist` | pending | SVG file |
| 2.2 | Edit `menus.pt-br.toml` — add `[[main]]` with `pre = "whatsapp"` and `url = "https://wa.me/5585988037625"` (~weight 65), add `[[footer]]` entry | `frontend-specialist` | pending | Updated TOML |
| 2.3 | Edit `menus.en.toml` — same as 2.2 for English | `frontend-specialist` | pending | Updated TOML |
| 2.4 | Edit `params.toml` — uncomment `sharingLinks` and include `"whatsapp"` | `frontend-specialist` | pending | Updated TOML |
| 2.5 | Edit `content/pt-br/contato.md` — add WhatsApp under "Redes Sociais" | `frontend-specialist` | pending | Updated markdown |
| 2.6 | Edit `content/en/contato.md` — add WhatsApp under "Social Media" | `frontend-specialist` | pending | Updated markdown |

**Commit Checkpoint**
- `git commit -m "feat(whatsapp): add WhatsApp link to menus, contato pages, and sharing"`

---

### Phase 3 — Validation & Build
> **Primary Agent:** `feature-developer`

**Objective:** Verify build succeeds and links are correct.

**Tasks**

| # | Task | Agent | Status | Deliverable |
|---|------|-------|--------|-------------|
| 3.1 | Run `hugo --gc --minify` to verify clean build | `feature-developer` | pending | Build output |
| 3.2 | Run `hugo server -D` and visually confirm WhatsApp icon in header, footer, and contato page (both languages) | `feature-developer` | pending | Visual confirmation |
| 3.3 | Check internal links use trailing slashes for link checker compliance | `feature-developer` | pending | Verified |

**Commit Checkpoint**
- `git commit -m "feat(whatsapp): validate build and WhatsApp link placement"`

## Rollback Plan
- **Phase 2 Rollback:** `git revert` the implementation commit
- **Phase 3 Rollback:** Same as above; no data migration involved
- **Post-rollback:** Verify `hugo --gc --minify` still passes

## Success Metrics
- WhatsApp icon appears in header (both langs)
- WhatsApp icon appears in footer (both langs)
- WhatsApp link listed on `/contato/` and `/en/contato/`
- `hugo --gc --minify` exits with code 0
- Link `https://wa.me/5585988037625` is functional
