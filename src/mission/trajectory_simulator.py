# src/mission/trajectory_simulator.py

import numpy as np
from scipy.integrate import solve_ivp
from utils import constants

class TrajectorySimulator:
    """
    Simulates the trajectory of a multi-stage rocket.
    """
    def __init__(self, stages):
        """
        Initializes the simulator with a list of stages.
        Args:
            stages (list): A list of Stage objects.
        """
        self.stages = stages
        self.total_initial_mass = sum(s.total_mass for s in self.stages)

    def _atmospheric_model(self, altitude):
        """
        A simple exponential atmospheric density model.
        Args:
            altitude (float): Altitude in meters.
        Returns:
            float: Air density in kg/m^3.
        """
        # A very simplified model. Real models are more complex.
        scale_height = 8500  # meters
        sea_level_density = 1.225  # kg/m^3
        return sea_level_density * np.exp(-altitude / scale_height)

    def _rocket_equation(self, t, y, current_stage, initial_stage_mass):
        """
        Defines the differential equations for the rocket's flight.
        This function is used by the ODE solver.
        Args:
            t (float): Current time.
            y (list): State vector [velocity, altitude].
            current_stage (Stage): The currently firing stage.
            initial_stage_mass (float): The mass of the rocket at the start of the current stage burn.
        Returns:
            list: The derivatives [acceleration, velocity].
        """
        velocity, altitude = y
        
        # Calculate current mass
        mass_flow_rate = current_stage.get_mass_flow_rate()
        current_mass = initial_stage_mass - mass_flow_rate * t

        if current_mass <= current_stage.dry_mass:
            return [0, velocity] # Burnout

        # Get thrust from the engine
        thrust = current_stage.get_thrust(t)

        # Calculate gravitational acceleration
        g = constants.G * (constants.EARTH_RADIUS / (constants.EARTH_RADIUS + altitude))**2
        
        # Simple drag model (can be improved)
        # For this simulation, we'll keep it simple and ignore it for now
        # to focus on the core propulsion dynamics.
        # drag_force = 0.5 * self._atmospheric_model(altitude) * velocity**2 * drag_coefficient * area
        # drag_accel = drag_force / current_mass
        drag_accel = 0

        # Acceleration
        acceleration = (thrust / current_mass) - g - drag_accel
        
        return [acceleration, velocity]

    def simulate(self):
        """
        Runs the full multi-stage trajectory simulation.
        Returns:
            dict: A dictionary containing the simulation results (time, altitude, velocity, etc.).
        """
        results = {
            'time': [], 'altitude': [], 'velocity': [], 
            'mass': [], 'thrust': [], 'stage': []
        }
        
        current_mass = self.total_initial_mass
        time_offset = 0
        
        # Initial conditions
        y0 = [0, 0] # Initial velocity and altitude

        for i, stage in enumerate(self.stages):
            print(f"\n--- Simulating Stage {i+1}: {stage.stage_name} ---")
            
            burn_duration = stage.fuel_mass / stage.get_mass_flow_rate()
            t_span = [0, burn_duration]
            
            # We need to pass extra arguments to the solver
            args = (stage, current_mass)

            # Solve the ODEs for this stage
            sol = solve_ivp(
                self._rocket_equation, 
                t_span, 
                y0, 
                args=args,
                dense_output=True,
                max_step=1.0 # Use smaller steps for better resolution
            )

            # Record results for this stage
            sim_times = sol.t
            for t in sim_times:
                velocity, altitude = sol.sol(t)
                mass = current_mass - stage.get_mass_flow_rate() * t
                
                results['time'].append(t + time_offset)
                results['altitude'].append(altitude / 1000) # convert to km
                results['velocity'].append(velocity)
                results['mass'].append(mass)
                results['thrust'].append(stage.get_thrust(t))
                results['stage'].append(i + 1)

            # Update state for the next stage
            final_velocity, final_altitude = sol.y[:, -1]
            y0 = [final_velocity, final_altitude]
            time_offset += sol.t[-1]
            
            # Jettison the current stage's dry mass
            current_mass -= stage.dry_mass
            current_mass -= stage.fuel_mass # Fuel is already burned
            
            print(f"Stage {i+1} separation. T+ {time_offset:.2f}s")
            print(f"Altitude: {final_altitude/1000:.2f} km, Velocity: {final_velocity:.2f} m/s")

        print("\n--- Simulation Complete ---")
        return results
