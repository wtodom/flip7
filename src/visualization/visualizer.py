"""Visualization module for Flip 7 simulation results."""
import os
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ..simulation.simulator import SimulationResults, ProfileStats

class Visualizer:
    """Creates visualizations from simulation results."""
    
    def __init__(self, results: SimulationResults):
        """Initialize visualizer with simulation results."""
        self.results = results
        self.style = 'seaborn'
        plt.style.use(self.style)
    
    def _create_profile_dataframe(self) -> pd.DataFrame:
        """Convert profile statistics to a DataFrame."""
        data = []
        for profile_name, stats in self.results.profile_stats.items():
            data.append({
                'profile': profile_name,
                'games_played': stats.games_played,
                'win_rate': stats.win_rate,
                'average_score': stats.average_score,
                'bust_rate': stats.bust_rate,
                'freeze_rate': stats.freeze_rate,
                'pass_rate': stats.pass_rate,
                'lucky_cards_per_game': stats.lucky_cards_seen / max(1, stats.games_played),
                'superstition_cards_per_game': stats.superstition_cards_seen / max(1, stats.games_played),
                'average_risk': np.mean(stats.risk_adjustments) if stats.risk_adjustments else 0
            })
        return pd.DataFrame(data)
    
    def _create_game_history_dataframe(self) -> pd.DataFrame:
        """Convert game history to a DataFrame."""
        data = []
        for game in self.results.game_history:
            for player_name, player_data in game['players'].items():
                data.append({
                    'game_number': game['game_number'],
                    'player': player_name,
                    'profile': player_data['profile'],
                    'score': player_data['score'],
                    'status': player_data['status'],
                    'won': game['winner'] == player_name
                })
        return pd.DataFrame(data)
    
    def plot_profile_comparison(self, save_path: Optional[str] = None) -> None:
        """Create a comprehensive profile comparison dashboard."""
        df = self._create_profile_dataframe()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Profile Performance Comparison', fontsize=16)
        
        # Win rates
        sns.barplot(data=df, x='profile', y='win_rate', ax=ax1)
        ax1.set_title('Win Rates by Profile')
        ax1.set_ylabel('Win Rate')
        ax1.tick_params(axis='x', rotation=45)
        
        # Average scores
        sns.boxplot(data=self._create_game_history_dataframe(), 
                   x='profile', y='score', ax=ax2)
        ax2.set_title('Score Distribution by Profile')
        ax2.set_ylabel('Score')
        ax2.tick_params(axis='x', rotation=45)
        
        # Outcome rates
        outcome_data = pd.melt(df, 
                             id_vars=['profile'],
                             value_vars=['bust_rate', 'freeze_rate', 'pass_rate'],
                             var_name='outcome',
                             value_name='rate')
        sns.barplot(data=outcome_data, x='profile', y='rate', hue='outcome', ax=ax3)
        ax3.set_title('Outcome Rates by Profile')
        ax3.set_ylabel('Rate')
        ax3.tick_params(axis='x', rotation=45)
        
        # Risk levels
        sns.scatterplot(data=df, x='average_risk', y='win_rate', 
                       size='games_played', hue='profile', ax=ax4)
        ax4.set_title('Risk vs Win Rate')
        ax4.set_xlabel('Average Risk Level')
        ax4.set_ylabel('Win Rate')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    def plot_strategy_evolution(self, save_path: Optional[str] = None) -> None:
        """Plot how strategies evolve over games."""
        df = self._create_game_history_dataframe()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        fig.suptitle('Strategy Evolution Over Games', fontsize=16)
        
        # Win rate evolution
        df['rolling_win_rate'] = df.groupby('profile')['won'].transform(
            lambda x: x.rolling(window=50, min_periods=1).mean()
        )
        
        sns.lineplot(data=df, x='game_number', y='rolling_win_rate', 
                    hue='profile', ax=ax1)
        ax1.set_title('Win Rate Evolution (50-game rolling average)')
        ax1.set_ylabel('Win Rate')
        
        # Score evolution
        df['rolling_score'] = df.groupby('profile')['score'].transform(
            lambda x: x.rolling(window=50, min_periods=1).mean()
        )
        
        sns.lineplot(data=df, x='game_number', y='rolling_score',
                    hue='profile', ax=ax2)
        ax2.set_title('Score Evolution (50-game rolling average)')
        ax2.set_ylabel('Average Score')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    def plot_personality_impact(self, save_path: Optional[str] = None) -> None:
        """Plot the impact of personality traits (lucky cards and superstitions)."""
        df = self._create_profile_dataframe()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle('Impact of Personality Traits', fontsize=16)
        
        # Lucky cards impact
        sns.scatterplot(data=df, x='lucky_cards_per_game', y='win_rate',
                       size='games_played', hue='profile', ax=ax1)
        ax1.set_title('Lucky Cards Impact')
        ax1.set_xlabel('Lucky Cards Seen Per Game')
        ax1.set_ylabel('Win Rate')
        
        # Superstitions impact
        sns.scatterplot(data=df, x='superstition_cards_per_game', y='win_rate',
                       size='games_played', hue='profile', ax=ax2)
        ax2.set_title('Superstitions Impact')
        ax2.set_xlabel('Superstition Cards Seen Per Game')
        ax2.set_ylabel('Win Rate')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    def plot_head_to_head(self, profile1: str, profile2: str, 
                         save_path: Optional[str] = None) -> None:
        """Create head-to-head comparison between two profiles."""
        df = self._create_game_history_dataframe()
        df_filtered = df[df['profile'].isin([profile1, profile2])]
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Head-to-Head: {profile1} vs {profile2}', fontsize=16)
        
        # Win rate comparison
        win_rates = df_filtered.groupby('profile')['won'].mean()
        sns.barplot(x=win_rates.index, y=win_rates.values, ax=ax1)
        ax1.set_title('Win Rate Comparison')
        ax1.set_ylabel('Win Rate')
        
        # Score distribution comparison
        sns.violinplot(data=df_filtered, x='profile', y='score', ax=ax2)
        ax2.set_title('Score Distribution Comparison')
        ax2.set_ylabel('Score')
        
        # Outcome type comparison
        outcome_counts = pd.crosstab(df_filtered['profile'], df_filtered['status'])
        outcome_props = outcome_counts.div(outcome_counts.sum(axis=1), axis=0)
        outcome_props.plot(kind='bar', stacked=True, ax=ax3)
        ax3.set_title('Outcome Type Comparison')
        ax3.set_ylabel('Proportion')
        ax3.legend(title='Outcome')
        
        # Score evolution comparison
        df_filtered['rolling_score'] = df_filtered.groupby('profile')['score'].transform(
            lambda x: x.rolling(window=50, min_periods=1).mean()
        )
        sns.lineplot(data=df_filtered, x='game_number', y='rolling_score',
                    hue='profile', ax=ax4)
        ax4.set_title('Score Evolution')
        ax4.set_ylabel('Average Score (50-game rolling)')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    def create_profile_report(self, output_dir: str) -> None:
        """Create a complete set of profile analysis visualizations."""
        os.makedirs(output_dir, exist_ok=True)
        
        # Overall profile comparison
        self.plot_profile_comparison(
            os.path.join(output_dir, 'profile_comparison.png')
        )
        
        # Strategy evolution
        self.plot_strategy_evolution(
            os.path.join(output_dir, 'strategy_evolution.png')
        )
        
        # Personality impact
        self.plot_personality_impact(
            os.path.join(output_dir, 'personality_impact.png')
        )
        
        # Head-to-head comparisons for each pair of profiles
        profiles = list(self.results.profile_stats.keys())
        for i in range(len(profiles)):
            for j in range(i + 1, len(profiles)):
                self.plot_head_to_head(
                    profiles[i],
                    profiles[j],
                    os.path.join(output_dir, f'head_to_head_{profiles[i]}_{profiles[j]}.png')
                ) 