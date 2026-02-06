---
title: "prompt"
description: "Système hybride Starters + Mode Plan + Checklists + Agent Teams pour développement efficace - Templates légers, exploration contextuelle, validation automatisée, orchestration multi-agents"
version: "2.1.1"
---

# prompt <Badge type="info" text="v2.1.1" />


Système hybride combinant prompts structurés et mode plan pour un développement efficace.

## Philosophie

**Avant (v1.x)** : Templates longs (300+ lignes) avec tout le code boilerplate.

**Maintenant (v2.x)** : Starters légers (15 lignes) + Mode Plan + Checklists + Agent Teams.

```
┌─────────────────────────────────────────────────────────────┐
│  MODE SOLO                                                   │
│  1. STARTER (10-15 lignes)                                  │
│     → Contexte minimal + contraintes + livrable attendu     │
│  2. MODE PLAN (exploration + adaptation)                    │
│     → Claude explore le codebase et propose un plan         │
│  3. VALIDATION (checklist automatique)                      │
│     → Vérification avant exécution                          │
├─────────────────────────────────────────────────────────────┤
│  MODE TEAM (v2.1+)                                          │
│  /prompt:team "description"                                 │
│     → Équipe d'agents spécialisés auto-composée             │
│     → Workflow : Analyse → Challenge → Implémentation → QA  │
│     → Communication inter-agents native                     │
└─────────────────────────────────────────────────────────────┘
```

## Installation

Le plugin est automatiquement disponible via le marketplace.

## Slash Commands

| Command | Description |
|---------|-------------|
| `/prompt:start` | Démarre avec un starter + active le mode plan |
| `/prompt:team` | Orchestre une équipe d'agents spécialisés |
| `/prompt:validate` | Vérifie la checklist et liste les oublis |
| `/prompt:transform` | Transforme un prompt en tâches exécutables |

## Usage

### Mode Team (multi-agents)

```bash
# Le plus simple - type auto-détecté, équipe par défaut
/prompt:team "Gestion des factures"

# Avec type explicite
/prompt:team feature "Gestion des factures"

# Correction de bug - équipe réduite (challenger, developer, tester, qa)
/prompt:team "Corriger le bug de login"

# Override agents
/prompt:team "Simplifier PaymentService" --agents=architect,developer,qa
```

#### Agents disponibles

| Agent | Rôle | Accès écriture |
|-------|------|----------------|
| `architect` | Architecture, patterns, structure codebase | Non |
| `designer` | Design DDD, contrats, interfaces, data flow | Non |
| `challenger` | Avocat du diable, edge cases, sécurité | Non |
| `developer` | Implémentation code selon plan validé | Oui |
| `tester` | Écriture tests PHPUnit (TDD) | Oui |
| `qa` | PHPStan, CS-Fixer, tests, Chrome UI | Non |

#### Équipes par défaut

| Type | Agents |
|------|--------|
| `feature` | architect, designer, challenger, developer, tester, qa |
| `refactor` | architect, challenger, developer, qa |
| `api` | architect, designer, challenger, developer, tester, qa |
| `fix` | challenger, developer, tester, qa |

### Mode Solo (démarrage rapide)

```bash
# Feature métier
/prompt:start feature "Gestion des factures" --entity=Invoice --context=Billing

# Refactoring
/prompt:start refactor "Simplifier la validation" --target=src/Validator/

# API/Intégration
/prompt:start api "Intégration Stripe" --service=Stripe

# Bug fix
/prompt:start fix "Erreur 500 sur login" --target=src/Security/
```

### Validation avant exécution

```bash
# Validation PHP standard
/prompt:validate

# Validation API
/prompt:validate --checklist=api

# Validation sécurité
/prompt:validate --checklist=security
```

## Starters disponibles

| Starter | Fichier | Usage |
|---------|---------|-------|
| `feature` | starters/feature.md | Nouvelle fonctionnalité métier |
| `refactor` | starters/refactor.md | Refactoring de code existant |
| `api` | starters/api.md | API ou intégration externe |
| `fix` | starters/fix.md | Correction de bug |

## Checklists disponibles

| Checklist | Fichier | Points vérifiés |
|-----------|---------|-----------------|
| `php` | checklists/php.md | PHPStan, PSR-12, Elegant Objects, tests |
| `api` | checklists/api.md | Validation, auth, rate-limit, logging |
| `security` | checklists/security.md | OWASP, injection, auth, données sensibles |

## Workflow complet

```bash
# 1. Démarrer avec un starter (active automatiquement le mode plan)
/prompt:start feature "Gestion des factures" --entity=Invoice

# 2. Claude explore le codebase et propose un plan
# 3. Tu valides/ajustes le plan

# 4. Avant d'exécuter, valider la checklist
/prompt:validate

# 5. Si tout est OK, exécuter le plan
```

## Avantages vs anciens templates

| Aspect | Avant (v1.x) | Maintenant (v2.x) |
|--------|--------------|-------------------|
| Taille template | 300-400 lignes | 10-15 lignes |
| Flexibilité | Code boilerplate fixe | Adapté au contexte |
| Exploration | Manuelle | Mode plan automatique |
| Validation | Manuelle | Checklist automatisée |
| Temps de setup | Remplir variables | Description simple |

## Structure du plugin

```
prompt/
├── agents/                # Agents spécialisés (6 agents)
│   ├── prompt-architect.md
│   ├── prompt-designer.md
│   ├── prompt-challenger.md
│   ├── prompt-developer.md
│   ├── prompt-tester.md
│   └── prompt-qa.md
├── templates/
│   ├── starters/          # Starters légers (4 fichiers)
│   │   ├── feature.md
│   │   ├── refactor.md
│   │   ├── api.md
│   │   └── fix.md
│   └── checklists/        # Checklists de validation (3 fichiers)
│       ├── php.md
│       ├── api.md
│       └── security.md
├── skills/
│   ├── prompt-start/      # Skill hybride starter + plan
│   ├── prompt-team/       # Skill orchestrateur multi-agents
│   ├── prompt-validate/   # Skill de validation
│   └── prompt-transform/  # Conversion en tâches
└── scripts/               # Scripts utilitaires
```

## Licence

MIT
