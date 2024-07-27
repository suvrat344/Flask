# python -m pip install flask-restful

import json
from flask import Flask,request,make_response
from flask_restful import Api,Resource
from flask_restful import fields,marshal_with
from flask_restful import reqparse
from werkzeug.exceptions import HTTPException
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


# Configuring the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
app.app_context().push()    # Push the application context

api = Api(app)     # Initializing the Flask-RESTful API


# Output fields for marshaling the Course model
output_course = {
  "course_id":fields.Integer,
  "course_name": fields.String,
  "course_code": fields.String,
  "course_description": fields.String
}


# Output fields for marshaling the Student model
output_student = {
  "student_id": fields.Integer,
  "first_name": fields.String,
  "last_name": fields.String,
  "roll_number": fields.String
}


# Output fields for marshaling the Enrollment model
output_enrollment = {
  "enrollment_id": fields.Integer,
  "student_id": fields.Integer,
  "course_id": fields.Integer
}


# Parsers for validating and parsing incoming request data
create_course_parser = reqparse.RequestParser()
create_course_parser.add_argument("course_name")
create_course_parser.add_argument("course_code")
create_course_parser.add_argument("course_description")


create_student_parser = reqparse.RequestParser()
create_student_parser.add_argument("first_name")
create_student_parser.add_argument("last_name")
create_student_parser.add_argument("roll_number")


create_enrollment_parser = reqparse.RequestParser()
create_enrollment_parser.add_argument("course_id")


# Custom error classes for handling specific HTTP errors
class NotFoundError(HTTPException):
  def __init__(self,status_code,response):
    self.response = make_response(response,status_code)
    
    
class BusinessValidationError(HTTPException):
  def __init__(self,status_code,error_code,error_message):
    message = {"error_code" : error_code, "error_message": error_message }
    self.response = make_response(json.dumps(message), status_code)
    
    
class AlreadyExistError(HTTPException):
  def __init__(self,status_code,response):
    self.response = make_response(response,status_code)
    
    
# SQLAlchemy models for Student, Course, and Enrollment
class Student(db.Model):
  __tablename__ = "student"
  student_id = db.Column(db.Integer,primary_key = True,autoincrement = True)
  roll_number = db.Column(db.String(50),unique = True,nullable = False)
  first_name = db.Column(db.String(50),nullable = False)
  last_name = db.Column(db.String(50))
  # Many-to-many relationship with courses through enrollment
  enroll = db.relationship("Course",secondary="enrollment")
 
  
class Course(db.Model):
  __tablename__ = "course"
  course_id = db.Column(db.Integer,primary_key = True,autoincrement = True)
  course_name = db.Column(db.String(50),nullable = False)
  course_code = db.Column(db.String(50),unique = True,nullable = False)
  course_description = db.Column(db.String(50))


class Enrollment(db.Model):
  __tablename__ = "enrollment"
  enrollment_id = db.Column(db.Integer,primary_key = True,autoincrement = True)
  student_id = db.Column(db.Integer,db.ForeignKey("student.student_id"),nullable = False)
  course_id = db.Column(db.Integer,db.ForeignKey("course.course_id"),nullable = False)
  
  
# RESTful API resources for Course
class CourseApi(Resource):
  @marshal_with(output_course)
  def get(self,course_id):
    course = db.session.query(Course).filter(Course.course_id == course_id).first()
    if course:
      return course
    else:
      raise NotFoundError(response="Course not found",status_code = 404)
  
  
  @marshal_with(output_course)
  def post(self):
    args = create_course_parser.parse_args()
    course_name = args.get("course_name",None)
    course_code = args.get("course_code",None)
    course_description = args.get("course_description",None)
    
    if course_name is None:
      raise BusinessValidationError(status_code=400,error_code="COURSE001",error_message="Course Name is required")

    if course_code is None:
      raise BusinessValidationError(status_code=400,error_code="COURSE002",error_message="Course Code is required")
    
    course_exist = db.session.query(Course).filter(Course.course_code == course_code).first()
    
    if course_exist:
      raise AlreadyExistError(response = "course_code already exist",status_code = 409)
    
    new_course = Course(course_name = course_name,course_code = course_code,course_description = course_description)
    db.session.add(new_course)
    db.session.commit()
    
    return new_course,201


  @marshal_with(output_course)
  def put(self,course_id):
    args = create_course_parser.parse_args()
    course_name = args.get("course_name",None)
    course_code = args.get("course_code",None)
    course_description = args.get("course_description",None)
    
    if course_code is None:
      raise BusinessValidationError(status_code=400,error_code="COURSE002",error_message="Course Code is required")

    if course_name is None:
      raise BusinessValidationError(status_code=400,error_code="COURSE001",error_message="Course Name is required")
    
    course_exist = db.session.query(Course).filter(Course.course_id == course_id).first()
    
    if course_exist is None:
      raise NotFoundError(response = "Course not found",status_code = 404)
    
    course_exist.course_code = course_code
    course_exist.course_name = course_name
    course_exist.course_description = course_description

    db.session.commit()
    
    return course_exist,200
  
  
  def delete(self,course_id):
    course_exist = db.session.query(Course).filter(Course.course_id == course_id).first()
    
    if course_exist is None:
      raise NotFoundError(response="Course not found",status_code = 404)
    
    enroll_students = db.session.query(Enrollment).filter(Enrollment.course_id == course_id).all()
    
    for enroll_student in enroll_students:
      db.session.delete(enroll_student)
      db.session.commit()
      
    db.session.delete(course_exist)
    db.session.commit()
    return make_response("")


