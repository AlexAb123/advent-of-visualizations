from textual.reactive import reactive

from advent_of_visualizations.visualizations.puzzle import Puzzle


class ReversiblePuzzle(Puzzle):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("space", "toggle_play", "Toggle Play"),
        ("shift+space", "toggle_reverse", "Toggle Reverse"),
        ("right, w, d", "step_forward", "Step Forward"),
        ("left, s, a", "step_backward", "Step Backward"),
        ("+, =", "increase_speed", "Increase Speed"),
        ("-, _", "decrease_speed", "Decrease Speed"),
        ("r", "reset", "Reset"),
    ]

    step: int
    is_reverse = reactive(False)

    def watch_is_reverse(self) -> None:
        self.update_status()

    def action_toggle_reverse(self) -> None:
        self.is_reverse = not self.is_reverse

    def action_step_backward(self) -> None:
        """Manually step the puzzle backward"""
        self.step_backward()
        self.is_playing = False

    def step_backward(self) -> bool:
        """Step backward. Returns true if successful (not at start)."""
        if self.step > 0:
            self.step -= 1
            return True
        return False

    def auto_step(self) -> None:
        """Automatically step forward or backward based on direction"""
        success = self.step_backward() if self.is_reverse else self.step_forward()

        if not success:
            # Reached the end/beginning, stop playing
            self.is_playing = False
