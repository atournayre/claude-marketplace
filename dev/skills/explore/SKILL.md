---
name: dev:explore
description: Explorer le codebase avec agents parallèles (Phase 1)
model: sonnet
allowed-tools: [Task, Read, Glob, Grep]
version: 1.0.0
license: MIT
---

> ⚠️ **Déprécié** : Cette skill est remplacée par `analyst:explore`. Voir le plugin `analyst`. Sera supprimée en v3.0.

# Configuration de sortie

**IMPORTANT** : Cette skill génère un résumé d'exploration structuré et nécessite un format de sortie spécifique.

Lis le frontmatter de cette skill. Si un champ `output-style` est présent, exécute immédiatement :
```
/output-style <valeur-du-champ>
```

*Note : Une fois que le champ `output-style` sera supporté nativement par Claude Code, cette instruction pourra être supprimée.*

**Output-style requis** : `bullet-points`

# Objectif

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

Phase 1 du workflow de développement : explorer le codebase pour comprendre les patterns existants.

# Prérequis

⚠️ **Plugin feature-dev requis** pour les agents `code-explorer`.

Si non installé :
```
/plugin install feature-dev@claude-code-plugins
```

# Instructions

## 1. Lire le contexte

- Lire `.claude/data/.dev-workflow-state.json` pour connaître la feature en cours
- Si le fichier n'existe pas, demander à l'utilisateur de lancer `/dev:discover` d'abord

## 2. Créer les tâches d'exploration

Utiliser `TaskCreate` pour chaque agent :

```
TaskCreate #1: Explorer features similaires (code-explorer)
TaskCreate #2: Mapper architecture et abstractions (code-explorer)
TaskCreate #3: Analyser intégrations (code-explorer) - optionnel
TaskCreate #4: Consolider résultats et présenter résumé
```

**Important :**
- Utiliser `activeForm` (ex: "Explorant features similaires", "Mappant l'architecture")
- Tâche #3 optionnelle selon pertinence de la feature
- Tâche #4 bloquée par les agents 1-3 (utiliser `addBlockedBy`)
- Les agents 1-3 se lancent en parallèle

## 3. Lancer les agents code-explorer

**⚠️ Avant de lancer les agents :** Marquer les tâches en `in_progress` :
- `TaskUpdate` → tâche #1 en `in_progress`
- `TaskUpdate` → tâche #2 en `in_progress`
- `TaskUpdate` → tâche #3 en `in_progress` (si créée)

Lancer **2-3 agents `code-explorer` en parallèle** avec des focus différents.

**Limites d'exploration :**
- `max_turns: 10` pour chaque agent
- Si un agent atteint sa limite sans résultats, marquer tâche comme completed avec résultats partiels
- Chaque prompt agent doit inclure : "Tu as maximum 10 tours. Retourne tes meilleurs résultats partiels si tu atteins la limite."

### Agent 1 : Features similaires
```
Tu as maximum 10 tours. Retourne tes meilleurs résultats partiels si tu atteins la limite.

Trouve des features similaires à "{feature}" dans le codebase.
Trace leur implémentation de bout en bout.
Retourne les 5-10 fichiers clés à lire.
```

**Quand terminé :** `TaskUpdate` → tâche #1 en `completed`

### Agent 2 : Architecture
```
Tu as maximum 10 tours. Retourne tes meilleurs résultats partiels si tu atteins la limite.

Mappe l'architecture et les abstractions pour la zone concernée par "{feature}".
Identifie les patterns utilisés (repositories, services, events, etc.).
Retourne les 5-10 fichiers clés à lire.
```

**Quand terminé :** `TaskUpdate` → tâche #2 en `completed`

### Agent 3 : Intégrations (si pertinent)
```
Tu as maximum 10 tours. Retourne tes meilleurs résultats partiels si tu atteins la limite.

Analyse les points d'intégration existants (APIs, events, commands).
Identifie comment les features communiquent entre elles.
Retourne les 5-10 fichiers clés à lire.
```

**Quand terminé :** `TaskUpdate` → tâche #3 en `completed`

## 4. Consolider les résultats

**🔄 Progression :** `TaskUpdate` → tâche #4 en `in_progress`

- Fusionner les listes de fichiers identifiés
- Lire les fichiers clés pour construire une compréhension profonde
- Identifier les patterns récurrents

## 5. Présenter le résumé

```
🔍 Exploration du codebase

**Features similaires trouvées :**
- {feature 1} ({chemin}) : {description courte}
- {feature 2} ({chemin}) : {description courte}

**Patterns architecturaux identifiés :**
- {pattern 1} : utilisé dans {fichiers}
- {pattern 2} : utilisé dans {fichiers}

**Fichiers clés à connaître :**
1. `{fichier}:{ligne}` - {rôle}
2. `{fichier}:{ligne}` - {rôle}
...

**Points d'attention :**
- {observation 1}
- {observation 2}
```

## 6. Finaliser

**🔄 Progression :** `TaskUpdate` → tâche #4 en `completed`

Mettre à jour `.claude/data/.dev-workflow-state.json`

# Task Management

**Progression du workflow :**
- 4 tâches créées à l'initialisation (3 ou 4 selon pertinence)
- Les 3 premières tâches (agents) se lancent en parallèle
- La tâche #4 (consolidation) est bloquée par les 3 agents (`addBlockedBy`)
- Chaque agent marque sa tâche comme `completed` indépendamment
- Utiliser `TaskList` pour voir la progression des agents parallèles
- Les tâches permettent à l'utilisateur de suivre l'exploration multi-agents

# Prochaine étape

```
✅ Exploration terminée

Prochaine étape : /dev:clarify pour poser les questions de clarification
```
