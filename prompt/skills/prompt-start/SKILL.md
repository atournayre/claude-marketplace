---
name: prompt:start
description: Démarre un développement avec un starter léger puis active le mode plan
license: MIT
version: 1.0.0
allowed-tools: [Read, Write, Bash, AskUserQuestion, EnterPlanMode]
model: sonnet
---

Tu es un assistant qui combine prompts structurés et mode plan pour un développement efficace.

## Objectif

Démarrer un développement avec :
1. Un **starter léger** (contexte + contraintes)
2. Le **mode plan** pour exploration et adaptation
3. Une **checklist** pour validation finale

## Workflow

### 1. Parser les arguments

```
/prompt:start <type> "<description>" [options]
```

**Types disponibles** :
- `feature` → starter-feature.md + checklist-php.md
- `refactor` → starter-refactor.md + checklist-php.md
- `api` → starter-api.md + checklist-api.md
- `fix` → starter-fix.md + checklist-php.md

**Options** :
- `--entity=X` : Nom de l'entité (feature)
- `--context=X` : Bounded context (feature)
- `--target=X` : Fichier(s) cible (refactor, fix)
- `--service=X` : Service externe (api)
- `--checklist=X` : Checklist additionnelle (security, etc.)

### 2. Collecter les variables manquantes

Si des variables essentielles manquent, utiliser `AskUserQuestion` :

```json
{
  "questions": [
    {
      "question": "Quel type de développement ?",
      "header": "Type",
      "multiSelect": false,
      "options": [
        {"label": "feature", "description": "Nouvelle fonctionnalité métier"},
        {"label": "refactor", "description": "Refactoring de code existant"},
        {"label": "api", "description": "API ou intégration externe"},
        {"label": "fix", "description": "Correction de bug"}
      ]
    }
  ]
}
```

### 3. Lire et substituer le starter

```bash
# Lire le starter approprié
cat prompt/templates/starters/{type}.md
```

Substituer les variables `{VARIABLE}` par les valeurs collectées.

### 4. Afficher le starter

Afficher le starter substitué à l'utilisateur avec un résumé :

```
📋 Starter : {TYPE}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Contenu du starter]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Checklist associée : checklist-{checklist}.md
🔄 Activation du mode plan...
```

### 5. Activer le mode plan

Utiliser `EnterPlanMode` pour basculer en mode plan.

Le mode plan va :
- Explorer le codebase
- Proposer un plan d'implémentation
- Demander validation avant exécution

### 6. Rappeler la checklist

À la fin du mode plan (avant exécution), rappeler :

```
⚠️  Avant d'exécuter, vérifier la checklist :
/prompt:validate --checklist={checklist}
```

## Exemples d'utilisation

```bash
# Feature complète
/prompt:start feature "Gestion des factures" --entity=Invoice --context=Billing

# Refactoring
/prompt:start refactor "Simplifier la validation" --target=src/Validator/

# API/Webhook
/prompt:start api "Intégration Stripe" --service=Stripe

# Bug fix
/prompt:start fix "Erreur 500 sur login" --target=src/Security/
```

## Gestion des erreurs

- **Type inconnu** : Proposer les 4 types disponibles
- **Description vide** : Demander interactivement
- **Starter introuvable** : Vérifier installation du plugin

## Output attendu

Le skill doit :
1. Afficher le starter substitué
2. Indiquer la checklist associée
3. Activer automatiquement le mode plan
4. Ne PAS écrire de fichier (contrairement aux anciens prompts)
