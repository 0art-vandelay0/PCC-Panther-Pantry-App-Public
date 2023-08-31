# **********************************************************************************************************************
# **********************************************************************************************************************
# Author:           Casey Hill, Erika Brooks
# Lab:              Sprint 1 - CIS234A - PCC Spring 2023
# Date:             05.14.2023
# Description:      Logic class for creating and saving Notification Object
# Sources:          Panther Pantry Project Story 2 & 4, sending and saving notifications
#
# Change Log:       - 04.23.2023:
#                       Added getters, setters, and formatted date with strftime()
#
# **********************************************************************************************************************

from dateutil.utils import today

from Data.Database import Database


class Notification:
    __note_id = ""
    __note_senderid = ""
    __note_sender_name = ""
    __note_senddate = ""
    __note_subject = ""
    __note_body = ""
    __note_number_sent = ""

    def __init__(self, note_id, note_senderid, note_sender_name, note_senddate, note_subject, note_body, note_numbersent):
        self.__note_id = note_id
        self.__note_senderid = note_senderid
        self.__note_sender_name = note_sender_name
        self.__note_senddate = note_senddate
        self.__note_subject = note_subject
        self.__note_body = note_body
        self.__note_number_sent = note_numbersent

    note_senddate = today()

    # setters
    def set_senderid(self, note_senderid):
        self.__note_senderid = note_senderid

    def set_senddate(self, note_senddate):
        self.__note_senddate = note_senddate

    def set_subject(self, note_subject):
        self.__note_subject = note_subject

    def set_body(self, note_body):
        self.__note_body = note_body

    def set_numbersent(self, note_numbersent):
        self.__note_number_sent = note_numbersent

  # getters
    def get_note_id(self):
        return self.__note_id

    def get_sender_name(self):
        return self.__note_sender_name

    def get_note_senddate(self):
        # took out time format as it wasnt working  %H:%M:%S
        self.__note_senddate = self.__note_senddate.strftime('%m-%d-%Y')
        return self.__note_senddate

    def get_note_subject(self):
        return self.__note_subject

    def get_note_body(self):
        return self.__note_body

    def get_note_number_sent(self):
        return self.__note_number_sent

    # as called from SendNotificationUI.sendmessage
    # makes a call to the Database.py file to write an email notification to the DB
    @staticmethod
    def notification_to_database(current_user, subject, message, count_of_list):
        date = today()
        Database.add_notification_to_database(current_user, date, subject, message, count_of_list)

    # get the list of notifications from the database, filtered by date range
    @staticmethod
    def get_notifications(start_date, end_date):
        from Data.Database import Database
        return Database.get_notifications(start_date, end_date)

    def delete_notification_by_id(notification_id):
        Database.delete_notification_by_id(notification_id)