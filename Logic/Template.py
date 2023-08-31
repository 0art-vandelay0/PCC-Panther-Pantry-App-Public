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
# - Created separate file from Template UI builder
# - Added errors for missing name, subject and message contents
# - Added error for template name already existing in database
# - Added confirmation message when successfully storing new template
#
#                   - 05.07.2023:
# - Created function to close Template Creation window with "cancel" button.
#   Will add functionality to bring user back to landing page in sprint 2.
# - Fixed a bug with checking message contents where it was passing elif statement
#   even with a blank text box.
# **********************************************************************************************************************
# **********************************************************************************************************************


# **********************************************************************************************************************
# **********************************************************************************************************************

#!/usr/bin/python3
from Data.Database import Database


class Template:

    __temp_name = ""
    __temp_subject = ""
    __temp_body = ""

    def __init__(self, temp_name, temp_subject, temp_body):
        self.__temp_name = temp_name
        self.__temp_subject = temp_subject
        self.__temp_body = temp_body

    # getters
    def get_temp_name(self):
        return self.__temp_name

    def get_temp_subject(self):
        return self.__temp_subject

    def get_temp_body(self):
        return self.__temp_body

    # setters
    def set_temp_name(self, temp_name):
        self.__temp_name = temp_name

    def set_temp_subject(self, temp_subject):
        self.__temp_subject = temp_subject

    def set_temp_body(self, temp_body):
        self.__temp_body = temp_body

    # Insert template to the database
    @staticmethod
    def submit_template(name_contents, subject_contents, message_contents):
        Database.write_template_data(name_contents, subject_contents, message_contents)

    # Check for template name in the database, return count
    @staticmethod
    def check_template_name(name_contents):
        name_count = Database.check_template_name(name_contents)

        return name_count