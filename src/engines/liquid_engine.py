# src/engines/liquid_engine.py

from .base_engine import RocketEngine

class LiquidEngine(RocketEngine):
    """
    Represents a liquid-propellant rocket engine.
    """
    def __init__(self, name, thrust, isp, burn_time, throttle_range=(0.6, 1.0)):
        super().__init__(name, thrust, isp, burn_time)
        self.throttle_range = throttle_range
        self.current_throttle = 1.0

    def set_throttle(self, throttle):
        """
        Sets the throttle of the engine.
        """
        if self.throttle_range[0] <= throttle <= self.throttle_range[1]:
            self.current_throttle = throttle
        else:
            raise ValueError(f"Throttle must be within {self.throttle_range}")

    def get_thrust(self, time):
        """
        Returns the thrust at a given time, considering the throttle.
        """
        if 0 <= time <= self.burn_time:
            return self.thrust * self.current_throttle
        return 0

    def to_dict(self):
        """
        Serializes the engine's configuration to a dictionary.
        """
        data = super().to_dict()
        data["throttle_range"] = self.throttle_range
        return data
