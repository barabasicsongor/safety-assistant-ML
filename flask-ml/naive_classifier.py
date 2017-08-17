import preprocessing
import numpy as np

def data_prep(crimes):
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

    return X, Y

# Probability of crime, with laplacian smoothing
def pr_crime(Y):
    counter = 0
    for y in Y:
        if y == 1:
            counter += 1
    return (counter+1)/float(len(Y)+2)

# Probability of day, given crime is true, with laplacian smoothing
def pr_day_crime(X,Y,day):
    nr_distinct_days = 7
    counter_day = 0
    counter_cr = 0
    
    for i in range(0,len(X)):
        if Y[i] == 1:
            counter_cr += 1
            
            if X[i][1] == day:
                counter_day += 1
            
            
    return (counter_day+1)/float(counter_cr + nr_distinct_days)

# Probability of hood, given crime is true, with laplacian smoothing
def pr_hood_crime(X,Y,hood):
    nr_distinct_hoods = 42
    counter_hood = 0
    counter_cr = 0
    
    for i in range(0,len(X)):
        if Y[i] == 1:
            counter_cr += 1
            
            if X[i][0] == hood:
                counter_hood += 1
            
            
    return (counter_hood+1)/float(counter_cr + nr_distinct_hoods)

def predict(X,Y,day,hood_name):
    p_crime = pr_crime(Y)
    p_not_crime = 1 - p_crime
    
    # Pr of crime, given day and hood
    p_day_crime = pr_day_crime(X,Y,day)
    p_day_not_crime = 1 - p_day_crime
    p_hood_crime = pr_hood_crime(X,Y,hood_name)
    p_hood_not_crime = 1 - p_hood_crime
    
    p_crime_day_hood = p_crime * p_day_crime * p_hood_crime
    p_not_crime_day_hood = p_not_crime * p_day_not_crime * p_hood_not_crime
    
    print(p_crime_day_hood)
    print(p_not_crime_day_hood)
    
    return p_crime_day_hood > p_not_crime_day_hood
    
    

if __name__ == '__main__':
    nhoods = preprocessing.preprocess_neighbourhoods('files/datasets/SFN.json')
    crimes = preprocessing.preprocess_crimes_from_json('files/output/crimes.json', nhoods)
    X, Y = data_prep(crimes)
    
    p = predict(X,Y,'Thursday','Russian Hill')
    