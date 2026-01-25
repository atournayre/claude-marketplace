---
name: doc:adr
description: Génère un Architecture Decision Record (ADR) formaté et structuré
model: claude-sonnet-4-5-20250929
allowed-tools: [TaskCreate, TaskUpdate, TaskList, Read, Write, Edit, Bash]
argument-hint: [titre]
version: 1.0.0
license: MIT
---

# Configuration de sortie

**IMPORTANT** : Cette skill génère de la documentation structurée et nécessite un format de sortie spécifique.

Lis le frontmatter de cette skill. Si un champ `output-style` est présent, exécute immédiatement :
```
/output-style <valeur-du-champ>
```

*Note : Une fois que le champ `output-style` sera supporté nativement par Claude Code, cette instruction pourra être supprimée.*

**Output-style requis** : `markdown-focused`

# Génération d'ADR

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

## Purpose
Génère un Architecture Decision Record (ADR) complet et structuré pour documenter les décisions architecturales importantes du projet.

## Variables
- **DECISION_TITLE**: Le titre de la décision architecturale
- **DECISION_NUMBER**: Le numéro séquentiel de l'ADR (auto-généré si non fourni)

## Instructions
- Si `TITRE` n'est pas fourni, ARRETER immediatement et demander à l'utilisateur de le fournir.
- Crée un ADR suivant le format standard RFC
- Utilise la numérotation séquentielle automatique
- Intègre le contexte du projet actuel
- Respecte les conventions de documentation du projet

## Relevant Files
- `docs/adr/` - Dossier contenant les ADR existants
- `docs/adr/README.md` - Liste des ADR existants
- `docs/README.md` - Contexte général du projet
- `CLAUDE.md` - Conventions et préférences

## Codebase Structure
```
docs/
  adr/
    0001-use-php-for-backend.md
    0002-implement-elegant-objects.md
    README.md
```

## Workflow

- Analyse les ADR existants pour déterminer le prochain numéro
- Examine le projet pour comprendre le contexte architectural
- Crée un nouveau fichier ADR avec la numérotation appropriée
- Utilise le template standardisé avec les sections requises
- Valide la cohérence avec les décisions précédentes

## Expertise
- Architecture logicielle et patterns de conception
- Documentation technique et ADR standards
- Conventions de nommage et organisation des documents
- Principles DDD et Elegant Objects (selon le contexte du projet)

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

## Examples
```bash
# Génération d'un ADR pour l'adoption d'un nouveau framework

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**
/adr "Adoption du framework Symfony pour l'API"

# Génération d'un ADR pour une décision de base de données

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**
/adr "Migration vers PostgreSQL pour les performances"
```

## Report
- Affiche le numéro ADR généré
- Confirme la création du fichier dans `docs/adr/`
- Liste les fichiers ADR existants pour référence
- Rappelle les prochaines étapes (review, validation)
