#!/usr/bin/python
import MySQLdb
import sys
sys.path.append('../')
import datetime
import pandas as pd

MYSQL_PARAMS = ("localhost","root","mysqlpass","moodle_4nov14")
#MYSQL_PARAMS = ("localhost","root","mysqlpass","moodle_jan19_15")

#this function obtains the list of students assigned to the course
#with their prior performance
#1) all prior courses
#2) all prior CS courses
#3) last course
#4) last CS course
def studentsByCourse(MYSQL_PARAMS, requested_course = None):
    # Open database connection
    a,b,c,d = MYSQL_PARAMS
    db = MySQLdb.connect(a,b,c,d)
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    
    # identify starting date
    query = 'SELECT startdate, fullname FROM mdl_course WHERE id = %d;'%requested_course
    cursor.execute(query)
    course = list(cursor.fetchall())[0]
    print('Requested course is: %d, %s, starts: %d'%(requested_course, course[1], course[0]))
        
    d = datetime.datetime.fromtimestamp(course[0]).strftime('%d-%m-%Y')
    start_day = course[0]
    print(datetime.datetime.strptime(d, '%d-%m-%Y'))
    
    
#     #days of courses stars
#     start_days = dict()
#     query = 'SELECT id, fullname, startdate, visible FROM mdl_course;'
#     cursor.execute(query)
#     courses = cursor.fetchall()
#     courses_info = dict()
#     #iterate over courses in the base
#     for course in courses:
#         start_days[course[0]] = (course[0],course[2])
    
    
    # identify the list of enrolled students
    query = '''SELECT mdl_user_enrolments.userid
                FROM
                mdl_enrol, mdl_user_enrolments
                WHERE
                mdl_enrol.id = mdl_user_enrolments.enrolid
                AND
                mdl_enrol.courseid = %s;'''%requested_course
    cursor.execute(query)
    students = cursor.fetchall()
    students_info = list()
    #iterate over enrolled students
    for studentID in students:
        studentid = int(studentID[0])
        student = {'userID':studentid}
        query = "SELECT id, email, firstname, lastname FROM mdl_user WHERE id = %d;"%studentid
        cursor.execute(query);
        info = list(cursor.fetchall())[0]
        student['PrimaryEmail'] = info[1].decode('utf8', 'ignore')
        student['FirstName'] = info[2].decode('utf8', 'ignore')
        student['LastName'] = info[3].decode('utf8', 'ignore')
        if 'Instructor' in student['LastName']:
            continue
        
        print('Working on ',studentid,student['PrimaryEmail'],student['FirstName'],student['LastName'])
        
        # collect all prior final exams (grade > 0)
        query = '''SELECT 
        mdl_grade_grades.userid, mdl_grade_grades.rawgrade, 
        mdl_grade_items.courseid, mdl_course.fullname, mdl_course.startdate
        FROM
        mdl_grade_grades, mdl_grade_items, mdl_course
        WHERE 
        mdl_grade_grades.itemid = mdl_grade_items.id
        AND
        mdl_course.id = mdl_grade_items.courseid
        AND
        mdl_grade_items.itemmodule LIKE 'quiz'
        AND
        mdl_grade_items.itemname LIKE 'Final%%'
        AND
        mdl_grade_grades.rawgrade > 0
        AND
        mdl_grade_grades.userid = %d;'''%studentid
        cursor.execute(query)
        courses = cursor.fetchall()
        # courseID -> grade
        student_history = list()
        #iterate over enrolled students
        for course in courses:
            student_history.append({'grade':course[1],'courseid':course[2],
                                    'coursename':course[3],'coursestart':course[4]})
        student_history = pd.DataFrame(student_history)
        if len(student_history) == 0:
            student['allPrior']=None
            student['lastPrior']=None
            student['CSPrior']=None
            student['lastCSPrior']=None
        else:
            student_history = student_history.loc[student_history['coursestart'] < start_day - 100]
            
            #1) all prior courses
            student['allPrior'] = student_history['grade'].mean()
            #print(student_history)
            #2) last course
            lastStart = student_history['coursestart'].max()
            student['lastPrior'] = student_history.loc[student_history['coursestart']==lastStart]['grade'].mean()
        
            #3) all prior CS courses
            #4) last CS course
            student_CS_history = student_history[student_history.apply(lambda x:'CS' in x['coursename'],axis=1)]
            if len(student_CS_history) == 0:
                    student['CSPrior'] = None
                    student['lastCSPrior'] = None
            else:   
                    student['CSPrior'] = student_CS_history['grade'].mean()
                    lastCSStart = student_CS_history['coursestart'].max()
                    student['lastCSPrior'] = student_CS_history.loc[student_CS_history['coursestart']==lastCSStart]['grade'].mean()
    #print(student)
    students_info.append(student)           
    print('Number of Student: %d'%len(students_info))
             
    #save
    students_df = pd.DataFrame(students_info)
    students_df.to_csv('../data/course2students/'+str(requested_course)+'_students.csv',index=False)
        
       
    # disconnect from server
    db.close()
    print("\nDONE\n")


#run function
if __name__ == "__main__":
    '''
    Get the list of students with info for the given courseID 
    '''
    if len(sys.argv) > 1:
        studentsByCourse(MYSQL_PARAMS, int(sys.argv[1]))
    else:
        print("Appropriate format: python studentsByCourseID.py 826")
