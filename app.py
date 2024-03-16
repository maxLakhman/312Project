from flask import Flask, render_template
from routes.auth import auth_blueprint
from routes.chat import chat_blueprint

app = Flask(__name__)
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


if __name__ == '__main__':
    app.run(debug=True, port=8080)
