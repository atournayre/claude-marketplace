---
model: claude-sonnet-4-5-20250929
description: Charge la documentation depuis leurs sites web respectifs dans des fichiers markdown locaux que nos agents peuvent utiliser comme contexte.
allowed-tools: Task, WebFetch, Write, Edit, Bash (ls*), mcp_firecrawl-mcp_firecrawl_scrape
---

# Charger la Documentation Symfony

Charge la documentation depuis leurs sites web respectifs dans des fichiers markdown locaux que nos agents peuvent utiliser comme contexte.

## Variables

README_PATH: docs/symfony/README.md
DELETE_OLD_SYMFONY_DOCS_AFTER_HOURS: 24

## Gestion du Rate Limiting et Restrictions d'Accès

**IMPORTANT** : Les sites web de documentation peuvent implémenter des rate limiters ou restrictions d'accès qui limitent le nombre de requêtes par période de temps. Si tu rencontres des erreurs de type 429 (Too Many Requests), 401 (Unauthorized) ou des échecs de connexion :

1. Implémenter des délais entre les requêtes (pause de 2-3 secondes entre chaque URL)
2. Réduire le nombre de tâches parallèles si nécessaire
3. En cas d'échec, réessayer avec un délai exponentiel (attendre 5s, puis 10s, puis 20s, etc.)
4. Pour les erreurs 401 : tenter avec des user-agents différents ou signaler l'URL comme inaccessible
5. Noter les URLs qui échouent (rate limiting, accès refusé, etc.) dans le rapport final avec le type d'erreur

## Flux de Travail

1. Lire le fichier `README_PATH`

2. Vérifier si des fichiers docs/symfony/<nom-de-fichier>.md existent déjà

1. S'ils existent, vérifier s'ils ont été créés dans les dernières `DELETE_OLD_SYMFONY_DOCS_AFTER_HOURS` heures

2. Si c'est le cas, les ignorer - noter qu'ils ont été ignorés

3. Sinon, les supprimer et noter qu'ils ont été supprimés

3. Pour chaque URL dans `README_PATH` qui n'a pas été ignorée, utiliser l'outil Task en parallèle et suivre le `scrape_loop_prompt` comme prompt exact pour chaque Task

<scrape_loop_prompt>

Utiliser l'agent @symfony-docs-scraper en lui passant l'URL comme prompt

</scrape_loop_prompt>

4. Une fois toutes les tâches terminées, répondre selon le Format de Rapport

## Format de Rapport

```yaml
task: "Chargement de la documentation Symfony"
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
  documentation_files: "[nombre total de fichiers .md dans docs/symfony/]"
  total_size: "[taille totale en MB]"
  coverage: "[pourcentage de couverture des URLs]"
notes:
  - "Documentation Symfony disponible dans docs/symfony/ pour les agents"
  - "Fichiers individuels pour éviter les conflits"
  - "[autres notes importantes]"
```
