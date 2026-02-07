---
name: prompt:team
description: "Orchestre une équipe d'agents spécialisés pour les tâches complexes. Auto-détecte le type, compose l'équipe, coordonne les phases analyse → challenge → implémentation → QA."
model: sonnet
allowed-tools: [Task, TaskCreate, TaskUpdate, TaskList, TeamCreate, TeamDelete, SendMessage, AskUserQuestion, Read, Write, Grep, Glob, Bash]
version: 2.0.0
license: MIT
---

# Objectif

Orchestrer une équipe d'agents natifs via Agent Teams pour les tâches de développement complexes. Tu es le **team lead** : tu crées l'équipe, distribues les tâches, coordonnes les phases et rapportes les résultats.

## Invocation

```
/prompt:team "<description>"
/prompt:team <type> "<description>"
/prompt:team "<description>" --agents=analyst,implementer
/prompt:team "<description>" --safe
```

## Architecture

### Agents fusionnés

L'équipe utilise 3 agents au lieu de 6 pour limiter la consommation de ressources :

| Agent | Fusionne | Fichier agent | Outils |
|-------|----------|---------------|--------|
| **analyst** | architect + designer | `prompt/agents/prompt-analyst.md` | Read, Grep, Glob, Bash |
| **challenger** | challenger + QA review | `prompt/agents/prompt-challenger.md` | Read, Grep, Glob, Bash |
| **implementer** | developer + tester | `prompt/agents/prompt-implementer.md` | Read, Write, Edit, Grep, Glob, Bash |

### Fichiers intermédiaires

Les agents communiquent via des fichiers dans le scratchpad, pas dans le contexte du team lead. Cela évite la saturation du contexte et la perte d'information lors de la compression.

```
{scratchpad}/prompt-{slug}/
  01-analysis.md        <- output analyst (architecture + design)
  02-challenge.md       <- output challenger (concerns)
  03-plan.md            <- synthèse validée par l'utilisateur (écrit par le team lead)
  04-implementation.md  <- résumé implementer (fichiers créés/modifiés)
  05-qa-report.md       <- rapport QA du challenger
```

Chaque agent :
- **Lit** les fichiers dont il a besoin (pas tout le contexte)
- **Écrit** son output dans son fichier dédié
- Le team lead ne garde en contexte qu'un **résumé court** de chaque phase

### Modes d'exécution

| Mode | Condition | Comportement |
|------|-----------|-------------|
| **Normal** | RAM >= 4 GB | Parallèle intra-phase (max 2 agents), shutdown entre phases |
| **Safe** | RAM >= 2 GB et < 4 GB, ou `--safe` | Séquentiel strict (1 agent), shutdown après chaque agent |
| **Abort** | RAM < 2 GB | Abandon, proposer `/prompt:start` comme alternative |

## Workflow

### Phase 0 : Initialisation

#### 1. Parser les arguments

Extraire :
- `description` : la description en langage naturel (obligatoire)
- `type` : feature / refactor / api / fix (optionnel, auto-détecté)
- `--agents=` : override de la composition d'équipe (optionnel)
- `--safe` : force le mode séquentiel strict (1 agent à la fois)

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

| Type | Agents | Total |
|------|--------|-------|
| `feature` | analyst, challenger, implementer | 3 |
| `refactor` | analyst, implementer | 2 |
| `api` | analyst, challenger, implementer | 3 |
| `fix` | challenger, implementer | 2 |

**Override avec `--agents=` :**
Si l'utilisateur passe `--agents=analyst,implementer`, utiliser uniquement ces agents.

#### 4. Health check système

Avant de créer l'équipe, vérifier les ressources disponibles :

```bash
free -m | grep Mem | awk '{print $7}'
```

| RAM disponible | Mode |
|---------------|------|
| >= 4 GB | Normal (parallèle intra-phase, max 2 agents simultanés) |
| >= 2 GB et < 4 GB | Safe (séquentiel strict, 1 agent à la fois) |
| < 2 GB | Abort : afficher un warning et proposer `/prompt:start` comme alternative |

Si `--safe` est passé, forcer le mode safe indépendamment de la RAM.

Afficher le mode détecté :

```
Ressources système : {X} GB disponibles -> mode {normal|safe|abort}
```

#### 5. Créer le répertoire intermédiaire

```bash
mkdir -p {scratchpad}/prompt-{slug}
```

#### 6. Créer l'équipe et les tâches

```
TeamCreate("prompt-{slug}")
```

Où `{slug}` est la description slugifiée (ex: "gestion-des-factures").

Créer les tâches avec dépendances :

