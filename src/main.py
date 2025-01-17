import os
from loguru import logger
from simulation.simulator import Simulator
from visualization.visualizer import Visualizer

def main():
    # Setup logging
    logger.add("simulation.log", rotation="1 day")
    
    # Create output directory for visualizations
    os.makedirs("output", exist_ok=True)
    
    # Initialize simulator and visualizer
    simulator = Simulator(num_players=6, base_seed=42)
    visualizer = Visualizer()
    
    # Run simulations
    logger.info("Starting simulations")
    results_df = simulator.simulate_games(num_games=1000, rounds_per_game=1)
    summary_stats = simulator.get_summary_stats()
    
    # Log summary statistics
    logger.info("\nSummary Statistics:")
    logger.info(f"Total Games: {summary_stats['total_games']}")
    logger.info(f"Average Winning Score: {summary_stats['avg_winning_score']:.2f}")
    logger.info(f"Max Winning Score: {summary_stats['max_winning_score']}")
    logger.info(f"Min Winning Score: {summary_stats['min_winning_score']}")
    
    # Generate visualizations
    logger.info("Generating visualizations")
    
    visualizer.plot_winning_scores_distribution(
        results_df, 
        save_path="output/winning_scores_dist.png"
    )
    
    visualizer.plot_player_outcomes(
        summary_stats, 
        save_path="output/player_outcomes.png"
    )
    
    visualizer.plot_win_rates(
        summary_stats, 
        save_path="output/win_rates.png"
    )
    
    visualizer.plot_score_progression(
        results_df, 
        save_path="output/score_progression.png"
    )
    
    visualizer.create_summary_dashboard(
        results_df, 
        summary_stats, 
        save_path="output/dashboard.png"
    )
    
    logger.info("Simulation and visualization complete!")

if __name__ == "__main__":
    main() 