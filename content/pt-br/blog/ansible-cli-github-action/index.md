---
title: "Ansible CLI GitHub Action — Execute Comandos Ansible no seu Pipeline CI/CD"
description: "A EF-TECH lança o ansible-cli-github-action, uma GitHub Action baseada em Docker que permite executar ansible, ansible-playbook, ansible-galaxy e outros comandos CLI diretamente nos seus workflows."
summary: "Conheça o ansible-cli-github-action — uma GitHub Action baseada na imagem python:3.11-slim que empacota Ansible, pywinrm e um ambiente shell completo para que você possa executar qualquer comando Ansible CLI (ansible, ansible-playbook, ansible-galaxy, etc.) diretamente nos seus workflows do GitHub Actions. Suporta Windows via WinRM, Linux via SSH e runners auto-hospedados."
date: 2026-07-29
draft: false
tags: ["ansible", "github-actions", "devops", "ci-cd", "automacao", "iac"]
categories: ["infraestrutura"]
featureimage: "img/blog/ansible-cli-github-action/cover.png"
featureimagecaption: "Ansible CLI GitHub Action — pré-visualização da interface do terminal"
---

A EF-TECH tem o prazer de anunciar o **ansible-cli-github-action**, uma GitHub Action leve que traz todo o poder do Ansible CLI para os seus workflows do GitHub Actions. Seja para executar playbooks, gerenciar roles do Galaxy ou rodar comandos ad-hoc, esta action cobre todas as necessidades.

![Ansible CLI GitHub Action](img/blog/ansible-cli-github-action/cover.png)

## O Que É?

A action é baseada na imagem Docker `python:3.11-slim` e já vem pré-configurada com:

- **Ansible** e todas as ferramentas CLI relacionadas (`ansible`, `ansible-playbook`, `ansible-galaxy`, `ansible-inventory`, etc.)
- **Suporte a pywinrm com CredSSP** — pronta para gerenciar hosts Windows via WinRM sem configuração adicional
- **Um ambiente shell completo** — você também pode executar comandos Linux padrão em qualquer etapa

Sem instalação adicional, sem ambientes virtuais Python, sem instalação de dependências. Basta apontar, configurar e executar.

## Como Usar

A action tem uma única entrada — `command` — que aceita qualquer comando Ansible ou shell que você queira executar.

```yaml
- uses: eftechcombr/ansible-cli-github-action@master
  with:
    command: "ansible-playbook site.yml -i inventory.yml"
```

## Exemplos Práticos

### 1. Verificação de Conectividade Windows via WinRM

Gerencie servidores Windows sem SSH. O pacote `pywinrm[credssp]` já está pré-instalado.

**Inventário (`inventory.ini`):**
```ini
[windows]
windows-server-01.example.com

[windows:vars]
ansible_connection=winrm
ansible_winrm_transport=ntlm
ansible_user=Administrator
ansible_password={{ windows_admin_password }}
ansible_winrm_server_cert_validation=ignore
```

**Workflow (`.github/workflows/windows-check.yml`):**
```yaml
name: Windows Connectivity Check

on:
  schedule:
    - cron: "0 6 * * *"
  workflow_dispatch:

jobs:
  winrm-ping:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Executar playbook WinRM ping
        uses: eftechcombr/ansible-cli-github-action@master
        with:
          command: >
            ansible-playbook win-ping.yml
            -i inventory.ini
            -e windows_admin_password=${{ secrets.WINDOWS_ADMIN_PASSWORD }}
```

### 2. Verificação de Conectividade Linux via SSH

Conecte-se a qualquer destino Linux usando SSH padrão.

**Inventário (`inventory.yml`):**
```yaml
all:
  hosts:
    web-01.example.com:
    web-02.example.com:
  vars:
    ansible_connection: ssh
    ansible_user: ubuntu
    ansible_ssh_private_key_file: /tmp/ssh_key
```

**Workflow com comando ad-hoc:**
```yaml
name: Linux Connectivity Check

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  ssh-ping:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Instalar chave SSH
        run: |
          mkdir -p /tmp
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > /tmp/ssh_key
          chmod 600 /tmp/ssh_key

      - name: Executar playbook
        uses: eftechcombr/ansible-cli-github-action@master
        with:
          command: >
            ansible-playbook ping.yml
            -i inventory.yml

      - name: Teste ad-hoc de ping
        uses: eftechcombr/ansible-cli-github-action@master
        with:
          command: ansible all -i inventory.yml -m ping
```

### 3. Acesso a Redes Internas via Runner Auto-Hospedado

Para destinos dentro de redes privadas, use um runner auto-hospedado. Como a action é baseada em Docker, o runner só precisa do Docker instalado — não precisa de Ansible ou Python.

```yaml
jobs:
  health-check:
    runs-on: [self-hosted, linux, production]
    steps:
      - uses: actions/checkout@v4

      - name: Executar playbook de health check
        uses: eftechcombr/ansible-cli-github-action@master
        with:
          command: >
            ansible-playbook health-check.yml
            -i inventory.yml
```

## Por Que Criamos Isso

Na EF-TECH, gerenciamos infraestrutura em ambientes Windows e Linux para nossos clientes. Precisávamos de uma forma simples e repetível de executar comandos Ansible dentro do GitHub Actions sem:

- Instalar Ansible e suas dependências em cada runner
- Gerenciar ambientes virtuais Python no CI
- Depurar inconsistências de ambiente entre execuções

O resultado é uma imagem Docker que encapsula tudo que o Ansible precisa — e uma GitHub Action que a envolve em uma única diretiva `uses:`.

## Testes

A imagem inclui uma suíte de testes smoke que você pode executar localmente:

```bash
tests/smoke_build.sh \
  && tests/smoke_ansible.sh \
  && tests/smoke_python.sh \
  && tests/smoke_shell.sh \
  && tests/smoke_playbook.sh
```

Esses testes verificam:
- Build da imagem Docker
- Versões das ferramentas Ansible CLI (`ansible`, `ansible-playbook`, `ansible-inventory`)
- Importação de dependências Python (`winrm`, `ansible`)
- Passagem de comandos shell e propagação de código de saída
- Verificação de sintaxe de playbooks e execução em localhost

## Comece Agora

A action é **open-source** sob licença MIT e está disponível no GitHub:

🔗 [https://github.com/eftechcombr/ansible-cli-github-action](https://github.com/eftechcombr/ansible-cli-github-action)

Para usar no seu projeto:

1. Adicione um arquivo de workflow em `.github/workflows/`
2. Faça checkout do repositório com `actions/checkout@v4`
3. Adicione um passo usando `eftechcombr/ansible-cli-github-action@master`
4. Defina a entrada `command` com o comando Ansible desejado

## Links Úteis

- [Repositório no GitHub](https://github.com/eftechcombr/ansible-cli-github-action)
- [Documentação do Ansible](https://docs.ansible.com/)
- [Documentação do GitHub Actions](https://docs.github.com/pt/actions)
- [Guia WinRM do Ansible para Windows](https://docs.ansible.com/ansible/latest/os_guide/windows_winrm.html)

---

Na **EF-TECH**, somos especialistas em cloud computing, automação de infraestrutura de TI e práticas DevOps. Oferecemos suporte especializado para Ansible, GitHub Actions e soluções de infraestrutura como código. [Entre em contato](/pt-br/contato/) para saber como podemos ajudar sua equipe.
