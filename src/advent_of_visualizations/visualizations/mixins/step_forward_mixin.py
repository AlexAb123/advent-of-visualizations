from abc import ABC, abstractmethod


class StepForwardMixin(ABC):
    bindings = [("right, w, d", "step_forward", "Step Forward")]

    @abstractmethod
    def action_step_forward(self) -> None:
        self.step += 1
