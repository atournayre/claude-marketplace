---
description: Générer plan d'implémentation dans docs/specs/ (Phase 4)
model: claude-sonnet-4-5-20250929
allowed-tools: Write, Read, Glob
---

# Objectif

Phase 4 du workflow de développement : générer un plan d'implémentation détaillé basé sur l'architecture choisie.

# Instructions

## 1. Lire le contexte

- Lire `.claude/data/.dev-workflow-state.json` pour récupérer :
  - La feature description
  - Les décisions de clarification
  - L'architecture choisie
- Si phases précédentes non complétées, rediriger vers la phase manquante

## 2. Générer le plan

Créer le fichier `docs/specs/feature-{nom-kebab-case}.md` avec le contenu suivant :

```markdown
# Plan d'implémentation : {Feature Name}

## Résumé

**Feature :** {description}
**Approche :** {nom de l'approche choisie}
**Date :** {date du jour}

## Contexte

### Problème résolu
{description du problème}

### Décisions prises
- {décision 1}
- {décision 2}

## Architecture

### Composants
| Composant | Responsabilité | Fichier |
|-----------|---------------|---------|
| {nom} | {description} | `{chemin}` |

### Diagramme de flux
```
{représentation ASCII du flux}
```

## Plan d'implémentation

### Étape 1 : {titre}
- [ ] {tâche 1}
- [ ] {tâche 2}

**Fichiers :**
- `{chemin}` : {description}

### Étape 2 : {titre}
- [ ] {tâche 1}
- [ ] {tâche 2}

**Fichiers :**
- `{chemin}` : {description}

...

## Tests

### Tests unitaires
- [ ] {test 1}
- [ ] {test 2}

### Tests d'intégration
- [ ] {test 1}

## Risques et mitigations

| Risque | Probabilité | Impact | Mitigation |
|--------|------------|--------|------------|
| {risque} | {P} | {I} | {action} |

## Critères de succès

- [ ] {critère 1}
- [ ] {critère 2}
```

## 3. Créer le répertoire si nécessaire

```bash
mkdir -p docs/specs
```

## 4. Afficher le résumé

```
📝 Plan généré

Fichier : docs/specs/feature-{nom}.md

Étapes d'implémentation :
1. {étape 1}
2. {étape 2}
3. {étape 3}
...

Tests prévus : {nombre}
```

## 5. Mettre à jour le workflow state

```json
{
  "currentPhase": 4,
  "planPath": "docs/specs/feature-{nom}.md",
  "phases": {
    "4": {
      "status": "completed",
      "completedAt": "{timestamp}"
    }
  }
}
```

# Prochaine étape

```
✅ Plan généré : docs/specs/feature-{nom}.md

Prochaine étape : /dev:code docs/specs/feature-{nom}.md

⚠️ L'implémentation nécessite ton approbation explicite.
```

# Règles

- Le plan doit être **actionnable** (pas de descriptions vagues)
- Chaque étape doit avoir des **fichiers** et des **tâches** clairs
- Les tests doivent être **spécifiés** avant l'implémentation
- Respecter les **conventions du projet** (CLAUDE.md)
