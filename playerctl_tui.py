import subprocess
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button
from textual.containers import Container

class PlayerctlApp(App):
    """A TUI app to control media playback with Play/Pause, Skip Back, and Skip Forward buttons."""

    BINDINGS = [
        ("q", "quit", "Quit the app"),
    ]

    CSS = """
    Screen {
        layout: vertical; /* Arrange top-level widgets vertically */
    }

    #main-content {
        height: 1fr; /* Make this container take up all available vertical space between header/footer */
        width: 1fr;  /* Make this container take up all available horizontal space */
        layout: vertical; /* Arrange its children (Play/Pause button, Skip buttons container) vertically */
        /* We remove align: center middle here, as it might interfere with distributing height */
    }

    #play-pause-button {
        height: 1fr; /* Make Play/Pause button fill its vertical space within #main-content */
        width: 1fr; /* Make Play/Pause button fill its horizontal space within #main-content */
        align: center middle; /* Center text */
        margin: 1; /* Add a small margin around the button */
    }

    #skip-buttons-container {
        height: 1fr; /* Make this container also fill its vertical space, equal to play-pause-button */
        width: 1fr; /* Make this container fill available horizontal space within #main-content */
        layout: horizontal; /* Arrange skip buttons horizontally */
        margin: 1 0; /* Add top/bottom margin, no left/right */
    }

    #skip-buttons-container Button {
        width: 1fr; /* Make each skip button take up equal horizontal space within its container */
        height: 1fr; /* Make each skip button fill its vertical space within #skip-buttons-container */
        align: center middle; /* Center text */
        margin: 0 1; /* Add horizontal margin between skip buttons */
    }
    """

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Container(id="main-content"):
            yield Button("Play/Pause", id="play-pause-button", variant="primary")
            with Container(id="skip-buttons-container"):
                yield Button("Rewind 10s", id="rewind_button", variant="default")
                yield Button("Forward 10s", id="forward_button", variant="default")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when a button is pressed."""
        command = None
        if event.button.id == "play-pause-button":
            command = ["playerctl", "play-pause"]
        elif event.button.id == "rewind_button":
            command = ["playerctl", "position", "10-"]
        elif event.button.id == "forward_button":
            command = ["playerctl", "position", "10+"]

        if command:
            try:
                subprocess.run(command, check=True)
            except FileNotFoundError:
                self.bell()
                self.log(f"{command[0]} not found. Is playerctl installed?")
            except subprocess.CalledProcessError as e:
                self.bell()
                self.log(f"Error executing command: {' '.join(command)}. Error: {e}")

    def action_quit(self) -> None:
        """An action to quit the application."""
        self.exit()

if __name__ == "__main__":
    app = PlayerctlApp()
    app.run()
