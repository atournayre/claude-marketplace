---
model: claude-haiku-4-5-20251001
description: Automatise les mises à jour de version des plugins avec détection automatique du type de version
argument-hint: [plugin-name]
allowed-tools: Read, Edit, Bash, Glob, Grep, TodoWrite
---

# Bump Version Plugin

Mettre à jour la version d'un ou plusieurs plugins avec détection automatique du type de version.

## Arguments

```
/bump [plugin-name]
```

- `plugin-name` : Nom du plugin (optionnel, détecte automatiquement depuis git diff)

## Règles de versioning automatique

### MINOR (X.Y.0 → X.Y+1.0)
Nouveaux fichiers détectés :
- `agents/*.md` - Nouvel agent
- `commands/*.md` - Nouvelle commande
- `skills/*/` - Nouveau skill
- Nouveau plugin (répertoire non existant dans marketplace.json)

### PATCH (X.Y.Z → X.Y.Z+1)
- Modifications de fichiers existants
- Corrections de bugs
- Mises à jour de documentation
- Refactoring

### MAJOR (X.0.0 → X+1.0.0)
- Uniquement si explicitement demandé via `BREAKING:` dans les changements
- Ou si argument `--major` fourni

## Workflow

### Étape 1: Identifier les plugins modifiés

```bash
# Fichiers modifiés (stagés + non stagés)
MODIFIED=$(git diff --name-only HEAD)
STAGED=$(git diff --staged --name-only)
ALL_CHANGES=$(echo -e "$MODIFIED\n$STAGED" | sort -u | grep -v "^$")
echo "$ALL_CHANGES"
```

Extraire les noms de plugins uniques depuis les chemins (premier répertoire).
Ignorer : `.claude/`, fichiers à la racine (`README.md`, `CHANGELOG.md`).

### Étape 2: Pour chaque plugin, détecter le type de version

```bash
PLUGIN_CHANGES=$(echo "$ALL_CHANGES" | grep "^{plugin}/")
echo "$PLUGIN_CHANGES"
```

**Analyser les changements :**

```bash
# Nouveaux fichiers ?
NEW_FILES=$(git diff --staged --name-only --diff-filter=A | grep "^{plugin}/")
echo "Nouveaux fichiers: $NEW_FILES"

# Nouveaux agents ?
NEW_AGENTS=$(echo "$NEW_FILES" | grep "/agents/.*\.md$")

# Nouvelles commandes ?
NEW_COMMANDS=$(echo "$NEW_FILES" | grep "/commands/.*\.md$")

# Nouveaux skills ?
NEW_SKILLS=$(echo "$NEW_FILES" | grep "/skills/.*/")
```

**Déterminer le type :**
- SI `NEW_AGENTS` ou `NEW_COMMANDS` ou `NEW_SKILLS` non vides → **MINOR**
- SINON → **PATCH**

### Étape 3: Vérifier si nouveau plugin

```bash
grep -q "\"$PLUGIN\"" .claude-plugin/marketplace.json && echo "EXISTS" || echo "NEW"
```

SI nouveau plugin → **MINOR** (au minimum)

### Étape 4: Lire la version actuelle et calculer

```bash
CURRENT=$(cat {plugin}/.claude-plugin/plugin.json | grep '"version"' | sed 's/.*"\([0-9.]*\)".*/\1/')
echo "Version actuelle: $CURRENT"
```

**Calcul :**
- PATCH : `1.2.3` → `1.2.4`
- MINOR : `1.2.3` → `1.3.0`
- MAJOR : `1.2.3` → `2.0.0`

### Étape 5: Créer TodoWrite

Pour chaque plugin identifié :
- [ ] Bump version `{plugin}/.claude-plugin/plugin.json` (X.Y.Z → nouvelle)
- [ ] Mettre à jour `{plugin}/CHANGELOG.md`
- [ ] Mettre à jour `{plugin}/README.md` si nouvelles fonctionnalités
- [ ] Mettre à jour `README.md` global (tableau versions)
- [ ] Mettre à jour `CHANGELOG.md` global
- [ ] Mettre à jour `.claude-plugin/marketplace.json` si nouveau plugin

