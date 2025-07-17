# src/main.py

import argparse
import numpy as np
from mission.mission_loader import load_mission_from_json
from mission.trajectory_simulator import TrajectorySimulator
from visualization.plotter import plot_results

def main():
    """
    Main function to run the rocket simulation.
    """
    parser = argparse.ArgumentParser(description="StellarLab Rocket Propulsion Simulator")
    parser.add_argument(
        '--mission', 
        type=str, 
        required=True,
        help='Path to the mission JSON file.'
    )
    args = parser.parse_args()

    # Load the mission stages from the specified file
    try:
        stages = load_mission_from_json(args.mission)
    except FileNotFoundError:
        print(f"Error: Mission file not found at '{args.mission}'")
        return
    except Exception as e:
        print(f"An error occurred while loading the mission: {e}")
        return

    # Initialize and run the simulation
    simulator = TrajectorySimulator(stages)
    results = simulator.simulate()

    # Plot the results
    if results:
        plot_results(results)

if __name__ == "__main__":
    main()
