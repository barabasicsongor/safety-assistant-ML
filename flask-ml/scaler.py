from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib

class Scaler(object):

    def __init__(self):
        self.sc = StandardScaler()

    def fit_transform(self, X):
        return self.sc.fit_transform(X)

    def transform(self, X):
        return self.sc.transform(X)

    # Filetype is .save
    def save_to_disk(self, fpath):
        joblib.dump(self.sc, fpath)
        print('StandardScaler saved to disk')

    # Filetype is .save
    def load_from_disk(self, fpath):
        self.sc = joblib.load(fpath)
        print('StandardScaler loaded from disk')
