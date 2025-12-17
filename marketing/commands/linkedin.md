---
description: Génère un post LinkedIn attractif basé sur les dernières modifications du marketplace
argument-hint: "[nombre-de-jours]"
model: claude-sonnet-4-20250514
---

# Génération de post LinkedIn pour le marketplace Claude Plugins

## Contexte
Tu es un expert en communication LinkedIn et développement. Tu dois créer un post engageant pour promouvoir les dernières nouveautés du marketplace de plugins Claude Code.

## Étapes

### 1. Analyse des modifications récentes
Utilise git pour analyser les commits récents :
```bash
git log --oneline --since="$ARGUMENTS days ago" --no-merges 2>/dev/null || git log --oneline -20 --no-merges
```

Si `$ARGUMENTS` n'est pas fourni, utilise les 7 derniers jours par défaut.

### 2. Catégorisation des changements
Classe les modifications par type :
- **Nouveaux plugins** : Plugins entièrement nouveaux
- **Nouvelles fonctionnalités** : Commandes, skills, agents ajoutés
- **Améliorations** : Optimisations, corrections, refactoring

### 3. Génération du post LinkedIn

Crée un post qui respecte ces critères :
- **Longueur** : 1200-1500 caractères max (optimal LinkedIn)
- **Structure** :
  - Accroche percutante (1-2 lignes)
  - Corps avec les highlights (bullets points avec emojis)
  - Call-to-action final
- **Ton** : Professionnel mais accessible, enthousiaste sans être commercial
- **Emojis** : Utilise-les avec parcimonie (3-5 max)
- **Hashtags** : 3-5 hashtags pertinents en fin de post

### 4. Format de sortie

```
📝 POST LINKEDIN
================

[Le post formaté prêt à copier-coller]

---
📊 Statistiques :
- Caractères : X
- Hashtags : #tag1 #tag2...
- Période couverte : X jours
- Nombre de changements analysés : X
```

## Bonnes pratiques LinkedIn
- Première ligne = accroche visible sans "voir plus"
- Lignes courtes et aérées
- Questions pour engager
- Valeur ajoutée claire pour le lecteur
- Éviter le jargon technique excessif
