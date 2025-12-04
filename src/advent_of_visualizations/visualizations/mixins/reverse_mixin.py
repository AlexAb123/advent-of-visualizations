from abc import ABC, abstractmethod


class ReverseMixin(ABC):
    bindings = [("shift+space", "reverse", "Reverse")]

    @abstractmethod
    def action_reverse(self) -> None:
        self.is_reverse = not self.is_reverse
