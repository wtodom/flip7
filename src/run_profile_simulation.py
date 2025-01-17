"""Run a simulation with player profiles."""
import os
from pathlib import Path
from loguru import logger

from simulation.simulator import (
    Simulator, SimulationConfig, PlayerConfig, DEFAULT_PROFILES_DIR
)
from visualization.visualizer import Visualizer

def main():
    """Run simulation with configured profiles."""
    # Set up logging
    logger.add("simulation.log", rotation="1 day")
    logger.info("Starting simulation with profiles")

    # Create output directory for visualizations
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Verify profiles directory exists
    if not DEFAULT_PROFILES_DIR.exists():
        raise FileNotFoundError(f"Profiles directory not found: {DEFAULT_PROFILES_DIR}")

    # Configure simulation
    config = SimulationConfig(
        num_games=1000,
        num_players=6,
        base_seed=42,
        player_configs=[
            PlayerConfig(position=0, profile_name="Cautious Carl"),
            PlayerConfig(position=1, profile_name="Risk Taker Rachel"),
            PlayerConfig(position=2, profile_name="Balanced Betty"),
            PlayerConfig(position=3, profile_name="Superstitious Sam"),
            PlayerConfig(position=4, profile_name="YOLO Yuki"),
        ]
    )

    try:
        # Initialize simulator and visualizer
        simulator = Simulator(config)
        visualizer = Visualizer()

        # Run simulation
        logger.info("Running simulation...")
        results = simulator.run()

        # Log summary statistics
        logger.info(f"Total games: {results.total_games}")
        for profile_name, stats in results.profile_stats.items():
            logger.info(f"\nProfile: {profile_name}")
            logger.info(f"Games played: {stats.games_played}")
            logger.info(f"Win rate: {stats.win_rate:.2%}")
            logger.info(f"Average score: {stats.average_score:.1f}")
            logger.info(f"Bust rate: {stats.bust_rate:.2%}")
            logger.info(f"Freeze rate: {stats.freeze_rate:.2%}")
            logger.info(f"Pass rate: {stats.pass_rate:.2%}")

        # Generate visualizations
        logger.info("Generating visualizations...")
        visualizer.plot_winning_scores_distribution(save_path="output/winning_scores_dist.png")
        visualizer.plot_player_outcomes(save_path="output/player_outcomes.png")
        visualizer.plot_win_rates(save_path="output/win_rates.png")
        visualizer.plot_score_progression(save_path="output/score_progression.png")
        visualizer.create_summary_dashboard(save_path="output/dashboard.png")

        # Generate head-to-head comparisons
        profiles = ["Cautious Carl", "Risk Taker Rachel", "Balanced Betty", 
                   "Superstitious Sam", "YOLO Yuki"]
        for i, profile1 in enumerate(profiles):
            for profile2 in profiles[i+1:]:
                visualizer.plot_head_to_head(
                    profile1, profile2,
                    save_path=f"output/head_to_head_{profile1.lower().replace(' ', '_')}_vs_{profile2.lower().replace(' ', '_')}.png"
                )

        logger.info("Simulation complete! Check output directory for visualizations.")

    except Exception as e:
        logger.error(f"Error during simulation: {e}")
        raise

if __name__ == "__main__":
    main() 