```
TaskCreate #1: "Analyse (architecture + design)"   -> libre
TaskCreate #2: "Challenge des propositions"         -> addBlockedBy [#1]
TaskCreate #3: "Synthèse + validation utilisateur"  -> addBlockedBy [#2]
TaskCreate #4: "Implémentation (code + tests)"      -> addBlockedBy [#3]
TaskCreate #5: "QA + Review finale"                 -> addBlockedBy [#4]
TaskCreate #6: "Rapport final + cleanup"            -> addBlockedBy [#5]
```

Note : adapter les tâches selon les agents composés. Par exemple pour `fix`, pas de tâche #1 (analyse).

Afficher :

```
Equipe prompt-{slug} créée

Type détecté : {type}
Mode : {normal|safe}
Agents : {liste agents}
Tâches : {nombre} créées
Fichiers intermédiaires : {scratchpad}/prompt-{slug}/

Démarrage...
```

---

### Phase 1 : Analyse

**Agent :** prompt-analyst (si dans l'équipe)

**`TaskUpdate` tâche #1 -> `in_progress`**

#### Mode Normal (parallèle avec challenger)

Si le challenger est dans l'équipe, spawner analyst ET challenger en parallèle. Le challenger explore le codebase de son côté pendant que l'analyst produit son analyse.

```
Task(subagent_type="general-purpose", team_name="prompt-{slug}", name="prompt-analyst", max_turns=15)
Task(subagent_type="general-purpose", team_name="prompt-{slug}", name="prompt-challenger", max_turns=15)
```

Les 2 agents tournent en parallèle (max 2 processus). Ils PEUVENT communiquer entre eux via SendMessage :
- Le challenger peut poser des questions à l'analyst
- L'analyst peut demander au challenger de vérifier un point

#### Mode Safe (séquentiel)

Spawner uniquement l'analyst :

```
Task(subagent_type="general-purpose", team_name="prompt-{slug}", name="prompt-analyst", max_turns=15)
```

#### Prompt analyst

- Description de la tâche
- Instruction de lire `prompt/agents/prompt-analyst.md`
- Contexte : description utilisateur
- **Écrire l'output dans `{scratchpad}/prompt-{slug}/01-analysis.md`**

Quand l'analyst termine -> `TaskUpdate` tâche #1 en `completed`.

**Gestion d'erreur :**
- Si l'analyst échoue : continuer avec le challenger seul si actif, sinon arrêter

---

### Phase 2 : Challenge

**Agent :** prompt-challenger (si dans l'équipe)

**`TaskUpdate` tâche #2 -> `in_progress`**

#### Mode Normal

Le challenger a déjà été spawné en Phase 1 et a exploré le codebase en parallèle. Lui envoyer l'analyse :

```
SendMessage(type="message", recipient="prompt-challenger", content="L'analyse est terminée. Lis {scratchpad}/prompt-{slug}/01-analysis.md et produis ton rapport de challenge dans {scratchpad}/prompt-{slug}/02-challenge.md")
```

#### Mode Safe

Shutdown l'analyst d'abord, puis spawner le challenger :

```
SendMessage(type="shutdown_request", recipient="prompt-analyst")
Task(subagent_type="general-purpose", team_name="prompt-{slug}", name="prompt-challenger", max_turns=15)
```

#### Prompt challenger

- Instruction de lire `prompt/agents/prompt-challenger.md` (Mode 1)
- **Lire** `{scratchpad}/prompt-{slug}/01-analysis.md`
- Focus : identifier les concerns BLOQUANT / IMPORTANT / SUGGESTION
- **Écrire l'output dans `{scratchpad}/prompt-{slug}/02-challenge.md`**

Quand le challenger termine -> `TaskUpdate` tâche #2 en `completed`.

**Shutdown de la phase d'analyse :**

Tous les agents de la phase d'analyse ont terminé. Shutdown :

```
SendMessage(type="shutdown_request", recipient="prompt-analyst")   # si encore actif (mode Normal)
SendMessage(type="shutdown_request", recipient="prompt-challenger")
```

-> **0 agent en mémoire**

**Gestion d'erreur :**
- Si le challenger échoue : shutdown + présenter les propositions sans challenge

---

### Phase 3 : Synthèse + validation utilisateur

**Acteur :** le team lead (ce skill)

**`TaskUpdate` tâche #3 -> `in_progress`**

1. **Lire** les fichiers intermédiaires (pas tout stocker en contexte) :

```
Read("{scratchpad}/prompt-{slug}/01-analysis.md")
Read("{scratchpad}/prompt-{slug}/02-challenge.md")
```

2. Produire une **synthèse courte** et la présenter à l'utilisateur :

```
## Synthèse de l'analyse

### Architecture proposée
[Résumé en 5-10 lignes de l'analyse]

### Concerns identifiés
- BLOQUANT : [liste]
- IMPORTANT : [liste]
- SUGGESTION : [liste]

### Plan d'implémentation
1. [Étape 1]
2. [Étape 2]
...
```

3. **Écrire** le plan validé dans `{scratchpad}/prompt-{slug}/03-plan.md`

4. Demander validation via AskUserQuestion :

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

- **Valider** : écrire le plan dans `03-plan.md`, continuer à Phase 4
- **Ajuster** : demander les modifications, itérer, re-présenter
- **Arrêter** : afficher le rapport final, cleanup, terminer

**`TaskUpdate` tâche #3 -> `completed`**

---

### Phase 4 : Implémentation

**Agent :** prompt-implementer

**`TaskUpdate` tâche #4 -> `in_progress`**

Health check RAM avant de spawner :

```bash
free -m | grep Mem | awk '{print $7}'
```

Si RAM < 2 GB : proposer d'arrêter ou de continuer en mode safe.

```
Task(subagent_type="general-purpose", team_name="prompt-{slug}", name="prompt-implementer", max_turns=30)
```

#### Prompt implementer

- Instruction de lire `prompt/agents/prompt-implementer.md`
- **Lire** `{scratchpad}/prompt-{slug}/03-plan.md` (plan validé)
- **Lire** `{scratchpad}/prompt-{slug}/01-analysis.md` (architecture + design)
- **Lire** `{scratchpad}/prompt-{slug}/02-challenge.md` (concerns à adresser)
- **Écrire le résumé dans `{scratchpad}/prompt-{slug}/04-implementation.md`**

Quand l'implementer termine -> `TaskUpdate` tâche #4 en `completed`.

**Shutdown :**

```
SendMessage(type="shutdown_request", recipient="prompt-implementer")
```

-> **0 agent en mémoire**

**Gestion d'erreur :**
- Si l'implementer échoue : shutdown + proposer `/prompt:start` comme fallback

---

### Phase 5 : QA + Review finale

**Agent :** prompt-challenger (nouvelle instance, rôle QA + review)

**`TaskUpdate` tâche #5 -> `in_progress`**

```
Task(subagent_type="general-purpose", team_name="prompt-{slug}", name="prompt-challenger-qa", max_turns=20)
```

Note : utiliser le nom `prompt-challenger-qa` car le challenger original a été shutdown en Phase 2.

#### Prompt challenger (mode QA + review)

- Instruction de lire `prompt/agents/prompt-challenger.md` (Mode 2 : review finale)
- Instruction de lire `prompt/agents/prompt-qa.md` (découverte et exécution outils QA)
- **Lire** `{scratchpad}/prompt-{slug}/02-challenge.md` (ses concerns initiaux)
- **Lire** `{scratchpad}/prompt-{slug}/04-implementation.md` (résumé implémentation)
- Exécuter `git diff` pour voir le code implémenté
- Exécuter les outils QA découverts (PHPStan, tests, linters...)
- Focus : le code adresse-t-il les concerns ? Les tests passent-ils ?
- **Écrire le rapport dans `{scratchpad}/prompt-{slug}/05-qa-report.md`**

Quand terminé -> `TaskUpdate` tâche #5 en `completed`.

**Shutdown :**

```
SendMessage(type="shutdown_request", recipient="prompt-challenger-qa")
```

-> **0 agent en mémoire**

**Gestion d'erreur :**
- Si le challenger-qa échoue : shutdown + proposer `/prompt:validate` comme fallback

---

### Phase 6 : Cleanup + rapport final

**`TaskUpdate` tâche #6 -> `in_progress`**

1. **Lire** le rapport QA :

```
Read("{scratchpad}/prompt-{slug}/05-qa-report.md")
```

2. Afficher le rapport final :

```
## Rapport final - prompt-{slug}

### Résumé
- Type : {type}
- Mode : {normal|safe}
- Agents utilisés : {liste}
- Tâches complétées : X/Y

### Résultats QA
[Rapport QA condensé depuis 05-qa-report.md]

### Fichiers modifiés
[Liste depuis 04-implementation.md]

### Prochaines étapes
- [ ] Vérifier manuellement les changements
- [ ] /git:commit pour committer
- [ ] /git:git-pr pour créer la PR
```

3. Vérifier les processus orphelins :

```bash
pgrep -f "claude.*prompt-{slug}" || echo "Aucun processus orphelin"
```

Si des processus orphelins sont détectés :
- Tenter `SendMessage(type="shutdown_request")` pour chaque agent restant
- Signaler à l'utilisateur avec la commande pour forcer : `pkill -f "claude.*prompt-{slug}"`

4. Nettoyer l'équipe :

```
TeamDelete()
```

**`TaskUpdate` tâche #6 -> `completed`**

---

## Gestion des ressources

Les Agent Teams consomment beaucoup de ressources (chaque agent = un processus Node.js séparé). Ces mesures préviennent les freeze CPU, les memory leaks et l'épuisement de la RAM.

### Limites strictes

| Règle | Valeur |
|-------|--------|
| Max agents simultanés (mode Normal) | **2** (parallèle intra-phase) |
| Max agents simultanés (mode Safe) | **1** (séquentiel strict) |
| Max turns par agent d'analyse | **15** |
| Max turns par agent QA/review | **20** |
| Max turns par implementer | **30** |
| RAM minimum pour démarrer | **2 GB** disponibles |
| Max agents total par workflow | **3** (analyst, challenger, implementer) |

### Cycle de vie des agents

Les agents sont regroupés par phase. Le shutdown se fait **entre les phases**, pas après chaque agent individuel. En mode Normal, les agents d'une même phase peuvent communiquer entre eux en temps réel.

```
Phase 1-2 : analyst + challenger (parallèle en Normal, séquentiel en Safe)
            -> shutdown des deux -> 0 agent

Phase 3   : team lead seul -> 0 agent

Phase 4   : implementer seul
            -> shutdown -> 0 agent

Phase 5   : challenger-qa seul (nouvelle instance)
            -> shutdown -> 0 agent
```

Timeline mémoire pour `feature` en mode Normal :

| Phase | Agents actifs | En mémoire |
|-------|--------------|------------|
| 1-2 | analyst + challenger | 2 |
| shutdown | - | 0 |
| 3 | (team lead) | 0 |
| 4 | implementer | 1 |
| shutdown | - | 0 |
| 5 | challenger-qa | 1 |
| shutdown | - | 0 |
| 6 | (team lead) | 0 |

### Fichiers intermédiaires vs contexte

Le team lead ne stocke PAS les outputs complets des agents dans son contexte. Il utilise les fichiers intermédiaires :

| Quand | Le team lead... |
|-------|----------------|
| Un agent écrit son output | Ne lit PAS le fichier immédiatement |
| Il prépare la synthèse (Phase 3) | Lit les fichiers 01 et 02 |
| Il rédige le prompt d'un agent | Indique les fichiers à lire, ne copie pas le contenu |
| Il rédige le rapport final | Lit le fichier 05 uniquement |

Cela garantit que le contexte du team lead reste léger, même sur un workflow `feature` complet avec 3 agents.

### Health check inter-phases

Entre chaque phase, vérifier la RAM disponible :

```bash
free -m | grep Mem | awk '{print $7}'
```

Si la RAM disponible est passée sous 2 GB depuis le dernier check :
1. Afficher un warning
2. Si en mode Normal : basculer en mode Safe pour la suite
3. Si déjà en mode Safe : proposer d'arrêter ou de continuer

### En cas de crash ou freeze

Si un agent ne répond plus (timeout `max_turns` atteint) :
1. Signaler le timeout à l'utilisateur
2. Tenter un `SendMessage(type="shutdown_request")` vers l'agent
3. Continuer avec la phase suivante si possible
4. En fin de workflow, vérifier les processus orphelins : `pgrep -f "claude"`

## Règles

- **Fichiers intermédiaires** : les agents écrivent dans `{scratchpad}/prompt-{slug}/` et lisent les fichiers des phases précédentes — le team lead ne relaie PAS le contenu dans son contexte
- **Max 2 agents simultanés** : en mode Normal, max 2 agents en parallèle dans une même phase ; en mode Safe, max 1
- **Shutdown entre phases** : tous les agents d'une phase sont shutdown avant de passer à la phase suivante
- **max_turns obligatoire** : chaque `Task()` DOIT inclure `max_turns` pour éviter les sessions infinies
- **Health check** : vérifier la RAM disponible en Phase 0 et entre chaque phase
- **Task Management** : toutes les tâches doivent être créées au démarrage avec `activeForm` et dépendances `addBlockedBy`
- **Validation utilisateur** : toujours demander validation en Phase 3 avant implémentation
- **Cleanup** : vérifier les processus orphelins et TeamDelete en fin de session
- **Gestion d'erreurs** : appliquer les fallbacks définis, toujours shutdown un agent en erreur avant de continuer
- **Restriction** : ne JAMAIS créer de commits Git, l'utilisateur gère les commits
