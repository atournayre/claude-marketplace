---
name: infra:make-subagent
description: Guide expert pour créer et configurer des sous-agents Claude Code spécialisés. Couvre la structure des fichiers agent, le frontmatter, les prompts système, les outils, les modes background et les patterns d'orchestration. Utiliser pour créer de nouveaux agents ou configurer des workflows multi-agents.
model: sonnet
allowed-tools: [Read, Write, Edit, Bash, Glob, AskUserQuestion]
version: 1.0.0
license: MIT
---

# infra:make-subagent

Guide expert pour créer des sous-agents Claude Code spécialisés.

## Contrainte critique

**Les sous-agents ne peuvent pas interagir avec l'utilisateur.**

- Peuvent utiliser : Read, Write, Edit, Bash, Grep, Glob
- Ne peuvent pas : AskUserQuestion, présenter des options, attendre l'input utilisateur
- L'utilisateur ne voit que le rapport final de l'agent

## Structure des fichiers

| Type | Emplacement | Priorité |
|------|-------------|----------|
| Projet | `.claude/agents/` | Haute |
| Utilisateur | `~/.claude/agents/` | Basse |
| Plugin | `plugin/agents/` | Plus basse |

## Frontmatter obligatoire

```markdown
---
name: nom-en-kebab-case
description: "Description orientée action avec quand l'utiliser"
tools: Read, Grep, Glob, Bash
model: sonnet
---
```

Champs :
- `name` : lettres minuscules et tirets uniquement
- `description` : inclure les déclencheurs ("À utiliser proactivement pour...")
- `tools` : liste CSV (hérite tout si omis)
- `model` : sonnet, opus, haiku, ou inherit

## Structure du prompt système

Utiliser des balises XML (pas de titres Markdown dans le body) :

```markdown
<role>
Tu es un spécialiste en [domaine].
</role>

<focus_areas>
- Point 1
- Point 2
</focus_areas>

<workflow>
1. Étape 1
2. Étape 2
</workflow>

<output_format>
Format de sortie attendu.
</output_format>
```

## Sélection du modèle

- **sonnet** : tâches de raisonnement (review, analyse, génération)
- **haiku** : tâches simples (vérifications, formatage, recherches rapides)
- **opus** : tâches très complexes nécessitant un raisonnement profond

## Conception du workflow

Utiliser le **main chat** pour :
- Collecter les besoins utilisateur
- Présenter des options ou décisions
- Tout ce qui requiert confirmation

Utiliser les **agents** pour :
- Recherche (analyse de code, documentation API)
- Génération de code selon un plan prédéfini
- Analyse et reporting (review sécurité, couverture tests)

## Exécution en arrière-plan

```
Task(
  subagent_type="agent-name",
  run_in_background=True
)
```

Récupérer les résultats via TaskOutput avec l'agent_id retourné.

## Pattern d'agents parallèles

Lancer plusieurs agents dans le même message (sans dépendances entre eux), puis collecter les résultats.

## Créer un agent : workflow

1. Définir le rôle précis (pas d'agent générique)
2. Identifier les outils nécessaires (principe du moindre privilège)
3. Écrire le prompt système avec balises XML
4. Optimiser la description pour le routing automatique
5. Tester sur des tâches représentatives

## Template agent

```markdown
---
name: agent-name
description: "Description orientée action. À utiliser proactivement pour..."
tools: Read, Grep, Glob, Bash
model: sonnet
---

<role>
Tu es un [rôle précis].
</role>

<workflow>
1. [Étape 1]
2. [Étape 2]
3. [Étape 3]
</workflow>

<output_format>
[Format de sortie attendu]
</output_format>
```
