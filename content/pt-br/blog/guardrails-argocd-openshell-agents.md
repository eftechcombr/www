---
title: "Guardrails fora da caixa: OctoDoctor audita seu Argo CD e OpenShell isola seus agentes"
description: "O OctoDoctor é um binário open source e read-only que varre manifests ou clusters do Argo CD e transforma 26 antipadrões em relatório HTML, JSON e YAML — com direito a skill para agentes e gate de CI. Na mesma semana, a CNCF anunciou o OpenShell no Sandbox, com sandbox por agente, política por requisição e credenciais que nunca chegam ao modelo."
summary: "Duas ferramentas lançadas na semana do KubeCon NA 2026 atacam o mesmo problema por lados opostos: o OctoDoctor coloca a revisão de configuração do Argo CD fora do cluster, como um scanner read-only que falha o pipeline; o OpenShell coloca o controle do agente fora do sandbox, num supervisor que decide o que cada binário pode fazer. Nos dois casos, o guardrail mora fora daquilo que ele governa."
date: 2026-11-11
draft: false
tags: ["argocd", "gitops", "kubernetes", "ai-agents", "security", "cncf", "open-source"]
categories: ["infraestrutura"]
featureimage: "/img/blog/guardrails-argocd-openshell-agents/cover.png"
featureimagecaption: "À esquerda, o OctoDoctor lendo a configuração do Argo CD; à direita, o OpenShell mantendo o agente e a chave atrás de um supervisor."
---

Duas notícias caíram no mesmo dia na minha lista e, à primeira vista, não têm nada a ver. A primeira: o Octopus Deploy lançou o **OctoDoctor**, um utilitário gratuito e open source que varre a configuração do seu Argo CD e devolve um relatório do que está errado. A segunda: o **OpenShell**, runtime seguro para agentes de IA iniciado pela NVIDIA, entrou no CNCF Sandbox — e foi um dos destaques do anúncio da fundação no KubeCon NA 2026.

Uma é sobre YAML de GitOps. A outra é sobre agentes que executam shell e seguram credenciais de verdade. O elo entre elas é o desenho: **nos dois casos, o mecanismo de controle fica fora da coisa controlada**. O OctoDoctor lê seus manifests e nunca escreve neles. O OpenShell mantém o supervisor fora do sandbox e a chave de API fora do alcance do agente.

É a diferença entre documentar uma boa prática e fazer o pipeline parar quando ela é violada.

![OctoDoctor auditando um cluster Argo CD e OpenShell isolando um agente atrás de um supervisor](/img/blog/guardrails-argocd-openshell-agents/cover.png)

## OctoDoctor: o guia de antipadrões virou executável

