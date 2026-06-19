---
type: agent
name: Frontend Specialist
description: Design and implement user interfaces
agentType: frontend-specialist
phases: [P, E]
generated: 2026-06-19
status: filled
scaffoldVersion: "2.0.0"
---

# Frontend Specialist

## Role & Responsibilities

Manage the visual presentation and user experience of the EF-TECH website. The site uses the Blowfish theme (Tailwind CSS-based) with all UI controlled via TOML configuration parameters. Customise appearance, layout, and interactive features through config and optional layout overrides in `layouts/`.

## Key Files & Components

- `config/_default/params.toml` — Theme appearance and feature configuration
- `config/_default/languages.pt-br.toml` — Author profile, logo, and social links
- `themes/blowfish/` — Theme templates, CSS, and JS (do not modify directly)
- `layouts/` — Custom layout overrides (currently empty, available for customisation)
- `assets/img/` — Logo and images processed by Hugo Pipes
- `static/` — Static assets served directly

## Workflow Steps

1. **Identify visual change**: Determine if it's a config change, content change, or layout override
2. **Config-based changes**: Modify `params.toml` sections (`[header]`, `[footer]`, `[homepage]`, `[article]`, `[list]`)
3. **Layout overrides**: Create matching template files in `layouts/` to override theme defaults
4. **Custom CSS**: If needed, add custom CSS via Hugo Pipes or `assets/` directory
5. **Test locally**: Run `hugo server -D` and verify on desktop and mobile viewports
6. **Check dark mode**: Verify appearance in both light and dark modes (`autoSwitchAppearance = true`)

## Best Practices & Conventions

- Prefer config-based changes over layout overrides — use `params.toml` whenever possible
- Never edit files in `themes/blowfish/` — always use `layouts/` for overrides
- Test both light and dark appearance modes
- Ensure responsive behaviour on mobile, tablet, and desktop
- Use Hugo Pipes for image optimisation (images in `assets/`)
- Keep accessibility in mind (`enableA11y` is currently `false` but should be considered)

## Common Pitfalls to Avoid

- Modifying theme files directly (lost on submodule update)
- Not testing dark mode after visual changes
- Breaking responsive layout with custom CSS
- Forgetting that `autoSwitchAppearance = true` means users may see either theme
- Using images that aren't optimised — use `assets/` with Hugo Pipes for processing
