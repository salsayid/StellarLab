# src/mission/mission_loader.py

import json
from src.engines.base_engine import RocketEngine

class Stage:
    """
    Represents a single stage of a rocket.
    """
    def __init__(self, stage_name, dry_mass, fuel_mass, engine, num_engines):
        self.stage_name = stage_name
        self.dry_mass = dry_mass
        self.fuel_mass = fuel_mass
        self.engine = engine
        self.num_engines = num_engines
        self.total_mass = self.dry_mass + self.fuel_mass

    def get_thrust(self, time):
        """
        Calculates the total thrust from all engines in the stage.
        """
        return self.engine.get_thrust(time) * self.num_engines

    def get_mass_flow_rate(self):
        """
        Calculates the total mass flow rate from all engines.
        """
        return self.engine.mass_flow_rate * self.num_engines

def load_mission_from_json(file_path):
    """
    Loads a complete mission profile from a JSON file.
    """
    with open(file_path, 'r') as f:
        mission_data = json.load(f)

    print(f"Loading mission: {mission_data['name']}")
    
    stages = []
    for stage_data in mission_data['stages']:
        print(f"  - Loading stage: {stage_data['stage_name']}")
        engine_config_path = stage_data['engine_config']
        engine = RocketEngine.from_json(engine_config_path)
        
        stage = Stage(
            stage_name=stage_data['stage_name'],
            dry_mass=stage_data['dry_mass'],
            fuel_mass=stage_data['fuel_mass'],
            engine=engine,
            num_engines=stage_data['num_engines']
        )
        stages.append(stage)
        
    return stages
