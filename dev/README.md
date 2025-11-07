# Plugin Dev

Toolkit complet de développement pour PHP avec commandes Git, debugging, documentation, et QA automatisée.

## Installation

```bash
/plugin install dev@atournayre
```

## Commandes

### `/dev:prepare`

Crée un plan d'implémentation concis basé sur les besoins utilisateur et le sauvegarde dans `specs/`.

**Usage :**
```bash
/dev:prepare
```

**Génère :**
- Plan structuré avec étapes d'implémentation
- Fichier sauvegardé dans `specs/`
- Prêt pour `/dev:code`

---

### `/dev:code`

Code la codebase en suivant le plan d'implémentation.

**Arguments :**
```bash
/dev:code [path-to-plan]
```

**Exemples :**
```bash
/dev:code specs/feature-auth.md
```

**Workflow :**
- Lit le plan depuis `specs/`
- Implémente chaque étape
- Crée tests unitaires
- Valide la conformité

---

### `/dev:docker`

Exécute les actions définies via Docker.

**Usage :**
```bash
/dev:docker [action]
```

**Cas d'usage :**
- Lancer services Docker
- Exécuter commandes dans conteneurs
- Build d'images
- Gestion environnements

---

### `/dev:question`

Répond aux questions sur la structure du projet et la documentation sans coder.

**Usage :**
```bash
/dev:question [ta-question]
```

**Exemples :**
```bash
/dev:question "Comment fonctionne l'authentification ?"
/dev:question "Où sont les tests ?"
```

---

### `/dev:context:load`

Charge un preset de contexte pour la session.

**Arguments :**
```bash
/dev:context:load <preset>
```

**Presets disponibles :**
- `php` - Contexte PHP/Symfony
- `frontend` - Contexte JS/CSS
- `docker` - Contexte containers
- `api` - Contexte API Platform

**Exemple :**
```bash
/dev:context:load php
```

**Fonctionnalités :**
- Charge fichiers de contexte pertinents
- Configure outils appropriés
- Définit conventions de code

---

### `/dev:debug:error`

Analyse et résout une erreur (message simple ou stack trace).

**Arguments :**
```bash
/dev:debug:error <message-erreur-ou-fichier-log>
```

**Exemples :**
```bash
# Avec message d'erreur direct
/dev:debug:error "Call to undefined method User::getName()"

# Avec fichier de log
/dev:debug:error var/log/dev.log
```

**Workflow :**
- Parse l'erreur ou le stack trace
- Identifie la cause racine
- Localise le code problématique
- Propose correction
- Vérifie avec tests

**Rapport :**
```
🐛 Analyse d'erreur

Erreur : Call to undefined method
Fichier : src/Entity/User.php:42
Cause : Méthode getName() manquante

Correction proposée :
[code fix]

Tests : [tests ajoutés]
```

## Agents Spécialisés

Le plugin Dev inclut des agents spécialisés pour des tâches complexes :

### `phpstan-error-resolver`

Résout automatiquement les erreurs PHPStan niveau 9.

**Spécialités :**
- Types stricts
- Annotations generics
- Array shapes
- Collections Doctrine

### `elegant-objects-reviewer`

Examine le code PHP pour conformité Elegant Objects.

**Vérifie :**
- Constructeurs uniquement avec affectations
- Pas d'héritage d'implémentation
- Objets immuables
- Méthodes sans `null`
- Classes `final`

## Structure

```
dev/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── prepare.md
│   ├── code.md
│   ├── docker.md
│   ├── question.md
│   ├── context/
│   │   └── load.md
│   └── debug/
│       └── error.md
└── agents/
    ├── phpstan-error-resolver.md
    └── elegant-objects-reviewer.md
```

## Workflow Recommandé

1. **Planification** : `/dev:prepare`
2. **Implémentation** : `/dev:code specs/plan.md`
3. **Debug si erreur** : `/dev:debug:error`
4. **Questions** : `/dev:question`

## Licence

MIT
