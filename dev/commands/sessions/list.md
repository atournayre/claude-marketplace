---
model: claude-haiku-4-5-20251001
allowed-tools: Read, Bash(ls:*), Bash(find:*)
description: Lister toutes les sessions de développement
---

# Lister les Sessions de Développement

Afficher tous les fichiers de session avec les informations clés, triés par ordre chronologique inverse (plus récent en premier).

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

- **IMPORTANT : Vérifier si le répertoire `.claude/sessions/` existe**
- **IMPORTANT : Afficher les sessions par ordre chronologique inverse**
- **IMPORTANT : Mettre en évidence la session actuellement active**

## Processus

1. Vérifier si le répertoire `.claude/sessions/` existe
2. Si le répertoire n'existe pas :
   - Informer l'utilisateur qu'aucune session n'a encore été créée
   - Suggérer de démarrer la première session avec `session:start [nom]`
3. Si le répertoire existe :
   - Lister tous les fichiers `.md` de session (exclure les fichiers cachés et `.current-session`)
   - Pour chaque fichier de session, extraire et afficher :
     - Nom du fichier avec date/heure
     - Titre de la session depuis le contenu du fichier
     - Premières lignes de l'aperçu (si disponible)
     - Durée ou informations de statut
   - Mettre en évidence la session actuellement active (depuis le fichier `.current-session`)
   - Trier les sessions par ordre chronologique inverse (plus récent en premier)

## Format d'Affichage

```
Sessions trouvées dans .claude/sessions/ :

● [ACTIVE] 2024-01-15-1430-refactorisation-auth.md
  Titre : Refactorisation du Système d'Authentification
  Démarré : 15 jan 2024 à 14h30
  Aperçu : Modernisation du système d'auth avec OAuth2...

  2024-01-14-0900-corrections-bugs.md
  Titre : Corrections de Bugs Critiques
  Démarré : 14 jan 2024 à 9h00
  Statut : Terminé
  Aperçu : Correction des problèmes de traitement des paiements...
```

## Message Aucune Session

Si aucune session n'existe, fournir des conseils utiles :
- Aucune session trouvée
- Créer la première session avec `session:start [nom]`
- Utiliser `session:help` pour plus d'informations

Présenter les informations dans un format propre et lisible qui aide les utilisateurs à identifier rapidement les sessions pertinentes.

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]