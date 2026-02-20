---
name: dev:auto:feature
description: Workflow complet de développement automatisé (mode non-interactif)
argument-hint: <issue-number>
model: sonnet
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Task
  - Bash
version: 1.0.0
license: MIT
---

> ⚠️ **Déprécié** : Cette skill est remplacée par `orchestrator:feature`. Voir le plugin `orchestrator`. Sera supprimée en v3.0.

# Objectif

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


Orchestrateur du workflow de développement en 10 phases **SANS interaction utilisateur**.

Exécution automatique complète : récupérer issue → phases 1-8 → cleanup → créer PR.
Objectif : PR créée et prête pour review, CI passe.

# Issue GitHub

Issue #$ARGUMENTS (spec récupérée automatiquement)

# ⚠️ MODE NON-INTERACTIF

Ce workflow s'exécute automatiquement **sans checkpoints utilisateur**.

- **Worktree OBLIGATOIRE** : créé et nettoyé automatiquement
- **0 interaction requise** : heuristiques appliquées à chaque décision
- **CI DOIT PASSER** : PHPStan niveau 9, tests
- **Auto-fix en boucle** : max 3 tentatives en Phase 6, puis rollback si échec

Pour un workflow interactif avec validation à chaque phase, utilise `/dev:feature`.

# Prérequis obligatoires

Exécuter `/dev:auto:check-prerequisites` pour vérifier que TOUS les prérequis sont présents.

Exit code 1 et arrêt si quelque chose manque.

# Workflow

## Phase 0 : Vérifier les prérequis

**🔄 Progression :** `TaskUpdate` → tâche #0 en `in_progress`

**⏱️ Démarrer le timer**

Exécuter `/dev:auto:check-prerequisites`

Si la skill exit 1, arrêter immédiatement.

**⏱️ Arrêter le timer**

**🔄 Progression :** `TaskUpdate` → tâche #0 en `completed`

**Affichage :**
```
✅ Prérequis vérifiés

Tous les outils nécessaires sont présents :
  ✅ gh CLI authentifiée
  ✅ jq disponible
  ✅ git disponible

Lancement du workflow...
```

## Phase 1 : Fetch Issue (Initialisation)

**⏱️ Démarrer le timer**

**Déterminer le chemin :**

```bash
issue_number=$ARGUMENTS
workflow_state_file=".claude/data/workflows/issue-${issue_number}-dev-workflow-state.json"

# Créer le répertoire s'il n'existe pas
mkdir -p ".claude/data/workflows"
```

Exécuter `/dev:auto:fetch-issue $ARGUMENTS`

**Processus :**
- Valider que l'argument est un numéro d'issue
- Récupérer l'issue GitHub via `gh issue view`
- Vérifier que l'issue est OPEN et a une description
- Sauvegarder les infos dans `${workflow_state_file}`

Si `/dev:auto:fetch-issue` échoue :
- Exit avec code 1
- Afficher le message d'erreur explicite
- Arrêter

**⏱️ Arrêter le timer**

**Affichage :**
```
🔗 Issue GitHub récupérée

  #123 : Description du feature
  État : OPEN
  Labels : enhancement

Lancement du workflow...
```

## Initialisation

### 1. Créer automatiquement le worktree (OBLIGATOIRE)

```
🤖 Mode automatique activé pour : {feature}

📂 Création du worktree...
```

**Processus :**
- Normaliser le nom de la feature en slug (kebab-case, minuscules, tirets)
- Créer le répertoire `.worktrees/` s'il n'existe pas
- Créer le worktree avec `/dev:worktree create {feature-slug}`
- Mettre à jour `.claude/data/workflows/issue-${issue_number}-dev-workflow-state.json`

**Si création échoue :**
→ **FAIL HARD** avec message d'erreur et exit code 1.

### 2. Initialiser le fichier d'état

Le fichier `.claude/data/workflows/issue-{issue_number}-dev-workflow-state.json` a déjà été créé par Phase 0 avec les infos de l'issue.

Mettre à jour le fichier pour ajouter les infos du worktree :

```json
{
  "mode": "auto",
  "issue": {
    "number": {numéro},
    "title": "{issue title}",
    "description": "{issue body}",
    "labels": "{issue labels}",
    "state": "OPEN",
    "fetchedAt": "{ISO timestamp}"
  },
  "feature": "{issue title}",
  "status": "in_progress",
  "startedAt": "{ISO timestamp}",
  "currentPhase": 1,
  "worktree": {
    "name": "{feature-slug}",
    "path": ".worktrees/{feature-slug}",
    "branch": "feature/{feature-slug}",
    "cleaned": false,
    "branchDeleted": false
  },
  "autoConfig": {
    "worktreeCreated": true,
    "decisions": {},
    "autoFixAttempts": {}
  },
  "timing": {
    "totalDurationMs": null
  },
  "phases": {}
}
```

