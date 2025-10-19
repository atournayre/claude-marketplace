---
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Edit, Bash(git:*), Bash(date:*)
description: Terminer la session actuelle avec un résumé complet
---

# Terminer la Session de Développement

Terminer la session de développement actuelle en créant un résumé complet et en effaçant le marqueur de session active.

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

- **IMPORTANT : Créer un résumé de session complet pour référence future**
- **IMPORTANT : Inclure les statistiques git et les changements effectués**
- **IMPORTANT : Documenter tous les accomplissements et apprentissages**

## Processus

### Étape 0: Initialisation du Timing (OBLIGATOIRE - PREMIÈRE ACTION)
```
🕐 Démarrage: [timestamp Europe/Paris avec CEST/CET]
```
- Cette étape DOIT être la toute première action
- Enregistrer le timestamp pour calcul ultérieur

1. Vérifier `.claude/sessions/.current-session` pour la session active
2. Si aucune session active :
   - Informer l'utilisateur qu'il n'y a rien à terminer
   - Suggérer de consulter les sessions passées avec `session:list`
3. Si la session existe, ajouter un résumé complet incluant :

### Composants du Résumé de Session

**Durée & Chronologie :**
- Heures de début et de fin de la session
- Durée totale de travail

**Résumé Git :**
- Total des fichiers modifiés (ajoutés/modifiés/supprimés)
- Lister tous les fichiers modifiés avec le type de changement
- Nombre de commits effectués pendant la session
- Statut git final

**Résumé des Todos & Progression :**
- Total des tâches complétées vs restantes
- Lister toutes les tâches complétées
- Lister les tâches incomplètes avec leur statut actuel

**Accomplissements Principaux :**
- Toutes les fonctionnalités implémentées
- Problèmes résolus
- Améliorations du code effectuées

**Détails Techniques :**
- Dépendances ajoutées/supprimées
- Changements de configuration effectués
- Changements majeurs introduits
- Migrations de base de données ou changements de schéma

**Documentation & Déploiement :**
- Mises à jour du README ou de la documentation
- Étapes de déploiement effectuées
- Changements de configuration d'environnement

**Leçons Apprises :**
- Ce qui a bien fonctionné
- Ce qui n'a pas fonctionné comme prévu
- Conseils pour les futurs développeurs
- Domaines d'amélioration

**Travail Incomplet :**
- Ce qui n'a pas été terminé
- Blocages rencontrés
- Prochaines étapes recommandées

4. Vider le fichier `.claude/sessions/.current-session` (vider le contenu, ne pas supprimer)
5. Confirmer que la documentation de session est complète

## Format du Résumé

Le résumé doit être suffisamment complet pour qu'un autre développeur (ou IA) puisse comprendre tout ce qui s'est passé sans lire toute la conversation de la session.

Créer un enregistrement permanent du travail de développement qui sert de documentation précieuse pour la continuité du projet.

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]