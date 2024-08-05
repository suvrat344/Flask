import sys
import csv
from jinja2 import Template
import matplotlib.pyplot as plt


# Open the CSV file for reading
file1 = open("data.csv",mode="r")
csv_dict_reader = csv.DictReader(file1)


# Read the header (field names) from the CSV file
header = csv_dict_reader.fieldnames

data = []    # List to store the processed CSV data
marks = []   # List to store marks for the specified course


# Process each row in the CSV file
for row in csv_dict_reader:
  dict = {}
  # Strip leading/trailing whitespace from keys and values
  for key,value in row.items():
    dict[key.lstrip()] = value.lstrip()
  dict["Marks"] = int(dict["Marks"])    # Convert marks to integer
  data.append(dict)                     # Add the processed dictionary to data list
  
  # If the course id matches the argument, add the marks to the marks list
  if(sys.argv[2] == dict["Course id"]):
    marks.append(dict["Marks"])
    
    
# Read the HTML template file
with open("template1.html",mode="r") as file2:
  temp = file2.read()
  
# Create a Jinja2 Template object from the template string
template = Template(temp)


# Function to check if the provided ID is valid
def IsValid(flag,id,data):
  for row in data:
    if(flag == "-s"):
      if(id == row["Student id"]):
        return True
    elif(flag == "-c"):
      if(id == row["Course id"].lstrip()):
        return True
    else:
      return False
  
  
# Check if the argument is for a student and if the student ID is valid
if(sys.argv[1] == "-s" and IsValid(sys.argv[1],sys.argv[2],data)):
  # Render the template with student data
  output = template.render(data = data,header = header,title = "Student",student_id = sys.argv[2])
  # Write the rendered HTML to output.html
  with open("output.html","w") as file3:
    file3.write(output)

# Check if the argument is for a course and if the course ID is valid 
elif(sys.argv[1] == "-c" and IsValid(sys.argv[1],sys.argv[2],data)):
  # Plot histogram for given course id
  plt.hist(x = marks,bins = 10)
  plt.xlabel("Marks")
  plt.ylabel("Frequency")
  plt.savefig("course.jpg")     # # Save histogram as an image file
  
  # Render the template with course data
  output = template.render(data=data,title = "Course",course_id = sys.argv[2])
  # Write the rendered HTML to output.html
  with open("output.html","w") as file3:
    file3.write(output)

# Handle invalid arguments or IDs 
else:
  # Render the template for wrong inputs
  output = template.render(title = "Wrong")
  file3 = open("output.html","w")
  file3.write(output)


# Close the CSV file
file1.close()