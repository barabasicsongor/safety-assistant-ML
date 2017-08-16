import numpy as np
from flask import Flask, abort, jsonify, request
import predictor
import json
import numpy as np
import utilities
from shapely import geometry
import preprocessing

predictor = predictor.Predictor(classifier_path='files/ann/classifier.json',
                      classifier_weights_path='files/ann/classifier_weights.h5',
                      nhood_encoder_path='files/ann/nhood_encoder.npy',
                      weekday_encoder_path='files/ann/weekday_encoder.npy',
                      scaler_path='files/ann/scaler.save')

nhoods = preprocessing.preprocess_neighbourhoods(fpath='files/datasets/SFN.json')

# Flask App

app = Flask(__name__)


@app.route('/api', methods=['POST'])
def make_predict():
    data = request.get_json(force=True)
    day = data['day']
    place = data['place']

    lat, lng = utilities.reverse_geocode(place)
    place = geometry.Point(lat, lng)

    nhood = utilities.get_nhood(nhoods, place)

    if nhood == '':
    	pred = -1
    else:
    	print('Hood found: {}'.format(nhood))
    	pred = predictor.predict(np.array([[nhood, day]]))
    	pred = float(pred[0][0])

    return jsonify(results=pred)

@app.route('/heatmap', methods=['GET'])
def heatmap():
	with open('files/output/heatmap.json') as data_file:
		data = json.load(data_file)
	return jsonify(data)

@app.route('/armap', methods=['GET'])
def heatmap():
	with open('files/output/ar_map.json') as data_file:
		data = json.load(data_file)
	return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
