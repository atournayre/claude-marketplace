---
model: claude-opus-4-1-20250805
allowed-tools: Read, Write, Edit, Bash
argument-hint: [titre]
description: Génère un Architecture Decision Record (ADR) formaté et structuré
---

# Génération d'ADR

## Purpose
Génère un Architecture Decision Record (ADR) complet et structuré pour documenter les décisions architecturales importantes du projet.

## Timing

### Début d'Exécution
**OBLIGATOIRE - PREMIÈRE ACTION** :
1. Exécuter `date` pour obtenir l'heure réelle
2. Afficher immédiatement : 🕐 **Démarrage** : [Résultat de la commande date]
3. Stocker le timestamp pour le calcul de durée

### Fin d'Exécution
**OBLIGATOIRE - DERNIÈRE ACTION** :
1. Exécuter `date` à nouveau pour obtenir l'heure de fin
2. Calculer la durée réelle entre début et fin
3. Afficher :
   - ✅ **Terminé** : [Résultat de la commande date]
   - ⏱️ **Durée** : [Durée calculée au format lisible]

### Formats
- Date : résultat brut de la commande `date` (incluant CEST/CET automatiquement)
- Durée :
  - Moins d'1 minute : `XXs` (ex: 45s)
  - Moins d'1 heure : `XXm XXs` (ex: 2m 30s)
  - Plus d'1 heure : `XXh XXm XXs` (ex: 1h 15m 30s)

### Instructions CRITIQUES
- TOUJOURS exécuter `date` via Bash - JAMAIS inventer/halluciner l'heure
- Le timestamp de début DOIT être obtenu en exécutant `date` immédiatement
- Le timestamp de fin DOIT être obtenu en exécutant `date` à la fin
- Calculer la durée en soustrayant les timestamps unix (utiliser `date +%s`)
- NE JAMAIS supposer ou deviner l'heure

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

### Étape 0: Initialisation du Timing (OBLIGATOIRE - PREMIÈRE ACTION)
```
🕐 Démarrage: [timestamp Europe/Paris avec CEST/CET]
```
- Cette étape DOIT être la toute première action
- Enregistrer le timestamp pour calcul ultérieur

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
/adr "Adoption du framework Symfony pour l'API"

# Génération d'un ADR pour une décision de base de données
/adr "Migration vers PostgreSQL pour les performances"
```

## Report
- Affiche le numéro ADR généré
- Confirme la création du fichier dans `docs/adr/`
- Liste les fichiers ADR existants pour référence
- Rappelle les prochaines étapes (review, validation)

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]
