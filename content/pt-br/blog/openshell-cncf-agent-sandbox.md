---
title: "OpenShell: o guardrail mora fora do sandbox do agente"
description: "A CNCF aceitou o OpenShell no Sandbox na KubeCon NA 2026: um sandbox por agente, um supervisor confiável fora dele, política por requisição — inclusive por método HTTP — e credenciais que o modelo nunca vê."
summary: "O OpenShell parte da premissa de que controle escrito no prompt não é controle. Ele roda cada agente num sandbox e mantém o supervisor fora, com política em YAML nas dimensões de filesystem, processo, rede e credenciais. Passo pelo caminho de controle de oito etapas no Kubernetes, pelo argumento NetworkPolicy versus L7, pela camada de admissão com Kyverno, pela comparação com o Agent Substrate e pelos limites que a documentação admite."
date: 2026-11-11
draft: false
tags: ["ai-agents", "security", "kubernetes", "cncf", "open-source"]
categories: ["infraestrutura"]
featureimage: "/img/blog/openshell-cncf-agent-sandbox/cover.png"
featureimagecaption: "O agente fica selado dentro do sandbox; o supervisor, as camadas de política e a chave de API ficam do lado de fora do vidro."
---

Um agente de IA não só chama APIs: ele roda shell, instala pacotes, lê arquivos e abre conexões de rede. Muitas vezes agindo sobre texto que ele leu na internet um minuto antes. Como resume o [guia da CNCF para engenheiros de plataforma](https://www.cncf.io/blog/2026/11/11/openshell-on-kubernetes-a-guide-for-platform-engineers/): **todo agente é código não confiável que carrega credenciais reais**.

O **OpenShell**, runtime seguro para agentes de IA iniciado pela NVIDIA, entrou no CNCF Sandbox e foi um dos destaques da fundação no KubeCon NA 2026. Ele parte de uma premissa simples: se o controle mora no prompt, o controle não existe. Roda cada agente num sandbox e coloca um **supervisor confiável fora do sandbox** para decidir o que o agente pode alcançar.

![Um agente robô selado dentro de um sandbox de vidro, com o supervisor e a chave de API fora da redoma](/img/blog/openshell-cncf-agent-sandbox/cover.png)

## Onde mora o controle

A decisão de desenho é arquitetural, não procedimental. Um system prompt que diz "não toque em produção" é uma sugestão que o modelo pode seguir ou ignorar, e é invisível na sua trilha de auditoria. Um supervisor fora do sandbox é um processo que o modelo não alcança, não edita e não consegue convencer.

A política é declarada em YAML, em quatro dimensões:

| Controle | Mecanismo | Efeito prático |
| --- | --- | --- |
| **Filesystem** | Landlock | Limita paths de leitura e escrita. No demo, `/usr` e `/etc` são read-only; só `/sandbox`, `/tmp` e `/dev/null` são graváveis |
| **Process** | UID/GID não-root, zero capabilities, seccomp | O agente não nasce privilegiado — e não consegue escalar |
| **Network** | Egress negado por padrão | Regras por binário, host, porta e **método HTTP** |
| **Credentials** | Placeholder + swap no supervisor | O agente nunca vê a chave real; o supervisor injeta só nos endpoints permitidos |

### Por que uma NetworkPolicy não basta

A linha de rede é o argumento mais forte do desenho inteiro, e o mais fácil de subestimar.

Uma `NetworkPolicy` do Kubernetes consegue dizer "este Pod pode alcançar `api.github.com` na 443". Ela **não** consegue dizer "o `curl` pode ler issues, mas não pode criar issues". As duas requisições têm o mesmo destino, a mesma porta e o mesmo protocolo; elas diferem só dentro da sessão TLS, na camada HTTP.

O OpenShell faz essa distinção — e consegue mudar a regra num sandbox em execução, sem restart. É a diferença entre isolamento de rede e controle de capacidade.

## Como o sandbox nasce no Kubernetes

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

A ordem é a parte interessante. A política de rede existe antes do workload. O workload fica suspenso até a identidade ser verificada. O supervisor é confiável porque provou quem é, não porque mora num namespace privilegiado.

### O comando de criação

Na prática, o comando de criação fica assim:

```bash
openshell sandbox create \
  --workspace demo \
  --name policy-demo \
  --from nicolaka/netshoot@sha256:<digest> \
  --no-auto-providers
```

Repare no `@sha256:`. Imagem por tag é uma dependência móvel; por digest, não. Esse único caractere é a diferença entre "testamos esta imagem" e "testamos uma imagem que tinha esse nome naquele momento".

## Política em tempo de execução, sem restart

Cada requisição de saída do agente passa pelo supervisor, que confere destino, porta, binário que chamou e a requisição HTTP antes de abrir a conexão. É por isso que o caso do demo funciona: o `curl` começa bloqueado, recebe uma política que permite `GET` em `api.github.com`, e continua recebendo `policy_denied` num `POST /issues`.

```bash
openshell policy update <arquivo-de-politica>   # carrega nova versão e espera o sandbox confirmar
openshell logs policy-demo --source sandbox   # mostra cada requisição permitida e negada
```

O log por sandbox, com fonte `sandbox`, é o que transforma política em auditoria. Sem isso você tem bloqueio; com isso, você tem evidência. Quando o time de segurança perguntar o que o agente fez na terça passada, é esse log que responde.

## Limites que a documentação admite

Dois pontos merecem atenção antes de colocar isso em produção:

- **Sem CRD ainda.** Sandboxes só podem ser criados pela API do gateway, não pela API do Kubernetes. Existe uma issue aberta para um `OpenShellSandbox` CRD e um operator ([openshell#1719](https://github.com/NVIDIA/OpenShell/issues/1719)).
- **Um supervisor por agente** dá isolamento forte, mas pode não escalar bem em ambientes grandes. O roadmap discute opções flexíveis de deployment ([RFC 0018](https://github.com/NVIDIA/OpenShell/pull/4377)).

A ausência de CRD é o ponto que muda seu modelo operacional hoje: fluxos de GitOps que esperam um objeto Kubernetes para reconciliar ainda não se aplicam. Você cria sandboxes pelo gateway, e o registro do gateway é a fonte de verdade.

## OpenShell e Agent Substrate: dois problemas diferentes

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

## Kyverno por cima: admissão

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

Essa é a fronteira honesta da arquitetura. O OpenShell governa o que passa por ele. A admissão governa o que pode ser criado. A telemetria de kernel é o que sobra para tudo que nunca pede permissão.

## Como começar

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

O objetivo não é tornar o agente inofensivo. É tornar as permissões dele explícitas, pequenas e revogáveis — e manter a decisão fora do alcance daquilo sobre o que se decide.

Na EF-TECH, operamos clusters Kubernetes e ajudamos times a desenhar isolamento para cargas de IA sem travar a entrega. [Entre em contato](/pt-br/contato/) se quiser desenhar os guardrails dos seus agentes. Para mais artigos como este, visite nosso [blog](/pt-br/blog/).

## Links e Referências

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

O anúncio foi capturado na nota diária de 2026-11-11, a partir de posts no X (Twitter). Links originais e destinos resolvidos:

- `https://t.co/QaFxfAGfYf` → [anúncio da CNCF](https://www.cncf.io/announcements/2026/11/10/cncf-hits-major-milestones-with-global-community-growth-record-industry-investment-and-a-new-generation-of-projects-to-build-ai-systems-in-production/)
- `https://t.co/vhJfyRjfMX` (imagem do post) → [x.com/CloudNativeFdn/status/2120250399219188199](https://x.com/CloudNativeFdn/status/2120250399219188199)
