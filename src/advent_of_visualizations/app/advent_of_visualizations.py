from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from advent_of_visualizations.app.puzzle_selector import PuzzleSelector
from advent_of_visualizations.visualizations.aoc2025.day04 import Day04
from advent_of_visualizations.visualizations.puzzle import Puzzle


class AdventOfVisualizations(App):
    """Main Advent of Visualizations Application"""

    CSS_PATH = "styles.tcss"

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield PuzzleSelector()
        yield Footer()

    def on_mount(self) -> None:
        self.push_screen(
            Day04(open("src/advent_of_visualizations/visualizations/aoc2025/inputs/day04.txt", "r").read()),
        )

    @property
    def puzzle(self) -> Puzzle:
        """Get the current puzzle screen"""
        return self.query_one(Puzzle)


def run() -> None:
    """Entry point for the application"""
    app = AdventOfVisualizations()
    app.run()
