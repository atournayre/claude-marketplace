---
description: Review qualité complète - PHPStan + Elegant Objects + code review (Phase 6)
model: claude-sonnet-4-5-20250929
allowed-tools: Task, Bash, Read, Grep, Glob
---

# Objectif

Phase 6 du workflow de développement : review qualité complète du code implémenté.

# Prérequis

⚠️ **Plugin feature-dev requis** pour l'agent `code-reviewer`.

Si non installé :
```
/plugin install feature-dev@claude-code-plugins
```

# Instructions

## 1. Lire le contexte

- Lire `.dev-workflow-state.json` pour récupérer les fichiers modifiés
- Si phase 5 (code) non complétée, rediriger vers `/dev:code`

## 2. Lancer les reviews en parallèle

### Review 1 : Code Review (feature-dev)

Lancer l'agent `code-reviewer` avec le focus sur :
- Simplicité / DRY / Élégance
- Bugs / Correction fonctionnelle
- Conventions du projet

### Review 2 : PHPStan

Lancer l'agent `phpstan-error-resolver` (local) :
```
Analyse les fichiers modifiés avec PHPStan niveau 9.
Corrige les erreurs de types stricts.
```

### Review 3 : Elegant Objects

Lancer l'agent `elegant-objects-reviewer` (local) :
```
Vérifie la conformité aux principes Elegant Objects :
- Classes final
- Max 4 attributs
- Pas de getters/setters
- Objets immuables
- Pas de null returns
```

## 3. Consolider les résultats

```
🔍 Résultats de la review

**Code Review :**
{nombre} issues trouvées

Haute priorité :
- [{confiance}%] {description} (`{fichier}:{ligne}`)
  → {suggestion de fix}

Moyenne priorité :
- [{confiance}%] {description} (`{fichier}:{ligne}`)
  → {suggestion de fix}

---

**PHPStan (niveau 9) :**
{nombre} erreurs

- `{fichier}:{ligne}` : {erreur}
  → {fix proposé}

---

**Elegant Objects :**
Score de conformité : {X}/100

Violations :
- `{fichier}` : {violation}
  → {recommandation}
```

## 4. Demander l'action utilisateur

```
Que souhaites-tu faire ?

1. 🔧 Fix now - Corriger toutes les issues maintenant
2. 📋 Fix later - Noter pour plus tard et continuer
3. ✅ Proceed - Continuer sans corrections (non recommandé)
```

⚠️ **Attendre la décision avant de continuer.**

## 5. Si "Fix now" choisi

- Appliquer les corrections PHPStan en priorité (bloquent la CI)
- Appliquer les corrections Elegant Objects
- Relancer une review pour vérifier

## 6. Mettre à jour le workflow state

```json
{
  "currentPhase": 6,
  "phases": {
    "6": {
      "status": "completed",
      "completedAt": "{timestamp}",
      "results": {
        "codeReview": {"issues": {nombre}, "fixed": {nombre}},
        "phpstan": {"errors": {nombre}, "fixed": {nombre}},
        "elegantObjects": {"score": {X}, "violations": {nombre}}
      },
      "decision": "{fix_now|fix_later|proceed}"
    }
  }
}
```

# Prochaine étape

```
✅ Review complétée

Résumé :
- Code review : {X} issues ({Y} corrigées)
- PHPStan : {X} erreurs ({Y} corrigées)
- Elegant Objects : {score}/100

Prochaine étape : /dev:summary pour le résumé final
```

# Règles

- **PHPStan erreurs = BLOQUANT** (font échouer la CI)
- Confiance minimum 80% pour les issues code review
- Respecter le choix utilisateur (ne pas forcer les corrections)
