---
model: claude-sonnet-4-5-20250929
allowed-tools: Bash, WebFetch, WebSearch
argument-hint: [url|doc-name]
description: Lit la documentation technique - RTFM (Read The Fucking Manual)
---

# Documentation Reader - RTFM

## Purpose
Force Claude à lire et comprendre la documentation technique fournie, que ce soit via une URL directe ou en recherchant une documentation par nom.

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
DOC_SOURCE: L'URL ou le nom de la documentation à lire

## Instructions
- Si une URL est fournie directement, utilise WebFetch pour la lire
- Si un nom de documentation est fourni, utilise WebSearch pour la trouver puis WebFetch pour la lire
- Force Claude à lire complètement la documentation avant de répondre
- Fournis un résumé structuré des points clés

## Relevant Files
- Documentation externe via WebFetch/WebSearch

## Codebase Structure
Cette commande ne modifie pas le codebase, elle lit uniquement la documentation externe.

## Workflow

### Étape 0: Initialisation du Timing (OBLIGATOIRE - PREMIÈRE ACTION)
```
🕐 Démarrage: [timestamp Europe/Paris avec CEST/CET]
```
- Cette étape DOIT être la toute première action
- Enregistrer le timestamp pour calcul ultérieur

- Si DOC_SOURCE commence par http/https, utilise directement WebFetch
- Sinon, recherche la documentation avec WebSearch puis lis le résultat avec WebFetch
- Parse et structure l'information de la documentation
- Fournis un résumé concis et actionnable

## Expertise
- Lecture et analyse de documentation technique
- Extraction d'informations clés
- Synthèse et structuration de contenu

## Template
```
# Documentation: [NOM]

## Résumé
[Résumé concis en 2-3 phrases]

## Points clés
- Point important 1
- Point important 2
- Point important 3

## Exemples pratiques
[Exemples d'usage si disponibles]

## Liens utiles
[Références additionnelles si pertinentes]
```

## Examples
- `/rtfm https://docs.anthropic.com/claude/reference` - Lit directement la documentation Claude
- `/rtfm symfony doctrine` - Recherche et lit la documentation Symfony Doctrine
- `/rtfm php 8.3 new features` - Recherche les nouvelles fonctionnalités PHP 8.3

## Report
Résumé structuré de la documentation lue avec points clés et exemples pratiques.

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]
