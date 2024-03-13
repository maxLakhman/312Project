import json, bcrypt
from flask import Flask, render_template, request
from routes.auth import auth_blueprint
from routes.chat import chat_blueprint

app = Flask(__name__)
app.register_blueprint(auth_blueprint)
app.register_blueprint(chat_blueprint)

# index page
@app.route('/')
def home():
    return render_template('index.html')

# setting nosniff header

#settings page
#docker compose up --build --force-recreate
@app.route('/settings.html')
def openSettings():
    return render_template('settings.html')

@app.after_request
def set_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8080)
