---
description: Designer 2-3 approches architecturales (Phase 3)
model: claude-sonnet-4-5-20250929
allowed-tools: Task, Read, Glob, Grep, AskUserQuestion
---

# Objectif

Phase 3 du workflow de développement : proposer plusieurs approches architecturales et aider l'utilisateur à choisir.

# Prérequis

⚠️ **Plugin feature-dev requis** pour les agents `code-architect`.

Si non installé :
```
/plugin install feature-dev@claude-code-plugins
```

# Instructions

## 1. Lire le contexte

- Lire `.dev-workflow-state.json` pour la feature, les findings et les décisions
- Si phases précédentes non complétées, rediriger vers la phase manquante

## 2. Lancer les agents code-architect

Lancer **2-3 agents `code-architect` en parallèle** avec des focus différents :

### Agent 1 : Minimal changes
```
Conçois l'architecture pour "{feature}" avec un focus sur :
- Le plus petit changement possible
- Réutilisation maximale de l'existant
- Minimum de nouveaux fichiers

Contexte du codebase :
{keyFiles et patterns de la phase 1}

Décisions prises :
{décisions de la phase 2}
```

### Agent 2 : Clean architecture
```
Conçois l'architecture pour "{feature}" avec un focus sur :
- Maintenabilité long terme
- Abstractions élégantes
- Séparation des responsabilités
- Testabilité

Contexte du codebase :
{keyFiles et patterns de la phase 1}

Décisions prises :
{décisions de la phase 2}
```

### Agent 3 : Pragmatic balance
```
Conçois l'architecture pour "{feature}" avec un focus sur :
- Balance entre rapidité et qualité
- Bonnes pratiques sans over-engineering
- Respect des patterns existants

Contexte du codebase :
{keyFiles et patterns de la phase 1}

Décisions prises :
{décisions de la phase 2}
```

## 3. Consolider et comparer

Présenter les approches de manière structurée :

```
🏗️ Propositions d'architecture

**Approche 1 : Minimal Changes**
- Description : {résumé}
- Fichiers impactés : {nombre}
- Pros : {avantages}
- Cons : {inconvénients}

**Approche 2 : Clean Architecture**
- Description : {résumé}
- Fichiers impactés : {nombre}
- Pros : {avantages}
- Cons : {inconvénients}

**Approche 3 : Pragmatic Balance**
- Description : {résumé}
- Fichiers impactés : {nombre}
- Pros : {avantages}
- Cons : {inconvénients}

---

💡 **Recommandation :** Approche {N} car {raison}.

Différences concrètes :
- {différence 1}
- {différence 2}
```

## 4. Demander le choix de l'utilisateur

```
Quelle approche préfères-tu ?
1. Minimal Changes
2. Clean Architecture
3. Pragmatic Balance
```

⚠️ **CRITIQUE : Attendre le choix avant de passer à la phase suivante.**

## 5. Documenter l'architecture choisie

Mettre à jour le workflow state :

```json
{
  "currentPhase": 3,
  "phases": {
    "3": {
      "status": "completed",
      "completedAt": "{timestamp}",
      "chosenApproach": "{nom de l'approche}",
      "architecture": {
        "components": ["{liste}"],
        "files": ["{liste des fichiers à créer/modifier}"],
        "buildSequence": ["{étapes}"]
      }
    }
  }
}
```

# Prochaine étape

```
✅ Architecture choisie : {nom}

Prochaine étape : /dev:plan pour générer le plan d'implémentation
```
