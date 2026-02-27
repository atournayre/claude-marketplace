## [1.14.2] - 2026-02-27

### Fixed
- **Skills PR** - Créer les PR en draft par défaut pour limiter l'exécution automatique de la CI
  - Ajout du flag `--draft` à la création de PR (`safe_push_pr.sh`)
  - Les PR restent en draft jusqu'à confirmation manuelle pour éviter les faux positifs CI

## [1.14.1] - 2026-02-20

### Added
- Release for marketplace

### Changed
- Documentation updates

## [1.14.0] - 2026-02-08

### Added
- **Skill `/git:ci-autofix`** - Parse logs CI et corrige automatiquement les erreurs
  - Catégorise erreurs : linting, tests, build, types
  - Boucle auto-correction (max 3 tentatives)
  - Intégration avec `@phpstan-error-resolver` et scripts de correction

### Changed
- **Scripts Git durcis** : `set -euo pipefail` partout, `eval` supprimé, `mktemp + trap`, guard inputs vides
  - `analyze_changes.sh` : factorisation triple appel git diff
  - `auto_review.sh` : vérification `jq`/`gh`, guard diff vide
  - `create_pr.sh` : cleanup fichiers temporaires via trap
  - `gh_auth_setup.sh` : suppression eval, tableau bash
  - `final_report.sh` : guard PR_INFO vide

### Fixed
- Scripts shell : gestion d'erreurs robuste, pas de sortie trompeuse sur input vide

## [1.13.0] - 2026-02-08

### Added
- **New skill `git:worktree`** - Création de worktrees Git parallèles avec nommage automatique
  - Support issues GitHub et texte descriptif (même logique que `git:branch`)
  - Configuration `WORKTREE_DIR` via `.env.claude` du projet utilisateur
  - Convention répertoire : branche `feature/ma-fonctionnalite` → répertoire `feature-ma-fonctionnalite`
  - Première mise à jour depuis SOURCE_BRANCH avant création (via `fetch`)
  - Utilisateur reste sur sa branche courante dans le worktree principal

- **Refactorisation `git:branch`** - Mutualis logique de nommage de branches
  - Extraction de la détection de nom dans `branch-core/scripts/resolve-branch-name.sh`
  - SOURCE_BRANCH optionnel (défaut: `MAIN_BRANCH` de `.env.claude`)
  - Désambiguisation intelligente des arguments (issue vs texte vs branche existante)
  - Nettoyage de code et meilleure maintenabilité

### Changed
- **Scripts partagés** : nouvelle skill `git-branch-core` (interne)
  - `resolve-branch-name.sh` - Résolution nom branche depuis issue/texte (utilisé par branch + worktree)
  - `validate-source-branch.sh` - Validation branche source existe
  - `check-branch-exists.sh` - Vérification branche pas déjà existante
  - Version skills `git:branch` et `git:worktree` → `2.0.0`

- **Argument parsing** : nouvelle logique de désambiguisation
  - 2 arguments : `<source-branch> <issue-or-text>`
  - 1 argument entier : issue (source = MAIN_BRANCH)
  - 1 argument branche existante : source (issue demandé)
  - 1 argument texte : issue-or-text (source = MAIN_BRANCH)
  - 0 argument : source = MAIN_BRANCH, issue demandé

## [1.12.2] - 2026-02-08

### Fixed
- **PR title suffix** : Ajouter ` / Issue #NUMERO` au titre des PR quand créées depuis une issue
  - Modification dans `git-pr-core/scripts/create_pr.sh`
  - Modification dans `git-cd-pr/scripts/create_pr.sh`
  - Le suffixe est ajouté automatiquement si un numéro d'issue est détecté dans le nom de branche

## [1.12.1] - 2026-02-06

### Changed
- **Skill rename** : `release-notes` → `gen-release-notes`
  - Renamed skill to avoid conflicts with native command
  - Updated all documentation references
  - Usage: `/git:gen-release-notes` (instead of `/git:release-notes`)

## [1.12.0] - 2026-02-04

### Added
- **Task Management System obligatoire** dans `git:commit` skill
  - Chaque étape du workflow trackée via TaskCreate/TaskUpdate
  - Création de 5 tâches (workflow complet)
  - Validation de progression avant continuation
  - Checklists pour validation finale

