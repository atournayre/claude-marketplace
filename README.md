# Claude Plugin Marketplace

> ⚠️ **DISCLAIMER:** Ce marketplace est en cours de développement actif. Utilise-le avec précaution et n'hésite pas à remonter tout bug ou comportement inattendu via les issues GitHub.

Marketplace de plugins pour Claude Code, offrant un ensemble d'outils pour améliorer ton workflow de développement.

## 📦 Plugins Disponibles

| Plugin | Version | Description | Documentation |
|--------|---------|-------------|---------------|
| 🤖 **Claude** | 1.0.0 | Plugin de base pour Claude Code avec commandes essentielles | [README](claude/README.md) |
| 🎨 **Customize** | 1.0.0 | Personnalise ton expérience avec hooks, output styles et status lines | [README](customize/README.md) |
| ⚙️ **Dev** | 2.0.0 | Workflow structuré 8 phases + toolkit complet | [README](dev/README.md) |
| 🔧 **Git** | 1.4.16 | Workflow Git complet : branches, commits, conflits, PR | [README](git/README.md) |
| 🐙 **GitHub** | 1.1.0 | Gestion GitHub : issues, PR, analyse d'impact | [README](github/README.md) |
| 📋 **QA** | 1.2.0 | Quality assurance : PHPStan, tests, linters | [README](qa/README.md) |
| 📚 **Doc** | 1.1.1 | Documentation : ADR, RTFM, génération docs, framework docs | [README](doc/README.md) |
| 🎯 **Symfony** | 1.0.0 | Plugin Symfony avec commandes make, documentation et intégrations | [README](symfony/README.md) |
| 📊 **Output Styles** | 1.0.0 | Styles de sortie personnalisés pour formater les réponses | [README](output-styles/README.md) |
| 🏗️ **Framework** | 1.0.0 | Skills framework pour génération code PHP Elegant Objects | [README](framework/README.md) |
| 🔮 **Gemini** | 1.0.0 | Délégation Gemini CLI : contexte ultra-long (1M tokens), Deep Think, Google Search | [README](gemini/README.md) |
| 🔍 **Review** | 1.0.0 | Agents spécialisés code review : code-reviewer, silent-failure-hunter, test-analyzer, git-history-reviewer | [README](review/README.md) |

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
