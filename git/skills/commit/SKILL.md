---
name: git:commit
description: Créer des commits bien formatés avec format conventional et emoji
model: haiku
allowed-tools: [Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*), Bash(git push:*), TaskCreate, TaskUpdate, TaskList]
argument-hint: [message] [--verify] [--no-push]
version: 2.0.0
license: MIT
hooks:
  PreToolUse:
    - matcher: "Bash(git status:*)"
      hooks:
        - type: command
          command: |
            # Hook: Vérifier qu'il y a des changements à committer
            if git diff --cached --quiet && git diff --quiet; then
              echo "❌ Aucun changement détecté (stagé ou non stagé)"
              exit 1
            fi
          once: true
    - matcher: "Bash(git commit:*)"
      hooks:
        - type: command
          command: |
            # Hook: Vérifier si --verify est passé en argument
            if echo "$ARGUMENTS" | grep -q -- "--verify"; then
              echo "🔍 Exécution de make qa..."
              make qa || {
                echo "❌ QA échouée. Voulez-vous continuer quand même ?"
                exit 1
              }
            fi
          once: false
  PostToolUse:
    - matcher: "Bash(git commit:*)"
      hooks:
        - type: command
          command: |
            # Hook: Push automatique avec tracking intelligent
            BRANCH=$(git branch --show-current)
            echo "✅ Commit créé : $(git log -1 --oneline)"

            # Vérifier si --no-push est passé
            if echo "$ARGUMENTS" | grep -q -- "--no-push"; then
              echo "📝 Commit local uniquement (--no-push)"
              exit 0
            fi

            # Vérifier si la branche a un tracking remote
            if ! git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
              echo "🚀 Premier commit sur $BRANCH - configuration du tracking..."
              git push -u origin "$BRANCH"
              echo "✅ Branche pushée et tracking configuré"
            else
              echo "🚀 Push vers origin/$BRANCH..."
              git push
              echo "✅ Commit pushé"
            fi
          once: false
---

# Workflow Git Commit

Créer un commit bien formaté avec les arguments : $ARGUMENTS

## IMPORTANT : Task Management System obligatoire

**RÈGLE CRITIQUE** : Chaque étape DOIT être trackée via TaskCreate/TaskUpdate.
- Créer TOUTES les tâches AVANT de commencer
- Marquer `in_progress` au début de chaque étape
- Marquer `completed` UNIQUEMENT quand l'étape est 100% terminée
- NE JAMAIS sauter une étape

## Instructions à Exécuter

### Étape 1 : Créer TOUTES les tâches du workflow

**OBLIGATOIRE** : Utilise TaskCreate pour créer ces 5 tâches dans cet ordre exact :

```
TaskCreate #1: "Vérifier les changements disponibles"
  - activeForm: "Checking available changes"
  - description: "git status + git diff pour voir les fichiers modifiés"

TaskCreate #2: "Analyser le diff des changements"
  - activeForm: "Analyzing diff content"
  - description: "git diff --cached pour comprendre les changements"

TaskCreate #3: "Déterminer la stratégie de commit"
  - activeForm: "Determining commit strategy"
  - description: "Décider si un ou plusieurs commits sont nécessaires"

TaskCreate #4: "Créer le(s) commit(s)"
  - activeForm: "Creating commit(s)"
  - description: "git commit avec message formaté emoji + conventional"

TaskCreate #5: "Push vers remote"
  - activeForm: "Pushing to remote"
  - description: "git push (sauf si --no-push)"
```

**Après création** : Affiche `TaskList` pour confirmer que les 5 tâches existent.

---

### Étape 2 : Vérifier les changements disponibles

**TaskUpdate : Tâche #1 → `in_progress`**

Exécute en parallèle :
```bash
git status
git diff --cached --stat
```

**Traitement** :

1. **SI** aucun changement (ni stagé, ni non-stagé) :
   - Affiche "❌ Aucun changement à committer"
   - **TaskUpdate : Tâche #1 → `completed`**
   - **STOP** - Ne pas continuer

2. **SI** des fichiers modifiés mais rien de stagé :
   - Exécute `git add .` pour tout stager
   - Exécute `git status` pour confirmer

