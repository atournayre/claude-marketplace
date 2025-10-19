---
model: claude-haiku-4-5-20251001
description: Afficher l'aide pour les commandes de gestion de session
---

# Aide pour la Gestion de Session

Le système de session aide à documenter le travail de développement pour référence future.

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

## Commandes Disponibles :

- `session:start [nom]` - Démarrer une nouvelle session avec nom optionnel
- `session:update [notes]` - Ajouter des notes à la session actuelle
- `session:end` - Terminer la session avec un résumé complet
- `session:list` - Lister tous les fichiers de session
- `session:current` - Afficher le statut de la session actuelle
- `session:help` - Afficher cette aide

## Comment Ça Fonctionne :

1. Les sessions sont des fichiers markdown stockés dans `.claude/sessions/`
2. Les fichiers utilisent le format `AAAA-MM-JJ-HHMM-nom.md`
3. Une seule session peut être active à la fois
4. Les sessions suivent la progression, les problèmes, les solutions et les apprentissages

## Meilleures Pratiques :

- Démarrer une session lors du début d'un travail significatif
- Mettre à jour régulièrement avec les changements ou découvertes importantes
- Terminer avec un résumé complet pour référence future
- Revoir les sessions passées avant de commencer un travail similaire

## Exemple de Flux de Travail :

```
session:start refactorisation-auth
session:update Ajout de la restriction OAuth Google
session:update Correction du problème de Promise des params Next.js 15
session:end
```

Le système de gestion de session aide à maintenir la continuité entre les sessions de développement et sert de documentation précieuse pour les futurs développeurs.

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]