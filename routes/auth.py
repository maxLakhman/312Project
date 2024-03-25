from datetime import datetime, timedelta
from typing import List, Tuple, Any, Dict, Optional
import bcrypt
import hashlib
import secrets
from flask import Blueprint, jsonify, make_response, redirect, request, url_for, current_app
from flask_login import UserMixin, login_required, login_user, logout_user
from flask_login import LoginManager
from pymongo import MongoClient

login_manager = LoginManager()

auth_blueprint = Blueprint("auth_blueprint", __name__, template_folder="templates")
mongo_client = MongoClient("db")
db = mongo_client["BlackJack"]
user_collection = db["user"]


class User(UserMixin):
    """User class for Flask-Login"""
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(username):
    """Load user for Flask-Login"""
    if get_user(username):
        return User(username)
    return None


def escape_html(username: str) -> str:
    """Escape HTML characters in the username to prevent XSS attacks"""
    return username.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def get_user(username: str) -> List[Dict[str, Any]]:
    """Query the database for a user with the given username"""
    user_cursor = user_collection.find({"username": username})
    return list(user_cursor)


def is_empty(*args: Any) -> bool:
    """Check if any of the given arguments are empty"""
    return any(not arg for arg in args)


def create_response(status: str, message: str) -> Dict[str, str]:
    """Create a JSON response with the given status and message"""
    return jsonify({"status": status, "message": message})


def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """Hash and salt the password for secure storage"""
    password = password.encode()
    if not salt:
        salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt), salt


@auth_blueprint.route("/auth", methods=["POST"])
def auth() -> Dict[str, str]:
    """Handle the authentication process"""
    received_data = request.get_json()
    username = escape_html(received_data.get("username"))
    password = received_data.get("password")

    user_list = get_user(username)

    if is_empty(username, password):
        return create_response("error", "Empty Field")
    elif not user_list:
        return create_response("error", "Invalid Credentials")
    else:
        user_password = user_list[0]["hash"]
        user_salt = user_list[0]["salt"]
        check_pass, _ = hash_password(password, user_salt)

        if check_pass == user_password:
            login_user(User(username))

            auth_token = secrets.token_urlsafe(256)
            token_hash = hashlib.sha256(auth_token.encode()).hexdigest()
            user_collection.update_one(
                {"username": username}, {"$set": {"auth_token": token_hash}}
            )

            response_data = {"status": "success", "message": f"Welcome {username}"}
            response = make_response(jsonify(response_data))
            expires = datetime.now() + timedelta(hours=1)
            response.set_cookie("auth_token", auth_token, expires=expires, httponly=True)
            return response
        else:
            return create_response("error", "Invalid Credentials")


@auth_blueprint.route("/register", methods=["POST"])
def register() -> Dict[str, str]:
    """Handle the registration process"""
    received_data = request.get_json()
    username = escape_html(received_data.get("username"))
    password = received_data.get("password")
    password_confirm = received_data.get("password_confirm")

    user_list = get_user(username)

    if is_empty(username, password, password_confirm):
        return create_response("error", "Empty Field")
    elif user_list:
        return create_response("error", "Username Taken")
    elif password != password_confirm:
        return create_response("error", "Password Mismatch")
    else:
        password_hash, salt = hash_password(password)

        record = {
            "username": username,
            "hash": password_hash,
            "salt": salt,
            "tokens": 500,
        }
        user_collection.insert_one(record)

        if not user_list and password == password_confirm:
            login_user(User(username))
            return create_response("success", "Registration Successful")


@auth_blueprint.route("/logout")
@login_required
def logout():
    """Handle the logout process"""
    logout_user()
    return redirect(url_for('home'))

