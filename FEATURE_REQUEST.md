# Feature Request: Support natif du champ `output-style` dans le frontmatter des slash commands

## Contexte

Actuellement, Claude Code permet de définir des output-styles personnalisés dans `~/.claude/output-styles/` et de basculer entre eux avec `/output-style <nom>`. Cependant, il n'existe aucun mécanisme pour qu'une slash command spécifie automatiquement quel output-style elle souhaite utiliser.

## Problème

Certaines commandes génèrent des types de contenu très spécifiques qui nécessitent un formatage particulier :
- **Rapports HTML** : nécessitent `html-structured`
- **Documentation markdown** : nécessitent `markdown-focused`
- **Analyses d'impact** : nécessitent `bullet-points`
- **Comparaisons d'architectures** : nécessitent `table-based`
- **Statuts courts** : nécessitent `ultra-concise`

Aujourd'hui, l'utilisateur doit :
1. Se rappeler quel output-style utiliser pour quelle commande
2. Exécuter manuellement `/output-style <nom>` avant la commande
3. Risquer d'obtenir un résultat mal formaté s'il oublie cette étape

## Solution proposée

Ajouter le support d'un nouveau champ `output-style` dans le frontmatter YAML des slash commands.

### Exemple d'utilisation

```yaml
---
description: Génère un rapport HTML d'analyse d'impact
output-style: html-structured
arguments:
  - name: branch-source
    required: true
---
```

### Comportement attendu

Lorsqu'une slash command est invoquée :

1. Claude Code lit le frontmatter
2. Si le champ `output-style` est présent et valide :
   - Basculer automatiquement vers cet output-style
   - Exécuter la commande avec ce style actif
3. Si le champ est absent ou invalide :
   - Utiliser l'output-style actuel (comportement actuel)
   - Aucun changement par rapport au comportement existant

### Validation

- Le champ `output-style` est **optionnel**
- La valeur doit correspondre à un fichier existant dans `~/.claude/output-styles/`
- Si la valeur est invalide, afficher un warning et continuer avec le style actuel

## Bénéfices

### Pour les utilisateurs

- **Expérience améliorée** : Pas besoin de se rappeler quel style utiliser
- **Cohérence** : Chaque commande génère toujours le même format de sortie
- **Simplicité** : Une seule commande au lieu de deux (`/output-style` + `/command`)

### Pour les développeurs de commandes

- **Intentions claires** : Le frontmatter documente le format de sortie attendu
- **Prédictibilité** : Le comportement est déterministe
- **Maintenabilité** : Pas besoin d'instructions complexes dans le contenu de la commande

### Pour l'écosystème

- **Workflows automatisés** : Les commandes peuvent être chaînées sans intervention manuelle
- **Plugin marketplace** : Les plugins peuvent définir leurs propres conventions de sortie
- **Compatibilité** : Forward-compatible (les commandes existantes continuent de fonctionner)

## Use Cases concrets

### 1. Rapport HTML d'analyse de release

**Commande** : `/git:release-report`

```yaml
---
output-style: html-structured
---
```

**Avant** :
```bash
/output-style html-structured
/git:release-report release/v1.0.0 main
```

**Après** :
```bash
/git:release-report release/v1.0.0 main
# Bascule automatiquement vers html-structured
```

### 2. Documentation ADR

**Commande** : `/doc:adr`

```yaml
---
output-style: markdown-focused
---
```

**Avant** :
```bash
/output-style markdown-focused
/doc:adr "Adopter PostgreSQL"
```

**Après** :
```bash
/doc:adr "Adopter PostgreSQL"
# Génère automatiquement du markdown structuré
```

### 3. Statut de workflow

**Commande** : `/dev:status`

```yaml
---
output-style: ultra-concise
---
```

**Avant** :
```bash
/output-style ultra-concise
/dev:status
```

**Après** :
```bash
/dev:status
# Affiche un résumé court automatiquement
```

