---
model: claude-sonnet-4-5-20250929
allowed-tools: Bash(mkdir:*), Bash(date:*), Write
description: Démarrer une nouvelle session de développement
---

# Démarrer une Session de Développement

Démarrer une nouvelle session de développement en créant un fichier de session dans `.claude/sessions/` avec le format `AAAA-MM-JJ-HHMM-$ARGUMENTS.md` (ou simplement `AAAA-MM-JJ-HHMM.md` si aucun nom n'est fourni).

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

- **IMPORTANT : Créer le répertoire `.claude/sessions/` s'il n'existe pas**
- **IMPORTANT : Une seule session peut être active à la fois**
- **IMPORTANT : Demander les objectifs à l'utilisateur s'ils ne sont pas clairement spécifiés**

## Structure du Fichier de Session

Le fichier de session doit commencer par :
1. Nom de la session et horodatage comme titre
2. Section d'aperçu de la session avec l'heure de début
3. Section des objectifs (demander à l'utilisateur si ce n'est pas clair)
4. Section de progression vide prête pour les mises à jour

## Processus

1. Créer le répertoire `.claude/sessions/` si nécessaire
2. Générer le nom du fichier de session avec l'horodatage actuel
3. Créer le fichier de session avec la structure appropriée
4. Mettre à jour `.claude/sessions/.current-session` pour suivre la session active
5. Confirmer le démarrage de la session et fournir des rappels pour les prochaines étapes

## Après la Création de la Session

Rappeler à l'utilisateur qu'il peut :
- La mettre à jour avec `session:update [notes]`
- La terminer avec `session:end`
- Vérifier le statut avec `session:current`

## Arguments de Session

$ARGUMENTS

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]