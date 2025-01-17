# AI Version 2: Player Profiles Implementation Plan

## Overview
This document outlines the implementation of configurable player profiles in the Flip 7 game simulation. The system enables diverse and realistic player behaviors, from rational strategies to personality-driven play styles.

## 1. Profile System Architecture

### 1.1 Profile Organization
- All profiles stored in `src/profiles/data/`
- YAML-based configuration with validation
- Standardized format for all profiles
- Example profiles included:
  1. Balanced Betty (well-rounded)
  2. Cautious Carl (risk-averse)
  3. Risk Taker Rachel (aggressive)
  4. Superstitious Sam (numerology-focused)
  5. YOLO Yuki (chaotic)

### 1.2 Profile Structure
```yaml
name: "Profile Name"
description: "Profile description"
intelligence: 0.7  # Scale 0-1
risk_tolerance:
  base: 0.5       # Scale 0-1
  card_count_weights: [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4]
  score_sensitivity: 0.6
  deck_awareness: 0.7
target_score: 55
catch_up_aggression: 0.4
lucky_cards:
  enabled: true
  cards: [7, "Second Chance"]
superstitions:
  enabled: true
  negative: [13, "Deal Three"]
  threshold: 0.3
```

### 1.3 Profile Assignment
Supported through `SimulationConfig` and `PlayerConfig`:
```python
config = SimulationConfig(
    num_games=1000,
    num_players=6,
    base_seed=42,
    player_configs=[
        PlayerConfig(position=0, profile_name="Balanced Betty"),
        PlayerConfig(position=1, profile_name="Risk Taker Rachel"),
        # ... additional players
    ]
)
```

## 2. Strategic Decision Making

### 2.1 Base Strategy Components
1. **Risk Assessment**
   - Profile's base risk tolerance
   - Card count impact (configurable weights)
   - Score relative to target
   - Deck composition awareness

2. **Personality Factors**
   - Intelligence-based decision quality
   - Lucky/unlucky card effects
   - Superstition thresholds
   - Catch-up behavior

3. **Game State Analysis**
   - Other players' scores
   - Cards seen in play
   - Probability calculations
   - Position in turn order

### 2.2 Profile-Specific Behaviors

1. **Balanced Betty**
   - Adaptive risk tolerance
   - No superstitions
   - Moderate target score
   - High intelligence

2. **Cautious Carl**
   - Low base risk
   - Conservative card weights
   - Some superstitions
   - Moderate intelligence

3. **Risk Taker Rachel**
   - High base risk
   - Aggressive scoring
   - No superstitions
   - High intelligence

4. **Superstitious Sam**
   - Numerology-driven
   - Odd number preference
   - Strong superstitions
   - High intelligence but overridden

5. **YOLO Yuki**
   - Maximum risk tolerance
   - Unrealistic targets
   - Chaotic decisions
   - Low intelligence

## 3. Analytics System

### 3.1 Statistics Tracking
- Games played/won
- Score distributions
- Action rates (bust/freeze/pass)
- Risk adjustment patterns
- Personality effect metrics

### 3.2 Visualization Suite
1. **Core Visualizations**
   - Winning scores distribution
   - Player outcomes analysis
   - Win rates comparison
   - Score progression

2. **Head-to-Head Analysis**
   - Direct comparisons
   - Score distributions
   - Outcome types
   - Strategy evolution

3. **Dashboard Generation**
   - Combined statistics
   - Profile performance
   - Comparative metrics
   - Trend analysis

## 4. Implementation Status

### 4.1 Completed
- Profile system architecture
- YAML configuration
- Core strategy implementation
- Basic visualization suite
- Initial profile set

### 4.2 In Progress
- Advanced analytics
- Strategy refinement
- Performance optimization
- Documentation updates

### 4.3 Future Enhancements
- Additional profiles
- Machine learning integration
- Real-time visualization
- Profile generation tools

## 5. Testing Framework

### 5.1 Unit Tests
- Profile loading/validation
- Strategy calculations
- Personality effects
- Decision making

### 5.2 Integration Tests
- Full game simulations
- Multi-profile interactions
- Statistics collection
- Visualization generation

### 5.3 Profile Validation
- Behavior verification
- Statistical analysis
- Performance metrics
- Comparison studies 