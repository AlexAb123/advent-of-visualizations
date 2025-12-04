from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import Screen


class BasePuzzle(Screen):
    """Base class for all Advent of Code puzzle visualizations"""

    year: int
    day: int
    puzzle_name: str

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    step = reactive(0)
    total_steps = reactive(0)

    def __init_subclass__(cls, **kwargs) -> None:
        """Merge BINDINGS from all parent classes and mixins"""
        super().__init_subclass__(**kwargs)
        bindings = []
        seen = set()
        for class_ in reversed(cls.__mro__):
            for binding in vars(class_).get("BINDINGS", []):
                action = binding[1]  # action name
                if action not in seen:
                    bindings.append(binding)
                    seen.add(action)
        cls.BINDINGS = bindings

    def __init__(self, input_data: str) -> None:
        super().__init__()
        self.input_data = input_data
        self.setup()

    def setup(self) -> None:
        """Parse input and initialize puzzle state"""
        raise NotImplementedError

    def compose(self) -> ComposeResult:
        """Override to compose the screen layout"""
        raise NotImplementedError

    def step_forward(self) -> bool:
        """Go one step forward. Returns True if successful."""
        if self.step < self.total_steps:
            self.step += 1
            return True
        return False

    def step_backward(self) -> bool:
        """Go one step backward. Returns True if successful."""
        if self.step > 0:
            self.step -= 1
            return True
        return False

    def reset(self) -> None:
        """Reset puzzle to initial state"""
        self.step = 0
        self.setup()
