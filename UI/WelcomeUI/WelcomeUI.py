
# file that houses Pygubu code for welcome screen in
# the staff/employee GUI window

#!/usr/bin/python3
import pathlib
import tkinter.ttk as ttk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "welcome2.ui"


class WelcomeUI:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.__mainwindow = builder.get_object("frame1", master)
        builder.connect_callbacks(self)

    # Return the top frame for the app so that it can be displayed in a tabbed notebook.
    def get_top_frame(self):
        return self.__mainwindow

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = WelcomeUI(root)
    app.run()

