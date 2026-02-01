---
title: "doc"
description: "Documentation  - ADR, RTFM, génération docs, framework docs avec skills spécialisés"
version: "1.6.1"
---

# doc <Badge type="info" text="v1.6.1" />


Documentation : ADR, RTFM, génération docs, framework docs.

## Installation

```bash
/plugin install doc@atournayre
```

## Skills Disponibles

Le plugin doc fournit 4 skills (format natif Claude Code) :

### `/doc:adr`

Génère un Architecture Decision Record (ADR) formaté et structuré.

**Arguments :**
```bash
/doc:adr [titre]
```

**Exemples :**
```bash
/doc:adr "Choix architecture API"
/doc:adr "Migration vers PostgreSQL"
```

**Template ADR :**
```markdown
# ADR-001: [Titre]

Date: YYYY-MM-DD
Status: Proposed

## Context
[Contexte et problématique]

## Decision
[Décision prise]

## Consequences
### Positives
- [Avantage 1]

### Negatives
- [Inconvénient 1]

## Alternatives Considered
- [Alternative 1] - [Raison rejet]
```

**Sauvegarde :**
- `docs/adr/NNNN-titre.md`
- Numérotation automatique
- Index mis à jour

---

### `/doc:rtfm`

Lit la documentation technique - RTFM (Read The Fucking Manual).

**Arguments :**
```bash
/doc:rtfm [url|doc-name]
```

**Exemples :**
```bash
# Par URL
/doc:rtfm https://symfony.com/doc/current/security.html

# Par nom de doc locale
/doc:rtfm docs/symfony/security.md
```

**Workflow :**
1. Fetch URL ou lit fichier local
2. Parse documentation
3. Extrait sections pertinentes
4. Présente structuré

---

### `/doc:update`

Crée/met à jour la documentation pour la fonctionnalité en cours.

**Usage :**
```bash
/doc:update
```

**Workflow :**
1. Analyse modifications récentes (git diff)
2. Identifie fonctionnalités impactées
3. Génère/met à jour docs :
   - Docs techniques dans `docs/`
   - README global si nécessaire
4. Lie documents entre eux
5. Évite docs orphelines

**Structure générée :**
```
docs/
├── features/
│   ├── authentication.md
│   └── user-management.md
├── api/
│   └── endpoints.md
└── README.md (index)
```

**Contenu type :**
```markdown
# Feature: Authentication

## Overview
[Description]

## Usage
[Exemples code]

## API
[Endpoints]

## Configuration
[Config requise]

## See Also
- [user-management.md](user-management.md)
- [api/endpoints.md](../api/endpoints.md)
```

---

### `/doc:framework-load`

**🔹 Skill disponible : `doc-loader`**

Charge la documentation d'un framework depuis son site web dans des fichiers markdown locaux.

**Arguments :**
```bash
/doc:framework-load <framework-name> [version]
```

**Frameworks supportés :**
- `symfony` → Agent: `symfony-docs-scraper`
- `api-platform` → Agent: `api-platform-docs-scraper`
- `meilisearch` → Agent: `meilisearch-docs-scraper`
- `atournayre-framework` → Agent: `atournayre-framework-docs-scraper`
- `claude` → Agent: `claude-docs-scraper`

**Exemples :**
```bash
# Symfony version courante
/doc:framework-load symfony

# API Platform version spécifique
/doc:framework-load api-platform 3.2

# Meilisearch
/doc:framework-load meilisearch 1.5
```

**Fonctionnalités :**
- Cache intelligent 24h (ignore fichiers récents, supprime anciens)
- Délégation aux agents scraper spécialisés
- Support multi-version (argument optionnel)
- Anti-rate-limiting (délai 2s entre URLs)
- Stockage `docs/{framework}/[version]/`
- Disponible offline après chargement
- Statistiques détaillées (couverture, taille, fichiers)

**Workflow :**
1. Validation framework supporté
2. Lecture README avec liste URLs (`~/.claude/docs/<framework>/[version]/README.md`)
3. Gestion cache (skip/delete)
4. Pour chaque URL :
   - Délégation à agent scraper via Task tool
   - Sauvegarde markdown
   - Délai 2s anti-rate-limit
5. Rapport final (URLs traitées, fichiers créés, erreurs)

**Sauvegarde :**
```
docs/
├── symfony/
│   ├── 6.4/
│   │   ├── security.md
│   │   ├── routing.md
│   │   └── ...
│   └── latest/
│       └── ...
├── api-platform/
│   ├── 3.2/
│   │   └── ...
└── claude/
    ├── commands.md
    └── ...
```

---

### `/doc:framework-question`

Interroge la documentation locale d'un framework pour répondre à une question.

**Arguments :**
```bash
/doc:framework-question <framework-name> [version] <question>
```

**Exemples :**
```bash
/doc:framework-question symfony "Comment configurer la sécurité ?"
/doc:framework-question api-platform 3.2 "Créer une ressource API ?"
```

**Workflow :**
1. Cherche dans docs locales `docs/{framework}/`
2. Grep avec mots-clés
3. Parse sections pertinentes
4. Présente réponse structurée avec :
   - Explication
   - Code examples
   - Références fichiers sources

**Prérequis :**
- Documentation chargée via `/doc:framework-load`

## Workflow Documentation Complet

### ADR pour décision architecture

```bash
/doc:adr "Migration vers PostgreSQL"
# Éditer ADR généré
# Commit ADR
```

### Documenter nouvelle feature

```bash
# Après implémentation
/doc:update

# Génère docs automatiquement
# Lie avec docs existantes
```

### Apprendre framework

```bash
# 1. Charger docs
/doc:framework-load symfony

# 2. Poser questions
/doc:framework-question symfony "Comment créer un controller ?"

# 3. Travailler offline avec docs locales
```

### Lire doc externe

```bash
/doc:rtfm https://www.doctrine-project.org/projects/doctrine-orm/en/latest/reference/events.html
```

## Configuration

`.claude/settings.json` :
```json
{
  "doc": {
    "adr_path": "docs/adr",
    "auto_number": true,
    "frameworks": {
      "symfony": "https://symfony.com/doc/current",
      "api-platform": "https://api-platform.com/docs"
    }
  }
}
```

## Best Practices

**ADR :**
- 1 ADR par décision importante
- Status : Proposed → Accepted/Rejected
- Documenter alternatives

**Documentation code :**
- Mise à jour après chaque feature
- Exemples concrets
- Liens entre docs

**Framework docs :**
- Reload hebdomadaire pour updates
- Version spécifique pour prod
- Cache local pour perf

## Skills Disponibles

### `doc-loader`

**Localisation :** `skills/doc-loader/`

Skill générique pour le chargement de documentation de frameworks. Utilisé automatiquement par `/doc:framework-load`, `/symfony:doc:load`, et `/claude:doc:load`.

**Fonctionnalités :**
- Support multi-framework (5 frameworks)
- Support multi-version (optionnel)
- Gestion cache intelligent (24h)
- Délégation aux agents scraper spécialisés
- Anti-rate-limiting (délai 2s)
- Statistiques détaillées (couverture, taille)
- Gestion erreurs non bloquante

**Configuration :**
- `CACHE_HOURS`: 24h
- Délai entre URLs: 2s
- README requis: `~/.claude/docs/<framework>/[version]/README.md`

**Modèle :** sonnet-4.5

**Outils :** Task, WebFetch, Write, Edit, Bash, Read, Glob

## Licence

MIT
