---
slug: getting-started
category: getting-started
generatedAt: 2026-06-19
---

# How do I set up and run this project?

## Getting Started

### Prerequisites

- [Hugo](https://gohugo.io/installation/) v0.163.3+ (extended edition)
- Git

### Installation

```bash
# Clone the repository with theme submodule
git clone --recurse-submodules https://github.com/eftechcombr/www.git
cd www

# If already cloned without submodules, initialise them
git submodule update --init --recursive
```

### Running

```bash
# Start local dev server with hot reload (includes drafts)
hugo server -D

# Visit http://localhost:1313/
```

### Production Build

```bash
hugo --gc --minify
# Output is in public/
```

### Update Theme

```bash
git submodule update --remote themes/blowfish
git add themes/blowfish
git commit -m "chore: update blowfish theme"
```
