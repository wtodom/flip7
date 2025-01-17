"""Simulator for running Flip 7 games with player profiles."""
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional
from loguru import logger

from src.game.game import Game
from src.game.player import Player
from src.profiles.profile_loader import PlayerProfile, load_profile

# Default location for player profiles
DEFAULT_PROFILES_DIR = Path(__file__).parent.parent / "profiles" / "data"

@dataclass
class PlayerConfig:
    """Configuration for a player in the simulation."""
    profile_name: str
    position: Optional[int] = None
    
@dataclass
class SimulationConfig:
    """Configuration for running a simulation."""
    num_games: int = 1000
    players: List[PlayerConfig] = field(default_factory=list)
    base_seed: Optional[int] = None
    profiles_dir: Path = DEFAULT_PROFILES_DIR

@dataclass
class ProfileStats:
    """Statistics for a player profile."""
    games_played: int = 0
    games_won: int = 0
    total_score: int = 0
    busts: int = 0
    freezes: int = 0
    passes: int = 0
    
    @property
    def win_rate(self) -> float:
        """Calculate win rate."""
        return self.games_won / max(1, self.games_played)
    
    @property
    def average_score(self) -> float:
        """Calculate average score."""
        return self.total_score / max(1, self.games_played)
    
    @property
    def bust_rate(self) -> float:
        """Calculate bust rate."""
        return self.busts / max(1, self.games_played)
    
    @property
    def freeze_rate(self) -> float:
        """Calculate freeze rate."""
        return self.freezes / max(1, self.games_played)
    
    @property
    def pass_rate(self) -> float:
        """Calculate pass rate."""
        return self.passes / max(1, self.games_played)

class SimulationResults:
    """Results from running a simulation."""
    
    def __init__(self):
        self.total_games: int = 0
        self.profile_stats: Dict[str, ProfileStats] = {}
        self.game_history: List[Dict] = []
    
    def record_game(self, game_number: int, players: Dict[str, Player], winner: str) -> None:
        """Record the results of a game."""
        # Update game history
        game_data = {
            'game_number': game_number,
            'winner': winner,
            'winning_score': players[winner].get_score(),
            'players': {}
        }
        
        # Record player data
        for name, player in players.items():
            profile_name = player.profile.name
            
            # Initialize profile stats if needed
            if profile_name not in self.profile_stats:
                self.profile_stats[profile_name] = ProfileStats()
            
            stats = self.profile_stats[profile_name]
            stats.games_played += 1
            stats.total_score += player.get_score()
            
            if player.has_busted:
                stats.busts += 1
            elif player.is_frozen:
                stats.freezes += 1
            elif player.has_passed:
                stats.passes += 1
                
            if name == winner:
                stats.games_won += 1
            
            # Record player state
            game_data['players'][name] = {
                'profile': profile_name,
                'score': player.get_score(),
                'status': 'bust' if player.has_busted else 'freeze' if player.is_frozen else 'pass' if player.has_passed else 'active'
            }
        
        self.game_history.append(game_data)
        self.total_games += 1

class Simulator:
    """Runs Flip 7 game simulations."""
    
    def __init__(self, config: SimulationConfig):
        """Initialize simulator with configuration."""
        self.config = config
        self.results = SimulationResults()
        
        # Set random seed if provided
        if config.base_seed is not None:
            random.seed(config.base_seed)
        
        # Load player profiles
        self.profiles: Dict[str, PlayerProfile] = {}
        for player_config in config.players:
            if player_config.profile_name not in self.profiles:
                profile_path = config.profiles_dir / f"{player_config.profile_name.lower().replace(' ', '_')}.yaml"
                self.profiles[player_config.profile_name] = load_profile(profile_path)
    
    def run_simulation(self) -> SimulationResults:
        """Run the simulation for the configured number of games."""
        logger.info(f"Starting simulation with {len(self.config.players)} players")
        
        for game_number in range(self.config.num_games):
            # Create players for this game
            players = {}
            for i, player_config in enumerate(self.config.players):
                position = player_config.position if player_config.position is not None else i
                profile = self.profiles[player_config.profile_name]
                players[f"Player_{position}"] = Player(profile)
            
            # Run game
            game = Game(list(players.values()))
            winner = f"Player_{game.play_game()}"
            
            # Record results
            self.results.record_game(game_number, players, winner)
            
            if (game_number + 1) % 100 == 0:
                logger.info(f"Completed {game_number + 1} games")
        
        logger.info("Simulation complete!")
        return self.results 