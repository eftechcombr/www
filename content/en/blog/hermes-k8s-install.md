---
title: "How to Install the Hermes Agent on Kubernetes"
description: "Step-by-step guide to installing and configuring the Hermes Agent on a Kubernetes cluster using Kustomize"
summary: "Learn how to deploy the Hermes Agent on Kubernetes with ConfigMap, Deployment, Services, cert-manager, and Ingress — all managed via Kustomize."
date: 2026-06-19
draft: false
tags: ["hermes", "kubernetes", "k8s", "devops", "deploy"]
categories: ["infrastructure"]
---

The [Hermes Agent](https://github.com/NousResearch/hermes-agent) is a powerful tool for orchestrating AI agents. In this guide, you'll learn how to install it on a Kubernetes cluster using the manifests available in the EF-TECH repository.

We'll cover each required resource — from ConfigMap to Ingress — explaining the role of each component and how to apply them with `kubectl` and Kustomize.

## Prerequisites

Before you begin, make sure you have:

- A Kubernetes cluster (v1.19+)
- `kubectl` configured to access the cluster
- `kustomize` installed (or `kubectl` v1.21+ with native `-k` support)
- [cert-manager](https://cert-manager.io/docs/installation/) installed (for TLS)
- A compatible `StorageClass` (the example uses `longhorn`)
- [Reloader](https://github.com/stakater/Reloader) (optional, for automatic secret reloads)

## Manifest structure

The manifest files are organized in the `iac/files/kubernetes/hermes/` directory:

```
iac/files/kubernetes/hermes/
├── configmap.yaml
├── deployment.yaml
├── ingress.yaml
├── issuer.yaml
├── kustomization.yaml
├── persistentvolumeclaim.yaml
└── service.yaml
```

## Step 1: Namespace

Create the `hermes` namespace to isolate resources:

```bash
kubectl create namespace hermes
```

## Step 2: ConfigMap

The ConfigMap defines environment variables for the Hermes Agent:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: hermes-config
  labels:
    app.kubernetes.io/name: hermes
    app.kubernetes.io/part-of: hermes
data:
  HERMES_DASHBOARD: "1"
  HERMES_UID: "10000"
  HERMES_GID: "10000"
  HERMES_DASHBOARD_HOST: "0.0.0.0"
  HERMES_DASHBOARD_INSECURE: "1"
  DASHBOARD_PORT: "9119"
  GATEWAY_PORT: "8642"
  API_SERVER_ENABLED: "true"
  API_SERVER_HOST: "0.0.0.0"
  WEBHOOK_ENABLED: "true"
  WEBHOOK_PORT: "8644"
```

Key variables:
- `HERMES_DASHBOARD=1` — enables the web dashboard
- `API_SERVER_ENABLED=true` — enables the REST API
- `WEBHOOK_ENABLED=true` — enables webhooks for integrations
- Ports: Gateway (`8642`), Dashboard (`9119`), Webhook (`8644`)

## Step 3: Secrets

The deployment references an external Secret named `hermes-secret` with the annotation `secret.reloader.stakater.com/reload`. This allows Reloader to automatically restart the pod when the secret is updated.

Create the secret manually:

```bash
kubectl create secret generic hermes-secret \
  --namespace hermes \
  --from-literal=API_KEY=your-key-here \
  --from-literal=OUTH_TOKEN=your-token-here
```

> **Note:** The exact values depend on your Hermes Agent configuration. Refer to the [official documentation](https://github.com/NousResearch/hermes-agent) for the complete list of expected variables.

## Step 4: PersistentVolumeClaim

The Hermes Agent needs persistent storage for data. The PVC requests 5Gi on a `longhorn` storage class:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: hermes-data
  labels:
    app.kubernetes.io/name: hermes
    app.kubernetes.io/part-of: hermes
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: longhorn
  resources:
    requests:
      storage: 5Gi
```

Adjust `storageClassName` to match what's available in your cluster (e.g., `standard`, `gp2`, `ebs-sc`).

## Step 5: Deployment

The Deployment manages the Hermes Agent pod using the `nousresearch/hermes-agent:latest` image:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hermes
  labels:
    app.kubernetes.io/name: hermes
    app.kubernetes.io/part-of: hermes
  annotations:
    secret.reloader.stakater.com/reload: "hermes-secret"
spec:
  replicas: 1
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app.kubernetes.io/name: hermes
  template:
    metadata:
      labels:
        app.kubernetes.io/name: hermes
      annotations:
        secret.reloader.stakater.com/reload: "hermes-secret"
    spec:
      restartPolicy: Always
      enableServiceLinks: false
      containers:
        - name: hermes
          image: nousresearch/hermes-agent:latest
          args: ["gateway", "run"]
          envFrom:
            - configMapRef:
                name: hermes-config
            - secretRef:
                name: hermes-secret
          ports:
            - name: gateway
              containerPort: 8642
            - name: dashboard
              containerPort: 9119
            - name: webhook
              containerPort: 8644
          livenessProbe:
            httpGet:
              path: /health
              port: gateway
            initialDelaySeconds: 120
            periodSeconds: 15
          readinessProbe:
            httpGet:
              path: /health
              port: gateway
            initialDelaySeconds: 15
            periodSeconds: 10
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "4Gi"
              cpu: "1"
          volumeMounts:
            - name: hermes-data
              mountPath: /opt/data
      volumes:
        - name: hermes-data
          persistentVolumeClaim:
            claimName: hermes-data
```

### Key points:

- **`Recreate` strategy**: required because `ReadWriteOnce` volumes cannot be mounted by multiple pods simultaneously
- **Health checks**: readiness probe starts after 15s, liveness probe after 120s (allowing time for agent initialization)
- **Resources**: low requests (256Mi/100m) with generous limits (4Gi/1 CPU) to handle usage spikes
- **Ports**: three exposed ports — gateway (8642), dashboard (9119), and webhook (8644)
- **Volume**: mounted at `/opt/data` for persistent data

## Step 6: Services

Three ClusterIP Services expose each port internally within the cluster:

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: hermes-gateway
  labels:
    app.kubernetes.io/name: hermes
    app.kubernetes.io/part-of: hermes
spec:
  type: ClusterIP
  selector:
    app.kubernetes.io/name: hermes
  ports:
    - name: gateway
      port: 8642
      targetPort: gateway
---
apiVersion: v1
kind: Service
metadata:
  name: hermes-dashboard
  labels:
    app.kubernetes.io/name: hermes
    app.kubernetes.io/part-of: hermes
spec:
  type: ClusterIP
  selector:
    app.kubernetes.io/name: hermes
  ports:
    - name: dashboard
      port: 9119
      targetPort: dashboard
---
apiVersion: v1
kind: Service
metadata:
  name: hermes-webhook
  labels:
    app.kubernetes.io/name: hermes
    app.kubernetes.io/part-of: hermes
spec:
  type: ClusterIP
  selector:
    app.kubernetes.io/name: hermes
  ports:
    - name: webhook
      port: 8644
      targetPort: webhook
```

Each service maps by port name as defined in the Deployment, ensuring correct routing.

## Step 7: TLS with cert-manager

The Issuer configures Let's Encrypt certificate issuance:

```yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: letsencrypt-hermes-prod
  namespace: hermes
spec:
  acme:
    email: suporte@eftech.com.br
    privateKeySecretRef:
      name: letsencrypt-hermes-prod
    server: https://acme-v02.api.letsencrypt.org/directory
    solvers:
      - http01:
          ingress:
            class: traefik
```

Replace the `email` with yours and adjust `class` to match your ingress controller (nginx, traefik, haproxy, etc.).

## Step 8: Ingress

The Ingress exposes the service externally with TLS:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: hermes-ingress
  annotations:
    cert-manager.io/issuer: "letsencrypt-hermes-prod"
spec:
  ingressClassName: traefik
  tls:
    - hosts:
        - hermes.eftech.com.br
      secretName: hermes-tls
  rules:
    - host: hermes.eftech.com.br
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: hermes-gateway
                port:
                  number: 8642
```

> **Note:** The Ingress is commented out in `kustomization.yaml` by default. Uncomment it when you're ready to expose the service.

## Step 9: Apply everything with Kustomize

With `kustomization.yaml` configured, apply all resources at once:

```bash
kubectl apply -k iac/files/kubernetes/hermes/ --namespace hermes
```

Kustomize processes the files in the correct order: PVC → ConfigMap → Deployment → Services → Issuer → Ingress.

## Verification

Check that the pod is running:

```bash
kubectl get pods -n hermes
```

Follow the logs:

```bash
kubectl logs -n hermes -l app.kubernetes.io/name=hermes
```

Test the health check:

```bash
kubectl port-forward -n hermes svc/hermes-gateway 8642:8642
curl http://localhost:8642/health
```

Access the dashboard:

```bash
kubectl port-forward -n hermes svc/hermes-dashboard 9119:9119
# Open http://localhost:9119 in your browser
```

## Conclusion

In this guide, you installed the Hermes Agent on Kubernetes with:

- ConfigMap for centralized configuration
- Externally managed Secrets with Reloader
- Persistent storage via PVC with Longhorn
- Deployment with health checks and resource limits
- Services for internal exposure
- cert-manager for automatic TLS
- Ingress for external access

The entire configuration is declarative and versioned with Kustomize, making it easy to maintain and replicate across environments.

At **EF-TECH**, we help companies plan and execute Kubernetes deployments focused on reliability and best practices. [Contact us](/en/contato/) to learn how we can help your team.
