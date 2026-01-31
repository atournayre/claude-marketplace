# Plugin MLVN - AIBlueprint by Melvynx

> **Source** : [github.com/melvynx/aiblueprint](https://github.com/melvynx/aiblueprint)
> **Auteur** : Melvyn (Melvynx)
> **Licence** : MIT
> **Version** : 1.0.0

Plugin Claude Code intégrant les fonctionnalités d'AIBlueprint : agents spécialisés, workflows autonomes, hooks de sécurité et skills Git/Meta/Utils.

## 📦 Installation

```bash
/plugin install mlvn@atournayre
```

## ✨ Fonctionnalités

### 🤖 Agents (4)

| Agent | Description | Modèle |
|-------|-------------|--------|
| `action` | Actions génériques | Default |
| `explore-codebase` | Exploration de codebase pour réaliser une feature | Haiku |
| `explore-docs` | Exploration de documentation | Default |
| `websearch` | Recherche web rapide | Default |

### 🔧 Skills Git (4)

| Skill | Description | Commande |
|-------|-------------|----------|
| `git-commit` | Commits rapides avec format conventionnel + auto-push | `/commit` |
| `git-create-pr` | Création automatique de Pull Request | `/create-pull-request` |
| `git-fix-pr-comments` | Résolution de commentaires PR | `/fix-pr-comments` |
| `git-merge` | Gestion des merges | `/git-merge` |

**Particularités git-commit** :
- Auto-stage si rien en staged
- Auto-push après commit
- Format conventionnel strict
- Pas d'interaction (speed over perfection)

### 🧠 Skills Meta (4)

| Skill | Description | Commande |
|-------|-------------|----------|
| `meta-claude-memory` | Gestion de CLAUDE.md | `/claude-memory` |
| `meta-prompt-creator` | Création de prompts | `/prompt-creator` |
| `meta-skill-creator` | Générateur de skills complet | `/skill-creator` |
| `meta-subagent-creator` | Générateur de subagents | `/subagent-creator` |

**meta-skill-creator** inclut :
- Processus de création en 6 étapes
- Scripts `init-skill.ts` et `package-skill.ts`
- Guides de référence : XML tags, progressive disclosure, workflows, output patterns
- Documentation officielle : https://code.claude.com/docs/llms.txt

### 🔁 Skills Workflow (3)

| Skill | Description | Commande |
|-------|-------------|----------|
| `ralph-loop` | Boucle autonome AI pour développement | `/setup-ralph` |
| `workflow-apex` | Workflow avancé (premium) | `/apex` |
| `workflow-apex-free` | Workflow avancé (version free) | `/apex-free` |

**Ralph Loop** :
- Boucle autonome de développement
- Transforme PRD en user stories
- Implémente une tâche à la fois
- Commits automatiques avec apprentissage
- Setup interactif avec `-i` flag

### 🛠️ Skills Utilities (3)

| Skill | Description | Commande |
|-------|-------------|----------|
| `utils-fix-errors` | Correction d'erreurs | `/fix-errors` |
| `utils-fix-grammar` | Correction grammaticale | `/fix-grammar` |
| `utils-oneshot` | Actions rapides | `/oneshot` |

### 🛡️ Hooks de Sécurité

**PreToolUse - Validation de commandes Bash** :
- Bloque les commandes dangereuses (`rm -rf`, etc.)
- Validation via `validate-command.js`
- Logs de sécurité dans `~/.claude/security.log`

### 📊 Scripts Utilitaires

**Statusline Scripts** :
- `spend:today` / `spend:month` / `spend:project` - Rapports de dépenses
- `stats` - Statistiques quotidiennes
- `weekly` - Analyse hebdomadaire
- `config` - Configuration interactive
- `migrate` - Migration vers SQLite

**Command Validator** :
- Validation de sécurité des commandes Bash
- Règles de sécurité configurables
- Tests unitaires inclus

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
│   ├── action.md
│   ├── explore-codebase.md
│   ├── explore-docs.md
│   └── websearch.md
├── skills/
│   ├── git-commit/
│   ├── git-create-pr/
│   ├── git-fix-pr-comments/
│   ├── git-merge/
│   ├── meta-claude-memory/
│   ├── meta-prompt-creator/
│   ├── meta-skill-creator/
│   ├── meta-subagent-creator/
│   ├── ralph-loop/
│   ├── utils-fix-errors/
│   ├── utils-fix-grammar/
│   ├── utils-oneshot/
│   ├── workflow-apex/
│   └── workflow-apex-free/
├── hooks/
│   └── hooks.json
└── scripts/
    ├── command-validator/
    └── statusline/
```

## 🤝 Contribution

Ce plugin est une intégration d'AIBlueprint dans le marketplace atournayre.

Pour contribuer au projet original :
- [github.com/melvynx/aiblueprint](https://github.com/melvynx/aiblueprint)

## 📄 Licence

MIT - Voir le projet original pour les détails.

## 👤 Crédits

**Auteur original** : Melvyn (Melvynx)
- GitHub: [@melvynx](https://github.com/melvynx)
- Email: melvyn@aiblueprint.dev

**Intégration marketplace** : Aurélien Tournayre
- GitHub: [@atournayre](https://github.com/atournayre)
- Email: aurelien.tournayre@gmail.com
