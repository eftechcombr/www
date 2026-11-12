---
title: "OctoDoctor: o guia de antipadrões do Argo CD virou executável"
description: "O OctoDoctor é um binário gratuito, open source e read-only que varre manifests ou um cluster do Argo CD e transforma 26 antipadrões em relatório HTML, JSON e YAML — com skill para agentes e gate de CI embutidos."
summary: "A Octopus Deploy empacotou seus guias de boas práticas de Argo CD em verificações executáveis. O OctoDoctor lê Applications, ApplicationSets, AppProjects e Secrets de cluster, nunca escreve neles, e devolve um código de saída que transforma o relatório em gate de pipeline. Passo pelos dois modos, pelas regras que importam, pela progressão `none → high → medium` e pela skill que trata o exit 1 como resultado, não como falha."
date: 2026-11-11
draft: false
tags: ["argocd", "gitops", "kubernetes", "security", "open-source"]
categories: ["infraestrutura"]
featureimage: "/img/blog/octodoctor-argocd-anti-patterns/cover.png"
featureimagecaption: "O OctoDoctor inspeciona os manifests de aplicações do Argo CD como um scanner: o relatório é o diagnóstico, o código de saída é o gate."
---

Todo time que opera Argo CD já leu uma lista de antipadrões. Pouquíssimos têm um pipeline que para quando um deles aparece. É essa lacuna — entre o documento e o controle — que a Octopus Deploy atacou com o **OctoDoctor**, um utilitário gratuito e open source que varre a configuração do seu Argo CD e devolve um relatório do que está errado.

