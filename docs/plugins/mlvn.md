---
title: "mlvn"
description: "Adaptation du repo AIBlueprint de Melvynx - Agents spécialisés, workflows autonomes et skills Git/Meta/Utils"
version: "1.1.0"
---

# mlvn <Badge type="info" text="v1.1.0" />

> **🔗 Ce plugin est une adaptation du repo [AIBlueprint de Melvynx](https://github.com/Melvynx/aiblueprint)**
>
> **Auteur original** : Melvyn (Melvynx)
> **Adaptation pour marketplace** : Aurélien Tournayre (@atournayre)
> **Licence** : MIT

Plugin Claude Code adaptant les fonctionnalités d'AIBlueprint : agents spécialisés, workflows autonomes, hooks de sécurité et skills Git/Meta/Utils.

## Installation

```bash
/plugin install mlvn@atournayre
```

## ℹ️ Note de Migration

**⚠️ Attention** : Ce plugin a été partiellement **démantelé** et ses composants migrés vers des plugins spécialisés dans le marketplace pour éviter les doublons et améliorer la maintenabilité.

**Éléments migrés** :
- ✅ **Bash Security Validator** → `customize` v1.1.0 (hook PreToolUse, 82+ tests)
- ✅ **skill-creator** → `claude` v1.3.0 (progressive disclosure)
- ✅ **memory** → `claude` v1.3.0 (4-level hierarchy)
- ✅ **make-subagent** → `claude` v1.3.0
- ✅ **fix-pr-comments** → `git` v1.11.0 (batched MultiEdit)
- ✅ **oneshot** → `dev` v2.5.0
- ✅ **ralph-loop** → `dev` v2.5.0 (setup-ralph)
- ✅ **fix-grammar** → `utils` v1.0.0
- ✅ **action agent** → `utils` v1.0.0
- ✅ **explore-codebase agent** → `utils` v1.0.0

## ✨ Fonctionnalités (Restantes)

### 🤖 Agents (2)

| Agent | Description | Modèle |
|-------|-------------|--------|
| `explore-docs` | Exploration de documentation | Default |
| `websearch` | Recherche web rapide | Default |

### 🔧 Skills Git (3)

| Skill | Description | Commande |
|-------|-------------|----------|
| `git-commit` | Commits rapides avec format conventionnel + auto-push | `/commit` |
| `git-create-pr` | Création automatique de Pull Request | `/create-pull-request` |
| `git-merge` | Gestion des merges | `/git-merge` |

### 🧠 Skills Meta (1)

| Skill | Description | Commande |
|-------|-------------|----------|
| `meta-prompt-creator` | Création de prompts | `/prompt-creator` |

### 🔁 Skills Workflow (2)

| Skill | Description | Commande |
|-------|-------------|----------|
| `workflow-apex` | Workflow avancé (premium) | `/apex` |
| `workflow-apex-free` | Workflow avancé (version free) | `/apex-free` |

### 🛠️ Skills Utilities (1)

| Skill | Description | Commande |
|-------|-------------|----------|
| `utils-fix-errors` | Correction d'erreurs | `/fix-errors` |

### 📊 Scripts Utilitaires

**Statusline Scripts** :
- `spend:today` / `spend:month` / `spend:project` - Rapports de dépenses
- `stats` - Statistiques quotidiennes
- `weekly` - Analyse hebdomadaire
- `config` - Configuration interactive
- `migrate` - Migration vers SQLite

## 🚀 Exemples d'Utilisation

### Commit rapide
```bash
/commit
```
→ Auto-stage, commit conventionnel, auto-push

### Créer une PR
```bash
/create-pull-request
```
→ Génère titre + description, crée la PR

### Ralph Loop
```bash
/setup-ralph -i
# Puis lancer : bun run .claude/ralph/ralph.sh -f feature-name
```
→ Développement autonome par itérations

### Créer un skill
```bash
/skill-creator
```
→ Guide complet pour créer des skills efficaces

### Exploration de codebase
```bash
# Utiliser l'agent explore-codebase
```
→ Recherche parallèle, import chains, patterns découverts

## 📚 Documentation Complète

- [AIBlueprint Documentation](https://codelynx.dev/docs)
- [Premium Features](https://mlv.sh/claude-cli)
- [Claude Code Skills Guide](https://code.claude.com/docs/llms.txt)

## ⚙️ Configuration

### Dépendances optionnelles
- `bun` - Pour exécuter les scripts TypeScript
- `ccusage` - Pour le tracking des coûts
- `gh` - Pour les intégrations GitHub

### Structure du plugin
```
mlvn/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── explore-docs.md      (CONSERVÉ)
│   └── websearch.md         (CONSERVÉ)
├── skills/
│   ├── git-commit/          (CONSERVÉ)
│   ├── git-create-pr/       (CONSERVÉ)
│   ├── git-merge/           (CONSERVÉ)
│   ├── meta-prompt-creator/ (CONSERVÉ)
│   ├── utils-fix-errors/    (CONSERVÉ)
│   ├── workflow-apex/       (CONSERVÉ)
│   └── workflow-apex-free/  (CONSERVÉ)
└── scripts/
    └── statusline/          (CONSERVÉ)
```

## 🤝 Contribution

Ce plugin est une adaptation d'AIBlueprint dans le marketplace atournayre.

Pour contribuer au projet original :
- [github.com/melvynx/aiblueprint](https://github.com/melvynx/aiblueprint)

## 👤 Crédits

**Auteur original** : Melvyn (Melvynx)
- GitHub: [@melvynx](https://github.com/melvynx)
- Email: melvyn@aiblueprint.dev

**Intégration marketplace** : Aurélien Tournayre
- GitHub: [@atournayre](https://github.com/atournayre)
- Email: aurelien.tournayre@gmail.com

## 📄 Licence

MIT - Voir le [projet original](https://github.com/Melvynx/aiblueprint) pour les détails.
