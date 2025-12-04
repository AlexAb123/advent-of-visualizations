from abc import ABC, abstractmethod


class SpeedControlMixin(ABC):
    SPEEDS = [1.0, 2.0, 4.0, 6.0, 10.0]
    DEFAULT_SPEED_INDEX = 0

    bindings = [("+, =", "increase_speed", "Increase Speed"), ("-, _", "decrease_speed", "Decrease Speed")]

    @abstractmethod
    def action_increase_speed(self) -> None:
        pass

    @abstractmethod
    def action_decrease_speed(self) -> None:
        i = self.SPEEDS.index(self.speed)
        self.speed = self.SPEEDS[max(0, i - 1)]
        self.controls.update_speed(self.speed)

        if self.is_playing:
            self.stop_auto_step()
            self.start_auto_step()
