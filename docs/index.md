---
layout: home

hero:
  name: Claude Plugin Marketplace
  text: Plugins pour Claude Code
  tagline: 16 plugins, 69 commandes pour booster ton workflow
  image:
    src: /claude-marketplace/og-image.png
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
- **69 commandes** slash
- **Open Source** (MIT)

## Pourquoi ce marketplace ?

Ce marketplace centralise tous mes plugins Claude Code pour faciliter leur découverte et installation. Chaque plugin est conçu pour automatiser des tâches spécifiques du workflow de développement.

## Navigation

- [Tous les plugins](/plugins/) - Liste complète avec métadonnées
- [Par catégorie](/plugins/by-category) - Plugins organisés par domaine
- [Index des commandes](/commands/) - Les 69 slash commands disponibles

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
