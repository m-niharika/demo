import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.externals import joblib
import argparse

import os

# command line arguments
parser = argparse.ArgumentParser(description='Train a model for iris classification.')
#parser.add_argument('E:/Niharika/iris/data', type=str, help='Input directory containing the training set')
#parser.add_argument('E:/Niharika/iris/output', type=str, help='Output directory for the trained model')
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

input_datadir = "data/"
output_datadir = "output/"

# import the iris training set
irisDF = pd.read_csv(os.path.join(input_datadir, "iris.csv"), names=cols)

# fit the model
lda = LinearDiscriminantAnalysis().fit(irisDF[features], irisDF["Species"])

# output a text description of the model
f = open(os.path.join(output_datadir, 'model.txt'), 'w')
f.write(str(lda))
f.close()

# persist the model
joblib.dump(lda, os.path.join(output_datadir, 'model.pkl'))