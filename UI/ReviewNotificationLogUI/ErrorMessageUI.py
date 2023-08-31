#!/usr/bin/python3
import pathlib
import pygubu
import datetime
from datetime import datetime, timedelta

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ErrorMessageUI.ui"


class ErrormessageuiApp:
    def __init__(self, start_date, end_date, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)
        self.set_date_range(start_date, end_date)

    def run(self):
        self.mainwindow.mainloop()

    def close(self):
        self.mainwindow.destroy()

    # set the date range for the error message
    # use datetime strptime to remove the added day check from ReviewNotificationLogUI to
    def set_date_range(self, start_date, end_date):
        end_date = datetime.strptime(end_date, "%m/%d/%Y") - timedelta(days=1)
        end_date = end_date.strftime("%m/%d/%Y")
        date_select_range = f"{start_date} - {end_date}"
        self.builder.get_object("date_range_label").config(text=date_select_range)

if __name__ == "__main__":
    app = ErrormessageuiApp()
    app.run()
