import json, bcrypt, secrets, hashlib
from flask import Flask, render_template, request, jsonify, Blueprint, make_response
from routes.database_handler import *
from routes.function_handler import *

auth_blueprint = Blueprint("auth_blueprint", __name__, template_folder="templates")


# auth routing framework
@auth_blueprint.route("/auth", methods=["POST"])
def auth():
    # Getting JSON request and filling variables
    received_data = request.get_json()
    username = received_data.get("username")
    password = received_data.get("password")

    # HTML escape characters
    username = escape_html(username)

    # Getting record of username
    user_list = db_find_by_username(username)

    # Checking if a field is empty
    if not username or not password:
        response_data = {"status": "error", "message": "Empty Field"}
    # If username not found
    elif not user_list:
        response_data = {"status": "error", "message": "Invalid Credentials"}
    # Adding salt to given pw, hashing, then comparing to known user hash
    else:
        user_password = user_list[0]["hash"]
        user_salt = user_list[0]["salt"]
        password = password.encode()

        check_pass = bcrypt.hashpw(password, user_salt)

        if check_pass == user_password:

            # Making auth token log2(64^256) = 1536 bits of entropy
            auth_token = db_update_auth_token(username)

            # Making response
            response_data = {"status": "success", "message": "Welcome " + username}
            response = make_response(jsonify(response_data))
            response.set_cookie("auth_token", auth_token, httponly=True)

            return response
        else:
            response_data = {"status": "error", "message": "Invalid Credentials"}

    return jsonify(response_data)


@auth_blueprint.route("/register", methods=["POST"])
def register():
    # Getting JSON request and filling variables
    received_data = request.get_json()
    username = received_data.get("username")
    password = received_data.get("password")
    password_confirm = received_data.get("password_confirm")

    # HTML escape characters
    username = escape_html(username)

    # Checking if there will be duplicate username
    user_list = db_find_by_username(username)

    # Empty Field
    if not username or not password or not password_confirm:
        response_data = {"status": "error", "message": "Empty Field"}

    # Duplicate Username
    elif user_list:
        response_data = {"status": "error", "message": "Username Taken"}

    # Password Missmatch
    elif password != password_confirm:
        response_data = {"status": "error", "message": "Password Mismatch"}

    # Register User
    else:
        db_register_user(username)
        response_data = {"status": "success", "message": "Registration Successful"}

    return jsonify(response_data)
