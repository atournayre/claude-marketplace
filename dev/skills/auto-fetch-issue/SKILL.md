---
name: dev:auto:fetch-issue
description: Récupérer le contenu d'une issue GitHub - Mode AUTO (Phase 0)
model: haiku
allowed-tools:
  - Bash
  - Read
  - Write
version: 1.0.0
license: MIT
---

> ⚠️ **Déprécié** : Cette skill est remplacée par `orchestrator:fetch-issue`. Voir le plugin `orchestrator`. Sera supprimée en v3.0.

# Objectif

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


Phase 0 (Initialisation) du workflow automatisé : récupérer la specification depuis une issue GitHub.

Exécuté au démarrage du workflow avant Phase 1.

# Instructions

## 1. Valider le paramètre

- Vérifier que l'argument est un numéro valide
- Exit avec erreur si pas un numéro

```bash
issue_number=$ARGUMENTS

if ! [[ "$issue_number" =~ ^[0-9]+$ ]]; then
    echo "❌ Erreur : l'argument doit être un numéro d'issue GitHub"
    echo "Usage: /dev:auto:feature 123"
    exit 1
fi
```

## 2. Récupérer l'issue

Utiliser `gh issue view` pour récupérer le contenu :

```bash
issue_data=$(gh issue view "$issue_number" --json title,body,labels,state)
issue_exists=$?

if [ $issue_exists -ne 0 ]; then
    echo "❌ Issue #$issue_number non trouvée"
    echo "Vérifie que :"
    echo "  1. Le numéro est correct"
    echo "  2. Tu es authentifié sur GitHub (gh auth login)"
    echo "  3. L'issue existe dans le repo courant"
    exit 1
fi
```

## 3. Parser les données

Extraire les champs nécessaires :

```bash
# Utiliser jq pour parser
issue_title=$(echo "$issue_data" | jq -r '.title')
issue_body=$(echo "$issue_data" | jq -r '.body')
issue_state=$(echo "$issue_data" | jq -r '.state')
issue_labels=$(echo "$issue_data" | jq -r '.labels | map(.name) | join(", ")')
```

## 4. Valider l'issue

- Vérifier que l'issue est en state "OPEN"
- Vérifier que la description n'est pas vide

```bash
if [ "$issue_state" != "OPEN" ]; then
    echo "❌ Issue #$issue_number n'est pas ouverte (state: $issue_state)"
    exit 1
fi

if [ -z "$issue_body" ] || [ "$issue_body" == "null" ]; then
    echo "⚠️  Issue #$issue_number : description vide"
    echo "Ajoute une description détaillée avant de relancer le workflow"
    exit 1
fi
```

## 5. Afficher les infos

```
🔗 Issue GitHub récupérée

  #$issue_number : $issue_title
  État : $issue_state
  Labels : $issue_labels

  Description :
  ───────────────────────────────
  $issue_body
  ───────────────────────────────
```

## 6. Sauvegarder dans le workflow state

Déterminer le chemin :

```bash
issue_number=$ARGUMENTS
workflow_state_file=".claude/data/workflows/issue-${issue_number}-dev-workflow-state.json"
mkdir -p ".claude/data/workflows"
```

Créer le fichier `.dev-workflow-state.json` :

```json
{
  "mode": "auto",
  "issue": {
    "number": $issue_number,
    "title": "$issue_title",
    "description": "$issue_body",
    "labels": "$issue_labels",
    "state": "$issue_state",
    "fetchedAt": "{ISO timestamp}"
  },
  "feature": "$issue_title",
  "status": "in_progress",
  "startedAt": "{ISO timestamp}",
  "currentPhase": 0,
  "phases": {
    "0": {
      "status": "completed",
      "completedAt": "{ISO timestamp}",
      "durationMs": {durée}
    }
  }
}
```

## 7. Transférer à Phase 1

Passer la spec de l'issue à `discover.md` en paramètre :

```bash
spec="Issue #$issue_number: $issue_title\n\n$issue_body"
# Cette spec sera utilisée dans Phase 1 (Discover)
```

# Règles

- ✅ **Valider le numéro** (doit être entier)
- ✅ **Vérifier que l'issue existe** (gh auth required)
- ✅ **Vérifier que l'issue est OPEN**
- ✅ **Vérifier que la description n'est pas vide**
- ✅ **Sauvegarder dans workflow state** avec issue metadata
- ✅ **Afficher les infos** pour transparence
- ❌ **Ne pas modifier l'issue** (read-only)
- ❌ **Ne pas continuer si l'issue est invalide** (exit 1)

# Cas d'erreur

## Issue non trouvée
```
❌ Issue #123 non trouvée
Vérifie que :
  1. Le numéro est correct
  2. Tu es authentifié sur GitHub (gh auth login)
  3. L'issue existe dans le repo courant
```

## Issue fermée
```
❌ Issue #123 n'est pas ouverte (state: CLOSED)
```

## Description vide
```
⚠️  Issue #123 : description vide
Ajoute une description détaillée avant de relancer le workflow
```

# Dépendances

- `gh` CLI installé et authentifié (`gh auth login`)
- Exécuté depuis le repo contenant l'issue
