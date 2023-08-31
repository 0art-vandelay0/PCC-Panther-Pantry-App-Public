#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk

import UI.TabbedUI.TabbedUI_staff
from Logic.User import User
import bcrypt
from Data.Database import Database
from UI.TabbedUI.TabbedUI import *

#!/usr/bin/python3
import pathlib
import pygubu
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "welcomeUI.ui"

class WelcomeuiApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        self.username_entry = builder.get_object("username_entry", master)
        self.password_entry = builder.get_object("password_entry", master)
        builder.connect_callbacks(self)

    def login_submit_button(self):
        username_or_email = str(self.username_entry.get())
        user_pass = str(self.password_entry.get())
        user_hash = User.get_user_hash(username_or_email)
        if user_hash is None:
            # print(F"user hash is none\nusername: {username_or_email}")
            self.invalid_user_hash()
        elif bcrypt.checkpw(user_pass.encode(), user_hash[0]) is True:
            # print(F"user password matches hash\nusername: {username_or_email}")
            user_role = Database.get_role(username_or_email)
            manager_role = "Manager"
            staff_role = "Staff"
            for role in user_role:
                if role.lower() == manager_role.lower():
                    UI.TabbedUI.TabbedUI.launch_pantry()
                elif role.lower() == staff_role.lower():
                    UI.TabbedUI.TabbedUI_staff.launch_staff_pantry()
                else:
                    self.unauth_access_error()
        elif bcrypt.checkpw(user_pass.encode(), user_hash[0]) is False:
            self.invalid_user_hash()
        else:
            # print(F"login_submit_button has failed\nusername: {username_or_email}")
            self.login_else_error()

    def login_cancel_button(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    # code telling an error popup what to do
    def invalid_user_hash(self):
        too_long_popup = tk.Toplevel(self.mainwindow)
        self.popup_window(too_long_popup, "Invalid username, email, or password.\nPlease try again.")

    # code telling an error popup what to do
    def login_else_error(self):
        too_long_popup = tk.Toplevel(self.mainwindow)
        self.popup_window(too_long_popup, "LoginUI.login_submit_button has experienced an error.\nPlease try again.")

    # code telling an error popup what to do
    def unauth_access_error(self):
        too_long_popup = tk.Toplevel(self.mainwindow)
        self.popup_window(too_long_popup, "You do not have access to this tool.")

    # code to manage the email sent popup
    def popup_window(self, parent, text):
        root_frame = ttk.Frame(parent, padding=10)
        root_frame.grid(column=0, row=0)

        header_label = ttk.Label(root_frame, text="Notification Message", font="{Arial} 16 {bold}")
        header_label.grid(column=0, row=0)

        answer_label = ttk.Label(root_frame, text=text, justify=tk.CENTER, font="{Arial} 12 {bold}")
        answer_label.grid(column=0, row=1)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = WelcomeuiApp()
    app.run()


def get_username_or_email(self):
    my_user = str(self.username_entry.get())
    return my_user
