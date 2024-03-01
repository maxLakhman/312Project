from flask import Flask, render_template
from flask_pymongo import PyMongo


app = Flask(__name__)

# Connecting MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/BlackJack"
mongo = PyMongo(app)

# Making Tables
user_table = mongo.db.user
password_table = mongo.db.password
chat_table = mongo.db.table



# index page
@app.route('/')
def home():
    return render_template('index.html')

# setting nosniff header
@app.after_request
def set_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

# auth routing framework
@app.route('/auth')
def auth():
    # parse the login info from the request here
    
    return

# register routing framework
@app.route('/register')
def register():
    # do the registering stuff here
    
    return


if __name__ == '__main__':
    app.run(debug=True, port=8080)
