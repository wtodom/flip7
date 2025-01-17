"""Visualization module for Flip 7 simulation results."""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Optional

from src.simulation.simulator import SimulationResults

class Visualizer:
    """Creates visualizations of simulation results."""
    
    def __init__(self, results: SimulationResults):
        """Initialize visualizer with simulation results."""
        self.results = results
        # Set up the style
        sns.set_theme(style="darkgrid")
        sns.set_palette("husl")
        
    def _save_or_show(self, save_path: Optional[str] = None) -> None:
        """Helper method to either save or display a figure."""
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    def plot_winning_scores_distribution(self, save_path: Optional[str] = None) -> None:
        """Plot the distribution of winning scores."""
        plt.figure(figsize=(10, 6))
        
        scores = [game['winning_score'] for game in self.results.game_history]
        sns.histplot(scores, bins=20)
        
        plt.title('Distribution of Winning Scores')
        plt.xlabel('Score')
        plt.ylabel('Count')
        
        self._save_or_show(save_path)
    
    def plot_player_outcomes(self, save_path: Optional[str] = None) -> None:
        """Plot the distribution of player outcomes (bust/freeze/pass)."""
        plt.figure(figsize=(12, 6))
        
        outcomes = []
        for game in self.results.game_history:
            for player_data in game['players'].values():
                outcomes.append({
                    'profile': player_data['profile'],
                    'outcome': player_data['status']
                })
        
        df = pd.DataFrame(outcomes)
        outcome_counts = pd.crosstab(df['profile'], df['outcome'])
        outcome_props = outcome_counts.div(outcome_counts.sum(axis=1), axis=0)
        
        outcome_props.plot(kind='bar', stacked=True)
        plt.title('Player Outcomes by Profile')
        plt.xlabel('Profile')
        plt.ylabel('Proportion')
        plt.legend(title='Outcome')
        plt.xticks(rotation=45)
        
        self._save_or_show(save_path)
    
    def plot_win_rates(self, save_path: Optional[str] = None) -> None:
        """Plot win rates for each profile."""
        plt.figure(figsize=(10, 6))
        
        win_rates = {name: stats.win_rate 
                    for name, stats in self.results.profile_stats.items()}
        
        plt.bar(win_rates.keys(), win_rates.values())
        plt.title('Win Rates by Profile')
        plt.xlabel('Profile')
        plt.ylabel('Win Rate')
        plt.xticks(rotation=45)
        
        self._save_or_show(save_path)
    
    def plot_score_progression(self, save_path: Optional[str] = None) -> None:
        """Plot how scores progress over games."""
        plt.figure(figsize=(12, 6))
        
        df = pd.DataFrame([{
            'game_number': game['game_number'],
            'winning_score': game['winning_score']
        } for game in self.results.game_history])
        
        sns.regplot(data=df, x='game_number', y='winning_score',
                   scatter=True, scatter_kws={'alpha': 0.5})
        
        plt.title('Score Progression Over Games')
        plt.xlabel('Game Number')
        plt.ylabel('Winning Score')
        
        self._save_or_show(save_path)
    
    def create_summary_dashboard(self, save_path: Optional[str] = None) -> None:
        """Create a comprehensive dashboard of game statistics."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Game Statistics Dashboard', fontsize=16)
        
        # Win rates
        win_rates = {name: stats.win_rate 
                    for name, stats in self.results.profile_stats.items()}
        ax1.bar(win_rates.keys(), win_rates.values())
        ax1.set_title('Win Rates by Profile')
        ax1.set_ylabel('Win Rate')
        ax1.tick_params(axis='x', rotation=45)
        
        # Score distribution
        scores = [game['winning_score'] for game in self.results.game_history]
        sns.histplot(scores, bins=20, ax=ax2)
        ax2.set_title('Winning Score Distribution')
        ax2.set_xlabel('Score')
        ax2.set_ylabel('Count')
        
        # Outcome rates
        outcomes = []
        for game in self.results.game_history:
            for player_data in game['players'].values():
                outcomes.append({
                    'profile': player_data['profile'],
                    'outcome': player_data['status']
                })
        df = pd.DataFrame(outcomes)
        outcome_counts = pd.crosstab(df['profile'], df['outcome'])
        outcome_props = outcome_counts.div(outcome_counts.sum(axis=1), axis=0)
        outcome_props.plot(kind='bar', stacked=True, ax=ax3)
        ax3.set_title('Outcome Distribution')
        ax3.set_xlabel('Profile')
        ax3.set_ylabel('Proportion')
        ax3.legend(title='Outcome')
        ax3.tick_params(axis='x', rotation=45)
        
        # Score progression
        df_scores = pd.DataFrame([{
            'game_number': game['game_number'],
            'winning_score': game['winning_score']
        } for game in self.results.game_history])
        sns.regplot(data=df_scores, x='game_number', y='winning_score',
                   scatter=True, scatter_kws={'alpha': 0.5}, ax=ax4)
        ax4.set_title('Score Progression')
        ax4.set_xlabel('Game Number')
        ax4.set_ylabel('Winning Score')
        
        plt.tight_layout()
        self._save_or_show(save_path)
    
    def plot_head_to_head(self, profile1: str, profile2: str, 
                         save_path: Optional[str] = None) -> None:
        """Create head-to-head comparison between two profiles."""
        df = pd.DataFrame([{
            'game_number': game['game_number'],
            'profile': player_data['profile'],
            'score': player_data['score'],
            'status': player_data['status'],
            'won': game['winner'] == player_name
        } for game in self.results.game_history
          for player_name, player_data in game['players'].items()
          if player_data['profile'] in [profile1, profile2]])
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Head-to-Head: {profile1} vs {profile2}', fontsize=16)
        
        # Win rate comparison
        win_rates = df.groupby('profile')['won'].mean()
        sns.barplot(x=win_rates.index, y=win_rates.values, ax=ax1)
        ax1.set_title('Win Rate Comparison')
        ax1.set_ylabel('Win Rate')
        
        # Score distribution comparison
        sns.violinplot(data=df, x='profile', y='score', ax=ax2)
        ax2.set_title('Score Distribution Comparison')
        ax2.set_ylabel('Score')
        
        # Outcome type comparison
        outcome_counts = pd.crosstab(df['profile'], df['status'])
        outcome_props = outcome_counts.div(outcome_counts.sum(axis=1), axis=0)
        outcome_props.plot(kind='bar', stacked=True, ax=ax3)
        ax3.set_title('Outcome Type Comparison')
        ax3.set_ylabel('Proportion')
        ax3.legend(title='Outcome')
        
        # Score evolution comparison
        df['rolling_score'] = df.groupby('profile')['score'].transform(
            lambda x: x.rolling(window=50, min_periods=1).mean()
        )
        sns.lineplot(data=df, x='game_number', y='rolling_score',
                    hue='profile', ax=ax4)
        ax4.set_title('Score Evolution')
        ax4.set_ylabel('Average Score (50-game rolling)')
        
        plt.tight_layout()
        self._save_or_show(save_path) 