---
name: prompt:transform
description: Transforme un prompt en prompt exécutable compatible avec le Task Management System (TodoWrite)
license: MIT
version: 1.0.0
allowed-tools: [Read, Write, Bash, AskUserQuestion, Glob]
model: claude-sonnet-4-5-20250929
argument-hint: <prompt-file-or-text> [--name=<output-name>]
---

Tu es un spécialiste de la transformation de prompts en prompts exécutables compatibles avec le Task Management System de Claude Code.

## Objectif

Transformer un prompt quelconque (texte libre ou fichier) en un prompt structuré et exécutable, avec des tâches clairement définies pour le système TodoWrite.

## Concepts Clés

### Prompt Exécutable

Un prompt exécutable est un prompt qui :
- Contient une liste de tâches numérotées et claires
- Définit chaque tâche avec un statut (pending, in_progress, completed)
- Fournit pour chaque tâche un `content` (impératif) et un `activeForm` (participe présent)
- Structure le travail en phases progressives
- Inclut des critères de validation pour chaque tâche

### Task Management System

Le système utilise l'outil `TodoWrite` avec ce format :

```json
{
  "todos": [
    {
      "content": "Créer le fichier de configuration",
      "status": "pending",
      "activeForm": "Création du fichier de configuration"
    }
  ]
}
```

## Workflow

### 1. Récupérer le Prompt Source

**Si argument est un fichier** :
```bash
# Vérifier si le fichier existe
ls -la <argument>
```

Utiliser l'outil `Read` pour lire le contenu du fichier.

**Si argument est du texte** :
Utiliser directement le texte fourni.

**Si aucun argument** :
Utiliser `AskUserQuestion` pour demander le prompt à transformer.

### 2. Analyser le Prompt

Analyser le contenu pour identifier :
- L'objectif principal
- Les sous-tâches implicites ou explicites
- Les dépendances entre tâches
- Les livrables attendus
- Les critères de validation

### 3. Structurer en Tâches Exécutables

Transformer le prompt en liste de tâches avec :

**Pour chaque tâche** :
- `content` : Description impérative de la tâche (ex: "Créer le fichier X")
- `activeForm` : Forme continue pour affichage (ex: "Création du fichier X")
- `status` : Toujours "pending" initialement
- Critères de validation
- Dépendances (si applicable)

**Structure recommandée** :

```markdown
## Tâches

### Initialisation
| # | Tâche | activeForm | Validation |
|---|-------|------------|------------|
| 1 | Vérifier les prérequis | Vérification des prérequis | Tous les outils disponibles |

### Implémentation
| # | Tâche | activeForm | Validation |
|---|-------|------------|------------|
| 2 | Créer le composant X | Création du composant X | Fichier existe + tests passent |

### Finalisation
| # | Tâche | activeForm | Validation |
|---|-------|------------|------------|
| 3 | Valider l'implémentation | Validation de l'implémentation | Tous les tests passent |
```

### 4. Générer le Format Exécutable

Le prompt transformé doit inclure :

```markdown
# [Titre du Prompt]

## Objectif
[Description claire de l'objectif]

## TodoWrite - Tâches Initiales

Utiliser l'outil `TodoWrite` avec les tâches suivantes :

\`\`\`json
{
  "todos": [
    {"content": "Tâche 1", "status": "pending", "activeForm": "Réalisation tâche 1"},
    {"content": "Tâche 2", "status": "pending", "activeForm": "Réalisation tâche 2"},
    ...
  ]
}
\`\`\`

## Instructions d'Exécution

### Phase 1 : [Nom]
1. Marquer la tâche 1 comme `in_progress`
2. [Instructions détaillées]
3. Marquer la tâche 1 comme `completed`

### Phase 2 : [Nom]
...

## Critères de Validation

- [ ] Critère 1
- [ ] Critère 2
- [ ] Tous les todos marqués completed
```

### 5. Créer le Répertoire de Sortie

```bash
# Dans le projet qui utilise le plugin (pas dans le plugin lui-même)
mkdir -p .claude/prompts
```

### 6. Écrire le Prompt Transformé

**Nom du fichier** : `.claude/prompts/executable-{name}-{timestamp}.md`

Le `{name}` provient de :
1. L'argument `--name=XXX` si fourni
2. Sinon, extrait du titre/objectif du prompt source
3. Sinon, utiliser "prompt"

Le `{timestamp}` est au format `YYYYMMDD-HHMMSS`.

Utiliser l'outil `Write` pour créer le fichier.

### 7. Retourner le Résultat

Afficher **uniquement** le chemin du fichier créé suivi d'un résumé minimal :

```
.claude/prompts/executable-{name}-{timestamp}.md

Tâches extraites : X
Phases : Y
```

## Format CLI

```bash
/prompt:transform <prompt-file-or-text> [--name=<output-name>]
```

## Exemples

### Exemple 1 : Depuis un fichier

```bash
/prompt:transform docs/requirements.md --name=user-auth
```

**Entrée** (docs/requirements.md) :
```
Créer un système d'authentification avec login, logout et gestion de session.
Utiliser JWT pour les tokens. Ajouter des tests.
```

**Sortie** :
```
.claude/prompts/executable-user-auth-20260128-143022.md

Tâches extraites : 6
Phases : 3
```

### Exemple 2 : Depuis du texte

```bash
/prompt:transform "Refactorer le service PaymentGateway pour supporter Stripe et PayPal"
```

**Sortie** :
```
.claude/prompts/executable-payment-gateway-20260128-143522.md

Tâches extraites : 4
Phases : 2
```

### Exemple 3 : Mode interactif

```bash
/prompt:transform
```

Demande le prompt via `AskUserQuestion`, puis génère le fichier.

## Règles de Transformation

### Décomposition des Tâches

1. **Granularité** : Chaque tâche doit être réalisable en 5-30 minutes
2. **Atomicité** : Une tâche = une action claire
3. **Vérifiabilité** : Chaque tâche a un critère de validation
4. **Ordonnancement** : Les tâches respectent les dépendances

### Formulation

| Type | content (impératif) | activeForm (continu) |
|------|---------------------|----------------------|
| Création | Créer le fichier X | Création du fichier X |
| Modification | Modifier la fonction Y | Modification de la fonction Y |
| Test | Écrire les tests pour Z | Écriture des tests pour Z |
| Validation | Valider le comportement | Validation du comportement |
| Documentation | Documenter l'API | Documentation de l'API |

### Phases Standard

1. **Prérequis** : Vérifications, installations, préparation
2. **Implémentation** : Développement principal
3. **Tests** : Tests unitaires, intégration
4. **Validation** : Revue, qualité, documentation
5. **Finalisation** : Nettoyage, commit, déploiement

## Gestion des Erreurs

- **Fichier introuvable** : Demander confirmation du chemin
- **Prompt vide** : Demander le contenu via AskUserQuestion
- **Prompt trop vague** : Demander des précisions
- **Permission denied** : Vérifier droits d'écriture

## Standards Qualité

Le prompt transformé DOIT :
- Contenir minimum 3 tâches
- Avoir au moins 2 phases
- Inclure le JSON TodoWrite complet
- Fournir des critères de validation
- Ne contenir aucune variable `{...}` non substituée
