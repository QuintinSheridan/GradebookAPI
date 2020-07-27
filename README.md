# qtry2
This github repoo hosts a project to act as the backend for an online gradebook platform.  
The data is currently hosted as a sqlite database.  Here is a breakdown of the files in the repo:

## Files

migrations/ - files for flask database migration

Procfile - a file that tells heroku to run the python app on gunicorn

app.py - the main flask application containing the endpoints for the backend

auth.py - a script for extracting and verifying authorization tokens headers from requests

data_insert.py - a python script to insert test data into the database tables

database.db - a sqlite database for testing the endpoints and authorization

manage.py - a script for database management

models.py -  a script with the database models

requirements.txt - a text file with all required python libraries

setup.sh - a script to keep any environment variables that may be required for heroku deployment


## Local Setup
The scripts can be run locally.  First, create a virtual environment

virtualenvironment env

Then source the environement

source env/bin/activate

now all of the python dependencies can be installed in the virtual environment.

pip install -r requirements.txt

The application can be ran using flask:

export FLASK_APP=app.py
export FLASK_DEBUG=true
flask run

## Heroku Deployment
Currently, the app is deployed on Heroku.  For details on how to deploy applications on Heroku see https://devcenter.heroku.com/categories/deployment for more information.




