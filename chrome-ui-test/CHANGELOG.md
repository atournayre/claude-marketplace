# Changelog

Toutes les modifications notables de ce plugin seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [1.0.0] - 2026-02-01

### ✨ Ajouté

- Création du plugin `chrome-ui-test`
- Skill `/chrome-ui-test:ui-test` pour tests UI complets
- Support de la navigation et exploration de pages
- Validation visuelle avec screenshots automatiques
- Tests fonctionnels avec scénarios personnalisables
- Tests responsive (mobile, tablette, desktop)
- Mode debug avec console logs et network requests
- Enregistrement GIF des parcours utilisateur
- Génération de rapports détaillés en Markdown
- Fichier de références avec patterns courants
- Documentation complète avec exemples

**Options de viewport :**
- `--responsive` : teste les 3 viewports (mobile 375x667 + tablette 768x1024 + desktop 1920x1080)
- `--mobile` : teste uniquement mobile (375x667)
- `--tablet` : teste uniquement tablette (768x1024)
- `--desktop` : teste uniquement desktop (1920x1080)
- `--viewport=WxH` : viewport custom

**Mode Aide :**
- `--help` : affiche un résumé détaillé des actions qui seront effectuées
- Analyse toutes les options et explique ce qui va se passer
- Liste les fichiers qui seront générés
- Donne une estimation de durée
- Demande confirmation avant de continuer

### 📚 Documentation

- README complet avec cas d'usage
- Guide des patterns courants de tests
- Exemples de scénarios (login, formulaires, e-commerce)
- Bonnes pratiques et anti-patterns
- Section dépannage

### 🎯 Fonctionnalités Principales

**Navigation et Clics**
- Navigation vers URLs
- Détection et clic sur éléments
- Remplissage de formulaires
- Support form_input et computer type

**Validation Visuelle**
- Screenshots avant/après actions
- Nommage descriptif automatique
- Sauvegarde dans scratchpad

**Tests Fonctionnels**
- Scénarios en langage naturel
- Décomposition en étapes atomiques
- Validations automatiques
- Support de parcours complexes

**Tests Responsive**
- Viewports prédéfinis (mobile, tablette, desktop)
- Viewport custom (--viewport=WxH)
- Screenshots par taille d'écran
- Validation des breakpoints

**Debug**
- Lecture console messages avec filtrage
- Analyse network requests
- Détection erreurs JavaScript
- Identification requêtes échouées

**GIF Recording**
- Enregistrement automatique du parcours
- Options de qualité et overlay
- Export et téléchargement
- Frames optimisées

**Rapports**
- Format Markdown structuré
- Résumé avec compteurs (✅❌⚠️)
- Détails par catégorie
- Recommandations automatiques
- Liste des fichiers générés

### 🛠️ Outils Utilisés

- `mcp__claude-in-chrome__tabs_context_mcp` - Gestion des onglets
- `mcp__claude-in-chrome__tabs_create_mcp` - Création d'onglets
- `mcp__claude-in-chrome__navigate` - Navigation
- `mcp__claude-in-chrome__read_page` - Lecture de page
- `mcp__claude-in-chrome__find` - Recherche d'éléments
- `mcp__claude-in-chrome__computer` - Interactions (click, type, screenshot)
- `mcp__claude-in-chrome__form_input` - Remplissage de formulaires
- `mcp__claude-in-chrome__javascript_tool` - Exécution JavaScript
- `mcp__claude-in-chrome__read_console_messages` - Logs console
- `mcp__claude-in-chrome__read_network_requests` - Requêtes réseau
- `mcp__claude-in-chrome__resize_window` - Redimensionnement
- `mcp__claude-in-chrome__gif_creator` - Enregistrement GIF
- `mcp__claude-in-chrome__update_plan` - Présentation du plan

### 🎨 Options Disponibles

- `--scenario="description"` - Scénario de test
- `--responsive` - Tests multi-viewports
- `--visual` - Capture de screenshots
- `--debug` - Mode debug (console + network)
- `--gif` - Enregistrement GIF
- `--viewport=WxH` - Viewport personnalisé

### 📝 Exemples de Commandes

```bash
# Navigation simple
/chrome-ui-test:ui-test https://example.com

# Scénario login avec GIF
/chrome-ui-test:ui-test https://app.example.com/login \
  --scenario="login avec credentials" --gif

# Tests responsive
/chrome-ui-test:ui-test https://example.com --responsive --visual

# Debug
/chrome-ui-test:ui-test https://example.com/broken --debug
```

### 🔍 Fichiers Créés

- `plugin.json` - Métadonnées du plugin
- `README.md` - Documentation principale et guide de démarrage
- `CHANGELOG.md` - Historique des versions
- `skills/ui-test/SKILL.md` - Définition de la skill
- `skills/ui-test/references/common-patterns.md` - Patterns de référence
- `skills/ui-test/references/examples.md` - 12+ exemples détaillés

### 🎯 Prochaines Versions (Roadmap)

**v1.1.0 (Prévu)**
- Skill dédiée pour tests de performance
- Mesure des métriques Core Web Vitals
- Détection automatique de memory leaks

**v1.2.0 (Prévu)**
- Support des tests A/B (comparaison de 2 versions)
- Skill pour tests d'accessibilité (WCAG)
- Génération de rapports HTML interactifs

**v2.0.0 (Prévu)**
- Intégration avec outils de CI/CD
- Export des résultats en JSON/JUnit
- Scheduler de tests récurrents
