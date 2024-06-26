import sys
import csv
from jinja2 import Template
import matplotlib.pyplot as plt


file1 = open("data.csv",mode="r")
csv_dict_reader = csv.DictReader(file1)
header = csv_dict_reader.fieldnames

data = []
marks = []

for row in csv_dict_reader:
  dict = {}
  for key,value in row.items():
    dict[key.lstrip()] = value.lstrip()
  dict["Marks"] = int(dict["Marks"])
  data.append(dict)
  if(sys.argv[2] == dict["Course id"]):
    marks.append(dict["Marks"])
    

with open("template1.html",mode="r") as file2:
  temp = file2.read()
  
template = Template(temp)

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
  
  
if(sys.argv[1] == "-s" and IsValid(sys.argv[1],sys.argv[2],data)):
  print("Hello Student")
  output = template.render(data = data,header = header,title = "Student",student_id = sys.argv[2])
  with open("output.html","w") as file3:
    file3.write(output)
  
elif(sys.argv[1] == "-c" and IsValid(sys.argv[1],sys.argv[2],data)):
  print("Hello Course") 
  
  # Plot histogram for given course id
  plt.hist(x = marks,bins = 10)
  plt.xlabel("Marks")
  plt.ylabel("Frequency")
  plt.savefig("course.jpg")
  
  output = template.render(data=data,title = "Course",course_id = sys.argv[2])
  with open("output.html","w") as file3:
    file3.write(output)
    
else:
  print("Error")
  output = template.render(title = "Wrong")
  file3 = open("output.html","w")
  file3.write(output)


file1.close()