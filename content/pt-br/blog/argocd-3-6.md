---
title: "Argo CD 3.6: Server-Side Diff como padrão, performance e o fim do suporte ao 3.3"
description: "O Argo CD v3.6 remove o Structured-Merge Diff em favor do Server-Side Diff, reduz o custo de refresh em frotas grandes, adiciona generator OCI ao ApplicationSet e encerra o suporte ao 3.3."
summary: "O Argo CD v3.6 troca o motor de comparação de estado: o Structured-Merge Diff sai de cena e o Server-Side Diff passa a valer para Applications com ServerSideApply=true, via dry-run contra o kube-apiserver. A release também traz ganhos de performance no caminho de refresh, generator OCI e função tpl no ApplicationSet, uma interface mais responsiva, novos health checks embutidos e mudanças que quebram no OpenTelemetry. O v3.6.1 corrige dois problemas de interface, e o v3.3 chega ao fim de vida."
date: 2026-11-05
draft: false
tags: ["argocd", "kubernetes", "gitops", "server-side-apply", "devops"]
categories: ["infraestrutura"]
---

O Argo CD v3.6.0 foi publicado em 3 de novembro de 2026 e recebeu um patch no dia seguinte, o v3.6.1. A release mexe em uma peça central do controlador: como o Argo CD calcula o diff entre o estado desejado e o real no cluster. Ela também marca o fim de vida (EOL) do Argo CD v3.3, que deixa de receber correções de bug e de segurança.

## Server-Side Diff passa a ser o motor de comparação

Esta é a mudança com maior potencial de impacto silencioso. O diff decide se uma Application está `Synced` ou `OutOfSync`, alimentando alertas, políticas de sync automatizado e a percepção de saúde do ambiente.

Na v3.6, o **Structured-Merge Diff foi removido** e o **Server-Side Diff passa a ser usado quando a Application tem a sync option `ServerSideApply=true`**. Em vez de simular localmente a semântica de merge do Server-Side Apply, o controlador faz um **dry-run de Server-Side Apply contra o kube-apiserver** e compara o resultado. O Server-Side Diff também é acionado quando `controller.diff.server.side` está habilitado ou quando existe a annotation `argocd.argoproj.io/compare-options: ServerSideDiff=true`.

A motivação é precisão: o Structured-Merge aproximava o SSA com um modelo em memória, enquanto o dry-run responde com o que o cluster realmente faria. Isso reduz a classe de bugs em que a interface mostra `Synced` mas o sync falha.

O custo vem em chamadas ao kube-apiserver proporcionais ao número de recursos das Applications com `ServerSideApply=true`. Em frotas grandes, acompanhe a carga do apiserver após o upgrade; o resultado é cacheado até haver refresh, nova revisão, mudança no spec ou no `resourceVersion`.

E há um efeito colateral útil: **validating webhooks agora participam da etapa de diff**, então um recurso rejeitado aparece como erro de diff, não apenas como falha no sync.

Se a mudança causar problema, o opt-out é por Application:

```yaml
metadata:
  annotations:
    argocd.argoproj.io/compare-options: ServerSideDiff=false
```

Isso retorna ao diff client-side legado — uma válvula de escape para casos específicos, não um estado desejável a longo prazo.

## Performance: o custo de refresh em frotas grandes

Boa parte dos ganhos da 3.6 não aparece em nenhuma tela, mas no tempo de resposta do controlador quando o número de Applications cresce: unmarshalling parcial de JSON, remoção de duas cópias redundantes da Application no caminho de refresh, contagem de Applications por cluster em uma única passagem, resolução do servidor de destino sem copiar o objeto de cluster, reaproveitamento dos parâmetros dos filhos de Matrix quando o generator não mudou, e serialização e compressão configuráveis dos manifests em cache. O refresh é a operação mais frequente do Argo CD, e qualquer alocação desnecessária é multiplicada por milhares de Applications; a compressão configurável, por sua vez, troca CPU por memória e tamanho de cache.

## ApplicationSet: generator OCI, `tpl` e progressive sync mais rigoroso

O **generator OCI** cria Applications a partir de arquivos ou da estrutura de diretórios de um artefato em registry OCI, no mesmo espírito do generator Git. Para quem já publica charts e bundles de configuração em um registry — inclusive em ambientes air-gapped com registry espelhado — ele elimina a necessidade de manter um repositório Git só para servir esses arquivos. A função **`tpl`** permite renderizar strings como templates dentro do próprio template do ApplicationSet, simplificando generators com valores compostos.

