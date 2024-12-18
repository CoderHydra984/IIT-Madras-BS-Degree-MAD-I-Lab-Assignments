import os
from flask import Flask, render_template, request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "database.sqlite3")
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()




class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)
    students = db.relationship("Student", secondary="enrollments", back_populates="courses")

class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    courses = db.relationship("Course", secondary="enrollments", back_populates="students")

class Enrollments(db.Model):
    __tablename__= 'enrollments'
    enrollment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    estudent_id = db.Column(db.Integer,db.ForeignKey('student.student_id'), nullable=False)
    ecourse_id = db.Column(db.Integer,db.ForeignKey('course.course_id'), nullable=False)




@app.route("/", methods=["GET"])
def index():
    if request.method == 'GET':
        students = db.session.query(Student).all()
        return render_template("index.html",students=students)
    

@app.route("/student/create", methods=["GET","POST"])
def create():
    if request.method == 'GET':
        return render_template("add_students.html")
    elif request.method == 'POST':
        try:
            roll_number = request.form.get("roll")
            first_name = request.form.get("f_name")
            last_name = request.form.get("l_name")
            selected_courses = request.form.getlist("courses")
            new_student = Student(roll_number=roll_number, first_name=first_name, last_name=last_name)
            for course_value in selected_courses:
                if course_value == 'course_1':
                    course = db.session.query(Course).filter(Course.course_id=='1').one()
                elif course_value == 'course_2':
                    course = db.session.query(Course).filter(Course.course_id=='2').one()
                elif course_value == 'course_3':
                    course = db.session.query(Course).filter(Course.course_id=='3').one()
                elif course_value == 'course_4':
                    course = db.session.query(Course).filter(Course.course_id=='4').one()
                new_student.courses.append(course)
            
            db.session.add(new_student)
            db.session.commit()
            students_data = Student.query.all()
        except IntegrityError:
            return render_template("stud_exists.html")
        return redirect(url_for('index'))


@app.route("/student/<int:student_id>/update", methods=["GET","POST"])
def update(student_id):
    if request.method=='GET':
        student_details = db.session.query(Student).filter_by(student_id=student_id).first()
        return render_template("update.html",stud_data=student_details,current_roll=student_details.roll_number,current_f_name=student_details.first_name,current_l_name=student_details.last_name)
    elif request.method == 'POST':
        roll_number = request.form.get("roll")
        first_name = request.form.get("f_name")
        last_name = request.form.get("l_name")
        selected_courses = request.form.getlist("courses")

        student = db.session.query(Student).filter_by(student_id=student_id).first()

        student.first_name = first_name
        student.last_name = last_name

        student.courses.clear()
        for course_value in selected_courses:
            if course_value == 'course_1':
                course = db.session.query(Course).filter(Course.course_id=='1').one()
            elif course_value == 'course_2':
                course = db.session.query(Course).filter(Course.course_id=='2').one()
            elif course_value == 'course_3':
                course = db.session.query(Course).filter(Course.course_id=='3').one()
            elif course_value == 'course_4':
                course = db.session.query(Course).filter(Course.course_id=='4').one()
            student.courses.append(course)
        db.session.commit()
        return redirect(url_for('index'))


@app.route("/student/<int:student_id>/delete",methods=["GET"])
def delete(student_id):
    if request.method=='GET':
        student_details = db.session.query(Student).filter_by(student_id=student_id).first()
        student_details.courses.clear()
        db.session.delete(student_details)
        db.session.commit()
    return redirect(url_for('index')) 


@app.route("/student/<int:student_id>",methods=["GET"])
def student_info(student_id):
    if request.method=='GET':
        student_details = db.session.query(Student).filter_by(student_id=student_id).first()
        return render_template("view.html", Student_details=student_details)




if __name__=='__main__':
    app.run(debug=True,port=8080)