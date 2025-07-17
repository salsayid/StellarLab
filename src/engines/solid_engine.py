# src/engines/solid_engine.py

from .base_engine import RocketEngine

class SolidEngine(RocketEngine):
    """
    Represents a solid-propellant rocket engine.
    """
    def __init__(self, name, thrust, isp, burn_time, ignition_delay=0.1):
        super().__init__(name, thrust, isp, burn_time)
        self.ignition_delay = ignition_delay

    def get_thrust(self, time):
        """
        Returns the thrust at a given time.
        """
        if self.ignition_delay <= time <= self.burn_time + self.ignition_delay:
            return self.thrust
        return 0
    
    def to_dict(self):
        """
        Serializes the engine's configuration to a dictionary.
        """
        data = super().to_dict()
        data["ignition_delay"] = self.ignition_delay
        return data
