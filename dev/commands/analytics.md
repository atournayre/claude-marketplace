---
model: claude-sonnet-4-5-20250929
description: Execute claude-code-templates analytics and open in browser
---

# Analytics Dashboard

Lancer le tableau de bord d'analytics pour visualiser les statistiques d'utilisation de Claude Code.

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

- **IMPORTANT : Cette commande lance un serveur local sur le port 3333**
- **IMPORTANT : Le navigateur s'ouvre automatiquement après le démarrage du serveur**
- **IMPORTANT : Utiliser Ctrl+C pour arrêter le serveur quand terminé**

## Commandes

- Lancer le dashboard : !`(lsof -i :3333 > /dev/null 2>&1 && echo "⚠️ Port 3333 déjà utilisé. Arrêtez le processus existant avec la commande ci-dessous" || npx claude-code-templates@latest --analytics)`
- Lancer avec timeout (5min) : !`(lsof -i :3333 > /dev/null 2>&1 && echo "⚠️ Port 3333 déjà utilisé. Arrêtez le processus existant avec la commande ci-dessous" || timeout 300 npx claude-code-templates@latest --analytics)`
- Arrêter le serveur : !`(lsof -t -i:3333 > /dev/null 2>&1 && kill $(lsof -t -i:3333) && echo "✅ Serveur analytics arrêté") || echo "ℹ️ Aucun serveur analytics en cours"`

## Description

Cette commande :
1. Vérifie si le port 3333 est déjà utilisé
2. Si le port est occupé, affiche un message d'aide pour arrêter le processus
3. Sinon, lance l'outil d'analytics de claude-code-templates
4. Le navigateur s'ouvre automatiquement (géré par le serveur)

## Notes

- Le serveur reste actif jusqu'à interruption manuelle
- Les données d'analytics sont générées en temps réel
- Compatible avec les navigateurs modernes

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]