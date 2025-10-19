---
model: claude-haiku-4-5-20251001
allowed-tools: Read, Bash(date:*)
description: Afficher le statut et les détails de la session actuelle
---

# Statut de la Session Actuelle

Afficher le statut de la session actuelle en vérifiant l'existence d'une session active et en affichant les informations pertinentes.

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

- **IMPORTANT : Vérifier d'abord si `.claude/sessions/.current-session` existe**
- **IMPORTANT : Garder une sortie concise et informative**
- **IMPORTANT : Calculer la durée de la session avec précision**

## Processus

1. Vérifier si `.claude/sessions/.current-session` existe
2. Si aucune session active :
   - Informer l'utilisateur qu'il n'y a pas de session active
   - Suggérer d'en démarrer une avec `session:start [nom]`
3. Si une session active existe :
   - Afficher le nom et le fichier de la session
   - Calculer et afficher la durée depuis le début
   - Afficher les dernières mises à jour du fichier de session
   - Afficher les objectifs/tâches actuels si disponibles
   - Rappeler les commandes de session disponibles

## Informations à Afficher

- Nom du fichier et titre de la session
- Heure de début et durée
- Entrées de progression récentes
- Objectifs ou buts actuels
- Prochaines actions disponibles

## Rappel des Commandes Disponibles

- Mettre à jour : `session:update [notes]`
- Terminer : `session:end`
- Lister toutes : `session:list`

Garder la sortie propre et concentrée sur les informations exploitables.

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]