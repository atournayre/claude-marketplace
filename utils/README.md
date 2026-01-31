# Plugin Utils

Skills et agents utilitaires génériques pour tâches courantes.

## Installation

```bash
/plugin install utils@atournayre
```

## Skills Disponibles

Le plugin utils fournit 1 skill générique :

### `/fix-grammar`

Corrige grammaire et orthographe dans fichiers ou texte.

**Modes :**
- **Single mode** : Corrige un fichier unique
- **Multi mode** : Corrige plusieurs fichiers simultanément

**Usage :**
```bash
# Fichier unique
/fix-grammar path/to/file.md

# Plusieurs fichiers
/fix-grammar "*.md"

# Texte direct
/fix-grammar "text to fix"
```

**Features :**
- ✅ Détection automatique langue (FR/EN)
- ✅ Préservation formatage Markdown
- ✅ Batch processing pour multi-fichiers
- ✅ Affichage diff avant/après

---

## Agents Disponibles

Le plugin utils fournit 2 agents spécialisés :

### `action`

Agent de validation conditionnelle qui vérifie avant d'exécuter.

**Usage :**
- Valide les prérequis avant action
- Execute seulement si conditions remplies
- Utile pour workflows conditionnels

**Exemple :**
```yaml
agents:
  - name: action
    prompt: "Run tests only if source files changed"
```

---

### `explore-codebase`

Agent d'exploration codebase avec analyse imports chains.

**Usage :**
- Explore structure projet
- Trace chaînes d'imports
- Identifie dépendances
- Map architecture

**Exemple :**
```yaml
agents:
  - name: explore-codebase
    prompt: "Map all API endpoints and their dependencies"
```

---

## Structure

```
utils/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── fix-grammar/
│       └── SKILL.md
└── agents/
    ├── action.md
    └── explore-codebase.md
```

## Licence

MIT
