import pathlib
import subprocess
import sys
import time
import pygubu
import datetime
from Logic.Notification import Notification
from UI.ReviewNotificationLogUI.ViewNotificationUI import ViewnotificationuiApp
from UI.ReviewNotificationLogUI.ErrorMessageUI import ErrormessageuiApp
import webbrowser

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ReviewNotificationLogUI.ui"


# create the application UI class
class ReviewNotificationLogUI:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        # Main widget
        self.mainwindow = builder.get_object("root", master)
        builder.connect_callbacks(self)

        # set variables on builder objects
        self.log_table = builder.get_object("log_table", master)
        self.log_table_cols = self.log_table['columns']
        # self.log_table.heading('#0', text='ID')
        self.log_table.heading('subject', text='Subject')
        self.log_table.heading('body', text='Message')
        self.log_table.heading('dateSent', text='Date Sent')
        self.log_table.heading('sentBy', text='Sent By')
        self.log_table.heading('subscriberCount', text='Subscribers')
        self.start_date = builder.get_object("start_date_menu", master)
        self.end_date = builder.get_object("end_date_menu", master)

        # self.view_notification_app = ViewnotificationuiApp()

        # must add self.start_date._top_cal.overrideredirect(False) to menu widgets for macOS, or it crashes
        # https://github.com/j4321/tkcalendar/issues/41
        # self.start_date._top_cal.overrideredirect(False)
        # self.end_date._top_cal.overrideredirect(False)

    # Return the top frame for the app so that it can be displayed in a tabbed notebook.
    def get_top_frame(self):
        return self.mainwindow

    def run(self):
        self.mainwindow.mainloop()

    # resets the calendar to the current date
    def reset(self):
        today = datetime.date.today()
        self.start_date.set_date(today)
        self.end_date.set_date(today)

    # opens Notification data in new view (fully functioning in sprint 2)
    # console will read the subject of selected Notification object
    def view(self):
        selected_item = self.log_table.focus()
        if selected_item:
            selected_item_values = self.log_table.item(selected_item)['values']
            subject = selected_item_values[0]
            body = selected_item_values[1]
            date = selected_item_values[2]
            self.view_notification_app = ViewnotificationuiApp()
            self.view_notification_app.display_notification(subject, body, date)

    def clear(self):
        for row in self.log_table.get_children():
            self.log_table.delete(row)

    def open_browser(self):
        time.sleep(2)
        url = "http://localhost:8080/index"
        webbrowser.open(url)
        # print("Browser button clicked")
        
        # the below code may open the web ui without needing to run it separately but it can't find the file
        # python_executable = sys.executable
        # script_path = pathlib.Path(__file__).parent / "WebNotificationLogUI.py"
        # subprocess.Popen([python_executable, str(script_path)])

    # gets the date range input and searches the database for matching criteria
    # additional end_date code adds one day to the end_date selection to make inclusive
    def search(self):
        self.clear()
        start_date = self.start_date.get()
        end_date = self.end_date.get()
        end_date = datetime.datetime.strptime(end_date, '%m/%d/%Y') + datetime.timedelta(days=1)
        end_date = end_date.strftime('%m/%d/%Y')

        notification_objs = Notification.get_notifications(start_date, end_date)

        if not notification_objs:
            ErrormessageuiApp(start_date, end_date)
            return start_date, end_date

        for notification_obj in notification_objs:
            notification_list = Notification(notification_obj[0], 0, notification_obj[1], notification_obj[2],
                                             notification_obj[3], notification_obj[4], notification_obj[5])
            self.log_table.insert('', 'end',
                                  values=(notification_list.get_note_subject(), notification_list.get_note_body(),
                                          notification_list.get_note_senddate(), notification_list.get_sender_name(),
                                          notification_list.get_note_number_sent()))

    # closes main window
    def close_log(self):
        self.mainwindow.destroy()


if __name__ == "__main__":
    app = ReviewNotificationLogUI()
    app.run()
