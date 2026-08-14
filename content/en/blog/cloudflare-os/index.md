---
title: "Cloudflare OS: An Open Source Operating System for AI Agents"
description: "Cloudflare announced Cloudflare OS, an open source AI workspace. Learn about the isolated runtime, zero-trust security with Gatekeepers, and model flexibility through AI Gateway."
summary: "Cloudflare OS is Cloudflare's open source 'operating system' for AI agents: a workspace connected to your company's internal systems, with an isolated runtime for code execution, zero-trust security by default via Gatekeepers, and support for any model through AI Gateway. Here is how it works and how your company can adopt it."
date: 2026-08-14
draft: false
tags: ["cloudflare", "ai-agents", "artificial-intelligence", "open-source", "security"]
categories: ["technology"]
featureimage: "cover.png"
featureimagecaption: "Cloudflare OS — an open source operating system for AI agents"
---

In early August 2026, Cloudflare announced **Cloudflare OS**, an open source "operating system" designed for AI agents. The launch was discussed on the [Código Fonte TV channel](https://www.youtube.com/watch?v=WwWYQ76E2C4) and detailed on the [official Cloudflare blog](https://blog.cloudflare.com/cloudflare-os/).

Unlike a traditional operating system, Cloudflare OS does not manage hardware: it manages what agents can see, execute, and access inside your organization — with security built directly into the architecture.

![Cloudflare OS](cover.png)

## What Is Cloudflare OS

Cloudflare OS started as the internal platform Cloudflare uses to run its global workforce. Thousands of employees — from engineering to sales — use Cloudflare OS every day to do research, create documents connected to live data, automate repetitive tasks, and build small work apps.

The platform is now open sourced as version 2, a complete rewrite that any organization can deploy into its own Cloudflare account and adapt to its context. In Cloudflare's own words, the goal is not that your company "uses Cloudflare OS," but that you turn it into *your company's OS*.

Access happens through the browser, with no development expertise required: every employee gets an AI agent with their own workspace.

## A Workspace Connected to Your Organization

In practice, Cloudflare OS works like a browser-based conversation — similar to other AI tools — but with one essential difference: every conversation is grounded in the **context and skills** your organization has curated.

That means the agent understands how your company works: the terminology, the procedures, and the best-known ways of doing things. When an employee finds a better way to do something, that knowledge becomes shared context and skills — and everyone benefits.

The workspace also connects to your organization's **internal systems**. The agent can consult documents, use the tools, and work with the data your company already relies on to achieve the goals it is given, instead of answering from generic knowledge.

## Core Components

Cloudflare OS combines three core components:

### Isolated Runtime for Code Execution

Agents get work done by writing and immediately executing code in an **isolated runtime** (sandbox), with its own dedicated storage. That code cannot reach the internet or your internal systems — except through resources your organization explicitly provides.

### Security and Governance

A **security and governance layer** controls access to internal data and services. The Gatekeepers framework applies guardrails to both agents and applications, so non-technical users can work freely — without anything bad happening.

### An Environment to Build and Share Apps

An **app environment** lets people build, share, and keep modifying small personal apps called "gadgets." Every app built on Cloudflare OS automatically gets an agent-friendly API, so you can collaborate with AI inside the app itself — no need to build an MCP server or wire up a custom agent loop.

## Zero-Trust Security by Default

Security is not an add-on in Cloudflare OS — it is built into the architecture. Key principles:

- **Zero-trust access by default**: built on Cloudflare Access, which verifies every user and every request before anything is granted.
- **Agents start with no permissions**: an AI agent begins with zero permissions and is given access only to what it needs for a specific task.
- **Per-agent isolation**: each agent runs in its own sandbox with its own storage. It cannot read another agent's storage.
- **Capability-based security**: instead of access control lists (ACLs), the model follows capability-based security — an agent is accountable to a human user while having its own restricted permissions.

### Gatekeepers: Credential Guardians

The heart of the security model is **Gatekeepers**, governed connectors that control access to each internal system. They hold the credentials, enforce policy, record what was read, and mediate agent actions.

In practice, the owner of each internal system decides what the AI can see, what it can change, and when a human must sign off before an action goes through. Gatekeepers also act as MCP Server Portals, bringing existing MCP servers under your organization's Access policy.

## Model Flexibility Through Cloudflare AI Gateway

Cloudflare OS is not tied to a single model. Through the **Cloudflare AI Gateway**, the platform works with any model — and the platform team gets one place to manage routing and spend.

That means teams can control budgets, set rate limits, and manage model availability, ensuring agents use the best cost-to-quality option for each task without depending on a single AI vendor.

## Open Source and Ready for Your Company

Cloudflare OS is available today on [GitHub](https://github.com/cloudflare/cloudflare-os) and can be deployed into your own Cloudflare account in minutes. Because it is open source and runs in your account, **your data, processes, and integrations stay yours** — nothing gets locked into a closed vendor product.

The current release is early access: very capable, but still under heavy development. Cloudflare is already working on a managed option in the dashboard, containers for development workflows, and workspaces for Slack and other chat tools.

## Learn More

- [Blog: Cloudflare OS — an open platform for agents, apps, and work](https://blog.cloudflare.com/cloudflare-os/)
- [cloudflare-os repository on GitHub](https://github.com/cloudflare/cloudflare-os)
- [Cloudflare OS official site](https://os.cloudflare.app/)
- [Cloudflare press release](https://www.cloudflare.com/press/press-releases/2026/cloudflare-os-is-the-first-ai-workspace-built-around-how-companies-actually-work/)
- [Código Fonte TV video](https://www.youtube.com/watch?v=WwWYQ76E2C4)

---

At **EF-TECH**, we help companies design and operate cloud computing, edge, and AI solutions — including adopting open source platforms like Cloudflare OS. [Contact us](/en/contato/) to discuss how your organization can get started. For more articles like this, visit our [blog](/en/blog/).