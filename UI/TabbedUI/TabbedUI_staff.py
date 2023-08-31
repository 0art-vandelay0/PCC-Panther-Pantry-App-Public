# This will launch a GUI with a series of tabs.
# The tabs available are dependent upon the role
# of the user who has logged in.
#
#
# to launch the GUI, use the below two lines, then call run_panther_pantry()
# def run_panther_pantry():
#     PantherPantryUI.launch_pantry()

# Additional tabs can be added above def run(self): near the end of the file

import tkinter as tk
import tkinter.ttk as ttk

from UI.WelcomeUI.WelcomeUI import WelcomeUI
from UI.SendNotificationUI.SendNotificationUI import *


class TabbedUI:
    def __init__(self, toplevel):
        # This is needed to allow the notebook tabs to stretch.
        # toplevel = tk.Toplevel()
        tk.Grid.columnconfigure(toplevel, 0, weight=1)
        tk.Grid.rowconfigure(toplevel, 0, weight=1)

        # build ui
        self.__main_notebook = ttk.Notebook(toplevel)
        self.__main_notebook.grid(column='0', row='0', sticky='nsew')
        self.__main_notebook.rowconfigure('0', weight='1')
        self.__main_notebook.columnconfigure('0', weight='1')

        # TabbedUI widget
        self.__mainwindow = self.__main_notebook

        # Add Welcome tab
        about_app = WelcomeUI(self.__mainwindow)
        self.__main_notebook.add(about_app.get_top_frame(), text="Welcome")

        # Add additional tabs here
        #
        #
    def run(self):
        self.__mainwindow.mainloop()


def launch_staff_pantry():
    # if __name__ == '__main__':
    root = tk.Tk()
    root.title("Panther Pantry Notification Tool")
    app = TabbedUI(root)
    app.run()


# launch_staff_pantry()
# **********************************************************************************************************************
# **********************************************************************************************************************
