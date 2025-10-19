---
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Edit, Bash(git:*), Bash(date:*)
description: Ajouter une entrée de mise à jour à la session actuelle
---

# Mettre à Jour la Session Actuelle

Ajouter une mise à jour de progression à la session de développement active avec horodatage et contexte pertinent.

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

## Instructions

- **IMPORTANT : Vérifier si une session active existe dans `.claude/sessions/.current-session`**
- **IMPORTANT : Ajouter la mise à jour avec l'horodatage actuel**
- **IMPORTANT : Inclure automatiquement le résumé du statut git**

## Processus

1. Vérifier si la session actuelle existe
2. Si aucune session active :
   - Informer l'utilisateur qu'il n'y a pas de session active
   - Suggérer d'en démarrer une avec `session:start [nom]`
3. Si la session existe, ajouter la mise à jour avec :
   - Horodatage actuel
   - Résumé de la mise à jour (depuis les arguments)
   - Résumé du statut git (fichiers modifiés, staged, commits)
   - Progression de la liste des todos (si applicable)
   - Problèmes rencontrés et solutions
   - Résumé des changements de code

## Format de l'Entrée de Mise à Jour

```markdown
### Mise à jour - [HORODATAGE]

**Résumé :** [Détails de la mise à jour depuis les arguments]

**Changements Git :**
- Fichiers modifiés : [liste]
- Changements staged : [résumé]
- Commits récents : [si applicable]

**Progression :**
- [Accomplissements clés]
- [Problèmes résolus]
- [Prochaines étapes]

**Détails :**
[Contexte supplémentaire ou notes techniques]
```

## Notes de Mise à Jour

$ARGUMENTS

L'objectif est de créer des enregistrements complets mais concis pour référence future.

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]