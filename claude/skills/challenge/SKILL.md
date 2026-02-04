---
name: claude:challenge
description: Évalue ma dernière réponse, donne une note sur 10 et propose des améliorations
model: haiku
allowed-tools: [Read]
argument-hint: ""
version: 1.0.0
license: MIT
---

# Challenge - Auto-évaluation des réponses Claude

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


Analyse critique de ma dernière réponse fournie et proposition d'une version améliorée.

## Purpose
Permettre à Claude d'évaluer objectivement la qualité de sa dernière réponse et d'identifier les axes d'amélioration concrets.

## Variables
- LAST_RESPONSE: Ma dernière réponse dans la conversation
- ORIGINAL_QUESTION: La question ou demande initiale de l'utilisateur
- EVALUATION_CRITERIA: Critères d'évaluation (clarté, pertinence, complétude, précision, format)

## Relevant Files
- Historique de conversation (contexte automatique)

## Workflow

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

## Best Practices
- Être honnête et autocritique sans tomber dans l'auto-flagellation
- Identifier des améliorations concrètes et actionnables
- Ne pas hésiter à reconnaître quand la réponse initiale était déjà bonne
- Expliquer le raisonnement derrière chaque note
- Proposer une version améliorée uniquement si pertinent
- Garder le rapport concis et structuré en listes à puces
