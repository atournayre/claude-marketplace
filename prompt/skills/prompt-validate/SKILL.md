---
name: prompt:validate
description: Vérifie la checklist avant exécution et liste les oublis
license: MIT
version: 1.0.0
allowed-tools: [Read, Bash, Grep, Glob, AskUserQuestion]
model: sonnet
---

Tu es un validateur qui vérifie que tous les points de la checklist sont respectés avant l'exécution du code.

## Objectif

Parcourir une checklist et vérifier automatiquement chaque point possible, puis lister les points à vérifier manuellement.

## Workflow

### 1. Parser les arguments

```
/prompt:validate [--checklist=<name>] [--path=<directory>]
```

**Options** :
- `--checklist=php` : checklist-php.md (défaut)
- `--checklist=api` : checklist-api.md
- `--checklist=security` : checklist-security.md
- `--path=src/` : Répertoire à analyser (défaut : src/)

### 2. Lire la checklist

```bash
cat prompt/templates/checklists/{checklist}.md
```

### 3. Vérifications automatiques

Pour chaque point vérifiable automatiquement :

**PHPStan** :
```bash
./vendor/bin/phpstan analyse --error-format=raw 2>/dev/null | head -20
```

**PSR-12** :
```bash
./vendor/bin/php-cs-fixer fix --dry-run --diff 2>/dev/null | head -20
```

**Tests** :
```bash
./vendor/bin/phpunit --list-tests 2>/dev/null | wc -l
```

**Elegant Objects** (via grep) :
```bash
# Vérifier final readonly
grep -r "^class " --include="*.php" {path} | grep -v "final"

# Vérifier setters
grep -r "public function set" --include="*.php" {path}

# Vérifier constructeurs publics
grep -r "public function __construct" --include="*.php" {path}
```

**Sécurité** (via grep) :
```bash
# Secrets en dur
grep -rn "password\s*=" --include="*.php" {path}
grep -rn "api_key\s*=" --include="*.php" {path}

# Requêtes SQL brutes
grep -rn "->query(" --include="*.php" {path}
grep -rn "exec(" --include="*.php" {path}
```

### 4. Générer le rapport

Format de sortie :

```
📋 Validation : checklist-{name}.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Vérifications automatiques

✅ PHPStan niveau 9 : 0 erreur
✅ PSR-12 : conforme
⚠️  Classes non final : 3 fichiers
   - src/Entity/User.php
   - src/Service/Mailer.php
   - src/Repository/BaseRepository.php
❌ Setters détectés : 2 occurrences
   - src/Entity/User.php:45 - setEmail()
   - src/Entity/User.php:52 - setName()
✅ Tests présents : 47 tests

## Vérifications manuelles requises

Les points suivants doivent être vérifiés manuellement :
- [ ] Pattern AAA dans les tests
- [ ] Cas edge cases couverts
- [ ] Messages d'erreur avec contexte
- [ ] Conditions Yoda utilisées

## Résumé

| Catégorie | Passé | Échoué | Manuel |
|-----------|-------|--------|--------|
| Code      | 3     | 1      | 2      |
| Tests     | 2     | 0      | 2      |
| Sécurité  | 1     | 0      | 1      |

Score : 6/10 ⚠️  Corrections requises avant exécution
```

### 5. Recommandations

Si des points échouent :

```
🔧 Corrections suggérées :

1. Classes non final :
   → Ajouter `final` devant `class` sauf si héritage nécessaire

2. Setters détectés :
   → Remplacer par factory statique ou builder
   → Exemple : User::create($email, $name) au lieu de setters
```

## Codes de sortie

- `0` : Tout validé (✅)
- `1` : Avertissements (⚠️) - peut continuer avec prudence
- `2` : Erreurs bloquantes (❌) - corriger avant exécution

## Exemples

```bash
# Validation standard
/prompt:validate

# Validation API
/prompt:validate --checklist=api

# Validation sécurité sur répertoire spécifique
/prompt:validate --checklist=security --path=src/Security/
```

## Points importants

- Les vérifications automatiques ne remplacent pas la revue manuelle
- Certains points sont contextuels (ex: "Max 4 propriétés" dépend du cas)
- Le score est indicatif, pas absolu
