---
name: bump
description: Automatise les mises à jour de version des plugins avec détection automatique du type de version
model: haiku
allowed-tools: [Read, Edit, Bash, Glob, Grep, TaskCreate, TaskUpdate, TaskList, AskUserQuestion]
version: 2.0.0
license: MIT
---

# Bump Version Plugin

Mettre à jour automatiquement la version d'un ou plusieurs plugins avec détection automatique du type de version.

## IMPORTANT : Task Management System obligatoire

**RÈGLE CRITIQUE** : Chaque étape DOIT être trackée via TaskCreate/TaskUpdate.
- Créer la tâche AVANT de commencer l'étape
- Marquer `in_progress` au début
- Marquer `completed` UNIQUEMENT quand l'étape est 100% terminée
- NE JAMAIS sauter une étape

## Instructions à Exécuter

### Étape 1 : Créer TOUTES les tâches du workflow

**OBLIGATOIRE** : Utilise TaskCreate pour créer ces 6 tâches dans cet ordre exact :

```
TaskCreate #1: "Détecter les plugins modifiés"
  - activeForm: "Detecting modified plugins"
  - description: "git diff pour identifier plugins avec modifications"

TaskCreate #2: "Sélectionner les plugins à bumper"
  - activeForm: "Selecting plugins to bump"
  - description: "AskUserQuestion pour sélection utilisateur"

TaskCreate #3: "Mettre à jour fichiers du plugin"
  - activeForm: "Updating plugin files"
  - description: "plugin.json + CHANGELOG.md + README.md du plugin"

TaskCreate #4: "Mettre à jour fichiers du marketplace"
  - activeForm: "Updating marketplace files"
  - description: "README.md global + CHANGELOG.md global + marketplace.json"

TaskCreate #5: "Mettre à jour dépendances et documentation"
  - activeForm: "Updating dependencies and docs"
  - description: "DEPENDENCIES.json + rebuild VitePress (npm run build)"

TaskCreate #6: "Vérifier et afficher résumé"
  - activeForm: "Verifying final result"
  - description: "Lister tous les fichiers modifiés + prochaine étape"
```

**Après création** : Affiche `TaskList` pour confirmer que les 6 tâches existent.

---

### Étape 2 : Détecter les plugins modifiés

**TaskUpdate : Tâche #1 → `in_progress`**

Exécute en parallèle :
```bash
git diff --name-only HEAD
git diff --staged --name-only
```

**Traitement** :
1. Combine les deux listes
2. Filtre pour extraire les noms de plugins (premier répertoire)
3. Ignore : `.claude/`, fichiers à la racine
4. Compte les fichiers par plugin

**TaskUpdate : Tâche #1 → `completed`**

---

### Étape 3 : Sélection interactive

**TaskUpdate : Tâche #2 → `in_progress`**

Utilise `AskUserQuestion` :
```json
{
  "questions": [{
    "question": "Quels plugins veux-tu bumper ?",
    "header": "Plugins",
    "multiSelect": true,
    "options": [
      {"label": "Tous les plugins modifiés (N plugins) (Recommended)", "description": "Bumper automatiquement tous"},
      {"label": "{plugin} (N fichiers)", "description": "Version actuelle : X.Y.Z"}
    ]
  }]
}
```

**TaskUpdate : Tâche #2 → `completed`**

---

### Étape 4 : Mettre à jour fichiers du plugin

**TaskUpdate : Tâche #3 → `in_progress`**

**Pour CHAQUE plugin sélectionné, dans cet ordre :**

#### 4.1 Détecter le type de version

```bash
git diff --staged --name-only --diff-filter=A | grep "^{plugin}/"
```

**Règles** :
- Nouveaux agents (`agents/*.md`) → MINOR
- Nouveaux skills (`skills/*/`) → MINOR
- Nouveau plugin (pas dans marketplace.json) → MINOR
- Sinon → PATCH

#### 4.2 Calculer la nouvelle version

Lis `{plugin}/.claude-plugin/plugin.json` et calcule :
- PATCH : `1.2.3` → `1.2.4`
- MINOR : `1.2.3` → `1.3.0`

#### 4.3 Analyser les changements

```bash
git diff {plugin}/
git diff --staged {plugin}/
```

Catégorise en : Added, Changed, Fixed, Removed

#### 4.4 Mettre à jour plugin.json

```json
"version": "NOUVELLE_VERSION"
```

#### 4.5 Mettre à jour CHANGELOG du plugin

