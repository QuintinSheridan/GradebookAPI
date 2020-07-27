import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


####################
# DB Model Classes #
####################

class User(db.Model):
    __tablename__ = 'users'
    # Autoincrementing, unique primary key
    id = db.Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    first = db.Column(String(80))
    last = db.Column(String(80))
    email = db.Column(String(100))
    user_type = db.Column(Integer)

    def __init__(self, first, last, email, user_type):
        self.first = first
        self.last = last
        self.email = email
        self.user_type = user_type 

    # insert
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # update
    def update(self):
        db.session.commit()

    # delete
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<User {self.id, self.first, self.last, self.email, self.type}>'
       

class UserType(db.Model):
    __tablename__ = 'user_types'
    id = db.Column(Integer, primary_key=True)
    description = db.Column(String(100))

    def __init__(self, id, description):
        self.id = id
        self.description = description 

    # insert
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # update
    def update(self):
        db.session.commit()

    # delete
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<UserType{self.id, self.description}>'
       

class Course(db.Model):
    __tablename__ = 'courses'
    # Autoincrementing, unique primary key
    id = db.Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = db.Column(String(250))
    days = db.Column(String(10))
    start = db.Column(String(20))
    end = db.Column(String(20))

    def __init__(self, id, description):
        self.id = id
        self.description = description 

    # insert
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # update
    def update(self):
        db.session.commit()

    # delete
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Course {self.id, self.title}>'


class CourseAttendee(db.Model):
    __tablename__ = 'course_roster'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True) 
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True) 

    def __init__(self, user_id, course_id):
        self.user_id = user_id
        self.course_id = course_id 

    # insert
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # update
    def update(self):
        db.session.commit()

    # delete
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<CourseAttendee {self.user_id, self.course_id}>'


class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(Integer, primary_key=True)
    course_id = db.Column(Integer, db.ForeignKey('courses.id'))
    assignment_number = db.Column(Integer)
    title = db.Column(String(250))
    max_points = db.Column(Integer)

    def __init__(self, course_id, assignment_number, title, max_points):
        self.course_id = course_id
        self.assignment_number = assignment_number 
        self.title = title  
        self.max_ppoints = max_points

    # insert
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # update
    def update(self):
        db.session.commit()

    # delete
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'< Assignment {self.id, self.course_id, self.assignment_number, self.title, self.max_points}>'


class Grade(db.Model):
    __tablename__ = 'grades'
    assignment_id = db.Column(Integer, db.ForeignKey('assignments.id'), primary_key=True)
    user_id = db.Column(Integer, db.ForeignKey('users.id'), primary_key=True)
    points = db.Column(Integer)

    def __init__(self, assignment_id, user_id, points):
        self.assignment_id = assignment_id 
        self.user_id = user_id  
        self.points = points  

    # insert
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # update
    def update(self):
        db.session.commit()

    # delete
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Grade {self.assignment_id, self.user_id, self.points}>'
        

