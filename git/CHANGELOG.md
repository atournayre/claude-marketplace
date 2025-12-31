# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

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
- Skills `git-pr`, `release-notes` : réduction tokens SKILL.md
  - Externalisation templates et workflows vers `references/`
  - `git-pr` : review template + todos template (lignes: 374→64)
  - `release-notes` : HTML template + writing rules (lignes: 302→62)

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
- Skill `release-notes` - Génère des notes de release HTML orientées utilisateurs finaux
  - Transformation commits techniques → descriptions accessibles
  - Catégorisation automatique (Nouveautés, Améliorations, Corrections, Sécurité)
  - Filtrage des commits internes (tests, CI, refactoring)
  - Modèle sonnet pour qualité rédactionnelle
- Commande `/git:release-notes` - Délègue au skill `release-notes`

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
