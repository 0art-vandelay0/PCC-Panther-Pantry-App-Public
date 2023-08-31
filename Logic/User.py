# **********************************************************************************************************************
# **********************************************************************************************************************   
# Authors:           Erika Brooks, Casey Hill
# **********************************************************************************************************************
# **********************************************************************************************************************  

from Data.Database import Database


class User:

    def __init__(self, first_name, last_name, username, email, user_pass, user_role):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.user_pass = user_pass
        self.user_role = user_role

    # setters
    def set_first_name(self, new_first_name):
        self.first_name = new_first_name

    def set_last_name(self, new_last_name):
        self.last_name = new_last_name

    def set_username(self, new_username):
        self.username = new_username

    def set_email(self, new_email):
        self.email = new_email

    def set_user_pass(self, new_user_pass):
        self.user_pass = new_user_pass

    def set_user_role(self, new_role):
        self.user_role = new_role

    # getters
    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def get_user_pass(self):
        return self.user_pass

    def get_user_role(self):
        return self.user_role

    # searches to see if user already exists
    @staticmethod
    def find_user(username, email):
        return Database.find(username, email)

    # saves user to database
    def save_user(self):
        return Database.save(self.first_name, self.last_name, self.username, self.user_role, self.email,
                             self.user_pass)

    # the below proves DB functionality
    @staticmethod
    def pull_user_data():
        Database.read_user_data()

    #searches for existing user using email or username and password and returns the stored password hash
    @staticmethod
    def get_user_hash(username_or_email):
        return Database.get_hash(username_or_email)


