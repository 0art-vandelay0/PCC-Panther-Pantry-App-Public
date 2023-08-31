from datetime import datetime
from unittest import TestCase
from Logic.Notification import Notification


class TestNotification(TestCase):

    # tests the setters
    def test_constructor(self):
        note_id = "420"
        sender_id = "1"
        sender_name = "George Glass"
        send_date = datetime.now()
        subject = "Subject Line"
        body = "Test Body"
        numbers_sent = 10

        notification = Notification(note_id, sender_id, sender_name, send_date, subject, body, numbers_sent)

        self.assertEqual(notification.get_note_id(), note_id)
        self.assertEqual(notification.get_sender_name(), sender_name)
        self.assertEqual(notification.get_note_senddate(), send_date.strftime("%m-%d-%Y"))
        self.assertEqual(notification.get_note_subject(), subject)
        self.assertEqual(notification.get_note_body(), body)
        self.assertEqual(notification.get_note_number_sent(), numbers_sent)

    # tests the get notifications module of Notification.py
    def test_get_notifications(self):
        start_date = "2023-05-01"
        end_date = "2023-05-22"

        result = Notification.get_notifications(start_date, end_date)
        self.assertIsInstance(result, list)
        self.assertEqual(tuple(result[0]), (1, 'Luke Skywalker', datetime(2023, 5, 10, 0, 0), 'Manager Login Test',
                                            'Manager has logged in via the pygubu-designer GUI method!\n', 5))

    # tests the notification_to_database module of Notification.py
    def test_notification_to_database(self):
        current_user = 1
        subject = "Test Subject"
        message = "Test Message"
        count_of_list = 5

        Notification.notification_to_database(current_user, subject, message, count_of_list)

    def test_get_note_number_sent(self):
        notification = Notification("", "", "", "", "", "", 10)
        result = notification.get_note_number_sent()
        self.assertEqual(result, 10)

    def test_set_senddate(self):
        notification = Notification("", "", "", "", "", "", "")
        send_date = datetime(2023, 5, 16)
        notification.set_senddate(send_date)
        result = notification.get_note_senddate()
        self.assertEqual(result, send_date.strftime("%m-%d-%Y"))