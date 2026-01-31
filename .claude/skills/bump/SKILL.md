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
   - subject: `Sélectionner les plugins à bumper (AskUserQuestion)`
   - activeForm: `Selecting plugins to bump`
   - description: Demander sélection utilisateur des plugins à bumper

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

### 2. Sélection interactive des plugins

**Utilise AskUserQuestion pour demander la sélection :**
- Question : "Quels plugins veux-tu bumper ?"
- header : "Plugins"
- multiSelect : true
- Options :
  1. "Tous les plugins modifiés ({N} plugins)" (Recommended) - Description : "Bumper automatiquement tous les plugins avec des modifications"
  2. Pour chaque plugin : "{plugin} ({N} fichiers modifiés)" - Description : "Version actuelle : {version}"

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

#### 3.10. Synchroniser README.md et marketplace.json

Après avoir traité tous les plugins, vérifie la cohérence entre `README.md` et `.claude-plugin/marketplace.json` :

**Étapes :**
1. Extrais la liste des plugins depuis `README.md` (tableau "Plugins Disponibles")
2. Extrais la liste des plugins depuis `.claude-plugin/marketplace.json`
3. Identifie les différences :
   - Plugins dans README mais pas dans marketplace.json → ajouter au marketplace.json
   - Plugins dans marketplace.json mais pas dans README → ajouter au README
4. Pour chaque plugin manquant :
   - Dans marketplace.json : ajoute une entrée avec name, source, description (extraite du README)
   - Dans README : ajoute une ligne dans le tableau (extraire version depuis `{plugin}/.claude-plugin/plugin.json`)

**Règles d'ordre :**
- marketplace.json : ordre alphabétique par `name`
- README.md : ordre alphabétique par nom de plugin

#### 3.11. Mettre à jour DEPENDENCIES.json et init-marketplace.md

Pour chaque plugin bumpé, utilise ou crée `DEPENDENCIES.json` puis mets à jour la section AUTO-GENERATED dans `.claude/commands/init-marketplace.md` :

**Étapes :**

1. **Vérifier si DEPENDENCIES.json existe**

   ```bash
   # Vérifier l'existence du fichier
   if [ -f {plugin}/DEPENDENCIES.json ]; then
     # Fichier existe → passer à l'étape 2
   else
     # Fichier n'existe pas → scanner le plugin (étape 1.1)
   fi
   ```

1.1. **Scanner le plugin pour détecter les dépendances** (si DEPENDENCIES.json n'existe pas)

   Utilise Grep et Read pour analyser tous les fichiers du plugin :

   **a) Détecter les commandes système dans les skills/agents**
   ```bash
   # Scanner tous les fichiers SKILL.md et agents/*.md
   grep -rh "allowed-tools:" {plugin}/skills/*/SKILL.md {plugin}/agents/*.md 2>/dev/null

   # Exemples de patterns à chercher :
   # - Bash(git :*) → dépendance `git`
   # - Bash(gh :*) → dépendance `gh`
   # - Bash(npm :*) → dépendance `npm`
   # - Bash(pnpm :*) → dépendance `pnpm`
   # - Bash(bun :*) → dépendance `bun`
   # - Bash(php :*) → dépendance `php`
   # - Bash(composer :*) → dépendance `composer`
   ```

   **b) Détecter les commandes dans les scripts**
   ```bash
   # Scanner tous les types de scripts courants
   find {plugin}/scripts -type f \( \
     -name "*.ts" -o -name "*.js" -o -name "*.sh" -o \
     -name "*.py" -o -name "*.rb" -o -name "*.pl" -o \
     -name "*.php" \
   \) 2>/dev/null | head -20

   # Vérifier les shebangs pour détecter le runtime/interpréteur
   find {plugin}/scripts -type f -exec head -1 {} \; 2>/dev/null | grep "^#!"

   # Mapping shebang → dépendance :
   # #!/usr/bin/env bun → dépendance `bun`
   # #!/usr/bin/env node → dépendance `node`
   # #!/usr/bin/env python3 → dépendance `python3`
   # #!/usr/bin/env python → dépendance `python`
   # #!/usr/bin/env ruby → dépendance `ruby`
   # #!/usr/bin/env perl → dépendance `perl`
   # #!/usr/bin/env php → dépendance `php`
   # #!/bin/bash → dépendance `bash`
   # #!/bin/sh → dépendance `sh`
   ```

   **c) Détecter les packages NPM**
   ```bash
   # Chercher tous les package.json dans le plugin
   find {plugin} -name "package.json" -type f

   # Pour chaque package.json trouvé, extraire :
   # - dependencies
   # - devDependencies
   # - peerDependencies
   ```

   **d) Détecter les dépendances dans les hooks**
   ```bash
   # Scanner hooks.json s'il existe
   grep -h "command.*bun\|command.*node\|command.*npm" {plugin}/hooks/hooks.json 2>/dev/null
   ```

   **e) Scanner le contenu des fichiers pour mentions explicites**
   ```bash
   # Chercher des patterns dans tous les .md du plugin
   grep -rh "npm install\|bun install\|composer require\|apt install\|brew install" {plugin}/*.md 2>/dev/null
   ```

