import pandas as pd
from sklearn import svm
from sklearn import model_selection
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
import argparse
import os
from pandas._libs import json

# command line arguments
parser = argparse.ArgumentParser(description='Train a model for iris classification.')
#parser.add_argument('indir', type=str, help='Input directory containing the training set')
#parser.add_argument('outdir', type=str, help='Output directory for the trained model')
args = parser.parse_args()

# training set column names
cols = [
    "Sepal_Length",
    "Sepal_Width",
    "Petal_Length",
    "Petal_Width",
    "Species"
]

features = [
    "Sepal_Length",
    "Sepal_Width",
    "Petal_Length",
    "Petal_Width"
]
metrics_file = "prediction/eval.txt"
metrics_json = "prediction/metrics.json"
input_datadir = "data/"
output_datadir = "prediction/"

# import the iris training set
irisDF = pd.read_csv(os.path.join(input_datadir, "iris_test.csv"), names=cols)
# Split-out validation dataset

# fit the model
svc = svm.SVC(kernel='linear', C=1.0).fit(irisDF[features], irisDF["Species"])
#array = irisDF.values
#X = array[:,0:4]
#Y = array[:,4]
#validation_size = 0.20
#seed = 7
#X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
# output a text description of the model
f = open(os.path.join(output_datadir, 'model.txt'), 'w')
f.write(str(svc))
f.close()
#medium
x_train,x_test,y_train,y_test= model_selection.train_test_split(irisDF[features],irisDF["Species"],test_size=.5)
predictions=svc.predict(x_test)
#from sklearn.metrics import accuracy_score
auc=(accuracy_score(y_test,predictions))
with open(metrics_file, 'w') as fd:
    fd.write('AUC: {:4f}\n'.format(auc))

with open(metrics_json, 'w') as outfile:
    json.dump(auc, outfile)
     
#kfold = svc.KFold(n_splits=10, random_state=seed)
# cv_results = model_selection.cross_val_score(model.pkl, X_train, Y_train, cv=kfold, scoring=scoring)
# msg = "%f (%f)" % (cv_results.mean(), cv_results.std())
# print(msg)
# persist the model
joblib.dump(svc, os.path.join(output_datadir, 'model.pkl'))
