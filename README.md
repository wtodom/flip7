# Flip 7 Card Game Simulator

A sophisticated simulation of the Flip 7 card game with AI players, profile-based strategies, and detailed analytics. Created by AI with Cursor.

## Game Overview

Flip 7 is a card game where players aim to collect exactly 7 unique number cards. The game includes:
- Number cards (0-12)
- Action cards (Freeze, Deal Three, Second Chance)
- Modifier cards (bonuses and multipliers)

Players take turns drawing cards, trying to achieve exactly 7 unique numbers while avoiding busting.

## Features

### Core Game Mechanics
- Complete implementation of Flip 7 rules
- Support for 2-6 players
- Action cards with special effects
- Modifier cards for score adjustments

### Player Profiles System
- YAML-based player profile configuration
- Customizable player personalities and strategies
- Profile attributes include:
  - Intelligence (affects decision quality)
  - Risk tolerance (base risk and situational adjustments)
  - Target score preferences
  - Lucky/unlucky card superstitions
  - Catch-up behavior when behind

### AI Strategy Engine
- Profile-driven decision making
- Dynamic risk assessment based on:
  - Current hand composition
  - Cards seen in play
  - Other players' scores
  - Game state awareness
- Learning capabilities for high-intelligence profiles
- Personality-based decision modifications

### Simulation Features
- Configurable number of games and players
- Detailed statistics tracking
- Support for mixed player types (profiled and default)
- Reproducible results with seed control

### Visualization and Analytics
- Distribution of winning scores
- Player outcome analysis (bust/freeze/pass rates)
- Win rates by player and profile
- Score progression analysis
- Summary dashboards

## Project Structure

```
flip7/
├── src/
│   ├── game/
│   │   ├── card.py         # Card types and mechanics
│   │   ├── player.py       # Player implementation
│   │   └── game.py         # Core game logic
│   ├── profiles/
│   │   ├── profile_loader.py  # Profile loading and validation
│   │   └── strategy.py        # Profile-based decision making
│   ├── simulation/
│   │   └── simulator.py    # Simulation engine
│   └── visualization/
│       └── visualizer.py   # Data visualization
├── profiles/              # Player profile definitions
│   ├── cautious_carl.yaml
│   └── risk_taker_rachel.yaml
├── tests/                # Test suite
└── output/              # Simulation results and visualizations
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

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running a Simulation

```python
from src.simulation.simulator import Simulator, SimulationConfig

config = SimulationConfig(
    num_games=1000,
    num_players=6,
    base_seed=42,
    profiles_dir="profiles"
)

simulator = Simulator(config)
results = simulator.run()
```

### Creating Player Profiles

Create a YAML file in the `profiles` directory:

```yaml
name: "Cautious Carl"
description: "A conservative player who prefers to play it safe"
intelligence: 0.7
risk_tolerance:
  base: 0.4
  card_count_weights: [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4]
  score_sensitivity: 0.6
  deck_awareness: 0.8
target_score: 50
catch_up_aggression: 0.3
lucky_cards:
  enabled: true
  cards: [7]
superstitions:
  enabled: true
  negative: [13]
  threshold: 0.5
```

## Technical Details

### Profile System Architecture
- **Profile Loading**: YAML-based configuration with validation
- **Strategy Components**:
  - Base risk calculation
  - Deck awareness adjustments
  - Personality-based modifications
  - Catch-up behavior
  - Learning and adaptation

### Decision Making Process
1. Calculate base risk from profile settings
2. Adjust for current game state
3. Apply personality modifiers
4. Consider catch-up behavior
5. Make final decision with randomization

### Learning Mechanism
- Tracks successful decisions
- Adapts risk tolerance based on outcomes
- Intelligence-based learning rate
- Per-game state memory

## Dependencies

- numpy>=1.26.0
- pandas>=2.1.0
- matplotlib>=3.8.0
- seaborn>=0.13.0
- pytest>=7.4.0
- loguru>=0.7.0
- pyyaml>=6.0.1
- tqdm>=4.66.0

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
