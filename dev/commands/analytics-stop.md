---
model: claude-haiku-4-5-20251001
description: Stop the running analytics dashboard server
---

# Stop Analytics Dashboard

Arrête proprement le serveur analytics dashboard s'il est en cours d'exécution.

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

## Commandes

- Arrêter le serveur : !`(lsof -t -i:3333 > /dev/null 2>&1 && kill $(lsof -t -i:3333) && echo "✅ Serveur analytics arrêté sur le port 3333") || echo "ℹ️ Aucun serveur analytics en cours d'exécution"`

## Description

Cette commande :
1. Vérifie si un processus écoute sur le port 3333
2. Si oui, termine le processus proprement
3. Affiche un message de confirmation
4. Si non, informe qu'aucun serveur n'est actif

## Utilisation

Utilisez `/analytics-stop` pour arrêter le dashboard analytics lancé avec `/analytics`.

## Notes

- Fonctionne même si le serveur a été lancé en arrière-plan
- Libère immédiatement le port 3333
- Aucun effet si aucun serveur n'est actif

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]