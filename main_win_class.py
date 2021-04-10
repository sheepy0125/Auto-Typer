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