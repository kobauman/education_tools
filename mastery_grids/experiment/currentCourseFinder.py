#!/usr/bin/python
import MySQLdb
import sys
sys.path.append('../')
import time
import datetime
from copy import copy



MYSQL_PARAMS = ("localhost","root","mysqlpass","moodle_jan19_15")


#this function obtains current courses by date
def courseFinder(MYSQL_PARAMS, requested_date = None):
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
        print("Appropriate format: 01/12/2011")
        courseFinder(MYSQL_PARAMS)