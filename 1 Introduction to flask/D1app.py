from flask import Flask

# Create the flask app
app = Flask(__name__)


# HomePage
@app.route("/")
@app.route("/home")
def home():
  return "<h1> Welcome to the Home Page!</h1>"


# About Page
@app.route("/about")
def about():
  return "<h1> Welcome to the About Page!</h1>"


# Example of path parameter
@app.route("/welcome/<name>")
def welcome(name):
  return f"<h1>Hi {name.title()}, you're welcome to this Page!</h1>"


# Example of integer path parameter
@app.route("/addition/<int:num>")
def addition(num):
  return f"<h1> Input is {num}, Output is {num + 10}</h1>"


# Example of two integer path parameter
@app.route("/addition_two/<int:num1>/<int:num2>")
def addition_two(num1,num2):
  return f"<h1>{num1} + {num2} = {num1 + num2}</h1>"


if __name__ == "__main__":
  app.run(debug=True)