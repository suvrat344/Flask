from flask import Flask,render_template,request,redirect,url_for,make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


# Initalize the Flask application
app = Flask(__name__)


# Configure the SQLite database URI and track modifications setting
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///week7_database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Initialize SQLAlchemy
db = SQLAlchemy(app)
app.app_context().push()
db.create_all()


# Define the Student model
class Student(db.Model):
  __tablename__ = "student"
  student_id = db.Column(db.Integer,primary_key = True,autoincrement = True)
  roll_number = db.Column(db.String(50),unique = True,nullable = False)
  first_name = db.Column(db.String(50),nullable = False)
  last_name = db.Column(db.String(50))
  # Many-to-many relationship with courses through enrollment
  enroll_student = db.relationship("Course",secondary="enrollments")
 
  
# Define the Course model
class Course(db.Model):
  __tablename__ = "course"
  course_id = db.Column(db.Integer,primary_key = True,autoincrement = True)
  course_code = db.Column(db.String(50),unique = True,nullable = False)
  course_name = db.Column(db.String(50),nullable = False)
  course_description = db.Column(db.String(50))


# Define the Enrollments model for the many-to-many relationship
class Enrollments(db.Model):
  __tablename__ = "enrollments"
  enrollment_id = db.Column(db.Integer,primary_key = True,autoincrement = True)
  estudent_id = db.Column(db.Integer,db.ForeignKey("student.student_id"),nullable = False)
  ecourse_id = db.Column(db.Integer,db.ForeignKey("course.course_id"),nullable = False)
  

# Route to display all students
@app.route("/")
def get_students():
  students = Student.query.order_by(func.cast(Student.roll_number,db.Integer)).all()   
  if(students is not None):
    response = make_response(render_template("index.html",students=students))
    return response,200
    
  return render_template("index.html")


# Route to create a new student
@app.route("/student/create",methods=["GET","POST"])
def create_student():
  if(request.method == "POST"):
    roll = request.form.get("roll")
    f_name = request.form.get("f_name")
    l_name = request.form.get("l_name")
    student = Student.query.filter_by(roll_number = roll).first()
    if(student is None):
      s1 = Student(roll_number = roll,first_name = f_name,last_name = l_name)
      db.session.add(s1)
      db.session.commit()
      return redirect(url_for("get_students")),200
    else:
      return f'''
                <p>Student already exists. Please use different Roll Number!</p>
                <a href="{ url_for('get_students') }"> Go Home </a>
             ''' 
  response = make_response(render_template("add_student.html"))
  return response,200
  
  
# Route to update an existing student's details and enroll them in a course
@app.route("/student/<int:student_id>/update",methods=["GET","POST"])
def update_student(student_id):
  student = Student.query.get(student_id)
  courses = Course.query.all()

  if(request.method == "POST"):
    student = Student.query.get(student_id)
    f_name = request.form.get("f_name")
    l_name = request.form.get("l_name")
    course = request.form.get("course")
    
    student.first_name = f_name
    student.last_name = l_name
    
    e1 = Enrollments(estudent_id=student_id,ecourse_id=course)
    db.session.add(e1)
    db.session.commit()
      
    return redirect(url_for("get_students")),200
  
  response = make_response(render_template("update_student.html",student=student,courses=courses))
  return response,200


# Route to delete a student and their enrollments
@app.route("/student/<int:student_id>/delete",methods=["GET","POST"])
def delete_student(student_id):
  Enrollments.query.filter_by(estudent_id=student_id).delete()
  student = Student.query.get(student_id)
  db.session.delete(student)
  db.session.commit()
  return redirect(url_for("get_students")),200


# Route to display details of a specific student
@app.route("/student/<int:student_id>",methods = ["GET","POST"])
def student_details(student_id):
  student = Student.query.get(student_id)
  enrollments = Enrollments.query.filter_by(estudent_id=student_id).all()
  courses = [Course.query.get(enrollment.ecourse_id) for enrollment in enrollments]
  response = make_response(render_template("student.html",student=student,courses=courses))
  return response,200


# Route to withdraw a student from a course
@app.route("/student/<int:student_id>/withdraw/<int:course_id>")
def withdraw_student(student_id,course_id):
  print(student_id,course_id)
  Enrollments.query.filter_by(estudent_id = student_id,ecourse_id = course_id ).delete()
  db.session.commit()
  return redirect(url_for("get_students")),200
  
 
# Route to display all courses
@app.route("/courses")
def get_courses():
  courses = Course.query.order_by(func.cast(Course.course_id,db.Integer)).all()   
  print(courses)
  if(courses is not None):
    response = make_response(render_template("course.html",courses=courses))
    return response,200
    
  return render_template("course.html"),200

# Route to create a new course
@app.route("/course/create",methods=["GET","POST"])
def create_course():
  if(request.method == "POST"):
    course_code = request.form.get("code")
    course_name = request.form.get("c_name")
    course_description = request.form.get("desc")
    course = Course.query.filter_by(course_code = course_code).first()
    if(course is None):
      c1 = Course(course_code = course_code,course_name = course_name,course_description = course_description)
      db.session.add(c1)
      db.session.commit()
      return redirect(url_for("get_courses")),200
    else:
      return f'''
                <p>Course already exists. Please create a different course !!</p>
                <a href="{ url_for('get_courses') }"> Go Home </a>
             ''' 
  response = make_response(render_template("add_course.html"))
  return response,200


# Route to update an existing course's details
@app.route("/course/<int:course_id>/update",methods=["GET","POST"])
def update_course(course_id):
  course = Course.query.get(course_id)

  if(request.method == "POST"):
    print(course_id)
    filter_course = Course.query.get(course_id)
    course_name = request.form.get("c_name")
    course_description = request.form.get("desc")
    
    filter_course.course_name = course_name
    filter_course.course_description = course_description
    
    db.session.commit()
      
    return redirect(url_for("get_courses")),200
  
  response = make_response(render_template("update_course.html",course = course))
  return response,200


# Route to delete a course and its enrollments
@app.route("/course/<int:course_id>/delete",methods=["GET","POST"])
def delete_course(course_id):
    Enrollments.query.filter_by(ecourse_id=course_id).delete()
    course = Course.query.get(course_id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for("get_students")),200


# Route to display details of a specific course
@app.route("/course/<int:course_id>",methods=["GET","POST"])
def course_details(course_id):
  course = Course.query.get(course_id)
  print(course)
  enrollments = Enrollments.query.filter_by(ecourse_id = course_id).all()
  students = [Student.query.get(enrollment.estudent_id) for enrollment in enrollments]
  response = make_response(render_template("course_detail.html",students = students,course = course))
  return response,200
 
 
# Run the application  
if __name__ == "__main__":
  app.run(debug = True)