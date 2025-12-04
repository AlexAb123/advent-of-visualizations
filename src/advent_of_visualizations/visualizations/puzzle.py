from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import Screen

from advent_of_visualizations.visualizations.puzzle_status import PuzzleStatus


class Puzzle(Screen):
    """Base class for all Advent of Code puzzle visualizations"""

    year: int
    day: int
    puzzle_name: str

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("space", "toggle_play", "Toggle Play"),
        ("right, w, d", "step_forward", "Step Forward"),
        ("+, =", "increase_speed", "Increase Speed"),
        ("-, _", "decrease_speed", "Decrease Speed"),
        ("r", "reset", "Reset"),
    ]

    SPEEDS = [1.0, 2.5, 5.0, 10.0, 25.0, 50.0, 100.0]

    step = reactive(0)
    is_playing = reactive(False)
    is_done = reactive(False)
    speed_index = reactive(0)

    def __init__(self, input_data: str) -> None:
        super().__init__()
        self.input_data = input_data
        self.auto_step_timer = None
        self.setup()

    def setup(self) -> None:
        """Parse input and initialize puzzle state."""
        raise NotImplementedError

    def compose(self) -> ComposeResult:
        """Override to compose the screen layout"""
        raise NotImplementedError

    @property
    def status(self) -> PuzzleStatus:
        """Get PuzzleStatus widget
        Override to make custom PuzzleStatuses"""
        return self.query_one(PuzzleStatus)

    def update_status(self) -> None:
        """Override to set status"""
        raise NotImplementedError

    def watch_step(self) -> None:
        self.update_status()

    def watch_is_playing(self) -> None:
        if self.is_playing:
            self.start_auto_step()
        else:
            self.stop_auto_step()
        self.update_status()

    def watch_speed_index(self) -> None:
        if self.is_playing:
            self.stop_auto_step()
            self.start_auto_step()
        self.update_status()

    def action_step_forward(self) -> None:
        """Manually step the puzzle forward"""
        self.step_forward()
        self.is_playing = False

    def step_forward(self) -> bool:
        """Step forward. Returns true if successful (not done)."""
        if not self.is_done:
            self.step += 1
            return True
        return False

    def action_reset(self) -> None:
        """Reset the puzzle"""
        self.step = 0
        self.is_playing = False
        self.is_done = False
        self.setup()

    def action_toggle_play(self) -> None:
        """Toggle auto-play"""
        self.is_playing = not self.is_playing

    def action_increase_speed(self) -> None:
        """Increase playback speed"""
        self.speed_index = min(len(self.SPEEDS) - 1, self.speed_index + 1)

    def action_decrease_speed(self) -> None:
        """Increase playback speed"""
        self.speed_index = max(0, self.speed_index - 1)

    def start_auto_step(self) -> None:
        """Start automatic stepping"""
        interval = 1.0 / self.SPEEDS[self.speed_index]
        self.auto_step_timer = self.set_interval(interval, self.auto_step)

    def stop_auto_step(self) -> None:
        """Stop automatic stepping"""
        if self.auto_step_timer:
            self.auto_step_timer.stop()
            self.auto_step_timer = None

    def auto_step(self) -> None:
        """Automatically step forward"""
        if not self.step_forward():
            # Reached the end, stop playing
            self.is_playing = False
