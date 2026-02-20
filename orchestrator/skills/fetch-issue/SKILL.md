---
name: orchestrator:fetch-issue
description: Récupère et valide le contenu d'une issue GitHub pour le workflow automatique. Vérifie que l'issue est OPEN et a une description non vide.
argument-hint: <issue-number>
model: haiku
allowed-tools: [Bash, Read, Write]
version: 1.0.0
license: MIT
---

# orchestrator:fetch-issue

Phase 0 (Initialisation) du workflow automatisé : récupérer la spécification depuis une issue GitHub.

## Instructions à Exécuter

### 1. Valider le paramètre

```bash
issue_number=$ARGUMENTS

if ! [[ "$issue_number" =~ ^[0-9]+$ ]]; then
    echo "Erreur : l'argument doit être un numéro d'issue GitHub"
    echo "Usage: /orchestrator:feature <issue-number>"
    exit 1
fi
```

### 2. Récupérer l'issue

```bash
issue_data=$(gh issue view "$issue_number" --json title,body,labels,state)
if [ $? -ne 0 ]; then
    echo "Issue #$issue_number non trouvée"
    echo "Vérifie : numéro correct, gh auth login, issue dans le repo courant"
    exit 1
fi
```

### 3. Parser et valider

```bash
issue_title=$(echo "$issue_data" | jq -r '.title')
issue_body=$(echo "$issue_data" | jq -r '.body')
issue_state=$(echo "$issue_data" | jq -r '.state')
issue_labels=$(echo "$issue_data" | jq -r '.labels | map(.name) | join(", ")')

if [ "$issue_state" != "OPEN" ]; then
    echo "Issue #$issue_number n'est pas ouverte (state: $issue_state)"
    exit 1
fi

if [ -z "$issue_body" ] || [ "$issue_body" == "null" ]; then
    echo "Issue #$issue_number : description vide"
    echo "Ajoute une description détaillée avant de relancer"
    exit 1
fi
```

### 4. Sauvegarder dans le workflow state

```bash
mkdir -p ".claude/data/workflows"
workflow_state_file=".claude/data/workflows/issue-${issue_number}-dev-workflow-state.json"
```

Créer le fichier JSON avec :
- `mode: "auto"`
- `issue` : number, title, description, labels, state, fetchedAt
- `feature` : issue title
- `status: "in_progress"`
- `startedAt` : ISO timestamp
- `currentPhase: 0`

### 5. Afficher les infos

```
Issue GitHub récupérée

  #$issue_number : $issue_title
  Etat : $issue_state
  Labels : $issue_labels
```

## Règles

- Valider le numéro (doit être entier)
- Vérifier que l'issue existe (gh auth requis)
- Vérifier que l'issue est OPEN
- Vérifier que la description n'est pas vide
- Sauvegarder dans workflow state avec metadata
- Ne pas modifier l'issue (read-only)
- Ne pas continuer si l'issue est invalide (exit 1)
