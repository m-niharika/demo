import pandas as pd
from sklearn.externals import joblib
import argparse
import flask
import os

# command line arguments
parser = argparse.ArgumentParser(description='Train a model for iris classification.')
#parser.add_argument('inmodeldir', type=str, help='Input directory containing the training set')
args = parser.parse_args()

app = flask.Flask(__name__)
port = int(os.getenv("PORT", 9090))


# attribute column names

input_datadir = "E:/Niharika/automation/output"
# load the model
mymodel = joblib.load(os.path.join(input_datadir, 'model.pkl')) 

# walk the input attributes directory and make an
# inference for every attributes file found


# read in the attributes

# attr = pd.read_csv(os.path.join(dirpath, file), names=features)

# make the inference
@app.route('/predict', methods=['POST'])
def predict():
    
    features = flask.request.get_json(force=True)['features']
    pred = mymodel.predict([features])
    pred_list = pred.tolist()
    response = {'prediction': pred_list}
    return flask.jsonify(response)

        # save the inference
        #output = pd.DataFrame(pred, columns=["Species"])
        #output.to_csv(os.path.join(args.outdir, file.split(".")[0]), header=False, index=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
