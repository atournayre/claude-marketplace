# Claude Plugin Marketplace

> ⚠️ **DISCLAIMER:** Ce marketplace est en cours de développement actif. Utilise-le avec précaution et n'hésite pas à remonter tout bug ou comportement inattendu via les issues GitHub.

Marketplace de plugins pour Claude Code, offrant un ensemble d'outils pour améliorer ton workflow de développement.

## 📦 Plugins Disponibles

| Plugin | Description | Documentation |
|--------|-------------|---------------|
| 🤖 **Claude** | Plugin de base pour Claude Code avec commandes essentielles | [README](claude/README.md) |
| 🎨 **Customize** | Personnalise ton expérience avec hooks, output styles et status lines | [README](customize/README.md) |
| ⚙️ **Dev** | Toolkit complet de développement pour PHP | [README](dev/README.md) |
| 🔧 **Git** | Workflow Git complet : branches, commits, conflits, PR | [README](git/README.md) |
| 🐙 **GitHub** | Gestion GitHub : issues, PR, analyse d'impact | [README](github/README.md) |
| 📋 **QA** | Quality assurance : PHPStan, tests, linters | [README](qa/README.md) |
| 📚 **Doc** | Documentation : ADR, RTFM, génération docs, framework docs | [README](doc/README.md) |
| 🎯 **Symfony** | Plugin Symfony avec commandes make, documentation et intégrations | [README](symfony/README.md) |
| 📊 **Output Styles** | Styles de sortie personnalisés pour formater les réponses | [README](output-styles/README.md) |

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

## ⚙️ Configuration des Plugins

Les plugins peuvent être configurés via `.claude/plugins.settings.json`.

### Structure

```json
{
  "atournayre-claude-plugin-marketplace": {
    "plugin-name": {
      "option": "value"
    }
  }
}
```

### Hiérarchie

Le fichier de configuration suit la même hiérarchie que `settings.json` :
- **Global** : `~/.claude/plugins.settings.json`
- **Projet** : `.claude/plugins.settings.json`

Les valeurs du projet écrasent les valeurs globales.

### Exemple Complet

`.claude/plugins.settings.json` :
```json
{
  "atournayre-claude-plugin-marketplace": {
    "git": {
      "default_branch": "main",
      "conventional_commits": true,
      "emoji": true,
      "auto_push": false,
      "pr": {
        "auto_delete_branch": false,
        "auto_request_review": true
      }
    },
    "qa": {
      "phpstan": {
        "level": 9,
        "auto_fix": true
      }
    }
  }
}
```

### Utilisation

Les commandes utilisent automatiquement la config si arguments non fournis.

Exemple :
```bash
# Sans config : arguments obligatoires
/git:branch main 123

# Avec config default_branch: "main"
/git:branch 123
```

Voir README de chaque plugin pour options disponibles.

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