A terceira mudança é comportamental: o **progressive sync agora atualiza as Applications que possui e espera a reconciliação antes de decidir o próximo passo**. A decisão reflete o estado real, e não o assumido — mais correto, porém potencialmente mais lento em frotas grandes. A release também expõe métricas de progressive sync e flags de rate limiter da workqueue no applicationset-controller, detalhes de cenário em `conditions` como reason e message, e uma annotation para forçar reconciliação antes de prosseguir.

## Interface: responsividade, busca e ajustes do 3.6.1

A interface ganhou uma **visão de resources explorer**, scrolling virtual na lista de Applications e nos tiles quando o filtro "all" está selecionado, e lazy loading. O build passou a usar o **React Compiler**, reduzindo rerenderizações em listas grandes — ganho invisível até a lista deixar de travar.

O filtro por nome na lista de Applications passou a rodar no servidor, então a busca não depende mais de todos os objetos já estarem no navegador. As listas de Applications e ApplicationSets ganharam toggle de busca por regex, e as páginas de settings receberam busca, paginação e uma visão de configurações avançadas. Também entraram âncoras na sidebar, botão para limpar logs no visualizador de pods e resumo de CronJob com as datas do último agendamento e da última execução.

O v3.6.1 corrige dois problemas: a sidebar que não permanecia sincronizada após ser recolhida ou expandida, e o webpack, que não minifica mais o `index.html` — necessário para que `--rootpath` e `--basehref` funcionem. Quem roda o Argo CD atrás de um proxy com prefixo de caminho deve subir direto para o 3.6.1.

## Health checks: mais cobertura e mais contexto

A lista de health checks embutidos cresceu: Kyverno, TLSRoute, AWS ACK, CloudNativePG, Prometheus Operator, cert-manager, trust-manager, ACME, Tekton, Velero, Flink, Kro, Medusa, Pulumi, KServe, Envoy Gateway, Airlock microgateway e ListenerSet do Gateway API; e o health check de VictoriaMetrics passou a ignorar o status. Cada health check customizado em `argocd-cm` é código que alguém revisa quando o CRD muda.

Duas mudanças de comportamento merecem atenção. Durante a deleção, o health check padrão agora **lista os finalizers pendentes**, deixando explícito por que um recurso continua em `Progressing`. E health checks embutidos ou customizados podem retornar um `deletionMessage` opcional, substituindo a mensagem padrão de "Pending deletion" — útil para explicar finalizers de vida longa e avisar quando a remoção manual é necessária.

Os eventos de transição de health passaram a identificar os recursos que causaram a mudança, com sufixo `(Caused by ...)` e até três recursos: `Updated health status: Healthy -> Degraded (Caused by apps/Deployment:default/api)`.

## Segurança, autenticação e configuração de cluster

O **rollback ganhou uma permissão de RBAC separada**, permitindo conceder sync sem conceder rollback — uma distinção útil onde reverter é mais arriscado do que aplicar a revisão atual do Git. No `argocd proj list`, `SIGNATURE-KEYS` foi substituída por `SOURCE-INTEGRITY`, e `--signature-keys` emite aviso de depreciação, o que exige ajuste em scripts que fazem parsing dessa saída.

No Dex, versão mínima de TLS, cipher suites e preferências de curva passaram a ser configuráveis, assim como tipo e configuração de storage a partir do `argocd-cm`; o redirecionamento para um conector específico está em Alpha. A tela de login ganhou texto de botão configurável via `ui.loginButtonText`, e a instância pode enviar `X-Robots-Tag` para impedir indexação por buscadores — relevante quando a interface fica exposta em rede interna. Também é possível desabilitar o Swagger UI.

## OpenTelemetry: mudanças que quebram

Esta seção merece destaque porque contém a mudança com maior risco de perda de dados sem erro aparente. A variável do repo-server `ARGOCD_REPO_OTLP_HEADERS` foi renomeada para `ARGOCD_REPO_SERVER_OTLP_HEADERS`. Os manifests padrão já usam o nome novo, mas qualquer manifest customizado que defina a variável antiga continua aplicando sem erro — e sem enviar headers.

As demais mudanças no bloco de OTLP:

