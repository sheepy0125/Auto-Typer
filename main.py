"""
Auto Typer
Created by sheepy0125
2021-04-08
"""

### Setup ###
# Import
import pynput.keyboard
import json
import time
import tkinter
import tkinter.ttk
import tkinter.filedialog

# Constants
BOILERPLATE_NEW_SCRIPT_CODE = {
    "keystrokes": {},
    "metadata": {
        "Title": "None",
        "Description": "None",
        "Commands": 0,
        "Author": "None",
    },
}
POSSIBLE_KEYS = ["space", "control", "esc", "alt", "tab"]
KEY_MODES = {
    "Send a key (tap)": "send_key",
    "Hold down a key": "hold_key",
    "Release a key": "release_key",
}

### Classes ###
class Typer:
    """Handles typing"""

    # Initialize
    def __init__(self):
        # Create controller
        self.keyboard = pynput.keyboard.Controller()

    # Send key
    def send_key(self, key: str):
        if len(key) > 1:
            exec(f"self.keyboard.tap(pynput.keyboard.Key.{key})")
        else:
            self.keyboard.tap(key)

    # Hold down key
    def hold_key(self, key: str):
        if len(key) > 1:
            exec(f"self.keyboard.press(pynput.keyboard.Key.{key})")
        else:
            self.keyboard.press(key)

    # Release key
    def release_key(self, key: str):
        if len(key) > 1:
            exec(f"self.keyboard.release(pynput.keyboard.Key.{key})")
        else:
            self.keyboard.press(key)


class MainWindowClass:
    """Boilerplate class for a window"""

    # Initialize window
    def __init__(
        self,
        win_size: tuple = None,
        win_title: str = None,
        win_resizable: bool = None,
        clearing: bool = False,
    ):
        # Create variables if not clearing
        if not clearing:
            self.win_size = win_size
            self.win_title = win_title
            self.win_resizable = win_resizable
            self.widget_width = self.win_size[0] // 10
            self.widget_height = 2
            self.margin_size = 16

        # Create actual window
        self.root = tkinter.Tk()
        self.root.title(self.win_title)
        self.root.geometry(f"{self.win_size[0]}x{self.win_size[1]}")
        self.root.resizable(width=self.win_resizable, height=self.win_resizable)

    # Clear window
    def clear_win(self):
        self.root.destroy()
        self.__init__(clearing=True)

    # Exit window
    def exit_win(self):
        self.root.quit()
        self.root.destroy()

    # Run
    def run(self):
        self.root.mainloop()


