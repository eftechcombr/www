---
title: "15 projetos open source brasileiros que valem a visita: de leis em Markdown a um acelerador de IA aberto"
description: "Um tour por 15 projetos open source brasileiros no GitHub: legislação em Markdown, um TPU aberto desenhado com agentes de IA, agentes de documentação reversa, um CRM self-hosted com WhatsApp e mais."
summary: "Um vídeo recente reuniu 15 projetos open source brasileiros. Este artigo reorganiza a lista por categoria, corrige os nomes que a transcrição embaralhou e acrescenta o que cada repositório realmente documenta: stack, licença e um detalhe concreto de implementação. Passa por Leis, Brasil API, pgModeler, openTPU, Bend, navi, Reversa, AI Memory, Git City, VirtualBuddy, Easy Effects, Winlator, PhotoGIMP, DeskcommCRM e Open Notebook."
date: 2026-11-07
draft: false
tags: ["open-source", "brasil", "github", "desenvolvimento", "ferramentas"]
categories: ["infraestrutura"]
featureimage: "/img/blog/projetos-open-source-brasileiros/cover.png"
featureimagecaption: "15 projetos open source brasileiros no GitHub"
---

Um vídeo recente, *15 projetos open source brasileiros no GitHub*, reuniu quinze repositórios mantidos por desenvolvedores brasileiros. A lista mistura coisas muito diferentes: infraestrutura de dados públicos, um acelerador de hardware, utilitários de desktop, ferramentas para agentes e aplicações completas.

O vídeo serve como ponto de partida, mas a transcrição automática tropeça em vários nomes — "Virtual Bunny" é VirtualBuddy, "Nave" é navi — e passa rápido demais para que os detalhes fiquem. Este artigo reorganiza a lista por categoria e descreve apenas o que cada repositório documenta: o que o projeto é, por que importa, sua stack, sua licença e um detalhe concreto de funcionamento.

![15 projetos open source brasileiros no GitHub](/img/blog/projetos-open-source-brasileiros/cover.png)

Três avisos antes de começar. O número de estrelas é aproximado e muda todo dia. As licenças são as declaradas em cada repositório, e alguns projetos combinam licenças diferentes para código e conteúdo. E nada disso é recomendação: é um mapa do que existe, para você decidir o que merece um clone.

## Dados, serviços públicos e infraestrutura

### Leis: a legislação brasileira como repositório Git

