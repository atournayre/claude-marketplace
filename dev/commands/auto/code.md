---
description: Implémenter selon le plan - Mode AUTO (Phase 6)
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
---

# Objectif

Phase 6 du workflow automatisé : implémenter selon le plan **SANS demander d'approbation**.

Démarrage immédiat de l'implémentation.

# Instructions

## 1. Lire le contexte

Déterminer le chemin du workflow state :

```bash
# Récupérer issue_number depuis le contexte
workflow_state_file=".claude/data/workflows/issue-${issue_number}-dev-workflow-state.json"
```

- Lire le workflow state pour accéder au plan généré (Phase 5)
- Lire `docs/specs/{feature}.md` (ou chemin du plan)
- Si le plan n'existe pas, exit avec erreur

## 2. Implémenter selon le plan

Exécuter le contenu du plan :
- Créer les fichiers nécessaires
- Modifier les fichiers existants
- Créer les tests unitaires

**Pas de checkpoint d'approbation** - implémentation directe.

## 3. Vérification PHPStan initiale

Lancer une première vérification PHPStan **sans l'arrêter l'implémentation** :

```bash
vendor/bin/phpstan analyse --level=9 2>&1
```

Noter les résultats pour la Phase 7 (Review).

## 4. Mettre à jour le workflow state

```json
{
  "currentPhase": 6,
  "phases": {
    "6": {
      "status": "completed",
      "completedAt": "{ISO timestamp}",
      "durationMs": {durée},
      "filesCreated": ["{liste des fichiers}"],
      "filesModified": ["{liste des fichiers}"],
      "testsCreated": {nombre},
      "phpstanErrorsInitial": {nombre}
    }
  }
}
```

# Règles

- ❌ **Pas de checkpoint d'approbation**
- ✅ **Implémenter directement selon le plan**
- ✅ **Créer les tests unitaires**
- ✅ **Vérifier PHPStan** (sans bloquer)
- ❌ **Ne PAS corriger les erreurs** (ce sera Phase 6)
