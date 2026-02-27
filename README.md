# Claude Plugin Marketplace

> ⚠️ **DISCLAIMER:** Ce marketplace est en cours de développement actif. Utilise-le avec précaution et n'hésite pas à remonter tout bug ou comportement inattendu via les issues GitHub.

Marketplace de plugins pour Claude Code, offrant un ensemble d'outils pour améliorer ton workflow de développement.

## 📦 Plugins Disponibles

| Plugin | Version | Description | Documentation |
|--------|---------|-------------|---------------|
| 🔬 **Analyst** | 1.1.0 | Analyse architecture + design DDD : explore le codebase, propose l'architecture technique et conçoit le modèle de domaine | [README](analyst/README.md) |
| 🏗️ **Architect** | 1.1.0 | Analyse l'architecture, les patterns et la structure du codebase pour proposer une conception technique solide | [README](architect/README.md) |
| 🌐 **Chrome UI Test** | 1.0.1 | Tests automatisés d'interface utilisateur dans Chrome (navigation, screenshots, responsive, GIF) | [README](chrome-ui-test/README.md) |
| 🤖 **Claude** | 1.3.2 | Plugin de base : skill-creator, memory, make-subagent, challenge, doc-loader | [README](claude/README.md) |
| 🎨 **Customize** | 1.1.3 | Personnalise ton expérience avec hooks, output styles, status lines + Bash Security Validator + PHPStan hook | [README](customize/README.md) |
| ⚙️ **Dev** | 2.6.1 | Workflow 8 phases + oneshot, ralph-loop, examine step + 28 skills (implement, parallel-implement, refactor-safe) | [README](dev/README.md) |
| 📚 **Doc** | 1.6.2 | Documentation : ADR, RTFM, génération docs, framework docs + 3 skills | [README](doc/README.md) |
| 🚀 **DevOps** | 1.1.0 | Pipeline CD/CI automation : branche, commit, PR, release-notes, conflict resolution, ci-autofix | [README](devops/README.md) |
| 📖 **Documenter** | 1.1.0 | Extraction et sauvegarde automatique de documentation : API Platform, Symfony, Meilisearch, atournayre-framework, Claude Code | [README](documenter/README.md) |
| 🏗️ **Framework** | 1.1.2 | Skills framework pour génération code PHP Elegant Objects | [README](framework/README.md) |
| 🔮 **Gemini** | 1.4.3 | Délégation Gemini CLI : contexte ultra-long (1M tokens), Deep Think, Google Search + 3 skills | [README](gemini/README.md) |
| 🔧 **Git** | 1.14.2 | Workflow Git complet : branches, worktrees, commits, conflits, PR, fix-pr-comments, ci-autofix + Task Management System | [README](git/README.md) |
| 🐙 **GitHub** | 1.3.3 | Gestion GitHub : issues, PR, analyse d'impact | [README](github/README.md) |
| 🛠️ **Implementer** | 1.1.0 | Implémentation code + tests TDD : agents developer et implementer pour execution complète des plans | [README](implementer/README.md) |
| 🔨 **Infra** | 1.1.0 | Infrastructure et configuration : skills, agents, hooks, règles projet et meta-agent creator | [README](infra/README.md) |
| 📱 **Marketing** | 1.2.2 | Génération de contenu marketing : posts LinkedIn, annonces, communications | [README](marketing/README.md) |
| 🎭 **MLVN** | 1.1.1 | Adaptation du repo AIBlueprint de Melvynx : agents spécialisés, workflows, skills Git/Meta/Utils (version épurée après migration) | [README](mlvn/README.md) |
| 🔔 **Notifications** | 1.0.3 | Système de notifications avancé avec queue persistante, dispatchers multiples et gestion complète | [README](notifications/README.md) |
| 🎼 **Orchestrator** | 1.1.0 | Orchestration multi-phase : check-prerequisites, discover, explore, design, plan, implement, review, validate | [README](orchestrator/README.md) |
| 🐘 **PHP** | 1.1.0 | Génération code PHP Elegant Objects : make-entity, make-contracts, make-collection, make-factory, etc. | [README](php/README.md) |
| 📝 **Prompt** | 2.3.2 | Système hybride Starters + Mode Plan + Checklists + Agent Teams - Templates légers, exploration contextuelle, validation automatisée, orchestration multi-agents + contraintes architecturales | [README](prompt/README.md) |
| 📋 **QA** | 1.3.4 | Quality assurance : PHPStan, tests, linters + anti-suppression automatique | [README](qa/README.md) |
| 🔍 **Researcher** | 1.1.0 | Recherche temps réel : Google Search via Gemini, analyse docs, agents spécialisés | [README](researcher/README.md) |
| 🔍 **Review** | 1.0.2 | Agents spécialisés code review : code-reviewer, silent-failure-hunter, test-analyzer, git-history-reviewer | [README](review/README.md) |
| 📊 **Reviewer** | 1.1.0 | Revue complète : PHPStan resolver, Elegant Objects reviewer, git-history reviewer, code reviewer, QA, silent failures | [README](reviewer/README.md) |
| 🎯 **Symfony** | 1.3.2 | Plugin Symfony avec skills make, documentation et intégrations | [README](symfony/README.md) |
| 🧪 **Tester** | 1.1.0 | Tests et QA : test-analyzer, tester agents pour exécution PHPUnit et validation | [README](tester/README.md) |
| 🛠️ **Utils** | 1.0.1 | Skills et agents utilitaires : fix-grammar, action, explore-codebase | [README](utils/README.md) |

