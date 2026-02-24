---
name: orchestrator:team
description: Orchestre une équipe d'agents spécialisés pour les tâches complexes. Auto-détecte le type (feature/refactor/api/fix), compose l'équipe, coordonne les phases analyse -> challenge -> implémentation -> QA.
argument-hint: "[type] <description> [--agents=analyst,implementer] [--safe]"
model: sonnet
allowed-tools: [Task, TaskCreate, TaskUpdate, TaskList, TeamCreate, TeamDelete, SendMessage, AskUserQuestion, Read, Write, Grep, Glob, Bash]
version: 1.0.0
license: MIT
---

# orchestrator:team

Orchestration d'une équipe d'agents natifs pour les tâches de développement complexes. Tu es le **team lead** : tu crées l'équipe, distribues les tâches, coordonnes les phases et rapportes les résultats.

## Invocation

```
/orchestrator:team "<description>"
/orchestrator:team <type> "<description>"
/orchestrator:team "<description>" --agents=analyst,implementer
/orchestrator:team "<description>" --safe
```

## Architecture des agents

| Agent | Rôle | Outils |
|-------|------|--------|
| **analyst** | Architecture + design | Read, Grep, Glob, Bash |
| **challenger** | Challenge + QA review | Read, Grep, Glob, Bash |
| **implementer** | Développement + tests | Read, Write, Edit, Grep, Glob, Bash |

## Fichiers intermédiaires

```
{scratchpad}/prompt-{slug}/
  01-analysis.md
  02-challenge.md
  03-plan.md
  04-implementation.md
  05-qa-report.md
```

## Modes d'exécution

| Mode | Condition | Comportement |
|------|-----------|-------------|
| **Normal** | RAM >= 4 GB | Parallèle intra-phase (max 2 agents) |
| **Safe** | RAM 2-4 GB ou `--safe` | Séquentiel strict (1 agent) |
| **Abort** | RAM < 2 GB | Abandon, proposer alternative |

## Workflow

### Phase 0 : Initialisation

1. Parser les arguments (description, type, --agents, --safe)
2. Auto-détecter le type si absent (feature/refactor/api/fix)
3. Composer l'équipe selon le type :
   - `feature` : analyst + challenger + implementer
   - `refactor` : analyst + implementer
   - `api` : analyst + challenger + implementer
   - `fix` : challenger + implementer
4. Health check RAM
5. `TeamCreate("prompt-{slug}")`
6. Créer les tâches avec dépendances (TaskCreate #1 à #6)

### Phase 1 : Analyse

Agent analyst (+ challenger en parallèle si mode Normal).
Output : `{scratchpad}/prompt-{slug}/01-analysis.md`

### Phase 2 : Challenge

Agent challenger lit `01-analysis.md`, produit `02-challenge.md`.
Shutdown de tous les agents d'analyse après cette phase.

### Phase 3 : Synthèse + validation

Team lead (pas d'agent) :
1. Lire `01-analysis.md` et `02-challenge.md`
2. Produire synthèse courte
3. Demander validation via AskUserQuestion (Valider / Ajuster / Arrêter)
4. Écrire `03-plan.md`

### Phase 4 : Implémentation

Agent implementer lit `03-plan.md` + `01-analysis.md` + `02-challenge.md`.
Output : `{scratchpad}/prompt-{slug}/04-implementation.md`
Shutdown après.

### Phase 5 : QA + Review

Agent challenger-qa (nouvelle instance) :
- Lit `02-challenge.md` + `04-implementation.md`
- Exécute `git diff` + outils QA (PHPStan, tests, linters)
- Output : `{scratchpad}/prompt-{slug}/05-qa-report.md`
Shutdown après.

### Phase 6 : Cleanup + rapport

Team lead :
1. Lire `05-qa-report.md`
2. Afficher rapport final
3. Vérifier processus orphelins
4. `TeamDelete()`

## Limites

| Règle | Valeur |
|-------|--------|
| Max agents simultanés (Normal) | 2 |
| Max agents simultanés (Safe) | 1 |
| Max turns analyse | 15 |
| Max turns QA/review | 20 |
| Max turns implementer | 30 |
| RAM minimum | 2 GB |

## Résultat

```markdown
## Rapport final — [Description de la tâche]

### Équipe mobilisée
- analyst : [durée]
- challenger : [durée]
- implementer : [durée]

### Fichiers créés
- [fichier] : [description]

### Fichiers modifiés
- [fichier] : [nature de la modification]

### Concerns adressés
- [concern BLOQUANT] : résolu via [approche]

### QA
- PHPStan : PASS / FAIL (X erreurs)
- Tests : PASS / FAIL (X/Y)

### Points d'attention
- [Élément nécessitant une vérification manuelle]
```

## Règles

- Fichiers intermédiaires pour communication inter-agents
- Shutdown entre les phases (0 agent en mémoire entre phases)
- Health check RAM entre chaque phase
- Validation utilisateur OBLIGATOIRE en Phase 3 avant implémentation
- Ne jamais créer de commits Git
