---
name: infra:alias-add
description: Crée un alias de slash command qui délègue à une autre slash command existante. Valide les arguments, crée le fichier d'alias, et met à jour la documentation.
allowed-tools: [Skill, Write, Read, Glob]
argument-hint: <alias> <commande>
model: sonnet
version: 1.0.0
license: MIT
---

# infra:alias-add

Créer un alias de slash command délégant à une commande existante.

## Instructions à Exécuter

### 1. Validation des arguments

- Vérifier que 2 arguments ont été fournis (alias et commande cible)
- Valider le format de l'alias (format kebab-case)
- Valider le format de la commande cible
- Vérifier que l'alias n'existe pas déjà
- Vérifier que la commande cible existe

### 2. Création du fichier d'alias

Créer dans le répertoire des skills/commands approprié :

```markdown
---
allowed-tools:
  - Skill
description: Alias vers [TARGET_COMMAND]
argument-hint: [arguments de la commande cible]
model: haiku
---

# [ALIAS]

Alias vers `[TARGET_COMMAND]`.

## Workflow
- Exécuter la commande cible via Skill
```

### 3. Exécution de la commande cible

Utiliser l'outil Skill pour exécuter TARGET_COMMAND avec les arguments fournis.

### 4. Mise à jour de la documentation

Ajouter l'alias dans la documentation avec :
- Nom de l'alias
- Description
- Commande cible
- Usage

### 5. Rapport final

```
Alias créé avec succès

Fichier : {chemin}
Cible : {TARGET_COMMAND}
Usage : /{alias} [arguments]
```

## Bonnes pratiques

- Noms d'alias courts et mémorisables
- Éviter les conflits avec les commandes existantes
- Documenter clairement la commande cible
- Utiliser Haiku pour les alias (simple délégation)
- Transmettre tous les arguments à la commande cible

## Exemples

```bash
/infra:alias-add status /git:status
/infra:alias-add doc /doc:update
```
