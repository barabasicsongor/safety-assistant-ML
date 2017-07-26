import utilities
import lb_encoder
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import numpy as np

def encode_categorical(X, encoder_paths):
    nhood_encoder = lb_encoder.LBEncoder()
    X[:, 0] = nhood_encoder.fit_transform(X[:, 0])
    nhood_encoder.save_to_disk(encoder_paths[0])
    weekday_encoder = lb_encoder.LBEncoder()
    X[:, 1] = weekday_encoder.fit_transform(X[:, 1])
    weekday_encoder.save_to_disk(encoder_paths[1])

    nr_categories = [nhood_encoder.nr_classes(), weekday_encoder.nr_classes()]

    categorical_features = [0, 1]
    for i in range(0, len(categorical_features)):
        onehotencoder = OneHotEncoder(categorical_features=[categorical_features[i]])
        X = onehotencoder.fit_transform(X).toarray()

        for j in range(i + 1, len(categorical_features)):
            categorical_features[j] = categorical_features[j] + nr_categories[i] - 1

    X = np.delete(X, categorical_features, axis=1)
    return X


def prep_data(crimes, encoder_paths):
    # Group crimes by date
    date_grouped = {}
    for cr in crimes:
        if cr.is_crime:
            date_int = 10000 * cr.date_time.year + 100 * cr.date_time.month + cr.date_time.day

            if date_int in list(date_grouped.keys()):
                date_grouped[date_int].append(cr)
            else:
                date_grouped[date_int] = [cr]

    # Inside groups by date, group crimes into neighbourhoods
    grouped = {}

    for x in list(date_grouped.keys()):
        crms = date_grouped[x]
        grouped[x] = {}

        for cr in crms:

            if cr.nhood.name in list(grouped[x].keys()):
                grouped[x][cr.nhood.name].append(cr)
            else:
                grouped[x][cr.nhood.name] = [cr]

    X = []
    Y = []
    for x in list(grouped.keys()):
        for hood in list(grouped[x].keys()):
            weekday_name = grouped[x][hood][0].weekday_name
            split = []

            for y in list(grouped.keys()):
                if hood in list(grouped[y]):
                    split.append(len(grouped[y][hood]))

            mx = max(split)
            nr = len(grouped[x][hood])
            p = float(nr / mx)

            if p >= 0.5:
                Y.append(1)
            else:
                Y.append(0)

            X_tmp = [hood, weekday_name]
            X.append(X_tmp)

    # Convert to numpy arrays
    X = np.array(X)
    Y = np.array(Y)

    # Encode categorical features
    X = encode_categorical(X, encoder_paths)

    return X, Y