- valores de header contendo `=` (credenciais em base64) passaram a ser aceitos;
- com `otlp.insecure: "false"`, o Argo CD também confia na CA do coletor em `argocd-tls-certs-cm` e respeita `OTEL_EXPORTER_OTLP_CERTIFICATE`, `OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE`, `OTEL_EXPORTER_OTLP_CLIENT_KEY` (mTLS) e `OTEL_EXPORTER_OTLP_HEADERS`;
- `otlp.insecure` agora decide integralmente entre TLS e texto puro;
- o sampler passou a ser parent-based e configurável via `--otlp-sample-ratio` ou `ARGOCD_<COMPONENT>_OTLP_SAMPLE_RATIO` (padrão 1.0), com a decisão propagada entre serviços e decisões "not sampled" recebidas em `traceparent` respeitadas;
- a instrumentação foi atualizada para otelgrpc/otelhttp v0.70.0 (convenções semânticas 1.42.0/1.43.0), e `server.address`/`server.port` agora vêm do alvo de dial do gRPC.

Esse último item costuma quebrar na prática: dashboards e alertas que agrupam por essas labels podem ver valores diferentes depois do upgrade.

## Ajustes menores que afetam automações

- **Helm:** em `argocd app diff --local --server-side-generate`, o `--local-include` padrão passou a incluir `*.tpl` e `Chart.lock` além de YAML e JSON. Passar a flag explicitamente ainda substitui o conjunto padrão inteiro.
- **Webhooks:** suporte a Harbor e DockerHub, e à annotation `manifest-generate-paths` no BitBucket Server.
- **Cluster:** novo campo efêmero `configHash` detecta mudanças de configuração; não é gravado no secret do cluster, é calculado na consulta e o valor é opaco.
- **Conectividade e CLI:** timeout server-side enviado por transport wrapper, `HTTP_PROXY`/`HTTPS_PROXY`/`NO_PROXY` respeitados em gRPC-web, e `argocd login` persistindo e reutilizando certificados de cliente.

## Como atualizar

A atualização segue o procedimento padrão de manifests, com a versão já corrigida:

```bash
kubectl apply -n argocd --server-side --force-conflicts \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/v3.6.1/manifests/install.yaml
```

Para alta disponibilidade, use `manifests/ha/install.yaml` no mesmo caminho de versão. Antes de aplicar: confirme se algum manifest customizado ainda define `ARGOCD_REPO_OTLP_HEADERS`; revise dashboards que dependem de `server.address`/`server.port`; identifique as Applications com `ServerSideApply=true` para estimar o impacto no apiserver; e verifique se scripts de CI dependem da lista padrão de `--local-include`.

## Conclusão

A 3.6 é uma release de consolidação com uma mudança estrutural no meio. Ao substituir o Structured-Merge Diff por um dry-run real contra o kube-apiserver, o Argo CD ganha precisão naquilo que ele mais faz — dizer se o cluster corresponde ao Git — ao custo de depender mais da API do cluster. O cache e a válvula de escape indicam que o risco foi tratado com cuidado.

Para frotas grandes, os ganhos de performance e o progressive sync mais rigoroso pesam mais do que qualquer item isolado de interface. Para quem está no 3.3, o argumento é outro: a linha saiu de suporte.

---

## Links e Referências

- [Anúncio do Argo CD v3.6 no X](https://x.com/argoproj/status/2117890245639250274)
- [Post oficial: Argo CD v3.6 RC1](https://blog.argoproj.io/argo-cd-v3-6-rc1-is-here-c0b562dc78d1)
- [Release v3.6.0 no GitHub](https://github.com/argoproj/argo-cd/releases/tag/v3.6.0)
- [Release v3.6.1 no GitHub](https://github.com/argoproj/argo-cd/releases/tag/v3.6.1)
- [Guia de upgrade 3.5 → 3.6](https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/3.5-3.6/)
- [Documentação do Argo CD](https://argo-cd.readthedocs.io/)
- [Argo CD 3.5 e a interface de ApplicationSet](/pt-br/blog/argocd-appset-ui/)

---

Na **EF-TECH**, ajudamos empresas a implementar e operar workflows GitOps com Argo CD em escala, do desenho de repositórios e políticas de sync à operação de frotas multi-cluster. [Entre em contato](/pt-br/contato/) para saber como podemos ajudar sua equipe. Para mais artigos como este, visite nosso [blog](/pt-br/blog/).
