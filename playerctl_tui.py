import subprocess
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button
from textual.containers import Container

class PlayerctlApp(App):
    """A TUI app to control media playback, system volume, and Hyprland."""

    BINDINGS = [
        ("q", "quit", "Quit the app"),
    ]

    CSS = """
    Screen {
        layout: vertical; /* Arrange top-level widgets vertically */
    }

    #main-content {
        height: 1fr; /* This container takes up all space between header/footer */
        width: 1fr;
        layout: vertical; /* Its children are stacked vertically */
    }

    /* Top row: Volume buttons */
    #volume-buttons-container {
        height: 1fr; /* Takes 1 fractional unit of vertical space */
        width: 1fr;
        layout: horizontal;
    }

    #volume-buttons-container Button {
        height: 1fr;
        width: 1fr;
        align: center middle;
        margin: 0 1;
    }

    /* Middle section: Control Pad */
    #control-pad-container {
        height: 3fr; /* Takes 5 fractional units of vertical space */
        width: 1fr;
        layout: vertical;
        align: center middle; /* Center the control pad grid visually */
    }

    /* Rows within the control pad */
    #dpad-row-1, #dpad-row-2, #dpad-row-3 {
        height: 1fr; /* Each row within the 5fr space takes 1fr of that 5fr */
        width: 1fr;
        layout: horizontal;
        margin: 1 0;
    }
    #control-pad-container Button {
        height: 1fr;
        width: 1fr; /* Default width for buttons in these rows */
        align: center middle;
        margin: 0 1;
    }
    
    /* Make the d-pad arrow buttons specifically smaller */
    #up_arrow_button, #down_arrow_button, #left_arrow_button, #right_arrow_button {
        width: 0.5fr; /* Make arrow buttons half the width for a tighter D-pad look */
        height: 1fr;
    }


    /* Bottom row: Media playback buttons */
    #media-playback-container {
        height: 1fr; /* Takes 1 fractional unit of vertical space */
        width: 1fr;
        layout: horizontal;
        margin: 1 0;
    }

    #media-playback-container Button {
        width: 1fr;
        height: 1fr;
        align: center middle;
        margin: 0 1;
    }
    """

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Container(id="main-content"):
            # Top row for volume buttons
            with Container(id="volume-buttons-container"):
                yield Button("Vol -", id="vol_down_button", variant="default")
                yield Button("Mute", id="mute_button", variant="default")
                yield Button("Vol +", id="vol_up_button", variant="default")

            # A container for the entire control pad
            # with Container(id="control-pad-container"):
            #     # D-pad up button row
            #     with Container(id="dpad-row-1"):
            #         yield Button("Up", id="up_arrow_button", variant="default")
            #
            #     # D-pad left, select, and right button row
            #     with Container(id="dpad-row-2"):
            #         yield Button("Left", id="left_arrow_button", variant="default")
            #         yield Button("Select", id="select_button", variant="primary")
            #         yield Button("Right", id="right_arrow_button", variant="default")
            #
            #     # D-pad down button row
            #     with Container(id="dpad-row-3"):
            #         yield Button("Down", id="down_arrow_button", variant="default")

            # Bottom row for media playback controls
            with Container(id="media-playback-container"):
                yield Button("Rewind 10s", id="rewind_button", variant="default")
                yield Button("Play/Pause", id="play-pause-button", variant="primary")
                yield Button("Forward 10s", id="forward_button", variant="default")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when a button is pressed."""
        command = None

        if event.button.id == "up_arrow_button":
            command = ["hyprctl", "dispatch", "movefocus", "u"]
        elif event.button.id == "down_arrow_button":
            command = ["hyprctl", "dispatch", "movefocus", "d"]
        elif event.button.id == "left_arrow_button":
            command = ["hyprctl", "dispatch", "movefocus", "l"]
        elif event.button.id == "right_arrow_button":
            command = ["hyprctl", "dispatch", "movefocus", "r"]
        elif event.button.id == "select_button":
            command = ["hyprctl", "dispatch", "fullscreen", "0"] # Toggle fullscreen
        elif event.button.id == "rewind_button":
            command = ["playerctl", "position", "10-"]
        elif event.button.id == "forward_button":
            command = ["playerctl", "position", "10+"]
        elif event.button.id == "play-pause-button":
            command = ["playerctl", "play-pause"]
        elif event.button.id == "mute_button":
            command = ["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle"]
        elif event.button.id == "vol_up_button":
            command = ["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "5%+"]
        elif event.button.id == "vol_down_button":
            command = ["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "5%-"]

        if command:
            try:
                subprocess.run(command, check=True)
            except FileNotFoundError:
                self.bell()
                self.log(f"Command '{command[0]}' not found. Is it installed?")
            except subprocess.CalledProcessError as e:
                self.bell()
                self.log(f"Error executing command: {' '.join(command)}. Error: {e}")

    def action_quit(self) -> None:
        """An action to quit the application."""
        self.exit()

if __name__ == "__main__":
    app = PlayerctlApp()
    app.run()
