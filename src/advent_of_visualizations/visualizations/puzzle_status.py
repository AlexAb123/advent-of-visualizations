from rich.console import RenderableType
from rich.panel import Panel
from textual.widgets import Static


class PuzzleStatus(Static):
    """Status display panel for puzzle info"""

    DEFAULT_CSS = """
    PuzzleStatus {
        width: 30;
        height: 100%;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self._status_data: dict[str, object] = {}

    def update_status(self, **kwargs: object) -> None:
        self._status_data = kwargs
        self.refresh()

    def render(self) -> RenderableType:
        lines = [f"{k}: {v}" for k, v in self._status_data.items()]
        return Panel("\n".join(lines), border_style="yellow")
