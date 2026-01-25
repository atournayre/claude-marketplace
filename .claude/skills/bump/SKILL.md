---
name: bump
description: Automatise les mises à jour de version des plugins avec détection automatique du type de version
model: claude-haiku-4-5-20251001
allowed-tools: [Read, Edit, Bash, Glob, Grep, TaskCreate, TaskUpdate, TaskList, AskUserQuestion]
version: 1.0.2
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

Mettre à jour automatiquement la version d'un ou plusieurs plugins avec détection automatique du type de version.

## Instructions à Exécuter

### 0. Créer les tâches de workflow

Utilise TaskCreate pour créer les tâches suivantes :

1. **Détecter plugins modifiés**
   - subject: `Détecter les plugins modifiés via git diff`
   - activeForm: `Detecting modified plugins`
   - description: Exécuter git diff pour identifier les plugins avec modifications

2. **Sélectionner plugins à bumper**
   - subject: `Sélectionner les plugins à bumper (vérification bumps + AskUserQuestion)`
   - activeForm: `Selecting plugins to bump`
   - description: Vérifier bumps du jour + demander sélection utilisateur

3. **Bumper les plugins sélectionnés**
   - subject: `Exécuter bump pour chaque plugin sélectionné`
   - activeForm: `Bumping selected plugins`
   - description: Détecter type version + analyser changements + mettre à jour fichiers

4. **Vérifier résultat final**
   - subject: `Vérifier que tous les fichiers sont à jour`
   - activeForm: `Verifying final result`
   - description: Afficher résumé avec fichiers modifiés

### 1. Identifier les plugins modifiés

Exécute les commandes suivantes en parallèle :
- `git diff --name-only HEAD` pour les fichiers modifiés (non stagés)
- `git diff --staged --name-only` pour les fichiers stagés

Combine les deux listes et filtre pour extraire les noms de plugins uniques (premier répertoire du chemin).

**Ignore** :
- Fichiers dans `.claude/`
- Fichiers à la racine (`README.md`, `CHANGELOG.md`)

Pour chaque plugin, compte le nombre de fichiers modifiés.

**Marque ensuite la tâche "Détecter plugins modifiés" comme `completed` avec TaskUpdate.**

### 2. Vérifier les bumps existants et sélection interactive

**Pour chaque plugin détecté :**
- Lis `{plugin}/CHANGELOG.md` (premières 20 lignes)
- Vérifie si la première version est datée d'aujourd'hui (format `## [X.Y.Z] - YYYY-MM-DD`)
- Si oui, marque le plugin comme "⚠️ Déjà bumpé aujourd'hui"

**Utilise AskUserQuestion pour demander la sélection :**
- Question : "Quels plugins veux-tu bumper ?"
- header : "Plugins"
- multiSelect : true
- Options :
  1. "Tous les plugins modifiés ({N} plugins)" (Recommended) - Description : "Bumper automatiquement tous les plugins avec des modifications"
  2. Pour chaque plugin : "{plugin} ({N} fichiers modifiés) {⚠️ Déjà bumpé aujourd'hui si applicable}" - Description : "Version actuelle : {version}"

**Si l'utilisateur sélectionne "Tous"**, utilise tous les plugins détectés.
**Sinon**, utilise uniquement les plugins sélectionnés individuellement.

**Marque ensuite la tâche "Sélectionner plugins à bumper" comme `completed` avec TaskUpdate.**

### 3. Pour chaque plugin sélectionné : bump complet

**Pour chaque plugin sélectionné, exécute les sous-étapes suivantes :**

#### 3.1. Détecter le type de version

**Exécute :**
- `git diff --staged --name-only --diff-filter=A` pour lister les nouveaux fichiers stagés du plugin

**Analyse les patterns suivants :**
- Nouveaux agents : fichiers `{plugin}/agents/*.md`
- Nouvelles commandes : fichiers `{plugin}/commands/*.md` (legacy)
- Nouveaux skills : répertoires `{plugin}/skills/*/`
- Nouveau plugin : le plugin n'existe pas dans `.claude-plugin/marketplace.json`

**Détermine le type de version :**
- Si nouveaux agents OU nouvelles commandes OU nouveaux skills OU nouveau plugin → **MINOR** (X.Y.0 → X.Y+1.0)
- Sinon → **PATCH** (X.Y.Z → X.Y.Z+1)

#### 3.2. Lire la version actuelle et calculer la nouvelle version

- Lis le fichier `{plugin}/.claude-plugin/plugin.json`
- Extrais la version actuelle (champ `version`)
- Calcule la nouvelle version selon le type détecté :
  - PATCH : `1.2.3` → `1.2.4`
  - MINOR : `1.2.3` → `1.3.0`

#### 3.3. Analyser les changements pour le CHANGELOG

**Exécute :**
- `git diff {plugin}/` pour voir tous les changements du plugin
- `git diff --staged {plugin}/` pour voir les changements stagés

**Analyse les changements et catégorise-les :**
- Nouveaux agents/skills/commandes → `### Added`
- Modifications de code/logique → `### Changed`
- Corrections de bugs → `### Fixed`
- Suppressions → `### Removed`

**Lis les nouveaux fichiers** pour extraire leurs descriptions (titre, description) depuis le frontmatter YAML.

#### 3.4. Mettre à jour plugin.json

Édite `{plugin}/.claude-plugin/plugin.json` et remplace la version :
```json
"version": "NOUVELLE_VERSION"
```

#### 3.5. Mettre à jour CHANGELOG du plugin

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

#### 3.6. Mettre à jour README du plugin (si applicable)

**Si** nouveaux agents, skills ou commandes ont été ajoutés :
- Lis `{plugin}/README.md`
- Ajoute la documentation pour les nouvelles fonctionnalités dans la section appropriée
- Mets à jour la section structure si nécessaire

#### 3.7. Mettre à jour README global

Lis `README.md` à la racine et mets à jour la ligne du plugin dans le tableau des versions :
```markdown
| ... | **{Plugin}** | NOUVELLE_VERSION |
```

#### 3.8. Mettre à jour CHANGELOG global

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

#### 3.9. Mettre à jour marketplace.json (si nouveau plugin)

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

**Marque ensuite la tâche "Bumper les plugins sélectionnés" comme `completed` avec TaskUpdate.**

### 4. Vérification et résumé final

Affiche un résumé pour chaque plugin bumpé :
```
✅ Plugin {plugin} : v{OLD} → v{NEW} ({TYPE})

Type détecté : {PATCH|MINOR}
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

**Marque ensuite la tâche "Vérifier résultat final" comme `completed` avec TaskUpdate.**

## Règles de versioning

- **MINOR** (X.Y.0 → X.Y+1.0) : Nouveaux agents, skills, commandes, ou nouveau plugin
- **PATCH** (X.Y.Z → X.Y.Z+1) : Modifications, corrections, refactoring, documentation

## Relevant Files
- @.claude-plugin/marketplace.json
- @README.md
- @CHANGELOG.md
- @{plugin}/.claude-plugin/plugin.json
- @{plugin}/CHANGELOG.md
- @{plugin}/README.md
