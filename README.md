# Flip 7 Card Game Simulator

A sophisticated simulation of the Flip 7 card game featuring AI players with configurable personalities, profile-based strategies, and comprehensive analytics.

## Overview

Flip 7 is a card game where players aim to collect exactly 7 unique number cards. The game combines strategy, risk management, and luck through:

- **Card Types**:
  - Number cards (0-12)
  - Action cards (Freeze, Deal Three, Second Chance)
  - Modifier cards (bonuses and multipliers)
- **Player Actions**:
  - Draw cards
  - Use action cards
  - Pass or freeze
- **Win Condition**: First player to collect exactly 7 unique number cards

## Features

### AI Strategy System
- **Profile-Based Decision Making**
  - YAML-configured player personalities
  - Dynamic risk assessment
  - Personality-driven choices
  - Learning and adaptation
  - Deck awareness and card counting

- **Player Attributes**
  - Intelligence (0-1): Affects decision quality
  - Risk Tolerance: Base risk and situational adjustments
  - Target Score: Preferred winning score
  - Catch-up Behavior: Aggression when behind
  - Lucky/Unlucky Cards: Superstitious preferences

### Simulation Engine
- Configurable game parameters
- Multi-player support (2-6 players)
- Reproducible results with seed control
- Detailed statistics tracking
- Mixed player types (profiled and default AI)

### Analytics and Visualization
- **Game Statistics**
  - Win rates by player/profile
  - Score distributions
  - Bust/freeze/pass rates
  - Risk adjustment patterns
  
- **Visual Analysis**
  - Score progression charts
  - Player outcome analysis
  - Head-to-head comparisons
  - Summary dashboards

## Project Structure

```
flip7/
├── src/
│   ├── game/               # Core game implementation
│   │   ├── card.py        # Card types and mechanics
│   │   ├── game.py        # Game logic and flow
│   │   └── player.py      # Player actions and state
│   ├── profiles/          # AI player profiles
│   │   ├── data/          # Profile configurations
│   │   ├── profile_loader.py  # YAML handling
│   │   └── strategy.py    # Decision making
│   ├── simulation/        # Simulation engine
│   │   └── simulator.py   # Game orchestration
│   ├── visualization/     # Analytics tools
│   │   └── visualizer.py  # Data visualization
│   └── run_profile_simulation.py  # Main script
├── tests/                 # Test suite
└── output/               # Generated results
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/flip7.git
cd flip7
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e .
```

## Usage

Run a simulation with pre-configured profiles:
```bash
python src/run_profile_simulation.py
```

This will:
1. Run 1000 games with various player profiles
2. Generate visualizations in `output/`
3. Log statistics to `simulation.log`

### Available Player Profiles

1. **Balanced Betty**
   - Well-rounded decision making
   - Adapts to game situations
   - Moderate risk tolerance
   - No superstitions

2. **Cautious Carl**
   - Risk-averse strategy
   - Values consistency
   - Prefers lower scores
   - Some card superstitions

3. **Risk Taker Rachel**
   - Aggressive play style
   - High risk tolerance
   - Aims for high scores
   - Pure logic-based decisions

4. **Superstitious Sam**
   - Heavily influenced by numerology
   - Avoids "unlucky" numbers
   - Prefers odd-numbered cards
   - High intelligence but superstitious

5. **YOLO Yuki**
   - Extremely aggressive
   - Maximum risk tolerance
   - Unrealistic target scores
   - Chaotic decision making

## Technical Implementation

### Profile System
```yaml
# Example Profile Structure
name: "Profile Name"
description: "Profile description"
intelligence: 0.7  # 0-1 scale
risk_tolerance:
  base: 0.5
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

### Decision Making Process
1. **Base Risk Calculation**
   - Profile's base risk tolerance
   - Current card count impact
   - Score relative to target
   - Intelligence factor

2. **Situational Adjustments**
   - Deck composition awareness
   - Other players' scores
   - Lucky/unlucky card effects
   - Catch-up behavior

3. **Final Decision**
   - Personality modifications
   - Random factor based on intelligence
   - Action selection (draw/pass/freeze)

### Learning Mechanism
- Tracks successful decisions
- Adapts risk tolerance based on outcomes
- Intelligence-based learning rate
- Per-game state memory

## Dependencies

- numpy>=1.26.0: Numerical operations
- pandas>=2.1.0: Data manipulation
- matplotlib>=3.8.0: Basic plotting
- seaborn>=0.13.0: Advanced visualization
- pytest>=7.4.0: Testing framework
- loguru>=0.7.0: Logging system
- pyyaml>=6.0.1: Profile configuration
- tqdm>=4.66.0: Progress tracking

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
