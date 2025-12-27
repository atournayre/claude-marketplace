---
description: Crée une Pull Request optimisée avec workflow structuré
argument-hint: [branch-base, milestone, project, --cd, --no-cd, --delete, --no-review]
---

# Détection automatique du mode (Standard vs CD)

## Étape 1 : Vérifier les flags explicites

Analyser les arguments fournis :
- Si `--cd` présent → Utiliser skill `git-cd-pr`
- Si `--no-cd` présent → Utiliser skill `git-pr`
- Sinon → Passer à l'étape 2

## Étape 2 : Détection automatique

Exécuter la commande suivante pour détecter si le repo est en mode Continuous Delivery :

```bash
gh label list --json name -q '.[].name' | grep -q "^version:" && echo "CD_DETECTED" || echo "STANDARD"
```

- Si `CD_DETECTED` → Utiliser skill `git-cd-pr`
- Si `STANDARD` → Utiliser skill `git-pr`

## Étape 3 : Invoquer le skill approprié

### Mode Standard (git-pr)
- Template PR : `.github/PULL_REQUEST_TEMPLATE/default.md`
- Pas de labels version automatiques

### Mode CD (git-cd-pr)
- Template PR : `.github/PULL_REQUEST_TEMPLATE/cd_pull_request_template.md`
- Labels version:major/minor/patch automatiques
- Copie des labels depuis l'issue liée
- Détection feature flags

## Arguments transmis au skill

Transmettre tous les arguments sauf `--cd` et `--no-cd` au skill sélectionné.
