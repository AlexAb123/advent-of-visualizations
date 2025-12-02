from typing import override

from rich.console import RenderableType
from textual.reactive import reactive
from textual.widget import Widget


class BasePuzzle(Widget):
    """Base class for all Advent of Code puzzle visualizations"""

    year: int
    day: int
    title: str

    step = reactive(0)
    total_steps = reactive(0)

    def __init__(self, input_data: str) -> None:
        super().__init__()
        self.input_data = input_data
        self.setup()

    def setup(self) -> None:
        """Parse input and initialize puzzle state"""
        raise NotImplementedError

    def step_forward(self) -> bool:
        """
        Go one step forward in the visualization.
        Returns True if step succeeded (not at the end), False otherwise.
        Default implementation: increment step by one if possible.
        """
        if self.step <= self.total_steps:
            self.step += 1
            return True
        return False

    def step_backward(self) -> bool:
        """
        Go one step backward in the visualization.
        Returns True if step succeeded (not at the start), False otherwise.
        Default implementation: decrement step by one if possible.
        """
        if self.step > 0:
            self.step -= 1
            return True
        return False

    def reset(self) -> None:
        """Reset puzzle to initial state"""
        self.step = 0
        self.setup()

    @override
    def render(self) -> RenderableType:
        """Return Rich renderable for current visualization state"""
        raise NotImplementedError
