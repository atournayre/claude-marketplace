---
title: Installation Détaillée
---

# Installation Détaillée

## Vue d'ensemble

Ce guide explique en détail comment installer et configurer les plugins du marketplace.

## Méthodes d'Installation

### Via le Marketplace (Recommandé)

```bash
# 1. Ajouter le marketplace
/plugin marketplace add atournayre/claude-marketplace

# 2. Lister les plugins disponibles
/plugin list

# 3. Installer un plugin
/plugin install git@atournayre
```

### Installation Manuelle

Tu peux aussi cloner directement le repository :

```bash
git clone https://github.com/atournayre/claude-marketplace.git ~/.claude/plugins/atournayre
```

Puis activer les plugins dans `.claude/settings.json`.

## Configuration Globale vs Projet

### Configuration Globale

Dans `~/.claude/settings.json` :

```json
{
  "plugins": {
    "git": { "enabled": true },
    "dev": { "enabled": true }
  }
}
```

S'applique à tous tes projets.

### Configuration Projet

Dans `<projet>/.claude/settings.json` :

```json
{
  "plugins": {
    "symfony": { "enabled": true }
  }
}
```

Surcharge la config globale pour ce projet.

## Dépendances

### Plugins avec Dépendances

| Plugin | Dépendances Recommandées |
|--------|-------------------------|
| dev | feature-dev, qa |
| framework | symfony |
| github | git |
| review | git, qa |

### Installation avec Dépendances

```bash
# Installer dev avec ses dépendances
/plugin install dev@atournayre feature-dev@atournayre qa@atournayre
```

## Vérification

### Tester les Commandes

Après installation, vérifie que les commandes sont reconnues :

```bash
# Test git plugin
/git:branch

# Test dev plugin
/dev:status

# Test symfony plugin
/symfony:make
```

### Lister les Plugins Installés

```bash
/plugin list --installed
```

### Vérifier les Versions

```bash
/plugin version git@atournayre
```

## Résolution de Problèmes

### Plugin Non Reconnu

Si une commande n'est pas reconnue :

1. Vérifie que le plugin est installé : `/plugin list --installed`
2. Redémarre Claude Code
3. Vérifie `.claude/settings.json`

### Conflits de Commandes

Si deux plugins ont la même commande :

```json
{
  "plugins": {
    "git": {
      "aliases": {
        "branch": "git:branch"
      }
    }
  }
}
```

### Problèmes de Permissions

Sur Linux/macOS :

```bash
chmod +x ~/.claude/plugins/atournayre/*/skills/*/SKILL.md
```

## Désinstallation

### Désinstaller un Plugin

```bash
/plugin uninstall git@atournayre
```

### Désactivation Temporaire

Dans `.claude/settings.json` :

```json
{
  "plugins": {
    "git": { "enabled": false }
  }
}
```

## Mise à Jour

### Mise à Jour Individuelle

```bash
/plugin update git@atournayre
```

### Mise à Jour Globale

```bash
/plugin update --all
```

### Vérifier les Mises à Jour

```bash
/plugin outdated
```

## Configuration Avancée

### Personnalisation des Skills

Certains plugins permettent de personnaliser les skills :

```json
{
  "plugins": {
    "dev": {
      "workflow": {
        "phases": ["discover", "explore", "design", "plan", "code", "review"]
      }
    }
  }
}
```

### Hooks

Configurer des hooks pour automatiser des actions :

```json
{
  "hooks": {
    "pre-commit": "/git:commit",
    "pre-push": "/qa:phpstan-resolver"
  }
}
```

## Prochaines Étapes

- [Voir tous les plugins](/plugins/)
- [Index des commandes](/commands/)
- [Comprendre l'architecture](/guide/workaround-slash-commands)
