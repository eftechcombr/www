---
title: "Gateway API v1.6 — TCPRoute e UDPRoute tornam-se Standard"
description: "O Gateway API v1.6.0 do Kubernetes traz TCPRoute e UDPRoute para Standard (GA) com roteamento L4 TCP/UDP portável, apresenta o novo recurso experimental XBackend e separa as APIs experimentais no grupo gateway.networking.x-k8s.io."
summary: "O Gateway API v1.6.0 chegou. TCPRoute e UDPRoute deixam o estágio Experimental e passam a Standard na versão v1, oferecendo a workloads como bancos de dados, DNS, VoIP, jogos e IoT uma forma portátil de rotear tráfego L4 puro. A release também adiciona o novo recurso experimental XBackend e separa as APIs experimentais no grupo gateway.networking.x-k8s.io."
date: 2026-08-03
draft: false
tags: ["kubernetes", "gateway-api", "redes", "service-mesh", "cncf"]
categories: ["infraestrutura"]
featureimage: "cover.png"
featureimagecaption: "Capa do Gateway API v1.6 — TCPRoute e UDPRoute promovidos a Standard"
---

A comunidade Kubernetes SIG Network lançou o **Gateway API v1.6.0** em 30 de junho de 2026, e esta é uma release marcante: **TCPRoute e UDPRoute deixam o estágio Experimental e passam a Standard (GA)** na versão de API `v1`. Pela primeira vez, você consegue rotear tráfego TCP e UDP puro com o Gateway API usando uma API portátil e neutra de fornecedor — sem precisar recorrer a um `Service` comum ou a CRDs específicos de cada implementação.

![Gateway API v1.6](cover.png)

## O Que Há de Novo no Gateway API v1.6

- **TCPRoute e UDPRoute agora são Standard** (`v1`), habilitando roteamento portátil de tráfego L4 puro.
- **Um novo recurso experimental, XBackend**, chega no grupo `gateway.networking.x-k8s.io/v1alpha1` como um decorator de uso geral para backends.
- **APIs experimentais ganham grupo próprio**: novos recursos experimentais passam a viver em `gateway.networking.x-k8s.io` com o prefixo `X`, em vez do antigo esquema de versões.
- **Seis implementações são conformes com o v1.6** no dia do anúncio.

## TCPRoute e UDPRoute tornam-se Standard

O roteamento puro na camada 4 (L4) é um dos recursos mais pedidos na história do Gateway API. Antes do v1.6, workloads que precisam de tráfego TCP ou UDP em nível de protocolo — bancos de dados, DNS, VoIP, jogos, telemetria de IoT — dependiam do `Service` comum do Kubernetes ou de CRDs atrelados a uma implementação específica.

Com `TCPRoute` e `UDPRoute` na versão de API `v1`, isso muda. Um `Gateway` declara um listener com `protocol: TCP` (ou `UDP`) e uma lista `allowedRoutes.kinds` que inclui o tipo de rota. A rota se conecta ao listener por meio de `parentRefs` — com `sectionName` e `port` opcionais — e encaminha o tráfego para um backend via `rules[].backendRefs`.

Veja como fica uma configuração TCP:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: tcp-gateway
spec:
  gatewayClassName: example
  listeners:
    - name: tcp
      protocol: TCP
      port: 3306
      allowedRoutes:
        kinds:
          - group: gateway.networking.k8s.io
            kind: TCPRoute
---
apiVersion: gateway.networking.k8s.io/v1
kind: TCPRoute
metadata:
  name: database
spec:
  parentRefs:
    - name: tcp-gateway
      sectionName: tcp
      port: 3306
  rules:
    - backendRefs:
        - name: database
          port: 3306
```

A `UDPRoute` segue exatamente o mesmo padrão — basta trocar `protocol: TCP` por `protocol: UDP` no listener e usar `kind: UDPRoute` (com a entrada correspondente em `allowedRoutes.kinds`) na rota.

**Nota sobre depreciação:** as versões `v1alpha2` de `TCPRoute` e `UDPRoute` estão deprecadas a partir do v1.6 e serão removidas em uma release futura. Quem ainda usa `v1alpha2` deve planejar a migração para `v1`.

## XBackend: um novo recurso experimental (GEP-4894)

Junto com a promoção a GA, o v1.6 introduz uma nova API experimental chamada **XBackend**, um decorator de uso geral para `Service` e outros tipos de backend. Ela vive no novo grupo de API `gateway.networking.x-k8s.io/v1alpha1`.

A primeira versão do `XBackend` suporta destinos `ExternalHostname` — um recurso Extended/Opcional útil para cenários de egress e workloads de IA agêntica. Como um `ExternalHostname` resolve para um endereço fora do cluster, vale lembrar da consideração de segurança conhecida como *confused deputy*: qualquer controlador que faça proxy para hostnames externos deve ser explícito sobre quais hostnames ele pode acessar.

A comunidade também está trabalhando para mover a configuração de Session Persistence do `XBackendTrafficPolicy` para dentro do `XBackend`, além de adicionar suporte a retries e TLS origination.

## APIs experimentais ganham grupo próprio

O v1.6 também muda *como* as APIs experimentais são versionadas. Novos recursos experimentais agora vivem em um grupo de API separado, `gateway.networking.x-k8s.io`, e os nomes de seus tipos recebem o prefixo `X` — por exemplo, `XBackend` e `XMesh`. Quando um recurso passa a Standard, ele é renomeado para `gateway.networking.k8s.io` e o prefixo `X` é removido (por exemplo, `XMesh` vira `Mesh`).

`TCPRoute` e `UDPRoute` foram os últimos recursos a serem promovidos sob o antigo esquema de versões (`v1alpha2` → `v1`). Daqui para frente, o grupo com prefixo `X` deixa claro de imediato quais recursos ainda são experimentais.

## Conformidade: seis implementações

A conformidade do Gateway API é garantida por uma suíte de testes formal, e as seis implementações a seguir eram conformes com o v1.6 no dia da publicação:

- Agentgateway
- Airlock Microgateway
- GKE Gateway
- kgateway
- NGINX Gateway Fabric
- Traefik Proxy

## Experimente Você Mesmo

Se quiser testar roteamento TCP ou UDP hoje, qualquer uma das implementações conformes acima é um bom ponto de partida. O projeto mantém guias de usuário para roteamento [TCP](https://gateway-api.sigs.k8s.io/guides/user-guides/tcp/) e [UDP](https://gateway-api.sigs.k8s.io/guides/user-guides/udp/), além da [documentação completa](https://gateway-api.sigs.k8s.io/) e das [notas da release v1.6.0](https://github.com/kubernetes-sigs/gateway-api/releases/tag/v1.6.0).

## Participe

O Gateway API é o padrão de service networking do Kubernetes: orientado a papéis, expressivo e construído sob o SIG Network. Para participar:

- Entre no canal **#sig-network-gateway-api** no [Slack do Kubernetes](https://slack.k8s.io/)
- Acompanhe o calendário do SIG Network para as reuniões da comunidade
- Explore e contribua com o [repositório do gateway-api](https://github.com/kubernetes-sigs/gateway-api)

---

Na **EF-TECH**, somos especialistas em Kubernetes, cloud computing e automação de infraestrutura. Ajudamos equipes a projetar e operar service networking moderno — incluindo o Gateway API. [Entre em contato](/pt-br/contato/) para saber como podemos ajudar sua equipe. Para mais artigos como este, visite nosso [blog](/pt-br/blog/).
