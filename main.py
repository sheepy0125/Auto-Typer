# --------------------------------- #
# Auto Typer, written by sheepy0125 #
# --------------------------------- #

# Import
import pynput
import sys
import tkinter
import tkinter.ttk

# Main window class (boilerplate code)
class MainWindowClass:
    # Initialize window
    def __init__(self, win_size:tuple = None, win_title:str = None, win_resizable:bool = None, clearing:bool = False):
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
        self.root.resizable(width = self.win_resizable, height = self.win_resizable)

    # Clear window
    def clear_win(self):
        self.root.destroy()
        self.__init__(clearing = True)

    # Exit window
    def exit_win(self):
        self.root.quit()
        self.root.destroy()

    # Run
    def run(self):
        self.root.mainloop()

# Auto typer class
class AutoTyper(MainWindowClass):
    # Initialize
    def __init__(self, **kwargs):
        # Setup variables
        self.loaded_script = None

        # Initialize main window class
        super().__init__(**kwargs)

    # Menu screen
    def menu(self, text_to_flash:str = None):
        self.clear_win()
        sec_to_wait = tkinter.IntVar(master = self.root)

        # GUI
        tkinter.Label(master = self.root, text = "Welcome to Sheepy's Auto Typer!").pack()
        tkinter.Label(master = self.root, text = "Please choose an option.").pack()
        tkinter.ttk.Separator(master = self.root, orient = "horizontal").pack(pady = 8, padx = self.margin_size, fill = "x")
        tkinter.Button(master = self.root, text = "Create a script", width = self.widget_width, height = self.widget_height, command = self.create_script).pack(pady = 8)
        tkinter.Button(master = self.root, text = "Load a script", width = self.widget_width, height = self.widget_height, command = self.load_script).pack(pady = 8)
        tkinter.ttk.Separator(master = self.root, orient = "horizontal").pack(pady = 8, padx = self.margin_size, fill = "x")
        tkinter.Button(master = self.root, text = "Start script", width = self.widget_width, height = self.widget_height, command = lambda: self.start_script(loaded_script, sec_to_wait.get())).pack(pady = 8)
        tkinter.Label(master = self.root, text = "Seconds until start typing").pack()
        sec_to_wait = tkinter.Spinbox(master = self.root, width = self.widget_width, justify = tkinter.CENTER, from_ = 0, to = 120).pack(pady = 0)

    # Create script
    def create_script(self):
        self.clear_win()

        # GUI
        tkinter.Label(master = self.root, text = "Creating a script").pack()

    # Load script
    def load_script(self):
        self.clear_win()

        # GUI
        tkinter.Label(master = self.root, text = "Loading a script").pack()

    # Starting script
    def start_script(self, script_to_start:str, time_until_start:int):
        # Check if the script is valid
        if (script_to_start is not None):
            # TODO: wait and tell how much time is left (progress bar if possible? idk how tkinter works)
            pass

        # Script is not valid
        else:
            self.menu(text_to_flash = "Can not start empty script!")

auto_typer_win = AutoTyper(win_title = "Sheepy's Auto Typer Program!", win_size = (500, 500), win_resizable = False)
auto_typer_win.menu()
auto_typer_win.run()