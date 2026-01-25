# Tâche : {TASK_NAME}

**Projet** : {PROJECT_NAME}
**Date** : {DATE}
**Auteur** : {AUTHOR}

## Objectif

[Décrire l'objectif de la tâche en 2-3 phrases]

### Besoin

[Expliquer le besoin métier ou technique]

### Scope

**Inclus** :
- [Ce qui est dans le scope]

**Exclus** :
- [Ce qui n'est pas dans le scope]

## Architecture

### Approche Proposée

[Décrire l'approche technique choisie]

### Composants

```
[Diagramme ou structure des composants]
```

### Patterns Utilisés

- [Pattern 1 : Description]
- [Pattern 2 : Description]

## Plan d'Implémentation

### Phase 1 : [Nom de la Phase]

#### 1.1 [Étape]

**Fichier** : `[chemin/vers/fichier]`

[Description de ce qu'il faut faire]

```php
// Exemple de code si applicable
```

#### 1.2 [Étape]

**Fichier** : `[chemin/vers/fichier]`

[Description]

### Phase 2 : [Nom de la Phase]

#### 2.1 [Étape]

[Description]

### Phase 3 : Tests

#### 3.1 Tests Unitaires

**Fichier** : `tests/[Path]/[Nom]Test.php`

[Description des tests à créer]

#### 3.2 Tests d'Intégration

[Si applicable]

### Phase 4 : Documentation

#### 4.1 Mettre à Jour README

[Sections à ajouter/modifier]

#### 4.2 Docblocks

[Standards de documentation]

## Vérification

### Tests Automatisés

```bash
# PHPStan
make phpstan

# Tests unitaires
make test

# Coverage
make coverage
```

### Tests Manuels

1. [Étape 1]
2. [Étape 2]
3. [Étape 3]

### Checklist Qualité

- [ ] [Critère de qualité 1]
- [ ] [Critère de qualité 2]
- [ ] PHPStan niveau 9 : 0 erreur
- [ ] Tests unitaires ≥ 80% coverage
- [ ] PSR-12 respecté
- [ ] Documentation mise à jour
- [ ] [Critère spécifique au projet]

## Points d'Attention

### Standards Qualité

- **PHPStan** : Niveau 9 obligatoire
- **Elegant Objects** : Classes final readonly, pas de setters
- **PSR-12** : Code style
- **TDD** : Tests avant implémentation
- **[Standard spécifique]** : [Description]

### Risques Identifiés

| Risque | Mitigation |
|--------|-----------|
| [Risque 1] | [Comment mitiger] |
| [Risque 2] | [Comment mitiger] |
| [Risque 3] | [Comment mitiger] |

### Patterns à Éviter

- ❌ [Anti-pattern 1]
- ❌ [Anti-pattern 2]
- ❌ [Anti-pattern 3]

### Patterns Recommandés

- ✅ [Pattern recommandé 1]
- ✅ [Pattern recommandé 2]
- ✅ [Pattern recommandé 3]

## Dépendances

### Packages Composer

```bash
# Si nécessaire
composer require [package]
```

### Services Externes

- [Service 1 : Description]
- [Service 2 : Description]

## Métriques de Succès

### Avant

- [Métrique 1 : Valeur actuelle]
- [Métrique 2 : Valeur actuelle]

### Après (Objectifs)

- [Métrique 1 : Valeur cible]
- [Métrique 2 : Valeur cible]

### Validation

```bash
# Comment mesurer le succès
[Commandes ou procédure]
```

## Fichiers Créés

- `[chemin/fichier1]`
- `[chemin/fichier2]`
- `[chemin/fichier3]`

## Fichiers Modifiés

- `[chemin/fichier1]`
- `[chemin/fichier2]`

## Documentation

### ADR (Architecture Decision Record)

Si décision architecturale majeure, créer un ADR :

**Fichier** : `docs/adr/YYYY-MM-DD-{TASK_NAME}.md`

[Lien vers template ADR ou contenu minimal]

### README

Ajouter section dans README.md si fonctionnalité visible par utilisateurs.

## Monitoring et Observabilité

### Logs

- [Événements à logger]
- [Niveau de log approprié]

### Métriques

- [Métriques à collecter]
- [Dashboards à créer]

### Alertes

- [Conditions d'alerte]
- [Seuils critiques]

## Rollback Plan

### Si Problème en Production

1. [Étape de rollback 1]
2. [Étape de rollback 2]
3. [Étape de rollback 3]

### Feature Flag (si applicable)

- Variable env pour désactiver rapidement
- Fallback vers comportement stable

## Timeline et Jalons

### Étapes Clés

1. **Phase 1 complète** : [Livrables]
2. **Phase 2 complète** : [Livrables]
3. **Tests validés** : [Critères]
4. **Déploiement prod** : [Date ou conditions]

### Prochaines Étapes (Post-v1)

- [Amélioration future 1]
- [Amélioration future 2]
- [Optimisation prévue]

## Ressources

### Documentation

- [Lien vers doc framework]
- [Lien vers RFC ou spécification]
- [Lien vers issue GitHub]

### Références

- [Article technique pertinent]
- [Exemple d'implémentation similaire]
- [Pattern catalog]
