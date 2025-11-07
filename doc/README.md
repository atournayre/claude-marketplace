# Plugin Doc

Documentation : ADR, RTFM, génération docs, framework docs.

## Installation

```bash
/plugin install doc@atournayre
```

## Commandes

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

Charge la documentation d'un framework depuis son site web dans des fichiers markdown locaux.

**Arguments :**
```bash
/doc:framework-load <framework-name> [version]
```

**Frameworks supportés :**
- `symfony`
- `api-platform`
- `doctrine`
- `phpunit`
- Custom (via configuration)

**Exemples :**
```bash
# Symfony version courante
/doc:framework-load symfony

# API Platform version spécifique
/doc:framework-load api-platform 3.2

# Doctrine ORM
/doc:framework-load doctrine
```

**Fonctionnalités :**
- Cache 24h
- Download depuis site officiel
- Stockage `docs/{framework}/`
- Disponible offline après chargement

**Sauvegarde :**
```
docs/
├── symfony/
│   ├── README.md
│   ├── security.md
│   ├── routing.md
│   └── ...
└── api-platform/
    ├── README.md
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

## Licence

MIT
