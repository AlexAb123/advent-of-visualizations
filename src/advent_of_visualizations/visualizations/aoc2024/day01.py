from typing import override

from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table
from textual.reactive import reactive

from advent_of_visualizations.puzzles.base_puzzle import BasePuzzle


class Day01(BasePuzzle):
    """Historian Hysteria - Example visualization"""

    title = "Historian Hysteria"

    @override
    def setup(self) -> None:
        lines = self.input_data.strip().split("\n")

        left, right = [], []
        for line in lines:
            l, r = map(int, line.split())
            left.append(l)
            right.append(r)

        self.states = [(l, r) for l, r in zip(sorted(left), sorted(right))]

        self.total_steps = len(self.states)
        self.step = 0

    @override
    def step_forward(self) -> bool:
        self.log(self.step, self.total_steps)
        if self.step >= self.total_steps:
            return False
        self.step += 1
        return True

    @override
    def step_backward(self) -> bool:
        if self.step <= 0:
            return False
        self.step -= 1
        return True

    @override
    def render(self) -> RenderableType:
        table = Table(title=f"Day 1: {self.title}")
        table.add_column("Index", style="dim", justify="right")
        table.add_column("Left", style="cyan", justify="right")
        table.add_column("Right", style="magenta", justify="right")
        table.add_column("Distance", style="yellow", justify="right")

        acc = 0
        for i in range(self.step):
            l, r = self.states[i]
            d = abs(l - r)
            acc += d

            style = "bold reverse" if i == self.step - 1 else ""
            table.add_row(str(i), str(l), str(r), str(d), style=style)

        if self.step > 0:
            table.add_row("", "", "Total:", str(acc), style="bold green")

        return Panel(table, border_style="green", subtitle=f"Step {self.step}/{self.total_steps}")
