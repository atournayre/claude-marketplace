---
allowed-tools:
  - SlashCommand
  - Write
  - Read
  - Glob
description: Crée un alias de commande qui délègue à une autre slash command
argument-hint: <alias> <commande>
model: claude-sonnet-4-5-20250929
---

# Générateur d'Alias de Slash Commands

Créer un alias de slash command qui délègue l'exécution à une autre commande existante via l'outil SlashCommand.

## Purpose
Permettre de créer des raccourcis (alias) vers des commandes existantes pour simplifier l'utilisation et éviter la duplication de code.

## Variables
- ALIAS: Nom de l'alias (format slash-command, ex: `/mon-alias`)
- TARGET_COMMAND: Commande cible à exécuter (format slash-command, ex: `/git:status`)

## Relevant Files
- `commands/` - Répertoire des commandes existantes
- `README.md` - Documentation du projet pour mise à jour

## Timing

### Début d'Exécution
**OBLIGATOIRE - PREMIÈRE ACTION** :
1. Exécuter `date` pour obtenir l'heure réelle
2. Afficher immédiatement : 🕐 **Démarrage** : [Résultat de la commande date]
3. Stocker le timestamp pour le calcul de durée

### Fin d'Exécution
**OBLIGATOIRE - DERNIÈRE ACTION** :
1. Exécuter `date` à nouveau pour obtenir l'heure de fin
2. Calculer la durée réelle entre début et fin
3. Afficher :
   - ✅ **Terminé** : [Résultat de la commande date]
   - ⏱️ **Durée** : [Durée calculée au format lisible]

### Formats
- Date : résultat brut de la commande `date` (incluant CEST/CET automatiquement)
- Durée :
  - Moins d'1 minute : `XXs` (ex: 45s)
  - Moins d'1 heure : `XXm XXs` (ex: 2m 30s)
  - Plus d'1 heure : `XXh XXm XXs` (ex: 1h 15m 30s)

### Instructions CRITIQUES
- TOUJOURS exécuter `date` via Bash - JAMAIS inventer/halluciner l'heure
- Le timestamp de début DOIT être obtenu en exécutant `date` immédiatement
- Le timestamp de fin DOIT être obtenu en exécutant `date` à la fin
- Calculer la durée en soustrayant les timestamps unix (utiliser `date +%s`)
- NE JAMAIS supposer ou deviner l'heure

## Workflow

### Étape 0: Initialisation du Timing (OBLIGATOIRE - PREMIÈRE ACTION)
```
🕐 Démarrage: [timestamp obtenu via `date`]
```
- Exécuter immédiatement `date` via Bash
- Stocker le timestamp de début pour calcul ultérieur

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
    - SlashCommand
  description: Alias vers [TARGET_COMMAND]
  argument-hint: [arguments de la commande cible]
  model: claude-haiku-4-5-20251001
  ---

  # [ALIAS]

  Alias vers `[TARGET_COMMAND]`.

  ## Usage
  Cette commande délègue directement à `[TARGET_COMMAND]`.

  ## Workflow
  - Exécuter la commande cible via SlashCommand
  ```

### Étape 3: Exécution de la Commande Cible
- Utiliser l'outil SlashCommand pour exécuter TARGET_COMMAND
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

---
✅ Terminé : [timestamp obtenu via `date`]

⏱️ Durée : [durée calculée]
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
