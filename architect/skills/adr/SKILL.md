---
name: architect:adr
description: Génère un Architecture Decision Record (ADR) formaté et structuré
model: sonnet
allowed-tools: [TaskCreate, TaskUpdate, TaskList, Read, Write, Edit, Bash]
argument-hint: [titre]
version: 1.0.0
license: MIT
---

# Génération d'ADR

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

## Purpose

Génère un Architecture Decision Record (ADR) complet et structuré pour documenter les décisions architecturales importantes du projet.

## Variables
- **DECISION_TITLE**: Le titre de la décision architecturale (`$ARGUMENTS`)
- **DECISION_NUMBER**: Le numéro séquentiel de l'ADR (auto-généré)

## Instructions

- Si `TITRE` n'est pas fourni, ARRETER immédiatement et demander à l'utilisateur de le fournir.
- Créer un ADR suivant le format standard RFC
- Utiliser la numérotation séquentielle automatique
- Intégrer le contexte du projet actuel
- Respecter les conventions de documentation du projet

## Fichiers pertinents
- `docs/adr/` - Dossier contenant les ADR existants
- `docs/adr/README.md` - Liste des ADR existants
- `docs/README.md` - Contexte général du projet
- `CLAUDE.md` - Conventions et préférences

## Structure des ADR

```
docs/
  adr/
    0001-use-php-for-backend.md
    0002-implement-elegant-objects.md
    README.md
```

## Workflow

1. Analyser les ADR existants pour déterminer le prochain numéro
2. Examiner le projet pour comprendre le contexte architectural
3. Créer un nouveau fichier ADR avec la numérotation appropriée
4. Utiliser le template standardisé avec les sections requises
5. Valider la cohérence avec les décisions précédentes

## Template

```markdown
# ADR-XXXX: [Titre de la décision]

## Statut
- **Statut**: [Proposé | Accepté | Rejeté | Déprécié | Remplacé par ADR-YYYY]
- **Date**: YYYY-MM-DD
- **Auteurs**: [Noms]
- **Reviewers**: [Noms]

## Contexte
[Description du problème ou de la situation qui nécessite une décision]

## Décision
[La décision prise et sa justification]

## Conséquences
### Positives
- [Bénéfices attendus]

### Négatives
- [Coûts et risques identifiés]

### Neutres
- [Autres implications]

## Alternatives considérées
### Option 1: [Nom]
- **Avantages**: [Liste]
- **Inconvénients**: [Liste]
- **Raison du rejet**: [Explication]

### Option 2: [Nom]
- **Avantages**: [Liste]
- **Inconvénients**: [Liste]
- **Raison du rejet**: [Explication]

## Références
- [Liens vers documentation, discussions, tickets]

## Notes d'implémentation
[Détails techniques spécifiques pour l'implémentation]
```

## Exemples

```bash
# ADR pour l'adoption d'un framework
/architect:adr "Adoption du framework Symfony pour l'API"

# ADR pour une décision de base de données
/architect:adr "Migration vers PostgreSQL pour les performances"
```

## Résultat

```markdown
## ADR créé

- Fichier : `docs/adr/{XXXX}-{slug}.md`
- Numéro : ADR-{XXXX}
- Statut initial : Proposé

### ADR existants
- ADR-0001 : [titre]
- ADR-0002 : [titre]

### Prochaines étapes
- Partager l'ADR avec l'équipe pour review
- Mettre à jour le statut : Accepté / Rejeté
- Mettre à jour `docs/adr/README.md`
```
