from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import ProgressBar, Static


class PlaybackControls(Widget):
    """Display playback state (keyboard controlled)"""

    is_playing = reactive(False)
    speed = reactive(1.0)

    def __init__(self, speeds: list[float]) -> None:
        super().__init__()
        self.speeds = speeds

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("⏸ Paused", id="status")
            yield Static("Speed: ", id="speed-indicator")
            yield ProgressBar(100, id="speed-bar")

    def update_is_playing_status(self, is_playing: bool) -> None:
        """Update playback status display"""
        status = self.query_one("#status", Static)
        if is_playing:
            status.update("[#9dff00]▶ Playing[/]")
        else:
            status.update("[#ff4d00ff]⏸ Paused[/]")

    def update_speed(self, speed: float) -> None:
        """Update speed display"""
        self.query_one("#speed-indicator", Static).update(f"Speed: {speed}x")

        min_speed, max_speed = min(self.speeds), max(self.speeds)
        progress = (speed - min_speed) / (max_speed - min_speed) * 100

        self.query_one("#speed-bar", ProgressBar).update(progress=progress)
