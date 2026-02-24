---
name: infra:skill-creator
description: Guide expert pour créer des skills Claude Code efficaces. Couvre la structure SKILL.md, le frontmatter, les ressources bundlées (scripts, references, assets), la progressive disclosure et les bonnes pratiques. Utiliser quand l'utilisateur demande de créer ou améliorer un skill.
model: sonnet
allowed-tools: [Read, Write, Edit, Bash, Glob, AskUserQuestion]
version: 1.0.0
license: MIT
---

# infra:skill-creator

Guide complet pour créer des skills Claude Code efficaces.

## Principes fondamentaux

### Concision

Le contexte est une ressource partagée. N'inclure que ce que Claude ne sait pas déjà. Préférer des exemples concis aux explications verbeuses.

### Degrés de liberté

- **Haute liberté** (instructions textuelles) : quand plusieurs approches sont valides
- **Liberté moyenne** (pseudocode avec paramètres) : quand un pattern préféré existe
- **Faible liberté** (scripts spécifiques) : quand la cohérence est critique

## Structure d'un skill

```
skill-name/
├── SKILL.md (requis)
└── Ressources bundlées (optionnel)
    ├── scripts/     - Code exécutable
    ├── references/  - Documentation à charger au besoin
    └── assets/      - Fichiers utilisés dans les outputs
```

## Frontmatter SKILL.md

Champs importants :
- `name` : identifiant (plugin:skill-name)
- `description` : CRITIQUE — Claude s'en sert pour décider de charger le skill
- `allowed-tools` : outils autorisés sans demande de permission
- `model` : sonnet / haiku / opus
- `argument-hint` : indice affiché en autocomplète
- `disable-model-invocation: true` : seul l'utilisateur peut invoquer
- `user-invocable: false` : seul Claude peut invoquer

## Progressive disclosure

3 niveaux de chargement :
1. **Metadata** (name + description) — toujours en contexte (~100 mots)
2. **SKILL.md body** — quand le skill se déclenche (< 5000 mots)
3. **Ressources bundlées** — chargées par Claude au besoin

Garder SKILL.md sous 500 lignes. Déplacer les détails dans `references/`.

## Processus de création

1. **Comprendre** le skill avec des exemples concrets
2. **Planifier** les ressources réutilisables (scripts, references, assets)
3. **Créer** la structure du répertoire
4. **Éditer** : commencer par les ressources, puis SKILL.md
5. **Itérer** sur des tâches réelles

## Rédaction du frontmatter description

Inclure quand utiliser le skill. Exemples :
- "Explique le code avec des diagrammes. Utiliser quand l'utilisateur demande 'comment ça marche ?'"
- "À utiliser proactivement après des changements de code pour la review qualité."

## Bonnes pratiques

- **Ne pas inclure** : README.md, CHANGELOG.md, guides d'installation dans le skill
- **Inclure** uniquement ce dont un agent IA a besoin pour faire le travail
- **references/** : documentation de référence chargée au besoin
- **scripts/** : code répété ou nécessitant fiabilité déterministe
- **assets/** : templates, images, boilerplate copiés/modifiés en output
- Éviter les références imbriquées profondément (1 niveau depuis SKILL.md)

## Template SKILL.md

```markdown
---
name: plugin:skill-name
description: Description concise avec quand l'utiliser
model: sonnet
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
version: 1.0.0
license: MIT
---

# Titre

Objectif en 1-2 phrases.

## Instructions à Exécuter

[Contenu structuré]
```
