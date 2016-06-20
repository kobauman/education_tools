import sys
import pandas as pd
import numpy as np
import mechanize
import time


def loginToMG(login,password):
    browser = mechanize.Browser()
    browser.set_handle_redirect(True)
    response = browser.open('http://adapt2.sis.pitt.edu/kt/content/Show')
    print('===========================================')
    print('r0\n',response.read())
    for form in browser.forms():
        print("Form name:",form.name)
        print(form)
    print('===========================================')
    browser.select_form(nr = 0)
    browser.form['j_username'] = login
    browser.form['j_password'] = password
    response1 = browser.submit()
    print('r1\n',response1.read())
        
    print('===========================================')
    for form in browser.forms():
        print("Form name:",form.name)
        print(form)
    browser.select_form(nr = 0)
    try:
        response2 = browser.submit()
    except:
        return -1
    print('r2\n',response2.read())
    #time.sleep(3)
    print('===========================================')
    
    response3 = browser.open('http://adapt2.sis.pitt.edu/kt/content/Show?id=5697')
    print('r3\n',response3.read())
#     time.sleep(300)
    print('Done')


def loggingForTheFirstTime(logins):
    #assign logins
    logins1 = pd.DataFrame.from_csv('../data/logins/'+logins+'_1.csv',index_col=None)
    logins2 = pd.DataFrame.from_csv('../data/logins/'+logins+'_2.csv',index_col=None)
    badPairs = list()
    
    logins = list(logins1['login'])
    passwds = list(logins1['pswd'])
    for i in range(len(logins)):
        login = logins[i]
        password = passwds[i]
        resp = loginToMG(login,password)
        if resp == -1:
            badPairs.append({'login':login,'pswd':password})

        print(i, login, password)
    
    logins = list(logins2['login'])
    passwds = list(logins2['pswd'])
    for i in range(len(logins)):
        login = logins[i]
        password = passwds[i]
        resp = loginToMG(login,password)
        if resp == -1:
            badPairs.append({'login':login,'pswd':password})

        print(i, login, password)
        
    badPairs = pd.DataFrame(badPairs)
    badPairs.to_csv('../data/logins/'+logins+'_badPairs.csv',index=None)
     
    
#run function
if __name__ == "__main__":
#     login = 'up1004'
#     password = 'oj7FIvdA'
#     loginToMG(login,password)
#      
#     exit()
    '''
    Logins to the Mastery Grids System for each student
    '''
    if len(sys.argv) > 1:
        loggingForTheFirstTime(sys.argv[1])
    else:
        print("Appropriate format: python loggingToMasteryGrid.py logins")