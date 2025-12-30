# Claude Plugin Marketplace

> ⚠️ **DISCLAIMER:** Ce marketplace est en cours de développement actif. Utilise-le avec précaution et n'hésite pas à remonter tout bug ou comportement inattendu via les issues GitHub.

Marketplace de plugins pour Claude Code, offrant un ensemble d'outils pour améliorer ton workflow de développement.

## 📦 Plugins Disponibles

| Plugin | Version | Description | Documentation |
|--------|---------|-------------|---------------|
| 🤖 **Claude** | 1.0.0 | Plugin de base pour Claude Code avec commandes essentielles | [README](claude/README.md) |
| 🎨 **Customize** | 1.0.0 | Personnalise ton expérience avec hooks, output styles et status lines | [README](customize/README.md) |
| ⚙️ **Dev** | 2.1.2 | Workflow structuré 8 phases + toolkit complet | [README](dev/README.md) |
| 🔧 **Git** | 1.7.1 | Workflow Git complet : branches, commits, conflits, PR avec labels CD + issue labels | [README](git/README.md) |
| 🐙 **GitHub** | 1.1.2 | Gestion GitHub : issues, PR, analyse d'impact | [README](github/README.md) |
| 📋 **QA** | 1.2.1 | Quality assurance : PHPStan, tests, linters | [README](qa/README.md) |
| 📚 **Doc** | 1.1.3 | Documentation : ADR, RTFM, génération docs, framework docs | [README](doc/README.md) |
| 🎯 **Symfony** | 1.0.1 | Plugin Symfony avec commandes make, documentation et intégrations | [README](symfony/README.md) |
| 🏗️ **Framework** | 1.0.1 | Skills framework pour génération code PHP Elegant Objects | [README](framework/README.md) |
| 🔮 **Gemini** | 1.0.1 | Délégation Gemini CLI : contexte ultra-long (1M tokens), Deep Think, Google Search | [README](gemini/README.md) |
| 🔍 **Review** | 1.0.0 | Agents spécialisés code review : code-reviewer, silent-failure-hunter, test-analyzer, git-history-reviewer | [README](review/README.md) |
| 📱 **Marketing** | 1.0.1 | Génération de contenu marketing : posts LinkedIn, annonces, communications | [README](marketing/README.md) |

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
