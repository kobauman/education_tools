import sys
import pandas as pd
import numpy as np

from scipy import stats


def significant(array1,array2):
    try:
        arr1 = np.array(array1)
        arr2 = np.array(array2)
        print(stats.ttest_ind(arr1,arr2)[1])
        return stats.ttest_ind(arr1,arr2)[1] < 0.1
    except:
        print('PROBLEM!')
        return None

def splitStudents(courseID, logins):
    df = pd.DataFrame.from_csv('../data/course2students/'+str(courseID)+'_students.csv',index_col=None)
    
    eqFlag = False
    iteration = 1
    while eqFlag == False:
        print(iteration)
        iteration+=1
        
        df['expGroup'] = np.random.choice([1,2],len(df))
        print(list(df['expGroup']))
        
        eqFlag = True
        #check significance of the difference
        allPrior1 = df[df['expGroup']==1]['allPrior']
        allPrior1 = list(allPrior1[pd.notnull(allPrior1)])
        allPrior2 = df[df['expGroup']==2]['allPrior']
        allPrior2 = list(allPrior2[pd.notnull(allPrior2)])
        if significant(allPrior1,allPrior2):
            eqFlag = False    
        print(np.average(allPrior1),np.average(allPrior2),significant(allPrior1,allPrior2))
        
        
        lastPrior1 = df[df['expGroup']==1]['lastPrior']
        lastPrior1 = list(lastPrior1[pd.notnull(lastPrior1)])
        lastPrior2 = df[df['expGroup']==2]['lastPrior']
        lastPrior2 = list(lastPrior2[pd.notnull(lastPrior2)])
        if significant(lastPrior1,lastPrior2):
            eqFlag = False
        print(np.average(lastPrior1),np.average(lastPrior2),significant(lastPrior1,lastPrior2))
        
        
        CSPrior1 = df[df['expGroup']==1]['CSPrior']
        CSPrior1 = list(CSPrior1[pd.notnull(CSPrior1)])
        CSPrior2 = df[df['expGroup']==2]['CSPrior']
        CSPrior2 = list(CSPrior2[pd.notnull(CSPrior2)])
        if significant(CSPrior1,CSPrior2):
            eqFlag = False    
        print(np.average(CSPrior1),np.average(CSPrior2),significant(CSPrior1,CSPrior2))
        
        
        lastCSPrior1 = df[df['expGroup']==1]['lastCSPrior']
        lastCSPrior1 = list(lastCSPrior1[pd.notnull(lastCSPrior1)])
        lastCSPrior2 = df[df['expGroup']==2]['lastCSPrior']
        lastCSPrior2 = list(lastCSPrior2[pd.notnull(lastCSPrior2)])
        if significant(lastCSPrior1,lastCSPrior2):
            eqFlag = False
        print(np.average(lastCSPrior1),np.average(lastCSPrior2),significant(lastCSPrior1,lastCSPrior2))
        
        print(df['expGroup'].value_counts())
    
    #assign logins
    logins1 = pd.DataFrame.from_csv('../data/logins/'+logins+'_1.csv',index_col=None)
    logins2 = pd.DataFrame.from_csv('../data/logins/'+logins+'_2.csv',index_col=None)
    
    df.loc[df['expGroup']==1,'login'] = list(logins1['login'])[:len(df.loc[df['expGroup']==1])]
    df.loc[df['expGroup']==2,'login'] = list(logins2['login'])[:len(df.loc[df['expGroup']==2])]
    
    df.loc[df['expGroup']==1,'password'] = list(logins1['pswd'])[:len(df.loc[df['expGroup']==1])]
    df.loc[df['expGroup']==2,'password'] = list(logins2['pswd'])[:len(df.loc[df['expGroup']==2])]

    
    df.to_csv('../data/panel_data/'+str(courseID)+'_panel.csv',index=False)
        
     
    
#run function
if __name__ == "__main__":
    '''
    Randomly split the students, checking the equivalence of the groups
    '''
    if len(sys.argv) > 1:
        splitStudents(int(sys.argv[1]),sys.argv[2])
    else:
        print("Appropriate format: python splitAndCheck.py 826 logins")
