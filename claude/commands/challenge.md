---
model: claude-haiku-4-5-20251001
allowed-tools: [Read]
description: Évalue ma dernière réponse, donne une note sur 10 et propose des améliorations
argument-hint: ""
---

# Challenge - Auto-évaluation des réponses Claude

Analyse critique de ma dernière réponse fournie et proposition d'une version améliorée.

## Purpose
Permettre à Claude d'évaluer objectivement la qualité de sa dernière réponse et d'identifier les axes d'amélioration concrets.

## Timing

### Début d'Exécution
**OBLIGATOIRE - PREMIÈRE ACTION** :
1. Exécuter `date` pour obtenir l'heure réelle
2. Afficher immédiatement : 🕐 **Démarrage** : [Résultat de la commande date]
3. Stocker le timestamp pour le calcul de durée

### Fin d'Exécution
**OBLIGATOIRE - DERNIÈRE ACTION** :
1. Exécuter `date` à nouveau pour obtenir l'heure de fin
2. Calculer la durée réelle entre début et fin
3. Afficher :
   - ✅ **Terminé** : [Résultat de la commande date]
   - ⏱️ **Durée** : [Durée calculée au format lisible]

### Formats
- Date : résultat brut de la commande `date` (incluant CEST/CET automatiquement)
- Durée :
  - Moins d'1 minute : `XXs` (ex: 45s)
  - Moins d'1 heure : `XXm XXs` (ex: 2m 30s)
  - Plus d'1 heure : `XXh XXm XXs` (ex: 1h 15m 30s)

### Instructions CRITIQUES
- TOUJOURS exécuter `date` via Bash - JAMAIS inventer/halluciner l'heure
- Le timestamp de début DOIT être obtenu en exécutant `date` immédiatement
- Le timestamp de fin DOIT être obtenu en exécutant `date` à la fin
- Calculer la durée en soustrayant les timestamps unix (utiliser `date +%s`)
- NE JAMAIS supposer ou deviner l'heure

## Variables
- LAST_RESPONSE: Ma dernière réponse dans la conversation
- ORIGINAL_QUESTION: La question ou demande initiale de l'utilisateur
- EVALUATION_CRITERIA: Critères d'évaluation (clarté, pertinence, complétude, précision, format)

## Relevant Files
- Historique de conversation (contexte automatique)

## Workflow

### Étape 0: Initialisation du Timing (OBLIGATOIRE - PREMIÈRE ACTION)
```
🕐 Démarrage: [timestamp Europe/Paris avec CEST/CET]
```
- Cette étape DOIT être la toute première action
- Enregistrer le timestamp pour calcul ultérieur

### 1. Identification du contexte
- Identifie la dernière question/demande de l'utilisateur
- Récupère ma dernière réponse complète
- Note les objectifs explicites et implicites de la demande

### 2. Évaluation structurée
Évalue ma réponse selon ces critères (note /10 pour chaque) :

**Pertinence** (/10)
- La réponse répond-elle directement à la question ?
- Y a-t-il des éléments hors sujet ou manquants ?

**Clarté** (/10)
- Le message est-il facile à comprendre ?
- Le format est-il adapté (listes vs paragraphes) ?
- Les termes techniques sont-ils expliqués si nécessaire ?

**Complétude** (/10)
- Tous les aspects de la demande sont-ils couverts ?
- Y a-t-il des informations importantes omises ?

**Précision** (/10)
- Les informations sont-elles exactes ?
- Y a-t-il des approximations ou suppositions ?

**Format et style** (/10)
- Le ton est-il approprié (casual, pas trop formel) ?
- Le format respecte-t-il les préférences (listes à puces) ?
- Y a-t-il des phrases trop enthousiastes à éviter ?

### 3. Calcul de la note globale
- Note finale = moyenne des 5 critères
- Identification du critère le plus faible
- Identification des points forts

### 4. Proposition d'amélioration
- Liste concrète de ce qui pourrait être amélioré
- Proposition d'une version améliorée si la note < 8/10
- Focus sur les critères les plus faibles

## Report

### Structure du rapport d'évaluation

**📊 Évaluation de ma dernière réponse**

**Question initiale :**
[Rappel de la question]

**Ma réponse :**
[Résumé bref de ce que j'ai fourni]

**Scores détaillés :**
- 🎯 Pertinence : X/10 - [justification courte]
- 💡 Clarté : X/10 - [justification courte]
- ✅ Complétude : X/10 - [justification courte]
- 🔍 Précision : X/10 - [justification courte]
- 📝 Format/Style : X/10 - [justification courte]

**Note globale : X/10**

**Points forts :**
- [Point fort 1]
- [Point fort 2]

**Axes d'amélioration :**
- [Amélioration 1]
- [Amélioration 2]
- [Amélioration 3]

**Version améliorée (si note < 8/10) :**
[Nouvelle version de la réponse intégrant les améliorations]

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]

## Best Practices
- Être honnête et autocritique sans tomber dans l'auto-flagellation
- Identifier des améliorations concrètes et actionnables
- Ne pas hésiter à reconnaître quand la réponse initiale était déjà bonne
- Expliquer le raisonnement derrière chaque note
- Proposer une version améliorée uniquement si pertinent
- Garder le rapport concis et structuré en listes à puces
