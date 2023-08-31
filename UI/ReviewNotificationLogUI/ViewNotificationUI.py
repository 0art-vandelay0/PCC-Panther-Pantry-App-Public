#!/usr/bin/python3
import pathlib
import pygubu
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ViewNotificationUI.ui"

# creates the additional View Notification window to show extended text of message selected
class ViewnotificationuiApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object(
            "view_notification_window", master)
        builder.connect_callbacks(self)

        self.subject_data_box = builder.get_object("subject_data_box")
        self.body_data_box = builder.get_object("body_data_box")
        self.date_data_box = builder.get_object("date_data_box")

    def run(self):
        self.mainwindow.mainloop()

    # closes main window
    def close_view(self):
        self.mainwindow.destroy()

    # copies the selected body_data_box text
    def copy(self):
        selected_text = self.body_data_box.selection_get()
        self.body_data_box.clipboard_clear()
        self.body_data_box.clipboard_append(selected_text)

    # selects all of the body_data_box text
    def select_all(self):
        self.body_data_box.focus_set()
        self.body_data_box.tag_add('sel', '1.0', 'end')

    # inserts the subject, body and date sent into the View Notification window when selected
    def display_notification(self, subject, body, date):
        self.subject_data_box.config(text=subject)
        # self.body_data_box.delete("1.0", "end")
        self.body_data_box.insert("1.0", body)
        self.date_data_box.config(text=date)

        # Disable editing of the body text box
        self.body_data_box.config(state="normal", insertontime=0)
        self.body_data_box.delete("1.0", "end")
        self.body_data_box.insert("1.0", body)
        self.body_data_box.config(state="disabled")


if __name__ == "__main__":
    app = ViewnotificationuiApp()
    app.run()