### Changed
- **Refonte complète de la documentation `git:commit`** (version 2.0.0 du SKILL.md)
  - Instructions réorganisées avec Task Management System
  - Ajout des permissions manquantes : TaskCreate, TaskUpdate, TaskList
  - Nouvelle stratégie de commit avec détection de division automatique
  - Table consolidée des emojis par type de commit (20+ catégories)
  - Clarification du workflow en 6 étapes majeures
  - Exemples HEREDOC pour création commits atomiques
  - Directives de division des commits (feat + docs, fix + refactor, etc.)
  - Pattern obligatoire : Documentation → Implémentation → Test

## [1.11.1] - 2026-02-04

### Changed
- Migrer noms de modèles Claude vers format court (sonnet, haiku, opus)

# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.11.0] - 2026-01-31

### Added
- **Skill `/fix-pr-comments`** - Implémente systématiquement TOUS les commentaires de review PR
  - Fetch automatique via `gh pr review list` + `gh api`
  - Batched MultiEdit pour same-file modifications (efficacité)
  - ALWAYS Read files BEFORE editing (sécurité)
  - Checklist avec progression visible
  - STAY IN SCOPE : never fix unrelated issues
  - Auto-commit + auto-push
  - Migré depuis mlvn plugin (AIBlueprint v1.0.0)

### Changed
- **Skill `/git:commit`** - Documentation clarifiée sur auto-push
  - Auto-push activé PAR DÉFAUT (déjà existant)
  - Flag `--no-push` pour désactiver
  - Tracking intelligent avec `git push -u` si premier commit
  - Cette fonctionnalité existait déjà, documentation mise à jour pour clarté

## [1.10.2] - 2026-01-26

