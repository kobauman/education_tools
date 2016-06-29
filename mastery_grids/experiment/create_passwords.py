import random
import pandas as pd
import time

def generatePassword(pw_length):
    mypw = ""
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(pw_length):
        next_index = random.randrange(len(alphabet))
        mypw = mypw + alphabet[next_index]
    return mypw


def generateLoginPasswordPairs(experiment = 1, number = 100, start = 0):
    # login constitutes 'up'+1digit_experiment_number+3digit_number
    # example: up1000
    logins = list()
    for i in range(start, start + number):
        l = dict()
        l['login'] = 'up%d%03d'%(experiment,i)
        l['pswd'] = generatePassword(8)
        logins.append(l)
    
    filename = '../data/logins/logins_new_%d.csv'%int(time.time())
    logins = pd.DataFrame(logins)
    logins.to_csv(filename,index=False)




generateLoginPasswordPairs(experiment = 1, number = 100, start = 100)