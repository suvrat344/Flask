from flask import Flask,render_template,request

app = Flask(__name__)

@app.route("/register",methods = ['GET','POST'])
def register():
  if(request.method == "POST"):
    name = request.form.get("stud_name")
    gender = request.form.get("gender")
    age = request.form.get("age")
    qualification = request.form.get("qual")
    stream = request.form.get("stream")
    address = request.form.get("address")
    return render_template("review.html",name = name,gender = gender,age = age,qualification = qualification,stream = stream,address = address)
    
  return render_template("register.html")

@app.route("/success")
def success():
  return "<h1>Form Submitted Successfully </h1>"

app.run(debug = True)