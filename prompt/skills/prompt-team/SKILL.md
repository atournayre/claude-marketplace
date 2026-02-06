---
name: prompt:team
description: "Orchestre une équipe d'agents spécialisés pour les tâches complexes. Auto-détecte le type, compose l'équipe, coordonne les phases analyse → challenge → implémentation → QA."
model: sonnet
allowed-tools: [Task, TaskCreate, TaskUpdate, TaskList, TeamCreate, TeamDelete, SendMessage, AskUserQuestion, Read, Grep, Glob, Bash]
version: 1.0.0
license: MIT
---

# Objectif

Orchestrer une équipe d'agents natifs via Agent Teams pour les tâches de développement complexes. Tu es le **team lead** : tu crées l'équipe, distribues les tâches, coordonnes les phases et rapportes les résultats.

## Invocation

```
/prompt:team "<description>"
/prompt:team <type> "<description>"
/prompt:team "<description>" --agents=architect,developer,qa
```

## Workflow

### Phase 0 : Initialisation

#### 1. Parser les arguments

Extraire :
- `description` : la description en langage naturel (obligatoire)
- `type` : feature / refactor / api / fix (optionnel, auto-détecté)
- `--agents=` : override de la composition d'équipe (optionnel)

#### 2. Auto-détecter le type

Si le type n'est pas explicite, analyser la description :

| Mots-clés | Type détecté |
|-----------|-------------|
| ajouter, créer, nouveau, implémenter, feature, fonctionnalité | `feature` |
| refactorer, simplifier, restructurer, nettoyer, extraire, déplacer | `refactor` |
| api, endpoint, webhook, intégration, REST, GraphQL | `api` |
| corriger, fixer, bug, erreur, régression, crash, 500 | `fix` |

Si ambiguïté, demander via AskUserQuestion :

```json
{
  "questions": [{
    "question": "Quel type de tâche ?",
    "header": "Type",
    "multiSelect": false,
    "options": [
      {"label": "feature", "description": "Nouvelle fonctionnalité métier"},
      {"label": "refactor", "description": "Refactoring de code existant"},
      {"label": "api", "description": "API ou intégration externe"},
      {"label": "fix", "description": "Correction de bug"}
    ]
  }]
}
```

#### 3. Composer l'équipe

**Par défaut selon le type :**

| Type | Agents |
|------|--------|
| `feature` | architect, designer, challenger, developer, tester, qa |
| `refactor` | architect, challenger, developer, qa |
| `api` | architect, designer, challenger, developer, tester, qa |
| `fix` | challenger, developer, tester, qa |

**Override avec `--agents=` :**
Si l'utilisateur passe `--agents=architect,developer,qa`, utiliser uniquement ces agents.

#### 4. Créer l'équipe et les tâches

```
TeamCreate("prompt-{slug}")
```

Où `{slug}` est la description slugifiée (ex: "gestion-des-factures").

Créer les tâches avec dépendances :

```
TaskCreate #1: "Analyse architecturale"        → libre
TaskCreate #2: "Design DDD"                     → libre
TaskCreate #3: "Challenge des propositions"     → addBlockedBy [#1, #2]
TaskCreate #4: "Synthèse + validation"          → addBlockedBy [#3]
TaskCreate #5: "Implémentation code"            → addBlockedBy [#4]
TaskCreate #6: "Écriture des tests"             → addBlockedBy [#4]
TaskCreate #7: "QA + Review finale"             → addBlockedBy [#5, #6]
TaskCreate #8: "Rapport final + cleanup"        → addBlockedBy [#7]
```

Note : adapter les tâches selon les agents composés. Par exemple pour `fix`, pas de tâche #1 ni #2.

Afficher :

```
Équipe prompt-{slug} créée

Type détecté : {type}
Agents : {liste agents}
Tâches : {nombre} créées avec dépendances

Démarrage de l'analyse...
```

### Phase 1 : Analyse (parallèle)

