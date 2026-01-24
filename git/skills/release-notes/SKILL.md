---
name: release-notes
description: >
  Génère des notes de release HTML orientées utilisateurs finaux.
  Transforme les commits techniques en descriptions accessibles sans jargon.
allowed-tools: [Bash, Read, Write, Grep, Glob, AskUserQuestion]
model: sonnet
---

# Release Notes Skill

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


## Usage
```
/git:release-notes <branche-source> <branche-cible> [nom-release]
```
Si arguments manquants : `AskUserQuestion` pour demander.

## Workflow

### Initialisation

**Créer les tâches du workflow :**

Utiliser `TaskCreate` pour chaque étape :

```
TaskCreate #1: Parser et valider arguments (branches source/cible)
TaskCreate #2: Collecter commits via git log
TaskCreate #3: Catégoriser par impact utilisateur
TaskCreate #4: Rédiger descriptions sans jargon
TaskCreate #5: Générer HTML dans .claude/reports/
```

**Important :**
- Utiliser `activeForm` (ex: "Validant les arguments", "Collectant les commits")
- Chaque tâche doit être marquée `in_progress` puis `completed`

**Pattern d'exécution pour chaque étape :**
1. `TaskUpdate` → tâche en `in_progress`
2. Exécuter l'étape
3. `TaskUpdate` → tâche en `completed`

### Étapes

1. Parser et valider arguments (branches source/cible)
2. Collecter commits via `git log`
3. Catégoriser par impact utilisateur
4. Rédiger descriptions sans jargon
5. Générer HTML dans `.claude/reports/`

## Catégories

| Catégorie | Icône | Mots-clés |
|-----------|-------|-----------|
| Nouveautés | ⭐ | feat, ✨, 🚀 |
| Améliorations | 📈 | improve, ⚡, perf |
| Corrections | ✅ | fix, 🐛 |
| Sécurité | 🔒 | security |

## Commits ignorés

- `refactor:`, `test:`, `chore:`, `ci:`, `docs:`, `style:`
- Commits de merge
- Mises à jour de dépendances

## Règles de rédaction

1. **ZÉRO jargon** - Pas de API, SQL, cache, endpoint, refactoring
2. **Bénéfice utilisateur** - "L'application est plus rapide" vs "Optimisation SQL"
3. **Verbes d'action** - Vous pouvez maintenant..., Nous avons corrigé...
4. **Phrases courtes** - Max 1-2 phrases par item

## Exemples

| Commit | Note utilisateur |
|--------|------------------|
| `feat: implémenter cache Redis` | L'affichage est plus rapide |
| `fix: corriger validation email` | Certaines adresses email sont maintenant acceptées |

## Output

`{REPORT_PATH}/release_notes_{RELEASE_NAME}.html`

## Task Management

**Progression du workflow :**
- 5 tâches créées à l'initialisation
- Chaque étape suit le pattern : `in_progress` → exécution → `completed`
- Utiliser `TaskList` pour voir la progression
- Les tâches permettent à l'utilisateur de suivre la génération des release notes

## References

- [Template HTML](references/html-template.html) - Structure et CSS du fichier généré
- [Règles de rédaction](references/writing-rules.md) - Exemples de transformation et conventions