### Étape 6: Analyser les changements pour le CHANGELOG

Lire les fichiers modifiés pour comprendre ce qui a changé :
- Nouveaux agents ? → `### Added` + description agent
- Nouvelles commandes ? → `### Added` + description commande
- Nouveaux skills ? → `### Added` + description skill
- Modifications ? → `### Changed` + description
- Corrections ? → `### Fixed` + description
- Suppressions ? → `### Removed` + description

### Étape 7: Mettre à jour plugin.json

Éditer `{plugin}/.claude-plugin/plugin.json` :
```json
"version": "NOUVELLE_VERSION"
```

### Étape 8: Mettre à jour CHANGELOG du plugin

Ajouter en haut de `{plugin}/CHANGELOG.md` (après le header) :

```markdown
## [NOUVELLE_VERSION] - YYYY-MM-DD

### Added
- [nouvelles fonctionnalités avec descriptions]

### Changed
- [modifications avec descriptions]

### Fixed
- [corrections avec descriptions]

### Removed
- [suppressions avec descriptions]
```

Supprimer les sections vides. Date du jour.

### Étape 9: Mettre à jour README du plugin

SI nouvelles commandes, agents, ou skills :
- Ajouter documentation dans `{plugin}/README.md`
- Mettre à jour la section structure si fichiers ajoutés

### Étape 10: Mettre à jour README global

Éditer `README.md` à la racine :
- Mettre à jour la version dans le tableau : `| ... **{Plugin}** | NOUVELLE_VERSION |`

### Étape 11: Mettre à jour CHANGELOG global

Éditer `CHANGELOG.md` à la racine.

**Vérifier si section du jour existe :**
```markdown
## [YYYY.MM.DD] - YYYY-MM-DD
```

SI n'existe pas, créer après `## [Unreleased]`.

**SI nouveau plugin :**
```markdown
### Plugins Added
- **{plugin} vX.Y.Z** - Description courte
  - Détails des fonctionnalités
```

**SI plugin existant :**
```markdown
### Plugins Updated
- **{plugin} vX.Y.Z** - Titre court du changement
  - Détails des modifications
```

### Étape 12: Vérifier marketplace.json (si nouveau plugin)

SI nouveau plugin, ajouter dans `.claude-plugin/marketplace.json` :
```json
{
  "name": "{plugin}",
  "source": "./{plugin}",
  "description": "Description du plugin"
}
```

### Étape 13: Ajouter lien CHANGELOG (si nouveau plugin)

SI nouveau plugin, ajouter dans la section "Notes de version" de `CHANGELOG.md` :
```markdown
- [{plugin}/CHANGELOG.md]({plugin}/CHANGELOG.md)
```

### Étape 14: Résumé final

```
✅ Plugin {plugin} : v{OLD} → v{NEW} ({TYPE})

Type détecté : {PATCH|MINOR|MAJOR}
Raison : {nouveaux agents|nouvelles commandes|modifications|...}

Fichiers modifiés :
- {plugin}/.claude-plugin/plugin.json
- {plugin}/CHANGELOG.md
- {plugin}/README.md (si applicable)
- README.md
- CHANGELOG.md
- .claude-plugin/marketplace.json (si nouveau)

Prochaine étape : /git:commit
```

## Exemples

```bash
# Détection automatique plugins et versions
/bump

# Plugin spécifique
/bump git

# Forcer major version (rare)
/bump git --major
```

## Checklist

1. `{plugin}/.claude-plugin/plugin.json` - version
2. `{plugin}/CHANGELOG.md` - nouvelle entrée
3. `{plugin}/README.md` - si nouvelles fonctionnalités
4. `README.md` - tableau versions
5. `CHANGELOG.md` - section du jour
6. `.claude-plugin/marketplace.json` - si nouveau plugin
7. Lien CHANGELOG dans notes de version - si nouveau plugin
