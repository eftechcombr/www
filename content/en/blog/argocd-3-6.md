---
title: "Argo CD 3.6: Server-Side Diff by default, performance work, and the end of support for 3.3"
description: "Argo CD v3.6 removes Structured-Merge Diff in favor of Server-Side Diff, cuts refresh cost on large fleets, adds an OCI generator to ApplicationSets, and ends support for 3.3."
summary: "Argo CD v3.6 replaces the engine that compares desired and live state: Structured-Merge Diff is gone, and Server-Side Diff now applies to Applications with ServerSideApply=true via a dry-run against the kube-apiserver. The release also brings refresh-path performance work, an OCI generator and a tpl function for ApplicationSets, a more responsive UI, new built-in health checks, and breaking changes in OpenTelemetry. v3.6.1 fixes two UI issues, and 3.3 reaches end of life."
date: 2026-11-05
draft: false
tags: ["argocd", "kubernetes", "gitops", "server-side-apply", "devops"]
categories: ["infrastructure"]
---

Argo CD v3.6.0 was published on November 3, 2026, and received a patch the following day, v3.6.1. The release touches a central part of the controller: how Argo CD computes the diff between desired and live state in the cluster. It also marks the end of life (EOL) of Argo CD v3.3, which no longer receives bug or security fixes.

## Server-Side Diff becomes the comparison engine

This is the change with the highest potential for silent impact. The diff decides whether an Application is `Synced` or `OutOfSync`, which in turn feeds alerts, automated sync policies, and the perceived health of the environment.

In v3.6, **Structured-Merge Diff has been removed**, and **Server-Side Diff is now used when the Application has the `ServerSideApply=true` sync option**. Instead of locally simulating Server-Side Apply merge semantics, the controller runs a **Server-Side Apply dry-run against the kube-apiserver** and compares the result. Server-Side Diff is also triggered when `controller.diff.server.side` is enabled or when the `argocd.argoproj.io/compare-options: ServerSideDiff=true` annotation is present.

The motivation is accuracy: where Structured-Merge approximated SSA with an in-memory model, the dry-run answers with what the cluster would actually do. That shrinks the class of bugs where the UI reports `Synced` but the sync fails.

The cost comes as calls to the kube-apiserver, proportional to the number of resources in Applications using `ServerSideApply=true`. On large fleets, watch apiserver load after upgrading; results are cached until a refresh, a new revision, a spec change, or a `resourceVersion` change.

There is a useful side effect: **validating webhooks now take part in the diff stage**, so a rejected resource surfaces as a diff error rather than only failing at sync time.

If the change causes trouble, the opt-out is per Application:

```yaml
metadata:
  annotations:
    argocd.argoproj.io/compare-options: ServerSideDiff=false
```

That falls back to the legacy client-side diff — an escape hatch for specific cases, not a desirable long-term state.

## Performance: the cost of refresh on large fleets

Much of the 3.6 work is invisible in the UI but shows up in controller response time as the number of Applications grows: partial JSON unmarshalling, removal of two redundant Application copies from the refresh path, counting Applications per cluster in a single pass, resolving the destination server without copying the cluster object, reusing matrix child parameters when the generator is unchanged, and configurable serialization and compression for cached manifests. Refresh is the most frequent operation in Argo CD, and any unnecessary allocation is multiplied by thousands of Applications; configurable compression, in turn, trades CPU for memory and cache size.

## ApplicationSet: OCI generator, `tpl`, and stricter progressive sync

The **OCI generator** creates Applications from the files or the directory structure inside an OCI artifact, in the same spirit as the Git generator. For teams already publishing charts and config bundles to a registry — including air-gapped environments with a mirrored registry — it removes the need to keep a Git repository just to serve those files. The **`tpl`** function renders strings as templates inside the ApplicationSet template itself, simplifying generators with composed values.

The third change is behavioral: **progressive sync now refreshes the Applications it owns and waits for reconciliation before deciding the next step**. Decisions reflect actual state rather than assumed state — more correct, but potentially slower on large fleets. The release also exposes progressive sync metrics and workqueue rate-limiter flags on the applicationset-controller, surfaces scenario details in `conditions` as reason and message, and adds an annotation to force reconciliation before proceeding.

## UI: responsiveness, search, and the 3.6.1 fixes

The UI gained a new **resources explorer view**, virtual scrolling for the Applications list and tiles when the "all" filter is selected, and lazy loading. The build now uses the **React Compiler**, cutting re-renders on large lists — a gain nobody notices until the list stops freezing.

The name filter on the Applications list now runs server-side, so search no longer depends on every object already being in the browser. Application and ApplicationSet lists gained a regex search toggle, and settings pages received search, pagination, and an advanced settings view. Sidebar anchors, a button to clear logs in the pod log viewer, and a CronJob summary showing last scheduled and last successful times also landed.

v3.6.1 fixes two issues: the sidebar no longer staying in sync after collapsing or expanding, and webpack, which no longer minifies `index.html` — required for `--rootpath` and `--basehref` to work. If you run Argo CD behind a proxy with a path prefix, go straight to 3.6.1.

## Health checks: broader coverage and more context

The list of built-in health checks grew: Kyverno, TLSRoute, AWS ACK, CloudNativePG, Prometheus Operator, cert-manager, trust-manager, ACME, Tekton, Velero, Flink, Kro, Medusa, Pulumi, KServe, Envoy Gateway, Airlock microgateway, and Gateway API ListenerSet; the VictoriaMetrics health check now ignores status. Every custom health check in `argocd-cm` is code someone reviews when the CRD changes, so built-in coverage is maintenance you no longer own.

