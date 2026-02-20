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

## RÈGLE ANTI-OUBLI : Vérification avant completed

**INTERDICTION** de marquer une tâche `completed` sans avoir :
1. Exécuté CHAQUE sous-étape listée (4.1, 4.2, 4.3... pas juste certaines)
2. Vérifié la sous-checklist `🔒 AVANT DE MARQUER COMPLETED` de l'étape
3. Lu les fichiers cibles pour confirmer que la modification est bien faite

**Si une sous-étape semble "non applicable"** : tu DOIS quand même lire le fichier cible pour le vérifier. Ne JAMAIS supposer qu'une étape est inapplicable sans preuve.

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
  - description: "README.md global + CHANGELOG.md global + marketplace.json + PR template"

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

**Vérification dépréciation** : Pour chaque plugin sélectionné, lis `{plugin}/.claude-plugin/plugin.json` et vérifie si `"deprecated": true` est présent. Si oui, afficher un avertissement :
```
⚠️  {plugin} est déprécié (remplacé par : {replaced_by}). Continuer quand même ? (bump patch uniquement recommandé)
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

**OBLIGATOIRE si MINOR** : Lis `{plugin}/README.md` avec Read et mets à jour :
- Ajouter la nouvelle commande/skill dans le tableau "Slash Commands" ou équivalent
- Ajouter les nouveaux agents dans la section agents si elle existe
- Mettre à jour la structure du plugin (arborescence `tree`)
- Ajouter une section usage/exemples pour les nouvelles fonctionnalités

Si le README ne contient pas de section pertinente, en ajouter une.

**🔒 AVANT DE MARQUER COMPLETED - Vérifie ces points :**
- [ ] `{plugin}/.claude-plugin/plugin.json` → version mise à jour (Read pour vérifier)
- [ ] `{plugin}/CHANGELOG.md` → nouvelle entrée en haut du fichier (Read pour vérifier)
- [ ] `{plugin}/README.md` → nouvelles commandes/agents/structure documentés (Read pour vérifier)
- [ ] Si MINOR et aucune modif README → ERREUR, tu as oublié quelque chose

**TaskUpdate : Tâche #3 → `completed`**

---

### Étape 5 : Mettre à jour fichiers du marketplace

**TaskUpdate : Tâche #4 → `in_progress`**

#### 5.1 Mettre à jour README.md global

**OBLIGATOIRE** : Lis `README.md` avec Read. Trouve le tableau des plugins et mets à jour la ligne du plugin :
```markdown
| 📝 **{Plugin}** | NOUVELLE_VERSION | Description mise à jour | [README](...) |
```

#### 5.2 Mettre à jour CHANGELOG.md global

**OBLIGATOIRE** : Lis `CHANGELOG.md` avec Read. Vérifie si section du jour existe :
```markdown
## [YYYY.MM.DD] - YYYY-MM-DD
```

Si non, crée-la après `## [Unreleased]`.

Ajoute :
```markdown
### Plugins Updated
- **{plugin} vNOUVELLE_VERSION** - Résumé des changements
  - Détail changement 1
  - Détail changement 2
  - Dépôt : [{plugin}/CHANGELOG.md]({plugin}/CHANGELOG.md)
```

#### 5.3 Mettre à jour marketplace.json (si nouveau plugin)

**OBLIGATOIRE** : Lis `.claude-plugin/marketplace.json` avec Read. Si le plugin n'existe pas :
```json
{
  "name": "{plugin}",
  "source": "./{plugin}",
  "description": "..."
}
```

Si le plugin existe déjà, vérifier que sa description est à jour.

#### 5.4 Synchroniser README.md et marketplace.json

Vérifie la cohérence :
- Plugins dans README mais pas marketplace → ajouter
- Plugins dans marketplace mais pas README → ajouter
- Ordre alphabétique dans les deux fichiers

#### 5.5 Mettre à jour la documentation `.env.claude` (si applicable)

**Condition** : Vérifie si les fichiers modifiés du plugin contiennent des références à `.env.claude` :
```bash
git diff {plugin}/ | grep -i "env\.claude\|MAIN_BRANCH\|WORKTREE_DIR\|REPO\|PROJECT"
```

**Si des variables `.env.claude` sont ajoutées ou modifiées dans les skills** :
1. Lis `docs/guide/env-claude.md` avec Read
2. Vérifie que chaque variable utilisée dans les skills modifiés est documentée dans la page
3. Pour chaque variable manquante ou obsolète :
   - Ajouter la variable dans la section "Variables disponibles" avec le même format que les existantes
   - Ajouter le skill dans le tableau "Skills qui l'utilisent" de la variable
4. Vérifier que les exemples sont cohérents avec les changements

**Si aucune référence `.env.claude` détectée** : passer cette sous-étape.

#### 5.6 Mettre à jour les badges de dépréciation dans VitePress

**Condition** : Exécuter si `{plugin}/.claude-plugin/plugin.json` contient `"deprecated": true`.

**5.6.1 Sidebar (`docs/.vitepress/config.ts`)** :
Lis le fichier. Trouve l'item sidebar correspondant au plugin (cherche `link: '/plugins/{plugin}'`). Ajoute le champ `badge` si absent :
```ts
{ text: '{Plugin}', link: '/plugins/{plugin}', badge: { text: 'Déprécié', type: 'danger' } }
```