### 3. Créer les tâches du workflow

Utiliser `TaskCreate` pour chaque phase :

```
TaskCreate #0: Prérequis - Vérifier les outils
TaskCreate #1: Fetch - Récupérer l'issue GitHub
TaskCreate #2: Discover - Comprendre le besoin
TaskCreate #3: Explore - Explorer codebase
TaskCreate #4: Clarify - Heuristiques automatiques
TaskCreate #5: Design - Architecture (Pragmatic)
TaskCreate #6: Plan - Générer specs
TaskCreate #7: Code - Implémenter
TaskCreate #8: Review - Auto-fix × 3
TaskCreate #9: Cleanup - Nettoyer worktree
TaskCreate #10: Create PR - Créer la Pull Request
```

**Important :**
- Utiliser `activeForm` (ex: "Vérifiant les outils", "Récupérant l'issue GitHub")
- Toutes les tâches sont créées d'office (mode automatique)

### 4. Afficher le statut initial

```
🤖 Workflow automatique : {feature}

  🔵 0. Prérequis  - Vérifier les outils        ← En cours
  ⬜ 1. Fetch      - Récupérer l'issue GitHub
  ⬜ 2. Discover   - Comprendre le besoin
  ⬜ 3. Explore    - Explorer codebase
  ⬜ 4. Clarify    - Heuristiques automatiques
  ⬜ 5. Design     - Architecture (Pragmatic)
  ⬜ 6. Plan       - Générer specs
  ⬜ 7. Code       - Implémenter
  ⬜ 8. Review     - Auto-fix × 3
  ⬜ 9. Cleanup    - Nettoyer worktree
  ⬜ 10. Create PR - Créer la Pull Request
```

## Gestion du timing et progression

**⚠️ IMPORTANT :** Chaque phase suit ce pattern :
1. `TaskUpdate` → tâche en `in_progress`
2. ⏱️ Démarrer le timer + exécuter la phase
3. ⏱️ Arrêter le timer
4. `TaskUpdate` → tâche en `completed`

**Avant chaque phase :**
1. Utiliser `TaskUpdate` pour marquer la tâche comme `in_progress`
2. Enregistrer le timestamp de début :
```json
{
  "phases": {
    "{N}": { "status": "in_progress", "startedAt": "{ISO timestamp}" }
  }
}
```

**Après chaque phase :**
1. Calculer la durée et mettre à jour :
```json
{
  "phases": {
    "{N}": {
      "status": "completed",
      "startedAt": "{ISO timestamp}",
      "completedAt": "{ISO timestamp}",
      "durationMs": {durée en millisecondes}
    }
  }
}
```
2. Utiliser `TaskUpdate` pour marquer la tâche comme `completed`

**Pattern illustré dans Phase 0 - À reproduire pour toutes les phases 1-10.**

## Phase 1 : Discover

**⏱️ Démarrer le timer**

Exécuter `/dev:auto:discover`

Si `/dev:auto:discover` échoue (ambiguïté critique) :
- Exit avec code 1
- Cleanup worktree
- Arrêter

**⏱️ Arrêter le timer**

**Affichage :**
```
✅ Phase 1 : Discover complétée (45s)
🔵 Phase 2 : Explore en cours
```

## Phase 3 : Explore

**⏱️ Démarrer le timer**

Exécuter `/dev:auto:explore` (exploration codebase sans interaction)

**Time-box :** si exploration dépasse 5 minutes, passer à la phase suivante avec résultats partiels. Enregistrer `timebox_triggered: true` dans le workflow state.

**⏱️ Arrêter le timer**

## Phase 4 : Clarify

**⏱️ Démarrer le timer**

Exécuter `/dev:auto:clarify` (applique heuristiques, zéro question)

**⏱️ Arrêter le timer**

## Phase 5 : Design

**⏱️ Démarrer le timer**

Exécuter `/dev:auto:design` (choisit Pragmatic Balance automatiquement)

**⏱️ Arrêter le timer**

## Phase 6 : Plan

**⏱️ Démarrer le timer**

Exécuter `/dev:auto:plan` (génération plan sans interaction)

**⏱️ Arrêter le timer**

## Phase 7 : Code

**⏱️ Démarrer le timer**

