---
title: "mcp-glpi"
description: "mcp-glpi v3.4: MCP server connecting AI assistants to GLPI with OAuth2, 88 tools, and GLPI 11 and 12 support."
summary: "Connect AI assistants to GLPI with 88 tools for tickets, ITIL, assets, RSQL search, and statistics. EF-TECH supports evaluation, deployment, and operations."
date: 2026-10-14
tags: ["mcp-glpi", "glpi", "mcp", "ai", "service-desk", "open-source"]
categories: ["produtos"]
---
## mcp-glpi

**mcp-glpi v3.4** is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that connects MCP-compatible AI assistants to GLPI. It exposes standardized tools for querying and operating tickets, assets, problems, changes, and other GLPI resources, bringing AI closer to the daily work of service desk and operations teams.

The project uses the stable **High-Level API v2.3** path, compatible with GLPI 11 and GLPI 12. EF-TECH can support use-case evaluation, deployment, and operation of the integration according to the organization's environment and requirements.

### Coverage for service desk and operations

mcp-glpi provides **88 MCP tools** across the main operational areas of GLPI:

- Tickets, followups, tasks, solutions, validations, and SLA tracking
- Problems and changes
- Computers, software, network equipment, printers, monitors, and phones
- Knowledge base, contracts, suppliers, locations, and projects
- Users, groups, categories, entities, and documents
- Multi-criteria search, counts, and statistics

Ticket tools include chronological timelines, user or group assignment, ticket linking, validation requests, and task lifecycle management with time tracking. This lets AI assistants query operational context and perform GLPI actions while respecting the permissions and configuration of the GLPI instance.

### Search and operational visibility

Multi-criteria search accepts RSQL filters with `AND`, `OR`, `AND NOT`, and `OR NOT`, together with field selection, pagination, full-result retrieval, and a dedicated count probe. Dynamic searchable-field mapping helps keep the integration valid across GLPI versions. Ticket search provides direct parameters for status, assignee, requester, and date ranges.

The server can report ticket statistics by status, category, technician, entity, or month, asset totals by type, and tickets past their SLA deadline. Detail responses can resolve foreign keys and return both the related ID and readable name.

### OAuth2 authentication and safety signals

Tools include MCP safety annotations to distinguish read and write operations. Listing, get, search, count, and statistics tools receive `readOnlyHint`; update, delete, set, and assignment operations receive `destructiveHint`. Ticket tools also validate runtime inputs with Zod and return structured `InvalidParams` errors when parameters are invalid.

mcp-glpi v3 uses OAuth2 with `password`, `client_credentials`, or a `bearer` token. The v2 API `app_token` and `user_token` authentication is **not supported in v3**. An OAuth2 client with the appropriate grant must be configured in GLPI; credentials are supplied through environment variables or the HTTP session configuration. See the project README for the complete variable table and requirements for each method.

### Transport: stdio or Streamable HTTP

With **stdio** transport, the MCP client starts the server as a subprocess and exchanges messages through stdin/stdout. This is suitable for local integrations such as `bunx` or a container started by the client. With Docker, keep `-i` to preserve stdin and **do not use `-t`**, because a TTY can corrupt the protocol stream:

```bash
docker pull ghcr.io/eftechcombr/mcp-glpi:latest
docker run -i --rm --env-file /absolute/path/.env \
  ghcr.io/eftechcombr/mcp-glpi:latest
```

With **Streamable HTTP** transport, the server accepts network connections. Set `MCP_TRANSPORT=http` and publish the service port:

```bash
docker run -d --name mcp-glpi-http -p 3000:3000 \
  -e MCP_TRANSPORT=http -e PORT=3000 \
  ghcr.io/eftechcombr/mcp-glpi:latest
```

The default MCP endpoint is `/mcp`; `/health` and `/` provide health endpoints. When using a reverse proxy, the `/mcp` path must forward streaming without SSE buffering.

Streamable HTTP supports two operating models:

- **Single-tenant:** `GLPI_URL` and the authentication variables define one instance for sessions.
- **Multi-tenant:** leave `GLPI_URL` unset and let each session configure its own connection with `glpi_configure_connection`. Credentials remain in memory and are removed when the session ends or expires.

In multi-tenant mode, the client checks `glpi_connection_status`, calls `glpi_configure_connection` with the URL, OAuth2 method, and matching credentials, and then uses the tools normally.

### How EF-TECH can help

EF-TECH can support AI use-case assessment for service desk, GLPI and MCP client configuration, containerized execution, and service operations. The scope is defined according to the environment's architecture, permissions, and security requirements.

The source code is available on [GitHub](https://github.com/eftechcombr/mcp-glpi), with a package published on [npm](https://www.npmjs.com/package/mcp-glpi). See the README for the complete configuration, tool catalogue, and development details.

---

Want to connect AI to your company's GLPI? [Contact us](/en/contato/) to speak with our team.
