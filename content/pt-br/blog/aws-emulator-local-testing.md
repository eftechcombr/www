---
title: "AWS Emulator: teste contra a AWS sem conta e sem deploy"
description: "A AWS lançou o AWS Emulator oficial em 11 de novembro de 2026: todos os serviços num único endpoint HTTPS local, uma conta fixa, estado em memória e 501 para o que ainda não suporta. Aqui está o setup com Docker Compose, os quatro arquivos que ele gera, as variáveis de SDK que fazem funcionar — e as seis armadilhas que custam uma tarde."
summary: "O AWS Emulator roda a API da AWS localmente, assinada com credenciais que ele mesmo gera, então chamadas de SDK e CLI existentes voltam em milissegundos, sem conta e sem deploy. Passo pelo setup com Compose, pelos arquivos de credencial/config/CA, pelas variáveis de ambiente por SDK, pela verificação com `sts get-caller-identity` e pelos limites honestos: estado em memória, uma Region por instância, S3 Control inalcançável, injeção de host prefix, trust stores por SDK e o acoplamento de porta que pega todo mundo."
date: 2026-11-12
draft: false
tags: ["aws", "testing", "docker", "local-development", "ci"]
categories: ["cloud-computing"]
featureimage: "/img/blog/aws-emulator-local-testing/cover.png"
featureimagecaption: "Todos os serviços da AWS atrás de uma porta HTTPS local: as credenciais, o certificado e o estado em memória vivem na sua máquina — e desaparecem quando o container para."
---

