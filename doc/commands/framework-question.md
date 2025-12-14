---
allowed-tools: [Read, Grep, Glob, Bash]
description: Interroger la documentation locale d'un framework pour répondre à une question
argument-hint: <framework-name> [version] <question>
model: claude-haiku-4-5-20251001
---

# Interrogation Documentation Framework

Répondre à une question technique sur un framework en utilisant sa documentation locale.

{{_templates/timing.md}}

## Frameworks Supportés

- `symfony`
- `api-platform`
- `meilisearch`
- `atournayre-framework`

## Variables

- FRAMEWORK: Nom du framework (1er argument)
- VERSION: Version optionnelle (2ème argument si fourni)
- QUESTION: Question technique (dernier argument)
- DOCS_PATH: `docs/${FRAMEWORK}/${VERSION}/` (ou `docs/${FRAMEWORK}/` si pas de version)

## Parsing Arguments

Détecter automatiquement si VERSION fournie :
- 2 args : `<framework> <question>` → pas de version
- 3+ args : `<framework> <version> <question>` → version fournie
- Si 2ème arg ressemble version (chiffres+points) : VERSION
- Sinon : partie de QUESTION

## Validation

Si FRAMEWORK non supporté ou QUESTION vide :
- Afficher usage correct
- Arrêter l'exécution

## Workflow

### Étape 1: Vérification documentation
- Parser arguments (framework, version opt, question)
- Construire DOCS_PATH selon présence version
- Vérifier existence de `DOCS_PATH`
- Si absent : suggérer `/doc:framework:load ${FRAMEWORK} [${VERSION}]`
- Si version absente mais multiples versions existent : lister versions disponibles

### Étape 2: Analyse question
- Extraire mots-clés de QUESTION
- Identifier contexte technique

### Étape 3: Recherche
- Grep avec mots-clés dans DOCS_PATH
- Paramètres : `-i -C 3`
- Lire fichiers pertinents

### Étape 4: Synthèse
- Extraire sections pertinentes
- Organiser par pertinence
- Identifier : concept, exemples, bonnes pratiques

### Étape 5: Réponse

```markdown
## 📚 Réponse : [Sujet] ([Framework] [version])

### Concept
- Explication
- Points clés

### Exemple Code
[Si disponible]

### Documentation Référence
- 📄 `docs/${FRAMEWORK}/[version]/[fichier].md`

### Voir Aussi
- Concepts connexes
```

## Gestion Erreurs

- **Doc manquante** : Suggérer `/doc:framework:load ${FRAMEWORK} [version]`
- **Versions multiples** : Lister versions + demander précision
- **Aucun résultat** : Termes alternatifs
- **Question vague** : Demander précisions

## Exemples

```bash
# Sans version (cherche dans toutes versions ou latest)
/doc:framework:question symfony "Comment créer un controller ?"
/doc:framework:question api-platform "Configurer sérialisation"

# Avec version spécifique
/doc:framework:question symfony 6.4 "Comment créer un controller ?"
/doc:framework:question api-platform 3.2 "Configurer sérialisation"
/doc:framework:question meilisearch 1.5 "Ajouter des filtres"
```