Se você já leu [Top 30 Argo CD anti-patterns](https://octopus.com/blog/30-argo-cd-antipatterns-for-gitops), conhece o problema: as regras são boas, mas ninguém as aplica. O OctoDoctor é a tentativa de fechar essa lacuna — ele empacota as boas práticas que a Octopus vinha publicando em guias e as transforma em verificações executáveis.

O escopo é honestamente restrito. Ele não olha o seu código de aplicação, não avalia imagens e não substitui um policy engine. Ele lê **Applications, ApplicationSets, AppProjects**, os ConfigMaps e Secrets do Argo CD e os Secrets de cluster — e ignora todo o resto. Você pode apontar o binário para um repositório que também tem outros manifests Kubernetes sem medo.

E ele é **read-only**. Nos dois modos de execução, só lê. Pode rodar contra produção sem cerimônia.

A Octopus afirma que a ferramenta foi testada em instalações grandes — mais de 100 clusters e 20.000 Applications — e que o time de suporte a usa como instrumento de descoberta: em vez de pedir que o cliente descreva a instalação do Argo CD, pede o relatório.

### Dois modos, o mesmo resultado

O OctoDoctor é um binário único, sem dependências de runtime. Instalação é baixar da página de releases, extrair e colocar no `PATH`:

```bash
tar -xzf octodoctor_<version>_linux_amd64.tar.gz
chmod +x octodoctor
./octodoctor --version
```

A partir daí, existem duas formas de análise:

```bash
# 1. Manifests em disco (um checkout do repositório GitOps)
./octodoctor --directory /path/to/argocd/manifests

# 2. Cluster vivo: exporta e analisa em um passo
./octodoctor --export --context production --namespace argocd
```

As opções relevantes:

| Flag | Padrão | O que faz |
| --- | --- | --- |
| `-d, --directory` | diretório atual | Varre um diretório em busca de `.yaml`/`.yml` |
| `-e, --export` | desligado | Exporta os manifests de um cluster vivo e analisa |
| `-c, --context` | contexto atual do kubeconfig | Contexto usado no export |
| `-n, --namespace` | `argocd` | Namespace do Argo CD no export |
| `-l, --limit` | 5 | Quantos arquivos listar por regra no HTML |
| `--fail-on` | `medium` | Menor severidade que faz o processo sair com código 1: `high`, `medium` ou `none` |

`--export` e `--directory` são mutuamente exclusivos. Sem nenhum dos dois, ele analisa o diretório atual. Sem `--export`, as flags de contexto e namespace são ignoradas — e o log avisa isso, o que é um detalhe pequeno que evita muita confusão.

O relatório sai em `octodoctor-output/`, dentro do diretório varrido:

```text
/path/to/argocd/manifests/
└── octodoctor-output/
    ├── index.html     # abra no navegador
    ├── report.json
    └── report.yaml
```

O HTML lista no máximo `--limit` arquivos por regra, para não virar uma parede. Os arquivos JSON e YAML contêm **todos** os arquivos, e são a escolha certa para scripts.

### O ponto que importa: código de saída

A parte mais útil do desenho é o contrato de saída. O OctoDoctor retorna `1` quando pelo menos uma regra falha e `0` caso contrário. Isso o transforma em gate de pipeline sem nenhum wrapper:

```bash
# Primeira adoção: só observa, sempre sai com 0
./octodoctor -d ./gitops --fail-on none

# Depois: bloqueia apenas falhas de severidade alta
./octodoctor -d ./gitops --fail-on high
```

A progressão `none` → `high` → `medium` é o jeito certo de introduzir uma ferramenta dessas num repositório que já tem dívida. Você começa medindo, não bloqueando.

### Regras que valem a leitura

A lista completa tem 26 regras implementadas, com severidade e documentação por regra. Algumas que explicam bem o tipo de problema:

| Regra | O que detecta | Severidade |
| --- | --- | --- |
| R01 | Application com `prune=true` **e** `allowEmpty=true` no sync policy | Alta |
| R05 | AppProject com `sourceRepos: "*"` | Alta |
| R11 | Usuário anônimo habilitado no Argo CD | Alta |
| R17 | Parameter overrides em Application | Alta |
| R30 | Image Updater sem write-back para o Git | Alta |
| R19 | Hash de commit ou nome de branch em `targetRevision` (qualquer coisa além de `HEAD`) | Média |
| R02 | Application sem sync policy automatizada | Média |
| R15/R16 | Values de Helm ou `kustomize` hardcoded | Média |

R01 é o clássico que apaga recursos sem querer quando o render de um Application vem vazio. R05 e R11 são portas abertas. R19 é o que quebra reprodutibilidade: um `targetRevision` apontando para branch significa que "o mesmo commit" pode produzir resultados diferentes amanhã.

Nada disso substitui entender o próprio ambiente. A própria Octopus admite que não dá para prever toda configuração existente — se uma regra falha e você sabe exatamente por quê, isso é esperado. O relatório é o começo de uma conversa, não um veredito.

### A skill para agentes

Junto com o binário, o projeto publica uma skill chamada `octodoctor-report`. Ela usa o `octodoctor` do `PATH` se ele existir; se não, baixa a release mais recente para um diretório temporário e verifica o checksum. Só precisa de `curl` e `tar`.

```bash
# Com o skills CLI
npx skills add OctopusDeploy/octodoctor-argocd --skill octodoctor-report

# Ou com o GitHub CLI (gh skill está em preview)
gh skill install OctopusDeploy/octodoctor-argocd octodoctor-report --agent claude-code
```

Depois disso, a interação é em linguagem natural: *"verifique os manifests do Argo CD em ./gitops contra as boas práticas"* ou *"audite a instalação do Argo CD no meu cluster de produção"*. O agente escolhe o modo, roda a ferramenta e responde com o número de regras que falharam, a lista ordenada por severidade e o caminho do `index.html`.

Dois detalhes de implementação que merecem elogio. Primeiro: a skill trata o exit code `1` como **resultado normal**, não como erro — é exatamente o comportamento correto, e é onde muita integração de agente com ferramenta de lint erra. Segundo: o agente só edita manifests para corrigir as falhas **se você pedir**.

Se você opera Argo CD, vale comparar esse tipo de verificação estática com as mudanças recentes do próprio Argo CD. No [Argo CD 3.6](/pt-br/blog/argocd-3-6/), o Server-Side Diff passou a fazer dry-run real contra o kube-apiserver para decidir se algo está `Synced` — mais precisão no runtime. O OctoDoctor ataca a camada de cima: a configuração que gerou aquele estado. E se você usa ApplicationSets em escala, a [interface dedicada do Argo CD 3.5](/pt-br/blog/argocd-appset-ui/) ajuda a enxergar o que a ferramenta vai reportar.

## OpenShell: o guardrail do lado de fora do sandbox

A segunda notícia é de outra categoria de risco. Um agente de IA não só chama APIs: ele roda shell, instala pacotes, lê arquivos e abre conexões de rede. Muitas vezes agindo sobre texto que ele leu na internet um minuto antes. Como resume o [guia da CNCF para engenheiros de plataforma](https://www.cncf.io/blog/2026/11/11/openshell-on-kubernetes-a-guide-for-platform-engineers/): **todo agente é código não confiável que carrega credenciais reais**.

O [OpenShell](https://github.com/NVIDIA/OpenShell) parte de uma premissa simples: se o controle mora no prompt, o controle não existe. Ele roda cada agente num sandbox e coloca um **supervisor confiável fora do sandbox** para decidir o que o agente pode alcançar. A política é declarada em YAML, em quatro dimensões:

| Controle | Mecanismo | Efeito prático |
| --- | --- | --- |
| **Filesystem** | Landlock | Limita paths de leitura e escrita. No demo, `/usr` e `/etc` são read-only; só `/sandbox`, `/tmp` e `/dev/null` são graváveis |
| **Process** | UID/GID não-root, zero capabilities, seccomp | O agente não nasce privilegiado — e não consegue escalar |
| **Network** | Egress negado por padrão | Regras por binário, host, porta e **método HTTP** |
| **Credentials** | Placeholder + swap no supervisor | O agente nunca vê a chave real; o supervisor injeta só nos endpoints permitidos |

A linha de rede é o argumento mais forte. Uma `NetworkPolicy` do Kubernetes consegue dizer "este Pod pode alcançar `api.github.com` na 443". Ela **não** consegue dizer "o `curl` pode ler issues, mas não pode criar issues". O OpenShell consegue — e consegue mudar essa regra num sandbox em execução, sem restart.

### Como o sandbox nasce no Kubernetes

O OpenShell não traz scheduler próprio. O backend Kubernetes usa o [Agent Sandbox](https://agent-sandbox.sigs.k8s.io/), o recurso `Sandbox` de `agents.x-k8s.io` mantido pelo SIG Apps. Na prática, agentes aparecem como Pods, Services, PVCs, Secrets e NetworkPolicies — objetos que você já sabe operar.

O caminho de controle, em resumo:

1. **Preparação.** CNI que aplique NetworkPolicy de ingress e egress, controller e CRDs do Agent Sandbox, e o chart Helm do gateway do OpenShell.
2. **Criação.** `openshell sandbox create` fala com o gateway por mTLS. Clientes nunca falam direto com a API do Kubernetes.
3. **Registro.** O gateway autentica quem chamou, resolve imagem, política, providers e recursos, e grava o registro do sandbox na fase `Provisioning`. Esse registro — não o Pod — é a fonte de verdade.
4. **Rede primeiro.** O driver cria duas NetworkPolicies no namespace: workload sem nenhum egress e ingress só dos supervisors na 5500; e o lado dos supervisors. Só depois o recurso `Sandbox` é criado, já suspenso.
5. **Workload.** O Agent Sandbox cria o Pod e um PVC para `/sandbox`, com um scheduling gate segurando o Pod.
6. **Verificação.** O driver relê o Pod admitido e confere UID/GID não-root, nenhuma capability adicionada, seccomp `RuntimeDefault`, ausência de host namespaces, ausência de token de ServiceAccount e os labels e volumes esperados. Se um webhook de admissão mudou algo, a criação falha.
7. **Supervisor.** Um Pod supervisor, um Service na frente da porta 5500 do workload, Secrets de TLS e bootstrap, e um token de vida curta. O workload nunca recebe credenciais do gateway.
8. **Conexão.** O supervisor autentica com identidade amarrada a namespace, UID do Sandbox, UID do próprio Pod e geração do runtime. Só então os gates de scheduling são liberados. Dentro do workload, os controles de filesystem, processo, socket e DNS são aplicados **antes** do comando do agente começar.

Na prática, o comando de criação fica assim:

```bash
openshell sandbox create \
  --workspace demo \
  --name policy-demo \
  --from nicolaka/netshoot@sha256:<digest> \
  --no-auto-providers
```

Repare no `@sha256:`. Imagem por tag é uma dependência móvel; por digest, não.

### Política em tempo de execução, sem restart

Cada requisição de saída do agente passa pelo supervisor, que confere destino, porta, binário que chamou e a requisição HTTP antes de abrir a conexão. É por isso que o caso do demo funciona: o `curl` começa bloqueado, recebe uma política que permite `GET` em `api.github.com`, e continua recebendo `policy_denied` num `POST /issues`.

```bash
openshell policy update <arquivo-de-politica>   # carrega nova versão e espera o sandbox confirmar
openshell logs policy-demo --source sandbox   # mostra cada requisição permitida e negada
```

O log por sandbox, com fonte `sandbox`, é o que transforma política em auditoria. Sem isso você tem bloqueio; com isso, você tem evidência.

### Limites que a documentação admite

Dois pontos merecem atenção antes de colocar isso em produção:

- **Sem CRD ainda.** Sandboxes só podem ser criados pela API do gateway, não pela API do Kubernetes. Existe uma issue aberta para um `OpenShellSandbox` CRD e um operator ([openshell#1719](https://github.com/NVIDIA/OpenShell/issues/1719)).
- **Um supervisor por agente** dá isolamento forte, mas pode não escalar bem em ambientes grandes. O roadmap discute opções flexíveis de deployment ([RFC 0018](https://github.com/NVIDIA/OpenShell/pull/4377)).

### OpenShell e Agent Substrate: dois problemas diferentes

O OpenShell e o [Agent Substrate](https://github.com/agent-substrate/substrate) (Google) entraram no CNCF Sandbox em setembro de 2026, com dois dias de diferença, e é fácil tratá-los como concorrentes. Eles respondem a perguntas distintas:

| | OpenShell | Agent Substrate |
| --- | --- | --- |
| Origem | NVIDIA | Google |
| Pergunta principal | **O que este agente pode fazer?** | **Como rodar milhares de agentes ociosos barato?** |
| Unidade de trabalho | Um sandbox por agente: Sandbox, Pod de workload e Pod supervisor | Um ator: identidade + snapshot, rodando em worker Pods compartilhados |
| Base Kubernetes | Agent Sandbox (`agents.x-k8s.io`) | CRD própria `WorkerPool` (`ate.dev`) |
| Isolamento | Container padrão + Landlock + seccomp (RuntimeClass mais forte é opcional) | gVisor ou Cloud Hypervisor obrigatório por ator |
| Estado | PVC `/sandbox` que sobrevive a stop/start | Snapshots de RAM e filesystem em object storage |
| Escala | HPA no gateway (mais de uma réplica exige PostgreSQL externo) | HPA no `WorkerPool`, que tem subrecurso `/scale` |
| Maturidade | v0.1.x | Pré-1.0 |

A regra de bolso: **agentes ociosos e intermitentes, um por usuário, com custo por agente como métrica principal → Substrate. Agentes com credenciais reais alcançando sistemas de produção, com necessidade de controle por requisição → OpenShell.** Empresas grandes provavelmente vão querer os dois, e há trabalho em andamento para o OpenShell aceitar backends de isolamento plugáveis — incluindo um backend Substrate.

### Kyverno por cima: admissão

O OpenShell checa as configurações de Pod das quais ele depende para continuar seguro. O resto fica com o time de plataforma — e é aí que entra admission control. O demo da Nirmata mostra sete políticas Kyverno em modo `Enforce`, escritas em CEL:

| Controle | Tentativa | Resultado |
| --- | --- | --- |
| Pod security | Container com `privileged: true` | Negado: non-root, drop de capabilities e `allowPrivilegeEscalation: false` são obrigatórios |
| RBAC | Role `openshell-*` com `*` em `*` | Negado: regras de RBAC do OpenShell não podem ter wildcards |
| Network | Patch que libera todo egress na NetworkPolicy de workloads | Negado: workloads não podem ter egress direto |
| Supply chain | Imagem `nicolaka/netshoot:v0.13` (tag) | Negado: imagens de sandbox exigem digest `sha256` |
| Resources | Sandbox sem resources / pedindo 8 CPU e 16Gi | Recebe defaults (`100m` de CPU) / negado acima de 4 CPU, 8Gi e 20Gi efêmeros |
| Credentials | `envFrom` com Secret do Kubernetes | Negado: use providers do OpenShell em vez de injetar Secrets |

O detalhe importante: as políticas olham a **requisição**, não o remetente. Nem um gateway comprometido consegue empurrar um sandbox privilegiado, sem digest ou acima do limite. Mas o ServiceAccount do gateway ainda pode criar Pods e NetworkPolicies direto no namespace — em produção, estenda as políticas para Pods e para qualquer NetworkPolicy que selecione workloads do OpenShell.

E existe o furo que admission control não cobre por definição: um Deployment do seu time chamando `api.openai.com` nunca passa pelo gateway nem por um supervisor. Para esse caso, monitores de kernel como o [Runtime for Kyverno](https://github.com/nirmata/runtime) rodam como DaemonSet, anexam programas eBPF e reportam `exec`, abertura de arquivos, rede e DNS como `OpenReports`.

## O padrão comum

Voltando às duas notícias. O OctoDoctor pega um documento — as boas práticas do Argo CD — e o transforma em verificação que quebra o build. O OpenShell pega uma instrução de prompt — "não acesse isso" — e a transforma em política aplicada por um processo fora do alcance do modelo.

Nos dois casos, o guardrail é **externo, declarativo e auditável**. Nos dois casos, existe um código de saída ou um evento de admissão que diz "não". E nos dois casos a ferramenta deixa explícito o que não decide: o OctoDoctor não sabe se a violação foi intencional, e o OpenShell deixa para o time de plataforma quais imagens rodam, qual o tamanho máximo de um sandbox, quais credenciais cada agente recebe e quem pode mexer no RBAC dele.

Isso é o que separa uma boa prática de um controle. Boa prática é o que está escrito. Controle é o que acontece quando alguém tenta ir contra.

## Como começar

Para o Argo CD, o caminho mais curto é rodar sem bloquear:

```bash
./octodoctor -d ./gitops --fail-on none
# abra ./gitops/octodoctor-output/index.html
```

Leia o relatório com o time, escolha as duas ou três regras que doem mais, corrija, e só então suba para `--fail-on high`.

Para o OpenShell, o demo da Nirmata sobe tudo num cluster kind de dois nós (Kubernetes 1.35, Cilium 1.20, Agent Sandbox v1.0.5, OpenShell 0.1.3, Kyverno 1.18.2):

```bash
git clone https://github.com/nirmata/demo-openshell
cd demo-openshell
./scripts/setup.sh && ./scripts/install-cli.sh && ./scripts/verify.sh
./scripts/demo.sh           # política L7 do OpenShell
./scripts/kyverno-demo.sh   # políticas de admissão Kyverno
./scripts/cleanup.sh
```

Precisa de Docker, kind, kubectl, Helm, curl, SSH e nc. É a forma mais barata que conheço de ver `policy_denied` acontecendo de verdade antes de discutir isso com o time de segurança.

Na EF-TECH, operamos clusters Kubernetes com Argo CD e ajudamos times a colocar guardrails em pipelines GitOps e em cargas de IA sem travar a entrega. [Entre em contato](/pt-br/contato/) se quiser revisar a configuração do seu Argo CD ou desenhar o isolamento dos seus agentes. Para mais artigos como este, visite nosso [blog](/pt-br/blog/).

## Links e Referências

- **OctoDoctor: check your Argo CD cluster for best practices** — [octopus.com/blog/octodoctor-for-argocd](https://octopus.com/blog/octodoctor-for-argocd)
- **Documentação do OctoDoctor** — [octodoctor-argocd.readthedocs.io](https://octodoctor-argocd.readthedocs.io/)
- **Repositório do OctoDoctor** — [github.com/OctopusDeploy/octodoctor-argocd](https://github.com/OctopusDeploy/octodoctor-argocd)
- **Releases do OctoDoctor (binários e checksums)** — [github.com/OctopusDeploy/octodoctor-argocd/releases](https://github.com/OctopusDeploy/octodoctor-argocd/releases)
- **Top 30 Argo CD anti-patterns** — [octopus.com/blog/30-argo-cd-antipatterns-for-gitops](https://octopus.com/blog/30-argo-cd-antipatterns-for-gitops)
- **Anúncio da CNCF no KubeCon NA 2026 (OpenShell e Agent Substrate no Sandbox)** — [cncf.io/announcements/2026/11/10/...](https://www.cncf.io/announcements/2026/11/10/cncf-hits-major-milestones-with-global-community-growth-record-industry-investment-and-a-new-generation-of-projects-to-build-ai-systems-in-production/)
- **Página do projeto OpenShell na CNCF** — [cncf.io/projects/openshell](https://www.cncf.io/projects/openshell/)
- **OpenShell no GitHub** — [github.com/NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell)
- **Documentação do OpenShell (arquitetura e setup no Kubernetes)** — [docs.nvidia.com/openshell/latest](https://docs.nvidia.com/openshell/latest/)
- **OpenShell on Kubernetes: a guide for platform engineers** — [cncf.io/blog/2026/11/11/openshell-on-kubernetes-a-guide-for-platform-engineers](https://www.cncf.io/blog/2026/11/11/openshell-on-kubernetes-a-guide-for-platform-engineers/)
- **Agent Sandbox (SIG Apps)** — [agent-sandbox.sigs.k8s.io](https://agent-sandbox.sigs.k8s.io/)
- **Agent Substrate** — [github.com/agent-substrate/substrate](https://github.com/agent-substrate/substrate)
- **Demo do OpenShell no Kubernetes (Nirmata)** — [github.com/nirmata/demo-openshell](https://github.com/nirmata/demo-openshell)
- **Runtime for Kyverno (monitoramento eBPF)** — [github.com/nirmata/runtime](https://github.com/nirmata/runtime)
- **KubeCon + CloudNativeCon North America 2026** — [events.linuxfoundation.org/kubecon-cloudnativecon-north-america](https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/)

### Origem das notas

Os dois anúncios foram capturados na nota diária de 2026-11-11, a partir de posts no X (Twitter). Links originais e destino resolvido:

- `https://t.co/Exv4ar4B0y` → [octopus.com/blog/octodoctor-for-argocd](https://octopus.com/blog/octodoctor-for-argocd)
- `https://t.co/QaFxfAGfYf` → [anúncio da CNCF](https://www.cncf.io/announcements/2026/11/10/cncf-hits-major-milestones-with-global-community-growth-record-industry-investment-and-a-new-generation-of-projects-to-build-ai-systems-in-production/)
- `https://t.co/vhJfyRjfMX` (imagem do post) → [x.com/CloudNativeFdn/status/2120250399219188199](https://x.com/CloudNativeFdn/status/2120250399219188199)
