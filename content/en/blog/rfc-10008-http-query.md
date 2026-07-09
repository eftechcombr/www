---
title: "Understanding RFC 10008: The HTTP QUERY Method"
description: "A deep dive into RFC 10008, introducing the HTTP QUERY method as a safe, idempotent alternative for large-volume data retrieval."
summary: "RFC 10008 standardizes the HTTP QUERY method, filling the long-standing gap between GET and POST. It enables safe, idempotent requests that carry parameters in the request body, solving URI length limits while retaining caching and retry benefits."
date: 2026-07-09
draft: false
tags: ["http", "rfc", "web-development", "api", "architecture"]
categories: ["architecture"]
---

The IETF has officially published **RFC 10008**, standardizing the **HTTP QUERY** request method. This specification defines a new, standardized way to execute safe and idempotent queries carrying complex or voluminous query parameters within the request body. 

For years, developers have struggled with the trade-offs of using `GET` versus `POST` for search and query endpoints. RFC 10008 fills this gap, offering a clean, idiomatic solution for modern API design.

Here is a comprehensive breakdown of the HTTP QUERY method, why it matters, and how to use it.

---

## The Core Problem: GET vs. POST

Historically, web APIs had two primary options for retrieving data:

1. **HTTP GET**: Excellent for retrieving resources because it is safe (does not change server state) and idempotent (can be repeated without side effects). However, `GET` parameters must be encoded in the URI. If a query has complex parameters (e.g., deep JSON filters, raw SQL, or long search terms), the URI can quickly exceed size limits (usually recommended to be at least 8000 octets, but limits vary across proxies and browsers). Furthermore, URIs are frequently logged in plain text, presenting a security risk for sensitive query data.
2. **HTTP POST**: Allows parameters to be sent in the request body, bypassing URI length limits and logging risks. However, `POST` is not semantically safe or idempotent by default. Caches, proxies, and web browsers cannot automatically retry failed `POST` requests, nor can they cache the results easily.

### The QUERY Method Compromise

The `QUERY` method acts as a bridge. Like `POST`, the input to the operation is passed in the request body (the query content) rather than in the URI. Like `GET`, the method is explicitly **safe** and **idempotent**, allowing features like caching and automatic retries to operate out-of-the-box.

---

## Method Property Comparison

The table below summaries how `QUERY` compares to `GET` and `POST` (adapted from the RFC specification):

| Property | GET | QUERY | POST |
| :--- | :--- | :--- | :--- |
| **Safe** | Yes | Yes | Potentially No |
| **Idempotent** | Yes | Yes | Potentially No |
| **URI for Query Itself** | Yes (by definition) | Optional (`Location` header) | No |
| **URI for Query Result** | Optional (`Content-Location`) | Optional (`Content-Location`) | Optional (`Content-Location`) |
| **Cacheable** | Yes | Yes | Yes, but only for future GET/HEAD |
| **Request Body** | No defined semantics | Expected (per resource rules) | Expected (per resource rules) |

---

## Examples in Action

Let’s look at how a typical verbose query is transformed from `GET` or `POST` to the new `QUERY` method.

### The old, verbose GET pattern:
If the parameters are too large, this is inefficient to parse, risks being truncated, and exposes data in server logs:

```http
GET /feed?q=foo&limit=10&sort=-published&filter=highly-specific-nested-filter-content HTTP/1.1
Host: example.org
```

### The old POST workaround:
While safe from logging and truncation, intermediaries cannot assume this request is safe or idempotent:

```http
POST /feed HTTP/1.1
Host: example.org
Content-Type: application/x-www-form-urlencoded

q=foo&limit=10&sort=-published
```

### The new QUERY Method:
By sending a `QUERY` request, we get the best of both worlds:

```http
QUERY /feed HTTP/1.1
Host: example.org
Content-Type: application/x-www-form-urlencoded
Accept: application/json

q=foo&limit=10&sort=-published
```

#### Response:
```http
HTTP/1.1 200 OK
Content-Type: application/json

[
  { "id": 1, "title": "First Match" },
  { "id": 2, "title": "Second Match" }
]
```

---

## Key Technical Features of RFC 10008

### 1. The `Accept-Query` Header Field
Servers can advertise their support for `QUERY` and the formats they accept using the `Accept-Query` response header. It uses the modern "Structured Fields" syntax:

```http
Accept-Query: "application/jsonpath", application/sql;charset="UTF-8"
```

Clients can discover support through an `OPTIONS` request or by inspecting the `Allow` header in a `405 Method Not Allowed` response:

```http
OPTIONS /contacts HTTP/1.1
Host: example.org

--- Response ---
HTTP/1.1 200 OK
Allow: GET, QUERY, OPTIONS, HEAD
```

### 2. Caching & Caching Keys
Caching `QUERY` requests is inherently more complex than caching `GET` requests because the cache must compute a key using both the URI and the request body (the query content) along with relevant metadata.

To optimize caching, caches are permitted to normalize minor, semantically insignificant differences in request bodies (such as stripping content encoding or JSON whitespace normalization) before generating the cache key.

### 3. Redirection & Equivalent Resources
When executing a `QUERY`, the server can assign a URI to either the query definition itself or the specific query result. 

- **`Location` response field**: Indicates a URI representing the query itself. A client can perform a standard `GET` request on this URI to repeat the query without resending the heavy body payload.
- **`Content-Location` response field**: Points to a temporary resource containing the static result of the query just executed.

For instance, the server might respond with:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Location: /contacts/stored-queries/42
Content-Location: /contacts/stored-results/17
```

Clients can subsequently execute a `GET /contacts/stored-queries/42` request to run the same query again.

---

## Security Considerations

RFC 10008 highlights several safety advantages and implementation requirements:

- **Logging Avoidance**: Query parameters are enclosed in the body, mitigating the risk of exposing sensitive data (like user IDs or custom search terms) in plain-text server and proxy logs.
- **Temporary Resource URIs**: If a server assigns a URI to a query (using `Location` or `Content-Location`), it **must** ensure that the newly created URI itself does not contain sensitive parts of the original request body in plain text.
- **CORS Handling**: Browsers implementing Cross-Origin Resource Sharing (CORS) will trigger a "preflight" options request for `QUERY` because it is not in the CORS-safelisted method group.

---

## Conclusion & Further Reading

The standardization of the `QUERY` method represents a significant milestone in RESTful architecture. It cleans up the semantic abuse of `POST` for searching, resolves the size constraints and security leaks of `GET`, and opens up better optimization avenues for API servers and caches alike.

As web frameworks and reverse proxies begin implementing native support for RFC 10008, developers should consider adopting `QUERY` for all search, filter, and reporting endpoints carrying non-trivial query payloads.

To read the complete technical specification, check the official standard:
- [RFC 10008: The HTTP QUERY Method](https://www.rfc-editor.org/info/rfc10008/)

Are you looking to modernize your API architecture or improve observability across your systems? At EF-TECH, we help organizations design scalable, efficient, and robust software architectures. [Contact us](/en/contato/).
