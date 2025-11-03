---
model: claude-sonnet-4-5-20250929
allowed-tools: Bash, Read
description: Charger un preset de contexte pour la session
argument-hint: <preset>
---

# Chargement Contexte

Charge un preset de contexte pour configurer la session selon le type de travail.

{{_templates/timing.md}}

## Presets Disponibles

- `default` - Contexte projet basique (structure + docs)
- `elegant-objects` - Règles conception Elegant Objects
- `ddd` - Principes Domain-Driven Design
- `full` - Tous les presets combinés

## Variables

- PRESET: Nom du preset (argument utilisateur)

## Validation

Si PRESET non supporté :
- Afficher liste presets disponibles
- Arrêter

## Workflows par Preset

### default
1. Exécuter `git ls-files`
2. Lire `docs/README.md`
3. Résumer compréhension projet

### elegant-objects
1. Charger règles Elegant Objects de Yegor Bugayenko
2. Appliquer à toute écriture/modification code
3. Confirmer activation

**Règles principales :**
- Classes `final`, 1-4 attributs max
- Objets immuables privilégiés
- Pas d'héritage implémentation
- Constructeurs : affectations uniquement
- Méthodes via interfaces
- Jamais retourner `null`
- Fail fast sur exceptions
- Pas de getters/setters
- Docblocks français UTF-8
- Tests : 1 assertion par test
- Pas de mocks, privilégier fakes

### ddd
1. Charger principes Domain-Driven Design
2. Structure : Entities, ValueObjects, Aggregates, Repositories, Services
3. Confirmer activation

**Principes :**
- Ubiquitous Language
- Bounded Contexts
- Aggregates avec invariants
- Repositories pour persistance
- Domain Events
- Séparation domaine/infra

### full
Charge tous les presets dans l'ordre : default → elegant-objects → ddd

## Rapport Format

```markdown
## 🎯 Contexte Chargé : [PRESET]

### Éléments Activés
- [Liste des règles/principes activés]

### Compréhension Projet
[Si preset=default ou full]
- Type projet : [description]
- Stack technique : [liste]
- Structure principale : [répertoires clés]

### Règles Appliquées
[Si preset=elegant-objects ou full]
- [Liste concise règles actives]

### Patterns DDD
[Si preset=ddd ou full]
- [Liste patterns disponibles]

```

## Exemples

```bash
/context:load default
/context:load elegant-objects
/context:load ddd
/context:load full
```

## Notes

- Presets cumulables manuellement : `/context:load default` puis `/context:load elegant-objects`
- `full` équivaut à tous les presets en une fois
- Contexte persiste pour toute la session
