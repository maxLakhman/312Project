# Import the Flask class and the render_template function from the flask module
from flask import Flask, render_template

# Create an instance of the Flask class. This instance will be the WSGI application.
app = Flask(__name__)

# Define a route for the root URL ("/"). This means when a user visits the root URL,
# the function below this decorator will be executed.
@app.route('/')
def home():
    # The function that is called when the root URL is visited. It renders and returns
    # the 'index.html' template to the user.
    return render_template('index.html')

# Ensure the security header "X-Content-Type-Options: nosniff" is included in all responses.
# This is a security measure to prevent browsers from trying to guess (“sniff”) the MIME type,
# which can have security implications.
@app.after_request
def set_header(response):
    # Add the "X-Content-Type-Options: nosniff" header to the response.
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # Return the modified response
    return response

# Check if the script is executed as the main program and not imported as a module in another script.
# This is a common pattern for making sure the web server is started only when the script is executed directly.
if __name__ == '__main__':
    # Run the Flask application on the local development server.
    # 'debug=True' enables debug mode which will automatically reload the code upon changes
    # and provides a debugger if something goes wrong.
    # 'port=8080' specifies the port number (8080) on which the application will listen for incoming requests.
    app.run(debug=True, port=8080)
