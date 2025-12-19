---
description: Résumé de ce qui a été construit (Phase 7)
model: claude-haiku-4-5-20251001
allowed-tools: Read, Glob
---

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

## 3. Nettoyer le workflow state

Marquer le workflow comme terminé :

```json
{
  "status": "completed",
  "completedAt": "{timestamp}",
  "currentPhase": 7
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
