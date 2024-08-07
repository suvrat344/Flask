from flask import Flask,render_template,request,redirect,url_for,make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


# Initialize the Flask application
app = Flask(__name__)

# Configure the database URI and disable track modification
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)
app.app_context().push()
db.create_all()


# Define the Student model
class Student(db.Model):
  student_id = db.Column(db.Integer,primary_key = True,autoincrement = True)
  roll_number = db.Column(db.String(50),unique = True,nullable = False)
  first_name = db.Column(db.String(50),nullable = False)
  last_name = db.Column(db.String(50))
  # Many-to-many relationship with Course through Enrollments
  stu_enrollment = db.relationship("Course",backref = "student_enrollment",secondary="enrollments")
 
  
# Define the Course Model
class Course(db.Model):
  course_id = db.Column(db.Integer,primary_key = True,autoincrement = True)
  course_code = db.Column(db.String(50),unique = True,nullable = False)
  course_name = db.Column(db.String(50),nullable = False)
  course_description = db.Column(db.String(50))
  #  Many-to-many relationship with Student through Enrollments
  cou_enrollment = db.relationship("Student",backref = "course_enrollment",secondary="enrollments")


# Define the Enrollments model for many-to-many relationships
class Enrollments(db.Model):
  enrollment_id = db.Column(db.Integer,primary_key = True,autoincrement = True)
  estudent_id = db.Column(db.Integer,db.ForeignKey("student.student_id"),nullable = False)
  ecourse_id = db.Column(db.Integer,db.ForeignKey("course.course_id"),nullable = False)
  

# Route to display all students, sorted by roll number
@app.route("/")
def get_students():
  students = Student.query.order_by(func.cast(Student.roll_number,db.Integer)).all()
  response = make_response(render_template("index.html",students=students))
  response.status_code = 200
  return response


# Route to create a new student
@app.route("/student/create",methods=["GET","POST"])
def create_student():
  if(request.method == "POST"):
    roll = request.form.get("roll")
    f_name = request.form.get("f_name")
    l_name = request.form.get("l_name")
    courses = request.form.getlist("courses")
    student = Student.query.filter_by(roll_number = roll).first()
    if(student is None):
      # Create a new student and commit to the database
      s1 = Student(roll_number = roll,first_name = f_name,last_name = l_name)
      db.session.add(s1)
      db.session.commit()
      student_id = s1.student_id
      # Add course enrollments for the new student
      for course in  courses:
        c1 = Course.query.filter_by(course_name=course).first()
        e1 = Enrollments(estudent_id=student_id,ecourse_id=c1.course_id)
        db.session.add(e1)
        db.session.commit()
      return redirect(url_for("get_students"))
    else:
      # If student already exists, show a message
      return f'''
                <p>Student already exists. Please use different Roll Number!</p>
                <a href="{ url_for('get_students') }"> Go Home </a>
             ''' 
  response = make_response(render_template("add_student.html"))
  response.status_code = 200
  return response
  

# Route to update an existing student 
@app.route("/student/<int:student_id>/update",methods=["GET","POST"])
def update_student(student_id):
  student = Student.query.get(student_id)
  courses = Course.query.all()
  enroll_course_id = [enrollment.ecourse_id for enrollment in  Enrollments.query.filter_by(estudent_id=student_id).all()]

  if(request.method == "POST"):
    student = Student.query.get(student_id)
    f_name = request.form.get("f_name")
    l_name = request.form.get("l_name")
    courses = request.form.getlist("courses")
    
    # Update student information
    student.first_name = f_name
    student.last_name = l_name
    db.session.commit()
    
    # Remove existing enrollments and add new ones
    Enrollments.query.filter_by(estudent_id = student_id).delete()
    for course in courses:
      c1 = Course.query.filter_by(course_name=course).first()
      e1 = Enrollments(estudent_id=student_id,ecourse_id=c1.course_id)
      db.session.add(e1)
      db.session.commit()
      
    return redirect(url_for("get_students"))
  
  response = make_response(render_template("update_student.html",student=student,courses=courses,enroll_course_id=enroll_course_id))
  response.status_code = 200
  return response


# Route to delete a student
@app.route("/student/<int:student_id>/delete",methods=["GET","POST"])
def delete_student(student_id):
  # Remove all enrollments for the student
  Enrollments.query.filter_by(estudent_id=student_id).delete()
  student = Student.query.get(student_id)
  # Delete the student record
  db.session.delete(student)
  db.session.commit()
  return redirect(url_for("get_students"))


# Route to display details of a student
@app.route("/student/<int:student_id>",methods = ["GET","POST"])
def student_details(student_id):
  student = Student.query.get(student_id)
  enrollments = Enrollments.query.filter_by(estudent_id=student_id).all()
  courses = [Course.query.get(enrollment.ecourse_id) for enrollment in enrollments]
  response = make_response(render_template("student.html",student=student,courses=courses))
  response.status_code = 200
  return response
  
  
# Run the Flask application
if __name__ == "__main__":
  app.run(debug = True)