**5.6.2 Page doc (`docs/plugins/{plugin}.md`)** :
Lis le fichier. Si le badge `Déprécié` est absent :
1. Ajouter `<Badge type="danger" text="Déprécié" />` après le badge de version dans le H1
2. Ajouter le callout juste après le H1 (avant le texte d'introduction) :
```md
::: danger Plugin déprécié
Ce plugin est remplacé par **[{replaced_by[0]}](/plugins/{replaced_by[0]})**{si plusieurs : ` et **[{replaced_by[1]}](/plugins/{replaced_by[1]})**`}. Il sera supprimé en v3.0.
:::
```

**Si aucun `deprecated: true` détecté** : passer cette sous-étape.

#### 5.7 Mettre à jour le template PR

Met à jour `.github/PULL_REQUEST_TEMPLATE/default.md` avec la liste des plugins :

1. Liste tous les dossiers contenant un `plugin.json` :
```bash
find . -name "plugin.json" -path "*/.claude-plugin/*" | sed 's|^\./||' | sed 's|/.claude-plugin/plugin.json||' | grep -v "^templates/" | sort
```

2. Génère la section "Plugin(s) concerné(s)" avec checkboxes :
```markdown
## Plugin(s) concerné(s)

<!-- Coche les plugins impactés -->

- [ ] {plugin1}
- [ ] {plugin2}
...
```

3. Remplace la section existante dans le template (entre `## Plugin(s) concerné(s)` et `## Checklist`)

**🔒 AVANT DE MARQUER COMPLETED - Vérifie ces points :**
- [ ] `README.md` global → ligne du plugin mise à jour avec nouvelle version (Read pour vérifier)
- [ ] `CHANGELOG.md` global → entrée du jour avec résumé du plugin (Read pour vérifier)
- [ ] `.claude-plugin/marketplace.json` → plugin présent avec description à jour (Read pour vérifier)
- [ ] `docs/guide/env-claude.md` → variables `.env.claude` à jour si applicable (Read pour vérifier)
- [ ] Si `deprecated: true` → `docs/.vitepress/config.ts` badge ajouté + `docs/plugins/{plugin}.md` callout ajouté (Read pour vérifier)
- [ ] `.github/PULL_REQUEST_TEMPLATE/default.md` → liste plugins synchronisée (Read pour vérifier)

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

**OBLIGATOIRE - TOUJOURS EXÉCUTER, SANS EXCEPTION** :
```bash
cd docs && npm run build
```

Vérifie que la commande s'exécute sans erreur. Si erreur, corriger avant de continuer.

#### 6.3 Vérifier les fichiers générés

```bash
git status --short docs/
```

Les fichiers `docs/plugins/{plugin}.md` et `docs/commands/index.md` doivent être modifiés.
Si nouveaux agents ajoutés, `docs/agents/index.md` doit aussi être modifié.

**🔒 AVANT DE MARQUER COMPLETED - Vérifie ces points :**
- [ ] `{plugin}/DEPENDENCIES.json` → existe (Read pour vérifier)
- [ ] `cd docs && npm run build` → exécuté avec succès (0 erreurs)
- [ ] `git status --short docs/` → au moins `docs/plugins/{plugin}.md` et `docs/commands/index.md` modifiés
- [ ] Si nouveaux agents → `docs/agents/index.md` aussi modifié

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
✓ .github/PULL_REQUEST_TEMPLATE/default.md
✓ docs/plugins/{plugin}.md
✓ docs/commands/index.md

Prochaine étape : /git:commit
```

**TaskUpdate : Tâche #6 → `completed`**

---

## Checklist de validation finale

**OBLIGATOIRE** : Avant de terminer, vérifie chaque fichier individuellement avec `git diff --name-only` et confirme que TOUS ces fichiers apparaissent dans la liste des modifiés :

### Fichiers du plugin (par plugin bumpé)
- [ ] `{plugin}/.claude-plugin/plugin.json` → version incrémentée
- [ ] `{plugin}/CHANGELOG.md` → nouvelle entrée datée du jour
- [ ] `{plugin}/README.md` → à jour si MINOR (nouveaux skills/agents documentés)

### Fichiers du marketplace (toujours)
- [ ] `README.md` → tableau des plugins avec nouvelle version
- [ ] `CHANGELOG.md` → entrée du jour avec résumé plugin
- [ ] `.claude-plugin/marketplace.json` → description à jour (si nouveau plugin)
- [ ] `docs/guide/env-claude.md` → variables `.env.claude` à jour (si nouvelles variables détectées)
- [ ] `.github/PULL_REQUEST_TEMPLATE/default.md` → liste plugins synchronisée

### Documentation générée (toujours)
- [ ] `docs/plugins/{plugin}.md` → régénéré via VitePress
- [ ] `docs/commands/index.md` → régénéré via VitePress
- [ ] `docs/agents/index.md` → régénéré si nouveaux agents

### Tâches
- [ ] Tâche #1 completed : Plugins détectés
- [ ] Tâche #2 completed : Sélection faite
- [ ] Tâche #3 completed : Fichiers plugin mis à jour
- [ ] Tâche #4 completed : Fichiers marketplace mis à jour
- [ ] Tâche #5 completed : Dépendances + VitePress rebuild
- [ ] Tâche #6 completed : Résumé affiché

**Si un fichier manque dans `git diff --name-only`, STOP : tu as oublié une étape.**

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
- `docs/guide/env-claude.md`
- `.github/PULL_REQUEST_TEMPLATE/default.md`
