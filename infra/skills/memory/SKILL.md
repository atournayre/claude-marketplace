---
name: infra:memory
description: Crée et optimise les fichiers de mémoire Claude Code (CLAUDE.md ou .claude/rules/). Couvre la hiérarchie de fichiers, la structure du contenu, les règles path-scoped, les bonnes pratiques et les anti-patterns. Utiliser pour CLAUDE.md, .claude/rules/, nouveaux projets, ou améliorer la conscience contextuelle.
argument-hint: "[task description]"
model: sonnet
allowed-tools: [Read, Write, Edit, Glob, Bash, AskUserQuestion]
version: 1.0.0
license: MIT
---

# infra:memory

Maîtrise du système de mémoire Claude Code via CLAUDE.md ou `.claude/rules/`.

## Décision initiale obligatoire

**TOUJOURS DEMANDER EN PREMIER : Stratégie de stockage**

Avant de créer ou modifier des fichiers mémoire, demander via AskUserQuestion :

- **Option 1 : CLAUDE.md unique** — Toutes les instructions dans un fichier (plus simple, petits projets)
- **Option 2 : .claude/rules/ modulaire** — Fichiers séparés par thème avec path-scoping optionnel (grands projets)

Guide de décision :
- CLAUDE.md si : < 100 lignes d'instructions, projet simple, règles universelles
- .claude/rules/ si : 100+ lignes, plusieurs types de fichiers, équipe maintient différentes zones

## Hiérarchie de chargement

| Priorité | Emplacement | Portée |
|----------|-------------|--------|
| 1 (haute) | CLAUDE.md projet | Équipe via git |
| 1 | .claude/rules/*.md | Équipe via git |
| 2 | ~/.claude/CLAUDE.md | Tous tes projets |
| 3 (basse) | CLAUDE.local.md | Toi seul |

## Structure du contenu (WHAT-WHY-HOW)

- **WHAT** : Stack technique, architecture du projet
- **WHY** : Décisions architecturales, pourquoi les patterns existent
- **HOW** : Commandes, tests, git workflow, étapes de vérification

## Path-scoping (.claude/rules/)

```yaml
---
paths:
  - "src/api/**/*.ts"
---
# Règles API
```

## Emphase pour règles critiques

| Mot-clé | Usage |
|---------|-------|
| **CRITICAL** | Règles non-négociables |
| **NEVER** | Prohibitions absolues |
| **ALWAYS** | Comportements obligatoires |
| **IMPORTANT** | Guidance significative |

## Limites de taille

- Idéal : 100-200 lignes maximum
- Max pratique : 300 lignes avant de découper
- Au-delà : déplacer les détails vers des fichiers séparés et lier

## Anti-patterns à éviter

- Règles de style de code (utiliser des linters)
- Secrets / API keys (JAMAIS)
- Trop de contenu (lier vers des docs externes)
- Instructions vagues ("formater correctement" → "exécuter `pnpm lint`")

## Workflow de création

### Nouveau projet (CLAUDE.md)

1. Commencer avec le template minimal
2. Ajouter stack et commandes en premier
3. Ajouter conventions au fur et à mesure
4. Tester sur des tâches réelles

### Nouveau projet (.claude/rules/)

1. Créer `.claude/rules/`
2. Un fichier par thème : `general.md`, `testing.md`, `code-style.md`
3. Ajouter path-scoping selon les besoins
4. Tester dans différents contextes de fichiers

## Template minimal CLAUDE.md

```markdown
# Nom du projet

## Stack
- [Framework principal]
- [Bibliothèques clés]

## Commandes
- `{cmd}` - Démarrer le dev
- `{cmd}` - Lancer les tests

## Conventions
- [2-3 conventions critiques]
```
