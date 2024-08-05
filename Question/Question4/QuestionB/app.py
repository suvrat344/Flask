from flask import Flask,render_template,request
import csv
import matplotlib
import matplotlib.pyplot as plt


# Set the backend for matplotlib to work in a non-interactive environment
matplotlib.use("agg")


# Initialize the Flask application
app = Flask(__name__)


# Read data from CSV file
with open("data.csv",newline = "") as csv_file:
  student_data = list(csv.reader(csv_file))


# Extract header from the CSV file
header = [student_data[0][0].strip(),student_data[0][1].strip(),student_data[0][2].strip()]
 
 
# Function to get details of a student by ID 
def get_student_detail(id_value):
  data = []
  total = 0
  for row in student_data:
    if(row[0] == id_value):
      data.append([row[0].strip(),row[1].strip(),row[2].strip()])
      total = total + int(row[2].strip())
  
  # Return 0,0 if no data found
  if(data == []):
    return 0,0
      
  return data,total


# Function to get course details by course ID
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
      
  # Return 0,0,0 if no data found
  if(data == []):
    return 0,0,0
  
  # Calculate average
  average = total/counter
  return data,average,maximum


# Route for the home page
@app.route("/",methods = ["GET","POST"])
def index():
  if(request.method == "GET"):
    return render_template("index.html")
  elif(request.method == "POST"):
    # Check if the form is for student details
    if(request.form.get("ID") == "student_id"):
      id_value = request.form.get("id_value")
      
      data,total = get_student_detail(id_value)
      # Render student detail page or show an error if no data found
      if(data != 0):
        return render_template("student_detail.html",header = header,data =  data,total = total)
      else:
        return '''<h1> Wrong Inputs </h1>
                  <p> Something went wrong </p>
                  <a href = "/"> Go Back </a>
              '''
    # Check if the form is for course details
    else:
      id_value = request.form.get("id_value")
      data,average_marks,maximum_marks = get_course_detail(id_value)
      
      # Generate histogram and render course detail page or show an error if no data found
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
  
            
# Run the Flask application
if __name__ == "__main__": 
  app.run(debug=True)