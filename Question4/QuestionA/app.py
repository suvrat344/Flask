from flask import Flask,render_template,request


# Initialize the Flask application
app = Flask(__name__)


# Route to handle the registration form
@app.route("/register",methods = ['GET','POST'])
def register():
  if(request.method == "POST"):
    name = request.form.get("stud_name")
    gender = request.form.get("gender")
    age = request.form.get("age")
    qualification = request.form.get("qual")
    stream = request.form.get("stream")
    address = request.form.get("address")
    
    # Render the review page with the collected data
    return render_template("review.html",
                           name = name,
                           gender = gender,
                           age = age,
                           qualification = qualification,
                           stream = stream,
                           address = address)
    
  # Render the registration form page for GET request
  return render_template("register.html")


# Route to handle success message after form submission
@app.route("/success")
def success():
  return "<h1>Form Submitted Successfully </h1>"


# Run the Flask application
if __name__ == "__main__":
  app.run(debug = True)