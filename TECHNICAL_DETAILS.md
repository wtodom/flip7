# Technical Details

## 1. Project Structure and Organization

The project follows a modular architecture with clear separation of concerns:

```
flip7/
├── src/               # Source code directory
│   ├── game/         # Core game mechanics
│   │   ├── card.py   # Card definitions and types
│   │   ├── game.py   # Game state and rules
│   │   └── player.py # Player state and actions
│   ├── simulation/   # Simulation engine
│   └── visualization/# Data visualization
```

### Key Design Principles:
- **Modularity**: Each component (game, simulation, visualization) is independent
- **Single Responsibility**: Each class has a focused purpose
- **Dependency Management**: Clear dependency flow from game → simulation → visualization
- **Type Safety**: Comprehensive type hints throughout the codebase

## 2. Game Mechanics and Implementation

### Card System
- **Number Cards**: Values 0-12
- **Action Cards**:
  - `Freeze`: Immediately ends the player's turn
  - `Deal Three`: Forces player to draw three additional cards
  - `Second Chance`: Prevents one bust, can be saved for later
- **Modifier Cards**:
  - Point modifiers: +2, +4, +6, +8, +10
  - Multiplier: x2

### Player States
```python
class Player:
    has_second_chance: bool  # Has available Second Chance
    is_frozen: bool         # Cannot take more actions
    has_passed: bool        # Voluntarily ended turn
    has_busted: bool        # Exceeded limits
```

### Scoring System
1. Base score: Sum of number cards
2. +15 bonus for collecting exactly 7 unique numbers
3. Modifier cards applied last
4. Busted players score 0

## 3. Simulation Strategy and Statistics

### Monte Carlo Simulation
The simulator runs multiple independent games with configurable parameters:
- Number of players (5-12)
- Number of games (default: 1000)
- Random seed for reproducibility

### AI Strategy
Players use a probability-based decision system:
```python
if num_cards <= 3:
    flip = True
elif num_cards == 4:
    flip = random.random() < 0.7  # 70% chance
elif num_cards == 5:
    flip = random.random() < 0.5  # 50% chance
elif num_cards == 6:
    flip = random.random() < 0.3  # 30% chance
else:
    flip = False
```

### Tracked Statistics
- Winning scores distribution
- Player outcomes (bust/freeze/pass rates)
- Win rates by player position
- Score progression over games
- Card distribution patterns

## 4. Visualization Approaches

### Core Visualization Types

1. **Winning Scores Distribution**
   ```python
   sns.histplot(data=df, x='winning_score', bins=30)
   ```
   Shows the frequency distribution of winning scores, helping understand typical game outcomes.

2. **Player Outcomes**
   ```python
   plt.bar(players, data[outcome], bottom=bottom, label=outcome)
   ```
   Stacked bar chart showing how often each player busts, freezes, or passes.

3. **Win Rates**
   ```python
   sns.barplot(data=df, x='player', y='win_rate')
   ```
   Displays win probability by player position.

4. **Score Progression**
   ```python
   sns.regplot(data=df, x='game_number', y='winning_score')
   ```
   Shows how winning scores trend over multiple games.

### Visualization Features
- Consistent styling using seaborn
- High DPI output (300 dpi)
- Configurable save locations
- Comprehensive labels and titles
- Color schemes optimized for readability

## 5. Development Setup and Tools

### Core Dependencies
```python
numpy>=1.26.0     # Numerical computations
pandas>=2.1.0     # Data manipulation
matplotlib>=3.8.0 # Base plotting
seaborn>=0.13.0   # Statistical visualization
pytest>=7.4.0     # Testing framework
loguru>=0.7.0     # Logging
tqdm>=4.66.0      # Progress bars
```

### Development Environment
- Python 3.13 compatible
- Virtual environment management
- Installable package with setup.py
- Git version control with .gitignore

### Testing Framework
- pytest for unit testing
- Coverage reporting
- Type checking with mypy

### Logging System
- Rotating log files
- Structured logging format
- Configurable log levels
- Performance statistics tracking 