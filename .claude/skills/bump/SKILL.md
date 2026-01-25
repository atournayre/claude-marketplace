---
name: bump
description: Automatise les mises à jour de version des plugins avec détection automatique du type de version
model: claude-haiku-4-5-20251001
argument-hint: [plugin-name]
allowed-tools: [Read, Edit, Bash, Glob, Grep, TaskCreate, TaskUpdate, TaskList]
version: 1.0.0
license: MIT
hooks:
  PreToolUse:
    - matcher: "Bash(git diff:*)"
      hooks:
        - type: command
          command: |
            # Hook 1: Validation workspace clean
            if ! git diff --quiet; then
              echo "⚠️  Attention : modifications non stagées détectées"
              echo "Les fichiers suivants seront inclus dans le bump :"
              git diff --name-only
            fi
          once: true
    - matcher: "Read"
      hooks:
        - type: command
          command: |
            # Hook 3: Validation fichiers requis
            PLUGIN_FILE=$(echo "$CLAUDE_TOOL_ARGS" | grep -oP '(?<=file_path: ).*?plugin\.json' || echo "")
            if [ -n "$PLUGIN_FILE" ]; then
              PLUGIN_DIR=$(dirname $(dirname "$PLUGIN_FILE"))
              for file in "$PLUGIN_DIR/.claude-plugin/plugin.json" "$PLUGIN_DIR/CHANGELOG.md" "$PLUGIN_DIR/README.md"; do
                if [ ! -f "$file" ]; then
                  echo "❌ Fichier manquant : $file"
                  exit 1
                fi
              done
            fi
          once: true
  PostToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: |
            # Hook 2: Auto-commit après bump (suggéré)
            if ! git diff --quiet; then
              # Détecter le plugin et la version depuis le dernier fichier édité
              if echo "$CLAUDE_TOOL_ARGS" | grep -q "plugin.json"; then
                PLUGIN_JSON=$(echo "$CLAUDE_TOOL_ARGS" | grep -oP '(?<=file_path: ).*?plugin\.json' || echo "")
                if [ -n "$PLUGIN_JSON" ] && [ -f "$PLUGIN_JSON" ]; then
                  PLUGIN=$(basename $(dirname $(dirname "$PLUGIN_JSON")))
                  NEW_VERSION=$(grep '"version"' "$PLUGIN_JSON" | sed 's/.*"\([0-9.]*\)".*/\1/')
                  OLD_VERSION=$(git show HEAD:"$PLUGIN_JSON" 2>/dev/null | grep '"version"' | sed 's/.*"\([0-9.]*\)".*/\1/' || echo "unknown")

                  echo ""
                  echo "📝 Bump détecté : $PLUGIN $OLD_VERSION → $NEW_VERSION"
                  echo ""
                  echo "Prêt pour commit. Tu peux lancer :"
                  echo "   /git:commit"
                  echo ""
                  echo "Message suggéré :"
                  echo "   🔖 chore(git): bump version $OLD_VERSION → $NEW_VERSION (PATCH)"
                fi
              fi
            fi
          once: false
---

# Bump Version Plugin

Mettre à jour automatiquement la version d'un ou plusieurs plugins avec détection du type de version.

## Arguments
- `plugin-name` : Nom du plugin (optionnel, détection automatique depuis git)
- `--major` : Forcer une version MAJOR (rare)

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

### 1. Identifier les plugins modifiés

- Exécute `git diff --name-only HEAD` pour obtenir les fichiers modifiés (non stagés)
- Exécute `git diff --staged --name-only` pour obtenir les fichiers stagés
- Combine les deux listes et filtre pour extraire les noms de plugins uniques (premier répertoire du chemin)
- **Ignore** : fichiers dans `.claude/` et fichiers à la racine (`README.md`, `CHANGELOG.md`)
- Si un plugin-name est fourni en argument, utilise uniquement celui-ci

### 2. Pour chaque plugin détecté, détecter le type de version

**Exécute :**
- `git diff --staged --name-only --diff-filter=A` pour lister les nouveaux fichiers stagés du plugin

**Analyse les patterns suivants :**
- Nouveaux agents : fichiers `{plugin}/agents/*.md`
- Nouvelles commandes : fichiers `{plugin}/commands/*.md` (legacy)
- Nouveaux skills : répertoires `{plugin}/skills/*/`
- Nouveau plugin : le plugin n'existe pas dans `.claude-plugin/marketplace.json`

**Détermine le type de version :**
- Si nouveaux agents OU nouvelles commandes OU nouveaux skills OU nouveau plugin → **MINOR** (X.Y.0 → X.Y+1.0)
- Si `--major` passé en argument → **MAJOR** (X.0.0 → X+1.0.0)
- Sinon → **PATCH** (X.Y.Z → X.Y.Z+1)

### 3. Lire la version actuelle et calculer la nouvelle version

- Lis le fichier `{plugin}/.claude-plugin/plugin.json`
- Extrais la version actuelle (champ `version`)
- Calcule la nouvelle version selon le type détecté :
  - PATCH : `1.2.3` → `1.2.4`
  - MINOR : `1.2.3` → `1.3.0`
  - MAJOR : `1.2.3` → `2.0.0`

### 4. Créer les tâches avec TaskCreate

Utilise TaskCreate pour créer les tâches suivantes pour chaque plugin :

1. **Bump version du plugin**
   - subject: `Bump version {plugin}/.claude-plugin/plugin.json ({OLD} → {NEW})`
   - activeForm: `Bumping version {plugin}`

