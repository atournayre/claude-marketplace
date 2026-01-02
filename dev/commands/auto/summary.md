---
description: Résumé de ce qui a été construit - Mode AUTO (Phase 8)
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

Phase 8 du workflow automatisé : documenter ce qui a été accompli et préparer la PR.

Pas de checkpoint, exécution automatique.

# Instructions

## 1. Lire le contexte

Déterminer le chemin du workflow state :

```bash
# Récupérer issue_number depuis le contexte
workflow_state_file=".claude/data/workflows/issue-${issue_number}-dev-workflow-state.json"
```

- Lire le workflow state pour récupérer toutes les informations du workflow
- Lister tous les fichiers créés/modifiés

## 2. Générer le résumé

```
🎉 Feature développée automatiquement : {Feature Name}

---

## Ce qui a été construit

{Description courte de la feature}

### Composants créés
- `{fichier}` : {description}
- `{fichier}` : {description}

### Fichiers modifiés
- `{fichier}` : {description des changements}

---

## Décisions appliquées

| Catégorie | Décision |
|-----------|----------|
| Architecture | Pragmatic Balance |
| Edge cases | Exception métier InvalideXXX |
| Gestion erreurs | Exceptions typées + logging PSR-3 |
| Intégration | Patterns existants réutilisés |
| Rétrocompatibilité | API publique préservée |

---

## Résultats qualité

- **PHPStan** : ✅ PASS (niveau 9)
- **Elegant Objects** : {score}/100
- **Tests** : ✅ {nombre} tests passants

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

✅ **PRÊTE POUR PR**

La feature est complète, testée (CI passe) et prête pour review.
```

## 3. Mettre à jour le workflow state

Marquer le workflow comme terminé :

```json
{
  "status": "completed",
  "completedAt": "{ISO timestamp}",
  "currentPhase": 8,
  "timing": {
    "totalDurationMs": {somme de tous les durationMs}
  },
  "phases": {
    "8": {
      "status": "completed",
      "completedAt": "{ISO timestamp}",
      "durationMs": {durée}
    }
  }
}
```

## 4. Afficher les étapes suivantes

```
📋 Feature ready for merge

Worktree : {path}
Branch : {branch}

Prochaines étapes :
1. Relancer Claude Code (hors worktree)
2. Créer une PR : /git:pr
3. Review et merge

✨ Phase 8 : Cleanup du worktree en cours...
```

# Format de durée

Formater les durées de manière lisible :
- `< 60s` → `{X}s` (ex: `45s`)
- `< 60min` → `{X}m {Y}s` (ex: `2m 30s`)
- `>= 60min` → `{X}h {Y}m` (ex: `1h 15m`)

# Règles

- ✅ **Être concis** mais **complet**
- ✅ **Mettre en avant les décisions importantes**
- ✅ **Afficher les résultats qualité**
- ✅ **Inclure le timing total**
- ❌ **Pas de checkpoint ou interaction**
