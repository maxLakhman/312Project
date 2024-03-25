from flask import Flask, render_template
from flask_login import LoginManager, current_user
from routes.auth import auth_blueprint, load_user
from routes.chat import chat_blueprint

app = Flask(__name__)
app.secret_key = "super_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)

# Set the user_loader function
login_manager.user_loader(load_user)


app.register_blueprint(auth_blueprint)
app.register_blueprint(chat_blueprint)


@app.route('/')
def home():
    """Render the index page."""
    return render_template('index.html')


@app.route('/settings.html')
def open_settings():
    """Render the settings page."""
    return render_template('settings.html')


@app.after_request
def set_header(response):
    """Set the 'X-Content-Type-Options' header to 'nosniff'."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response



# lobby stuff
@app.route('/lobby')
def lobby():
    # call to open the lobby page
    return render_template('lobby.html')



# creating a blackjack table
@app.route('/create-table', methods=['POST'])
def create_table():

    # finding the user who created the through their auth token
    user = request.cookies.get('auth_token')

    # creating a new table after request received
    received_data = request.get_json()
    table_name = "Table " + str(table_collection.count_documents({}) + 1)

    # retrieve the player name who created the table
    author_name = received_data.get('player_name')

    # set a uuid for the table
    table_id = str(uuid.uuid4())

    # HTML escape
    table_name = table_name.replace('&', '&amp;')
    table_name = table_name.replace('<', '&lt;')
    table_name = table_name.replace('>', '&gt;')

    # creating the table
    table_collection.insert_one({"table_id": table_id, "table_name": table_name, "players": [author_name]})

    # send the user to the table page
    return redirect(url_for('table', table_id=table_id))


# lobby stuff
@app.route('/lobby')
def lobby():
    # call to open the lobby page
    return render_template('lobby.html')



# creating a blackjack table
@app.route('/create-table', methods=['POST'])
def create_table():

    # finding the user who created the through their auth token
    user = request.cookies.get('auth_token')

    # creating a new table after request received
    received_data = request.get_json()
    table_name = "Table " + str(table_collection.count_documents({}) + 1)

    # retrieve the player name who created the table
    author_name = received_data.get('player_name')

    # set a uuid for the table
    table_id = str(uuid.uuid4())

    # HTML escape
    table_name = table_name.replace('&', '&amp;')
    table_name = table_name.replace('<', '&lt;')
    table_name = table_name.replace('>', '&gt;')

    # creating the table
    table_collection.insert_one({"table_id": table_id, "table_name": table_name, "players": [author_name]})

    # send the user to the table page
    return redirect(url_for('table', table_id=table_id))

if __name__ == '__main__':
    app.run(debug=True, port=8080)
