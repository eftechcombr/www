---
title: "15 Brazilian open-source projects worth a look: from laws as Markdown to an open AI accelerator"
description: "A curated tour of 15 Brazilian open-source projects on GitHub: legislation as Markdown, an open TPU built with AI agents, reverse-documentation agents, a self-hosted CRM with WhatsApp, and more."
summary: "A recent video roundup listed 15 Brazilian open-source projects. This article reorganizes that list by category, corrects the names the transcript garbled, and adds what each repository actually documents: stack, license, and one concrete implementation detail. It covers Leis, Brasil API, pgModeler, openTPU, Bend, navi, Reversa, AI Memory, Git City, VirtualBuddy, Easy Effects, Winlator, PhotoGIMP, DeskcommCRM, and Open Notebook."
date: 2026-11-07
draft: false
tags: ["open-source", "brazil", "github", "software-development", "tools"]
categories: ["infrastructure"]
featureimage: "/img/blog/projetos-open-source-brasileiros/cover.png"
featureimagecaption: "15 Brazilian open-source projects on GitHub"
---

A recent video roundup, *15 projetos open source brasileiros no GitHub*, gathered fifteen repositories maintained by Brazilian developers. The list mixes very different things: public data infrastructure, a hardware accelerator, desktop utilities, agent tooling, and full applications.

The video is useful as a starting point, but its automatic transcript mangles several names — "Virtual Bunny" is VirtualBuddy, "Nave" is navi — and it moves fast enough that details get lost. This article reorganizes the list by category and describes only what each repository documents: what the project is, why it matters, its stack, its license, and one concrete detail about how it works.

![15 Brazilian open-source projects on GitHub](/img/blog/projetos-open-source-brasileiros/cover.png)

Three caveats before we start. Star counts are approximate and change daily. Licenses are the ones declared in each repository, and a few projects combine different licenses for code and content. And none of this is an endorsement: it is a map of what exists, so you can decide what deserves a clone.

## Data, public services, and infrastructure

### Leis: Brazilian legislation as a Git repository

