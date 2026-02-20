---
name: infra:init
description: Initialise le marketplace et vérifie toutes les dépendances nécessaires aux plugins (git, gh, node, npm, bun). Génère un rapport avec les dépendances installées/manquantes et les commandes d'installation.
model: haiku
allowed-tools: [Bash, Read, Write, Glob, Grep]
version: 1.0.0
license: MIT
---

# infra:init

Initialisation du marketplace et vérification des dépendances système.

## Instructions à Exécuter

### Étape 1 : Vérifier les dépendances système

```bash
which git && echo "git OK" || echo "git MANQUANT"
which gh && echo "gh OK" || echo "gh MANQUANT"
which node && echo "node OK" || echo "node MANQUANT"
which npm && echo "npm OK" || echo "npm MANQUANT"
which bun && echo "bun OK" || echo "bun MANQUANT"
which pnpm && echo "pnpm OK" || echo "pnpm MANQUANT (optionnel)"
```

### Étape 2 : Afficher les versions

Pour chaque dépendance installée, afficher la version.

### Étape 3 : Analyser les plugins installés

Lire `.claude-plugin/marketplace.json` pour obtenir la liste des plugins.
Vérifier les dépendances de chaque plugin.

### Étape 4 : Générer le rapport

```
Marketplace Claude Plugin - Rapport de dépendances

Dépendances installées (X/Y)
  - git v2.x.x
  - gh v2.x.x
  - node v20.x.x

Dépendances manquantes (X/Y)
  - biome (optionnel)

Plugins affectés par les dépendances manquantes
  - plugin-name : raison

Résumé par plugin
  plugin1 : Toutes les dépendances satisfaites
  plugin2 : biome optionnel manquant
```

### Étape 5 : Proposer l'installation des dépendances manquantes

Si dépendances critiques manquent, afficher les commandes d'installation :

```bash
# bun
curl -fsSL https://bun.sh/install | bash

# gh (Linux)
sudo apt install gh

# biome
npm install -g @biomejs/biome
```

### Étape 6 : Installer les packages NPM des plugins si nécessaire

Pour chaque plugin avec packages NPM requis, proposer :

```bash
cd {plugin}/scripts && bun install
```

## Dépendances système

- `git` - Gestion de version (requis : git, dev)
- `gh` - GitHub CLI (requis : git, github)
- `node` - Runtime JavaScript
- `npm` - Package manager Node
- `bun` - Runtime JavaScript moderne

**Optionnelles :**
- `pnpm` - Package manager Node alternatif
- `biome` - Linter/formatter

## Format de sortie

Rapport formaté avec :
- Icônes succès/erreur/avertissement
- Sections claires
- Commandes d'installation prêtes à copier
