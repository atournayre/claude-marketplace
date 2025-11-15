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

## ✨ Nouveautés v1.1.0

### Skills Spécialisés

3 nouveaux skills ont été ajoutés pour automatiser des tâches complexes :

**🐙 github-impact** (`github` plugin v1.1.0)
- Analyse complète des PR (fichiers, dépendances, tests, sécurité)
- Génération 2 rapports (métier + technique)
- Intégration automatique dans description PR
- Utilisation : `/github:impact <pr-number>`

**🔍 phpstan-resolver** (`qa` plugin v1.1.0)
- Résolution automatique erreurs PHPStan
- Boucle itérative avec détection stagnation
- Batch processing (5 erreurs/fichier/itération)
- Utilisation : `/qa:phpstan`

**📚 doc-loader** (`doc` plugin v1.1.0)
- Chargement documentation multi-framework
- Support 5 frameworks (Symfony, API Platform, Meilisearch, atournayre-framework, Claude Code)
- Cache intelligent 24h + anti-rate-limiting
- Utilisation : `/doc:framework-load <framework> [version]`

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
