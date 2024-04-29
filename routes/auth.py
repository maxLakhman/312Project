from datetime import datetime, timedelta
from typing import List, Tuple, Any, Dict, Optional
import bcrypt, hashlib, secrets, os, magic
from flask import (
    Blueprint,
    jsonify,
    make_response,
    redirect,
    request,
    url_for,
    current_app,
)
from flask_login import UserMixin, login_required, login_user, logout_user, current_user
from flask_login import LoginManager
from pymongo import MongoClient


login_manager = LoginManager()

auth_blueprint = Blueprint("auth_blueprint", __name__, template_folder="templates")
mongo_client = MongoClient("db")
db = mongo_client["BlackJack"]
user_collection = db["user"]
id_collection = db["id"]


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
            response.set_cookie(
                "auth_token", auth_token, expires=expires, httponly=True
            )
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

    valid_pw = password_isvalid(password)

    user_list = get_user(username)
    if is_empty(username, password, password_confirm):
        return create_response("error", "Empty Field")
    elif user_list:
        return create_response("error", "Username Taken")
    elif password != password_confirm:
        return create_response("error", "Password Mismatch")
    elif "error" in valid_pw:
        return create_response("error", valid_pw["error"])
    else:

        password_hash, salt = hash_password(password)

        auth_token = secrets.token_urlsafe(256)
        token_hash = hashlib.sha256(auth_token.encode()).hexdigest()
        record = {
            "username": username,
            "balance": 1000,
            "bet": 0,
            "hash": password_hash,
            "salt": salt,
            "auth_token": token_hash,
            "tokens": 500,
        }
        user_collection.insert_one(record)

        if not user_list and password == password_confirm:
            login_user(User(username))
            response = create_response("success", "Registration Successful")
            expires = datetime.now() + timedelta(hours=1)
            response.set_cookie(
                "auth_token", auth_token, expires=expires, httponly=True
            )
            return response


@auth_blueprint.route("/logout")
@login_required
def logout():
    """Handle the logout process"""
    user = db_verify_auth_token(request)
    if user:
        # Updates auth token with random token
        auth_token = secrets.token_urlsafe(256)
        token_hash = hashlib.sha256(auth_token.encode()).hexdigest()
        user_collection.update_one(
            {"username": user.get("username")}, {"$set": {"auth_token": token_hash}}
        )
    logout_user()
    return redirect(url_for("home"))


def db_verify_auth_token(request):
    if "auth_token" in request.cookies:
        browser_token = request.cookies.get("auth_token")
        hashed_browser_token = hashlib.sha256(browser_token.encode()).hexdigest()

        user = user_collection.find_one(
            {"auth_token": hashed_browser_token}, {"_id": 0}
        )
        return user
    return False


def get_mime_type(file):
    mime = magic.Magic(mime=True)
    file_content = file.read()
    file.seek(0)
    return mime.from_buffer(file_content)


# Sets profile picture
@login_required
@auth_blueprint.route("/profile-pic", methods=["POST"])
def upload_profile_pic():
    file = request.files["profile_pic"]
    if file and (
        get_mime_type(file)
        in {"image/jpeg", "image/jpg", "image/webp", "image/png", "image/gif"}
    ):
        username = current_user.id

        # removing old pfp ########Commented out so old pfp will show in chat message ##########
        # old_pfp = user_collection.find_one(
        #     {"username": username}, {"profile_pic": 1}
        # ).get("profile_pic")

        # if old_pfp and os.path.isfile(old_pfp):
        #     print(old_pfp)
        #     os.remove(old_pfp)

        filename = get_id()
        upload_path = "static/images/profiles"
        file_path = os.path.join(upload_path, str(filename))
        file.save(file_path)
        user_collection.update_one(
            {"username": username}, {"$set": {"profile_pic": file_path}}
        )
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "File uploaded successfully",
                    "filepath": file_path,
                }
            ),
            200,
        )
    elif not file:
        return jsonify({"status": "error", "message": "No file selected"}), 400
    else:
        return jsonify({"status": "error", "message": "Image type not supported"}), 400


def get_id():
    # If the id_collection is empty create id #1
    if not list(id_collection.find({})):
        id_collection.insert_one({"_id": 1, "id": 1})

    json_id = id_collection.find_one({})
    id = json_id.get("id")
    id_collection.update_one({"_id": 1}, {"$set": {"id": (int(id) + 1)}})
    return id


def password_isvalid(password: str):
    # Array of special chars

    char_list = [
        "~",
        ":",
        "'",
        "+",
        "[",
        "\\",
        "@",
        "^",
        "{",
        "%",
        "(",
        "-",
        '"',
        "*",
        "|",
        ",",
        "&",
        "<",
        "`",
        "}",
        ".",
        "_",
        "=",
        "]",
        "!",
        ">",
        ";",
        "?",
        "#",
        "$",
        ")",
        "/",
    ]

    # All must be true
    valid_lower = False
    valid_upper = False
    valid_digit = False
    special_char = False

    pass_list = []

    for char in password:
        pass_list.append(char)

    if len(pass_list) < 8:
        return {"error": "Password length must be ≥ 8"}

    # Iterating through list of chars
    for char in pass_list:
        if char.isupper():
            valid_upper = True
        elif char.islower():
            valid_lower = True
        elif char.isdigit():
            valid_digit = True
        elif char in char_list:
            special_char = True
        else:
            return {"error": {"Invalid character in password"}}

    # Checking if password contains all
    if valid_lower and valid_upper and valid_digit and special_char:
        return {"success": "Valid"}
    elif not valid_lower:
        return {"error": "Password must contain at least one lowercase letter"}
    elif not valid_upper:
        return {"error": "Password must contain at least one uppercase letter"}
    elif not valid_digit:
        return {"error": "Password must contain at least one number"}
    elif not special_char:
        return {"error": "Password must contain at least one special character"}
    else:
        return {"penis": "penis"}