## Implémentation suggérée

### 1. Parser le frontmatter

```typescript
interface CommandFrontmatter {
  description?: string;
  'argument-hint'?: string;
  'allowed-tools'?: string | string[];
  model?: string;
  'output-style'?: string; // NOUVEAU CHAMP
  arguments?: CommandArgument[];
}
```

### 2. Appliquer l'output-style avant l'exécution

```typescript
async function executeCommand(command: Command) {
  const frontmatter = parseCommandFrontmatter(command);

  if (frontmatter['output-style']) {
    const stylePath = resolveOutputStyle(frontmatter['output-style']);

    if (stylePath && fileExists(stylePath)) {
      await applyOutputStyle(frontmatter['output-style']);
    } else {
      console.warn(`Output style "${frontmatter['output-style']}" not found. Using current style.`);
    }
  }

  // Exécuter la commande normalement
  await runCommand(command);
}
```

### 3. Fonction de résolution

```typescript
function resolveOutputStyle(styleName: string): string | null {
  const paths = [
    `~/.claude/output-styles/${styleName}.md`,
    `./.claude/output-styles/${styleName}.md`,
  ];

  for (const path of paths) {
    if (fileExists(expandPath(path))) {
      return path;
    }
  }

  return null;
}
```

## Rétrocompatibilité

Cette fonctionnalité est **100% rétrocompatible** :

- ✅ Les commandes existantes sans `output-style` fonctionnent comme avant
- ✅ Aucun changement de comportement par défaut
- ✅ Aucune migration nécessaire
- ✅ Les utilisateurs peuvent adopter progressivement

## Workaround actuel

En attendant le support natif, nous utilisons une instruction dans le contenu de chaque commande :

```markdown
# Configuration de sortie

**IMPORTANT** : Cette commande nécessite un format de sortie spécifique.

Lis le frontmatter de cette commande. Si un champ `output-style` est présent, exécute immédiatement :
```
/output-style <valeur-du-champ>
```

*Note : Une fois que le champ `output-style` sera supporté nativement par Claude Code, cette instruction pourra être supprimée.*
```

**Limites du workaround** :
- Dépend de l'interprétation de Claude (pas garanti à 100%)
- Ajoute du boilerplate dans chaque commande
- Pas de validation automatique
- Nécessite une instruction explicite

## Commandes du marketplace utilisant cette feature

Nous avons identifié **14 commandes** dans le marketplace qui bénéficieraient immédiatement de cette fonctionnalité :

### HTML structuré (1 commande)
- `git/commands/release-report.md`

### Markdown focusé (4 commandes)
- `doc/commands/adr.md`
- `marketing/commands/linkedin.md`
- `doc/commands/rtfm.md`

### Ultra concis (3 commandes)
- `dev/commands/status.md`
- `dev/commands/summary.md`
- `git/commands/branch.md`

### Bullet points (4 commandes)
- `dev/commands/explore.md`
- `dev/commands/discover.md`
- `gemini/commands/analyze.md`
- `github/commands/impact.md`

### Table-based (2 commandes)
- `dev/commands/design.md`
- `dev/commands/clarify.md`

## Références

- [Output styles - Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code/output-styles)
- [Slash commands - Claude Code Docs](https://code.claude.com/docs/en/slash-commands)
- [Claude Code Marketplace](https://github.com/atournayre/claude-marketplace)

## Prochaines étapes

1. ✅ Implémenter le champ dans les commandes du marketplace (avec workaround)
2. ⏳ Soumettre cette feature request à l'équipe Claude Code
3. ⏳ Si accepté : Supprimer les instructions de workaround
4. ⏳ Documenter la convention dans le guide des plugins

## Contact

Pour toute question ou discussion sur cette proposition :
- **Repository** : https://github.com/atournayre/claude-marketplace
- **Author** : @atournayre

---

**Date de création** : 2025-12-20
**Version du document** : 1.0
