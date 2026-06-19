# EF-TECH Website

Website oficial da EF-TECH — Solucoes em Cloud Computing.

## Stack

- **Hugo** v0.163.3 (Static Site Generator)
- **Blowfish** v2.103.0 (Theme, via git submodule)
- **Cloudflare Pages** (Hosting + GitOps deploy)

## Desenvolvimento Local

### Prerequisitos

- [Hugo](https://gohugo.io/installation/) v0.163.3+ (extended)
- Git

### Rodar localmente

```bash
git clone --recurse-submodules https://github.com/eftechcombr/www.git
cd www
hugo server -D
```

Acesse `http://localhost:1313/`

### Build de producao

```bash
hugo --gc --minify
```

Output em `public/`.

## Estrutura

```
www/
├── config/_default/       # Configuracao Hugo + Blowfish (PT-BR)
├── content/pt-br/         # Conteudo em Portugues
│   ├── _index.md          # Landing page
│   ├── servicos/          # Paginas de servicos
│   ├── sobre.md           # Sobre a EF-TECH
│   ├── blog/              # Blog
│   └── contato.md         # Contato
├── static/img/            # Imagens estaticas (logo)
├── assets/img/            # Imagens para processamento Hugo
├── themes/blowfish/       # Theme (git submodule)
└── .github/workflows/     # CI: build check + link checker
```

## Deploy (GitOps)

1. Push para `main` branch
2. Cloudflare Pages detecta o push via webhook
3. Build: `hugo --gc --minify`
4. Deploy automatico para `www.eftech.com.br`

### Configuracao Cloudflare Pages

| Setting | Value |
|---|---|
| Framework preset | Hugo |
| Build command | `hugo --gc --minify` |
| Output directory | `public` |
| Env var | `HUGO_VERSION=0.163.3` |
| Production branch | `main` |

## Atualizando o Theme

```bash
git submodule update --remote themes/blowfish
git add themes/blowfish
git commit -m "chore: update blowfish theme"
```
