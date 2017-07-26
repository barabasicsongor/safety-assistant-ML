import preprocessing
import ann
import ann_data_prep
import scaler

if __name__ == '__main__':
    # Read datasets from file
    nhoods = preprocessing.preprocess_neighbourhoods('files/datasets/SFN.json')
    crimes = preprocessing.preprocess_crimes_from_json('files/output/crimes.json', nhoods)
    X, Y = ann_data_prep.prep_data(crimes, ['files/ann/nhood_encoder.npy', 'files/ann/weekday_encoder.npy'])

    # Split into training and test set
    # Just for testing purposes, later all datapoints will be training sets
    from sklearn.model_selection import train_test_split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

    # Feature Scaling
    sc = scaler.Scaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    sc.save_to_disk('files/ann/scaler.save')

    # # ANN
    input_dim = len(X[0])
    ann = ann.ANN()
    ann.setup(input_dim=input_dim)
    ann.fit(X, Y, batch_size=32, epochs=100)
    ann.save_to_disk(fpath_classifier='files/ann/classifier.json',
                     fpath_weights='files/ann/classifier_weights.h5')