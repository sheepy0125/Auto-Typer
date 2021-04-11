# --------------------------------- #
# Auto Typer, written by sheepy0125 #
# --------------------------------- #

# Import
import pynput.keyboard
import sys
import json
import tkinter
import tkinter.ttk
import tkinter.filedialog

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

# Auto typer Tkinter class
class AutoTyperTkinter(MainWindowClass):
    # Initialize
    def __init__(self, **kwargs):
        # Setup variables
        if "clearing" not in kwargs:
            self.loaded_script = None
            self.text_to_flash = None

        # Initialize main window class
        super().__init__(**kwargs)

    # Exception handling
    def exception_handling(self, message:str = None, exception:str = None):
        self.text_to_flash = ""

        if message is not None: self.text_to_flash += f"{message}"
        if exception is not None: self.text_to_flash += f" Information: \"{type(exception).__name__}: {exception}\""

        if self.text_to_flash == "": self.text_to_flash = "There was an error, but no information was given on why. I have no clue either."

        print(self.text_to_flash)

    # Footer
    def footer_gui(self, show_menu_button:bool = True):
        # Flashed text
        if self.text_to_flash is not None: 
            tkinter.Label(master = self.root, text = f"{self.text_to_flash}").place(relx = 0.5, rely = (0.8 if show_menu_button else 0.875), anchor = tkinter.CENTER)
            # Reset for next page
            self.text_to_flash = None

        # Credits
        tkinter.Label(master = self.root, text = "Created by sheepy0125.").place(relx = 0.5, rely = (0.875 if show_menu_button else 0.95), anchor = tkinter.CENTER)

        # Menu button at bottom
        if show_menu_button:
            tkinter.Button(master = self.root, text = "Menu", width = self.widget_width, height = self.widget_height, command = self.menu).place(relx = 0.5, rely = 0.95, anchor = tkinter.CENTER)

    # Menu screen
    def menu(self):
        self.clear_win()

        # GUI
        tkinter.Label(master = self.root, text = "Welcome to Sheepy's Auto Typer!").pack()
        tkinter.Label(master = self.root, text = "Please choose an option.").pack()
        tkinter.ttk.Separator(master = self.root, orient = "horizontal").pack(pady = 8, padx = self.margin_size, fill = "x")
        tkinter.Button(master = self.root, text = "Create a script", width = self.widget_width, height = self.widget_height, command = self.create_script).pack(pady = 8)
        tkinter.Button(master = self.root, text = "Load a script", width = self.widget_width, height = self.widget_height, command = self.load_script).pack(pady = 8)
        tkinter.ttk.Separator(master = self.root, orient = "horizontal").pack(pady = 8, padx = self.margin_size, fill = "x")
        tkinter.Button(master = self.root, text = "Start script", width = self.widget_width, height = self.widget_height, command = lambda: self.start_script(sec_to_wait.get())).pack(pady = 8)
        tkinter.Label(master = self.root, text = "Seconds until start typing").pack()
        sec_to_wait = tkinter.Spinbox(master = self.root, width = self.widget_width, justify = tkinter.CENTER, from_ = 0, to = 120)
        sec_to_wait.pack(pady = 0)

        self.footer_gui(show_menu_button = False)

    # Create script
    def create_script(self):
        self.clear_win()

        # GUI
        tkinter.Label(master = self.root, text = "Creating a script").pack()

        self.footer_gui()

    # Load script
    def load_script(self):
        try:
            file_to_open = tkinter.filedialog.askopenfilename(initialdir = "D:\Code\Python\Auto Typer", title = "Select script to load", filetypes = (("JSON files","*.json"), ("All of the files", "*.*")))
            self.text_to_flash = f"Loaded file \"{file_to_open}\""

            with open (file_to_open) as script_file:
                self.loaded_script = json.load(script_file)

            # GUI
            # If there is already an existing GUI, nope it.
            try: 
                for widget in self.widget_list: widget.destroy()
            except Exception: pass

            metadata_sep = tkinter.ttk.Separator(master = self.root, orient = "horizontal")
            metadata_sep.pack(pady = 8, padx = self.margin_size, fill = "x")

            # Metadata
            metadata_label = tkinter.Label(master = self.root, text = "Metadata")
            metadata_label.pack()
            metadata_text = tkinter.Text(master = self.root, height = 4, width = self.widget_width)
            metadata_text.pack()
            for metadata_item in self.loaded_script["metadata"].items(): metadata_text.insert(tkinter.END, f"{metadata_item[0]}: {metadata_item[1]}\n")
            metadata_text.config(state = tkinter.DISABLED)

            self.widget_list = [metadata_sep, metadata_label, metadata_text]

        # Error occured
        except Exception as exception:
            self.exception_handling(message = "There was an error parsing the JSON data.", exception = exception)
            self.loaded_script = None
            self.menu()

    # Starting script
    def start_script(self, time_until_start:int):
        # Start typing
        def start_typing():
            try: num_keystrokes = self.loaded_script["metadata"]["Keystrokes"]
            except Exception as exception:
                self.exception_handling(message = "Error: Impropper metadata.", exception = exception)
                self.menu()

            for current_keystroke in range(num_keystrokes):
                # Attempt to find 
                try:
                    keystroke_data = self.loaded_script["keystrokes"][f"{current_keystroke + 1}"]                    

                # Could not find
                except Exception as exception:
                    self.exception_handling(message = "Error: Could not find keystroke.", exception = exception)
                    self.menu()
                    
        # Check if the script is valid
        if (self.loaded_script is not None):
            # Wait seconds
            self.root.after((time_until_start * 1000), start_typing)
        
        # Script is not valid
        else:
            self.text_to_flash = "Can not start empty script!"
            self.menu()

auto_typer_win = AutoTyperTkinter(win_title = "Sheepy's Auto Typer Program!", win_size = (500, 500), win_resizable = False)
auto_typer_win.menu()
auto_typer_win.run()