Se você já leu [Top 30 Argo CD anti-patterns](https://octopus.com/blog/30-argo-cd-antipatterns-for-gitops), conhece o problema: as regras são boas, mas ninguém as aplica. O OctoDoctor é a tentativa de fechar essa lacuna — ele empacota as boas práticas que a Octopus vinha publicando em guias e as transforma em verificações executáveis.

![OctoDoctor varrendo uma pilha de manifests de aplicações do Argo CD contra um checklist](/img/blog/octodoctor-argocd-anti-patterns/cover.png)

## O que ele lê, e o que ele ignora

O escopo é honestamente restrito, e isso é uma qualidade. O OctoDoctor não olha o seu código de aplicação, não avalia imagens e não substitui um policy engine. Ele lê **Applications, ApplicationSets, AppProjects**, os ConfigMaps e Secrets do Argo CD e os Secrets de cluster — e ignora todo o resto. Você pode apontar o binário para um repositório que também tem outros manifests Kubernetes sem medo.

E ele é **read-only**. Nos dois modos de execução, só lê. Pode rodar contra produção sem cerimônia.

A Octopus afirma que a ferramenta foi testada em instalações grandes — mais de 100 clusters e 20.000 Applications — e que o time de suporte a usa como instrumento de descoberta: em vez de pedir que o cliente descreva a instalação do Argo CD, pede o relatório. Esse detalhe diz muito sobre o uso pretendido. O relatório não é um placar; é uma linguagem comum para uma conversa sobre configuração.

## Um binário, dois modos

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

### O que cai no disco

O relatório sai em `octodoctor-output/`, dentro do diretório varrido:

```text
/path/to/argocd/manifests/
└── octodoctor-output/
    ├── index.html     # abra no navegador
    ├── report.json
    └── report.yaml
```

O HTML lista no máximo `--limit` arquivos por regra, para não virar uma parede. Os arquivos JSON e YAML contêm **todos** os arquivos, e são a escolha certa para scripts. Gosto dessa divisão: o humano recebe uma visão curada, a máquina recebe a verdade inteira.

## O código de saída é o contrato

A parte mais útil do desenho é o contrato de saída. O OctoDoctor retorna `1` quando pelo menos uma regra falha e `0` caso contrário. Isso o transforma em gate de pipeline sem nenhum wrapper:

```bash
# Primeira adoção: só observa, sempre sai com 0
./octodoctor -d ./gitops --fail-on none

# Depois: bloqueia apenas falhas de severidade alta
./octodoctor -d ./gitops --fail-on high
```

A progressão `none` → `high` → `medium` é o jeito certo de introduzir uma ferramenta dessas num repositório que já tem dívida. Você começa medindo, não bloqueando. Um time que liga `--fail-on medium` no primeiro dia odeia a ferramenta no terceiro; um time que lê o relatório primeiro, corrige as duas regras que mais doem e só então sobe a régua mantém a ferramenta.

## Regras que valem a leitura

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

## A skill para agentes

Junto com o binário, o projeto publica uma skill chamada `octodoctor-report`. Ela usa o `octodoctor` do `PATH` se ele existir; se não, baixa a release mais recente para um diretório temporário e verifica o checksum. Só precisa de `curl` e `tar`.

```bash
# Com o skills CLI
npx skills add OctopusDeploy/octodoctor-argocd --skill octodoctor-report

# Ou com o GitHub CLI (gh skill está em preview)
gh skill install OctopusDeploy/octodoctor-argocd octodoctor-report --agent claude-code
```

Depois disso, a interação é em linguagem natural: *"verifique os manifests do Argo CD em ./gitops contra as boas práticas"* ou *"audite a instalação do Argo CD no meu cluster de produção"*. O agente escolhe o modo, roda a ferramenta e responde com o número de regras que falharam, a lista ordenada por severidade e o caminho do `index.html`.

Dois detalhes de implementação merecem elogio. Primeiro: a skill trata o exit code `1` como **resultado normal**, não como erro — é exatamente o comportamento correto, e é onde muita integração de agente com ferramenta de lint erra. Um agente que lê saída diferente de zero como crash vai tentar de novo para sempre ou pedir desculpa em vez de mostrar o relatório. Segundo: o agente só edita manifests para corrigir as falhas **se você pedir**. Um scanner que reescreve seu repositório GitOps em silêncio é outro produto, com outro perfil de risco.

## Onde isso se encaixa ao lado do próprio Argo CD

Se você opera Argo CD, vale comparar esse tipo de verificação estática com as mudanças recentes do próprio Argo CD. No [Argo CD 3.6](/pt-br/blog/argocd-3-6/), o Server-Side Diff passou a fazer dry-run real contra o kube-apiserver para decidir se algo está `Synced` — mais precisão no runtime. O OctoDoctor ataca a camada de cima: a configuração que gerou aquele estado. E se você usa ApplicationSets em escala, a [interface dedicada do Argo CD 3.5](/pt-br/blog/argocd-appset-ui/) ajuda a enxergar o que a ferramenta vai reportar.

Essa divisão de trabalho é a parte útil. O Argo CD diz se o cluster corresponde ao repositório. O OctoDoctor diz se o repositório merece ser correspondido.

## Como começar

O caminho mais curto é rodar sem bloquear:

```bash
./octodoctor -d ./gitops --fail-on none
# abra ./gitops/octodoctor-output/index.html
```

Leia o relatório com o time, escolha as duas ou três regras que doem mais, corrija, e só então suba para `--fail-on high`. Se preferir o caminho com agente, instale a skill `octodoctor-report` e peça a auditoria em linguagem natural — a primeira execução baixa e verifica o binário para você.

O objetivo não é chegar a zero achados. É tornar a decisão visível: cada regra que falha agora é uma linha num relatório com que você pode discutir, não uma convenção que ninguém verificava. É isso que separa uma boa prática de um controle — o controle é o que acontece quando alguém tenta ir contra.

Na EF-TECH, operamos clusters Kubernetes com Argo CD e ajudamos times a colocar guardrails em pipelines GitOps sem travar a entrega. [Entre em contato](/pt-br/contato/) se quiser revisar a configuração do seu Argo CD. Para mais artigos como este, visite nosso [blog](/pt-br/blog/).

## Links e Referências

- **OctoDoctor: check your Argo CD cluster for best practices** — [octopus.com/blog/octodoctor-for-argocd](https://octopus.com/blog/octodoctor-for-argocd)
- **Documentação do OctoDoctor** — [octodoctor-argocd.readthedocs.io](https://octodoctor-argocd.readthedocs.io/)
- **Repositório do OctoDoctor** — [github.com/OctopusDeploy/octodoctor-argocd](https://github.com/OctopusDeploy/octodoctor-argocd)
- **Releases do OctoDoctor (binários e checksums)** — [github.com/OctopusDeploy/octodoctor-argocd/releases](https://github.com/OctopusDeploy/octodoctor-argocd/releases)
- **Top 30 Argo CD anti-patterns** — [octopus.com/blog/30-argo-cd-antipatterns-for-gitops](https://octopus.com/blog/30-argo-cd-antipatterns-for-gitops)

### Origem das notas

O anúncio foi capturado na nota diária de 2026-11-11, a partir de um post no X (Twitter). Link original e destino resolvido:

- `https://t.co/Exv4ar4B0y` → [octopus.com/blog/octodoctor-for-argocd](https://octopus.com/blog/octodoctor-for-argocd)
