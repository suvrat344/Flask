import time
from flask import Flask,redirect,url_for

app = Flask(__name__)

@app.route("/")
def home():
  return "<h1>Welcome to the home page!"


@app.route("/pass")
def passed():
  return f"<h1>Congratz, you 've passed !</h1>"


@app.route("/fail")
def failed():
  return f"<h1>Sorry, you 've failed with marks!</h1>"


@app.route("/score/<name>/<int:num>")
def score(name,num):
  if(num < 30):
    time.sleep(1)
    # redirect user to fail page
    return redirect(url_for("failed"))
  else:
    time.sleep(1)
    # redirect user to pass page
    return redirect(url_for("passed"))

if __name__ == "__main__":
  app.run(debug=True)