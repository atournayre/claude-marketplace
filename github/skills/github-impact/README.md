# GitHub Impact Analysis Skill

Génère automatiquement deux rapports d'impact (métier et technique) pour une PR GitHub et les intègre dans la description.

## Fonctionnalités

- Analyse complète des modifications PR
- Détection automatique des dépendances (PHP, JS, templates)
- Analyse de couverture de tests
- Génération de 2 rapports distincts (métier + technique)
- Intégration automatique dans la description PR
- Sauvegarde locale pour référence

## Usage

Via la commande délégante :
```bash
/github:impact <pr-number>
```

Ou directement via le skill :
```bash
# Utiliser l'outil Task avec le skill github-impact
```

## Rapports générés

### Rapport Métier
- Vue d'ensemble des changements fonctionnels
- Impact utilisateur
- Risques identifiés
- Recommandations déploiement

### Rapport Technique
- Métriques détaillées (fichiers, lignes, commits)
- Analyse par type de fichier
- Changements architecturaux
- Analyse de sécurité
- Couverture de tests

## Fichiers générés

- `.analysis-reports/impact_pr_<number>.md` - Rapports combinés
- Description PR mise à jour avec marqueurs `<!-- IMPACT-REPORTS-START/END -->`

## Dépendances

- `gh` CLI configuré et authentifié
- Accès en lecture à la PR
- Accès en écriture pour mise à jour description
