from typing import override

from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Header, Static

from advent_of_visualizations.visualizations.puzzle import Puzzle
from advent_of_visualizations.visualizations.puzzle_status import PuzzleStatus


def get_adjs(r, c, lines):
    for dr in -1, 0, 1:
        for dc in -1, 0, 1:
            if dr == dc == 0:
                continue
            if not (0 <= r + dr < len(lines) and 0 <= c + dc < len(lines[0])):
                continue
            if lines[r + dr][c + dc] != "@":
                continue
            yield (r + dr, c + dc)


class Day04Visualization(Static):
    DEFAULT_CSS = """
    Day04Visualization {
        width: 1fr;
        height: 100%;
    }
    """

    def __init__(self, puzzle: "Day04") -> None:
        super().__init__()
        self.puzzle = puzzle

    def render(self) -> RenderableType:
        s = ""
        for line in self.puzzle.lines:
            for c in line:
                match c:
                    case ".":
                        s += "[dim].[/dim]"
                    case "X":
                        s += f"[#ff5c0a].[/]"
                    case "@":
                        s += f"[#6fff00]@[/]"
        return Panel(s)


class Day04(Puzzle):
    """Historian Hysteria - Example visualization"""

    year = 2024
    day = 1
    puzzle_name = "Historian Hysteria"
    step: int  # Type hint for Pylance

    @override
    def setup(self) -> None:
        self.lines = list(map(list, (self.input_data.strip().split("\n"))))
        self.q = []
        self.adjs_count = {}
        for r in range(len(self.lines)):
            for c in range(len(self.lines[0])):
                if self.lines[r][c] != "@":
                    continue
                self.adjs_count[(r, c)] = len(list(get_adjs(r, c, self.lines)))
                if self.adjs_count[(r, c)] < 4:
                    self.q.append((r, c))
        self.seen = set(self.q)

    @override
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Day04Visualization(self)
            yield PuzzleStatus()
        yield Footer()

    def step_forward(self) -> bool:
        if self.is_done:
            return False

        new_q = []
        while self.q:
            r, c = self.q.pop(0)
            self.lines[r][c] = "X"
            for adj in get_adjs(r, c, self.lines):
                if adj in self.seen:
                    continue
                self.adjs_count[adj] -= 1
                if self.adjs_count[adj] < 4:
                    new_q.append(adj)
                    self.seen.add(adj)
        self.q = new_q
        if len(self.q) == 0:
            self.is_done = True

        self.step += 1
        self.query_one(Day04Visualization).refresh()
        self.update_status()
        return True

    @override
    def update_status(self):
        self.query_one(PuzzleStatus).update_status(
            total=len(self.seen),
            speed=self.SPEEDS[self.speed_index],
            playing=self.is_playing,
        )