Em 11 de novembro de 2026 a AWS anunciou o [AWS Emulator](https://aws.amazon.com/about-aws/whats-new/2026/11/aws-emulator-now-available/): uma implementação local da API da AWS com a qual **seus SDKs e sua CLI já sabem conversar**. Aponte tudo para `https://127.0.0.1:9297`, assine com as credenciais que o próprio emulador gera, e as chamadas voltam em milissegundos. Sem conta AWS. Sem deploy. Sem fatura.

É essa última parte que torna o assunto interessante para CI e para agentes de código. Uma suíte de testes que cria uma tabela no DynamoDB, grava itens e lê de volta não precisa de conta sandbox, script de limpeza nem orçamento noturno. Precisa de um container e algumas variáveis de ambiente.

![Um appliance de vidro sobre a mesa servindo todos os serviços da AWS numa única porta HTTPS local, com as credenciais e o certificado gerados ficando na máquina](/img/blog/aws-emulator-local-testing/cover.png)

## As regras do jogo

Antes de qualquer comando, o modelo de operação. Estas cinco decisões explicam quase toda surpresa que aparece depois:

| Regra | Valor | Consequência |
| --- | --- | --- |
| **Um endpoint** | `https://127.0.0.1:9297` (só HTTPS) | Um único `AWS_ENDPOINT_URL` cobre EC2, S3, IAM, Lambda e o resto. Não existe endpoint por serviço |
| **Uma conta** | `000000000000` | Nada de inventar account ID, e nenhuma chance de acertar produção por acidente |
| **Estado em memória** | Perdido no restart | Sem migração para limpar — mas também sem fixtures que sobrevivem a um `docker compose down` |
| **Uma Region por instância** | A que você exportar | Para testar várias Regions, rode vários containers em portas diferentes |
| **Operações não suportadas** | `501 Not Implemented` | Falha barulhenta em vez de resposta silenciosa e errada. É a decisão de projeto que torna o emulador confiável |

O anúncio é preciso nesse último ponto: *para as operações que suporta, o AWS Emulator devolve o mesmo resultado da AWS em chamadas válidas e os mesmos erros em chamadas inválidas*. Todo o resto responde `501`. A nuance importa — significa que "não implementado" é um sinal distinto, que você pode capturar, e não um resultado vazio que você confunde com comportamento real.

## Gerado a partir dos API models, não de mocks escritos à mão

Aqui está o que separa o AWS Emulator de uma pilha de projetos "mock AWS". Os serviços são gerados a partir dos **API models que a AWS publica, os mesmos por trás dos SDKs**. Quando a AWS adiciona um serviço ou uma API, ele aparece no emulador; o comportamento por trás é preenchido e verificado release a release.

É um trade-off de engenharia honesto, e vem com uma pergunta igualmente honesta: quão perto é perto o suficiente? A AWS publica um [relatório de fidelidade do AWS Emulator](https://docs.aws.amazon.com/emulator/latest/userguide/fidelity.html) comparando suas respostas com as do serviço real. Leia antes de decidir que um teste passando localmente significa alguma coisa em produção — a fidelidade é por operação, não por serviço.

O emulador **não tem custo adicional de serviço**, não é amarrado a uma Region da AWS e seu código é publicado sob a **CC0 1.0 Universal**, domínio público. Você paga por recursos AWS só quando faz deploy na AWS.

## Começando com Docker Compose

O [guia oficial de introdução com Docker](https://docs.aws.amazon.com/emulator/latest/userguide/getting-started-docker.html) é a fonte de verdade. Eu embrulhei esse guia num repositório público pequeno — [eftechcombr/aws-emulator](https://github.com/eftechcombr/aws-emulator) — com `Dockerfile`, `docker-compose.yaml` e a configuração de cliente, então tudo virou um comando:

```sh
mkdir -p ~/.aws/emulator
docker compose up -d
docker compose logs -f
curl --cacert ~/.aws/emulator/9297/ca.pem https://127.0.0.1:9297/__admin/health   # -> ok
docker compose down
```

Crie o diretório **antes** do primeiro `up`. No Linux, se o Docker criar por você, ele nasce com dono root e o seu SDK não consegue ler os arquivos gerados — uma falha com cara de problema de credencial que não é.

O que os dois arquivos fazem:

| Arquivo | Conteúdo |
| --- | --- |
| `Dockerfile` | `FROM public.ecr.aws/amazonlinux/amazonlinux:2023-minimal`, instala o RPM de `downloads.aws.com`, `USER 1000`, `HOME=/home/emulator`, `EXPOSE 9297`, `ENTRYPOINT ["aws-emulator", "-b", "0.0.0.0"]` |
| `docker-compose.yaml` | publica `127.0.0.1:${PORT:-9297}:${PORT:-9297}`, monta `${HOME}/.aws/emulator`, define `HOME`, `mem_limit`/`memswap_limit: 2g`, `command: ["-p", "${PORT:-9297}"]`, `stop_grace_period: 10s` |

A imagem é feita para **Arm64** (`aws-emulator-aarch64.rpm`). Em host Intel ou AMD, troque a linha `ADD` do `Dockerfile` por `aws-emulator-x86_64.rpm` antes do primeiro build.

O endpoint de health merece um comentário: `GET /__admin/health` responde na **mesma porta HTTPS da API**, com o mesmo certificado autoassinado. Não existe porta de admin em HTTP puro para ficar consultando, e é por isso que o `curl` acima precisa do `--cacert`.

## Os quatro arquivos que o emulador escreve

Na inicialização, o emulador escreve em `~/.aws/emulator/<porta>/` na sua máquina:

| Arquivo | Para que serve | Variável de ambiente |
| --- | --- | --- |
| `emulator_credentials` | Access key ID e secret desta execução | `AWS_SHARED_CREDENTIALS_FILE` |
| `config` | Arquivo de configuração do SDK | `AWS_CONFIG_FILE` |
| `ca.pem` | Certificado autoassinado | `AWS_CA_BUNDLE` |
| `truststore.p12` | O mesmo certificado como trust store PKCS12 sem senha, para Java | `JAVA_TOOL_OPTIONS` |

As chaves valem **só para a execução atual**, e o certificado é regenerado a cada start. Nunca faça commit desses arquivos; coloque `~/.aws/emulator/` na sua lista mental de coisas que não são código-fonte.

## Apontando o SDK para o emulador

macOS e Linux:

```sh
export AWS_ENDPOINT_URL=https://127.0.0.1:9297
export AWS_SHARED_CREDENTIALS_FILE=~/.aws/emulator/9297/emulator_credentials
export AWS_CONFIG_FILE=~/.aws/emulator/9297/config
export AWS_CA_BUNDLE=~/.aws/emulator/9297/ca.pem
export AWS_EC2_METADATA_DISABLED=true
export AWS_DISABLE_HOST_PREFIX_INJECTION=true
export AWS_REGION=us-east-1
export AWS_DEFAULT_REGION=us-east-1
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN AWS_PROFILE
```

Duas dessas linhas fazem trabalho defensivo, não trabalho de configuração:

- `AWS_EC2_METADATA_DISABLED=true` impede o SDK de pedir credenciais ao metadata service da instância. Numa EC2 de verdade esse pedido funciona — e o seu teste "local" passa a assinar com a role da instância sem avisar.
- O `unset` importa porque **variável de ambiente ganha do arquivo de credenciais**. Deixe chaves reais exportadas e o emulador rejeita suas requisições — ou, pior, seus testes vão parar na AWS de verdade.

Com as variáveis definidas **no mesmo shell ou script que roda os testes**, seu código não precisa de endpoint nem de credencial como argumento:

```python
import boto3

s3 = boto3.client("s3")
print(s3.list_buckets()["Buckets"])
```

> `AWS_CONFIG_FILE` **substitui** o seu próprio arquivo de config naquele shell — configurações de retry, de transferência do S3 e o que mais você guarda ali deixam de valer. O arquivo gerado é reescrito a cada start, então não o edite: copie, ajuste a cópia e aponte `AWS_CONFIG_FILE` para ela.

## Verifique antes de confiar no resultado

Um comando diz se a ligação funcionou:

```sh
aws sts get-caller-identity
```

Saída esperada: `Account` = `000000000000` e `Arn` = `arn:aws:iam::000000000000:user/emulator`. Se aparecer o seu account ID real, as requisições ainda estão indo para a AWS e todo teste verde depois disso é mentira. Rode essa checagem no topo do script de teste, antes das asserções.

## As armadilhas que custam uma tarde

### Use `127.0.0.1`, não `localhost`

Com `localhost` na URL do endpoint, os SDKs de JavaScript, Java e Go passam a fazer requisições S3 no estilo **virtual-hosted** — o nome do bucket vai para o host — e o emulador rejeita. O IP mantém o bucket no path da requisição, que é o estilo que ele aceita.

### Injeção de host prefix

Alguns SDKs prependam `data-`, `sync-`, `stream-` e afins em operações específicas (o `DiscoverInstances` do Cloud Map é o exemplo clássico), gerando um host como `data-127.0.0.1` que nunca chega ao emulador.

| Cliente | Como desligar |
| --- | --- |
| AWS CLI / Boto3 | `AWS_DISABLE_HOST_PREFIX_INJECTION=true` (no Boto3 também: `Config(inject_host_prefix=False)`) |
| JavaScript v3 | `disableHostPrefix: true` no cliente |
| Java 2.x | `SdkAdvancedClientOption.DISABLE_HOST_PREFIX_INJECTION` |

Defina isso **só** no shell do emulador. Contra a AWS real, operações que exigem host prefix falham enquanto a variável estiver ligada.

### O certificado é por SDK

Autoassinado, e regenerado a **cada start**. `AWS_CA_BUNDLE` resolve para alguns clientes; outros precisam de ajuste próprio:

| Cliente | Configuração |
| --- | --- |
| AWS CLI / Boto3 / Go v2 | `AWS_CA_BUNDLE` |
| JavaScript v3 (Node.js) | `NODE_EXTRA_CA_CERTS=~/.aws/emulator/9297/ca.pem` |
| Rust / .NET | `SSL_CERT_FILE=~/.aws/emulator/9297/ca.pem` |
| Java 2.x | o trust store PKCS12, abaixo |

Java não lê `ca.pem`; use o trust store PKCS12 gerado:

```sh
export JAVA_TOOL_OPTIONS="-Djavax.net.ssl.trustStore=$HOME/.aws/emulator/9297/truststore.p12 -Djavax.net.ssl.trustStoreType=PKCS12"
```

**Essas configurações substituem as raízes de confiança padrão** — com uma exceção: `NODE_EXTRA_CA_CERTS` soma às do Node. Resultado: qualquer outra chamada HTTPS no mesmo processo falha com `PKIX path building failed`, inclusive para a AWS real. Se um processo precisa falar com os dois, monte um bundle combinado com os certificados do sistema mais o `ca.pem` — e refaça depois de cada start do emulador.

### A porta está acoplada aos arquivos

O emulador grava a porta **dentro dos arquivos que gera**, então três coisas precisam concordar: a porta publicada, a opção `-p` e o diretório `~/.aws/emulator/<porta>`. Mude as três juntas, só pela variável `PORT`:

```sh
PORT=9300 docker compose up -d
curl -sf --cacert ~/.aws/emulator/9300/ca.pem https://127.0.0.1:9300/__admin/health
PORT=9300 docker compose down
```

Nunca mapeie `9300:9297`. Dois containers passariam a compartilhar `~/.aws/emulator/9297` e apagariam as credenciais e os certificados um do outro no meio da execução. Também não use `-p 0` dentro do container: o Docker não consegue encaminhar uma porta escolhida na inicialização.

### Duas requisições que nunca chegam

- **Amazon S3 Control** é inalcançável. O SDK sempre coloca o account ID no host (`000000000000.127.0.0.1`) e não existe opção para desligar isso. O S3 normal funciona.
- **Não existe endpoint por serviço.** Tudo é `https://127.0.0.1:<porta>`, o que é conveniente até você precisar que dois serviços se enxerguem em Regions diferentes.

## Notas de segurança

- **SigV4 é exigido por padrão**, exatamente como na AWS. O emulador valida assinatura em vez de confiar na rede.
- `--auth off` (`-a off`) desliga a checagem de assinatura e para de escrever `emulator_credentials`. Só para máquina confiável de um usuário — e leia antes [o que a própria AWS diz que você perde com isso](https://docs.aws.amazon.com/emulator/latest/userguide/security.html#security-what-you-do).
- **`mem_limit` e `memswap_limit` estão limitados a 2 GiB.** Passar disso mata o container com código de saída **137** — que parece OOM da sua suíte de testes e não é.
- **A porta é publicada só no loopback** (`127.0.0.1`), nunca em `0.0.0.0`. Mantenha assim: o container serve uma API que aceita conta fixa e, com auth off, nenhuma assinatura.

## Para que serve, e para que não serve

Serve: testes de integração que precisam de semântica real de API em vez de mock, jobs de CI que não deveriam carregar credenciais AWS, desenvolvimento offline no avião e agentes de código que precisam criar uma tabela, quebrá-la e consertar sem pagar o ciclo de um deploy.

Não serve: nada que dependa de estado sobrevivendo a um restart, comportamento entre Regions, S3 Control ou a fidelidade exata de uma operação cujo relatório você não abriu. Trate como um primeiro gate rápido e honesto — não como substituto de uma conta de staging antes de um release de produção.

A ordem que funciona: emulador no loop interno, AWS real no gate de release. O emulador pega os 80% que são o seu typo, o seu modelo de permissão faltando, o seu SDK mal configurado. Ele não vai pegar o que a AWS faz diferente, e não promete isso — `501` e um relatório de fidelidade publicado são os dois mecanismos que o mantêm honesto.

Na EF-TECH, construímos pipelines de CI e plataformas de cloud para times que preferem encontrar o erro no laptop e não em produção. [Fale conosco](/pt-br/contato/) se quiser encaixar emulação local no seu fluxo de entrega. Para mais artigos como este, visite nosso [blog](/pt-br/blog/).

## Links e Referências

- **AWS Emulator — anúncio no what's new (11 de novembro de 2026)** — [aws.amazon.com/about-aws/whats-new/2026/11/aws-emulator-now-available](https://aws.amazon.com/about-aws/whats-new/2026/11/aws-emulator-now-available/)
- **Página do produto AWS Emulator** — [aws.amazon.com/products/developer-tools/emulator](https://aws.amazon.com/products/developer-tools/emulator/)
- **Documentação do AWS Emulator** — [docs.aws.amazon.com/emulator](https://docs.aws.amazon.com/emulator)
- **O que é o AWS Emulator?** — [docs.aws.amazon.com/emulator/latest/userguide/what-is-service.html](https://docs.aws.amazon.com/emulator/latest/userguide/what-is-service.html)
- **Introdução com Docker** — [docs.aws.amazon.com/emulator/latest/userguide/getting-started-docker.html](https://docs.aws.amazon.com/emulator/latest/userguide/getting-started-docker.html)
- **Apontando seu SDK para o AWS Emulator** — [docs.aws.amazon.com/emulator/latest/userguide/point-sdk-to-emulator.html](https://docs.aws.amazon.com/emulator/latest/userguide/point-sdk-to-emulator.html)
- **Referência de comandos do AWS Emulator** — [docs.aws.amazon.com/emulator/latest/userguide/cli-reference.html](https://docs.aws.amazon.com/emulator/latest/userguide/cli-reference.html)
- **Relatório de fidelidade do AWS Emulator** — [docs.aws.amazon.com/emulator/latest/userguide/fidelity.html](https://docs.aws.amazon.com/emulator/latest/userguide/fidelity.html)
- **Segurança no AWS Emulator** — [docs.aws.amazon.com/emulator/latest/userguide/security.html](https://docs.aws.amazon.com/emulator/latest/userguide/security.html)
- **AWS Emulator no GitHub (CC0 1.0)** — [github.com/aws/aws-emulator](https://github.com/aws/aws-emulator)
- **Imagem Docker e setup com Compose (EF-TECH)** — [github.com/eftechcombr/aws-emulator](https://github.com/eftechcombr/aws-emulator)

### Origem das notas

Estas notas vêm do daily de **2026-11-12** (`daily/2026-11-12-Thu.md`) e da nota companheira `AWS-Emulator`, que registraram o anúncio de 11 de novembro de 2026 e o setup com Docker construído em cima dele. URLs originais:

- `https://aws.amazon.com/about-aws/whats-new/2026/11/aws-emulator-now-available/` — o post de what's new citado na abertura
- `https://aws.amazon.com/products/developer-tools/emulator/` — página do produto
- `https://docs.aws.amazon.com/emulator` — raiz da documentação
- `https://docs.aws.amazon.com/emulator/latest/userguide/fidelity.html` — relatório de fidelidade
- `https://docs.aws.amazon.com/emulator/latest/userguide/getting-started-docker.html` — quick start com Docker
- `https://docs.aws.amazon.com/emulator/latest/userguide/point-sdk-to-emulator.html` — variáveis de ambiente de SDK
- `https://docs.aws.amazon.com/emulator/latest/userguide/cli-reference.html` — referência de CLI e arquivos gerados
- `https://github.com/aws/aws-emulator` — repositório oficial
- `https://github.com/eftechcombr/aws-emulator` — repositório wrapper criado junto com essas notas
