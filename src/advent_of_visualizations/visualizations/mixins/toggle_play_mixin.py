from abc import ABC, abstractmethod


class TogglePlayMixin(ABC):
    bindings = [("space", "toggle_play", "Toggle Play")]

    @abstractmethod
    def action_toggle_play(self) -> None:
        pass
