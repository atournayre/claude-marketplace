---
model: claude-sonnet-4-5-20250929
description: Charge la documentation depuis leurs sites web respectifs dans des fichiers markdown locaux que nos agents peuvent utiliser comme contexte.
allowed-tools: Task, WebFetch, Write, Edit, Bash (ls*), mcp_firecrawl-mcp_firecrawl_scrape
---

# Charger la Documentation Atournayre Framework

Charge la documentation depuis leurs sites web respectifs dans des fichiers markdown locaux que nos agents peuvent utiliser comme contexte.

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

README_PATH: ~/.claude/docs/atournayre-framework/README.md
DELETE_OLD_ATOURNAYRE_FRAMEWORK_DOCS_AFTER_HOURS: 24

## Gestion du Rate Limiting et Restrictions d'Accès

**IMPORTANT** : Les sites web de documentation peuvent implémenter des rate limiters ou restrictions d'accès qui limitent le nombre de requêtes par période de temps. Si tu rencontres des erreurs de type 429 (Too Many Requests), 401 (Unauthorized) ou des échecs de connexion :

1. Implémenter des délais entre les requêtes (pause de 2-3 secondes entre chaque URL)
2. Réduire le nombre de tâches parallèles si nécessaire
3. En cas d'échec, réessayer avec un délai exponentiel (attendre 5s, puis 10s, puis 20s, etc.)
4. Pour les erreurs 401 : tenter avec des user-agents différents ou signaler l'URL comme inaccessible
5. Noter les URLs qui échouent (rate limiting, accès refusé, etc.) dans le rapport final avec le type d'erreur

## Flux de Travail

1. Lire le fichier `README_PATH`

2. Vérifier si des fichiers docs/atournayre-framework/<nom-de-fichier>.md existent déjà

1. S'ils existent, vérifier s'ils ont été créés dans les dernières `DELETE_OLD_ATOURNAYRE_FRAMEWORK_DOCS_AFTER_HOURS` heures

2. Si c'est le cas, les ignorer - noter qu'ils ont été ignorés

3. Sinon, les supprimer et noter qu'ils ont été supprimés

3. Pour chaque URL dans `README_PATH` qui n'a pas été ignorée, utiliser l'outil Task en parallèle et suivre le `scrape_loop_prompt` comme prompt exact pour chaque Task

<scrape_loop_prompt>

Utiliser l'agent @atournayre-framework-docs-scraper en lui passant l'URL comme prompt

</scrape_loop_prompt>

4. Une fois toutes les tâches terminées, répondre selon le Format de Rapport

## Format de Rapport

```yaml
task: "Chargement de la documentation Atournayre Framework"
status: "terminé"
details:
  total_urls: "[nombre total d'URLs dans README.md]"
  processed: "[nombre d'URLs traitées]"
  skipped: "[nombre d'URLs ignorées car récentes]"
  deleted: "[nombre de fichiers supprimés car anciens]"
  created: "[nombre de nouveaux fichiers créés]"
  errors: "[nombre d'erreurs]"
files:
  created:
    - path: "[chemin du fichier]"
      source: "[URL source]"
      size: "[taille en KB]"
  skipped:
    - path: "[chemin du fichier]"
      reason: "[raison - ex: 'créé il y a 2 heures']"
  deleted:
    - path: "[chemin du fichier]"
      reason: "[raison - ex: 'créé il y a 30 heures']"
  errors:
    - url: "[URL en erreur]"
      error: "[message d'erreur]"
statistics:
  documentation_files: "[nombre total de fichiers .md dans docs/atournayre-framework/]"
  total_size: "[taille totale en MB]"
  coverage: "[pourcentage de couverture des URLs]"
notes:
  - "Documentation Atournayre Framework disponible dans docs/atournayre-framework/ pour les agents"
  - "Fichiers individuels pour éviter les conflits"
  - "[autres notes importantes]"

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]
```
