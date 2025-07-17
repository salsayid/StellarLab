# src/engines/hybrid_engine.py

from .base_engine import RocketEngine
import numpy as np

class HybridEngine(RocketEngine):
    """
    Represents a hybrid rocket engine.
    """
    def __init__(self, name, thrust, isp, burn_time, throttle_delay=0.5):
        super().__init__(name, thrust, isp, burn_time)
        self.throttle_delay = throttle_delay
        self.target_throttle = 1.0
        self.current_throttle = 0.0

    def set_throttle(self, throttle):
        """
        Sets the target throttle. The engine will ramp up/down to this value.
        """
        self.target_throttle = np.clip(throttle, 0, 1)


    def get_thrust(self, time):
        """
        Returns the thrust at a given time, simulating throttle delay.
        """
        # A simple model for throttle response
        if self.current_throttle < self.target_throttle:
            self.current_throttle += (1.0 / self.throttle_delay) * 0.1 # simplified time step
        elif self.current_throttle > self.target_throttle:
            self.current_throttle -= (1.0 / self.throttle_delay) * 0.1 # simplified time step
            
        self.current_throttle = np.clip(self.current_throttle, 0, 1)

        if 0 <= time <= self.burn_time:
            return self.thrust * self.current_throttle
        return 0

    def to_dict(self):
        """
        Serializes the engine's configuration to a dictionary.
        """
        data = super().to_dict()
        data["throttle_delay"] = self.throttle_delay
        return data
