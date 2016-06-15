#!/usr/bin/python
import MySQLdb
import sys
sys.path.append('../')
import nltk
import time
import datetime
from copy import copy
from utils.functions import *


MYSQL_PARAMS = ("localhost","root","mysqlpass","moodle_jan19_15")


#this function obtains current courses by date
def studentsByCourse(MYSQL_PARAMS, requested_course = None):
    # Open database connection
    a,b,c,d = MYSQL_PARAMS
    db = MySQLdb.connect(a,b,c,d)
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    
    #days of courses stars
    start_days = dict()
    
    try:
        requested_timestamp = time.mktime(datetime.datetime.strptime(requested_date, "%d/%m/%Y").timetuple())
    except:
        requested_timestamp = time.time()
    print('requested date is: %s'%datetime.datetime.fromtimestamp(requested_timestamp).strftime('%d-%m-%Y'))
    query = 'SELECT id, fullname, startdate, visible FROM mdl_course WHERE startdate < %d;'%requested_timestamp
    cursor.execute(query)
    courses = cursor.fetchall()
    courses_info = dict()
    #iterate over courses in the base
    for course in courses:
        # check if the course started recently
        if requested_timestamp - course[2] < 5443200:
            d = datetime.datetime.fromtimestamp(course[2]).strftime('%d-%m-%Y')
            start_days[course[0]] = datetime.datetime.strptime(d, '%d-%m-%Y')
            courses_info[course[0]] = '|%-60s| %d | %s |'%(course[1],course[0],d)
            
    print('Number of Courses: %d'%len(courses_info))
             
    # find number of students that finished at least one assignment         
    for courseID in courses_info:
        #searching for course grade Items
        query = 'SELECT id FROM  mdl_grade_items WHERE itemmodule LIKE \'quiz\' AND courseid = %d;'%courseID
        cursor.execute(query)
        grade_items = cursor.fetchall()
            
        students_set = set([])
        for grade_i in grade_items:
            #grades
            query = "SELECT userid, rawgrade FROM  mdl_grade_grades WHERE itemid = %d;"%grade_i[0]
            cursor.execute(query);
            students_grades = cursor.fetchall();
            for grade in students_grades:
                students_set.add(grade[0])
        
        courses_info[courseID] += ' students = %3d |'%len(students_set)
        #courses_info[courseID] = courses_info[courseID].split(' ')[0]+'| %3d |'%len(students_set)
        
    # find MidTerm and number of its week
    for courseID in courses_info:
        #searching for course grade Items
        query = "SELECT itemname, iteminstance FROM  mdl_grade_items WHERE itemmodule LIKE 'quiz' AND courseid = %d;"%courseID
        cursor.execute(query)
        grade_items = cursor.fetchall()
            
        midterm_list = list()
        for grade_i in grade_items:
            if  unitNumberByName(grade_i[0]) in [0,1,2,3,4,5,6,7,8,9,10,20,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,20.5]:
                query = "SELECT name,timeopen,timeclose FROM  mdl_quiz WHERE id = %d;"%grade_i[1]
                cursor.execute(query);
                quizes = cursor.fetchall();
                for quiz in quizes:
                    timeopen = datetime.datetime.fromtimestamp(quiz[1])
                    difopen = (timeopen - start_days[courseID]).days
                    timeclose = datetime.datetime.fromtimestamp(quiz[2])
                    difclose = (timeclose - start_days[courseID]).days
                    midterm_list.append('%-20s:from %s(%d) to %s(%s)'%(quiz[0],timeopen.strftime('%d-%m'),difopen,timeclose.strftime('%d-%m'),difclose))
        
        midterm_list.sort(reverse=False)
        if midterm_list:
            courses_info[courseID] += '\n%s\n'%'\n'.join(midterm_list)
        
       
    # disconnect from server
    db.close()
    print("\nDONE\n")
    
    courses_list = copy(courses_info.values())
    courses_list.sort()
    print('\n\n'.join(courses_list))



#run function
if __name__ == "__main__":
    '''
    Get the list of courses (id, name) for the given date 
    '''
    if len(sys.argv) > 1:
        courseFinder(MYSQL_PARAMS, sys.argv[1])
    else:
        print "Appropriate format: 01/12/2011"
        courseFinder(MYSQL_PARAMS)