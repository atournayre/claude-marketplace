---
model: claude-sonnet-4-5-20250929
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob, Task]
description: "Corriger une issue GitHub avec workflow simplifié et efficace"
argument-hint: "[issue-number]"
---

# Correction d'Issue GitHub

## Purpose
Corriger une issue GitHub de manière structurée et efficace, en se concentrant sur l'essentiel.

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

## Variables
ISSUE_NUMBER: $1 (obligatoire)

## Instructions
- Utilise les outils Bash pour les opérations Git et GitHub CLI
- Focus sur la résolution rapide et efficace du problème
- Applique les standards du projet NEO

## Relevant Files
- Issues GitHub du repository
- Code source pertinent selon l'issue
- Documentation technique si nécessaire

## Workflow

### Étape 0: Initialisation du Timing (OBLIGATOIRE - PREMIÈRE ACTION)
```
🕐 Démarrage: [timestamp Europe/Paris avec CEST/CET]
```
- Cette étape DOIT être la toute première action
- Enregistrer le timestamp pour calcul ultérieur

### 1. Analyse de l'issue
- Récupérer les détails de l'issue via `gh issue view $ISSUE_NUMBER`
- Analyser le problème : type (bug, feature, enhancement), priorité, description
- Identifier les fichiers/modules concernés
- Vérifier les éventuels liens Sentry pour plus de contexte

### 2. Préparation de l'environnement
- Vérifier le statut git actuel
- S'assurer d'être sur la bonne branche de base (develop/main)
- Créer une branche de travail : `issue/$ISSUE_NUMBER-{description-courte}`
- Exemple : `issue/966-stockage-epuration-historique`

### 3. Investigation du code
- Localiser les fichiers concernés par l'issue
- Comprendre le code existant et identifier la cause du problème
- Analyser l'impact de la modification sur les autres parties du système
- Identifier les dépendances et side-effects potentiels

### 4. Implémentation de la solution
- Implémenter la correction en respectant :
  - Standards PHP 8.2+ avec typage strict
  - Conditions Yoda (`null === $value`)
  - Documentation des exceptions avec `@throws`
  - Conventions de nommage françaises
- Éviter les changements inutiles ou trop larges
- Maintenir la cohérence avec l'architecture existante

### 5. Validation et tests
- Exécuter les tests existants : `make run-unit-php`
- Ajouter des tests si nécessaire pour couvrir le nouveau code
- Vérifier avec PHPStan : ZÉRO erreur acceptée
- Tester la solution manuellement si applicable

### 6. Finalisation
- Informer l'utilisateur
- Ne pas faire de commit

## Report
- Issue analysée avec titre et type
- Branche créée avec nom approprié
- Fichiers modifiés avec résumé des changements
- Tests exécutés avec résultats

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]

## Validation
- ✅ `ISSUE_NUMBER` doit être fourni et exister sur GitHub
- ✅ Branche de travail créée avec convention de nommage
- ✅ Solution implémentée respectant les standards
- ✅ PHPStan passe sans erreur (CRITIQUE)
- ✅ Tests unitaires passent

## Expertise
Standards de qualité NEO :
- PHP 8.2+ avec typage strict obligatoire
- Conditions Yoda pour toutes les comparaisons
- Exceptions documentées avec `@throws`
- Nommage en français pour les concepts métier
- PHPStan niveau 9 sans erreur
- Tests unitaires pour nouveau code

## Examples
```bash
# Correction d'un bug
/github:fix 966

# Résultat attendu :
# 1. Analyse issue #966 "STOCKAGE - Épuration historique"
# 2. Création branche : issue/966-stockage-epuration-historique
# 3. Investigation du code de gestion des devis/alertes
# 4. Implémentation de l'épuration automatique
# 5. Tests et validation PHPStan
```
