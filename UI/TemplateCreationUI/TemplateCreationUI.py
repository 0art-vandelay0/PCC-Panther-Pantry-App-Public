# **********************************************************************************************************************
# **********************************************************************************************************************
# Author:           Alex Huddleston
# Lab:              Template Creation
# Date:             04.24.2023
# Description:      This program prompts the user for a template name, template subject line
#                   and template message and saves it to the CIS234A_OOP database
# Input:            Template Name, Subject, Message (string)
# Output:           Template Name, Subject, Message
# Sources:
#
# Change Log:       - 05.01.2023:
# separated logic files into separate file "Template.py"
#
#                   - 05.21.2023:
# Fixed n-tier separation
# **********************************************************************************************************************
# **********************************************************************************************************************


# **********************************************************************************************************************
# **********************************************************************************************************************

#!/usr/bin/python3
import pathlib
import pygubu
import tkinter as tk
import tkinter.messagebox as mb
from Logic.Template import Template

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "template.ui"


class TemplateCreationUI:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)

    def get_top_frame(self):
        return self.mainwindow

    def run(self):
        self.mainwindow.mainloop()

    def clear_text(self):
        name = self.builder.get_object("template_name_entry")
        subject = self.builder.get_object("subject_entry")
        message = self.builder.get_object("message_box")

        # Delete contents of objects
        name.delete(0, tk.END)
        subject.delete(0, tk.END)
        message.delete("1.0", tk.END)

    def submit_template(self):

        # get entered text from Template Name, Subject and Message boxes
        name = self.builder.get_object("template_name_entry")
        name_contents = name.get()

        subject = self.builder.get_object("subject_entry")
        subject_contents = subject.get()

        message = self.builder.get_object("message_box")
        message_contents = message.get("1.0", "end-1c")

        # Check to see if Template name was entered
        if name_contents == "":
            mb.showerror(title="Error", message="Please enter a name for the template")

        elif Template.check_template_name(name_contents) > 0:
            mb.showerror(title="Error", message="A template with this name already exists")

        # Check to see if template subject was entered
        elif subject_contents == "":
            mb.showerror(title="Error", message="Please enter a subject for the template")

        # Check to see if template message was entered
        elif message_contents == "":
            mb.showerror(title="Error", message="Please enter a message for the template")

        # Write the template data to the template table in the database
        else:
            Template.submit_template(name_contents, subject_contents, message_contents)
            mb.showinfo(title="Submitted", message="New template submitted to the database successfully!")


    def cancel_template(self):
        # Close the Template Creation window.
        # This button will bring the user back to the landing page once all
        # pygubu apps are merged in sprint 2.

        self.mainwindow.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    root.title("Template Creation")
    app = TemplateCreationUI()
    app.run()