**Agents :** prompt-architect + prompt-designer (si dans l'équipe)

Spawner les agents en parallèle comme team members :

```
Task(subagent_type="general-purpose", team_name="prompt-{slug}", name="prompt-architect")
Task(subagent_type="general-purpose", team_name="prompt-{slug}", name="prompt-designer")
```

**Prompt de chaque agent :**
- Description de la tâche
- Instruction de lire son propre fichier agent (`prompt/agents/prompt-{role}.md`)
- Contexte : description utilisateur

Les agents :
- Explorent le codebase
- Produisent leurs outputs (architecture, design)
- PEUVENT communiquer entre eux via SendMessage

Quand ils terminent → `TaskUpdate` les tâches en `completed`.

**Gestion d'erreur :**
- Si un seul agent échoue : continuer avec l'autre + warning
- Si les deux échouent : arrêter et signaler à l'utilisateur

### Phase 2 : Challenge (séquentiel)

**Agent :** prompt-challenger

Spawner le challenger avec les outputs des phases précédentes :

```
Task(subagent_type="general-purpose", team_name="prompt-{slug}", name="prompt-challenger")
```

**Prompt :**
- Outputs de l'architecte et du designer
- Instruction de lire `prompt/agents/prompt-challenger.md`
- Focus : identifier les concerns BLOQUANT / IMPORTANT / SUGGESTION

Le challenger PEUT envoyer des questions aux agents précédents via SendMessage.

Quand terminé → `TaskUpdate` tâche #3 en `completed`.

**Gestion d'erreur :**
- Si le challenger échoue : présenter les propositions sans challenge

### Phase 3 : Synthèse + validation utilisateur

**Acteur :** le team lead (ce skill)

1. Consolider les outputs : architecture + design + challenges
2. Présenter une synthèse structurée :

```
## Synthèse de l'analyse

### Architecture proposée
[Résumé de l'architecte]

### Design DDD
[Résumé du designer]

### Concerns identifiés
- BLOQUANT : [liste]
- IMPORTANT : [liste]
- SUGGESTION : [liste]

### Plan d'implémentation
1. [Étape 1]
2. [Étape 2]
...
```

3. Demander validation via AskUserQuestion :

```json
{
  "questions": [{
    "question": "Comment procéder ?",
    "header": "Action",
    "multiSelect": false,
    "options": [
      {"label": "Valider", "description": "Lancer l'implémentation selon le plan"},
      {"label": "Ajuster", "description": "Modifier le plan avant implémentation"},
      {"label": "Arrêter", "description": "Stopper ici (analyse uniquement)"}
    ]
  }]
}
```

- **Valider** : continuer à Phase 4
- **Ajuster** : demander les modifications, itérer, re-présenter
- **Arrêter** : afficher le rapport final, cleanup, terminer

### Phase 4 : Implémentation (parallèle)

**Agents :** prompt-developer + prompt-tester (si dans l'équipe)

Spawner en parallèle :

```
Task(subagent_type="general-purpose", team_name="prompt-{slug}", name="prompt-developer")
Task(subagent_type="general-purpose", team_name="prompt-{slug}", name="prompt-tester")
```

**Prompt developer :**
- Plan validé (architecture + design + concerns adressés)
- Instruction de lire `prompt/agents/prompt-developer.md`
- Liste des fichiers à créer/modifier

**Prompt tester :**
- Spécifications du designer
- Concerns du challenger (edge cases)
- Instruction de lire `prompt/agents/prompt-tester.md`

Les agents PEUVENT communiquer entre eux (tester signale tests qui échouent, developer demande le comportement attendu).

Quand terminés → `TaskUpdate` tâches #5 et #6 en `completed`.

**Gestion d'erreur :**
- Si developer échoue : proposer `/prompt:start` comme fallback
- Si tester échoue : logger warning, QA compensera en phase 5

### Phase 5 : QA + Review finale

**Agents :** prompt-qa + prompt-challenger (si dans l'équipe)

Spawner en parallèle :

```
Task(subagent_type="general-purpose", team_name="prompt-{slug}", name="prompt-qa")
Task(subagent_type="general-purpose", team_name="prompt-{slug}", name="prompt-challenger")
```

**Prompt QA :**
- Instruction de lire `prompt/agents/prompt-qa.md`
- Découvrir et exécuter tous les outils QA du projet (Phase 0 : scanner Makefile, composer.json, package.json, vendor/bin/, fichiers de config)
- Si URL disponible : tester l'UI via Chrome

**Prompt challenger (review finale) :**
- Code implémenté (git diff)
- Instruction de lire `prompt/agents/prompt-challenger.md` (section Mode 2)
- Focus : le code implémenté adresse-t-il les concerns initiaux ?

Les agents PEUVENT signaler des problèmes au developer via SendMessage.

Quand terminés → `TaskUpdate` tâche #7 en `completed`.

**Gestion d'erreur :**
- Si QA échoue : proposer `/prompt:validate` comme fallback
- Si challenger échoue : logger warning, QA suffira

### Phase 6 : Cleanup + rapport final

1. Consolider les rapports QA + review
2. Afficher le rapport final :

```
## Rapport final - prompt-{slug}

### Résumé
- Type : {type}
- Agents utilisés : {liste}
- Tâches complétées : X/Y

### Résultats QA
[Rapport QA condensé]

### Review finale
[Verdict du challenger]

### Fichiers modifiés
[Liste des fichiers créés/modifiés]

### Prochaines étapes
- [ ] Vérifier manuellement les changements
- [ ] /git:commit pour committer
- [ ] /git:git-pr pour créer la PR
```

3. Shutdown tous les agents :

```
SendMessage(type="shutdown_request", recipient="prompt-architect")
SendMessage(type="shutdown_request", recipient="prompt-designer")
...
```

4. Nettoyer l'équipe :

```
TeamDelete()
```

## Règles

- **Task Management** : toutes les tâches doivent être créées au démarrage avec `activeForm` et dépendances `addBlockedBy`
- **Communication** : utiliser SendMessage pour la communication inter-agents, pas de Bash
- **Validation utilisateur** : toujours demander validation en Phase 3 avant implémentation
- **Cleanup** : toujours shutdown les agents et TeamDelete en fin de session
- **Gestion d'erreurs** : appliquer les fallbacks définis, ne jamais laisser un agent en erreur sans action
- **Restriction** : ne JAMAIS créer de commits Git, l'utilisateur gère les commits
