import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any
import numpy as np

class Visualizer:
    """Creates visualizations of Flip 7 game statistics."""
    
    def __init__(self):
        """Initialize visualizer with default style settings."""
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def plot_winning_scores_distribution(self, df: pd.DataFrame, 
                                       save_path: str = None):
        """Plot distribution of winning scores."""
        plt.figure(figsize=(12, 6))
        sns.histplot(data=df, x='winning_score', bins=30)
        plt.title('Distribution of Winning Scores', pad=20)
        plt.xlabel('Winning Score')
        plt.ylabel('Frequency')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    def plot_player_outcomes(self, summary: Dict[str, Any], 
                           save_path: str = None):
        """Plot stacked bar chart of player outcomes (bust/freeze/pass rates)."""
        # Prepare data
        players = list(summary['player_stats'].keys())
        outcomes = ['Busted', 'Frozen', 'Passed']
        data = {
            outcome: [summary['player_stats'][p][outcome] for p in players]
            for outcome in outcomes
        }
        
        # Create stacked bar chart
        plt.figure(figsize=(12, 6))
        bottom = np.zeros(len(players))
        
        for outcome in outcomes:
            plt.bar(players, data[outcome], bottom=bottom, label=outcome)
            bottom += data[outcome]
        
        plt.title('Player Outcomes by Percentage', pad=20)
        plt.xlabel('Player')
        plt.ylabel('Percentage of Games')
        plt.legend(title='Outcome')
        plt.xticks(rotation=45)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    def plot_win_rates(self, summary: Dict[str, Any], 
                      save_path: str = None):
        """Plot win rates for each player."""
        plt.figure(figsize=(12, 6))
        players = list(summary['win_rates'].keys())
        rates = list(summary['win_rates'].values())
        
        sns.barplot(x=players, y=rates)
        plt.title('Win Rates by Player', pad=20)
        plt.xlabel('Player')
        plt.ylabel('Win Rate')
        plt.xticks(rotation=45)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    def plot_score_progression(self, df: pd.DataFrame, 
                             save_path: str = None):
        """Plot how winning scores progress over games."""
        plt.figure(figsize=(12, 6))
        
        sns.regplot(data=df, x='game', y='winning_score', 
                   scatter=True, scatter_kws={'alpha':0.5})
        plt.title('Winning Score Progression Over Games', pad=20)
        plt.xlabel('Game Number')
        plt.ylabel('Winning Score')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    def create_summary_dashboard(self, df: pd.DataFrame, 
                               summary: Dict[str, Any], 
                               save_path: str = None):
        """Create a dashboard with multiple plots."""
        plt.figure(figsize=(20, 15))
        
        # Winning scores distribution
        plt.subplot(2, 2, 1)
        sns.histplot(data=df, x='winning_score', bins=30)
        plt.title('Distribution of Winning Scores')
        
        # Player outcomes
        plt.subplot(2, 2, 2)
        players = list(summary['player_stats'].keys())
        outcomes = ['Busted', 'Frozen', 'Passed']
        bottom = np.zeros(len(players))
        for outcome in outcomes:
            data = [summary['player_stats'][p][outcome] for p in players]
            plt.bar(players, data, bottom=bottom, label=outcome)
            bottom += data
        plt.title('Player Outcomes')
        plt.legend(title='Outcome')
        plt.xticks(rotation=45)
        
        # Win rates
        plt.subplot(2, 2, 3)
        players = list(summary['win_rates'].keys())
        rates = list(summary['win_rates'].values())
        sns.barplot(x=players, y=rates)
        plt.title('Win Rates by Player')
        plt.xticks(rotation=45)
        
        # Score progression
        plt.subplot(2, 2, 4)
        sns.regplot(data=df, x='game', y='winning_score', 
                   scatter=True, scatter_kws={'alpha':0.5})
        plt.title('Score Progression')
        
        plt.tight_layout(pad=3.0)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show() 