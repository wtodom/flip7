# Flip 7 Card Game Simulator

A sophisticated simulation of the Flip 7 card game featuring AI players with configurable personalities, profile-based strategies, and comprehensive analytics. Created by AI with Cursor.

For detailed simulation results and visualization examples, see [RESULTS.md](RESULTS.md).

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
- **Win Condition**: First player to collect exactly 7 unique number cards or highest score when all players are done

## Features

### AI Strategy System
- **Profile-Based Decision Making**
  - YAML-configured player personalities
  - Dynamic risk assessment
  - Personality-driven choices
  - Learning and adaptation
  - Deck awareness and card counting

- **Player Attributes**
  - Intelligence (0-1): Affects decision quality and learning
  - Risk Tolerance: Base risk and situational adjustments
  - Target Score: Preferred winning score
  - Catch-up Behavior: Aggression when behind
  - Lucky/Unlucky Cards: Superstitious preferences

### Profile System
The AI player profiles are designed to provide diverse and realistic behaviors, from rational strategies to personality-driven play styles. All profiles are stored in `src/profiles/data/` and are defined in a standardized YAML format.

#### Profile Structure
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

#### Example Profiles
1. **Balanced Betty**: Well-rounded decision making, adapts to game situations, moderate risk tolerance (0.55), target score: 52, no superstitions.
2. **Cautious Carl**: Risk-averse strategy, values consistency, prefers lower scores (Target: 45), superstitious about 12 and Deal Three cards, high deck awareness.
3. **Risk Taker Rachel**: Aggressive play style, high intelligence (0.9), aims for high scores (Target: 65), strong deck awareness, pure logic-based decisions.
4. **Superstitious Sam**: Heavily influenced by numerology, avoids specific "unlucky" numbers, high intelligence but superstitious, moderate risk tolerance.
5. **YOLO Yuki**: Extremely aggressive (Base risk: 0.95), low intelligence (0.3), unrealistic target score (77), maximum catch-up aggression.

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
  - Head-to-head comparisons with detailed metrics
  - Summary dashboards
  - Rolling average performance tracking

## Project Structure

```
flip7/
├── src/
│   ├── game/               # Core game implementation
│   │   ├── __init__.py
│   │   ├── card.py        # Card types and mechanics
│   │   ├── deck.py        # Deck management
│   │   ├── game.py        # Game logic and flow
│   │   └── player.py      # Player actions and state
│   ├── profiles/          # AI player profiles
│   │   ├── __init__.py
│   │   ├── data/          # Profile configurations
│   │   │   ├── balanced_betty.yaml
│   │   │   ├── cautious_carl.yaml
│   │   │   ├── risk_taker_rachel.yaml
│   │   │   ├── superstitious_sam.yaml
│   │   │   └── yolo_yuki.yaml
│   │   ├── profile_loader.py  # YAML handling
│   │   └── strategy.py    # Decision making
│   ├── simulation/        # Simulation engine
│   │   ├── __init__.py
│   │   └── simulator.py   # Game orchestration
│   ├── visualization/     # Analytics tools
│   │   ├── __init__.py
│   │   └── visualizer.py  # Data visualization
│   └── run_profile_simulation.py  # Main script
├── tests/                 # Test suite
├── setup.py              # Package configuration
├── requirements.txt      # Dependencies
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
2. Generate visualizations in `output/`:
   - Winning scores distribution
   - Player outcomes analysis
   - Win rates comparison
   - Score progression
   - Head-to-head comparisons
   - Summary dashboard
3. Log detailed statistics to `simulation.log`

## Technical Implementation

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
