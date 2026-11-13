---
title: "AWS Emulator: Test Against AWS Without an Account or a Deployment"
description: "AWS released an official AWS Emulator on November 11, 2026: every service on a single local HTTPS endpoint, one fixed account, state in memory, and 501 for what it does not support yet. Here is the Docker Compose setup, the four files it generates, the SDK variables that make it work — and the six caveats that will cost you an afternoon."
summary: "The AWS Emulator runs the AWS API locally, signed with credentials it generates, so existing SDK and CLI calls come back in milliseconds with no account and no deployment. I walk through the Compose setup, the generated credentials/config/CA files, the environment variables per SDK, verification via `sts get-caller-identity`, and the honest limits: in-memory state, one Region per instance, S3 Control unreachable, host prefix injection, per-SDK trust stores, and the port coupling that surprises everyone."
date: 2026-11-12
draft: false
tags: ["aws", "testing", "docker", "local-development", "ci"]
categories: ["cloud-computing"]
featureimage: "/img/blog/aws-emulator-local-testing/cover.png"
featureimagecaption: "Every AWS service behind one local HTTPS port: the credentials, the certificate and the in-memory state all live on your machine — and disappear when the container stops."
---

On November 11, 2026, AWS announced the [AWS Emulator](https://aws.amazon.com/about-aws/whats-new/2026/11/aws-emulator-now-available/): a local implementation of the AWS API that your **existing SDK and CLI calls already know how to talk to**. Point them at `https://127.0.0.1:9297`, sign with the credentials the emulator generates, and calls come back in milliseconds. No AWS account. No deployment. No billing.

That last part is what makes it interesting for CI and for coding agents. A test suite that creates a DynamoDB table, writes items and reads them back does not need a sandbox account, a cleanup script, or a nightly budget. It needs a container and a few environment variables.

![A glass appliance on a desk serving every AWS service on one local HTTPS port, with the generated credentials and certificate kept on the machine](/img/blog/aws-emulator-local-testing/cover.png)

## The ground rules

Before any command, the operating model. These five decisions explain almost every surprise later:

| Rule | Value | Consequence |
| --- | --- | --- |
| **One endpoint** | `https://127.0.0.1:9297` (HTTPS only) | A single `AWS_ENDPOINT_URL` covers EC2, S3, IAM, Lambda and the rest. There is no per-service endpoint |
| **One account** | `000000000000` | No account IDs to invent, and no chance of hitting production by accident |
| **State in memory** | Lost on restart | No migrations to clean up — but no fixtures that survive a `docker compose down` either |
| **One Region per instance** | Whatever you export | To test multiple Regions, run multiple containers on different ports |
| **Unsupported operations** | `501 Not Implemented` | A loud failure instead of a silent, wrong answer. This is the design choice that makes it safe to trust |

The announcement is precise about that last line: *for the operations it supports, AWS Emulator returns the same result as AWS for valid calls and the same errors for invalid ones*. Everything else answers `501`. The nuance matters — it means "not implemented" is a distinct signal you can catch, not an empty result you might mistake for real behavior.

## Generated from the API models, not hand-written mocks

This is the part that separates the AWS Emulator from the pile of "mock AWS" projects. Its services are generated from the **API models AWS publishes, the same models behind the AWS SDKs**. When AWS adds a service or an API, it shows up in the emulator; the behavior behind it is filled in and verified release by release.

That is an honest engineering trade-off, and it comes with an honest question: how close is close enough? AWS publishes an [AWS Emulator fidelity report](https://docs.aws.amazon.com/emulator/latest/userguide/fidelity.html) that compares its responses against the real service. Read it before you decide a test passing locally means anything in production — fidelity is per operation, not per service.

The emulator carries **no additional service fee**, is not tied to an AWS Region, and its source is published under the **CC0 1.0 Universal** public domain dedication. You pay for AWS resources only when you deploy to AWS.

## Quick start with Docker Compose

The official [Docker getting-started guide](https://docs.aws.amazon.com/emulator/latest/userguide/getting-started-docker.html) is the source of truth. I wrapped it in a small public repo — [eftechcombr/aws-emulator](https://github.com/eftechcombr/aws-emulator) — with a `Dockerfile`, a `docker-compose.yaml` and the client configuration, so the whole thing is one command:

```sh
mkdir -p ~/.aws/emulator
docker compose up -d
docker compose logs -f
curl --cacert ~/.aws/emulator/9297/ca.pem https://127.0.0.1:9297/__admin/health   # -> ok
docker compose down
```

Create that directory **before** the first `up`. On Linux, if Docker creates it for you, it lands owned by root and your SDK cannot read the generated files — a failure that looks like a credentials problem and is not.

What the two files do:

| File | Contents |
| --- | --- |
| `Dockerfile` | `FROM public.ecr.aws/amazonlinux/amazonlinux:2023-minimal`, installs the RPM from `downloads.aws.com`, `USER 1000`, `HOME=/home/emulator`, `EXPOSE 9297`, `ENTRYPOINT ["aws-emulator", "-b", "0.0.0.0"]` |
| `docker-compose.yaml` | publishes `127.0.0.1:${PORT:-9297}:${PORT:-9297}`, mounts `${HOME}/.aws/emulator`, sets `HOME`, `mem_limit`/`memswap_limit: 2g`, `command: ["-p", "${PORT:-9297}"]`, `stop_grace_period: 10s` |

The image is built for **Arm64** (`aws-emulator-aarch64.rpm`). On an Intel or AMD host, change the `ADD` line in the `Dockerfile` to `aws-emulator-x86_64.rpm` before the first build.

The health endpoint deserves a note: `GET /__admin/health` answers on the **same HTTPS port as the API**, with the same self-signed certificate. There is no plain-HTTP admin port to poll, which is why the `curl` above needs `--cacert`.

## The four files the emulator writes

On startup, the emulator writes into `~/.aws/emulator/<port>/` on your host:

| File | Purpose | Environment variable |
| --- | --- | --- |
| `emulator_credentials` | Access key ID and secret for this run | `AWS_SHARED_CREDENTIALS_FILE` |
| `config` | AWS SDK config file | `AWS_CONFIG_FILE` |
| `ca.pem` | Self-signed certificate | `AWS_CA_BUNDLE` |
| `truststore.p12` | The same certificate as a passwordless PKCS12 store, for Java | `JAVA_TOOL_OPTIONS` |

The keys are valid **only for the current run**, and the certificate is regenerated on every start. Never commit these files; add `~/.aws/emulator/` to your mental list of things that are not source code.

## Pointing your SDK at it

macOS and Linux:

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

Two of those lines are doing defensive work, not configuration work:

- `AWS_EC2_METADATA_DISABLED=true` stops the SDK from asking the instance metadata service for credentials. On a real EC2 instance, that request succeeds — and your "local" test quietly signs with the instance role.
- The `unset` line matters because **environment variables beat the credentials file**. Leave real keys exported and the emulator rejects your requests, or worse, your tests reach real AWS.

With the variables set in **the same shell or script that runs the tests**, your code needs no endpoint or credential arguments at all:

```python
import boto3

s3 = boto3.client("s3")
print(s3.list_buckets()["Buckets"])
```

> `AWS_CONFIG_FILE` **replaces** your own config file for that shell — retry settings, S3 transfer settings and anything else you keep there stop applying. The generated file is rewritten on every start, so do not edit it: copy it, customize the copy, and point `AWS_CONFIG_FILE` at the copy.

## Verify before you trust the result

One command tells you whether the wiring worked:

```sh
aws sts get-caller-identity
```

Expected output: `Account` = `000000000000` and `Arn` = `arn:aws:iam::000000000000:user/emulator`. If you see your real account ID, requests are still going to AWS and every subsequent green test is a lie. Run this check at the top of your test script, before the assertions.

## The caveats that cost an afternoon

### Keep `127.0.0.1`, not `localhost`

With `localhost` in the endpoint URL, the JavaScript, Java and Go SDKs switch to **virtual-hosted-style S3 requests** — the bucket name goes into the host name — and the emulator rejects them. The IP address keeps the bucket in the request path, which is the style it accepts.

### Host prefix injection

Some SDKs prepend `data-`, `sync-`, `stream-` and similar prefixes for specific operations (Cloud Map `DiscoverInstances` is the classic example), producing a host like `data-127.0.0.1` that never reaches the emulator.

| Client | How to disable |
| --- | --- |
| AWS CLI / Boto3 | `AWS_DISABLE_HOST_PREFIX_INJECTION=true` (Boto3 also: `Config(inject_host_prefix=False)`) |
| JavaScript v3 | `disableHostPrefix: true` on the client |
| Java 2.x | `SdkAdvancedClientOption.DISABLE_HOST_PREFIX_INJECTION` |

Set this **only** in the emulator shell. Against real AWS, operations that require a host prefix will fail while it is set.

### The certificate is per SDK

Self-signed, and regenerated on **every start**. `AWS_CA_BUNDLE` covers some clients; others need their own setting:

| Client | Setting |
| --- | --- |
| AWS CLI / Boto3 / Go v2 | `AWS_CA_BUNDLE` |
| JavaScript v3 (Node.js) | `NODE_EXTRA_CA_CERTS=~/.aws/emulator/9297/ca.pem` |
| Rust / .NET | `SSL_CERT_FILE=~/.aws/emulator/9297/ca.pem` |
| Java 2.x | the PKCS12 store, below |

Java does not read `ca.pem`; use the generated passwordless trust store:

```sh
export JAVA_TOOL_OPTIONS="-Djavax.net.ssl.trustStore=$HOME/.aws/emulator/9297/truststore.p12 -Djavax.net.ssl.trustStoreType=PKCS12"
```

**These settings replace the default trust roots** — with one exception: `NODE_EXTRA_CA_CERTS` adds to Node's defaults. So any other HTTPS call in the same process fails with `PKIX path building failed`, including real AWS. If a process must reach both, build a combined bundle of your system certificates plus `ca.pem` — and rebuild it after every emulator start.

### The port is coupled to the files

The emulator writes its port **into the files it generates**, so three things must agree: the published port, the `-p` option, and the `~/.aws/emulator/<port>` directory. Change them together, through `PORT` only:

```sh
PORT=9300 docker compose up -d
curl -sf --cacert ~/.aws/emulator/9300/ca.pem https://127.0.0.1:9300/__admin/health
PORT=9300 docker compose down
```

Never map `9300:9297`. Two containers would then share `~/.aws/emulator/9297` and delete each other's credentials and certificates mid-run. Do not use `-p 0` inside a container either: Docker cannot forward a port chosen at startup.

### Two requests that never arrive

- **Amazon S3 Control** is unreachable. The SDK always puts the account ID in the host name (`000000000000.127.0.0.1`) and there is no switch to disable it. Regular S3 works normally.
- **Per-service endpoints do not exist.** Everything is `https://127.0.0.1:<port>`, which is convenient until you need two services to believe they are in different Regions.

## Security notes

- **SigV4 is required by default**, exactly like AWS. The emulator validates signatures rather than trusting the network.
- `--auth off` (`-a off`) disables signature checks and stops writing `emulator_credentials`. Only for a trusted single-user machine — and read the [AWS guidance on what that costs you](https://docs.aws.amazon.com/emulator/latest/userguide/security.html#security-what-you-do) first.
- **`mem_limit` and `memswap_limit` are capped at 2 GiB.** Exceeding it kills the container with exit code **137** — which reads like an OOM in your test suite and is not one.
- **The port is published on loopback only** (`127.0.0.1`), never `0.0.0.0`. Keep it that way: the container serves an API that accepts a fixed account and, with auth off, no signature at all.

## What it is good for, and what it is not

Good: integration tests that need real API semantics rather than mocks, CI jobs that should not hold AWS credentials, offline development on a plane, and coding agents that need to create a table, break it, and fix it without the round trip of a deploy.

Not good: anything that depends on state surviving a restart, cross-Region behavior, S3 Control, or the exact fidelity of an operation you have not opened the report for. Treat it as a fast, honest first gate — not as a replacement for a staging account before a production release.

The ordering that works: emulator in the inner loop, real AWS in the release gate. The emulator catches the 80% that is your typo, your missing permission model, your SDK misconfiguration. It will not catch what AWS does differently, and it does not claim to — `501` and a published fidelity report are the two mechanisms that keep it honest.

At EF-TECH, we build CI pipelines and cloud platforms for teams that would rather find the error on a laptop than in production. [Contact us](/en/contato/) if you want to wire local emulation into your delivery pipeline. For more articles like this, visit our [blog](/en/blog/).

## Links and References

- **AWS Emulator — what's new announcement (November 11, 2026)** — [aws.amazon.com/about-aws/whats-new/2026/11/aws-emulator-now-available](https://aws.amazon.com/about-aws/whats-new/2026/11/aws-emulator-now-available/)
- **AWS Emulator product page** — [aws.amazon.com/products/developer-tools/emulator](https://aws.amazon.com/products/developer-tools/emulator/)
- **AWS Emulator documentation** — [docs.aws.amazon.com/emulator](https://docs.aws.amazon.com/emulator)
- **What is AWS Emulator?** — [docs.aws.amazon.com/emulator/latest/userguide/what-is-service.html](https://docs.aws.amazon.com/emulator/latest/userguide/what-is-service.html)
- **Getting started with Docker** — [docs.aws.amazon.com/emulator/latest/userguide/getting-started-docker.html](https://docs.aws.amazon.com/emulator/latest/userguide/getting-started-docker.html)
- **Pointing your AWS SDK at AWS Emulator** — [docs.aws.amazon.com/emulator/latest/userguide/point-sdk-to-emulator.html](https://docs.aws.amazon.com/emulator/latest/userguide/point-sdk-to-emulator.html)
- **AWS Emulator command reference** — [docs.aws.amazon.com/emulator/latest/userguide/cli-reference.html](https://docs.aws.amazon.com/emulator/latest/userguide/cli-reference.html)
- **AWS Emulator fidelity report** — [docs.aws.amazon.com/emulator/latest/userguide/fidelity.html](https://docs.aws.amazon.com/emulator/latest/userguide/fidelity.html)
- **AWS Emulator security** — [docs.aws.amazon.com/emulator/latest/userguide/security.html](https://docs.aws.amazon.com/emulator/latest/userguide/security.html)
- **AWS Emulator on GitHub (CC0 1.0)** — [github.com/aws/aws-emulator](https://github.com/aws/aws-emulator)
- **Docker image and Compose setup (EF-TECH)** — [github.com/eftechcombr/aws-emulator](https://github.com/eftechcombr/aws-emulator)

### Where these notes came from

These notes come from the **2026-11-12** daily note (`daily/2026-11-12-Thu.md`) and the companion `AWS-Emulator` note, which documented the announcement from November 11, 2026 and the Docker setup built on top of it. Original URLs:

- `https://aws.amazon.com/about-aws/whats-new/2026/11/aws-emulator-now-available/` — the what's-new post quoted in the lead
- `https://aws.amazon.com/products/developer-tools/emulator/` — product page
- `https://docs.aws.amazon.com/emulator` — documentation root
- `https://docs.aws.amazon.com/emulator/latest/userguide/fidelity.html` — fidelity report
- `https://docs.aws.amazon.com/emulator/latest/userguide/getting-started-docker.html` — Docker quick start
- `https://docs.aws.amazon.com/emulator/latest/userguide/point-sdk-to-emulator.html` — SDK environment variables
- `https://docs.aws.amazon.com/emulator/latest/userguide/cli-reference.html` — CLI and generated-files reference
- `https://github.com/aws/aws-emulator` — official source repository
- `https://github.com/eftechcombr/aws-emulator` — wrapper repo created alongside those notes
