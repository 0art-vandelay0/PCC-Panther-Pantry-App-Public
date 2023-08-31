from flask import Flask, render_template, request, redirect
from Logic.Notification import Notification

class WebNotificationLogUI:
    app = Flask(__name__)


    @app.route("/")
    @app.route("/index")
    @app.route("/index.html")

    @staticmethod
    def homepage():
        menu_choices = {
            "/review_notification_log": "Review Notification Log"
        }
        return render_template("index.html", menu_choices=menu_choices)


    @staticmethod
    @app.route("/review_notification_log")
    def review_notification_log():
        return render_template("view_notifications.html", notifications=[])


    @staticmethod
    @app.route("/search", methods=["POST"])
    def search():
        # Retrieve notifications based on date range
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        notification_objs = Notification.get_notifications(start_date, end_date)

        # Convert notification objects to a list of dictionaries
        notifications = []
        for notification_obj in notification_objs:
            notification = {
                "id": notification_obj[0],  # Add the notification ID to the dictionary
                "subject": notification_obj[3],
                "body": notification_obj[4],
                "dateSent": notification_obj[2],
                "sentBy": notification_obj[1],
                "subscriberCount": notification_obj[5]  # Assuming the subscriber count is at index 5
            }
            notifications.append(notification)

        return render_template("view_notifications.html", notifications=notifications)


    @staticmethod
    @app.route("/delete", methods=["POST"])
    def delete_notification():
        notification_id = request.form["notification_id"]
        Notification.delete_notification_by_id(notification_id)
        return render_template("deleting_notification.html")


    if __name__ == "__main__":
        app.run(port=8080)