### Removed
- Commandes legacy : `git:branch`, `git:commit`, `git:conflit`, `git:git-cd-pr`, `git:git-pr-core`, `git:git-pr`, `git:gen-release-notes`, `git:release-report`
  - Migrées vers plugin centralisé `command` (workaround issue #15178)
  - Skills restent fonctionnels via le plugin `command`

## [1.10.1] - 2026-01-25

### Changed
- Commande `/git:commit` - Mise à jour légacy command reference vers skill

## [1.10.0] - 2026-01-25

### Added
- Commande `/git:branch` - Création de branche Git avec workflow structuré
- Commande `/git:commit` - Créer des commits bien formatés avec format conventional et emoji
- Commande `/git:conflit` - Analyse les conflits git et propose à l'utilisateur une résolution pas à pas avec validation de chaque étape.
- Commande `/git:git-cd-pr` - Crée une Pull Request en mode Continuous Delivery avec workflow complet : QA, labels version (major/minor/patch), feature flags, code review automatique.
- Commande `/git:git-pr-core` - Skill interne fournissant les scripts communs pour la création de Pull Requests. Ne pas appeler directement - utilisé par git-pr et git-cd-pr.
- Commande `/git:git-pr` - Crée une Pull Request GitHub standard avec workflow complet : QA, commits, assignation milestone/projet, code review automatique.
- Commande `/git:gen-release-notes` - Génère des notes de release HTML orientées utilisateurs finaux. Transforme les commits techniques en descriptions accessibles sans jargon.
- Commande `/git:release-report` - Génère un rapport HTML d'analyse d'impact entre deux branches

## [1.9.2] - 2026-01-24

### Changed
- Stabilisation des skills suite à migration commands → skills

## [1.9.1] - 2026-01-24

### Changed
- Intégration du task management system dans 3 skills git/ :
  - `git-pr` - 13 tâches (workflow création PR standard)
  - `git-cd-pr` - 15 tâches (workflow CD avec labels version)
  - `git:gen-release-notes` - 5 tâches (génération notes de release)
- Ajout de TaskCreate/TaskUpdate pour suivi progression
- Documentation patterns task management et dépendances

## [1.9.0] - 2026-01-22

### Changed
- Migration de 4 commands vers le format skills (branch, commit, conflit, release-report)
- Préservation des hooks avancés (validation, push automatique, feedback)
- Format natif Claude Code avec support complet frontmatter YAML

### Removed
- Répertoire /commands/ - complètement migré en /skills/

## [1.8.2] - 2026-01-18

### Fixed
- Documentation des scripts `assign_milestone.py` et `assign_project.py` dans `git-pr-core/SKILL.md`
  - Clarification de la syntaxe requise : `--milestone "<name>"` et `--project "<name>"`
  - Ajout d'exemples corrects/incorrects pour éviter les erreurs d'appel
  - Références croisées dans les skills `git-pr` et `git-cd-pr`

## [1.8.1] - 2026-01-15

### Fixed
- Script `detect_cd_mode.sh` : ajout du flag `--limit 1000` pour lister tous les labels
  - Évite la limite par défaut de 30 labels qui causait des faux négatifs
  - Améliore la fiabilité de la détection du mode CD sur repos avec 30+ labels

## [1.8.0] - 2026-01-10

### Added
- **Script QA externe** : `git/commands/scripts/qa-before-pr.sh`
  - Détection automatique des outils QA disponibles (PHPStan, PHPUnit, PHP-CS-Fixer)
  - Fallbacks multiples : make → vendor/bin → composer
  - Pas d'échec si outil manque, feedback clair sur exécution
  - Réutilisable par n'importe quelle commande

### Changed
- **Hooks pour commandes** : Validation et automatisation ajoutées
  - `/git:commit` : Validation QA avec `--verify`, vérification workspace propre, push automatique avec tracking intelligent
  - `/git:branch` : Blocage si modifications non commitées, validation branche source, feedback création
  - `/git:pr` : Vérification branche à jour, QA complète avant création PR
- **Corrections** : `argument-hint` au format correct pour toutes les commandes (`argument-hint: <requis> [optionnel]`)
  - `/git:pr`, `/git:commit`, `/git:gen-release-notes`, `/git:release-report` normalisés

## [1.7.7] - 2026-01-08

### Fixed
- Documentation clarifiée pour le flag `--delete` : supprime UNIQUEMENT la branche locale
- Règles critiques ajoutées dans les skills `git:pr` et `git:cd-pr` pour éviter suppression branche remote
- Commentaire renforcé dans `cleanup_branch.sh` expliquant pourquoi la branche remote ne doit jamais être supprimée

## [1.7.6] - 2026-01-05

### Fixed
- Correction du chemin du script de détection de mode CD dans la commande `/git:pr`

## [1.7.5] - 2026-01-02

### Added
- Support `.env.claude` pour configuration defaults dans `/git:pr` et `/git:cd-pr`
  - Lecture automatique de `MAIN_BRANCH`, `REPO`, `PROJECT` depuis `.env.claude`
  - Fallback sur valeurs par défaut si variables absentes
  - Utilisé automatiquement si arguments non fournis

### Changed
- Skills `git:pr` et `git:cd-pr` : ajout support flag `--no-interaction`
  - Permet d'automatiser création PR sans demandes de confirmation
  - Utilise valeurs pré-remplies (arguments + `.env.claude`)
  - Essentiel pour workflows entièrement automatisés
- Commande `/git:pr` : argument-hint mis à jour pour inclure `--no-interaction`

## [1.7.4] - 2026-01-02

### Changed
- Commande `/git:branch` : détection automatique du préfixe de branche
  - Basée sur les labels de l'issue GitHub (priorité haute)
  - Basée sur les mots-clés dans la description de l'issue
  - Basée sur les mots-clés dans le titre de l'issue (dernier recours)
  - Préfixes supportés : `feature/`, `fix/`, `hotfix/`, `chore/`, `docs/`, `test/`
  - Détection pour texte descriptif : analyse du préfixe explicite au début du texte
  - Améliore la cohérence du nommage des branches sans intervention manuelle

## [1.7.3] - 2025-12-31

### Added
- **Script `detect_cd_mode.sh`** : détection fiable du mode CD
  - Analyse TOUS les labels du repo sans troncature
  - Empêche les modifications ad-hoc de la commande de détection
  - Exit codes : 0 (CD détecté) / 1 (mode standard)

### Changed
- Commande `/git:pr` : utilise désormais le script dédié pour la détection du mode
  - Meilleure fiabilité avec repos ayant 20+ labels
  - Instructions claires d'exécution sans modifications

## [1.7.2] - 2025-12-31

### Changed
- Skills `git:pr` et `git:cd-pr` : ajout d'étape de confirmation initiale avant exécution
  - Affichage du nom de la skill lancée
  - Résumé de tous les paramètres reçus (branche, milestone, projet, flags)
  - Demande de confirmation explicite avant de continuer le workflow

## [1.7.1] - 2025-12-30

### Changed
- Commande `/git:commit` : reformulation instructions en format impératif pour exécution fiable
  - Format documentaire → instructions explicites ("Exécute", "Analyse", "Crée")
  - Utilisation HEREDOC pour éviter problèmes permissions bash sur `git commit -m`
  - Clarification étapes workflow pour comportement stable

## [1.7.0] - 2025-12-27

### Added
- **git-pr-core skill** : centralisation du workflow PR standard
  - Scripts core partagés : `safe_push_pr.sh`, `create_pr.sh`, `final_report.sh`, etc.
  - Support assignation milestone et projet GitHub
  - Code review automatique multi-agents
  - Templates références (review et todos)

- **git-cd-pr skill** : workflow PR optimisé pour Continuous Delivery
  - Héritage des fonctionnalités core
  - Copie automatique des labels d'issue (`copy_issue_labels.sh`)
  - Détection intelligente du type de version CD (`apply_cd_labels.sh`)
  - Labels version (major/minor/patch) et feature flags automatiques

### Changed
- Refactoring : migration du skill `git-pr` vers architecture modulaire (core + variants)
- Dépendances entre skills sont maintenant explicites et testées
- Structure : skills spécialisés hériten du core pour éviter duplication

## [1.6.0] - 2025-12-26

### Added
- Script `copy_issue_labels.sh` : copie automatique des labels d'une issue liée vers la PR
  - Extraction des labels via `gh issue view`
  - Application à la PR via `gh pr edit`
  - Messages informatifs si issue sans labels ou introuvable

- Script `apply_cd_labels.sh` : labels CD (Continuous Delivery) automatiques
  - Détection CD via présence des labels `version:*` dans le repo
  - Détection intelligente du type de version avec 5 stratégies de fallback :
    1. Breaking change dans commits (`!:` ou `BREAKING CHANGE`)
    2. Labels de l'issue liée (insensible casse, ignore emojis/préfixes)
    3. Nom de branche (`feat/*` → minor, `fix/*` → patch)
    4. Premier commit de la branche
    5. Demande utilisateur si indéterminé (exit code 2)
  - Label `🚩 Feature flag` si composant `Feature:Flag` détecté dans fichiers Twig modifiés
  - Création automatique des labels manquants avec couleurs appropriées

### Changed
- Skill `git-pr` : intégration des nouveaux scripts de labels dans le workflow
  - Copie labels issue après création PR
  - Application labels CD si projet en CD

## [1.5.0] - 2025-12-20

### Added
- Script utilitaire `scripts/commit-emoji.sh` : source de vérité unique pour le mapping type → emoji
  - Support 16 types de commits (feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert, wip, hotfix, security, deps, breaking)
  - Réutilisable par tous les scripts et skills du plugin
  - Peut être sourcé ou appelé directement

### Changed
- Skill `git-pr` : utilisation du script centralisé `commit-emoji.sh` pour la génération des titres PR
  - Titres PR au format `emoji type(scope): description` conforme aux conventions
  - Détection automatique du type depuis le nom de branche
  - Scope optionnel détecté (format `type/scope/description`)
  - Description depuis issue #N ou nom de branche
  - Fallback sur `chore` si type non reconnu

## [1.4.18] - 2025-12-20

### Changed
- Commande `git:commit` : réoptimisation options pour meilleur workflow
- Ajout du champ `output-style` dans le frontmatter des commandes pour formatage automatique
  - `git:branch` → `ultra-concise`
  - `git:release-report` → `html-structured`

## [1.4.17] - 2025-12-20

### Changed
- Skills `git-pr`, `gen-release-notes` : réduction tokens SKILL.md
  - Externalisation templates et workflows vers `references/`
  - `git-pr` : review template + todos template (lignes: 374→64)
  - `gen-release-notes` : HTML template + writing rules (lignes: 302→62)

## [1.4.16] - 2025-12-17

### Changed
- Skill `git-pr` : délégation review au plugin `review` avec 4 agents spécialisés
  - Vérification automatique présence plugin review
  - Invocation parallèle des 4 agents (code-reviewer, silent-failure-hunter, test-analyzer, git-history-reviewer)
  - Message d'incitation si plugin review non installé
  - Agrégation des résultats avec filtrage score >= 80

### Removed
- Agent `git-history-reviewer` déplacé vers plugin `review`

## [1.4.15] - 2025-12-17

### Added
- Agent `git-history-reviewer` : analyse le contexte historique git pour détecter problèmes potentiels
  - Git blame des lignes modifiées
  - Historique commits sur fichiers touchés
  - PRs précédentes pertinentes
  - TODOs/FIXMEs existants
  - Scoring de confiance (seuil 70)

### Changed
- Skill `git-pr` : intégration analyse historique dans review automatique
  - Contexte historique git (blame, commits récents)
  - Détection patterns récurrents et régressions potentielles
  - Section "Contexte historique" dans rapport review
  - Checklist "TODOs existants adressés"

## [1.4.14] - 2025-12-14

### Changed
- Commande `/git:branch` : modèle sonnet → haiku (création branche simple, plus rapide)
- Commande `/git:commit` : modèle sonnet → haiku (message commit simple, plus rapide)
- Skill `git-pr` : suppression `/clear` inutile (simplification workflow)

## [1.4.13] - 2025-12-08

### Changed
- Skill `git-pr` : exécution `/clear` en début de workflow pour nettoyer le contexte

## [1.4.12] - 2025-12-03

### Fixed
- Skill `git-pr` : correction chemin `SCRIPTS_DIR` (suppression `/git/` dupliqué)
- Skill `git-pr` : utilisation Bash heredoc au lieu de Write tool pour `/tmp/pr_body_generated.md` (évite échec Write + fallback)

## [1.4.11] - 2025-12-02

### Changed
- Skill `git-pr` : utilisation variable `${CLAUDE_PLUGIN_ROOT}` au lieu de chemins absolus (portabilité)
- Skill `git-pr` : skip appel `confirm_base_branch.py` quand branche de base fournie en argument

### Fixed
- Cache scopes GitHub (TTL 1h) pour éviter vérifications répétées à chaque PR

## [1.4.10] - 2025-11-27

### Added
- Support des branches `hotfix/*` comme branche de base pour les PR

## [1.4.9] - 2025-11-26

### Added
- Skill `gen-release-notes` - Génère des notes de release HTML orientées utilisateurs finaux
  - Transformation commits techniques → descriptions accessibles
  - Catégorisation automatique (Nouveautés, Améliorations, Corrections, Sécurité)
  - Filtrage des commits internes (tests, CI, refactoring)
  - Modèle sonnet pour qualité rédactionnelle
- Commande `/git:gen-release-notes` - Délègue au skill `gen-release-notes`

## [1.4.8] - 2025-11-26

### Changed
- `/git:release-report` demande interactivement les arguments obligatoires manquants (branche-source, branche-cible)

## [1.4.7] - 2025-11-21

### Fixed
- Suppression scope `read:project` obsolète des requis GitHub
- Correction parsing des scopes dans `check_scopes.sh`

## [1.4.6] - 2025-11-21

### Changed
- Review automatique intelligente : `auto_review.sh` récupère les données JSON, Claude analyse et génère une vraie review (conformité template, qualité code, tests, documentation, suggestions)

## [1.4.5] - 2025-11-21

### Added
- Scripts bash modulaires pour workflow PR : `auto_review.sh`, `check_scopes.sh`, `create_pr.sh`, `final_report.sh`

### Changed
- Documentation SKILL.md renforcée pour imposer utilisation scripts Python avec cache (milestone/projet)

## [1.4.4] - 2025-11-20

### Fixed
- Génération titre PR explicite basée sur le titre de l'issue (détection depuis nom de branche)

## [1.4.3] - 2025-11-20

### Fixed
- Interdiction explicite `gh pr edit --add-project` (Projects classic deprecated)
- Documentation API GraphQL V2 (`addProjectV2ItemById`) pour assignation projets

## [1.4.2] - 2025-11-20

### Fixed
- Génération aliases milestone supportant formes courtes ("26" → "26.0.0 (Avenant)")
- Renforcement SKILL.md pour imposer utilisation scripts Python avec cache (milestone/projet)

## [1.4.1] - 2025-11-15

### Fixed
- Corrections mineures et stabilité

## [1.4.0] - 2025-11-15

### Added
- Commande `/git:release-report` - Génère rapports HTML d'analyse d'impact pour releases

## [1.3.0] - Date antérieure

### Added
- Documentation arguments commande `/git:pr`

### Changed
- Amélioration workflow Pull Requests

## [1.2.0] - Date antérieure

### Added
- Cache persistant pour milestones GitHub
- Cache projets GitHub

### Changed
- Réorganisation tests

## [1.1.1] - Date antérieure

### Fixed
- Correction référence skill `git:git-pr`

## [1.1.0] - Date antérieure

### Added
- Skill `git:git-pr` - Workflow création Pull Requests optimisé

### Changed
- Déplacement skill git-pr depuis plugin dev vers git

## [1.0.0] - Version initiale

### Added
- Commande `/git:branch` - Création branches Git structurée
- Commande `/git:commit` - Commits conventional avec emoji
- Commande `/git:conflit` - Résolution conflits git assistée
- Commande `/git:pr` - Création Pull Requests GitHub