3. **SI** des fichiers déjà stagés :
   - Continue avec ces fichiers uniquement

**TaskUpdate : Tâche #1 → `completed`**

---

### Étape 3 : Analyser le diff des changements

**TaskUpdate : Tâche #2 → `in_progress`**

Exécute en parallèle :
```bash
git diff --cached
git log -5 --oneline
```

**Traitement** :
1. Lis TOUT le diff des changements stagés
2. Note le style des commits récents du repo
3. Identifie les types de changements présents :
   - feat (nouvelles fonctionnalités)
   - fix (corrections de bugs)
   - docs (documentation)
   - refactor (refactorisation)
   - test (tests)
   - chore (configuration, maintenance)
   - style (formatage)
   - perf (performance)

**TaskUpdate : Tâche #2 → `completed`**

---

### Étape 4 : Déterminer la stratégie de commit

**TaskUpdate : Tâche #3 → `in_progress`**

**Critères pour DIVISER en plusieurs commits :**
1. Préoccupations distinctes (feat + docs + tests mélangés)
2. Types de changements différents (fix + refactor)
3. Fichiers non-liés modifiés ensemble
4. Diff > 200 lignes sur sujets différents

**SI plusieurs types détectés :**
- Liste les commits à créer
- Pour chaque commit, utilise :
  ```bash
  git reset HEAD <fichiers-à-exclure>
  git commit -m "..."
  git add <fichiers-suivants>
  ```

**SINON :**
- Continue avec un seul commit

**TaskUpdate : Tâche #3 → `completed`**

---

### Étape 5 : Créer le(s) commit(s)

**TaskUpdate : Tâche #4 → `in_progress`**

**Pour CHAQUE commit à créer :**

#### 5.1 Déterminer le message

1. **Type** : feat, fix, docs, refactor, test, chore, style, perf, ci, revert
2. **Emoji** : Voir table ci-dessous
3. **Scope** : Optionnel, entre parenthèses (auth, api, ui...)
4. **Description** : < 72 caractères, mode impératif, présent

#### 5.2 Exécuter le commit

**OBLIGATOIRE : Utilise TOUJOURS un HEREDOC pour le message :**

```bash
git commit -m "$(cat <<'EOF'
<emoji> <type>(<scope>): <description courte>

<détails optionnels - explique le "pourquoi">
EOF
)"
```

**Exemple simple :**
```bash
git commit -m "$(cat <<'EOF'
✨ feat(auth): ajouter connexion OAuth Google
EOF
)"
```

**Exemple avec corps :**
```bash
git commit -m "$(cat <<'EOF'
🐛 fix(api): corriger fuite mémoire dans le cache

Le cache ne libérait pas les entrées expirées, causant une
augmentation progressive de la mémoire utilisée.

Fixes #123
EOF
)"
```

**TaskUpdate : Tâche #4 → `completed`**

---

### Étape 6 : Push vers remote

**TaskUpdate : Tâche #5 → `in_progress`**

#### 6.1 Vérifier l'option --no-push

**SI** `--no-push` présent dans $ARGUMENTS :
- Affiche "📝 Commit local uniquement (--no-push)"
- **TaskUpdate : Tâche #5 → `completed`**
- **STOP** - Workflow terminé

#### 6.2 Push automatique

Le hook PostToolUse gère automatiquement :
- Premier push : `git push -u origin <branch>`
- Push suivants : `git push`

**TaskUpdate : Tâche #5 → `completed`**

---

## Checklist de validation finale

Avant de terminer, vérifie que TOUTES ces conditions sont remplies :

- [ ] Tâche #1 completed : Changements vérifiés et stagés
- [ ] Tâche #2 completed : Diff analysé
- [ ] Tâche #3 completed : Stratégie déterminée
- [ ] Tâche #4 completed : Commit(s) créé(s) avec HEREDOC
- [ ] Tâche #5 completed : Push effectué (ou skip si --no-push)

**Si une tâche n'est pas completed, NE PAS terminer.**

---

## Table des Emojis par Type