# RESTful API resources for Student
class StudentApi(Resource):
  @marshal_with(output_student)
  def get(self,student_id):
    student = db.session.query(Student).filter(Student.student_id == student_id).first()
    if student:
      return student
    else:
      raise NotFoundError(response="Student not found",status_code = 404)
    
  
  @marshal_with(output_student)
  def post(self):
    args = create_student_parser.parse_args()
    first_name = args.get("first_name",None)
    last_name = args.get("last_name",None)
    roll_number = args.get("roll_number",None)
    
    if roll_number is None:
      raise BusinessValidationError(status_code=400,error_code="STUDENT001",error_message="Roll Number required")

    if first_name is None:
      raise BusinessValidationError(status_code=400,error_code="STUDENT002",error_message="First Name is required")
    
    student_exist = db.session.query(Student).filter(Student.roll_number == roll_number).first()
    
    if student_exist:
      raise AlreadyExistError(response = "Student already exist",status_code = 409)
    
    new_student = Student(first_name = first_name,last_name = last_name,roll_number = roll_number)
    db.session.add(new_student)
    db.session.commit()
    
    return new_student,201
  
  
  @marshal_with(output_student)
  def put(self,student_id):
    args = create_student_parser.parse_args()
    first_name = args.get("first_name",None)
    last_name = args.get("last_name",None)
    roll_number = args.get("roll_number",None)
    
    if roll_number is None:
      raise BusinessValidationError(status_code=400,error_code="STUDENT001",error_message="Roll Number required")

    if first_name is None:
      raise BusinessValidationError(status_code=400,error_code="STUDENT002",error_message="First Name is required")
    
    student_exist = db.session.query(Student).filter(Student.student_id == student_id).first()
    
    if student_exist is None:
      raise NotFoundError(response = "Student not found",status_code = 404)
    
    student_exist.first_name = first_name
    student_exist.last_name = last_name
    student_exist.roll_number = roll_number

    db.session.commit()
    
    return student_exist,200
    
  
  def delete(self,student_id):
    student_exist = db.session.query(Student).filter(Student.student_id == student_id).first()
    if student_exist is None:
      raise NotFoundError(status_code = 404)
    
    enroll_students = db.session.query(Enrollment).filter(Enrollment.student_id == student_id).all()
    
    for enroll_student in enroll_students:
      db.session.delete(enroll_student)
      db.session.commit()
    
    db.session.delete(student_exist)
    db.session.commit()
    return make_response("")


# RESTful API resources for Enrollment
class EnrollmentApi(Resource):
  @marshal_with(output_enrollment)
  def get(self,student_id):
    student_exist = db.session.query(Student).filter(Student.student_id == student_id).first()
    
    if student_exist is None:
      raise BusinessValidationError(status_code=400,error_code="ENROLLMENT002",error_message="Student does not exist")
    
    enrolled_student = db.session.query(Enrollment).filter(Enrollment.student_id == student_id).all()
    
    if enrolled_student == []:
      raise NotFoundError(response="Student is not enrolled in any course",status_code = 404)
    
    return enrolled_student
  
  
  @marshal_with(output_enrollment)
  def post(self,student_id):
    args = create_enrollment_parser.parse_args()
    course_id = int(args.get("course_id",None))
    
    student_exist = db.session.query(Student).filter(Student.student_id == student_id).first()
    if(student_exist is None):
      raise BusinessValidationError(status_code=400,error_code="ENROLLMENT002",error_message="Student does not exist")
    
    course_exist = db.session.query(Course).filter(Course.course_id == course_id).first()
    if course_exist is None:
      raise BusinessValidationError(status_code=400,error_code="ENROLLMENT001",error_message="Course does not exist")
      
    new_enrollment = Enrollment(student_id = student_id,course_id=course_exist.course_id)
    db.session.add(new_enrollment)
    db.session.commit()
    
    e = db.session.query(Enrollment).filter(Enrollment.student_id == student_id).all()
    return e,201
  
  
  def delete(self,student_id,course_id):
    student_exist = db.session.query(Student).filter(Student.student_id == student_id).first()
    if(student_exist is None):
      raise BusinessValidationError(status_code=400,error_code="ENROLLMENT002",error_message="Student does not exist")
    
    course_exist = db.session.query(Course).filter(Course.course_id == course_id).first()
    if course_exist is None:
      raise BusinessValidationError(status_code=400,error_code="ENROLLMENT001",error_message="Course does not exist")
    
    e = db.session.query(Enrollment).filter(Enrollment.student_id == student_id,Enrollment.course_id == course_id).first()

    if(e is None):
      raise NotFoundError(response="Enrollment for the student not found",status_code=404)
    
    db.session.delete(e)
    db.session.commit()
    
    return make_response("")

api.add_resource(CourseApi,'/api/course','/api/course/<int:course_id>')
api.add_resource(StudentApi,'/api/student','/api/student/<int:student_id>')
api.add_resource(EnrollmentApi,'/api/student/<int:student_id>/course','/api/student/<int:student_id>/course/<int:course_id>')


if __name__ == "__main__":
  app.run(debug = True)