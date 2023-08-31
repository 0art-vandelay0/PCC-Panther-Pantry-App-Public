from unittest import TestCase
from User import User

class TestUser(TestCase):
    def test_constructor(self):
        first_name = "Marc"
        last_name = "Goodman"
        username = "marc.goodman"
        email = "marc.goodman@pcc.edu"
        user_pass = "testme"
        user_role = "subscriber"
        user = User(first_name, last_name, username, email, user_pass, user_role)
        self.assertEqual(first_name, user.get_first_name())
        self.assertEqual(last_name, user.get_last_name())
        self.assertEqual(username, user.get_username())
        self.assertEqual(email, user.get_email())
        self.assertEqual(user_pass, user.get_user_pass())
        self.assertEqual(user_role, user.get_user_role())

    def test_set_username(self):
        user = User("", "", "start", "", "", "")
        self.assertEqual("start", user.get_username())
        user.set_username("new")
        self.assertEqual("new", user.get_username())

    def test_find_user(self):
        user = User.find_user("Marc", "marc.goodman@pcc.edu")
        self.assertIsNotNone(user)
        self.assertEqual("Marc", user[3])
        self.assertEqual("marc.goodman@pcc.edu", user[5])
        self.assertEqual("Manager", user[4])
