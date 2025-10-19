---
model: claude-sonnet-4-5-20250929
allowed-tools: Bash(git ls-files:*), Read
description: Répondre aux questions sur la structure du projet et la documentation sans coder
---

# Question

Répondre à la question de l'utilisateur en analysant la structure du projet et la documentation. Cette invite est conçue pour fournir des informations et répondre aux questions sans apporter de modifications au code.

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

$ARGUMENTS

## Instructions

- **IMPORTANT : Il s'agit uniquement d'une tâche de réponse à des questions - NE PAS écrire, éditer ou créer de fichiers**
- **IMPORTANT : Se concentrer sur la compréhension et l'explication du code existant et de la structure du projet**
- **IMPORTANT : Fournir des réponses claires et informatives basées sur l'analyse du projet**
- **IMPORTANT : Si la question nécessite des modifications de code, expliquer ce qui devrait être fait conceptuellement sans implémenter**

## Workflow

- Examiner la structure du projet depuis !`git ls-files`
- Comprendre l'objectif du projet depuis le @docs/README.md
- Connecter la question aux parties pertinentes du projet
- Fournir des réponses complètes basées sur l'analyse

## Format de réponse

- Réponse directe à la question
- Preuves à l'appui de la structure du projet
- Références à la documentation pertinente
- Explications conceptuelles le cas échéant

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]
