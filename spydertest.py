import pickle
from statsmodels import robust
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn import neighbors
from sklearn.ensemble import RandomForestClassifier

pickle_in=open('classifiers.pickle','rb')
dictclf=pickle.load(pickle_in)

for key in dictclf:
    print(dictclf[key])
    print(key)
    