O [Leis](https://github.com/ctresb/leis) ("todas as leis do Brasil") converte a legislação federal, estadual e municipal para Markdown, um arquivo por norma, com links para a origem e o histórico completo preservado no Git. O repositório já cobre mais de 323 mil normas.

O interessante não é o parsing em si, e sim a interface que ele cria. A legislação vira um corpus que você pode passar por `grep`, fazer `diff` e revisar como código. Uma alteração em uma norma aparece como commit; uma versão histórica é um checkout. Para quem constrói legal tech, ferramentas de compliance ou pesquisa sobre a lei brasileira, é um ponto de partida muito melhor do que raspar PDF de diário oficial.

O projeto é explícito sobre os limites: a cobertura é parcial, a conversão pode introduzir erros de OCR e o texto não substitui o diário oficial. Os textos oficiais são atos públicos; os scripts de conversão estão sob MIT. Com cerca de 2,6 mil estrelas, é o tipo de repositório cujo valor fica mais claro quando você precisa dele do que quando você o navega.

### Brasil API: dados públicos brasileiros sem chave de API

A [Brasil API](https://github.com/BrasilAPI/BrasilAPI) é uma API pública, gratuita e comunitária para dados brasileiros: CEP, CNPJ, DDD, bancos, feriados e taxas, entre outros.

O problema que ela resolve é conhecido de quem integra sistemas no Brasil: as fontes oficiais são fragmentadas, inconsistentes e muitas vezes exigem cadastro ou oferecem interfaces hostis a scraping. A Brasil API centraliza o acesso em endpoints previsíveis, com página de status e documentação em [brasilapi.com.br](https://brasilapi.com.br). É escrita em Node.js, licenciada sob MIT e tem cerca de 11,5 mil estrelas.

Para projetos paralelos e ferramentas internas, ela economiza uma semana de integração. Em produção, trate como serviço comunitário: cache as respostas, trate falhas e saiba de qual fonte cada endpoint depende.

### pgModeler: modelagem visual para PostgreSQL

O [pgModeler](https://github.com/nullptrlabs/pgmodeler) é uma ferramenta de modelagem de dados feita especificamente para PostgreSQL. Você desenha o diagrama e a ferramenta gera o DDL. Ela também compara o modelo com um banco em execução, o que torna visível a divergência entre desenho e realidade, e exporta e importa entre o modelo visual e SQL.

É escrito em C++ com Qt, licenciado sob GPL-3.0 e tem cerca de 3,6 mil estrelas. O projeto existe há tempo suficiente para ser entediante no melhor sentido — há documentação e um site dedicado em [pgmodeler.io](https://pgmodeler.io).

Por que importa: a maioria das ferramentas de modelagem trata o PostgreSQL como um dialeto entre muitos. O pgModeler acompanha recursos específicos do PostgreSQL, que é exatamente onde as ferramentas genéricas começam a gerar DDL que não corresponde ao que você queria.

## Hardware e computação de alto desempenho

### openTPU: um acelerador de IA aberto desenhado com agentes de IA

O [openTPU](https://github.com/FeSens/openTPU) é o item mais ambicioso da lista: um acelerador de IA open source, desenhado com ajuda de agentes de IA e publicado até o nível de RTL.

O repositório inclui RTL em SystemVerilog, uma ISA, um simulador bit-exact, uma linguagem de kernels com compilador e o software de host. Ele roda Qwen3, LFM2.5 e Qwen3.5 em uma placa FPGA Kintex-7 PCIe — mais especificamente uma Inspur YPCB-00338 com 4 GiB de DDR3. Apache-2.0, Verilog, cerca de 930 estrelas.

O rótulo "desenhado com agentes de IA" é o que chama atenção, mas a substância de engenharia está no simulador: um modelo bit-exact permite validar kernels antes de tocar no hardware, e é isso que torna o trabalho em FPGA reproduzível. É também um caso raro de projeto brasileiro atuando no nível de RTL com uma stack de software completa em volta.

### Bend: programação massivamente paralela sem a cerimônia habitual

[Bend](https://github.com/bendlang/bend) é uma linguagem de programação de Victor Taelin (HigherOrderCO) feita para paralelismo massivo: o mesmo programa pode rodar em milhares de núcleos de GPU ou CPU. Ela se apoia em semântica funcional e usa provas para pegar erros em tempo de compilação, não às três da manhã.

A linguagem é implementada em TypeScript, licenciada sob Apache-2.0 e tem cerca de 24,8 mil estrelas. Ela saiu da antiga organização `HigherOrderCO/Bend` para `bendlang/bend`; a URL antiga redireciona, mas o link canônico é o novo. A documentação está em [bend-lang.com](https://bend-lang.com).

Bend é uma linguagem com sabor de pesquisa, não um substituto direto do seu backend de produção. O valor está no modelo: escrever código paralelo em uma linguagem em que o runtime cuida da distribuição muda a forma como você pensa o problema.

## Ferramentas para desenvolvedores

### navi: cheatsheets executáveis

O [navi](https://github.com/denisidoro/navi) é uma ferramenta interativa de cheatsheet para linha de comando. Você navega pelos snippets, escolhe um, preenche os argumentos dinâmicos e executa — sem sair do terminal.

É escrito em Rust e usa fzf ou skim como seletor, com widgets para shell e tmux, de modo que a cheatsheet abre em um popup. Cerca de 17,8 mil estrelas, Apache-2.0. As cheatsheets são arquivos de texto simples, o que permite ao time versionar o conhecimento operacional ao lado do código que ele opera:

```bash
eval "$(navi widget zsh)"
```

Essa linha entrega um atalho de teclado que abre as cheatsheets do time em um menu com busca fuzzy. Para runbooks, é uma alternativa mais leve do que uma wiki que ninguém abre durante o incidente.

### Reversa: documentação reversa para bases legadas

O [Reversa](https://github.com/sandeco/reversa) ataca um problema que toda consultoria conhece: um sistema sem documentação, sem testes e com regras de negócio que existem apenas na cabeça de quem está prestes a se aposentar.

O fluxo começa dentro do projeto legado:

```bash
npx reversa install
```

A partir daí, um time de agentes especializados — Scout, Archaeologist, Detective, Architect, Writer e Reviewer — extrai regras de negócio e produz especificações executáveis e rastreáveis (SDD, spec-driven development) que agentes de código conseguem consumir. Ele escreve apenas em `.reversa/` e `_reversa_sdd/`, então a base legada não é modificada. Há um artigo no arXiv descrevendo a abordagem.

Escrito em JavaScript, MIT, cerca de 1,9 mil estrelas. A decisão de design que merece nota é o limite de escrita: uma ferramenta baseada em agentes que reescreve o código que está analisando é difícil de confiar, e o Reversa deliberadamente não faz isso.

### AI Memory: memória de longo prazo para agentes de código

O [AI Memory](https://github.com/akitaonrails/ai-memory) dá aos agentes de código uma memória que sobrevive à sessão. Funciona com Claude Code, Codex, Cursor, OpenCode, Gemini CLI e mais de vinte harnesses.

O modelo de armazenamento é deliberadamente pouco exótico: uma wiki em Markdown versionada no Git. A recuperação é zero-LLM por padrão, então lembrar não custa tokens nem depende de chamada a modelo, e os handoffs entre agentes ou máquinas são tipados e claim-once, o que evita dois agentes pegarem a mesma tarefa pendente. Escrito em Rust, MIT, cerca de 15,3 mil estrelas, com documentação em [aimemory.sh](https://aimemory.sh).

O efeito prático é que contexto deixa de ser algo que você reexplica toda manhã. É também um bom exemplo de padrão de design que vai sobreviver aos frameworks de agente atuais: texto puro no Git, com estrutura por cima.

### Git City: seu perfil do GitHub como prédio

O [Git City](https://github.com/srizzon/git-city) transforma um perfil do GitHub em um prédio 3D em pixel art dentro de uma cidade interativa. Contribuições definem a altura, repositórios definem a largura e estrelas definem o brilho das janelas.

É construído com Next.js, Three.js e Supabase, licenciado sob AGPL-3.0, com cerca de 6 mil estrelas. Dá para ver rodando em [thegitcity.com](https://thegitcity.com).

É o projeto mais leve da lista, e tudo bem. É também uma demonstração compacta de como renderizar uma cena 3D gerada proceduralmente no navegador sem derrubar o frame rate — material de referência útil mesmo que você nunca construa uma cidade.

## Desktop e mobile

### VirtualBuddy: VMs de macOS em Apple Silicon

O [VirtualBuddy](https://github.com/insidegui/VirtualBuddy) é uma interface nativa para rodar macOS 12 ou superior — incluindo betas — em máquinas virtuais no Apple Silicon, além de algumas distribuições Linux ARM. Ele é construído sobre o framework de virtualização da Apple.

Os recursos são os que tornam o uso diário tolerável: assistente de instalação, download de IPSW, salvar e retomar o estado da máquina, compartilhamento de clipboard e de pastas. Escrito em Swift, BSD-2-Clause, cerca de 8,9 mil estrelas.

Para quem precisa testar software contra uma versão beta do macOS sem dedicar uma máquina a isso, é o caminho mais curto. A transcrição do vídeo chama de "Virtual Bunny"; o repositório é VirtualBuddy.

### Easy Effects: processamento de áudio em tempo real no PipeWire

O [Easy Effects](https://github.com/wwmm/easyeffects) leva um rack de efeitos de áudio em tempo real para desktops Linux com PipeWire: equalizador, compressor, limiter, convolver, redução de ruído e autovolume, aplicados a microfones e saídas.

GPL-3.0, cerca de 10,5 mil estrelas. O valor não está em um efeito isolado, mas no modelo de roteamento: os efeitos são por dispositivo e persistem, então um microfone de notebook e uma interface USB podem ter cadeias próprias.

É o tipo de projeto que silenciosamente elimina a necessidade de bootar outro sistema operacional só para soar aceitável em uma chamada.

### Winlator: aplicativos Windows no Android

O [Winlator](https://github.com/brunodev85/winlator) roda aplicativos e jogos Windows no Android usando Wine combinado com Box86 e Box64 para emular x86 em dispositivos ARM.

Escrito em C, LGPL-2.1, cerca de 19,8 mil estrelas, com releases e documentação em [winlator.org](https://winlator.org). O desempenho depende muito do dispositivo e do aplicativo: é tradução e emulação, não execução nativa, e o projeto é honesto quanto a isso.

A engenharia interessante está na camada de integração — configuração de contêiner, drivers gráficos e mapeamento de entrada — que é o que transforma um conjunto de emuladores em algo que uma pessoa consegue usar.

### PhotoGIMP: fazendo o GIMP se comportar como o Photoshop

O [PhotoGIMP](https://github.com/Diolinux/PhotoGIMP) é um patch e um conjunto de configurações que fazem o GIMP 3 ou superior parecer familiar para usuários de Photoshop: atalhos de teclado, disposição das ferramentas e organização da interface são ajustados para seguir as convenções da Adobe.

Python, GPL-3.0, cerca de 18,5 mil estrelas. Ele não adiciona recursos; remove o custo de migração. Para um time de design mudando para software livre, esse custo costuma ser o bloqueio real — não o filtro que falta.

## Aplicações e agentes de IA

### DeskcommCRM: CRM self-hosted com WhatsApp e agentes

O [DeskcommCRM](https://github.com/melgarafael/DeskcommCRM) se descreve como um "sistema operacional de vendas com IA": um CRM self-hosted com agentes de IA nativos e integração com WhatsApp, posicionado como alternativa a Kommo, Octadesk e Intercom.

Ele conecta ao WhatsApp via WAHA com pareamento por QR code ou via Meta Cloud API; cada tenant tem seu próprio contexto de RAG, o CRM é exposto por MCP para que agentes possam consultá-lo, e o multi-tenancy é garantido com row-level security e atenção à LGPD. Stack: Next.js e Supabase, TypeScript, MIT, cerca de 5,2 mil estrelas.

As escolhas de arquitetura importam mais do que a lista de recursos: self-hosted, isolamento por tenant e um protocolo aberto para acesso de agentes. Essa combinação ainda é incomum em ferramentas brasileiras de CRM, onde o padrão é o SaaS fechado.

### Open Notebook: uma alternativa self-hosted ao NotebookLM

O [Open Notebook](https://github.com/lfnovo/open-notebook) é uma alternativa open source e self-hosted ao NotebookLM. Você escolhe o modelo e o provedor, ingere fontes e gera podcasts e notas a partir delas.

TypeScript, MIT, cerca de 41,7 mil estrelas, com documentação em [www.open-notebook.ai](https://www.open-notebook.ai). É o projeto com mais estrelas da lista, o que diz algo sobre a demanda por rodar esse tipo de ferramenta na própria infraestrutura.

Para times que não podem enviar documentos internos a um serviço de terceiros, a propriedade interessante não é o gerador de podcast — é o fato de o provedor de modelo ser uma escolha de configuração, não uma decisão de fornecedor.

## O que esses quinze projetos têm em comum

Dois padrões se destacam.

O primeiro é problema local resolvido com ferramenta global. Leis, Brasil API, DeskcommCRM e Winlator existem porque o contexto brasileiro tem restrições específicas — dados públicos fragmentados, WhatsApp como canal padrão de comunicação, legislação que muda o tempo todo. Nenhum deles é tradução de um produto existente.

O segundo é mantenedor brasileiro trabalhando em infraestrutura global. openTPU, Bend, navi, AI Memory e Open Notebook disputam atenção com projetos de qualquer lugar, e seu público é internacional. O perfil no GitHub não diz onde o mantenedor mora; o README também não.

As licenças são majoritariamente permissivas — MIT e Apache-2.0 dominam — com GPL-3.0 nas aplicações de desktop e AGPL-3.0 no Git City. Essa distribuição é típica do cenário atual: permissiva para bibliotecas e infraestrutura, copyleft para aplicações em que a brecha do serviço hospedado importa.

Uma nota prática: estrelas medem atenção, não manutenção. Antes de adotar qualquer coisa de uma lista como esta, olhe o último commit, o tratamento das issues e se o projeto publica releases. Muitas estrelas com um ano de silêncio são um alerta, não uma recomendação.

## Resumo

| Projeto | O que faz | Stack | Licença | Estrelas (aprox.) |
| --- | --- | --- | --- | --- |
| [Leis](https://github.com/ctresb/leis) | Legislação brasileira em Markdown | — | MIT (scripts) | 2,6 mil |
| [openTPU](https://github.com/FeSens/openTPU) | Acelerador de IA aberto | Verilog | Apache-2.0 | 930 |
| [Reversa](https://github.com/sandeco/reversa) | Agentes de documentação reversa | JavaScript | MIT | 1,9 mil |
| [DeskcommCRM](https://github.com/melgarafael/DeskcommCRM) | CRM self-hosted com WhatsApp | TypeScript | MIT | 5,2 mil |
| [pgModeler](https://github.com/nullptrlabs/pgmodeler) | Modelagem de dados PostgreSQL | C++/Qt | GPL-3.0 | 3,6 mil |
| [VirtualBuddy](https://github.com/insidegui/VirtualBuddy) | VMs de macOS em Apple Silicon | Swift | BSD-2-Clause | 8,9 mil |
| [Easy Effects](https://github.com/wwmm/easyeffects) | Processamento de áudio em tempo real | — | GPL-3.0 | 10,5 mil |
| [navi](https://github.com/denisidoro/navi) | Cheatsheets interativas | Rust | Apache-2.0 | 17,8 mil |
| [Brasil API](https://github.com/BrasilAPI/BrasilAPI) | API de dados públicos brasileiros | Node.js | MIT | 11,5 mil |
| [Winlator](https://github.com/brunodev85/winlator) | Apps Windows no Android | C | LGPL-2.1 | 19,8 mil |
| [PhotoGIMP](https://github.com/Diolinux/PhotoGIMP) | GIMP com cara de Photoshop | Python | GPL-3.0 | 18,5 mil |
| [Bend](https://github.com/bendlang/bend) | Linguagem massivamente paralela | TypeScript | Apache-2.0 | 24,8 mil |
| [Git City](https://github.com/srizzon/git-city) | Perfil do GitHub como cidade 3D | Next.js/Three.js | AGPL-3.0 | 6 mil |
| [AI Memory](https://github.com/akitaonrails/ai-memory) | Memória para agentes de código | Rust | MIT | 15,3 mil |
| [Open Notebook](https://github.com/lfnovo/open-notebook) | Alternativa self-hosted ao NotebookLM | TypeScript | MIT | 41,7 mil |

## Conclusão

Listas como esta funcionam melhor como fila do que como catálogo. Escolha dois projetos que toquem um problema que você realmente tem — um sistema legado sem documentação, uma integração com dados públicos brasileiros, um CRM que precisa ficar na sua infraestrutura — e leia o repositório antes do marketing do README.

O sinal mais interessante é estrutural: o open source brasileiro deixou de se limitar a utilitários e traduções de projetos estrangeiros. Há trabalho original em design de RTL, pesquisa em linguagens de programação, memória para agentes e infraestrutura de dados, publicado sob licenças que permitem uso comercial.

---

## Links e Referências

- [Vídeo: 15 projetos open source brasileiros no GitHub](https://www.youtube.com/watch?v=rcoZzJ8ifeU)
- [Leis](https://github.com/ctresb/leis)
- [openTPU](https://github.com/FeSens/openTPU)
- [Reversa](https://github.com/sandeco/reversa)
- [DeskcommCRM](https://github.com/melgarafael/DeskcommCRM)
- [pgModeler](https://github.com/nullptrlabs/pgmodeler) — [pgmodeler.io](https://pgmodeler.io)
- [VirtualBuddy](https://github.com/insidegui/VirtualBuddy)
- [Easy Effects](https://github.com/wwmm/easyeffects)
- [navi](https://github.com/denisidoro/navi)
- [Brasil API](https://github.com/BrasilAPI/BrasilAPI) — [brasilapi.com.br](https://brasilapi.com.br)
- [Winlator](https://github.com/brunodev85/winlator) — [winlator.org](https://winlator.org)
- [PhotoGIMP](https://github.com/Diolinux/PhotoGIMP)
- [Bend](https://github.com/bendlang/bend) — [bend-lang.com](https://bend-lang.com)
- [Git City](https://github.com/srizzon/git-city) — [thegitcity.com](https://thegitcity.com)
- [AI Memory](https://github.com/akitaonrails/ai-memory) — [aimemory.sh](https://aimemory.sh)
- [Open Notebook](https://github.com/lfnovo/open-notebook) — [www.open-notebook.ai](https://www.open-notebook.ai)

---

Na **EF-TECH**, trabalhamos com infraestrutura open source todos os dias, de Kubernetes e GitOps às integrações que conectam sistemas brasileiros ao resto da stack. [Entre em contato](/pt-br/contato/) se seu time precisa de ajuda para avaliar ou operar essas ferramentas. Para mais artigos como este, visite nosso [blog](/pt-br/blog/).
