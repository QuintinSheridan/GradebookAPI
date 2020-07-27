import json
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_cors import CORS

#################
# Local Modules #
#################
# from data.models import db_drop_and_create_all, setup_db, User, UserType, Course, CourseAttendee, Assignment, Grade
# from auth.auth import AuthError, requires_auth

from models import db_drop_and_create_all, setup_db, User, UserType, Course, CourseAttendee, Assignment, Grade
from auth import AuthError, requires_auth

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
setup_db(app)
CORS(app)
# db_drop_and_create_all() only needs to be run once, afterwords it will erase
# and recreate the database with no data
#db_drop_and_create_all()


#----------------------------------------------------------------------------#
# Helper Functions
#----------------------------------------------------------------------------#

def get_user_type(user_id):
    ''' Function to lookup the user type from user id
    Args:
        user_id (int): id in users table
    Returns:
        usert_type (str): 'teacher' or 'student'
    '''

    user_type = UserType.query.join(User, User.user_type == UserType.id)\
        .filter(User.id == user_id).one_or_none()
    
    if user_type:
        return user_type.description
    else:
        abort(404)

#----------------------------------------------------------------------------#
# API Endpoints
#----------------------------------------------------------------------------#


##########
# Grades #
##########

# Note: in a real gradebook application, user_id tokens would also be generated and authenticated 
# using Auth0 and they would be included in the request headers to determine the 
# functionality of get methods and prevent students from accessing other students grades.
# The user tokens have not yet been implemented and would be required to prevent
# students from asccessing data they shouln't have eg. other students grades.  Additionally,
# the request origins would all be limited to the specific user page  

# get all grades for course
@app.route('/user/<int:user_id>/courses/<int:course_id>/assignments/grades', methods=['GET'])
@requires_auth(permission='get:grades')
def get_grades(permission, user_id, course_id):
    # check if user is student or teacher
    user_type = get_user_type(user_id)

    if user_type == 'student':
        grades =  Grade.query\
            .join(Assignment, Assignment.id == Grade.assignment_id)\
            .filter(Assignment.course_id == course_id)\
            .filter(Grade.user_id == user_id).all()

    elif user_type == 'teacher':
        grades =  Grade.query\
        .join(Assignment, Assignment.id == Grade.assignment_id)\
        .filter(Assignment.course_id == course_id).all()

    if not grades:
        abort(404)

    gs = [(g.assignment_id, g.user_id, g.points) for g in grades]

    return jsonify({
        'status': 200,
        'success': True,
        'course_id': course_id,
        'grades': gs
    })


# get grade for assignment
@app.route('/user/<int:user_id>/courses/<int:course_id>/assignments/<int:assignment_number>/grades', methods=['GET'])
@requires_auth(permission='get:grade')
def get_grade(permission, user_id, course_id, assignment_number):
    user_type = get_user_type(user_id)
    print(f'user_type: {user_type}')

    if user_type == 'student':
        grade =  Grade.query\
            .join(Assignment, Assignment.id == Grade.assignment_id)\
            .filter(Assignment.course_id == course_id)\
            .filter(Assignment.assignment_number==assignment_number)\
            .filter(Grade.user_id == user_id).all()

    if user_type=='teacher':
        grade =  Grade.query\
        .join(Assignment, Assignment.id == Grade.assignment_id)\
        .filter(Assignment.assignment_number==assignment_number)\
        .filter(Assignment.course_id == course_id).all()

    if not grade:
        abort('404')

    # print('grade: ', grade)
    
    grades = [(g.assignment_id, g.user_id, g.points) for g in grade]
    
    return jsonify({
        'status': 200,
        'success': True,
        'course_id': course_id, 
        'assignment_number': assignment_number,
        'grade': grades
        })


