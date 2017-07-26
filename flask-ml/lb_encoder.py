from sklearn.preprocessing import LabelEncoder
import numpy as np

class LBEncoder(object):

    def __init__(self):
        self.encoder = LabelEncoder()

    def fit_transform(self, X):
        return self.encoder.fit_transform(X)

    def transform(self, X):
        return self.encoder.transform(X)

    def nr_classes(self):
        return len(self.encoder.classes_)

    # Filetype is .npy
    def save_to_disk(self, fpath):
        np.save(fpath, self.encoder.classes_)
        print('LabelEncoder saved to disk')

    # Filetype is .npy
    def load_from_disk(self, fpath):
        self.encoder.classes_ = np.load(fpath)
        print('LabelEncoder loaded from disk')