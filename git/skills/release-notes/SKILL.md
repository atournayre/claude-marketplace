---
name: release-notes
description: >
  Génère des notes de release HTML orientées utilisateurs finaux.
  Transforme les commits techniques en descriptions accessibles sans jargon.
allowed-tools: [Bash, Read, Write, Grep, Glob, AskUserQuestion]
model: sonnet
---

# Release Notes Skill

## Usage
```
/git:release-notes <branche-source> <branche-cible> [nom-release]
```
Si arguments manquants : `AskUserQuestion` pour demander.

## Workflow

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

## References

- [Template HTML](references/html-template.html) - Structure et CSS du fichier généré
- [Règles de rédaction](references/writing-rules.md) - Exemples de transformation et conventions
