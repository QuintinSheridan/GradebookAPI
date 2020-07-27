# qtry2
This github repoo hosts a project to act as the backend for an online gradebook platform.  
The data is currently hosted as a sqlite database.  Here is a breakdown of the files in the repo:

## Files

`migrations/` - files for flask database migration

`Procfile` - a file that tells heroku to run the python app on gunicorn

`app.py` - the main flask application containing the endpoints for the backend

`auth.py` - a script for extracting and verifying authorization tokens headers from requests

`data_insert.py` - a python script to insert test data into the database tables

`database.db` - a sqlite database for testing the endpoints and authorization

`manage.py` - a script for database management

`models.py` -  a script with the database models

`requirements.txt` - a text file with all required python libraries

`setup.sh` - a script to keep any environment variables that may be required for heroku deployment


## Local Setup and Deployment
The scripts can be run locally.  First, create a virtual environment

`virtualenvironment env`

Then source the environement

`source env/bin/activate`

now all of the python dependencies can be installed in the virtual environment.

`pip install -r requirements.txt`

The application can be ran using flask:

`export FLASK_APP=app.py`
`export FLASK_DEBUG=true`
`flask run`

## Heroku Deployment
Currently, the app is deployed on Heroku.  For details on how to deploy applications on Heroku see https://devcenter.heroku.com/categories/deployment for more information.
The Heroku app is currently hosed at the following URL:

https://qtry2.herokuapp.com

## Authentication
Authentication for the app is provided using Auth0.  Authenticaion tokens are generated by visiting https://dev-l3q-km4v.us.auth0.com/authorize?audience=gradebook&response_type=token&client_id=GdPNY3xTH1DN8bkH6RnOYu6baZzGN3iz&redirect_uri=http://127.0.0.1:5000/login-results

To log out of Auth0, https://dev-l3q-km4v.us.auth0.com/logout

The access tokens provided in the postman test collection will only be valid for 24 hours.

## API endpoints
The app in this project serves as an API backend for a gradebook application with two roles: students and teachers


## API Testing
All testing for this project was performed using postman in the collection 


## Example API Usage
### Student
**get:grades**
eg call: {host}/user/1/courses/1/assignments/grades
returns: `{
    "course_id": 1,
    "grades": [
        [
            1,
            1,
            78
        ],
        [
            2,
            1,
            88
        ]
    ],
    "status": 200,
    "success": true
}`

**get:grade**
eg: {host} /user/1/courses/1/assignments/1/grades
returns: `{
    "assignment_number": 1,
    "course_id": 1,
    "grade": [
        [
            1,
            1,
            78
        ]
    ],
    "status": 200,
    "success": true
}`

**get:courses**
eg: {host}//user/1/courses
returns: `{
    "courses": [
        [
            1,
            "'4:00",
            "MTWRF",
            "8:00",
            "8:50"
        ],
        [
            2,
            "English101",
            "MTWRF",
            "9:00",
            "9:50"
        ],
        [
            3,
            "Science101",
            "MTWRF",
            "10:00",
            "10:50"
        ],
        [
            4,
            "History101",
            "MTWRF",
            "11:00",
            "11:50"
        ]
    ],
    "status": 200,
    "success": true,
    "user_id": 1
}`

### Teacher
**get:grades**
eg: {host}/user/3/courses/1/assignments/grades
returns: `{
    "course_id": 1,
    "grades": [
        [
            1,
            1,
            78
        ],
        [
            1,
            2,
            77
        ],
        [
            2,
            1,
            88
        ],
        [
            2,
            2,
            84
        ]
    ],
    "status": 200,
    "success": true
}`

**get:grade**
eg: {host}/user/1/courses/1/assignments/1/grades
returns: `{
    "assignment_number": 1,
    "course_id": 1,
    "grade": [
        [
            1,
            1,
            78
        ]
    ],
    "status": 200,
    "success": true
}`

**post:grade**
eg: {host}/user/1/courses/1/assignments/3/grades?points=80&assignment_id=9
returns: `{
    "assignment_number": 3,
    "course_id": 1,
    "points": "80",
    "status": 200,
    "success": true
}`

**patch:grade**
eg: {host}/user/1/courses/1/assignments/3/grades?points=80
returns: `{
    "assignment_number": 3,
    "course_id": 1,
    "points": "80",
    "status": 200,
    "success": true,
    "user_id": 1
}`

**delete:grade**
eg: /user/1/courses/1/assignments/3/grades
returns: `{
    "course_id": 1,
    "deleted_assignment_number": 3,
    "status": 200,
    "success": true,
    "user_id": 1
}`

**get:courses**
eg: {host}/user/3/courses
reurns: `{
    "courses": [
        [
            1,
            "'4:00",
            "MTWRF",
            "8:00",
            "8:50"
        ],
        [
            2,
            "English101",
            "MTWRF",
            "9:00",
            "9:50"
        ],
        [
            3,
            "Science101",
            "MTWRF",
            "10:00",
            "10:50"
        ],
        [
            4,
            "History101",
            "MTWRF",
            "11:00",
            "11:50"
        ]
    ],
    "status": 200,
    "success": true,
    "user_id": 3
}`

**patch:course**
eg: /user/3/courses/1?start='3:00'&end='4:00'
returns: `{
    "status": 200,
    "success": true,
    "updated_course": 1,
    "user_id": 3
}`






