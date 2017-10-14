import psycopg2
import pandas
import numpy
from numpy import nan
from sklearn.preprocessing import Imputer
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeRegressor

#connecting to database
conn = psycopg2.connect(dbname="planes")

#converting table into dataframe
df = pandas.DataFrame()
for chunk in pandas.read_sql('select * from plane_table', con=conn, chunksize=5000):
    df = df.append(chunk)

#replacing Null values by NaN
df.fillna(value=nan, inplace=True)

#split dataset to train models
array = df.values

#only considering columns with numerical values for now
X = numpy.column_stack((array[:,0:8],array[:,9:12],array[:,16:22],array[:,26],array[:,28:30]))

#replacing NaN values by mean values
imputer = Imputer()
transformed_X = imputer.fit_transform(X)

Y = array[:,30]
Y = Y.astype('int')

validation_size = 0.20
seed = None
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(transformed_X, Y, test_size=validation_size, random_state=seed)

scoring = 'accuracy'

#compare various models
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))
models.append(('DTR', DecisionTreeRegressor()))
results = []
names = []
for name, model in models:
	kfold = model_selection.KFold(n_splits=10, random_state=seed)
	cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
	results.append(cv_results)
	names.append(name)
	msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
	print(msg)


# Make predictions on validation dataset
cr = DecisionTreeClassifier()
cr.fit(X_train, Y_train)
predictions = cr.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
