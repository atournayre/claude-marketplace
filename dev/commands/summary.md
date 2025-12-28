---
description: Résumé de ce qui a été construit (Phase 7)
model: claude-haiku-4-5-20251001
allowed-tools: Read, Glob
output-style: ultra-concise
---

# Configuration de sortie

**IMPORTANT** : Cette commande génère un résumé concis et nécessite un format de sortie spécifique.

Lis le frontmatter de cette commande. Si un champ `output-style` est présent, exécute immédiatement :
```
/output-style <valeur-du-champ>
```

*Note : Une fois que le champ `output-style` sera supporté nativement par Claude Code, cette instruction pourra être supprimée.*

# Objectif

Phase 7 du workflow de développement : documenter ce qui a été accompli et suggérer les prochaines étapes.

# Instructions

## 1. Lire le contexte

- Lire `.claude/data/.dev-workflow-state.json` pour récupérer toutes les informations du workflow
- Lister tous les fichiers créés/modifiés

## 2. Générer le résumé

```
🎉 Feature complétée : {Feature Name}

---

## Ce qui a été construit

{Description courte de la feature}

### Composants créés
- `{fichier}` : {description}
- `{fichier}` : {description}

### Fichiers modifiés
- `{fichier}` : {description des changements}

---

## Décisions clés

| Décision | Choix | Raison |
|----------|-------|--------|
| Architecture | {approche} | {raison} |
| {autre} | {choix} | {raison} |

---

## Résultats qualité

- **PHPStan** : ✅ 0 erreurs
- **Elegant Objects** : {score}/100
- **Code Review** : {X} issues corrigées

---

## ⏱️ Temps de développement

| Phase | Durée |
|-------|-------|
| 0. Discover | {duration} |
| 1. Explore | {duration} |
| 2. Clarify | {duration} |
| 3. Design | {duration} |
| 4. Plan | {duration} |
| 5. Code | {duration} |
| 6. Review | {duration} |
| 7. Summary | {duration} |
| **Total** | **{total_duration}** |

---

## Prochaines étapes suggérées

1. [ ] {suggestion 1}
2. [ ] {suggestion 2}
3. [ ] {suggestion 3}

---

## Commandes utiles

```bash
# Tester la feature
make run-unit-php

# Vérifier la qualité
make before-pr-back

# Créer un commit
/git:commit
```
```

## Format de durée

Formater les durées de manière lisible :
- `< 60s` → `{X}s` (ex: `45s`)
- `< 60min` → `{X}m {Y}s` (ex: `2m 30s`)
- `>= 60min` → `{X}h {Y}m` (ex: `1h 15m`)

## 3. Nettoyer le workflow state

Marquer le workflow comme terminé :

```json
{
  "status": "completed",
  "completedAt": "{ISO timestamp}",
  "currentPhase": 7,
  "timing": {
    "totalDurationMs": {somme de tous les durationMs des phases}
  }
}
```

## 4. Proposer les actions suivantes

```
📋 Et maintenant ?

- /git:commit - Commiter les changements
- /git:pr - Créer une Pull Request
- /dev:feature <nouvelle-feature> - Démarrer une nouvelle feature

Merci d'avoir utilisé le workflow de développement !
```

# Règles

- Être **concis** mais **complet**
- Mettre en avant les **décisions importantes**
- Toujours suggérer des **prochaines étapes**
- Ne pas oublier de **marquer les todos comme complétés**
