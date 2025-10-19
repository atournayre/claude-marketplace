---
model: claude-opus-4-1-20250805
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
description: Engage in intensive analytical thinking for complex problem solving and decision making
---

# Think Harder

Engage in intensive analytical thinking to think harder about: **$ARGUMENTS**

## Purpose
This command applies systematic reasoning methodology to complex problems, helping you break down challenges and arrive at well-reasoned solutions through deep analysis.

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
ARGUMENTS: The problem, question, or topic to analyze deeply

## Deep Analysis Protocol

Apply systematic reasoning with the following methodology:

### 1. Problem Clarification
- Define the core question and identify implicit assumptions
- Establish scope, constraints, and success criteria
- Surface potential ambiguities and multiple interpretations

### 2. Multi-Dimensional Analysis
- **Structural decomposition**: Break into fundamental components and dependencies
- **Stakeholder perspectives**: Consider viewpoints of all affected parties
- **Temporal analysis**: Examine short-term vs. long-term implications
- **Causal reasoning**: Map cause-effect relationships and feedback loops
- **Contextual factors**: Assess environmental, cultural, and situational influences

### 3. Critical Evaluation
- Challenge your initial assumptions and identify cognitive biases
- Generate and evaluate alternative hypotheses or solutions
- Conduct pre-mortem analysis: What could go wrong and why?
- Consider opportunity costs and trade-offs for each approach
- Assess confidence levels and sources of uncertainty

### 4. Synthesis and Integration
- Connect insights across different domains and disciplines
- Identify emergent properties from component interactions
- Reconcile apparent contradictions or paradoxes
- Develop meta-insights about the problem-solving process itself

## Workflow

### Étape 0: Initialisation du Timing (OBLIGATOIRE - PREMIÈRE ACTION)
```
🕐 Démarrage: [timestamp Europe/Paris avec CEST/CET]
```
- Cette étape DOIT être la toute première action
- Enregistrer le timestamp pour calcul ultérieur

### Analysis Process
- Read relevant files in the codebase if the problem is code-related
- Apply the Deep Analysis Protocol systematically
- Document findings and reasoning at each step
- Synthesize insights into actionable recommendations

### Output Structure
Present your analysis in this format:
1. **Problem Reframing**: How you understand the core issue
2. **Key Insights**: Most important discoveries from your analysis
3. **Reasoning Chain**: Step-by-step logical progression
4. **Alternatives Considered**: Different approaches evaluated
5. **Uncertainties**: What you don't know and why it matters
6. **Actionable Recommendations**: Specific, implementable next steps

## Instructions
- Be thorough yet concise
- Show your reasoning process, not just conclusions
- Question assumptions and consider multiple perspectives
- Focus on practical, implementable solutions
- Acknowledge limitations and uncertainties

## Examples

### Example Usage
```
/think:harder "Should we refactor this legacy codebase or rewrite it?"
```

### Expected Analysis Structure
1. **Problem Reframing**: "This is fundamentally a question of technical debt management vs. development velocity"
2. **Key Insights**: Major factors affecting the decision
3. **Reasoning Chain**: Cost-benefit analysis process
4. **Alternatives Considered**: Refactor, rewrite, hybrid approach
5. **Uncertainties**: Team capacity, timeline constraints
6. **Actionable Recommendations**: Specific next steps with timelines

## Report
Apply the Deep Analysis Protocol to generate comprehensive insights that enable better decision-making and problem-solving for complex technical and strategic challenges.

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]