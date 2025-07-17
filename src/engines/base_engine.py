# src/engines/base_engine.py

from abc import ABC, abstractmethod
import json

class RocketEngine(ABC):
    """
    Abstract base class for a rocket engine.
    """
    def __init__(self, name, thrust, isp, burn_time):
        self.name = name
        self.thrust = thrust  # in Newtons
        self.isp = isp  # in seconds
        self.burn_time = burn_time  # in seconds
        self.mass_flow_rate = self.thrust / (self.isp * 9.80665)

    @abstractmethod
    def get_thrust(self, time):
        """
        Returns the thrust at a given time.
        """
        pass

    def to_dict(self):
        """
        Serializes the engine's configuration to a dictionary.
        """
        return {
            "name": self.name,
            "thrust": self.thrust,
            "isp": self.isp,
            "burn_time": self.burn_time,
            "type": self.__class__.__name__
        }

    @classmethod
    def from_json(cls, file_path):
        """
        Loads an engine configuration from a JSON file.
        """
        with open(file_path, 'r') as f:
            config = json.load(f)
        
        engine_type = config.pop("type")
        # This is a simple factory. A more robust implementation
        # would avoid this direct import logic here.
        if engine_type == "LiquidEngine":
            from .liquid_engine import LiquidEngine
            return LiquidEngine(**config)
        elif engine_type == "SolidEngine":
            from .solid_engine import SolidEngine
            return SolidEngine(**config)
        elif engine_type == "HybridEngine":
            from .hybrid_engine import HybridEngine
            return HybridEngine(**config)
        else:
            raise ValueError(f"Unknown engine type: {engine_type}")

