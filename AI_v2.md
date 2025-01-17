# AI Version 2: Player Profiles Implementation Plan

## Overview
This document outlines the implementation plan for adding configurable player profiles to the Flip 7 game simulation. The new system will allow for more diverse and realistic player behaviors, ranging from purely rational strategies to quirky, personality-driven play styles.

## 1. Profile System Architecture

### 1.1 Profile Format
- Profiles defined in YAML files
- Each profile represents a distinct player personality and strategy
- Profiles can be mixed with default AI players
- Example profile structure:
```yaml
name: "Cautious Carl"
description: "A risk-averse player who values consistency over high scores"
intelligence: 0.7  # Scale 0-1
risk_tolerance:
  base: 0.3       # Scale 0-1
  card_count_weights: [1.0, 0.9, 0.8, 0.6, 0.4, 0.2, 0.1]  # Weight per card count
  score_sensitivity: 0.8  # How much current score affects decisions
  deck_awareness: 0.6    # How much remaining cards influence decisions
target_score: 45
catch_up_aggression: 0.4  # Scale 0-1
lucky_cards:
  enabled: true
  cards: [7, "Second Chance"]  # Can be numbers or card types
superstitions:
  enabled: true
  negative: [13, "Deal Three"]  # Numbers or cards considered unlucky
  threshold: 0.2  # Probability modifier when these cards are drawn
```

### 1.2 Profile Assignment
Two supported methods:
1. **Explicit Assignment**:
```yaml
game_config:
  players:
    - position: 1
      profile: "Cautious Carl"
    - position: 2
      profile: "default"
    - position: 3
      profile: "Risk Taker Rachel"
```

2. **Random Assignment**:
```yaml
game_config:
  total_players: 6
  profiles:
    - name: "Cautious Carl"
      count: 2
    - name: "Risk Taker Rachel"
      count: 2
    # Remaining 2 players will use default AI
```

## 2. Strategic Decision Making

### 2.1 Base Strategy Components
1. **Risk Tolerance**
   - Base risk level modified by:
     - Current card count
     - Current score
     - Analysis of remaining deck
     - Position relative to other players

2. **Target Score**
   - Influences when player chooses to pass
   - Affects risk calculations when near target

3. **Catch-up Behavior**
   - Aggression level modifies risk tolerance
   - More aggressive when behind leader
   - Risk modification = base_risk * (1 + aggression * score_difference / max_possible_score)

### 2.2 Personality Elements
1. **Lucky Cards**
   - Increases risk tolerance after drawing specified cards
   - Effect scales with how many lucky cards seen in current round

2. **Superstitions**
   - Decreases risk tolerance after drawing specified cards
   - Can make player more likely to pass or freeze

### 2.3 Intelligence-Based Adaptation
Intelligence metric affects:
1. **Game State Analysis**
   - Higher intelligence = better at counting cards
   - More accurate assessment of bust probability

2. **Opponent Modeling**
   - Tracking other players' tendencies
   - Adjusting strategy based on opponent patterns

3. **Learning**
   - Adapting strategy based on previous game outcomes
   - Persistence within simulation, reset between simulations

## 3. Statistics and Analysis

### 3.1 Profile-Specific Statistics
Track per profile:
- Win rate
- Average score
- Bust/freeze/pass rates
- Lucky card impact
- Superstition impact
- Risk adjustment frequency
- Strategy adaptation patterns
- Catch-up behavior effectiveness

### 3.2 Comparative Analysis
Support for:
- Profile vs profile performance
- Profile vs default AI performance
- Impact of intelligence on win rates
- Effect of personality traits on outcomes

## 4. Visualization Enhancements

### 4.1 Profile Performance Visualizations
1. **Profile Comparison Dashboard**
```python
def create_profile_comparison(data):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Win rates by profile
    sns.barplot(data=data, x='profile', y='win_rate', ax=ax1)
    
    # Score distributions by profile
    sns.violinplot(data=data, x='profile', y='score', ax=ax2)
    
    # Outcome types by profile
    sns.heatmap(data.pivot('profile', 'outcome', 'frequency'), ax=ax3)
    
    # Risk tolerance over time
    sns.lineplot(data=data, x='game_number', y='risk_level', 
                hue='profile', ax=ax4)
```

2. **Strategy Adaptation Visualization**
```python
def plot_strategy_evolution(data):
    # Show how profiles adapt over simulation
    sns.relplot(data=data, x='game_number', y='risk_taken',
                col='profile', hue='position',
                kind='line', col_wrap=3)
```

3. **Personality Impact Analysis**
```python
def plot_personality_effects(data):
    # Lucky card and superstition effects
    g = sns.FacetGrid(data, col='profile', row='trait_type')
    g.map_dataframe(sns.boxplot, x='trait_active', y='risk_taken')
```

### 4.2 Head-to-Head Analysis
Specific visualizations for profile vs profile comparisons:
- Direct win rate comparisons
- Score distribution overlays
- Strategy difference analysis
- Adaptation pattern comparison

## 5. Implementation Phases

### Phase 1: Core Profile System
1. Create YAML profile structure
2. Implement profile loading and validation
3. Modify Player class to support profiles
4. Update Simulator for profile assignment

### Phase 2: Strategic Behaviors
1. Implement risk tolerance system
2. Add catch-up behavior
3. Develop personality trait effects
4. Create intelligence-based adaptations

### Phase 3: Statistics and Analysis
1. Add profile-specific stat tracking
2. Implement comparative analysis
3. Create profile performance metrics
4. Develop analysis tools

### Phase 4: Visualization
1. Create profile comparison visualizations
2. Implement strategy adaptation plots
3. Add personality impact analysis
4. Develop head-to-head comparison tools

## 6. Testing Strategy

### 6.1 Unit Tests
- Profile loading and validation
- Strategy calculation
- Personality trait effects
- Intelligence adaptation

### 6.2 Integration Tests
- Profile assignment methods
- Multi-profile simulations
- Statistics collection
- Visualization generation

### 6.3 Validation Tests
- Strategy effectiveness
- Profile behavior accuracy
- Statistical significance
- Visualization accuracy 