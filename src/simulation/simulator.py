"""Simulation engine for Flip 7."""
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Union
import random
from tqdm import tqdm
from loguru import logger

from ..game.game import Game
from ..game.player import Player
from ..profiles.profile_loader import PlayerProfile, load_profile, load_all_profiles

@dataclass
class PlayerConfig:
    """Configuration for a player in the simulation."""
    position: Optional[int] = None  # If None, position is random
    profile_name: Optional[str] = None  # If None, uses default AI

@dataclass
class SimulationConfig:
    """Configuration for a simulation run."""
    num_games: int = 1000
    num_players: int = 6
    base_seed: Optional[int] = None
    player_configs: Optional[List[PlayerConfig]] = None
    profiles_dir: Optional[Path] = None

@dataclass
class ProfileStats:
    """Statistics for a specific profile."""
    games_played: int = 0
    games_won: int = 0
    total_score: int = 0
    busts: int = 0
    freezes: int = 0
    passes: int = 0
    lucky_cards_seen: int = 0
    superstition_cards_seen: int = 0
    risk_adjustments: List[float] = None
    
    def __post_init__(self):
        if self.risk_adjustments is None:
            self.risk_adjustments = []
    
    @property
    def win_rate(self) -> float:
        """Calculate win rate for this profile."""
        return self.games_won / max(1, self.games_played)
    
    @property
    def average_score(self) -> float:
        """Calculate average score for this profile."""
        return self.total_score / max(1, self.games_played)
    
    @property
    def bust_rate(self) -> float:
        """Calculate bust rate for this profile."""
        return self.busts / max(1, self.games_played)
    
    @property
    def freeze_rate(self) -> float:
        """Calculate freeze rate for this profile."""
        return self.freezes / max(1, self.games_played)
    
    @property
    def pass_rate(self) -> float:
        """Calculate pass rate for this profile."""
        return self.passes / max(1, self.games_played)

class SimulationResults:
    """Results from a simulation run."""
    
    def __init__(self):
        self.total_games = 0
        self.profile_stats: Dict[str, ProfileStats] = {}
        self.game_history: List[Dict] = []
    
    def add_game_result(self, game_number: int, winner: Player, players: List[Player]):
        """Add results from a single game."""
        self.total_games += 1
        
        # Record game result
        game_result = {
            'game_number': game_number,
            'winner': winner.name,
            'winning_score': winner.get_score(),
            'players': {}
        }
        
        # Update stats for each player
        for player in players:
            profile_name = player.profile.name if player.profile else 'default'
            
            # Initialize profile stats if needed
            if profile_name not in self.profile_stats:
                self.profile_stats[profile_name] = ProfileStats()
            
            stats = self.profile_stats[profile_name]
            stats.games_played += 1
            
            if player == winner:
                stats.games_won += 1
            
            stats.total_score += player.get_score()
            
            if player.has_busted:
                stats.busts += 1
            elif player.is_frozen:
                stats.freezes += 1
            elif player.has_passed:
                stats.passes += 1
            
            # Record strategy adaptations if available
            if player.strategy:
                stats.lucky_cards_seen += player.strategy.current_game_state['lucky_cards_seen']
                stats.superstition_cards_seen += player.strategy.current_game_state['superstition_cards_seen']
                stats.risk_adjustments.append(player.strategy.current_game_state['last_decision_risk'])
            
            # Record player details
            game_result['players'][player.name] = {
                'profile': profile_name,
                'score': player.get_score(),
                'status': 'busted' if player.has_busted else 'frozen' if player.is_frozen else 'passed' if player.has_passed else 'active'
            }
        
        self.game_history.append(game_result)

class Simulator:
    """Runs simulations of Flip 7 games."""
    
    def __init__(self, config: SimulationConfig):
        """Initialize the simulator with the given configuration."""
        self.config = config
        self.results = SimulationResults()
        
        # Load profiles if directory specified
        self.available_profiles: Dict[str, PlayerProfile] = {}
        if config.profiles_dir:
            for profile in load_all_profiles(config.profiles_dir):
                self.available_profiles[profile.name] = profile
    
    def _create_players(self) -> List[Player]:
        """Create players for a game based on configuration."""
        players = []
        used_positions = set()
        
        # Create configured players first
        if self.config.player_configs:
            for player_config in self.config.player_configs:
                # Get profile if specified
                profile = None
                if player_config.profile_name:
                    if player_config.profile_name not in self.available_profiles:
                        raise ValueError(f"Profile not found: {player_config.profile_name}")
                    profile = self.available_profiles[player_config.profile_name]
                
                # Get position
                position = player_config.position
                if position is not None:
                    if position in used_positions:
                        raise ValueError(f"Duplicate position: {position}")
                    if not 0 <= position < self.config.num_players:
                        raise ValueError(f"Invalid position: {position}")
                    used_positions.add(position)
                
                # Create player
                player = Player(
                    name=f"Player_{len(players) + 1}",
                    profile=profile
                )
                
                if position is not None:
                    # Insert at specific position
                    while len(players) < position:
                        players.append(None)
                    players.insert(position, player)
                else:
                    # Add to first available position
                    pos = 0
                    while pos < len(players) and players[pos] is not None:
                        pos += 1
                    if pos < len(players):
                        players[pos] = player
                    else:
                        players.append(player)
        
        # Fill remaining positions with default players
        while len(players) < self.config.num_players:
            players.append(Player(
                name=f"Player_{len(players) + 1}"
            ))
        
        # Remove any None placeholders
        players = [p for p in players if p is not None]
        
        return players
    
    def run(self) -> SimulationResults:
        """Run the simulation and return results."""
        logger.info(f"Starting simulation of {self.config.num_games} games with {self.config.num_players} players")
        
        if self.config.base_seed is not None:
            random.seed(self.config.base_seed)
        
        for game_number in tqdm(range(self.config.num_games)):
            # Create new set of players for each game
            players = self._create_players()
            
            # Create and play game
            game = Game(
                players=players,
                seed=self.config.base_seed + game_number if self.config.base_seed else None
            )
            
            winner = game.play()
            
            # Record results
            self.results.add_game_result(game_number, winner, players)
        
        logger.info("Simulation complete")
        return self.results 