class AutoTyperTkinter(MainWindowClass):
    """Auto Typer Tkinter Window"""

    # Initialize
    def __init__(self, **kwargs):
        # Setup variables
        if "clearing" not in kwargs:
            self.loaded_script = None
            self.text_to_flash = None
            self.script = BOILERPLATE_NEW_SCRIPT_CODE

            # Create typer class
            self.typer = Typer()

        # Initialize main window class
        super().__init__(**kwargs)

    # Exception handling
    def exception_handling(
        self, message: str = None, exception: str = None, show_menu_button: bool = True
    ):
        self.text_to_flash = ""

        if message is not None:
            self.text_to_flash += f"{message}"
        if exception is not None:
            self.text_to_flash += (
                f' Information: "{type(exception).__name__}: {exception}"'
            )
        if self.text_to_flash == "":
            self.text_to_flash = "There was an error, but no information was given on why. I have no clue either."

        self.footer_gui(show_menu_button=show_menu_button)

    # Footer
    def footer_gui(self, show_menu_button: bool = True, master=None):
        if master is None:
            master = self.root

        # Flashed text
        if self.text_to_flash is not None:
            tkinter.Label(master=master, text=f"{self.text_to_flash}").place(
                relx=0.5,
                rely=(0.8 if show_menu_button else 0.875),
                anchor=tkinter.CENTER,
            )
            # Reset for next page
            self.text_to_flash = None

        # Credits
        tkinter.Label(master=master, text="Created by sheepy0125.").place(
            relx=0.5, rely=(0.875 if show_menu_button else 0.95), anchor=tkinter.CENTER
        )

        # Menu button at bottom
        if show_menu_button:
            tkinter.Button(
                master=master,
                text="Menu",
                width=self.widget_width,
                height=self.widget_height,
                command=self.menu,
            ).place(relx=0.5, rely=0.95, anchor=tkinter.CENTER)

    # Menu screen
    def menu(self):
        self.clear_win()

        # GUI
        tkinter.Label(master=self.root, text="Welcome to Sheepy's Auto Typer!").pack()
        tkinter.Label(master=self.root, text="Please choose an option.").pack()
        tkinter.ttk.Separator(master=self.root, orient="horizontal").pack(
            pady=8, padx=self.margin_size, fill="x"
        )
        tkinter.Button(
            master=self.root,
            text="Create a script",
            width=self.widget_width,
            height=self.widget_height,
            command=self.create_script,
        ).pack(pady=8)
        tkinter.Button(
            master=self.root,
            text="Load a script",
            width=self.widget_width,
            height=self.widget_height,
            command=self.load_script,
        ).pack(pady=8)
        tkinter.ttk.Separator(master=self.root, orient="horizontal").pack(
            pady=8, padx=self.margin_size, fill="x"
        )
        tkinter.Button(
            master=self.root,
            text="Start script",
            width=self.widget_width,
            height=self.widget_height,
            command=lambda: self.start_script(sec_to_wait.get()),
        ).pack(pady=8)
        tkinter.Label(master=self.root, text="Seconds until start typing").pack()
        sec_to_wait = tkinter.Spinbox(
            master=self.root,
            width=self.widget_width,
            justify=tkinter.CENTER,
            from_=0,
            to=120,
        )
        sec_to_wait.pack(pady=0)

        self.footer_gui(show_menu_button=False)

    # Create script
    def create_script(self):
        # Save script
        def save_script():
            # Get file location of where to save script
            pass

        # Add command
        def add_command(
            command_id: int,
        ):
            # Add command
            def add_command_to_dict(key_input: str, delay_next_key: str, key_mode: str):
                # Make sure that the command is able to be added

                # Check if the command id is not already there
                if self.script.get(command_id):
                    self.text_to_flash = "Command already exists... overwriting!"

                # Check if key and delay is invalid
                if len(key_input) <= 1 and str(key_input).lower() not in POSSIBLE_KEYS:
                    self.text_to_flash = "Error, key is not a valid key."
                elif not str(delay_next_key).isnumeric():
                    self.text_to_flash = "Error, delay is not a valid integer."

                # Stuff is valid
                else:
                    # Save it in script code
                    self.script[command_id] = {}
                    self.script[command_id]["key"] = key_input
                    self.script[command_id]["delay_next_key"] = int(delay_next_key)
                    self.script[command_id]["mode"] = key_mode
                    return

                # Was not valid
                add_command(command_id=command_id)

            # Open new window with steps for adding a command
            add_command_window = tkinter.Toplevel(master=self.root)
            add_command_window.title("Add new command")
            add_command_window.geometry("500x500")

            # GUI
            tkinter.Label(master=add_command_window, text="Adding a command!").pack(
                pady=8
            )
            tkinter.ttk.Separator(master=self.root, orient="horizontal").pack(
                pady=4, padx=self.margin_size, fill="x"
            )
            # Key input
            tkinter.Label(master=add_command_window, text="Type a key").pack(pady=8)
            tkinter.Label(
                master=add_command_window,
                text='You may also use "shift", "alt", "control", "space", and "esc"',
            ).pack(pady=8)
            key_input = tkinter.Text(
                master=add_command_window, width=self.widget_width, height=1
            )
            key_input.pack(pady=8)
            tkinter.Label(master=add_command_window).pack(pady=4)
            # Delay until next key
            tkinter.Label(
                master=add_command_window, text="Delay until next key (milliseconds)"
            ).pack(pady=8)
            delay_next_key = tkinter.Spinbox(
                master=add_command_window,
                width=self.widget_width,
                justify=tkinter.CENTER,
                from_=0,
                to=1000000,
                increment=1000.0,
            )
            delay_next_key.pack(pady=8)
            # Mode
            tkinter.Label(master=add_command_window, text="Key mode (choose one)").pack(
                pady=8
            )
            key_mode_combobox = tkinter.ttk.Combobox(
                master=add_command_window,
                width=self.widget_width,
                values=list(KEY_MODES.keys()),
                state="readonly",
            )
            key_mode_combobox.pack()

            tkinter.Button(
                master=add_command_window,
                text="Add command",
                width=self.widget_width,
                height=self.widget_height,
                command=lambda: (
                    add_command_to_dict(
                        key_input=str(key_input.get("1.0", tkinter.END)),
                        delay_next_key=delay_next_key.get(),
                        key_mode=KEY_MODES[str(key_mode_combobox.get())],
                    )
                ),
            ).pack(pady=8)

            self.footer_gui(show_menu_button=False, master=add_command_window)

        self.clear_win()

        # GUI

        # Initial command text
        command_text = tkinter.StringVar(master=self.root)
        command_text.set("Commands: 0")

        tkinter.Label(master=self.root, text="Creating a script").pack()
        tkinter.Label(master=self.root, textvariable=command_text).pack(pady=8)
        tkinter.ttk.Separator(master=self.root, orient="horizontal").pack(
            pady=4, padx=self.margin_size, fill="x"
        )

        tkinter.Button(
            master=self.root,
            text="Add a command",
            width=self.widget_width,
            height=self.widget_height,
            command=lambda: add_command(
                command_id=(int(command_text.get().replace("Commands: ", "")))
            ),
        ).pack(pady=8)

        # Command viewer
        tkinter.ttk.Separator(master=self.root, orient="horizontal").pack(
            pady=4, padx=self.margin_size, fill="x"
        )

        # Script code
        tkinter.ttk.Separator(master=self.root, orient="horizontal").pack(
            pady=4, padx=self.margin_size, fill="x"
        )
        tkinter.Label(master=self.root, text="Script code").pack(pady=4)
        script_code_text_box = tkinter.Text(
            master=self.root, width=self.widget_width, height=4
        )
        script_code_text_box.pack(pady=8)

        tkinter.ttk.Separator(master=self.root, orient="horizontal").pack(
            pady=4, padx=self.margin_size, fill="x"
        )
        tkinter.Button(
            master=self.root,
            text="Save script",
            width=self.widget_width,
            height=self.widget_height,
            command=save_script,
        ).pack(pady=8)

        self.footer_gui()

        # Boilerplate script code
        self.script = BOILERPLATE_NEW_SCRIPT_CODE
        script_code_text_box.insert(1.0, str(self.script))

    # Load script
    def load_script(self):
        try:
            file_to_open = tkinter.filedialog.askopenfilename(
                initialdir="D:\Code\Python\Auto Typer",
                title="Select script to load",
                filetypes=(("JSON files", "*.json"), ("All of the files", "*.*")),
            )
            self.text_to_flash = f'Loaded file "{file_to_open}"'
            # Reload footer (so flash will show up)
            self.footer_gui(show_menu_button=False)

            with open(file_to_open) as script_file:
                self.loaded_script = json.load(script_file)

            # GUI
            # If there is already an existing GUI, nope it.
            try:
                for widget in self.widget_list:
                    widget.destroy()
            except Exception:
                pass

            metadata_sep = tkinter.ttk.Separator(master=self.root, orient="horizontal")
            metadata_sep.pack(pady=8, padx=self.margin_size, fill="x")

            # Metadata
            metadata_label = tkinter.Label(master=self.root, text="Metadata")
            metadata_label.pack()
            metadata_text = tkinter.Text(
                master=self.root, width=self.widget_width, height=4
            )
            metadata_text.pack()
            for metadata_item in self.loaded_script["metadata"].items():
                metadata_text.insert(
                    tkinter.END, f"{metadata_item[0]}: {metadata_item[1]}\n"
                )
            metadata_text.config(state=tkinter.DISABLED)

            self.widget_list = [metadata_sep, metadata_label, metadata_text]

        # FileNotFound occured
        except FileNotFoundError:
            # Determine whether file is not found or it is empty
            if file_to_open == "":
                self.exception_handling(
                    message="No file is selected.", show_menu_button=False
                )
            else:
                self.exception_handling(message="File is not found.")
            self.menu()

        # Error occured
        except Exception as exception:
            self.exception_handling(
                message="There was an error parsing the JSON data.", exception=exception
            )
            self.loaded_script = None
            self.menu()

    # Starting script
    def start_script(self, time_until_start: int):
        # Start typing
        def start_typing():
            try:
                num_commands = self.loaded_script["metadata"]["Commands"]
            except Exception as exception:
                self.exception_handling(
                    message="Error: Impropper metadata.", exception=exception
                )
                self.menu()

            for current_keystroke in range(num_commands):
                # Attempt to find
                try:
                    keystroke_data = self.loaded_script["keystrokes"][
                        f"{current_keystroke + 1}"
                    ]

                    # Do the stuff!
                    try:
                        exec(
                            f"self.typer.{keystroke_data['mode']}(\"{keystroke_data['key']}\")"
                        )
                    except Exception as exception:
                        self.exception_handling(
                            message="Error: Failed to send keystroke.",
                            exception=exception,
                        )
                        self.menu()

                    # Wait
                    time.sleep((keystroke_data["delay_next_key"] // 1000))

                # Could not find
                except Exception as exception:
                    self.exception_handling(
                        message="Error: Could not find keystroke.", exception=exception
                    )
                    self.menu()

        # Check if the script is valid
        if self.loaded_script is not None:
            # Wait seconds
            time.sleep(int(time_until_start))
            start_typing()

        # Script is not valid
        else:
            self.text_to_flash = "Can not start empty script!"
            self.menu()


auto_typer_win = AutoTyperTkinter(
    win_title="Sheepy's Auto Typer Program!", win_size=(500, 500), win_resizable=False
)
auto_typer_win.menu()
auto_typer_win.run()
