"""Run simulation with player profiles and generate visualizations."""
import os
from pathlib import Path
from loguru import logger

from src.simulation.simulator import (
    Simulator, SimulationConfig, PlayerConfig, DEFAULT_PROFILES_DIR
)
from src.visualization.visualizer import Visualizer

def main():
    """Run simulation and generate visualizations."""
    # Set up logging
    logger.add("simulation.log", rotation="1 day")
    logger.info("Starting simulation with player profiles")
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Initialize simulator and visualizer
    config = SimulationConfig(
        num_games=1000,
        players=[
            PlayerConfig(profile_name="Cautious Carl"),
            PlayerConfig(profile_name="Risk Taker Rachel"),
            PlayerConfig(profile_name="Balanced Betty"),
            PlayerConfig(profile_name="Superstitious Sam"),
            PlayerConfig(profile_name="YOLO Yuki")
        ],
        profiles_dir=DEFAULT_PROFILES_DIR
    )
    
    simulator = Simulator(config)
    results = simulator.run_simulation()
    visualizer = Visualizer(results)
    
    # Generate visualizations
    logger.info("Generating visualizations...")
    
    visualizer.plot_winning_scores_distribution(
        str(output_dir / "winning_scores_dist.png")
    )
    
    visualizer.plot_player_outcomes(
        str(output_dir / "player_outcomes.png")
    )
    
    visualizer.plot_win_rates(
        str(output_dir / "win_rates.png")
    )
    
    visualizer.plot_score_progression(
        str(output_dir / "score_progression.png")
    )
    
    visualizer.create_summary_dashboard(
        str(output_dir / "dashboard.png")
    )
    
    # Generate head-to-head comparisons
    profiles = ["Cautious Carl", "Risk Taker Rachel", "Balanced Betty"]
    for i, profile1 in enumerate(profiles):
        for profile2 in profiles[i+1:]:
            visualizer.plot_head_to_head(
                profile1, profile2,
                str(output_dir / f"head_to_head_{profile1.lower().replace(' ', '_')}_vs_{profile2.lower().replace(' ', '_')}.png")
            )
    
    logger.info("Visualization generation complete. Check the output directory for results.")

if __name__ == "__main__":
    main() 