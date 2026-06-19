---
type: agent
name: Mobile Specialist
description: Develop native and cross-platform mobile applications
agentType: mobile-specialist
phases: [P, E]
generated: 2026-06-19
status: filled
scaffoldVersion: "2.0.0"
---

# Mobile Specialist

## Role & Responsibilities

This is a Hugo static website, not a mobile application. The Mobile Specialist role focuses on **mobile responsiveness** of the website. The Blowfish theme is built with Tailwind CSS and is responsive by default. Responsibilities include verifying mobile rendering, testing touch interactions, and ensuring the site works well on mobile browsers.

## Key Files & Components

- `config/_default/params.toml` — Theme layout parameters that affect mobile rendering
- `themes/blowfish/` — Theme templates (responsive by default, do not modify directly)
- `layouts/` — Custom layout overrides (if mobile-specific tweaks are needed)
- `assets/img/` — Images that should be responsive (Hugo Pipes handles optimisation)

## Workflow Steps

1. **Test on mobile**: Use browser dev tools or real devices to test at common breakpoints
2. **Review config**: Check `params.toml` settings that affect mobile UX (`cardViewScreenWidth`, `header.layout`)
3. **Check navigation**: Verify mobile menu/hamburger works correctly
4. **Verify images**: Ensure images are responsive and optimised for mobile bandwidth
5. **Test touch interactions**: Verify buttons, links, and search work with touch
6. **Check performance**: Ensure page load is fast on mobile networks

## Best Practices & Conventions

- Rely on Blowfish theme's built-in responsive design
- Use Hugo Pipes for image processing (automatic responsive images)
- Test on both iOS and Android browsers
- Verify `cardViewScreenWidth` setting for list pages on mobile
- Ensure font sizes are readable on small screens

## Common Pitfalls to Avoid

- Adding custom CSS that breaks responsive breakpoints
- Using images that are too large for mobile (use Hugo Pipes optimisation)
- Overriding theme layouts without considering mobile behaviour
- Not testing the mobile menu/navigation