Ajoute en haut (après le titre) :
```markdown
## [NOUVELLE_VERSION] - YYYY-MM-DD

### Added
- ...

### Changed
- ...
```

#### 4.6 Mettre à jour README du plugin (si nouveaux agents/skills)

**TaskUpdate : Tâche #3 → `completed`**

---

### Étape 5 : Mettre à jour fichiers du marketplace

**TaskUpdate : Tâche #4 → `in_progress`**

#### 5.1 Mettre à jour README.md global

Dans le tableau des plugins :
```markdown
| 📝 **{Plugin}** | NOUVELLE_VERSION | Description | [README](...) |
```

#### 5.2 Mettre à jour CHANGELOG.md global

Vérifie si section du jour existe :
```markdown
## [YYYY.MM.DD] - YYYY-MM-DD
```

Si non, crée-la après `## [Unreleased]`.

Ajoute :
```markdown
### Plugins Updated
- **{plugin} vNOUVELLE_VERSION** - Résumé des changements
```

#### 5.3 Mettre à jour marketplace.json (si nouveau plugin)

Si le plugin n'existe pas dans `.claude-plugin/marketplace.json` :
```json
{
  "name": "{plugin}",
  "source": "./{plugin}",
  "description": "..."
}
```

#### 5.4 Synchroniser README.md et marketplace.json

Vérifie la cohérence :
- Plugins dans README mais pas marketplace → ajouter
- Plugins dans marketplace mais pas README → ajouter
- Ordre alphabétique dans les deux fichiers

**TaskUpdate : Tâche #4 → `completed`**

---

### Étape 6 : Mettre à jour dépendances et documentation

**TaskUpdate : Tâche #5 → `in_progress`**

#### 6.1 DEPENDENCIES.json

Si `{plugin}/DEPENDENCIES.json` n'existe pas, scanner et créer :
```json
{
  "version": "1.0",
  "critical": {},
  "optional": {},
  "packages": {"npm": {}}
}
```

#### 6.2 Rebuild VitePress

**OBLIGATOIRE - NE PAS OUBLIER** :
```bash
cd docs && npm run build
```

Vérifie que la commande s'exécute sans erreur.

#### 6.3 Vérifier les fichiers générés

```bash
git status --short docs/
```

Les fichiers `docs/plugins/{plugin}.md` et `docs/commands/index.md` doivent être modifiés.

**TaskUpdate : Tâche #5 → `completed`**

---

### Étape 7 : Vérification et résumé final

**TaskUpdate : Tâche #6 → `in_progress`**

Affiche le résumé complet :

```
✅ Plugin {plugin} : v{OLD} → v{NEW} ({TYPE})

Type : {PATCH|MINOR}
Raison : {description}

Fichiers modifiés :
✓ {plugin}/.claude-plugin/plugin.json
✓ {plugin}/CHANGELOG.md
✓ {plugin}/README.md (si applicable)
✓ README.md
✓ CHANGELOG.md
✓ .claude-plugin/marketplace.json (si nouveau)
✓ docs/plugins/{plugin}.md
✓ docs/commands/index.md

Prochaine étape : /git:commit
```

**TaskUpdate : Tâche #6 → `completed`**

---

## Checklist de validation finale

Avant de terminer, vérifie que TOUTES ces conditions sont remplies :

- [ ] Tâche #1 completed : Plugins détectés
- [ ] Tâche #2 completed : Sélection faite
- [ ] Tâche #3 completed : plugin.json + CHANGELOG plugin + README plugin mis à jour
- [ ] Tâche #4 completed : README global + CHANGELOG global + marketplace.json mis à jour
- [ ] Tâche #5 completed : DEPENDENCIES.json + VitePress rebuild
- [ ] Tâche #6 completed : Résumé affiché

**Si une tâche n'est pas completed, NE PAS continuer.**

---

## Règles de versioning

- **MINOR** (X.Y.0 → X.Y+1.0) : Nouveaux agents, skills, ou nouveau plugin
- **PATCH** (X.Y.Z → X.Y.Z+1) : Modifications, corrections, refactoring, documentation

## Relevant Files

- `{plugin}/.claude-plugin/plugin.json`
- `{plugin}/CHANGELOG.md`
- `{plugin}/README.md`
- `README.md`
- `CHANGELOG.md`
- `.claude-plugin/marketplace.json`
- `{plugin}/DEPENDENCIES.json`
- `docs/plugins/{plugin}.md`
- `docs/commands/index.md`
