# Standards Qualité - Claude Plugin Marketplace

Ce document définit les standards de qualité pour tous les plugins du marketplace.

## 📋 Checklist Qualité Plugin

### Obligatoire (MUST HAVE)

- [x] **plugin.json** : Métadonnées complètes (name, description, version, author, keywords)
- [x] **README.md** : Documentation complète des skills/agents avec exemples
- [x] **CHANGELOG.md** : Historique versions au format Keep a Changelog
- [x] **DEPENDENCIES.json** : Liste dépendances critiques/optionnelles
- [x] **Ajout marketplace.json** : Plugin référencé dans `.claude-plugin/marketplace.json`
- [x] **Ajout README global** : Ligne dans tableau README.md racine
- [x] **Ajout CHANGELOG global** : Entry dans CHANGELOG.md racine

### Recommandé (SHOULD HAVE)

- [ ] **Tests unitaires** : Suite tests pour scripts complexes (82+ tests comme customize/validators/bash)
- [ ] **Linting** : Configuration Biome pour scripts TypeScript
- [ ] **TypeScript** : Préférer TypeScript/Bun pour scripts vs Bash
- [ ] **Documentation scripts** : CLAUDE.md dans dossiers scripts/

### Optionnel (NICE TO HAVE)

- [ ] **CI/CD** : GitHub Actions pour tests automatiques
- [ ] **Type safety** : TypeScript strict mode
- [ ] **Performance** : Benchmarks pour operations critiques

---

## 🧪 Standards Tests Unitaires

### Quand écrire des tests ?

**OUI** - Tests obligatoires pour :
- ✅ Validation sécurité (ex: customize/validators/bash - 82+ tests)
- ✅ Scripts complexes avec logique conditionnelle
- ✅ Parsers / Transformers de données
- ✅ Algorithmes critiques

**NON** - Tests non nécessaires pour :
- ❌ Skills simples (wrappers autour de commandes)
- ❌ Agents déclaratifs (juste du prompt)
- ❌ Scripts one-liner simples

### Framework recommandé

**Bun Test** (natif, rapide, zéro config)

```typescript
import { describe, expect, it } from "bun:test";

describe("MyValidator", () => {
  it("should validate safe commands", () => {
    expect(validator.validate("ls -la")).toBe(true);
  });

  it("should block dangerous commands", () => {
    expect(validator.validate("rm -rf /")).toBe(false);
  });
});
```

### Structure tests

```
plugin/
├── src/
│   └── validator.ts
└── __tests__/
    └── validator.test.ts
```

### Commandes

```bash
bun test              # Run all tests
bun test --watch      # Watch mode
bun test --coverage   # Coverage report
```

---

## 🎨 Standards Linting

### Biome (Recommandé pour TypeScript)

**Pourquoi Biome ?**
- ✅ Ultra-rapide (écrit en Rust)
- ✅ Zero config par défaut
- ✅ Formatter + Linter en un
- ✅ Compatible VSCode/JetBrains

**Configuration minimale** (`biome.json`) :

```json
{
  "$schema": "https://biomejs.dev/schemas/2.3.11/schema.json",
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "tab"
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  }
}
```

**Commandes** :

```bash
bun run lint    # Check + auto-fix
bun run format  # Format only
```

---

## 📝 Standards TypeScript vs Bash

### Quand utiliser TypeScript/Bun ?

**TypeScript/Bun** pour :
- ✅ Scripts avec logique complexe
- ✅ Validation / Parsing de données
- ✅ Scripts réutilisables (libraries)
- ✅ Code nécessitant tests unitaires
- ✅ Interactions API (fetch, HTTP)

**Bash** pour :
- ✅ Wrappers simples autour de commandes
- ✅ Git operations basiques
- ✅ File system operations simples
- ✅ One-liners

### Migration Bash → TypeScript

**Avant (Bash)** :
```bash
#!/bin/bash
git status
git diff --cached
```

**Après (TypeScript)** :
```typescript
#!/usr/bin/env bun
import { $ } from "bun";

await $`git status`;
await $`git diff --cached`;
```

**Avantages migration** :
- Type safety
- Meilleur error handling
- Testable unitairement
- Cross-platform (Windows via WSL)

---

