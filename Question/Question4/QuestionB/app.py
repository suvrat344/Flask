from flask import Flask,render_template,request
import csv
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("agg")

app = Flask(__name__)

with open("data.csv",newline = "") as csv_file:
  student_data = list(csv.reader(csv_file))
  
header = [student_data[0][0].strip(),student_data[0][1].strip(),student_data[0][2].strip()]
  
def get_student_detail(id_value):
  data = []
  total = 0
  for row in student_data:
    if(row[0] == id_value):
      data.append([row[0].strip(),row[1].strip(),row[2].strip()])
      total = total + int(row[2].strip())
    
  if(data == []):
    return 0,0
      
  return data,total


def get_course_detail(id_value):
  data = []
  total,counter,maximum = 0,0,0
  for row in student_data:
    if(row[1].strip() == id_value):
      marks = int(row[2])
      total = total + marks
      counter = counter + 1
      
      data.append(marks)
      
      if(maximum < marks):
        maximum = marks    
      
  if(data == []):
    return 0,0,0
  average = total/counter
  return data,average,maximum


@app.route("/",methods = ["GET","POST"])
def index():
  if(request.method == "GET"):
    return render_template("index.html")
  elif(request.method == "POST"):
    if(request.form.get("ID") == "student_id"):
      id_value = request.form.get("id_value")
      
      data,total = get_student_detail(id_value)
      if(data != 0):
        return render_template("student_detail.html",header = header,data =  data,total = total)
      else:
        return '''<h1> Wrong Inputs </h1>
                  <p> Something went wrong </p>
                  <a href = "/"> Go Back </a>
              '''
    else:
      id_value = request.form.get("id_value")
      data,average_marks,maximum_marks = get_course_detail(id_value)
      
      if(average_marks != 0):
        plt.hist(x = data,bins = 10)
        plt.xlabel("Marks")
        plt.ylabel("Frequency")
        plt.savefig("static/course.jpg")
        plt.clf()
        return render_template("course_detail.html",average_marks = average_marks,maximum_marks = maximum_marks)
      else:
        return '''<h1>Wrong Inputs</h1>
                  <p>Something went wrong</p>
                  <a href = "/">Go Back</a>
              '''
if __name__ == "__main__": 
  app.run(debug=True)