---
model: claude-opus-4-1-20250805
allowed-tools: Bash
description: Ultra-comprehensive analytical thinking for the most complex problems
argument-hint: complex problem or question
---

# Think Ultra - Ultra-Comprehensive Analysis

Activate maximum cognitive ultrathink processing for ultra-comprehensive analysis of: $ARGUMENTS

## Purpose
Ultra-sophisticated analytical thinking framework that applies exhaustive, multi-dimensional problem analysis across seven distinct phases to provide the most comprehensive understanding and solutions for complex problems.

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
- ARGUMENTS: The complex problem or question to analyze (passed by user)

## Instructions
You are now engaging ultra-comprehensive analytical mode. Apply the complete 7-phase analytical framework to thoroughly examine the problem from every conceivable angle. This analysis may require significant processing time and computational resources. The depth of analysis should match the complexity and importance of the problem.

For less complex issues, consider using `/think:harder` instead.

## Ultra-Analysis Framework (7 Phases)

### Phase 1: Problem Architecture Analysis
**Objective**: Deconstruct the problem at its most fundamental level

**Analytical dimensions**:
- **Ontological Analysis**: What is the essential nature of this problem? What does it fundamentally represent?
- **Epistemological Analysis**: How do we know what we know about this problem? What are our knowledge sources and limitations?
- **Categorical Analysis**: How should this problem be classified? What type of problem is this?
- **Structural Analysis**: What are the core components and their relationships?
- **Boundary Analysis**: Where does this problem begin and end? What's included/excluded?

### Phase 2: Multi-Paradigm Analysis
**Objective**: Examine through multiple analytical lenses and perspectives

**Paradigmatic approaches**:
- **Reductionist Perspective**: Break down into smallest analyzable components
- **Holistic Perspective**: Understand as complete integrated system
- **Systems Thinking**: Analyze feedback loops, emergent properties, and system dynamics
- **Network Analysis**: Map relationships, dependencies, and influence patterns
- **Process Analysis**: Examine temporal flows, sequences, and transformations

### Phase 3: Cross-Disciplinary Integration
**Objective**: Apply knowledge and methodologies from multiple domains

**Disciplinary perspectives**:
- **Scientific Approach**: Hypothesis formation, evidence evaluation, reproducibility
- **Engineering Approach**: Constraints, optimization, trade-offs, feasibility
- **Economic Approach**: Costs, benefits, incentives, market dynamics
- **Philosophical Approach**: Ethics, logic, fundamental assumptions
- **Psychological Approach**: Cognitive biases, behavioral patterns, motivation
- **Social Approach**: Group dynamics, cultural factors, power structures
- **Historical Approach**: Precedents, patterns, evolutionary context

### Phase 4: Temporal and Spatial Scaling
**Objective**: Analyze across multiple time horizons and spatial scales

**Temporal scaling**:
- **Immediate**: Short-term implications and urgent considerations
- **Medium-term**: Intermediate consequences and development trajectories
- **Long-term**: Extended impacts and evolutionary outcomes
- **Historical**: Past patterns, precedents, and lessons learned
- **Cyclical**: Recurring patterns and seasonal considerations

**Spatial scaling**:
- **Local**: Immediate environment and direct stakeholders
- **Regional**: Broader geographic and organizational impacts
- **Global**: Worldwide implications and universal considerations
- **Micro**: Individual and small group effects
- **Macro**: System-wide and institutional ramifications

### Phase 5: Uncertainty and Risk Modeling
**Objective**: Comprehensive uncertainty analysis and risk assessment

**Uncertainty categories**:
- **Known Knowns**: Established facts and reliable information
- **Known Unknowns**: Identified gaps in knowledge and information needs
- **Unknown Unknowns**: Potential blind spots and unforeseen factors
- **Contradictory Information**: Conflicting data and interpretations

**Risk assessment**:
- **Probability Analysis**: Likelihood estimation for various outcomes
- **Impact Assessment**: Magnitude and scope of potential consequences
- **Risk Matrix**: Combined probability-impact evaluation
- **Scenario Planning**: Multiple future scenarios and contingencies
- **Monte Carlo Analysis**: Statistical modeling of uncertain variables

### Phase 6: Decision Theory and Game Theory
**Objective**: Optimize decision-making through mathematical and strategic frameworks

**Decision theory applications**:
- **Expected Utility**: Mathematical optimization of outcomes
- **Multi-Criteria Decision Analysis**: Systematic evaluation of trade-offs
- **Decision Trees**: Structured analysis of choices and consequences
- **Real Options**: Valuation of future flexibility and choices
- **Prospect Theory**: Behavioral decision-making under uncertainty

**Game theory applications**:
- **Stakeholder Analysis**: Identify players, strategies, and incentives
- **Nash Equilibrium**: Analyze stable strategic outcomes
- **Cooperative vs Non-cooperative**: Collaboration vs competition dynamics
- **Information Games**: Impact of asymmetric information
- **Evolutionary Strategies**: Long-term strategic adaptation

### Phase 7: Meta-Cognitive Reflection
**Objective**: Analyze the analysis itself and identify cognitive limitations