| Type | Emoji | Usage |
|------|-------|-------|
| feat | ✨ | Nouvelle fonctionnalité |
| fix | 🐛 | Correction de bug |
| docs | 📝 | Documentation |
| style | 💄 | Formatage/style (pas de changement de logique) |
| refactor | ♻️ | Refactorisation de code |
| perf | ⚡️ | Amélioration de performance |
| test | ✅ | Ajout/modification de tests |
| chore | 🔧 | Outils, configuration, maintenance |
| ci | 🚀 | CI/CD |
| revert | ⏪️ | Annulation de changements |

### Emojis Spécialisés

| Contexte | Emoji | Description |
|----------|-------|-------------|
| Breaking change | 💥 | Changement cassant |
| Security | 🔒️ | Sécurité |
| Hotfix | 🚑️ | Correction critique urgente |
| Typo | ✏️ | Faute de frappe |
| WIP | 🚧 | Travail en cours |
| Lint/warnings | 🚨 | Correction warnings linter |
| Dependencies + | ➕ | Ajout dépendance |
| Dependencies - | ➖ | Suppression dépendance |
| Database | 🗃️ | Changements BDD |
| Logs + | 🔊 | Ajout de logs |
| Logs - | 🔇 | Suppression de logs |
| Types | 🏷️ | Définitions de types |
| UX | 🚸 | Amélioration UX |
| Accessibility | ♿️ | Accessibilité |
| i18n | 🌐 | Internationalisation |
| Business logic | 👔 | Logique métier |
| Architecture | 🏗️ | Changements architecturaux |
| Dead code | ⚰️ | Suppression code mort |
| Remove files | 🔥 | Suppression fichiers |
| Move/rename | 🚚 | Déplacement/renommage |
| Assets | 🍱 | Assets (images, etc.) |
| UI animations | 💫 | Animations UI |
| Validation | 🦺 | Code de validation |
| Feature flags | 🚩 | Feature flags |
| Analytics | 📈 | Tracking/analytics |
| CI fix | 💚 | Correction CI |
| Snapshot tests | 📸 | Tests snapshot |
| Mock | 🤡 | Mocking |
| Experiment | ⚗️ | Expérimentations |
| Seed data | 🌱 | Données de seed |
| .gitignore | 🙈 | Fichier .gitignore |
| License | 📄 | Licence |
| Contributors | 👥 | Contributeurs |
| DX | 🧑‍💻 | Developer Experience |
| Responsive | 📱 | Design responsive |
| SEO | 🔍️ | SEO |
| Offline | ✈️ | Support offline |
| Concurrency | 🧵 | Multithreading |
| Easter egg | 🥚 | Easter egg |
| Comments | 💡 | Commentaires dans le code |
| Text/literals | 💬 | Textes et littéraux |
| External API | 👽️ | Changements API externe |
| Error handling | 🥅 | Gestion d'erreurs |
| Simple fix | 🩹 | Fix non-critique simple |
| Package build | 📦️ | Fichiers compilés/packages |
| Pin deps | 📌 | Épingler versions |
| Release tag | 🔖 | Tags de release |
| Init project | 🎉 | Début de projet |
| Merge | 🔀 | Fusion de branches |

---

## Format du Message de Commit

```
<emoji> <type>(<scope>): <description impérative courte>

[corps optionnel - explique le "pourquoi" pas le "quoi"]

[footer optionnel - références issues, breaking changes]
```

### Règles du Message

1. **Première ligne** : < 72 caractères
2. **Mode impératif** : "ajouter" pas "ajouté"
3. **Présent** : "corrige" pas "a corrigé"
4. **Pas de point final** sur la première ligne
5. **Ligne vide** entre titre et corps
6. **Corps** : explique le contexte et la raison

---

## Options de Commande

| Option | Description |
|--------|-------------|
| `--verify` | Exécute `make qa` avant le commit |
| `--no-push` | Ne push pas automatiquement après le commit |

**Combinaison possible :** `/git:commit --verify --no-push`

---

## Directives de Division

Divise les commits si tu détectes :
1. **feat + docs** → 2 commits séparés
2. **fix + refactor** → 2 commits séparés
3. **test + implementation** → peut être ensemble si cohérent
4. **chore (deps) + feat** → toujours séparés
5. **Plusieurs features distinctes** → 1 commit par feature
