import pandas as pd 
import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
 
    return conn


DB_FILE = 'database.db'
conn = create_connection(DB_FILE)
cur = conn.cursor()

# DROP ALL OLD DATA
delete_data = '''
    DELETE FROM user_types;
    DELETE FROM users;
    DELETE FROM grades;
    DELETE FROM assignments;
    DELETE FROM course_roster;
    DELETE FROM courses;
    '''

cur.execute(delete_data)

# User Types
user_type_df = pd.DataFrame({
    'id': [1,2],
    'descripiton': ['teacher', 'student'],
})

user_type_q = '''
INSERT INTO 
    user_types(id, description)
VALUES(?,?)
        '''

for row in user_type_df.itertuples(index=False):
    cur.execute(user_type_q, row)

# Users
users_df = pd.DataFrame({
    'first':['John', 'Billy', 'Jimmy'],
    'last': ['Doe', 'Bob', 'John'],
    'email': ['johndoe@gmail.com', 'billybob@gmail.com', 'jimmyjohn@gmail.com'],
    'user_type':[2,2,1]
})

user_q = '''
INSERT INTO 
    users(first, last, email, user_type)
VALUES(?,?,?,?)
        '''

for row in users_df.itertuples(index=False):
    cur.execute(user_q, row)

# Courses
courses_df = pd.DataFrame({
    'title': ['Math101', 'English101', 'Science101', 'History101'],
    'days': ['MTWRF','MTWRF','MTWRF','MTWRF'],
    'start':['8:00', '9:00', '10:00', '11:00'],
    'end': ['8:50', '9:50', '10:50', '11:50']
})

courses_q = '''
INSERT INTO 
    courses(title, days, start, end)
VALUES(?,?,?,?)
        '''

for row in courses_df.itertuples(index=False):
    cur.execute(courses_q, row)

# CourseAttendee
schedule_df = pd.DataFrame({
    'user_id': [1,1,1,1,2,2,2,2,3,3,3,3],
    'course_id': [1,2,3,4,1,2,3,4,1,2,3,4]
})

schedule_q = '''
INSERT INTO 
    course_roster(user_id, course_id)
VALUES(?,?)
        '''

for row in schedule_df.itertuples(index=False):
    cur.execute(schedule_q, row)


# Assignments
assignment_df =pd.DataFrame({
    'id': [1, 2, 3, 4, 5, 6, 7, 8, 9],
    'course_id': [1, 1, 2, 2, 3, 3, 4, 4, 1],
    'assignment_number': [1, 2, 1, 2, 1, 2, 1, 2, 3],
    'title': ['M1', 'M2', 'E1', 'E2', 'S1', 'S2', 'H1', 'H2', 'M3'],
    'max_points': [100, 100, 100, 100, 100, 100, 100, 100, 100]
})

assignment_q = '''
INSERT INTO 
    assignments(id, course_id, assignment_number, title, max_points)
VALUES(?,?,?,?,?)
        '''

for row in assignment_df.itertuples(index=False):
    cur.execute(assignment_q, row)

# Grade
grades_df = pd.DataFrame({
    'assignment_id':[1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8],
    'user_id':[1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
    'points':[78, 88, 98, 85, 74, 65, 80, 98, 77, 84, 86, 85, 89, 87, 94, 97]
})

grades_q = '''
INSERT INTO 
    grades(assignment_id, user_id, points)
VALUES(?,?,?)
        '''

for row in grades_df.itertuples(index=False):
    cur.execute(grades_q, row)

conn.commit()
cur.close()
conn.close()