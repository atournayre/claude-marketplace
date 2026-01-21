# Skill : prompt:feature

Génère un prompt pour une nouvelle feature métier basé sur les patterns DDD/CQRS.

## Usage

```bash
/prompt:feature <EntityName> <feature-name> [--bounded-context=<context>] [--duration=<hours>]
```

## Arguments

| Argument | Type | Requis | Description | Exemple |
|----------|------|--------|-------------|---------|
| `EntityName` | string | Oui* | Nom de l'entité (PascalCase) | `DeclarationDeBug` |
| `feature-name` | string | Oui* | Nom de la feature (kebab-case) | `declaration-bug` |
| `--bounded-context` | flag | Oui* | Bounded context DDD | `--bounded-context=Support` |
| `--duration` | flag | Non | Estimation en heures | `--duration=8` |
| `--interactive` | flag | Non | Mode interactif (demande tout) | `--interactive` |

*Si omis, Claude demandera interactivement via AskUserQuestion

## Exemples

### Exemple Complet

```bash
/prompt:feature DeclarationDeBug declaration-bug --bounded-context=Support --duration=8
```

Génère : `.claude/prompts/feature-declaration-bug-{timestamp}.md`

### Mode Interactif

```bash
/prompt:feature --interactive
```

Claude posera des questions pour collecter :
- Entity name
- Feature name
- Bounded context
- Duration (optionnel)

### Partiellement Renseigné

```bash
/prompt:feature Utilisateur utilisateur
```

Claude demandera uniquement le `bounded-context` manquant.

## Variables Substituées

Le template `feature.md` utilise ces variables :

**Automatiques** (détectées depuis le projet) :
- `{PROJECT_NAME}` - Nom du projet (composer.json)
- `{NAMESPACE}` - Namespace racine (composer.json)
- `{AUTHOR}` - Nom de l'auteur (git config)
- `{DATE}` - Date actuelle

**Interactives** (demandées ou passées en arguments) :
- `{ENTITY_NAME}` - Nom de l'entité
- `{FEATURE_NAME}` - Nom de la feature
- `{BOUNDED_CONTEXT}` - Bounded context DDD
- `{DURATION}` - Estimation en heures

## Prompt Généré

Le prompt généré contiendra :

1. **Objectif** - Description de la feature
2. **Architecture DDD** - Entity, Repository, Collection, Value Objects
3. **Architecture CQRS** - Commands, Queries, Handlers
4. **Plan d'Implémentation** - 4 phases détaillées :
   - Phase 1 : Domaine (Entity + Repository)
   - Phase 2 : Application (CQRS)
   - Phase 3 : Tests (Foundry + PHPUnit)
   - Phase 4 : Intégration (Services + Messenger)
5. **Vérification** - Tests automatisés et manuels
6. **Points d'Attention** - Standards qualité, risques, patterns

## Standards Inclus

Le prompt généré applique automatiquement :
- PHPStan niveau 9
- Elegant Objects (final readonly, factory statique)
- PSR-12
- Conditions Yoda
- TDD
- Pattern AAA (Arrange-Act-Assert)

## Fichier Généré

**Emplacement** : `.claude/prompts/feature-{feature-name}-{timestamp}.md`

**Timestamp** : Format YYYYMMDD-HHMMSS

Exemple : `.claude/prompts/feature-declaration-bug-20260121-143022.md`

## Validation

Le prompt généré est automatiquement validé :
- ✅ Toutes les variables `{...}` substituées
- ✅ Sections requises présentes (Objectif, Architecture, Plan, Vérification)
- ✅ Longueur raisonnable (< 2000 lignes)

## Erreurs Possibles

| Erreur | Cause | Solution |
|--------|-------|----------|
| `composer.json introuvable` | Pas dans un projet PHP | Exécuter depuis la racine du projet |
| `Template introuvable` | Plugin mal installé | Vérifier installation du plugin prompt |
| `Variables non substituées` | Bug dans substitution | Vérifier que toutes les variables sont fournies |
| `Permission denied` | Pas de droits d'écriture | `chmod +w .claude/prompts/` |

## Prochaines Étapes

Après génération du prompt :

1. **Lire** le prompt généré
2. **Copier** le contenu dans une nouvelle conversation Claude
3. **Implémenter** en suivant les phases du plan
4. **Vérifier** avec les checklists qualité
