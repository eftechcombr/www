---
title: "Argo CD 3.5 Lança Interface Dedicada para ApplicationSet: Gerenciando GitOps em Escala"
description: "O Argo CD v3.5 apresenta uma interface de primeira classe para ApplicationSets, com árvore de recursos, status de saúde, preview editável e badges de proprietário. Um mergulho no que muda para equipes GitOps."
summary: "O Argo CD v3.5 finalmente entrega uma interface dedicada para ApplicationSets, atendendo a uma das solicitações mais antigas da comunidade. A nova interface inclui página de listagem com busca e filtros, árvore de recursos que mostra o relacionamento entre ApplicationSets e Applications geradas, status de saúde como campo de primeira classe, modo preview com YAML editável e badges de proprietário para rastreabilidade. Uma visão geral dos recursos e limitações."
date: 2026-07-17
draft: false
tags: ["argocd", "kubernetes", "gitops", "applicationset"]
categories: ["infraestrutura"]
---

O Argo CD sempre foi reconhecido por sua interface de usuário — árvore de recursos, status de sincronização em tempo real, visualização de diffs — que tornou o GitOps acessível para equipes que não vivem dentro de arquivos YAML. Os ApplicationSets, no entanto, sempre se encaixaram de forma estranha nesse cenário. Até agora.

Com a versão 3.5, o Argo CD entrega uma interface de primeira classe para ApplicationSets, atendendo a uma solicitação de funcionalidade que acumulou 189 reações positivas na comunidade. Este artigo explora o que está sendo entregue e por que isso importa para equipes que gerenciam GitOps em escala.

## A lacuna de visibilidade dos ApplicationSets

ApplicationSets seguem um padrão de fábrica para Applications. Você escreve um único recurso que diz "para cada cluster que corresponda a esta label, gere uma Application a partir deste template", e o controlador produz N Applications filhas. Um único ApplicationSet pode se espalhar por dezenas de clusters e centenas de repositórios.

Antes da versão 3.5, os operadores tinham duas opções para inspecionar ApplicationSets: usar `kubectl` ou `argocd appset` no terminal, ou encapsular o ApplicationSet dentro de um App-of-Apps e navegar pela árvore de recursos da Application pai. Nenhuma das abordagens é ideal para ambientes de produção com dezenas ou centenas de ApplicationSets.

## O que a nova interface oferece

A nova interface é acessível pela rota `/applicationsets` e por um item dedicado na barra de navegação.

### Listagem com controles familiares

A página de listagem de ApplicationSets segue o mesmo padrão da lista de Applications — busca por substring, filtros, gráfico de pizza com resumo de saúde e layout alternável. As políticas de RBAC são aplicadas exatamente como no CLI.

### Árvore de recursos mostrando a genealogia

Cada ApplicationSet é exibido como um nó raiz, com cada Application gerada como um nó downstream. Clicar em uma Application filha leva diretamente para a página de detalhes, facilitando o rastreamento da relação entre o template gerador e suas instâncias implantadas.

### Saúde como campo de primeira classe

O controlador de ApplicationSet agora escreve `status.health` derivado das condições de status, com três estados possíveis: Healthy, Degraded e Progressing. As condições são expostas pela interface, dando aos operadores a mesma consciência de saúde que já possuem para Applications individuais.

### Painel lateral

Ao clicar em um nó de ApplicationSet ou no botão Details, um painel lateral é aberto com quatro abas: Summary, Manifest, Events e Preview.

### Preview do ApplicationSet

A aba Preview replica o comando `argocd appset generate` diretamente no navegador. É possível editar o YAML do ApplicationSet, alterar generators e executar o preview novamente. Três visualizações estão disponíveis: LIVE APPS (estado atual), DIFF (o que mudaria) e DESIRED APPS (saída gerada).

### Preview de App-of-AppSet

Para equipes que utilizam o padrão App-of-Apps, o preview também funciona a partir da Application pai, mostrando quais Applications filhas seriam alteradas na próxima sincronização.

### Badges de proprietário e nó raiz sintético

Applications filhas exibem um badge com o nome do ApplicationSet pai. Um ícone de nó raiz sintético pode ser ativado nas árvores de recursos das Applications filhas para contexto adicional.

## Limitações importantes

A interface de ApplicationSet é somente leitura nesta fase alpha. Operações de criação, atualização e exclusão continuam fluindo pelo Git, preservando o modelo Git como fonte única da verdade. O recurso está em alpha na versão 3.5, portanto a aparência e o comportamento podem mudar antes de atingir a versão estável.

Disponibilidade: o release candidate do Argo CD 3.5 chega em 16 de junho de 2026, com disponibilidade geral em 4 de agosto de 2026.

## Impacto prático para equipes GitOps

Para organizações que gerenciam deployments multi-cluster com ApplicationSets, a nova interface preenche uma lacuna significativa de observabilidade. Operadores não precisam mais alternar entre terminal e interface gráfica para entender o estado de seus ApplicationSets. A visualização em árvore deixa imediatamente claro quais Applications um determinado generator produziu e se essas Applications estão saudáveis.

O recurso de Preview é particularmente valioso para equipes que experimentam novos generators ou templates. Poder iterar sobre o spec do ApplicationSet e ver o diff ao vivo antes de fazer o commit reduz o ciclo de feedback de minutos para segundos.

## Conclusão

A interface de ApplicationSets do Argo CD 3.5 é um marco para o projeto. Ela tira os ApplicationSets do universo exclusivo de YAML e os leva para a interface visual que tornou o Argo CD popular. Embora a versão alpha seja somente leitura, a base é sólida e atende às necessidades mais urgentes de visibilidade para operadores de ApplicationSets.

Na EF-TECH, ajudamos empresas a implementar e gerenciar workflows GitOps com Argo CD em escala. [Entre em contato](/pt-br/contato/).
