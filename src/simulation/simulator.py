from typing import List, Dict, Any
import random
from tqdm import tqdm
import pandas as pd
from loguru import logger

from src.game.game import Game

class Simulator:
    """Runs multiple games of Flip 7 and collects statistics."""
    
    def __init__(self, num_players: int = 5, base_seed: int = None):
        """Initialize simulator with number of players and optional base seed."""
        if not 5 <= num_players <= 12:
            raise ValueError("Number of players must be between 5 and 12")
        
        self.num_players = num_players
        self.base_seed = base_seed
        self.stats: List[Dict[str, Any]] = []
    
    def _generate_player_names(self) -> List[str]:
        """Generate player names for a game."""
        return [f"Player_{i+1}" for i in range(self.num_players)]
    
    def _simulate_round(self, game: Game) -> Dict:
        """Simulate a single round of the game."""
        game.start_round()
        
        while not game.is_round_over():
            player = game.players[game.current_player_idx]
            if player.is_frozen or player.has_passed or player.has_busted:
                game.play_turn(False)
                continue
            
            # Simple strategy: 
            # - Always flip if 3 or fewer cards
            # - 70% chance to flip if 4 cards
            # - 50% chance to flip if 5 cards
            # - 30% chance to flip if 6 cards
            # - Never flip if 6+ cards unless we have Second Chance
            num_cards = len(player.number_cards)
            should_flip = False
            
            if num_cards <= 3:
                should_flip = True
            elif num_cards == 4:
                should_flip = random.random() < 0.7
            elif num_cards == 5:
                should_flip = random.random() < 0.5
            elif num_cards == 6:
                should_flip = random.random() < 0.3 or player.has_second_chance
            
            if game.play_turn(should_flip):
                break  # Someone got 7 unique numbers
        
        return game.get_round_results()
    
    def simulate_games(self, num_games: int, rounds_per_game: int = 1) -> pd.DataFrame:
        """
        Simulate multiple games and collect statistics.
        Returns a DataFrame with the results.
        """
        logger.info(f"Simulating {num_games} games with {rounds_per_game} rounds each")
        
        for game_num in tqdm(range(num_games)):
            seed = None if self.base_seed is None else self.base_seed + game_num
            game = Game(self._generate_player_names(), seed)
            
            for _ in range(rounds_per_game):
                round_results = self._simulate_round(game)
                round_results['game'] = game_num
                self.stats.append(round_results)
        
        return pd.DataFrame(self.stats)
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Calculate summary statistics from the simulations."""
        if not self.stats:
            raise ValueError("No simulations have been run yet")
        
        df = pd.DataFrame(self.stats)
        
        summary = {
            'total_games': df['game'].nunique(),
            'total_rounds': len(df),
            'avg_winning_score': df['winning_score'].mean(),
            'max_winning_score': df['winning_score'].max(),
            'min_winning_score': df['winning_score'].min(),
        }
        
        # Calculate win rates
        all_players = set()
        for status_dict in df['status'].values:
            all_players.update(status_dict.keys())
        
        win_counts = {player: 0 for player in all_players}
        total_games = df['game'].nunique()
        
        for _, row in df.iterrows():
            if row['winner']:
                win_counts[row['winner']] += 1
        
        summary['win_rates'] = {
            player: count / total_games 
            for player, count in win_counts.items()
        }
        
        # Calculate bust/freeze/pass rates
        status_counts = {player: {'Busted': 0, 'Frozen': 0, 'Passed': 0} 
                        for player in all_players}
        
        for _, row in df.iterrows():
            for player, status in row['status'].items():
                if status in status_counts[player]:
                    status_counts[player][status] += 1
        
        summary['player_stats'] = {
            player: {
                status: count / total_games
                for status, count in counts.items()
            }
            for player, counts in status_counts.items()
        }
        
        return summary 