Two behavior changes deserve attention. During deletion, the default health check now **lists pending finalizers**, making it explicit why a resource is still `Progressing`. And built-in or custom health checks can return an optional `deletionMessage` to override the default "Pending deletion" wording — useful to explain long-lived finalizers and warn when manual removal is required.

Health transition events now identify the resource or resources that caused the change, with a `(Caused by ...)` suffix covering up to three resources: `Updated health status: Healthy -> Degraded (Caused by apps/Deployment:default/api)`.

## Security, authentication, and cluster configuration

**Rollback now has a separate RBAC permission**, letting you grant sync without granting rollback — a useful distinction where reverting is riskier than applying the current revision from Git. In `argocd proj list`, `SIGNATURE-KEYS` was replaced by `SOURCE-INTEGRITY`, and `--signature-keys` emits a deprecation warning, which requires adjusting scripts that parse that output.

In Dex, the minimum TLS version, cipher suites, and curve preferences are now configurable, as are storage type and configuration from `argocd-cm`; redirecting to a selected connector is in Alpha. The login screen gained configurable button text via `ui.loginButtonText`, and the instance can send `X-Robots-Tag` to keep search engines from indexing it — relevant when the UI is exposed on an internal network. The Swagger UI endpoint can also be disabled.

## OpenTelemetry: breaking changes

This section deserves its own heading because it holds the change most likely to cause data loss with no visible error. The repo-server variable `ARGOCD_REPO_OTLP_HEADERS` was renamed to `ARGOCD_REPO_SERVER_OTLP_HEADERS`. Default manifests already use the new name, but any custom manifest that sets the old one keeps applying without error — and without sending headers.

The remaining OTLP changes:

- header values containing `=` (base64 credentials) are now accepted;
- with `otlp.insecure: "false"`, Argo CD also trusts the collector CA in `argocd-tls-certs-cm` and honors `OTEL_EXPORTER_OTLP_CERTIFICATE`, `OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE`, `OTEL_EXPORTER_OTLP_CLIENT_KEY` (mTLS), and `OTEL_EXPORTER_OTLP_HEADERS`;
- `otlp.insecure` now fully decides between TLS and plaintext;
- the sampler is now parent-based and configurable via `--otlp-sample-ratio` or `ARGOCD_<COMPONENT>_OTLP_SAMPLE_RATIO` (default 1.0), with the decision propagating across services and inbound "not sampled" `traceparent` decisions honored;
- instrumentation was upgraded to otelgrpc/otelhttp v0.70.0 (semantic conventions 1.42.0/1.43.0), and `server.address`/`server.port` now come from the gRPC dial target.

That last item is the usual breaker: dashboards and alerts that group by those labels may see different values after the upgrade.

## Smaller changes that affect automation

- **Helm:** in `argocd app diff --local --server-side-generate`, the default `--local-include` now includes `*.tpl` and `Chart.lock` alongside YAML and JSON. Passing the flag explicitly still replaces the whole default set.
- **Webhooks:** Harbor and DockerHub support, plus `manifest-generate-paths` annotation support for BitBucket Server.
- **Cluster:** a new ephemeral `configHash` field detects configuration changes; it is not stored in the cluster secret, is computed at query time, and its value is opaque.
- **Connectivity and CLI:** a server-side timeout query parameter sent through a transport wrapper, `HTTP_PROXY`/`HTTPS_PROXY`/`NO_PROXY` honored for gRPC-web, and `argocd login` persisting and reusing client certificates.

## How to upgrade

The upgrade follows the standard manifest procedure, using the already patched version:

```bash
kubectl apply -n argocd --server-side --force-conflicts \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/v3.6.1/manifests/install.yaml
```

For high availability, use `manifests/ha/install.yaml` at the same version path. Before applying: confirm no custom manifest still sets `ARGOCD_REPO_OTLP_HEADERS`; review dashboards that depend on `server.address`/`server.port`; identify Applications with `ServerSideApply=true` to estimate apiserver impact; and check whether CI scripts rely on the default `--local-include` list.

## Conclusion

3.6 is a consolidation release with a structural change in the middle. By swapping Structured-Merge Diff for a real dry-run against the kube-apiserver, Argo CD gains accuracy in what it does most — telling you whether the cluster matches Git — at the cost of depending more on the cluster API. The cache and the escape hatch suggest the risk was handled carefully.

For large fleets, the performance work and stricter progressive sync matter more than any single UI item. For anyone still on 3.3, the argument is different: the line is out of support.

---

## References

- [Argo CD v3.6 announcement on X](https://x.com/argoproj/status/2117890245639250274)
- [Official post: Argo CD v3.6 RC1](https://blog.argoproj.io/argo-cd-v3-6-rc1-is-here-c0b562dc78d1)
- [Release v3.6.0 on GitHub](https://github.com/argoproj/argo-cd/releases/tag/v3.6.0)
- [Release v3.6.1 on GitHub](https://github.com/argoproj/argo-cd/releases/tag/v3.6.1)
- [Upgrade guide 3.5 → 3.6](https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/3.5-3.6/)
- [Argo CD documentation](https://argo-cd.readthedocs.io/)
- [Argo CD 3.5 and the ApplicationSet UI](/en/blog/argocd-appset-ui/)

---

At **EF-TECH**, we help companies implement and operate GitOps workflows with Argo CD at scale, from repository layout and sync policies to running multi-cluster fleets. [Contact us](/en/contato/) to find out how we can support your team. For more articles like this, visit our [blog](/en/blog/).
