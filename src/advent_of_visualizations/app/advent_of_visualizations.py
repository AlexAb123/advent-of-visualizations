from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header

from advent_of_visualizations.app.playback_controls import PlaybackControls
from advent_of_visualizations.visualizations.aoc2024.day01 import Day01
from advent_of_visualizations.visualizations.base_puzzle import BasePuzzle


class AdventOfVisualizations(App):
    """Main Advent of Visualizations Application"""

    CSS_PATH = "styles.tcss"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "reset", "Reset"),
    ]

    SPEEDS = [1.0, 2.0, 4.0, 6.0, 10.0]
    DEFAULT_SPEED_INDEX = 0

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield Day01("""10 20
            50 90
            12 1203""")
            yield PlaybackControls(self.SPEEDS)
        yield Footer()

    def on_mount(self) -> None:
        """Initialize playback state"""
        self._is_playing = False
        self.is_reverse = False
        self.speed = self.SPEEDS[self.DEFAULT_SPEED_INDEX]
        self.auto_step_timer = None
        self.controls.update_speed(self.speed)

    @property
    def puzzle(self) -> BasePuzzle:
        """Get the current puzzle widget"""
        return self.query_one(BasePuzzle)

    @property
    def controls(self) -> PlaybackControls:
        """Get the controls widget"""
        return self.query_one(PlaybackControls)

    @property
    def is_playing(self) -> bool:
        """Get playing state"""
        return self._is_playing

    @is_playing.setter
    def is_playing(self, value: bool) -> None:
        """Set playing state and update controls"""
        prev = self._is_playing
        self._is_playing = value
        if value != prev:
            if value:
                self.start_auto_step()
            else:
                self.stop_auto_step()
        self.controls.update_is_playing_status(value)

    def action_step_forward(self) -> None:
        """Step the puzzle forward"""
        self.puzzle.step_forward()
        self.is_playing = False

    def action_step_backward(self) -> None:
        """Step the puzzle backward"""
        self.puzzle.step_backward()
        self.is_playing = False

    def action_reset(self) -> None:
        """Reset the puzzle"""
        self.puzzle.reset()

    def action_toggle_play(self) -> None:
        """Toggle auto-play"""
        self.is_playing = not self.is_playing

    def action_increase_speed(self) -> None:
        """Cycle through playback speeds"""
        i = self.SPEEDS.index(self.speed)
        self.speed = self.SPEEDS[min(len(self.SPEEDS) - 1, i + 1)]
        self.controls.update_speed(self.speed)

        if self.is_playing:
            self.stop_auto_step()
            self.start_auto_step()

    def action_decrease_speed(self) -> None:
        i = self.SPEEDS.index(self.speed)
        self.speed = self.SPEEDS[max(0, i - 1)]
        self.controls.update_speed(self.speed)

        if self.is_playing:
            self.stop_auto_step()
            self.start_auto_step()

    def action_toggle_reverse(self) -> None:
        """Toggle reverse playback"""
        self.is_reverse = not self.is_reverse

    def start_auto_step(self) -> None:
        """Start automatic stepping"""
        interval = 1.0 / self.speed
        self.auto_step_timer = self.set_interval(interval, self.auto_step)

    def stop_auto_step(self) -> None:
        """Stop automatic stepping"""
        if self.auto_step_timer:
            self.auto_step_timer.stop()
            self.auto_step_timer = None

    def auto_step(self) -> None:
        """Automatically step forward or backward based on direction"""
        success = self.puzzle.step_backward() if self.is_reverse else self.puzzle.step_forward()

        if not success:
            # Reached the end/beginning, stop playing
            self.is_playing = False


def run() -> None:
    """Entry point for the application"""
    app = AdventOfVisualizations()
    app.run()
