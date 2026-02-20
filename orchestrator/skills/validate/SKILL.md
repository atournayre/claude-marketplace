---
name: orchestrator:validate
description: Vérifie la checklist (PHP, API ou sécurité) avant exécution. Effectue les vérifications automatiques (PHPStan, PSR-12, tests, Elegant Objects, sécurité) et liste les points à vérifier manuellement.
argument-hint: "[--checklist=php|api|security] [--path=<directory>]"
model: sonnet
allowed-tools: [Read, Bash, Grep, Glob, AskUserQuestion]
version: 1.0.0
license: MIT
---

# orchestrator:validate

Validation de checklist avant exécution du code.

## Instructions à Exécuter

### 1. Parser les arguments

```
/orchestrator:validate [--checklist=<name>] [--path=<directory>]
```

- `--checklist=php` (défaut), `api`, `security`
- `--path=src/` (défaut : `src/`)

### 2. Lire la checklist

Chercher dans `prompt/templates/checklists/{checklist}.md` ou équivalent dans le projet.

### 3. Vérifications automatiques

**PHPStan :**
```bash
./vendor/bin/phpstan analyse --error-format=raw 2>/dev/null | head -20
```

**PSR-12 :**
```bash
./vendor/bin/php-cs-fixer fix --dry-run --diff 2>/dev/null | head -20
```

**Tests :**
```bash
./vendor/bin/phpunit --list-tests 2>/dev/null | wc -l
```

**Elegant Objects (via Grep) :**
```bash
# Classes sans final
grep -r "^class " --include="*.php" {path} | grep -v "final"
# Setters
grep -r "public function set" --include="*.php" {path}
```

**Sécurité (via Grep) :**
```bash
grep -rn "password\s*=" --include="*.php" {path}
grep -rn "->query(" --include="*.php" {path}
```

### 4. Générer le rapport

```
Validation : checklist-{name}.md

Vérifications automatiques

  PHPStan niveau 9 : 0 erreur
  PSR-12 : conforme
  Classes non final : 3 fichiers
  Setters détectés : 2 occurrences
  Tests présents : 47 tests

Vérifications manuelles requises

  - [ ] Pattern AAA dans les tests
  - [ ] Cas edge cases couverts

Résumé

  | Catégorie | Passé | Echoué | Manuel |
  |-----------|-------|--------|--------|
  | Code      | 3     | 1      | 2      |

Score : 6/10 Corrections requises avant exécution
```

### 5. Recommandations si points échouent

```
Corrections suggérées :

1. Classes non final :
   -> Ajouter `final` devant `class`

2. Setters détectés :
   -> Remplacer par factory statique
```

## Codes de sortie

- `0` : Tout validé
- `1` : Avertissements — peut continuer avec prudence
- `2` : Erreurs bloquantes — corriger avant exécution

## Exemples

```bash
/orchestrator:validate
/orchestrator:validate --checklist=api
/orchestrator:validate --checklist=security --path=src/Security/
```
