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
        # Set up the dark theme with colorblind-friendly colors
        plt.style.use('dark_background')
        # Color palette based on ColorBrewer's colorblind-friendly schemes
        # Modified pink (#e7298a -> #c45c93) to be less bright while maintaining contrast
        self.colors = ['#1b9e77', '#d95f02', '#7570b3', '#c45c93', '#66a61e']
        sns.set_palette(self.colors)
        
        # Configure general plot styling
        plt.rcParams.update({
            'axes.facecolor': '#2e2e2e',
            'figure.facecolor': '#1c1c1c',
            'grid.color': '#404040',
            'text.color': '#ffffff',
            'axes.labelcolor': '#ffffff',
            'xtick.color': '#ffffff',
            'ytick.color': '#ffffff',
            'axes.grid': True,
            'grid.alpha': 0.3,
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'legend.facecolor': '#2e2e2e',
            'legend.edgecolor': '#404040',
            'legend.fontsize': 10,
            'figure.titlesize': 16
        })
    
    def _save_or_show(self, save_path: Optional[str] = None) -> None:
        """Helper method to either save or display a figure."""
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='#1c1c1c')
            plt.close()
        else:
            plt.show()
    
    def plot_winning_scores_distribution(self, save_path: Optional[str] = None) -> None:
        """Plot the distribution of winning scores."""
        plt.figure(figsize=(10, 6))
        
        scores = [game['winning_score'] for game in self.results.game_history]
        sns.histplot(scores, bins=20, color=self.colors[0], alpha=0.7)
        
        plt.title('Distribution of Winning Scores', pad=20)
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
        
        ax = outcome_props.plot(kind='bar', stacked=True, width=0.8)
        plt.title('Player Outcomes by Profile', pad=20)
        plt.xlabel('Profile')
        plt.ylabel('Proportion')
        plt.legend(title='Outcome', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels
        for c in ax.containers:
            ax.bar_label(c, fmt='%.2f', label_type='center')
        
        self._save_or_show(save_path)
    
    def plot_win_rates(self, save_path: Optional[str] = None) -> None:
        """Plot win rates for each profile."""
        plt.figure(figsize=(10, 6))
        
        win_rates = {name: stats.win_rate 
                    for name, stats in self.results.profile_stats.items()}
        
        ax = plt.gca()
        bars = plt.bar(win_rates.keys(), win_rates.values(), 
                      color=self.colors[0], alpha=0.8)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2%}',
                   ha='center', va='bottom')
        
        plt.title('Win Rates by Profile', pad=20)
        plt.xlabel('Profile')
        plt.ylabel('Win Rate')
        plt.xticks(rotation=45, ha='right')
        
        self._save_or_show(save_path)
    
    def plot_score_progression(self, save_path: Optional[str] = None) -> None:
        """Plot how scores progress over games."""
        plt.figure(figsize=(12, 6))
        
        df = pd.DataFrame([{
            'game_number': game['game_number'],
            'winning_score': game['winning_score']
        } for game in self.results.game_history])
        
        sns.regplot(data=df, x='game_number', y='winning_score',
                   scatter=True, color=self.colors[0],
                   scatter_kws={'alpha': 0.3, 'color': self.colors[0]},
                   line_kws={'color': self.colors[1]})
        
        plt.title('Score Progression Over Games', pad=20)
        plt.xlabel('Game Number')
        plt.ylabel('Winning Score')
        
        self._save_or_show(save_path)
    
    def create_summary_dashboard(self, save_path: Optional[str] = None) -> None:
        """Create a comprehensive dashboard of game statistics."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Game Statistics Dashboard', fontsize=16, y=0.95)
        
        # Win rates
        win_rates = {name: stats.win_rate 
                    for name, stats in self.results.profile_stats.items()}
        bars = ax1.bar(win_rates.keys(), win_rates.values(), color=self.colors[0])
        ax1.set_title('Win Rates by Profile', pad=15)
        ax1.set_ylabel('Win Rate')
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2%}',
                    ha='center', va='bottom')
        
        # Score distribution
        scores = [game['winning_score'] for game in self.results.game_history]
        sns.histplot(scores, bins=20, ax=ax2, color=self.colors[1], alpha=0.7)
        ax2.set_title('Winning Score Distribution', pad=15)
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
        outcome_props.plot(kind='bar', stacked=True, ax=ax3, width=0.8)
        ax3.set_title('Outcome Distribution', pad=15)
        ax3.set_xlabel('Profile')
        ax3.set_ylabel('Proportion')
        ax3.legend(title='Outcome', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax3.tick_params(axis='x', rotation=45)
        plt.setp(ax3.get_xticklabels(), ha='right')
        
        # Score progression
        df_scores = pd.DataFrame([{
            'game_number': game['game_number'],
            'winning_score': game['winning_score']
        } for game in self.results.game_history])
        sns.regplot(data=df_scores, x='game_number', y='winning_score',
                   scatter=True, ax=ax4,
                   scatter_kws={'alpha': 0.3, 'color': self.colors[2]},
                   line_kws={'color': self.colors[3]})
        ax4.set_title('Score Progression', pad=15)
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
        fig.suptitle(f'Head-to-Head: {profile1} vs {profile2}', fontsize=16, y=0.95)
        
        # Win rate comparison
        win_rates = df.groupby('profile')['won'].mean()
        bars = sns.barplot(x=win_rates.index, y=win_rates.values, ax=ax1,
                          palette=[self.colors[0], self.colors[1]])
        ax1.set_title('Win Rate Comparison', pad=15)
        ax1.set_ylabel('Win Rate')
        
        # Add value labels
        for i, bar in enumerate(ax1.patches):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2%}',
                    ha='center', va='bottom')
        
        # Score distribution comparison
        sns.violinplot(data=df, x='profile', y='score', ax=ax2,
                      palette=[self.colors[0], self.colors[1]])
        ax2.set_title('Score Distribution Comparison', pad=15)
        ax2.set_ylabel('Score')
        
        # Outcome type comparison
        outcome_counts = pd.crosstab(df['profile'], df['status'])
        outcome_props = outcome_counts.div(outcome_counts.sum(axis=1), axis=0)
        outcome_props.plot(kind='bar', stacked=True, ax=ax3, width=0.8)
        ax3.set_title('Outcome Type Comparison', pad=15)
        ax3.set_ylabel('Proportion')
        ax3.legend(title='Outcome', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Score evolution comparison
        df['rolling_score'] = df.groupby('profile')['score'].transform(
            lambda x: x.rolling(window=50, min_periods=1).mean()
        )
        sns.lineplot(data=df, x='game_number', y='rolling_score',
                    hue='profile', ax=ax4,
                    palette=[self.colors[0], self.colors[1]])
        ax4.set_title('Score Evolution', pad=15)
        ax4.set_ylabel('Average Score (50-game rolling)')
        
        plt.tight_layout()
        self._save_or_show(save_path) 