Exécuter `/dev:auto:code` (implémente directement, pas d'approbation)

**⏱️ Arrêter le timer**

## Phase 8 : Review

**⏱️ Démarrer le timer**

Exécuter `/dev:auto:review` (boucle auto-fix max 3 tentatives)

**Si review échoue (PHPStan impossible) :**
- Logger l'erreur dans workflow-state.json
- **Déclencher ROLLBACK** :
  ```bash
  git reset --hard HEAD@{0}
  /dev:worktree remove {feature-name}
  ```
- Mettre à jour workflow-state.json avec `status: "failed"`
- Exit code 1 avec message explicite

**⏱️ Arrêter le timer**

**Si succès :**
- Continuer à Phase 8

**⏱️ Calculer le temps total :**
1. Lire `.claude/data/workflows/issue-${issue_number}-dev-workflow-state.json`
2. Calculer `totalDurationMs` = somme de tous les `durationMs` des phases
3. Mettre à jour le fichier avec `timing.totalDurationMs`

## Phase 9 : Cleanup (OBLIGATOIRE)

**⏱️ Démarrer le timer**

**Nettoyage automatique du worktree :**

```
🧹 Nettoyage du worktree...
```

1. Vérifier que worktree a été créé (vérifier workflow state)
2. Exécuter `/dev:worktree remove {feature-name}` automatiquement
3. Ne PAS supprimer la branche (elle sera utilisée pour la PR en Phase 10)
4. Mettre à jour workflow state :
```json
{
  "status": "in_progress",
  "completedAt": "{ISO timestamp}",
  "worktree": {
    "cleaned": true,
    "branchDeleted": false,
    "cleanedAt": "{ISO timestamp}"
  }
}
```

**⏱️ Arrêter le timer**

**Affichage :**
```
✅ Phase 9 : Cleanup complétée (5s)
🔵 Phase 10 : Create PR en cours
```

## Phase 10 : Create PR (AUTOMATISÉE)

**⏱️ Démarrer le timer**

Récupérer la branche-base et le projet depuis `.env.claude` (ou valeurs par défaut) :

```bash
MAIN_BRANCH=${MAIN_BRANCH:-main}
PROJECT=${PROJECT:-}
```

Exécuter `/git:pr` avec les paramètres du workflow automatique :

```bash
/git:pr $MAIN_BRANCH $PROJECT --no-interaction
```

**Paramètres :**
- `$MAIN_BRANCH` : branche de base (depuis `.env.claude` MAIN_BRANCH ou "main")
- `$PROJECT` : projet GitHub (depuis `.env.claude` PROJECT ou vide)
- `--no-interaction` : mode automatique, passer confirmations

Si `/git:pr` échoue (ex: branche inexistante, GitHub unreachable) :
- Logger l'erreur dans workflow state
- Exit code 1 avec message explicite

**⏱️ Arrêter le timer**

**Nettoyage du workflow state :**

```bash
# Supprimer le fichier de workflow state
rm -f ".claude/data/workflows/issue-${issue_number}-dev-workflow-state.json"
```

**Affichage final :**
```
✅ SUCCÈS - Workflow terminé

🎉 Feature prête pour Pull Request
✅ CI PASSE (PHPStan niveau 9, tests)
📂 Worktree nettoyé
🔗 PR créée : https://github.com/...#<pr-number>

Affichage du récapitulatif des temps (voir section "Récapitulatif final")
```

# Affichage du statut

**Deux systèmes complémentaires :**

1. **Task Management System** : Les tâches sont automatiquement mises à jour, `TaskList` peut être consulté

2. **Affichage manuel avec timings** : À chaque transition de phase, afficher le statut mis à jour avec timing :

```
🤖 Workflow automatique : {feature}

  ✅ 0. Prérequis  - Vérifier les outils        (1s)
  ✅ 1. Fetch      - Récupérer l'issue GitHub     (2s)
  ✅ 2. Discover   - Comprendre le besoin        (45s)
  ✅ 3. Explore    - Explorer codebase           (2m 30s)
  ✅ 4. Clarify    - Heuristiques automatiques   (20s)
  🔵 5. Design     - Architecture (Pragmatic)    ← En cours
  ⬜ 6. Plan       - Générer specs
  ⬜ 7. Code       - Implémenter
  ⬜ 8. Review     - Auto-fix × 3
  ⬜ 9. Cleanup    - Nettoyer worktree
  ⬜ 10. Create PR - Créer la Pull Request
```

**Note :** Le task system ne gère pas les timings, donc l'affichage manuel reste nécessaire pour montrer les durées.

Pas d'arrêt : exécution continue jusqu'à fin ou échec.

# Affichage du timing

## Format de durée

Formater les durées de manière lisible :
- `< 60s` → `{X}s` (ex: `45s`)
- `< 60min` → `{X}m {Y}s` (ex: `2m 30s`)
- `>= 60min` → `{X}h {Y}m` (ex: `1h 15m`)

## Récapitulatif final

À la fin du workflow (après phase 7, avant cleanup), afficher :

```
⏱️ Récapitulatif des temps

  Phase 0. Prérequis :  1s
  Phase 1. Fetch     :  2s
  Phase 2. Discover  :  45s
  Phase 3. Explore   :  2m 30s
  Phase 4. Clarify   :  20s
  Phase 5. Design    :  1m 15s
  Phase 6. Plan      :  50s
  Phase 7. Code      :  8m 20s
  Phase 8. Review    :  2m 45s
  Phase 9. Cleanup   :  5s
  Phase 10. Create PR:  10s
  ────────────────────────────
  Total              : 17m 23s
```

# Gestion des erreurs bloquantes

## Si une phase échoue (ex: Phase 0, Phase 7)

### 1. Logger l'erreur

Mettre à jour `.claude/data/workflows/issue-{issue_number}-dev-workflow-state.json` :
```json
{
  "status": "failed",
  "failedAt": "{ISO timestamp}",
  "failurePhase": {numéro},
  "failureReason": "Description de l'erreur",
  "errors": ["error1", "error2"]
}
```

### 2. Rollback automatique

```bash
git reset --hard HEAD@{0}
```

### 3. Cleanup worktree

```bash
/dev:worktree remove {feature-name}
```

Mettre à jour workflow state avec `cleaned: true`, `branchDeleted: true`, `rollback: true`.

### 4. Exit avec code d'erreur

```
❌ ÉCHEC du workflow automatique

Raison : {failureReason}
Phase échouée : {failurePhase}

Erreurs :
{liste des erreurs}

Le worktree a été nettoyé et la branche supprimée.
Utilise /dev:feature pour un workflow interactif.

Exit code: 1
```

# Règles

- **Worktree OBLIGATOIRE** en mode auto (création et cleanup)
- **0 checkpoints utilisateur** (aucune interaction)
- **Task Management** :
  - Créer les 11 tâches (0-10) à l'initialisation
  - Mettre à jour le statut avant/après chaque phase (in_progress → completed)
  - Les tâches se mettent à jour automatiquement en mode auto
- **Timing enregistré** pour chaque phase dans workflow state JSON
- **CI DOIT PASSER** (PHPStan niveau 9, tests)
- **Rollback automatique** en cas d'erreur bloquante
- **Cleanup automatique** avant création PR
- **PR créée automatiquement** via `/git:pr`
- **Mettre à jour** `.claude/data/workflows/issue-{issue_number}-dev-workflow-state.json` après chaque phase
- **Afficher le statut** à chaque transition (task system + timings)
- **Ne jamais sauter de phase** (0 à 10 obligatoires)

# Cas limites

## Ambiguïté non-résoluble (Phase 0)

```
Description : "Ajouter auth"
→ Trop vague (OAuth? Basic? JWT?)

Action : FAIL dans discover
Message : "Description trop ambiguë pour mode auto.
           Précise : OAuth? Basic Auth? JWT?
           Ou utilise /dev:feature pour mode interactif."
Exit code: 1
```

## Conflit worktree existant

```
Nom feature : "oauth-auth"
Worktree .worktrees/oauth-auth existe déjà

Action : Suffixe automatique
→ .worktrees/oauth-auth-2
Et logger warning dans workflow state
```

## Branche feature existe déjà

Vérifier avec `git show-ref refs/heads/feature/{name}`.
Si existe → FAIL dans initialisation.

# Comparaison avec /dev:feature

| Aspect | `/dev:feature` | `/dev:auto:feature` |
|--------|---|---|
| **Input** | Description texte libre | **Numéro issue GitHub** |
| **Interaction** | 5 checkpoints | **0 checkpoint** |
| **Worktree** | Optionnel | **OBLIGATOIRE** |
| **Phase 3** | Questions utilisateur | **Heuristiques** |
| **Phase 4** | Choix utilisateur | **Auto Pragmatic** |
| **Phase 6** | Approbation requise | **Immédiat** |
| **Phase 7** | Fix now/later/proceed | **Auto-fix × 3** |
| **Phase 8** | Proposer nettoyage | **Cleanup auto** |
| **Phase 9** | Manuel : `/git:pr` | **Auto : `/git:pr` + params** |
| **Erreurs** | Demander aide | **Rollback auto** |
| **Objectif** | Collaboration | **Automation** |