2. **Extraire et classifier les dépendances**

   Pour chaque dépendance détectée :

   **Dépendances critiques** :
   - Commandes utilisées dans `allowed-tools` de plusieurs skills
   - Runtime détecté dans les shebangs de scripts
   - Commandes mentionnées dans hooks
   - Sans ces dépendances, le plugin est non fonctionnel ou très limité

   **Dépendances optionnelles** :
   - Commandes utilisées par un seul skill/agent
   - Commandes marquées comme "optionnel" dans la documentation
   - Fonctionnalités secondaires

   **Packages NPM** :
   - Extraire de tous les package.json trouvés
   - Distinguer dependencies, devDependencies, peerDependencies
   - Garder les versions spécifiées (^, ~, >=, etc.)

   **Versions minimales** :
   - Chercher des patterns comme `>= X.Y.Z` dans les commentaires
   - Chercher dans plugin.json s'il y a un champ `engines` ou `requirements`

3. **Déduire les informations contextuelles**

   Pour améliorer la documentation, ajouter automatiquement les dépendances implicites :

   **Dépendances implicites système** :
   - Si `bun` détecté → ajouter `node` >= 16.0.0 (prérequis de Bun)
   - Si `composer` détecté → ajouter `php` si pas déjà listé
   - Si `npm` ou `pnpm` détecté → ajouter `node` si pas déjà listé
   - Si `pip` détecté → ajouter `python` si pas déjà listé
   - Si `gem` détecté → ajouter `ruby` si pas déjà listé

   **Dépendances implicites packages** :
   - Si scripts TypeScript (*.ts) → ajouter `typescript` dans packages NPM si absent
   - Si scripts Python avec imports → extraire via `grep "^import\|^from"` pour détecter modules
   - Si Makefile détecté → ajouter `make` dans dépendances
   - Si Dockerfile détecté → ajouter `docker` dans dépendances optionnelles

1.2. **Créer ou mettre à jour DEPENDENCIES.json**

   **Si le fichier n'existe pas** (résultat du scan en 1.1) :

   Créer `{plugin}/DEPENDENCIES.json` avec le format suivant :

   ```json
   {
     "version": "1.0",
     "critical": {
       "commande": {
         "version": ">=X.Y.Z",
         "description": "Description de l'utilisation",
         "detected_in": ["fichier1.ts", "fichier2.md"],
         "impact": "Fonctionnalités bloquées sans cette dépendance"
       }
     },
     "optional": {
       "commande": {
         "description": "Description"
       }
     },
     "packages": {
       "npm": {
         "dependencies": {},
         "devDependencies": {},
         "peerDependencies": {}
       },
       "python": {
         "dependencies": []
       }
     }
   }
   ```

   **Règles de génération** :
   - Classifier automatiquement en critical/optional selon fréquence d'utilisation
   - Inclure `detected_in` pour traçabilité
   - Inclure `impact` pour les dépendances critiques
   - Pour plugins sans dépendances : créer avec `{}`  vides

   **Si le fichier existe déjà** :
   - Lire le contenu actuel
   - Comparer avec ce qui a été détecté par le scan
   - Si nouvelles dépendances détectées → les ajouter
   - Si dépendances supprimées → les retirer
   - Conserver les descriptions/commentaires manuels existants

2. **Lire DEPENDENCIES.json du plugin**

   ```bash
   # Lire le fichier JSON
   cat {plugin}/DEPENDENCIES.json
   ```

   Extraire :
   - `critical` : dépendances obligatoires
   - `optional` : dépendances facultatives
   - `packages.npm` : packages NPM (dependencies, devDependencies, peerDependencies)
   - `packages.python` : packages Python le cas échéant
   - `packages.composer` : packages PHP le cas échéant

