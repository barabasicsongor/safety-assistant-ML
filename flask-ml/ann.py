import keras
from keras.models import  Sequential
from keras.layers import Dense
from keras.models import model_from_json

class ANN(object):

    def setup(self, input_dim):
        self.classifier = Sequential()
        self.classifier.add(Dense(units=(input_dim // 2), kernel_initializer='uniform', activation='relu', input_dim=input_dim))
        self.classifier.add(Dense(units=(input_dim // 2), kernel_initializer='uniform', activation='relu'))
        self.classifier.add(Dense(units=(input_dim // 2), kernel_initializer='uniform', activation='relu'))
        self.classifier.add(Dense(units=1, kernel_initializer='uniform', activation='sigmoid'))
        self.classifier.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

    # Classifier saved to .json file and weights to .h5 file
    def load_from_disk(self, fpath_classifier, fpath_weights):
        # Load the classifier
        json_file = open(fpath_classifier, 'r')
        loaded_classifier_json = json_file.read()
        json_file.close()
        self.classifier = model_from_json(loaded_classifier_json)

        # Load the weights
        self.classifier.load_weights(fpath_weights)
        print('Classifier loaded from disk')

    # Classifier has to be saved to .json file and weights to .h5 file
    def save_to_disk(self, fpath_classifier, fpath_weights):
        # Serialize classifier to JSON
        classifier_json = self.classifier.to_json()
        with open(fpath_classifier, 'w') as json_file:
            json_file.write(classifier_json)

        # Serialize weights to HDF5 file
        self.classifier.save_weights(fpath_weights)
        print('Classifier saved to disk')


    def fit(self, X, Y, batch_size=100, epochs=32):
        self.classifier.fit(X, Y, batch_size=batch_size, epochs=epochs)

    def predict(self, X):
        return self.classifier.predict(X)