# post grade for assignment
@app.route('/user/<int:user_id>/courses/<int:course_id>/assignments/<int:assignment_number>/grades', methods=['POST'])
@requires_auth(permission='post:grade')
def post_grade(permission, user_id, course_id, assignment_number):
    user_type = get_user_type(user_id)
    if user_type == 'teacher':
        abort(404)
    
    if user_type == 'student':
        data = request.args
        try:
            # get the assignment_id from the course and assignment#
            assignment = Assignment.query.filter(Assignment.assignment_number==assignment_number)\
                .filter(Assignment.course_id==course_id).one_or_none()

            assignment_id = assignment.id
            grade = Grade(assignment_id=assignment_id, user_id = user_id, points=data['points'])
            grade.insert()

            return jsonify({
                'status': 200,
                'success': True,
                'course_id': course_id, 
                'assignment_number':assignment_number,
                'points':data['points']
            })

        except Exception as e:
            print(f'The following exception occured while posting grades: {e}')
            abort(400)
    

# patch grade for assignment
@app.route('/user/<int:user_id>/courses/<int:course_id>/assignments/<int:assignment_number>/grades', methods=['PATCH'])
@requires_auth(permission='patch:grade')
def patch_grade(permission, user_id, course_id, assignment_number):
    try:
        # get grade 
        grade = Grade.query.filter(Grade.user_id == user_id)\
            .join(Assignment, Assignment.id == Grade.assignment_id)\
            .filter(Assignment.assignment_number == assignment_number).one_or_none()

        if not grade:
            abort(404) 
        
        data = request.args
        grade.points = data['points']
        grade.update()

        return jsonify({
                'status': 200,
                'success': True,
                'user_id': user_id,
                'course_id': course_id,
                'assignment_number': assignment_number,
                'points': data['points']
            })

    except Exception as e:
        print(f'The following error occured while trying to update grades: {e}')
        abort(400)


# delete grade for assignment
@app.route('/user/<int:user_id>/courses/<int:course_id>/assignments/<int:assignment_number>/grades', methods=['DELETE'])
@requires_auth(permission='delete:grade')
def delete_grade(permission, user_id, course_id, assignment_number):
    try:
        # get grade 
        grade = Grade.query.filter(Grade.user_id == user_id)\
            .join(Assignment, Assignment.id == Grade.assignment_id)\
            .filter(Assignment.assignment_number == assignment_number).one_or_none()

        if not grade:
            abort(404) 
        
        grade.delete()

        return jsonify({
                'status': 200,
                'success': True,
                'user_id': user_id,
                'course_id': course_id,
                'deleted_assignment_number': assignment_number
            })

    except Exception as e:
        print(f'The following error occured while trying to delete grades: {e}')
        abort(400)


###########
# Courses #
###########

# get courses
@app.route('/user/<int:user_id>/courses', methods=['GET'])
@requires_auth(permission='get:courses')
def get_courses(permission, user_id):
    try:
        # courses = CourseAttendee.query.join(Course, CourseAttnedee.course_id==Course.id)\
        # .filter(CourseAttendee.user_id == user_id).all()
        courses = Course.query.join(CourseAttendee, CourseAttendee.course_id==Course.id)\
            .filter(CourseAttendee.user_id == user_id)

        if not courses:
            abort(404)

        user_courses = [(c.id, c.title, c.days, c.start, c.end) for c in courses]

        return jsonify({
            'status': 200,
            'success': True,
            'user_id': user_id,
            'courses': user_courses
        })
        
        
    except Exception as e:
        print(f'The following error occured while trying to get Courses: {e}')
        abort(400)


@app.route('/user/<int:user_id>/courses/<int:course_id>', methods=['PATCH'])
@requires_auth(permission='patch:course')
def patch_course(permission, user_id, course_id):
    try:
        course = Course.query.filter(Course.id == course_id).one_or_none()

        if not course:
            abort(404)

        data = request.args
        
        # update provided attributes
        if 'title' in data:
            course.title = data['title']
        if 'days' in data:
            course.title = data['days']
        if 'start' in data:
            course.title = data['start']
        if 'end' in data:
            course.title = data['end']
        
        course.update()

        return jsonify({
            'status': 200,
            'user_id': user_id,
            'updated_course': course_id,
            'success': True,
        })
        
    except Exception as e:
        print(f'The following error occured while trying to update courses: {e}')
        abort(400)



## Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable"
            }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
            'success': False,
            'error': 404,
            'message': "resource not found"
            }), 404


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
            'success': False,
            'error': 401,
            'message': "unauthorized"
        }), 401



if __name__ == '__main__':
  app.run()

