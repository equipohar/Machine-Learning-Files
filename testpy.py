import MySQLdb
import sklearn
import math
import itertools
import numpy as np
import pickle
from statsmodels import robust
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn import neighbors
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')

def generateFeatures(Temp):
    f0=np.mean(Temp[:,0])
    f1=np.mean(Temp[:,1])
    f2=np.mean(Temp[:,2])
    f3=np.std(Temp[:,0])
    f4=np.std(Temp[:,1])
    f5=np.std(Temp[:,2])
    f6=np.var(Temp[:,0])
    f7=np.var(Temp[:,1])
    f8=np.var(Temp[:,2])
    f9=robust.mad(Temp[:,0])
    f10=robust.mad(Temp[:,1])
    f11=robust.mad(Temp[:,2])
    f12=abs(np.mean(Temp[:,0])-np.mean(Temp[:,1]))
    f13=abs(np.mean(Temp[:,0])-np.mean(Temp[:,2]))
    f14=abs(np.mean(Temp[:,1])-np.mean(Temp[:,2]))
    return [[f0,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14]]

try:
    db = MySQLdb.connect(host="localhost",user="root",passwd="equipohar123",db="testing_har") 
except:
    print "I am unable to connect to the database"

pickle_in=open('classifiers.pickle','rb')
dictclf=pickle.load(pickle_in)

clfRF=dictclf['RF']
clfKNN=dictclf['KNN']
clfNB=dictclf['NB']

cur = db.cursor()

curIn = db.cursor()


while True:

	cur.execute("SELECT * FROM testing_data WHERE labelRF is NULL OR labelKNN is NULL OR labelNN is NULL;")

	rows = cur.fetchall()

	testingData=np.empty((0,4),float)

	for row in rows:
	    testingData=np.vstack((testingData, [row[1], row[2], row[3], row[0]] ))
	    if len(testingData)==25:
	    	tempFeatures = generateFeatures(testingData[:,0:3])

	        pre=clfRF.predict(tempFeatures)
	        mylist = [(int(pre),i) for i in range(int(testingData[0,3]),int(testingData[-1,3])+1)]
	        curIn.executemany('''UPDATE testing_data SET labelRF = (%s) WHERE id = (%s);''', mylist)

	        pre=clfKNN.predict(tempFeatures)
	        mylist = [(int(pre),i) for i in range(int(testingData[0,3]),int(testingData[-1,3])+1)]
	        curIn.executemany('''UPDATE testing_data SET labelKNN = (%s) WHERE id = (%s);''', mylist)

	        pre=clfNB.predict(tempFeatures)
	        mylist = [(int(pre),i) for i in range(int(testingData[0,3]),int(testingData[-1,3])+1)]
	        curIn.executemany('''UPDATE testing_data SET labelNN = (%s) WHERE id = (%s);''', mylist)

	        testingData=np.empty((0,4),float)

	db.commit()


db.close()