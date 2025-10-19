---
model: claude-sonnet-4-5-20250929
description: Code the codebase based on the plan
argument-hint: [path-to-plan]
allowed-tools: Read, Write, Bash
---

# Code
Follow the `Workflow` to implement the `PATH_TO_PLAN` then `Report` the completed work.

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
PATH_TO_PLAN: $ARGUMENTS

## Workflow

### Étape 0: Initialisation du Timing (OBLIGATOIRE - PREMIÈRE ACTION)
```
🕐 Démarrage: [timestamp Europe/Paris avec CEST/CET]
```
- Cette étape DOIT être la toute première action
- Enregistrer le timestamp pour calcul ultérieur

- If no `PATH_TO_PLAN` is provided, STOP immediately and ask the user to provide it.
- Read the plan at `PATH_TO_PLAN`. Think hard about the plan and implement it into the codebase.

## Quality Assurance
- Run all quality checks (linters, static analysis, tests)
- Fix ALL errors and warnings until all checks pass
- Ensure the code is error-free before considering the task complete
- DO NOT proceed to reporting until all quality checks are green

# Report
- Confirm all quality checks have passed
- Summarize the work you've just done in a concise bullet point list.
- Report the files and total lines changed with `git diff —-stat`

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]
