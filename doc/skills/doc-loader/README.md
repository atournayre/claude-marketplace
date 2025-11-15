# Documentation Loader Skill

Charge la documentation de frameworks depuis leurs sites web dans des fichiers markdown locaux.

## Fonctionnalités

- Support multi-framework (Symfony, API Platform, Meilisearch, atournayre-framework, Claude Code)
- Support multi-version (optionnel)
- Gestion cache intelligent (24h)
- Délégation aux agents scraper spécialisés
- Anti-rate-limiting (délai 2s entre requêtes)
- Statistiques détaillées (couverture, taille, fichiers)

## Usage

Via les commandes délégantes :
```bash
# Sans version (latest)
/doc:framework-load symfony
/symfony:doc:load
/claude:doc:load

# Avec version spécifique
/doc:framework-load symfony 6.4
/doc:framework-load api-platform 3.2
```

Ou directement via le skill :
```bash
# Utiliser l'outil Task avec le skill doc-loader
```

## Frameworks Supportés

| Framework            | Agent                             |
|----------------------|-----------------------------------|
| symfony              | symfony-docs-scraper              |
| api-platform         | api-platform-docs-scraper         |
| meilisearch          | meilisearch-docs-scraper          |
| atournayre-framework | atournayre-framework-docs-scraper |
| claude               | claude-docs-scraper               |

## Workflow

1. Parser arguments (framework + version optionnelle)
2. Valider framework supporté
3. Vérifier README avec liste URLs
4. Gérer cache (ignorer fichiers récents < 24h, supprimer anciens)
5. Pour chaque URL :
   - Déléguer à agent scraper spécialisé
   - Sauvegarder markdown
   - Délai 2s anti-rate-limit
6. Rapport final avec statistiques

## Structure Fichiers

```
docs/
  symfony/
    6.4/
      url1.md
      url2.md
      ...
  api-platform/
    3.2/
      url1.md
      ...
  claude/
    url1.md
    ...
```

## Configuration

- `CACHE_HOURS`: 24h (fichiers plus anciens supprimés)
- Délai entre URLs: 2s
- README requis: `~/.claude/docs/<framework>/[version]/README.md`

## Rapport Généré

```yaml
details:
  framework: "[nom]"
  version: "[version ou latest]"
  total_urls: [N]
  processed: [N]
  created: [N]
  errors: [N]
statistics:
  documentation_files: [N]
  total_size: "[MB]"
  coverage: "[%]"
```

## Notes

- Cache évite rechargements inutiles
- Gestion erreurs non bloquante (continue si URL échoue)
- Support version optionnel pour flexibilité
- Délègue scraping aux agents spécialisés
