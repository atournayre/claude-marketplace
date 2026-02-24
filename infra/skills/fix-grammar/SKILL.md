---
name: infra:fix-grammar
description: Corrige les fautes de grammaire et d'orthographe dans un ou plusieurs fichiers en préservant le formatage, la structure et les termes techniques. Traitement parallèle pour plusieurs fichiers.
allowed-tools: [Read, Edit, Write, Task]
argument-hint: <file-path> [additional-files...]
model: sonnet
version: 1.0.0
license: MIT
---

# infra:fix-grammar

Correction grammaticale de fichiers en préservant le sens et le formatage.

## Instructions à Exécuter

### 1. Parser les fichiers

Découper les arguments en chemins de fichiers individuels.
Arrêter si aucun fichier spécifié — demander à l'utilisateur.

### 2. Déterminer la stratégie

- **Fichier unique** : traiter directement
- **Fichiers multiples** : lancer des agents fix-grammar en parallèle

### 3. Fichier unique

1. `Read` le fichier complètement
2. Appliquer les corrections de grammaire et d'orthographe
3. `Edit` pour mettre à jour le fichier

### 4. Fichiers multiples

Utiliser Task pour lancer un agent fix-grammar par fichier, tous en parallèle.

### 5. Rapport

```
Grammaire corrigée dans [fichier]
  - [N] corrections effectuées
```

## Règles de correction

- Corriger UNIQUEMENT les fautes d'orthographe et de grammaire
- Ne PAS modifier le sens ou l'ordre des mots
- Ne PAS traduire quoi que ce soit
- Ne PAS modifier les balises spéciales (MDX, syntaxe custom, blocs de code)
- CONSERVER : tout le formatage, la structure, les termes techniques
- Supprimer les marqueurs `"""` si présents
- Conserver la même langue dans chaque phrase
- Gérer le contenu multilingue (anglicismes, termes techniques)

## Exemples

```bash
/infra:fix-grammar README.md
/infra:fix-grammar docs/guide.md docs/api.md docs/setup.md
```