## 📚 Standards Documentation

### CHANGELOG.md

**Format** : [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/)

```markdown
## [1.1.0] - 2026-01-31

### Added
- Nouvelle feature X
- Skill `/new-skill`

### Changed
- Amélioration feature Y

### Fixed
- Correction bug Z

### Removed
- Suppression deprecated feature
```

**Règles** :
- Une section par version
- Catégories : Added, Changed, Fixed, Removed
- Date au format YYYY-MM-DD
- Versioning sémantique (MAJOR.MINOR.PATCH)

### README.md

**Structure minimale** :
1. Titre + description courte
2. Installation (`/plugin install`)
3. Skills disponibles (avec exemples)
4. Agents disponibles (si applicable)
5. Structure fichiers
6. Dépendances
7. Licence

### DEPENDENCIES.json

**Structure** :
```json
{
  "version": "1.0",
  "critical": {
    "bun": {
      "version": ">=1.0.0",
      "description": "Runtime pour scripts TypeScript",
      "installUrl": "https://bun.sh"
    }
  },
  "optional": {
    "gh": {
      "description": "Pour skills GitHub"
    }
  },
  "packages": {
    "npm": {
      "dependencies": {
        "package-name": "^1.0.0"
      }
    }
  }
}
```

---

## 🏆 Exemples de Référence

### Champion Qualité : customize/validators/bash

**Pourquoi exemplaire ?**
- ✅ 82+ tests unitaires (100% coverage logic critique)
- ✅ TypeScript avec types stricts
- ✅ Biome configuré
- ✅ Documentation complète (SKILL.md + README + CLAUDE.md)
- ✅ Architecture claire (src/, __tests__/, scripts/)

**À reproduire** :
```
customize/validators/bash/
├── src/
│   ├── cli.ts              # Entry point
│   └── lib/
│       ├── security-rules.ts  # 100+ patterns
│       ├── validator.ts       # Core logic
│       └── types.ts           # Type definitions
├── __tests__/
│   └── validator.test.ts   # 82+ tests
├── package.json
├── tsconfig.json
├── biome.json
└── README.md
```

---

## 🚀 Workflow Qualité Recommandé

### Création nouveau plugin

1. **Copier template** : `cp -r templates/plugin-structure/ new-plugin/`
2. **Remplir métadonnées** : plugin.json, README, CHANGELOG
3. **Implémenter skills/agents**
4. **Si scripts complexes** : Ajouter tests unitaires
5. **Si TypeScript** : Configurer Biome
6. **Ajouter au marketplace** : marketplace.json, README global, CHANGELOG global

### Modification plugin existant

1. **Implémenter changements**
2. **Si logique critique modifiée** : Ajouter/mettre à jour tests
3. **Linter** : `bun run lint` (si configuré)
4. **Tests** : `bun test` (si présents)
5. **Bump version** : plugin.json + CHANGELOG.md
6. **Mettre à jour docs** : README si nécessaire

### Pre-commit checklist

- [ ] Tests passent (si présents)
- [ ] Linter clean (si configuré)
- [ ] CHANGELOG.md mis à jour
- [ ] Version bumpée (MAJOR.MINOR.PATCH)
- [ ] README à jour si changements API

---

## 📊 Progression Qualité Actuelle

**État au 2026-01-31** :

| Plugin | CHANGELOG | Tests | Linting | Score |
|--------|-----------|-------|---------|-------|
| customize | ✅ | ✅ (82+) | ⚠️ | 🏆 9/10 |
| mlvn | ✅ | ✅ | ⚠️ | 🏆 8/10 |
| notifications | ✅ | ✅ | ⚠️ | 🏆 8/10 |
| Autres (14) | ✅ | ❌ | ❌ | ⚠️ 5/10 |

**Prochaines étapes** :
1. Ajouter Biome aux plugins avec scripts TypeScript
2. Ajouter tests pour scripts critiques
3. Documenter patterns dans CLAUDE.md

---

## 🔗 Références

- [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/)
- [Semantic Versioning](https://semver.org/lang/fr/)
- [Biome Documentation](https://biomejs.dev/)
- [Bun Test Documentation](https://bun.sh/docs/cli/test)
- Template : `templates/plugin-structure/`
