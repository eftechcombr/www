---
title: "Como instalar o Hermes Agent usando Kubernetes"
description: "Guia passo a passo para instalar e configurar o Hermes Agent em um cluster Kubernetes usando Kustomize"
summary: "Aprenda a fazer deploy do Hermes Agent no Kubernetes com ConfigMap, Deployment, Services, cert-manager e Ingress — tudo gerenciado via Kustomize."
date: 2026-06-19
draft: false
tags: ["hermes", "kubernetes", "k8s", "devops", "implantacao"]
categories: ["infraestrutura"]
---

O [Hermes Agent](https://github.com/NousResearch/hermes-agent) é uma ferramenta poderosa para orquestração de agentes de IA. Neste guia, você vai aprender a instalá-lo em um cluster Kubernetes utilizando os manifestos disponíveis no repositório da EF-TECH.

Vamos cobrir cada recurso necessário — desde o ConfigMap até o Ingress — explicando o papel de cada componente e como aplicá-los com `kubectl` e Kustomize.

## Pré-requisitos

Antes de começar, certifique-se de ter:

- Um cluster Kubernetes (v1.19+)
- `kubectl` configurado para acessar o cluster
- `kustomize` instalado (ou `kubectl` v1.21+ com suporte nativo a `-k`)
- [cert-manager](https://cert-manager.io/docs/installation/) instalado (para TLS)
- Uma `StorageClass` compatível (o exemplo usa `longhorn`)
- [Reloader](https://github.com/stakater/Reloader) (opcional, para recarga automática de secrets)

## Estrutura dos manifestos

Os arquivos de manifesto estão organizados no diretório `iac/files/kubernetes/hermes/`:

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

## Passo 1: Namespace

Crie o namespace `hermes` para isolar os recursos:

```bash
kubectl create namespace hermes
```

## Passo 2: ConfigMap

O ConfigMap define as variáveis de ambiente do Hermes Agent:

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

Principais variáveis:
- `HERMES_DASHBOARD=1` — habilita o dashboard web
- `API_SERVER_ENABLED=true` — ativa a API REST
- `WEBHOOK_ENABLED=true` — ativa o webhook para integrações
- Portas: Gateway (`8642`), Dashboard (`9119`), Webhook (`8644`)

## Passo 3: Secrets

O deployment referencia um Secret externo chamado `hermes-secret` com a anotação `secret.reloader.stakater.com/reload`. Isso permite que o Reloader reinicie o pod automaticamente quando o secret for atualizado.

Crie o secret manualmente:

```bash
kubectl create secret generic hermes-secret \
  --namespace hermes \
  --from-literal=API_KEY=sua-chave-aqui \
  --from-literal=OUTH_TOKEN=seu-token-aqui
```

> **Nota:** Os valores exatos dependem da configuração do seu Hermes Agent. Consulte a [documentação oficial](https://github.com/NousResearch/hermes-agent) para obter a lista completa de variáveis esperadas.

## Passo 4: PersistentVolumeClaim

O Hermes Agent precisa de armazenamento persistente para dados. O PVC solicita 5Gi em um storage class `longhorn`:

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

Ajuste o `storageClassName` conforme a disponível no seu cluster (use `standard`, `gp2`, `ebs-sc` etc.).

## Passo 5: Deployment

O Deployment gerencia o pod do Hermes Agent com a imagem `nousresearch/hermes-agent:latest`:

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

### Pontos importantes:

- **Estratégia `Recreate`**: necessária porque o volume `ReadWriteOnce` não pode ser montado por múltiplos pods simultaneamente
- **Health checks**: o readiness probe começa após 15s e o liveness probe após 120s (tempo para o agente inicializar)
- **Recursos**: requests baixos (256Mi/100m) com limits generosos (4Gi/1 CPU) para acomodar picos de uso
- **Portas**: três portas expostas — gateway (8642), dashboard (9119) e webhook (8644)
- **Volume**: montado em `/opt/data` para dados persistentes

## Passo 6: Services

Três Services do tipo ClusterIP expõem cada porta internamente no cluster:

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

Cada service mapeia pelo nome da porta definida no Deployment, garantindo o roteamento correto.

## Passo 7: TLS com cert-manager

O Issuer configura a emissão de certificados Let's Encrypt:

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

Substitua o `email` pelo seu e-mail e ajuste `class` para o ingress controller do seu cluster (nginx, traefik, haproxy etc.).

## Passo 8: Ingress

O Ingress expõe o serviço externamente com TLS:

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

> **Nota:** O Ingress está comentado no `kustomization.yaml` por padrão. Descomente quando estiver pronto para expor o serviço.

## Passo 9: Aplicar tudo com Kustomize

Com o `kustomization.yaml` configurado, aplique todos os recursos de uma vez:

```bash
kubectl apply -k iac/files/kubernetes/hermes/ --namespace hermes
```

O Kustomize processa os arquivos na ordem correta: PVC → ConfigMap → Deployment → Services → Issuer → Ingress.

## Verificação

Confira se o pod está rodando:

```bash
kubectl get pods -n hermes
```

Acompanhe os logs:

```bash
kubectl logs -n hermes -l app.kubernetes.io/name=hermes
```

Teste o health check:

```bash
kubectl port-forward -n hermes svc/hermes-gateway 8642:8642
curl http://localhost:8642/health
```

Acesse o dashboard:

```bash
kubectl port-forward -n hermes svc/hermes-dashboard 9119:9119
# Abra http://localhost:9119 no navegador
```

## Conclusão

Neste guia, você instalou o Hermes Agent no Kubernetes com:

- ConfigMap para configuração centralizada
- Secrets gerenciados externamente com Reloader
- Persistência via PVC com Longhorn
- Deployment com health checks e limites de recursos
- Services para exposição interna
- cert-manager para TLS automático
- Ingress para acesso externo

Toda a configuração é declarativa e versionada com Kustomize, facilitando manutenção e replicação em outros ambientes.

Na **EF-TECH**, ajudamos empresas a planejar e executar implantações Kubernetes com foco em confiabilidade e boas práticas. [Entre em contato](/pt-br/contato/) para saber como podemos ajudar sua equipe.
