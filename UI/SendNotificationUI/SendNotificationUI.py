# file that houses Pygubu code for sending the notification

# !/usr/bin/python3

import tkinter as tk
import pathlib
import tkinter.ttk as ttk
import pygubu
from Logic.SendEmail import send_email
from Logic.Notification import Notification
from Logic.User import *

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "sendnoteUI2.ui"


# build/define the class with fetches from the GUI built with pygubu-designer
class SendNotificationUI:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object("sendnote_toplevel1", master)
        builder.connect_callbacks(self)

        self.sendnote_subject = builder.get_object('sendnote_subject')
        self.sendnote_messagebody = builder.get_object('sendnote_messagebody')

    # code that will clear all fields of the GUI
    #  https://itecnote.com/tecnote/python-cannot-clear-output-text-tkinter-tclerror-bad-text-index-0/
    def clear(self):
        self.sendnote_subject.delete(0, tk.END)
        self.sendnote_messagebody.delete('1.0', tk.END)

    # code telling the confirmation popup what to do
    def confirm_send_popup(self, count_of_list):
        confirm_popup = tk.Toplevel(self.mainwindow)
        subject = str(self.sendnote_subject.get())
        message = str(self.sendnote_messagebody.get('1.0', tk.END))
        self.popup_window(confirm_popup, F"The following email has been sent to {count_of_list} users:\n\n"
                                         F"{subject}")

    # code telling the error popup what to do
    def body_too_long(self, length_of_message):
        too_long_popup = tk.Toplevel(self.mainwindow)
        self.popup_window(too_long_popup, F"The body of the message is {length_of_message}.\n"
                                          F"This exceeds the character limit of 1000!\n"
                                          F"Please shorten your message!")

    # fetch the subject and message from the user GUI
    # call send_mail to send the email and receive back the total count of email addresses sent to
    # write the notification to the DB
    # print a message that confirms the DB write was successful
    def sendmessage(self):
        subject = str(self.sendnote_subject.get())
        message = str(self.sendnote_messagebody.get('1.0', tk.END))
        count_of_list = send_email(subject, message)
        # below line needs to be amended to ensure that
        # we are pulling the current logged-in user's ID to the template message sent.
        # current_user = User.get_user_id()
        current_user = 1
        while True:
            length_of_message = int(len(message))
            try:
                if length_of_message <= 536870912:
                    # if length_of_message <= 1000:
                    Notification.notification_to_database(current_user, subject, message, count_of_list)
                    self.confirm_send_popup(count_of_list)
                    print("saved to DB without error")
                    break
                if length_of_message > 536870912:
                    # if length_of_message > 1000:
                    self.body_too_long(length_of_message)
                    print("length of message exceeded 536,870,912 characters")
                    # print("length of message exceeded 1,000 characters")
                    break
            except ValueError:
                self.body_too_long(length_of_message)
                print("SendNotificationUI.def_sendmessage failed the try and landed in except")
                break

    # code to manage the email sent popup
    def popup_window(self, parent, text):
        root_frame = ttk.Frame(parent, padding=10)
        root_frame.grid(column=0, row=0)

        header_label = ttk.Label(root_frame, text="Notification Sent", font="{Arial} 16 {bold}")
        header_label.grid(column=0, row=0)

        answer_label = ttk.Label(root_frame, text=text, justify=tk.CENTER, font="{Arial} 12 {bold}")
        answer_label.grid(column=0, row=1)

    def cancel(self):
        # self.destroy()
        popup1 = tk.Toplevel(self.mainwindow)
        self.popup_window(popup1, "Please click the 'X' to close.")

    # Return the top frame for the app so that it can be displayed in a tabbed notebook.
    def get_top_frame(self):
        return self.mainwindow

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = SendNotificationUI(root)
    app.run()
