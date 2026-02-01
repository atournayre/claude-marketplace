---
layout: home

hero:
  name: Claude Plugin Marketplace
  text: Plugins pour Claude Code
  tagline: Écosystème complet pour booster ton workflow
  image:
    src: /og-image.png
    alt: Claude Plugin Marketplace illustration
  actions:
    - theme: brand
      text: Démarrer
      link: /guide/getting-started
    - theme: alt
      text: Voir les plugins
      link: /plugins/

features:
  - icon: 🔧
    title: Git & Workflow
    details: Automatise branches, commits, PR
    link: /plugins/git

  - icon: ⚙️
    title: Développement
    details: Workflow 8 phases structuré
    link: /plugins/dev

  - icon: 🎯
    title: Framework Symfony
    details: Skills make et intégrations
    link: /plugins/symfony

  - icon: 📚
    title: Documentation
    details: Génération et gestion de docs
    link: /plugins/doc

  - icon: 🤖
    title: Intelligence Artificielle
    details: Intégration Gemini
    link: /plugins/gemini

  - icon: 🛠️
    title: Outils
    details: Personnalisation et tests
    link: /plugins/customize
---

<script setup>
import { data as plugins } from './.vitepress/data/plugins.data'
import { computed } from 'vue'

const totalSkills = computed(() =>
  plugins.reduce((sum, p) => sum + p.skillCount, 0)
)

const totalAgents = computed(() =>
  plugins.reduce((sum, p) => sum + p.agentCount, 0)
)

const totalHooks = computed(() =>
  plugins.reduce((sum, p) => sum + p.hookCount, 0)
)
</script>

## Installation rapide

```bash
# Ajouter le marketplace
/plugin marketplace add atournayre/claude-marketplace

# Installer un plugin
/plugin install git@atournayre
```

## Statistiques

- **{{ plugins.length }} plugins** disponibles
- **{{ totalSkills }} skills** pour automatiser ton workflow
- **{{ totalAgents }} agents** spécialisés
- **{{ totalHooks }} hooks** pour événements
- **Open Source** (MIT)

## Pourquoi ce marketplace ?

Ce marketplace centralise tous mes plugins Claude Code pour faciliter leur découverte et installation. Chaque plugin est conçu pour automatiser des tâches spécifiques du workflow de développement.

## Navigation

- [Tous les plugins](/plugins/) - Liste complète avec métadonnées
- [Par catégorie](/plugins/by-category) - Plugins organisés par domaine
- [Index des skills](/commands/) - Toutes les skills disponibles

## Composants du Marketplace

### 🎯 Skills
Les **skills** sont des prompts réutilisables invoqués via slash commands (`/git:commit`, `/dev:feature`, etc.). Elles automatisent des tâches spécifiques du workflow de développement.

### 🤖 Agents
Les **agents** sont des sous-processus spécialisés qui exécutent des tâches complexes de manière autonome (exploration de codebase, review de code, résolution d'erreurs, etc.).

### 🪝 Hooks
Les **hooks** sont des scripts déclenchés automatiquement lors d'événements (pre-commit, post-merge, file-save, etc.) pour automatiser ton workflow.

## Contribuer

Le marketplace est open source et les contributions sont les bienvenues !

- **Repository GitHub** : [atournayre/claude-marketplace](https://github.com/atournayre/claude-marketplace)
- **Issues** : Signaler un bug ou proposer une fonctionnalité
- **Pull Requests** : Contribuer du code ou de la documentation

### Développement local

```bash
git clone https://github.com/atournayre/claude-marketplace.git
cd claude-marketplace

# Installer et lancer la doc
cd docs
npm install
npm run dev
```