**Meta-analytical considerations**:
- **Cognitive Bias Assessment**: Identification of potential analytical biases
- **Assumption Validation**: Challenge underlying assumptions and premises
- **Perspective Gaps**: Identify missing viewpoints and stakeholder perspectives
- **Method Limitations**: Recognize constraints of analytical approaches used
- **Confidence Calibration**: Assess accuracy of confidence levels in conclusions

## Ultra-Structured Output Format

### Section 1: Problem Reconceptualization
**Deliverable**: Reformulated problem statement with enhanced clarity and precision

- **Original Problem**: [Restate the original problem]
- **Fundamental Nature**: [Ontological and epistemological insights]
- **Reconceptualized Problem**: [Enhanced problem formulation]
- **Key Assumptions**: [Explicit statement of underlying assumptions]
- **Scope and Boundaries**: [Clear delineation of problem boundaries]

### Section 2: Multi-Dimensional Mapping
**Deliverable**: Comprehensive multi-perspective problem map

- **Component Analysis**: [Key elements and their relationships]
- **System Dynamics**: [Feedback loops and emergent properties]
- **Stakeholder Map**: [All affected parties and their interests]
- **Constraint Analysis**: [Limitations and boundary conditions]
- **Paradigm Synthesis**: [Integration of multiple analytical approaches]

### Section 3: Evidence and Research Integration
**Deliverable**: Comprehensive evidence synthesis across disciplines

- **Scientific Evidence**: [Empirical data and research findings]
- **Historical Precedents**: [Relevant past cases and outcomes]
- **Cross-Disciplinary Insights**: [Knowledge from multiple domains]
- **Evidence Quality Assessment**: [Reliability and validity evaluation]
- **Knowledge Gaps**: [Areas requiring additional research]

### Section 4: Comprehensive Option Analysis
**Deliverable**: Exhaustive evaluation of potential solutions and approaches

- **Option Generation**: [Complete set of potential approaches]
- **Multi-Criteria Evaluation**: [Systematic assessment against key criteria]
- **Trade-off Analysis**: [Explicit examination of compromises]
- **Implementation Feasibility**: [Practical considerations for execution]
- **Option Ranking**: [Prioritized list with justification]

### Section 5: Risk and Uncertainty Assessment
**Deliverable**: Detailed risk analysis and uncertainty quantification

- **Risk Register**: [Comprehensive list of identified risks]
- **Probability-Impact Matrix**: [Quantified risk assessment]
- **Scenario Analysis**: [Multiple future scenarios with probabilities]
- **Sensitivity Analysis**: [Impact of key variable changes]
- **Mitigation Strategies**: [Risk reduction and management approaches]

### Section 6: Strategic Recommendations
**Deliverable**: Actionable strategic guidance with implementation roadmap

- **Primary Recommendation**: [Main strategic direction with justification]
- **Alternative Strategies**: [Secondary options and contingencies]
- **Implementation Roadmap**: [Phased approach with milestones]
- **Success Metrics**: [Measurable indicators of progress]
- **Contingency Plans**: [Adaptive strategies for different scenarios]

### Section 7: Meta-Analysis and Reflection
**Deliverable**: Critical assessment of the analytical process and limitations

- **Analytical Strengths**: [Robust aspects of the analysis]
- **Potential Biases**: [Identified cognitive and methodological biases]
- **Confidence Assessment**: [Calibrated confidence in conclusions]
- **Areas for Further Analysis**: [Recommendations for additional research]
- **Learning and Adaptation**: [How to improve future analyses]

## Workflow

### Étape 0: Initialisation du Timing (OBLIGATOIRE - PREMIÈRE ACTION)
```
🕐 Démarrage: [timestamp Europe/Paris avec CEST/CET]
```
- Cette étape DOIT être la toute première action
- Enregistrer le timestamp pour calcul ultérieur

### Phase Execution
- Apply each of the 7 analytical phases systematically
- Generate comprehensive insights for each phase
- Integrate findings across phases for holistic understanding
- Maintain rigorous analytical standards throughout

### Output Generation
- Structure findings according to the 7-section output format
- Ensure actionable and implementable recommendations
- Provide clear reasoning chains for all conclusions
- Include confidence levels and uncertainty acknowledgments

### Quality Assurance
- Validate findings against multiple analytical frameworks
- Check for internal consistency and logical coherence
- Assess completeness of analysis across all dimensions
- Calibrate confidence levels appropriately

## Report
Generate ultra-comprehensive analysis report including:

**Executive Summary**:
- Problem reconceptualization and key insights
- Primary strategic recommendations
- Critical risks and mitigation strategies
- Implementation priorities and success factors

**Detailed Analysis**:
- Complete 7-section structured output
- Supporting evidence and reasoning chains
- Risk assessment and scenario analysis
- Implementation roadmap and success metrics

**Meta-Analysis**:
- Analytical confidence assessment
- Identified limitations and biases
- Recommendations for ongoing monitoring
- Areas requiring additional analysis

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]

---

**Note**: This ultra-comprehensive analysis framework is designed for complex, high-stakes problems requiring exhaustive examination. The analysis may require significant time and computational resources. For simpler problems, consider using `/think:harder` instead.