3. **Mettre à jour init-marketplace.md**

   ```bash
   # 1. Lire le fichier actuel
   Read .claude/commands/init-marketplace.md

   # 2. Localiser la section AUTO-GENERATED
   # Chercher entre "<!-- AUTO-GENERATED" et "<!-- END AUTO-GENERATED -->"

   # 3. Construire la nouvelle entrée du plugin
   ```

   **Format de sortie** :
   ```markdown
   #### Plugin: {plugin} (v{VERSION})
   **Dépendances critiques:**
   - `commande` >= version - Description de l'utilisation

   **Dépendances optionnelles:**  (si applicable)
   - `commande` - Description

   **Packages NPM requis:**  (si applicable)
   - package@^version
   - package@^version (dev)
   - package@^version (peer)

   **Fonctionnalités bloquées sans dépendances:**  (si pertinent)
   - Sans X : Liste des fonctionnalités impactées
   ```

   **Règles d'édition** :
   - Si le plugin existe déjà dans AUTO-GENERATED → remplacer sa section complètement
   - Si le plugin est nouveau → insérer à la position alphabétique
   - Maintenir l'ordre alphabétique par nom de plugin
   - Ne jamais toucher aux autres plugins

4. **Exemple concret : workflow DEPENDENCIES.json → init-marketplace.md**

   **Plugin analysé** : `mlvn` (v1.0.0)

   **Étape 1 : Lire DEPENDENCIES.json**
   ```bash
   cat mlvn/DEPENDENCIES.json
   ```

   **Contenu extrait** :
   ```json
   {
     "version": "1.0",
     "critical": {
       "bun": {
         "version": ">=1.0.0",
         "description": "Runtime pour scripts TypeScript et hooks de sécurité",
         "impact": "Hook PreToolUse (sécurité), statusline, Ralph Loop, scripts"
       },
       "node": {
         "version": ">=16.0.0",
         "description": "Prérequis pour Bun et packages NPM"
       }
     },
     "optional": {
       "gh": {"description": "Pour skills git-create-pr, git-fix-pr-comments, git-merge"},
       "ccusage": {"description": "Pour statusline tracking des coûts"},
       "biome": {"description": "Pour lint/format des scripts"}
     },
     "packages": {
       "npm": {
         "dependencies": {
           "@ai-sdk/anthropic": "^3.0.6",
           "ai": "^6.0.11",
           "picocolors": "^1.1.1",
           "table": "^6.9.0",
           "zod": "^4.3.5"
         },
         "devDependencies": {
           "@biomejs/biome": "^2.3.2"
         },
         "peerDependencies": {
           "typescript": "^5.0.0"
         }
       }
     }
   }
   ```

   **Étape 2 : Générer la section pour init-marketplace.md**
   ```markdown
   #### Plugin: mlvn (v1.0.0)
   **Dépendances critiques:**
   - `bun` >= 1.0.0 - Runtime pour scripts TypeScript et hooks de sécurité
   - `node` >= 16.0.0 - Prérequis pour Bun et packages NPM

   **Dépendances optionnelles:**
   - `gh` - Pour skills git-create-pr, git-fix-pr-comments, git-merge
   - `ccusage` - Pour statusline tracking des coûts
   - `biome` - Pour lint/format des scripts

   **Packages NPM requis:**
   - @ai-sdk/anthropic@^3.0.6
   - ai@^6.0.11
   - picocolors@^1.1.1
   - table@^6.9.0
   - zod@^4.3.5
   - @biomejs/biome@^2.3.2 (dev)
   - typescript@^5.0.0 (peer)

   **Fonctionnalités bloquées sans dépendances:**
   - Sans Bun : Hook PreToolUse (sécurité), statusline, Ralph Loop, scripts
   ```

   **Étape 3 : Insérer/Remplacer dans init-marketplace.md**
   - Lire `.claude/commands/init-marketplace.md`
   - Localiser la section AUTO-GENERATED (entre `<!-- AUTO-GENERATED` et `<!-- END AUTO-GENERATED -->`)
   - Si le plugin existe déjà : remplacer complètement sa section
   - Si le plugin est nouveau : insérer à la position alphabétique
   - Conserver l'ordre alphabétique par nom de plugin

5. **Gestion des cas particuliers**

   - **Plugin sans dépendances** : écrire `**Dépendances critiques:** Aucune`
   - **Plugin supprimé** : retirer complètement sa section de AUTO-GENERATED
   - **Dépendances inchangées** : conserver la section existante telle quelle
   - **Nouvelle dépendance** : ajouter dans la section appropriée

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
