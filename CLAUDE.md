# Claude Code Plugins Marketplace

## Architecture

Chaque plugin est un repertoire autonome avec la structure suivante :

```
plugin-name/
  .claude-plugin/
    plugin.json        # Metadata semver, auteur, description
    hooks.json         # Hooks Claude Code (optionnel)
  DEPENDENCIES.json    # Dependances inter-plugins (optionnel)
  skills/              # Skills invocables via /plugin:skill
    skill-name/
      SKILL.md         # Frontmatter YAML + instructions
      references/      # Documentation detaillee (optionnel)
      scripts/         # Scripts shell utilises par la skill
  agents/              # Agents specialises
    agent-name.md      # Frontmatter YAML + instructions
  scripts/             # Scripts shell partages du plugin
  hooks/               # Scripts de hooks (Python 3)
```

## Conventions des skills

### Frontmatter YAML obligatoire

```yaml
---
name: plugin:skill-name
description: Description concise de la skill
model: sonnet | opus
allowed-tools: [Task, Read, Write, Edit, Grep, Glob, Bash]
version: 1.0.0
license: MIT
---
```

### Contenu
- SKILL.md < 5000 mots
- Pour les details supplementaires, utiliser `references/` avec des fichiers .md dedies
- Section `## Instructions a Executer` obligatoire

## Conventions des agents

### Frontmatter YAML obligatoire

```yaml
---
name: agent-name
description: Description du role de l'agent
tools: Read, Edit, Grep, Glob, Bash
model: sonnet
---
```

### Structure du rapport
- Section `## Rapport / Reponse` decrivant le format de sortie attendu
- Restrictions explicites (ex: pas de commits Git)

## Conventions des scripts shell

1. `set -euo pipefail` en premiere ligne de chaque script (apres le shebang)
2. Pas d'`eval` — utiliser des tableaux et expansion directe
3. Pas de `2>/dev/null` sans gestion du cas d'erreur (verifier le resultat apres)
4. `mktemp` + `trap 'cleanup' EXIT` pour fichiers temporaires
5. Verifier les outils requis au debut du script :
   ```bash
   command -v jq >/dev/null 2>&1 || { echo "jq requis" >&2; exit 1; }
   ```
6. Guard clauses pour les inputs vides/invalides — ne jamais produire de sortie trompeuse

## Conventions des hooks

- Langage : Python 3
- Input : JSON sur stdin
- Exit codes : 0 (ok) / 2 (block avec message sur stderr)
- Suivre le pattern des hooks existants dans `customize/hooks/`

## Versioning

- Semver dans `plugin.json` (`version: "X.Y.Z"`)
- CHANGELOG.md par plugin
- Bump via `/bump`
