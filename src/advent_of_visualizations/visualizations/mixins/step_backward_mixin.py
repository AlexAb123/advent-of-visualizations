from abc import ABC, abstractmethod


class StepBackwardMixin(ABC):
    bindings = [("left, s, a", "step_backward", "Step Backward")]

    @abstractmethod
    def action_step_backward(self) -> None:
        pass
