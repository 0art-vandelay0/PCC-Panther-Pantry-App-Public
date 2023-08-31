# **********************************************************************************************************************
# **********************************************************************************************************************
# Author:           Teresa Harris, Casey Hill
# **********************************************************************************************************************
# **********************************************************************************************************************
import bcrypt
# Web UI for Food insecurity notification system

# imports
from flask import Flask, render_template, request
from Logic.User import User
import bcrypt


class FoodPantryWebUI:
    app = Flask(__name__)
    #bcrypt = bcrypt(app)

    @staticmethod
    @app.route("/")
    @app.route("/index")
    @app.route("/index.html")
    def homepage():
        menu_choices = {
            "/account_login_form": "Account Login",
            "/new_subscriber_form": "Create new subscriber",

        }
        return render_template("index.html", menu_choices=menu_choices)

    # Account Login form
    @staticmethod
    @app.route("/account_login_form")
    def account_login_form():
        return render_template("account_login_form.html")

    # back end of user log in
    @staticmethod
    @app.route("/account_login", methods=["POST"])
    def account_login():
        username_or_email = request.form["username_or_email"]
        user_pass = request.form["user_pass"]
        user_hash = User.get_user_hash(username_or_email)
        if user_hash is None:
            return render_template("error.html", error_header="Error!",
                                   error="Invalid username, email, or password. Please try again")
        if bcrypt.checkpw(user_pass.encode(), user_hash[0]) is True:
            return render_template("account_logged_in.html")
        else:
            return render_template("error.html", error_header="Error!",
                                   error="Invalid username, email, or password. Please try again")

    # New subscriber form
    @staticmethod
    @app.route("/new_subscriber_form")
    def new_subscriber_form():
        return render_template("new_subscriber_form.html")

    # back end of adding a new subscriber to the database
    @staticmethod
    @app.route("/new_subscriber", methods=["POST"])
    def new_subscriber():
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        username = request.form["username"]
        email = request.form["email"]
        user_pass = request.form["user_pass"]
        user_pass2 = request.form["user_pass2"]
        user_role = "subscriber"
        if user_pass == user_pass2:
            hashed_pass = bcrypt.hashpw(user_pass.encode(), bcrypt.gensalt())
            user = User.find_user(username, email)
            if user is None:
                user = User(first_name, last_name, username, email, hashed_pass, user_role)
            else:
                return render_template("error.html", error_header="Error!",
                                       error="something went wrong, please try again")
        else:
            return render_template("error.html", error_header="Error!",
                                   error="Passwords must match, please try again")
        user.save_user()
        return render_template("subscriber_created.html")

    @staticmethod
    def run():
        FoodPantryWebUI.app.run(port=8080)


if __name__ == "__main__":
    FoodPantryWebUI.run()