2. **Mettre à jour CHANGELOG du plugin**
   - subject: `Mettre à jour {plugin}/CHANGELOG.md`
   - activeForm: `Updating {plugin} changelog`

3. **Mettre à jour README du plugin** (si nouvelles fonctionnalités)
   - subject: `Mettre à jour {plugin}/README.md`
   - activeForm: `Updating {plugin} readme`

4. **Mettre à jour README global**
   - subject: `Mettre à jour README.md global (tableau versions)`
   - activeForm: `Updating global README`

5. **Mettre à jour CHANGELOG global**
   - subject: `Mettre à jour CHANGELOG.md global`
   - activeForm: `Updating global changelog`

6. **Mettre à jour marketplace.json** (si nouveau plugin)
   - subject: `Mettre à jour .claude-plugin/marketplace.json`
   - activeForm: `Updating marketplace.json`

**Au fur et à mesure que tu complètes chaque tâche, utilise TaskUpdate pour marquer la tâche comme `completed`.**

### 5. Analyser les changements pour le CHANGELOG

**Exécute :**
- `git diff {plugin}/` pour voir tous les changements du plugin
- `git diff --staged {plugin}/` pour voir les changements stagés

**Analyse les changements et catégorise-les :**
- Nouveaux agents/skills/commandes → `### Added`
- Modifications de code/logique → `### Changed`
- Corrections de bugs → `### Fixed`
- Suppressions → `### Removed`

**Lis les nouveaux fichiers** pour extraire leurs descriptions (titre, description) depuis le frontmatter YAML.

### 6. Mettre à jour plugin.json

Édite `{plugin}/.claude-plugin/plugin.json` et remplace la version :
```json
"version": "NOUVELLE_VERSION"
```

**Marque ensuite la tâche correspondante comme `completed` avec TaskUpdate.**

### 7. Mettre à jour CHANGELOG du plugin

Lis `{plugin}/CHANGELOG.md` et ajoute **en haut** (après le titre) une nouvelle section :

```markdown
## [NOUVELLE_VERSION] - YYYY-MM-DD

### Added
- Description des nouvelles fonctionnalités

### Changed
- Description des modifications

### Fixed
- Description des corrections

### Removed
- Description des suppressions
```

**Règles :**
- Utilise la date du jour (format YYYY-MM-DD)
- Supprime les sections vides (sans contenu)
- Garde les sections dans l'ordre : Added, Changed, Fixed, Removed

**Marque ensuite la tâche correspondante comme `completed` avec TaskUpdate.**

### 8. Mettre à jour README du plugin (si applicable)

**Si** nouveaux agents, skills ou commandes ont été ajoutés :
- Lis `{plugin}/README.md`
- Ajoute la documentation pour les nouvelles fonctionnalités dans la section appropriée
- Mets à jour la section structure si nécessaire

**Marque ensuite la tâche correspondante comme `completed` avec TaskUpdate.**

### 9. Mettre à jour README global

Lis `README.md` à la racine et mets à jour la ligne du plugin dans le tableau des versions :
```markdown
| ... | **{Plugin}** | NOUVELLE_VERSION |
```

**Marque ensuite la tâche correspondante comme `completed` avec TaskUpdate.**

### 10. Mettre à jour CHANGELOG global

Lis `CHANGELOG.md` à la racine.

**Vérifie si une section avec la date du jour existe :**
```markdown
## [YYYY.MM.DD] - YYYY-MM-DD
```

**Si elle n'existe pas**, crée-la juste après `## [Unreleased]` :
```markdown
## [YYYY.MM.DD] - YYYY-MM-DD
```

**Ajoute l'entrée du plugin :**
- Si **nouveau plugin** :
  ```markdown
  ### Plugins Added
  - **{plugin} vNOUVELLE_VERSION** - Description courte
    - Liste des fonctionnalités
  ```
- Si **plugin existant** :
  ```markdown
  ### Plugins Updated
  - **{plugin} vNOUVELLE_VERSION** - Résumé des changements
    - Détails des modifications
  ```

**Marque ensuite la tâche correspondante comme `completed` avec TaskUpdate.**

### 11. Mettre à jour marketplace.json (si nouveau plugin)

**Si** le plugin est nouveau (n'existe pas dans `.claude-plugin/marketplace.json`) :
- Lis `.claude-plugin/marketplace.json`
- Ajoute une entrée pour le nouveau plugin :
  ```json
  {
    "name": "{plugin}",
    "source": "./{plugin}",
    "description": "Description du plugin"
  }
  ```
- Ajoute aussi un lien vers le CHANGELOG dans la section "Notes de version" du `CHANGELOG.md` global

**Marque ensuite la tâche correspondante comme `completed` avec TaskUpdate.**

### 12. Vérification et résumé final

**Vérifie avec TaskList que toutes les tâches sont marquées comme `completed`.**

Affiche un résumé avec :
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

✅ Toutes les tâches complétées

Prochaine étape : /git:commit
```

## Règles de versioning

- **MINOR** (X.Y.0 → X.Y+1.0) : Nouveaux agents, skills, commandes, ou nouveau plugin
- **PATCH** (X.Y.Z → X.Y.Z+1) : Modifications, corrections, refactoring, documentation
- **MAJOR** (X.0.0 → X+1.0.0) : Uniquement si `--major` passé en argument (breaking changes)

## Relevant Files
- @.claude-plugin/marketplace.json
- @README.md
- @CHANGELOG.md
- @{plugin}/.claude-plugin/plugin.json
- @{plugin}/CHANGELOG.md
- @{plugin}/README.md
