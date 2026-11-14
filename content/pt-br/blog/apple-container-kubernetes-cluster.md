---
title: "Apple container 1.7.1: clusters Kubernetes locais em VMs leves no macOS"
description: "A CLI container 1.7.1 da Apple traz o container cluster: clusters Kubernetes em VMs leves no macOS com registro automático no kubeconfig, pools heterogêneos de workers, --shared-image-store (com alertas de segurança) e suporte a CNI customizada."
summary: "Com a release 1.7.1, a CLI nativa container da Apple ganha gerenciamento completo de clusters Kubernetes locais via container cluster. Passo pelo quickstart, clusters nomeados por branch, topologias com múltiplos workers heterogêneos, isolamento do ciclo de vida dos nós, compartilhamento de imagens locais com --shared-image-store (incluindo os riscos com root e pull secrets), CNI customizada com Cilium e as demais novidades da 1.7.1."
date: 2026-11-13
draft: false
tags: ["kubernetes", "macos", "containers", "desenvolvimento-local", "cilium"]
categories: ["infraestrutura"]
---

Em 6 de novembro de 2026, a Apple publicou a versão [`1.7.1` da CLI `container`](https://github.com/apple/container/releases/tag/1.7.1), trazendo suporte nativo a clusters Kubernetes locais por meio do subcomando `container cluster` diretamente no runtime de containers da Apple para macOS. Em vez de manter o Docker Desktop ou outro gerenciador de VMs Linux só para validar manifestos, você sobe clusters Kubernetes baseados em VMs leves pela mesma CLI usada para construir e rodar containers — com registro automático no `~/.kube/config` para que `kubectl` e o restante do ecossistema funcionem de imediato.

## Por que rodar Kubernetes no Apple `container`

Rodar Kubernetes localmente no macOS costuma exigir concessões entre tempo de startup, isolamento ou compatibilidade com ferramentas padrão. O `container cluster` acerta um ponto de equilíbrio prático:

- **VMs leves por nó.** Os clusters rodam como máquinas virtuais leves no macOS, em vez de containers aninhados dentro de uma única VM Linux compartilhada.
- **Sem configuração manual de kubeconfig.** Ao criar o cluster, o contexto é gravado automaticamente no `~/.kube/config`, então `kubectl`, `helm` e ferramentas de GitOps funcionam sem variáveis extras.
- **Clusters concorrentes e isolados.** Dá para subir vários clusters nomeados lado a lado — um por branch de feature ou por versão de Kubernetes — sem conflito de porta ou estado.
- **Compartilhamento direto de imagens locais (opt-in).** Imagens geradas com `container build` podem ser usadas pelo cluster sem subir para um registry remoto.

## Quickstart

Criar, inspecionar, usar e remover um cluster padrão leva cinco comandos:

```sh
# Cria um cluster (nome padrão: "cluster-dev")
container cluster create

# Lista os clusters em execução
container cluster list

# Valida o acesso com kubectl
kubectl cluster-info
kubectl get nodes

# Remove quando terminar
container cluster delete
```

Na versão `1.7.1`, `container cluster list` (ou `container cluster ls`) exibe uma linha por cluster por padrão. Passe `--nodes` quando quiser visualizar uma linha por nó. Clusters criados com versões anteriores à `1.7.1` não aparecem na listagem.

## Clusters nomeados e ambientes simultâneos

Se você omitir `--name`, o cluster nasce como `cluster-dev`. Informar `--name` permite manter múltiplos ambientes isolados rodando ao mesmo tempo no mesmo Mac:

```sh
container cluster create --name feature-auth
container cluster create --name feature-payments

kubectl --context feature-auth get pods
kubectl config use-context feature-payments
```

Para execuções rápidas e descartáveis, a flag `--rm` remove os containers dos nós automaticamente quando eles param. Vale um detalhe: a configuração armazenada do cluster permanece, então ele continua listado como `stopped` no `container cluster list` até você rodar `container cluster delete --name <nome>` ou criar outro cluster com o mesmo nome. Da mesma forma, se o nó de control plane parar inesperadamente (por exemplo, após um `container system stop`), o caminho de recuperação é deletar e recriar o cluster.

## Dimensionamento e topologias multi-nó

Por padrão, o cluster aloca **1/4 das CPUs do host (mínimo 2)** e **1/4 da memória do host (mínimo 2 GB)** em um único nó que acumula control plane e worker.

Você pode ajustar CPU e memória do control plane (ou do nó único) na criação:

```sh
container cluster create --name high-resource --cpus 4 --memory 8g
```

Para testar agendamento real em múltiplos nós, use `--workers`:

```sh
# Control plane mais 3 worker nodes dedicados
container cluster create --name my-cluster --workers 3
```

Quando `--workers` é maior que `0`, o `container cluster` **aplica taint automaticamente no control plane** para que os pods sejam agendados apenas nos workers (`<nome-do-cluster>-worker-<n>`), reproduzindo o comportamento típico de produção. Os workers herdam a mesma `--node-image` do control plane.

Novidade da `1.7.1`, agora também é possível dimensionar os workers explicitamente — e até combinar grupos heterogêneos repetindo `--workers`:

```sh
# Control plane: 2 CPUs / 4 GB
# 2 workers maiores: 4 CPUs / 8 GB cada
# 1 worker menor: 2 CPUs / 4 GB
container cluster create --name my-cluster --cpus 2 --memory 4g \
  --workers count=2,cpus=4,memory=8g \
  --workers count=1,cpus=2,memory=4g
```

Dentro de cada grupo, `count` assume `1` por padrão, e os campos omitidos de `cpus` ou `memory` voltam aos valores padrão de nó único (1/4 dos recursos do host, mínimo 2 CPUs e 2 GB).

## Isolamento do ciclo de vida dos nós na 1.7.1

Como cada nó do cluster roda como um container, fluxos anteriores corriam o risco de quebrar um cluster inteiro caso alguém parasse ou apagasse um nó por engano com comandos comuns do `container`. A release `1.7.1` separa claramente os papéis:

- `container list` oculta nós de cluster, mesmo com `--all`. Use `container cluster list --nodes` para vê-los.
- Comandos de ciclo de vida de alto nível — `container start`, `container stop`, `container kill` e `container delete` — rejeitam nomes de nós de cluster como não encontrados (enquanto continuam processando outros containers comuns passados no mesmo comando).
- Comandos de inspeção e diagnóstico (`container inspect`, `container logs`, `container exec`, `container stats` e `container clean`) continuam funcionando normalmente quando você aponta para o nome de um nó.

Para encerrar nós de cluster do jeito certo, use sempre `container cluster delete --name <cluster>`.

## Compartilhando imagens locais (`--shared-image-store`)

A versão `1.7.1` substitui o antigo subcomando `load-image` pela flag `--shared-image-store` na criação do cluster:

```sh
container cluster create --name test --shared-image-store
container build -t my-app:dev .
kubectl --context test run my-app --image=my-app:dev --image-pull-policy=Never
```

Com a opção habilitada, os nós copiam o conteúdo da imagem compatível com sua plataforma diretamente do seu image store local do `container` no primeiro uso — sem precisar subir um registry local nem rodar `push`. Nomes sem registry (como `my-app:dev`) são resolvidos usando o `registry.domain` padrão e aparecem dentro do Kubernetes sob o prefixo `docker.io` (por exemplo, `docker.io/library/my-app:dev`).

Três detalhes operacionais importantes:

1. **Todas as políticas de pull funcionam**, inclusive `imagePullPolicy: Never`.
2. **Rebuilds na mesma tag exigem atenção.** Se você reconstruir `my-app:dev` mantendo a tag, `IfNotPresent` reutiliza a cópia já cacheada no nó. Use uma tag nova a cada build ou defina `imagePullPolicy: Always`.
3. **A configuração é imutável por cluster.** O compartilhamento é definido em `container cluster create`; para ligar ou desligar depois, é preciso deletar e recriar o cluster.

### Aviso de segurança: por que o compartilhamento vem desligado por padrão

A [documentação oficial de clusters](https://github.com/apple/container/blob/1.7.1/docs/cluster.md) destaca dois impactos de segurança relevantes ao ativar `--shared-image-store`:

- **Qualquer workload com root em um nó pode ler todo o seu image store local.** Pods privilegiados ou com montagem `hostPath` conseguem acessar todas as imagens armazenadas localmente no Mac via `container`, incluindo imagens privadas baixadas com suas credenciais de registry.
- **Imagens locais têm prioridade sobre registries e ignoram pull secrets.** Se existir uma imagem local com o mesmo nome pedido pelo pod, o nó a utiliza *antes* de consultar qualquer registry remoto, para qualquer `imagePullPolicy`, e sem validar `imagePullSecrets`. (Os nós, ao menos, não conseguem adicionar, alterar nem remover imagens do seu store local.)

Mantenha `--shared-image-store` desligado quando não precisar de imagens exclusivamente locais naquele cluster, e evite rodar manifestos não confiáveis ou charts de terceiros com pods privilegiados em clusters com o store compartilhado.

## Versões de Kubernetes e CNI customizada (exemplo com Cilium)

Por padrão, os clusters sobem com a imagem `kindest/node:v1.35.5` e a CNI `kindnet`. Para testar outra versão do Kubernetes, basta trocar `--node-image`:

```sh
container cluster create --node-image docker.io/kindest/node:v1.34.11
```

Se você precisa de NetworkPolicies, observabilidade com eBPF ou paridade de CNI com produção, passe um manifesto YAML plano via `--cni`:

```sh
container cluster create --name my-cluster --cni ./my-cni.yaml
```

O `--cni` espera um manifesto YAML pronto para `kubectl apply -f`, e não um chart Helm diretamente. Para usar o Cilium `1.20.1`, renderize o manifesto primeiro com `helm template`:

```sh
helm repo add cilium https://helm.cilium.io/
helm repo update
helm template cilium cilium/cilium \
  --version 1.20.1 \
  --namespace kube-system \
  --set ipam.mode=kubernetes > cilium.yaml

container cluster create --name cilium-demo --cni ./cilium.yaml
```

O parâmetro `ipam.mode=kubernetes` é obrigatório nesse cenário: o modo padrão do chart (`cluster-pool`, `10.0.0.0/8`) colide com a sub-rede de pods e o CIDR de serviços configurados pelo kubeadm nesses clusters. Depois de criar, valide o estado:

```sh
kubectl --context cilium-demo get pods -n kube-system
kubectl --context cilium-demo get nodes -o wide
```

## Outras novidades da versão 1.7.1

Além do `container cluster`, a release `1.7.1` traz melhorias práticas no runtime para o dia a dia no macOS:

- **Exclusão automática do Time Machine:** snapshots de imagens e filesystems de containers agora são excluídos dos backups do Time Machine, evitando que camadas temporárias inflam backups locais e discos externos.
- **Kernel e Containerization atualizados:** o kernel Kata padrão passa para `4.3.1` (`vmlinux-6.18.56-208-debug`) junto com Containerization `0.54.0`.
- **DNS padrão em `config.toml`:** nameservers padrão, domínios de busca (`search`) e opções de DNS podem ser definidos de forma persistente no `config.toml`.
- **`cpuUtilization` no `container stats`:** os formatos legíveis por máquina (`JSON`, `YAML` e `TOML`) agora expõem `cpuUtilization`.
- **Correções no BuildKit:** resolve falhas do `container build` com versões recentes do BuildKit e erros de contexto incompleto em etapas que dependem do build context inteiro.

## Onde ele se encaixa no fluxo local

O `container cluster` não substitui um ambiente compartilhado de staging, nem entrega paridade com IAM gerenciado ou load balancers de provedores de nuvem. Onde ele realmente brilha é no loop interno rápido em Apple Silicon: validar manifestos Kubernetes, testar políticas do Cilium localmente, construir uma imagem com `container build` e vê-la rodar em segundos, ou isolar um cluster por branch sem pagar o peso de uma VM tradicional monolítica.

Na EF-TECH, ajudamos times de engenharia a construir plataformas de desenvolvimento rápidas e pipelines de entrega Kubernetes reproduzíveis. [Fale conosco](/pt-br/contato/) se quiser simplificar o fluxo do laptop à produção, ou explore outros artigos técnicos no nosso [blog](/pt-br/blog/).

## Links e Referências

- **Documentação de Cluster do Apple `container` (`1.7.1`)** — [github.com/apple/container/blob/1.7.1/docs/cluster.md](https://github.com/apple/container/blob/1.7.1/docs/cluster.md)
- **Release `1.7.1` do Apple `container`** — [github.com/apple/container/releases/tag/1.7.1](https://github.com/apple/container/releases/tag/1.7.1)
- **Repositório oficial Apple `container`** — [github.com/apple/container](https://github.com/apple/container)

### Origem das notas

Estas notas tiveram origem no daily de **2026-11-13** (`daily/2026-11-13-Fri.md`), que registrou a chegada do suporte a Kubernetes na CLI `container` da Apple por meio dos seguintes links:

- `https://t.co/RkbfF72KEC` — link encurtado que aponta para `https://github.com/apple/container/blob/1.7.1/docs/cluster.md`
- `https://github.com/apple/container/releases/tag/1.7.1` — notas da release `1.7.1`, publicada em 6 de novembro de 2026
