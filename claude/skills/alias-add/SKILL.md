---
name: claude:alias:add
description: Crée un alias de commande qui délègue à une autre slash command
allowed-tools: [Skill, Write, Read, Glob]
argument-hint: <alias> <commande>
model: sonnet
version: 1.0.0
license: MIT
---

> ⚠️ **Déprécié** : Cette skill est remplacée par `infra:alias-add`. Voir le plugin `infra`. Sera supprimée en v3.0.

# Générateur d'Alias de Slash Commands

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


Créer un alias de slash command qui délègue l'exécution à une autre commande existante via l'outil Skill.

## Purpose
Permettre de créer des raccourcis (alias) vers des commandes existantes pour simplifier l'utilisation et éviter la duplication de code.

## Variables
- ALIAS: Nom de l'alias (format slash-command, ex: `/mon-alias`)
- TARGET_COMMAND: Commande cible à exécuter (format slash-command, ex: `/git:status`)

## Relevant Files
- `commands/` - Répertoire des commandes existantes
- `README.md` - Documentation du projet pour mise à jour

## Workflow

### Étape 1: Validation des Arguments
- Vérifier que 2 arguments ont été fournis (alias et commande cible)
- Valider le format de l'alias (doit commencer par `/`, format kebab-case)
- Valider le format de la commande cible (doit commencer par `/`)
- Vérifier que l'alias n'existe pas déjà (chercher dans `commands/`)
- Vérifier que la commande cible existe

### Étape 2: Création du Fichier d'Alias
- Créer le répertoire `commands/alias/` s'il n'existe pas
- Générer le fichier avec la structure suivante :
  ```markdown
  ---
  allowed-tools:
    - Skill
  description: Alias vers [TARGET_COMMAND]
  argument-hint: [arguments de la commande cible]
  model: haiku
  ---

  # [ALIAS]

  Alias vers `[TARGET_COMMAND]`.

  ## Usage
  Cette commande délègue directement à `[TARGET_COMMAND]`.

  ## Workflow
  - Exécuter la commande cible via Skill
  ```

### Étape 3: Exécution de la Commande Cible
- Utiliser l'outil Skill pour exécuter TARGET_COMMAND
- Transmettre tous les arguments supplémentaires à la commande cible

### Étape 4: Mise à Jour de la Documentation
- Ajouter l'alias dans la section "Commandes personnalisées" du README.md
- Inclure :
  - Nom de l'alias
  - Description
  - Commande cible
  - Usage

### Étape 5: Rapport Final
- Confirmer la création de l'alias
- Afficher le chemin du fichier créé
- Rappeler la commande cible
- Calculer et afficher la durée totale

## Report
```
✅ Alias créé avec succès

📁 Fichier : commands/alias/[nom-alias].md
🎯 Cible : [TARGET_COMMAND]
📝 Usage : /[alias] [arguments]
```

## Examples

### Créer un alias pour git:status
```bash
/alias:add status /git:status
```

### Créer un alias pour doc:update
```bash
/alias:add doc /doc:update
```

## Best Practices
- Noms d'alias courts et mémorisables
- Éviter les conflits avec les commandes existantes
- Documenter clairement la commande cible
- Utiliser Haiku pour les alias (simple délégation)
- Transmettre tous les arguments à la commande cible
