---
model: claude-sonnet-4-5-20250929
description: Charge la documentation d'un framework depuis son site web dans des fichiers markdown locaux
allowed-tools: Task, WebFetch, Write, Edit, Bash (ls*), mcp_firecrawl-mcp_firecrawl_scrape
argument-hint: <framework-name> [version]
---

# Charger Documentation Framework

Charge la documentation d'un framework depuis son site web dans des fichiers markdown locaux.

{{_templates/timing.md}}

## Frameworks Supportés

- `symfony` - Documentation Symfony
- `api-platform` - Documentation API Platform
- `meilisearch` - Documentation Meilisearch
- `atournayre-framework` - Documentation atournayre-framework

## Variables

- FRAMEWORK: Nom du framework (1er argument)
- VERSION: Version du framework (2ème argument, optionnel)
- README_PATH: `~/.claude/docs/${FRAMEWORK}/${VERSION}/README.md` (ou `~/.claude/docs/${FRAMEWORK}/README.md` si pas de version)
- CACHE_HOURS: 24 (durée de validité du cache)
- AGENT_NAME: `${FRAMEWORK}-docs-scraper`
- DOCS_DIR: `docs/${FRAMEWORK}/${VERSION}/` (ou `docs/${FRAMEWORK}/` si pas de version)

## Validation

Si FRAMEWORK n'est pas dans la liste supportée :
- Afficher liste des frameworks disponibles
- Arrêter l'exécution

Si VERSION fournie :
- Vérifier que la version existe pour ce framework
- Si version inexistante : avertir et proposer versions disponibles ou latest

## Gestion du Rate Limiting

**IMPORTANT** : Les sites peuvent limiter les requêtes. En cas d'erreurs 429/401 :

1. Délai de 2-3s entre requêtes
2. Réduire parallélisme si nécessaire
3. Retry avec backoff exponentiel (5s, 10s, 20s)
4. Noter URLs en échec dans rapport final

## Workflow

1. Valider que FRAMEWORK est supporté
2. Parser arguments : framework + version optionnelle
3. Construire paths selon présence VERSION :
   - Avec version : `~/.claude/docs/${FRAMEWORK}/${VERSION}/`
   - Sans version : `~/.claude/docs/${FRAMEWORK}/`
4. Lire `README_PATH`
5. Vérifier fichiers existants dans `DOCS_DIR`
6. Si fichiers < CACHE_HOURS heures : ignorer
7. Si fichiers > CACHE_HOURS heures : supprimer
8. Pour chaque URL, lancer agent `@${AGENT_NAME}` en parallèle
9. Générer rapport final

## Format Rapport

```yaml
task: "Chargement documentation ${FRAMEWORK} [${VERSION}]"
status: "terminé"
details:
  framework: "[nom]"
  version: "[version ou 'latest']"
  total_urls: "[nombre]"
  processed: "[nombre]"
  skipped: "[nombre]"
  deleted: "[nombre]"
  created: "[nombre]"
  errors: "[nombre]"
files:
  created:
    - path: "[chemin]"
      source: "[URL]"
      size: "[KB]"
  skipped:
    - path: "[chemin]"
      reason: "[raison]"
  deleted:
    - path: "[chemin]"
      reason: "[raison]"
  errors:
    - url: "[URL]"
      error: "[message]"
statistics:
  documentation_files: "[nombre]"
  total_size: "[MB]"
  coverage: "[%]"
notes:
  - "Documentation ${FRAMEWORK} [version ${VERSION}] disponible"
```

## Exemples

```bash
# Sans version (latest par défaut)
/doc:framework:load symfony
/doc:framework:load api-platform

# Avec version spécifique
/doc:framework:load symfony 6.4
/doc:framework:load api-platform 3.2
/doc:framework:load meilisearch 1.5
```