## 🎨 Convention Output Styles

Certaines commandes du marketplace spécifient un **output-style** recommandé dans leur frontmatter pour optimiser le formatage de sortie.

### Fonctionnement

Chaque commande concernée inclut un champ `output-style` dans son frontmatter YAML :

```yaml
---
description: Génère un rapport HTML d'analyse d'impact
output-style: html-structured
---
```

Lors de l'exécution, Claude détecte ce champ et bascule automatiquement vers le style approprié.

### Styles Utilisés

| Style | Usage | Commandes |
|-------|-------|-----------|
| `html-structured` | Rapports HTML complets | `git:release-report` |
| `markdown-focused` | Documentation structurée | `doc:adr`, `marketing:linkedin`, `doc:rtfm` |
| `ultra-concise` | Statuts et résumés courts | `dev:status`, `dev:summary`, `git:branch` |
| `bullet-points` | Analyses et explorations | `dev:explore`, `dev:discover`, `gemini:analyze`, `github:impact` |
| `table-based` | Comparaisons structurées | `dev:design`, `dev:clarify` |

### Configuration des Styles

Les output-styles sont définis dans `~/.claude/output-styles/`. Claude Code les charge automatiquement au démarrage.

Pour créer un style personnalisé, crée un fichier `~/.claude/output-styles/mon-style.md` :

```markdown
---
name: Mon Style Custom
description: Description du style
---

Instructions de formatage pour Claude...
```

### Feature Request

Le champ `output-style` dans le frontmatter n'est **pas encore supporté nativement** par Claude Code. Nous avons soumis une [feature request](FEATURE_REQUEST.md) pour ajouter ce support.

En attendant, les commandes incluent une instruction manuelle pour que Claude lise et applique le style automatiquement.

**Voir** : [FEATURE_REQUEST.md](FEATURE_REQUEST.md) pour les détails techniques et la proposition complète.

## 🚀 Installation

### Ajouter le Marketplace

```bash
/plugin marketplace add atournayre/claude-marketplace
```

### Installer un Plugin

```bash
/plugin install <nom-plugin>@atournayre
```

**Exemples :**
```bash
/plugin install claude@atournayre
/plugin install git@atournayre
/plugin install symfony@atournayre
```

### Installer Tous les Plugins

```bash
/plugin
```

Sélectionne "Browse Plugins" et installe les plugins souhaités.

### Configuration Équipe

`.claude/settings.json` :
```json
{
  "plugins": {
    "marketplaces": ["atournayre/claude-marketplace"],
    "installed": [
      "claude@atournayre",
      "dev@atournayre",
      "git@atournayre",
      "symfony@atournayre"
    ]
  }
}
```

Installation automatique au trust du projet.

## 🧪 Tests

Lance tous les tests du projet:

```bash
./run_tests.sh
```

Chaque skill peut avoir son dossier `tests/` avec `run_tests.sh`.

## 🤝 Contribution

Contributions bienvenues via issues ou PR.

## 📄 Licence

MIT

## 👤 Auteur

**Aurélien Tournayre**
- GitHub: [@atournayre](https://github.com/atournayre)
- Email: aurelien.tournayre@gmail.com
