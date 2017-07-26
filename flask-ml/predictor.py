import numpy as np
import preprocessing
import ann
import lb_encoder
import scaler
from sklearn.preprocessing import OneHotEncoder

class Predictor(object):

    threshold = 0.7

    def __init__(self, classifier_path, classifier_weights_path, nhood_encoder_path,
        weekday_encoder_path, scaler_path):
        self.ann = ann.ANN()
        self.ann.load_from_disk(fpath_classifier=classifier_path,
                                fpath_weights=classifier_weights_path)
        self.nhood_encoder = lb_encoder.LBEncoder()
        self.nhood_encoder.load_from_disk(fpath=nhood_encoder_path)
        self.weekday_encoder = lb_encoder.LBEncoder()
        self.weekday_encoder.load_from_disk(fpath=weekday_encoder_path)
        self.sc = scaler.Scaler()
        self.sc.load_from_disk(fpath=scaler_path)

    def predict(self, X):
        # LabelEncoder
        X[:, 0] = self.nhood_encoder.transform(X[:, 0])
        X[:, 1] = self.weekday_encoder.transform(X[:, 1])

        # Manual OneHotEncoder
        cat_0 = [0 for x in range(0, self.nhood_encoder.nr_classes())]
        cat_0[int(X[0][0])] = 1
        cat_0 = cat_0[1:]
        cat_1 = [0 for x in range(0, self.weekday_encoder.nr_classes())]
        cat_1[int(X[0][1])] = 1
        cat_1 = cat_1[1:]
        cat_0.extend(cat_1)
        X = np.array([cat_0])

        # Scaler
        X = self.sc.transform(X)

        # Predict
        pred = self.ann.predict(X)

        return pred
