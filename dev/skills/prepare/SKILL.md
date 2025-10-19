---
name: prepare
description: Creates a concise engineering implementation plan based on user requirements and saves it to specs directory
allowed-tools: [Read, Write, Edit, Grep, Glob, MultiEdit]
model: claude-opus-4-1-20250805
---


# Quick Plan
Create a detailed implementation plan based on the user's requirements provided through the `USER_PROMPT` variable. Analyze the request, think through the implementation approach, and save a comprehensive specification document to `PLAN_OUTPUT_DIRECTORY/<name-of-plan>.md` that can be used as a blueprint for actual development work.

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
USER_PROMPT: $ARGUMENTS
PLAN_OUTPUT_DIRECTORY: `docs/specs/`

## Instructions
- Carefully user's requirements provided in the USER_PROMPT variable
- Think deeply about the best approach to implement the requested functionality or solve the problem
- Create a concise implementation plan that includes:
- Clear problem statement and objectives
- Technical approach and architecture decisions
- Step-by-step implementation guide
- Potential challenges and solutions
- Testing strategy
- Success criteria
- Generate a descriptive, kebab-case filename based on the main topic of the plan
- Save the complete implementation plan to `PLAN_OUTPUT_DIRECTORY/<descriptive-name>.md`
  - Ensure the plan is detailed enough that another developer could follow it to implement the solution
  - Include code examples or pseudo-code where appropriate to clarify complex concepts
- Consider edge cases, error handling, and scalability concerns
  - Structure the document with clear sections and proper markdown formatting

## Workflow

### Étape 0: Initialisation du Timing (OBLIGATOIRE - PREMIÈRE ACTION)
```
🕐 Démarrage: [timestamp Europe/Paris avec CEST/CET]
```
- Cette étape DOIT être la toute première action
- Enregistrer le timestamp pour calcul ultérieur

1. Analyze Requirements - THINK HARD and parse the USER_PROMPT to understand the core problem and desired outcome
2. Design Solution - Develop technical approach including architecture decisions and implementation strategy
3. Document Plan - Structure a comprehensive markdown document with problem statement, implementation steps, and testing approach
4. Generate Filename - Create a descriptive kebab-case filename based on the plan's main topic
5. Save & Report - Write the plan to `PLAN_OUTPUT_DIRECTORY/<filename>.md` and provide a summary of key components

## Report

After creating and saving the implementation plan, provide a concise report with the following format:

```
✅ Implementation Plan Created

File: PLAN_OUTPUT_DIRECTORY/<filename>.md

Topic: <brief description of what the plan covers>

Key Comgonents:
- <main component 1>
- <main component 2>
- <main component 3>

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]
```
