# **********************************************************************************************************************
# **********************************************************************************************************************   
#
# This file interacts with the Panther Pantry Database
#
# **********************************************************************************************************************
# **********************************************************************************************************************
# comments

# define imports
import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

# Connects to the database (the db credentials are hidden in your .env file)
class Database:
    __connection = None

    @classmethod
    def connect(cls):
        if cls.__connection == None:
            server = os.getenv('DB_SERVER')
            database = os.getenv('DB_NAME')
            username = os.getenv('DB_USER')
            password = os.getenv('DB_PASSWORD')
            trustedconnection = 'yes'
            trustservercertificate = 'yes'
            try:
                cls.__connection = pyodbc.connect(
                    'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + server + ';DATABASE=' + database
                    + ';UID=' + username + ';PWD=' + password
                    + ';trustedconnection=' + trustedconnection
                    + ';trustservercertificate=' + trustservercertificate
                )
            except pyodbc.InterfaceError:
                cls.__connection = pyodbc.connect(
                    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database
                    + ';UID=' + username + ';PWD=' + password
                )

    # test code to ensure DB functionality
    @classmethod
    def read_user_data(cls):
        cls.connect()
        my_cursor = cls.__connection.cursor()
        my_cursor.execute("SELECT * FROM team;")
        users_list = []
        rows = my_cursor.fetchall()

        for r in rows:
            users_list.append({"users_id: ": r[0], "name:": r[1]})
        print(users_list)

    # as called from Notification.notification_to_database
    # Write an emailed notification to the DB
    @classmethod
    def add_notification_to_database(cls, current_user, date, subject, message, count_of_list):

        cls.connect()
        my_cursor = cls.__connection.cursor()
        query = ('''
                INSERT INTO notifications
                (note_senderid, note_senddate, note_subject, note_body, note_numbersent)
                VALUES
                (?,?,?,?,?)
                '''
                 )
        my_cursor.execute(query, current_user, date, subject, message, count_of_list)
        my_cursor.commit()

    # as called from SendEmail.get_recipient_list
    # pull a list of email addresses from the database
    # exclude email addresses where the role is not Subscriber
    # return the resulting list
    @classmethod
    def get_all_emails(cls):
        cls.connect()
        my_cursor = cls.__connection.cursor()
        my_cursor.execute('''
                                  SELECT users_email
                                  FROM users
                                  WHERE LOWER(users_role) = 'subscriber'
                                  '''
                          )
        email_list = []
        emaillist_rows = my_cursor.fetchall()

        for email in emaillist_rows:
            email_list.append(email[0])
        # print('list printing from Database.get_all_emails', email_list)
        return email_list

    # finds user in database using username and email which is unique
    @classmethod
    def find(cls, username, email):
        cls.connect()
        my_cursor = cls.__connection.cursor()
        sql = """
            SELECT *                          
            FROM users 
            WHERE users_username = ? 
            AND users_email = ?;
        """
        my_cursor.execute(sql, username, email)
        row = my_cursor.fetchone()
        return row

    # searches for existing user and fetches the stored hashed password
    @classmethod
    def get_hash(cls, username_or_email):
        cls.connect()
        my_cursor = cls.__connection.cursor()
        my_search_parameter = username_or_email.lower()
        my_cursor.execute('''
                SELECT  users_password
                FROM    users
                WHERE   LOWER(users_username) = ?
                OR LOWER(users_email) = ? 
            ''', my_search_parameter, my_search_parameter)
        row = my_cursor.fetchone()
        # print(row)
        return row

    # finds users role in database using username or email
    @classmethod
    def get_role(cls, username_or_email):
        cls.connect()
        my_cursor = cls.__connection.cursor()
        sql = """
            SELECT users_role                          
            FROM users 
            WHERE users_username = ? 
            OR users_email = ?;
        """
        my_cursor.execute(sql, username_or_email, username_or_email)
        row = my_cursor.fetchone()
        return row

    @classmethod
    def get_userid(cls, username_or_email):
        cls.connect()
        my_cursor = cls.__connection.cursor()
        sql = """
            SELECT users_id                          
            FROM users 
            WHERE users_username = ? 
            OR users_email = ?;
        """
        my_cursor.execute(sql, username_or_email, username_or_email)
        row = my_cursor.fetchone()
        return row

    # saves a new user to the users table
    @classmethod
    def save(cls, first_name, last_name, username, user_role, email, hashed_pass):
        if cls.__connection is None:
            cls.connect()
        my_cursor = cls.__connection.cursor()
        my_cursor.execute('''INSERT INTO users (users_firstname, users_lastname, users_username,
        users_role, users_email, users_password)
                          VALUES(?, ?, ?, ?, ?, ?);
                          ''', first_name, last_name, username, user_role, email, hashed_pass)
        my_cursor.commit()

    @classmethod
    # Write data to the templates database
    def write_template_data(cls, name_contents, subject_contents, message_contents):
        # connect to the database
        cls.connect()

        # Execute the SQL query to insert template data into the template table
        my_cursor = cls.__connection.cursor()
        my_cursor.execute("INSERT INTO templates (temp_name, temp_subject, temp_body) VALUES (?, ?, ?)",
                       (name_contents, subject_contents, message_contents))
        my_cursor.commit()

        # Close database connection
        my_cursor.close()

    @classmethod
    # Check for the name of template before submitting
    def check_template_name(cls, name_contents):

        # Connect to the database
        cls.connect()

        # execute the SQL query to check if the template name exists in the table
        my_cursor = cls.__connection.cursor()
        my_cursor.execute("SELECT COUNT(*) FROM templates WHERE temp_name = ?",
                          name_contents)

        # get a count of rows returned
        count = my_cursor.fetchone()[0]

        # Close database connection
        my_cursor.close()

        return count

    @classmethod
    def get_notifications(cls, start_date, end_date):
        sql = '''
                SELECT notifications.note_id, CONCAT(users.users_firstname, ' ', users.users_lastname) AS sender_name, notifications.note_senddate, notifications.note_subject, notifications.note_body,
                notifications.note_numbersent
                FROM notifications JOIN users
                ON notifications.note_senderid = users.users_id
                WHERE note_senddate BETWEEN ? AND ?;
                '''
        cls.connect()
        cursor = cls.__connection.cursor()
        cursor.execute(sql, start_date, end_date)
        notifications = cursor.fetchall()
        return notifications
    @classmethod
    def delete_notification_by_id(cls, notification_id):
        cls.connect()
        cursor = cls.__connection.cursor()
        cursor.execute("DELETE FROM notifications WHERE note_id = ?", (notification_id,))
        cls.__connection.commit()
        print("message deleted")
