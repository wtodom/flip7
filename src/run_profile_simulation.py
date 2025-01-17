"""Run a simulation with player profiles."""
import os
from pathlib import Path
from loguru import logger

from simulation.simulator import Simulator, SimulationConfig, PlayerConfig
from visualization.visualizer import Visualizer

def main():
    """Run the simulation and generate visualizations."""
    # Setup directories
    base_dir = Path(__file__).parent.parent
    profiles_dir = base_dir / "src" / "profiles"
    output_dir = base_dir / "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Configure logging
    log_file = output_dir / "profile_simulation.log"
    logger.add(log_file, rotation="1 day")
    
    logger.info("Starting profile simulation")
    
    # Create simulation config
    config = SimulationConfig(
        num_games=1000,
        num_players=6,
        base_seed=42,
        profiles_dir=profiles_dir,
        player_configs=[
            # Two Cautious Carls
            PlayerConfig(position=0, profile_name="Cautious Carl"),
            PlayerConfig(position=1, profile_name="Cautious Carl"),
            # Two Risk Taker Rachels
            PlayerConfig(position=2, profile_name="Risk Taker Rachel"),
            PlayerConfig(position=3, profile_name="Risk Taker Rachel"),
            # Two default players
            PlayerConfig(position=4, profile_name=None),
            PlayerConfig(position=5, profile_name=None)
        ]
    )
    
    # Run simulation
    simulator = Simulator(config)
    results = simulator.run()
    
    # Create visualizations
    logger.info("Generating visualizations")
    visualizer = Visualizer(results)
    visualizer.create_profile_report(output_dir)
    
    # Log summary statistics
    logger.info("\nSimulation Summary:")
    logger.info(f"Total Games: {results.total_games}")
    
    for profile_name, stats in results.profile_stats.items():
        logger.info(f"\n{profile_name} Statistics:")
        logger.info(f"Games Played: {stats.games_played}")
        logger.info(f"Win Rate: {stats.win_rate:.2%}")
        logger.info(f"Average Score: {stats.average_score:.1f}")
        logger.info(f"Bust Rate: {stats.bust_rate:.2%}")
        logger.info(f"Freeze Rate: {stats.freeze_rate:.2%}")
        logger.info(f"Pass Rate: {stats.pass_rate:.2%}")
        
        if profile_name != "default":
            logger.info(f"Lucky Cards per Game: {stats.lucky_cards_seen / stats.games_played:.2f}")
            logger.info(f"Superstition Cards per Game: {stats.superstition_cards_seen / stats.games_played:.2f}")
            logger.info(f"Average Risk Level: {sum(stats.risk_adjustments) / len(stats.risk_adjustments):.2f}")
    
    logger.info("\nSimulation complete. Check the output directory for visualizations.")

if __name__ == "__main__":
    main() 