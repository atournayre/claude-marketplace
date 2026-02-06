---
name: init-marketplace
description: Initialise le marketplace et vérifie toutes les dépendances nécessaires aux plugins
model: haiku
allowed-tools: [Bash, Read, Write, Glob, Grep]
version: 1.0.0
license: MIT
---

# Init Marketplace

Initialise le marketplace et vérifie toutes les dépendances système nécessaires aux plugins.

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

### Étape 1 : Vérifier les dépendances système

Exécuter les vérifications suivantes en parallèle avec Bash :

```bash
# Vérifier chaque dépendance
which git && echo "✅ git installé" || echo "❌ git manquant"
which gh && echo "✅ gh installé" || echo "❌ gh manquant"
which node && echo "✅ node installé" || echo "❌ node manquant"
which npm && echo "✅ npm installé" || echo "❌ npm manquant"
which bun && echo "✅ bun installé" || echo "❌ bun manquant"
which pnpm && echo "✅ pnpm installé" || echo "❌ pnpm manquant (optionnel)"
which ccusage && echo "✅ ccusage installé" || echo "❌ ccusage manquant (optionnel)"
which biome && echo "✅ biome installé" || echo "❌ biome manquant (optionnel)"
```

### Étape 2 : Afficher les versions

Pour chaque dépendance installée, afficher la version :

```bash
git --version
gh --version
node --version
npm --version
bun --version
pnpm --version 2>/dev/null || echo "pnpm non installé"
```

### Étape 3 : Analyser les plugins installés

Lire `.claude-plugin/marketplace.json` pour obtenir la liste des plugins.

Pour chaque plugin, vérifier si ses dépendances sont satisfaites en se basant sur la section "Dépendances par plugin" ci-dessous.

### Étape 4 : Générer le rapport

Créer un rapport structuré :

```
📦 Marketplace Claude Plugin - Rapport de dépendances

✅ Dépendances installées (X/Y)
- git v2.x.x
- gh v2.x.x
- node v20.x.x
- npm v10.x.x
- bun v1.3.8

❌ Dépendances manquantes (X/Y)
- biome (optionnel)

⚠️ Plugins affectés par les dépendances manquantes
- mlvn: Scripts de dev (biome manquant)

📊 Résumé par plugin
✅ git (1.10.2): Toutes les dépendances satisfaites
✅ github (1.3.1): Toutes les dépendances satisfaites
✅ mlvn (1.0.0): 100% fonctionnel (biome optionnel manquant)
...
```

### Étape 5 : Proposer l'installation des dépendances manquantes

Si des dépendances critiques manquent, afficher les commandes d'installation :

```bash
# Installer bun
curl -fsSL https://bun.sh/install | bash

# Installer gh (GitHub CLI)
# macOS
brew install gh
# Linux
sudo apt install gh  # ou yum, dnf selon la distro

# Installer biome
npm install -g @biomejs/biome
```

### Étape 6 : Installer les packages NPM des plugins

Pour chaque plugin nécessitant des packages NPM (comme mlvn), proposer :

```bash
# Plugin mlvn
cd mlvn/scripts
bun install
```

## Dépendances à vérifier

### Dépendances système de base
- `git` - Gestion de version (requis par: git, github, dev)
- `gh` - GitHub CLI (requis par: git, github)
- `node` - Runtime JavaScript (requis par: plusieurs plugins)
- `npm` - Package manager Node (requis par: plusieurs plugins)
- `bun` - Runtime JavaScript moderne (requis par: mlvn)

### Dépendances optionnelles
- `pnpm` - Package manager Node alternatif (optionnel)
- `ccusage` - Claude Code usage tracker (optionnel pour mlvn)
- `biome` - Linter/formatter (optionnel pour mlvn)

### Dépendances par plugin

<!-- AUTO-GENERATED: Ne pas modifier manuellement -->
<!-- Cette section est automatiquement mise à jour par la commande bump -->

#### Plugin: claude (v1.2.1)
**Dépendances critiques:** Aucune

#### Plugin: command (v1.0.0)
**Dépendances critiques:** Aucune

#### Plugin: customize (v1.0.0)
**Dépendances critiques:** Aucune

#### Plugin: dev (v2.4.1)
**Dépendances critiques:**
- `git` - Pour workflow de développement

#### Plugin: doc (v1.6.1)
**Dépendances critiques:** Aucune

#### Plugin: framework (v1.1.1)
**Dépendances critiques:**
- `php` >= 8.1 - Pour projets PHP
- `composer` >= 2.0 - Gestionnaire de dépendances PHP

#### Plugin: gemini (v1.4.1)
**Dépendances critiques:**
- `gcloud` - Google Cloud CLI (pour authentification Gemini API)

#### Plugin: git (v1.10.2)
**Dépendances critiques:**
- `git` - Commandes git
- `gh` - GitHub CLI pour PR

#### Plugin: github (v1.3.1)
**Dépendances critiques:**
- `gh` - GitHub CLI

#### Plugin: marketing (v1.2.1)
**Dépendances critiques:** Aucune

#### Plugin: mlvn (v1.0.0)
**Dépendances critiques:**
- `bun` >= 1.0.0 - Runtime pour scripts TypeScript et hooks de sécurité
- `node` >= 16.0.0 - Pour packages NPM

**Dépendances optionnelles:**
- `gh` - Pour skills git-create-pr, git-fix-pr-comments, git-merge
- `ccusage` - Pour statusline tracking
- `biome` - Pour lint/format des scripts

**Packages NPM requis:**
- @ai-sdk/anthropic@^3.0.6
- ai@^6.0.11
- picocolors@^1.1.1
- table@^6.9.0
- zod@^4.3.5
- @biomejs/biome@^2.3.2 (dev)
- @types/bun@latest (dev)
- typescript@^5.0.0 (peer)

**Fonctionnalités bloquées sans dépendances:**
- Sans Bun : Hook PreToolUse (sécurité), statusline, Ralph Loop, scripts
- Sans gh : Skills PR GitHub
- Sans ccusage : Tracking des coûts dans statusline

#### Plugin: notifications (v1.0.2)
**Dépendances critiques:** Aucune

#### Plugin: prompt (v1.3.0)
**Dépendances critiques:** Aucune

#### Plugin: qa (v1.3.1)
**Dépendances critiques:**
- `php` >= 8.1 - Pour PHPStan
- `composer` >= 2.0 - Pour dépendances PHP

**Dépendances optionnelles:**
- `phpstan` - Analyseur statique PHP

#### Plugin: review (v1.0.0)
**Dépendances critiques:**
- `git` - Pour analyse historique

#### Plugin: symfony (v1.3.1)
**Dépendances critiques:**
- `php` >= 8.1
- `composer` >= 2.0

**Dépendances optionnelles:**
- `symfony` CLI - Console Symfony officielle

<!-- END AUTO-GENERATED -->

## Sortie

Le rapport doit être formaté en markdown avec :
- ✅ Icônes pour succès
- ❌ Icônes pour échecs
- ⚠️ Icônes pour avertissements
- 📊 Sections claires
- 🔧 Commandes d'installation prêtes à copier-coller

## Notes

- Cette commande est mise à jour automatiquement par `/bump` quand un plugin ajoute de nouvelles dépendances
- Les sections AUTO-GENERATED ne doivent jamais être modifiées manuellement
- Utiliser cette commande avant d'installer ou mettre à jour des plugins