[Leis](https://github.com/ctresb/leis) ("all the laws of Brazil") converts Brazilian federal, state, and municipal legislation into Markdown, one file per norm, with links to the source and the full history preserved in Git. The repository already covers more than 323,000 norms.

The interesting part is not the parsing itself, but the interface it creates. Legislation becomes a text corpus you can `grep`, `diff`, and review like code. A change to a norm shows up as a commit; a historical version is a checkout. For anyone building legal tech, compliance tooling, or research on top of Brazilian law, that is a much better starting point than scraping a gazette PDF.

The project is explicit about its limits: coverage is partial, conversion can introduce OCR errors, and the text does not replace the official gazette. The official texts are public acts; the conversion scripts are under MIT. With roughly 2.6k stars, it is the kind of repository whose value is easier to see when you need it than when you browse it.

### Brasil API: Brazilian public data without an API key

[Brasil API](https://github.com/BrasilAPI/BrasilAPI) is a free, community-run API for Brazilian data: postal codes (CEP), company registrations (CNPJ), area codes (DDD), banks, holidays, and tax rates, among others.

The problem it solves is familiar to anyone who has integrated Brazilian systems: the official sources are fragmented, inconsistent, and often require registration or scrape-hostile interfaces. Brasil API centralizes access behind predictable endpoints, with a public status page and documentation at [brasilapi.com.br](https://brasilapi.com.br). It is written in Node.js, licensed MIT, and has around 11.5k stars.

For side projects and internal tools, it removes a week of integration work. For production, treat it as a community service: cache responses, handle failures, and know which upstream each endpoint depends on.

### pgModeler: visual modeling for PostgreSQL

[pgModeler](https://github.com/nullptrlabs/pgmodeler) is a data modeling tool built specifically for PostgreSQL. You draw the diagram, and the tool generates DDL. It also compares a model against a live database, so drift between design and reality becomes visible, and it exports and imports between the visual model and SQL.

It is written in C++ with Qt, licensed GPL-3.0, and has about 3.6k stars. The project has been around long enough to be boring in the best sense — there is documentation and a dedicated site at [pgmodeler.io](https://pgmodeler.io).

Why it matters: most modeling tools treat PostgreSQL as one dialect among many. pgModeler tracks PostgreSQL-specific features, which is exactly where generic tools start producing DDL that does not match what you meant.

## Hardware and high-performance computing

### openTPU: an open AI accelerator designed with AI agents

[openTPU](https://github.com/FeSens/openTPU) is the most ambitious item on the list: an open-source AI accelerator, designed with the help of AI agents, and published down to the RTL.

The repository includes SystemVerilog RTL, an instruction set architecture, a bit-exact simulator, a kernel language with its compiler, and host software. It runs Qwen3, LFM2.5, and Qwen3.5 on a Kintex-7 PCIe FPGA card — specifically an Inspur YPCB-00338 with 4 GiB of DDR3. Apache-2.0, Verilog, around 930 stars.

The "designed with AI agents" framing is what draws attention, but the engineering substance is the simulator: a bit-exact model lets you validate kernels before touching hardware, which is how you make FPGA work reproducible. It is also a rare case of a Brazilian project operating at the RTL level with a full software stack around it.

### Bend: massively parallel programming without the usual ceremony

[Bend](https://github.com/bendlang/bend) is a programming language by Victor Taelin (HigherOrderCO) built for massive parallelism: the same program can run across thousands of GPU or CPU cores. It is based on functional semantics and uses proofs to catch mistakes at compile time instead of at 3 a.m.

The language is implemented in TypeScript, licensed Apache-2.0, and has about 24.8k stars. It moved from the old `HigherOrderCO/Bend` organization to `bendlang/bend`; the old URL redirects, but the canonical link is the new one. Documentation lives at [bend-lang.com](https://bend-lang.com).

Bend is a research-flavored language, not a drop-in replacement for your production backend. Its value is in the model: writing parallel code in a language where the runtime handles the distribution changes how you think about the problem.

## Developer tools

### navi: executable cheatsheets

[navi](https://github.com/denisidoro/navi) is an interactive cheatsheet tool for the command line. You browse snippets, pick one, fill in dynamic arguments, and run it — without leaving the terminal.

It is written in Rust and uses fzf or skim as the picker, with shell and tmux widgets so a cheatsheet can open in a popup. Around 17.8k stars, Apache-2.0. The cheatsheets themselves are plain files, which means a team can version its operational knowledge next to the code it operates:

```bash
eval "$(navi widget zsh)"
```

That one line gives you a keybinding that opens your team's cheatsheets as a fuzzy-searchable menu. For runbooks, it is a lighter alternative to a wiki nobody opens during an incident.

### Reversa: reverse-documentation for legacy codebases

[Reversa](https://github.com/sandeco/reversa) attacks a problem that every consultancy knows: a system with no documentation, no tests, and business rules that exist only in the heads of people who are about to retire.

The workflow starts inside the legacy project:

```bash
npx reversa install
```

From there, a team of specialized agents — Scout, Archaeologist, Detective, Architect, Writer, and Reviewer — extracts business rules and produces traceable, executable specifications (SDD, spec-driven development) that coding agents can consume. It writes only to `.reversa/` and `_reversa_sdd/`, so the legacy codebase is not modified. There is a paper on arXiv describing the approach.

Written in JavaScript, MIT, around 1.9k stars. The design decision worth noting is the write boundary: an agent-based tool that rewrites the code it is analyzing is hard to trust, and Reversa deliberately does not.

### AI Memory: long-term memory for coding agents

[AI Memory](https://github.com/akitaonrails/ai-memory) gives coding agents a memory that survives the session. It works with Claude Code, Codex, Cursor, OpenCode, Gemini CLI, and more than twenty harnesses.

The storage model is deliberately unexotic: a git-backed Markdown wiki. Retrieval is zero-LLM by default, so recall does not cost tokens or depend on a model call, and handoffs between agents or machines are typed and claim-once, which avoids two agents picking up the same pending task. Written in Rust, MIT, around 15.3k stars, with documentation at [aimemory.sh](https://aimemory.sh).

The practical effect is that context stops being something you re-explain every morning. It is also a good example of a design pattern that will outlive the current agent frameworks: plain text in Git, with structure on top.

### Git City: your GitHub profile as a building

[Git City](https://github.com/srizzon/git-city) turns a GitHub profile into a 3D pixel-art building inside an interactive city. Contributions determine height, repositories determine width, and stars determine window brightness.

It is built with Next.js, Three.js, and Supabase, licensed AGPL-3.0, with around 6k stars. You can see it running at [thegitcity.com](https://thegitcity.com).

It is the lightest project on this list, and that is fine. It is also a compact demonstration of how to render a procedurally generated 3D scene in the browser without the frame rate collapsing — useful reference material even if you never build a city.

## Desktop and mobile

### VirtualBuddy: macOS VMs on Apple Silicon

[VirtualBuddy](https://github.com/insidegui/VirtualBuddy) is a native GUI for running macOS 12 and later — including betas — in virtual machines on Apple Silicon, plus some ARM Linux distributions. It is built on Apple's Virtualization framework.

The features are the ones that make daily use tolerable: an install wizard, IPSW download, save and resume of machine state, clipboard sharing, and shared folders. Written in Swift, BSD-2-Clause, around 8.9k stars.

For anyone who needs to test software against a beta macOS release without dedicating a machine to it, this is the shortest path. The transcript calls it "Virtual Bunny"; the repository is VirtualBuddy.

### Easy Effects: real-time audio processing on PipeWire

[Easy Effects](https://github.com/wwmm/easyeffects) brings a rack of real-time audio effects to Linux desktops running PipeWire: equalizer, compressor, limiter, convolver, noise reduction, and autovolume, applied to microphones and outputs.

GPL-3.0, around 10.5k stars. The value is not any single effect but the routing model: effects are per-device and persist, so a laptop microphone and a USB interface can each have their own chain.

It is the kind of project that quietly removes the need to boot another operating system just to sound acceptable on a call.

### Winlator: Windows applications on Android

[Winlator](https://github.com/brunodev85/winlator) runs Windows applications and games on Android using Wine combined with Box86 and Box64 for x86 emulation on ARM devices.

Written in C, LGPL-2.1, around 19.8k stars, with releases and documentation at [winlator.org](https://winlator.org). Performance depends heavily on the device and on the application: this is translation and emulation, not native execution, and the project is honest about that.

The interesting engineering is the integration layer — container configuration, graphics drivers, and input mapping — which is what turns a pile of emulators into something a person can actually use.

### PhotoGIMP: making GIMP behave like Photoshop

[PhotoGIMP](https://github.com/Diolinux/PhotoGIMP) is a patch and configuration set that makes GIMP 3 and later feel familiar to Photoshop users: keyboard shortcuts, tool arrangement, and UI organization are adjusted to match Adobe's conventions.

Python, GPL-3.0, around 18.5k stars. It does not add features; it removes the migration tax. For a design team moving to free software, that tax is usually the real blocker — not the missing filter.

## AI applications and agents

### DeskcommCRM: a self-hosted CRM with WhatsApp and agents

[DeskcommCRM](https://github.com/melgarafael/DeskcommCRM) describes itself as an "AI sales OS": a self-hosted CRM with native AI agents and WhatsApp integration, positioned as an alternative to Kommo, Octadesk, and Intercom.

It connects to WhatsApp either through WAHA with QR-code pairing or through the Meta Cloud API; each tenant gets its own RAG context, the CRM is exposed over MCP so agents can query it, and multi-tenancy is enforced with row-level security and LGPD concerns in mind. Stack: Next.js and Supabase, TypeScript, MIT, around 5.2k stars.

The architecture choices matter more than the feature list: self-hosted, per-tenant isolation, and an open protocol for agent access. That combination is still uncommon in Brazilian CRM tooling, where the default is a closed SaaS.

### Open Notebook: a self-hosted NotebookLM alternative

[Open Notebook](https://github.com/lfnovo/open-notebook) is an open-source, self-hosted alternative to NotebookLM. You choose your model and provider, ingest sources, and generate podcasts and notes from them.

TypeScript, MIT, around 41.7k stars, with documentation at [www.open-notebook.ai](https://www.open-notebook.ai). It is the most-starred project on this list, which says something about how much demand there is for running this class of tool on your own infrastructure.

For teams that cannot send internal documents to a third-party service, the interesting property is not the podcast generator — it is that the model provider is a configuration choice rather than a vendor decision.

## What these fifteen projects have in common

Two patterns stand out.

The first is local problems solved with global tools. Leis, Brasil API, DeskcommCRM, and Winlator exist because the Brazilian context has specific constraints — fragmented public data, WhatsApp as the default communication channel, legislation that changes constantly. None of them are translations of an existing product.

The second is Brazilian maintainers working on global infrastructure. openTPU, Bend, navi, AI Memory, and Open Notebook compete for attention with projects from anywhere else, and their audiences are international. The GitHub profile does not tell you where the maintainer lives; the README does not either.

Licensing is mostly permissive — MIT and Apache-2.0 dominate — with GPL-3.0 for desktop applications and AGPL-3.0 for Git City. That distribution is typical of the current open-source landscape: permissive for libraries and infrastructure, copyleft for applications where the hosted-service loophole matters.

One practical note: stars measure attention, not maintenance. Before adopting anything from a list like this, check the last commit, the issue triage, and whether the project publishes releases. A high star count with a year of silence is a warning, not a recommendation.

## Summary

| Project | What it does | Stack | License | Stars (approx.) |
| --- | --- | --- | --- | --- |
| [Leis](https://github.com/ctresb/leis) | Brazilian legislation as Markdown | — | MIT (scripts) | 2.6k |
| [openTPU](https://github.com/FeSens/openTPU) | Open AI accelerator | Verilog | Apache-2.0 | 930 |
| [Reversa](https://github.com/sandeco/reversa) | Reverse-documentation agents | JavaScript | MIT | 1.9k |
| [DeskcommCRM](https://github.com/melgarafael/DeskcommCRM) | Self-hosted CRM with WhatsApp | TypeScript | MIT | 5.2k |
| [pgModeler](https://github.com/nullptrlabs/pgmodeler) | PostgreSQL data modeling | C++/Qt | GPL-3.0 | 3.6k |
| [VirtualBuddy](https://github.com/insidegui/VirtualBuddy) | macOS VMs on Apple Silicon | Swift | BSD-2-Clause | 8.9k |
| [Easy Effects](https://github.com/wwmm/easyeffects) | Real-time audio processing | — | GPL-3.0 | 10.5k |
| [navi](https://github.com/denisidoro/navi) | Interactive cheatsheets | Rust | Apache-2.0 | 17.8k |
| [Brasil API](https://github.com/BrasilAPI/BrasilAPI) | Brazilian public data API | Node.js | MIT | 11.5k |
| [Winlator](https://github.com/brunodev85/winlator) | Windows apps on Android | C | LGPL-2.1 | 19.8k |
| [PhotoGIMP](https://github.com/Diolinux/PhotoGIMP) | Photoshop-like GIMP setup | Python | GPL-3.0 | 18.5k |
| [Bend](https://github.com/bendlang/bend) | Massively parallel language | TypeScript | Apache-2.0 | 24.8k |
| [Git City](https://github.com/srizzon/git-city) | GitHub profile as a 3D city | Next.js/Three.js | AGPL-3.0 | 6k |
| [AI Memory](https://github.com/akitaonrails/ai-memory) | Memory for coding agents | Rust | MIT | 15.3k |
| [Open Notebook](https://github.com/lfnovo/open-notebook) | Self-hosted NotebookLM alternative | TypeScript | MIT | 41.7k |

## Conclusion

Lists like this are best used as a queue, not a catalog. Pick two projects that touch a problem you actually have — a legacy system without documentation, an integration with Brazilian public data, a CRM that needs to stay on your own infrastructure — and read the repository before the README's marketing.

The more interesting signal is structural: Brazilian open source is no longer limited to utilities and translations of foreign projects. There is original work in RTL design, programming language research, agent memory, and data infrastructure, published under licenses that allow commercial use.

---

## References

- [Video: 15 projetos open source brasileiros no GitHub](https://www.youtube.com/watch?v=rcoZzJ8ifeU)
- [Leis](https://github.com/ctresb/leis)
- [openTPU](https://github.com/FeSens/openTPU)
- [Reversa](https://github.com/sandeco/reversa)
- [DeskcommCRM](https://github.com/melgarafael/DeskcommCRM)
- [pgModeler](https://github.com/nullptrlabs/pgmodeler) — [pgmodeler.io](https://pgmodeler.io)
- [VirtualBuddy](https://github.com/insidegui/VirtualBuddy)
- [Easy Effects](https://github.com/wwmm/easyeffects)
- [navi](https://github.com/denisidoro/navi)
- [Brasil API](https://github.com/BrasilAPI/BrasilAPI) — [brasilapi.com.br](https://brasilapi.com.br)
- [Winlator](https://github.com/brunodev85/winlator) — [winlator.org](https://winlator.org)
- [PhotoGIMP](https://github.com/Diolinux/PhotoGIMP)
- [Bend](https://github.com/bendlang/bend) — [bend-lang.com](https://bend-lang.com)
- [Git City](https://github.com/srizzon/git-city) — [thegitcity.com](https://thegitcity.com)
- [AI Memory](https://github.com/akitaonrails/ai-memory) — [aimemory.sh](https://aimemory.sh)
- [Open Notebook](https://github.com/lfnovo/open-notebook) — [www.open-notebook.ai](https://www.open-notebook.ai)

---

At **EF-TECH**, we work with open-source infrastructure every day, from Kubernetes and GitOps to the integrations that connect Brazilian systems to the rest of the stack. [Contact us](/en/contato/) if your team needs help evaluating or operating these tools. For more articles like this, visit our [blog](/en/blog/).
