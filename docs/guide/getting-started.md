---
title: Démarrage Rapide
---

# Démarrage Rapide

## Prérequis

- Claude Code installé
- Git configuré
- Node.js (pour certains plugins)

## Installation du Marketplace

```bash
/plugin marketplace add atournayre/claude-marketplace
```

Cette commande ajoute le marketplace à votre configuration Claude Code.

## Installer un Plugin

### Installation individuelle

```bash
/plugin install git@atournayre
/plugin install dev@atournayre
/plugin install symfony@atournayre
```

### Installation par batch

Pour installer plusieurs plugins d'un coup :

```bash
/plugin install git@atournayre dev@atournayre symfony@atournayre
```

## Vérifier l'Installation

Après installation, vérifie que les commandes sont disponibles :

```bash
/git:branch
# La commande doit être reconnue
```

## Configuration

Les plugins sont configurés via `.claude/settings.json` dans ton projet.

Exemple de configuration :

```json
{
  "plugins": {
    "git": {
      "enabled": true
    },
    "dev": {
      "enabled": true,
      "workflow": {
        "autoPhases": true
      }
    }
  }
}
```

## Dépendances entre Plugins

Certains plugins recommandent d'autres plugins :

- **dev** recommande **feature-dev** pour le workflow complet
- **framework** s'intègre avec **symfony**
- **qa** complète **dev** pour la qualité du code

## Prochaines Étapes

- [Voir tous les plugins](/plugins/) - Explore les 16 plugins disponibles
- [Index des commandes](/commands/) - Liste des 69 slash commands
- [Architecture](/guide/workaround-slash-commands) - Comprendre le système de commandes

## Aide et Support

Si tu rencontres un problème :

1. Vérifie la documentation du plugin spécifique
2. Consulte les issues GitHub
3. Ouvre une nouvelle issue si nécessaire

## Mise à Jour

Pour mettre à jour les plugins :

```bash
/plugin update git@atournayre
# ou
/plugin update --all
```
