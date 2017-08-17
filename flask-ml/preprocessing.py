import numpy as np
import pandas as pd
from datetime import datetime
import pygeoj
import json
from shapely import geometry
import crime
import neighbourhood
import utilities

CRIMES = ['BURGLARY','DRUG/NARCOTIC','KIDNAPPING','MISSING PERSON','LARCENY/THEFT','ROBBERY','VANDALISM','VEHICLE THEFT','SEX OFFENSES,FORCIBLE','WEAPON LAWS']

"""

Reading the crimes from the CSV files, and returning them in Crime
model format
Main columns to focus on: Type,DayOfWeek,Date,Time,X,Y ([1, 3, 4, 5, 9, 10])

"""
def preprocess_crimes(fpaths, columns):
    print('Started crime preprocessing')

    X_combined = []

    for fpath in fpaths:
        dataset = pd.read_csv(fpath)
        dataset = dataset.iloc[:, columns].values
        X_combined.extend(dataset)

    X = []
    for row in X_combined:

        try:
            date_str = row[2][0:10] + 'T' + row[3]
            date_time = datetime.strptime(date_str, '%m/%d/%YT%H:%M')
            is_crime = False

            if row[0] in CRIMES:
                is_crime = True

            cr = crime.Crime(type=row[0], weekday_name=row[1], date_time=date_time, lat=row[5], lng=row[4], is_crime=is_crime,
                       nhood=None)
            X.append(cr)
        except:
            print('Error: preproccess_crimes')
            continue

    print('Ended crime preprocessing')
    return X

"""

Preprocessing crimes from JSON file

"""
def preprocess_crimes_from_json(fname, nhoods):
    print('Started crime preprocessing')
    with open(fname) as data_file:
        data = json.load(data_file)

    data = data['items']
    crimes = []

    def find_hood(name):
        for hood in nhoods:
            if hood.name == name:
                return hood
        return None

    for i in range(0, len(data)):
        date = data[i]['date'] + 'T' + data[i]['time']
        date_time = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
        cr = crime.Crime(type=data[i]['type'], weekday_name=data[i]['weekday_name'], date_time=date_time, lat=data[i]['lat'],
                   lng=data[i]['lng'], is_crime=bool(data[i]['is_crime']), nhood=find_hood(data[i]['hood_name']))
        crimes.append(cr)

    print('Ended crime preprocessing')
    return crimes

"""

The methods reads a GeoJSON file about the neighbourhoods of San Francisco
Returns a list of Neighbourhood objects

"""
def preprocess_neighbourhoods(fpath):
    print('Started nhoods preprocessing')

    with open(fpath) as data_file:
        data = json.load(data_file)

    data = data['items']
    nhoods = []

    for i in range(0, len(data)):
        coords = data[i]['coordinates']
        poly = geometry.Polygon([coords[j+1], coords[j]] for j in range(0, len(coords), 2))
        nh = neighbourhood.Neighbourhood(name=data[i]['name'], polygon=poly)
        nhoods.append(nh)

    print('Ended nhoods preprocessing')
    return nhoods

"""

The method fixes those crimes which don't have a neighbourhood associated
Finds the closes point, which has a neighbourhood, and assigns it's neighbourhood to it

"""
def fix_missing_crime_hood(crimes, crimes_fix):
    print('Started fixing missing values')
    print('{} crimes to fix'.format(len(crimes_fix)))

    crimes_old = crimes
    crimes_new = []
    counter = 0

    for crime in crimes_fix:

        min_dist = float('inf')

        for cr in crimes_old:

            if utilities.get_distance_in_meters((cr.lat, cr.lng),(crime.lat, crime.lng)) < min_dist:
                min_dist = utilities.get_distance_in_meters((cr.lat, cr.lng),(crime.lat, crime.lng))
                crime.nhood = cr.nhood

        if crime.nhood != None:
            crimes_new.append(crime)
            print("Crime {} fixed".format(counter))
        counter += 1

    crimes_new.extend(crimes_old)

    print('Ended fixing missing values')
    return crimes_new

"""

The method groups the crimes into neighbourhoods
The list of crimes is returned, but for each Crime object a Neighbourhood object is assigned

Efficient algorithm used, by going through the crimes every time, but once a crime has
a neighbourhood assigned, it gets moved to the 'resolved' list
The efficiency is traded off for memory

"""
def group_crimes_by_nhood(crimes, nhoods):
    print('Started nhoods and crime grouping')

    crimes_old = crimes
    crimes_new = []

    for hood in nhoods:

        polygon = geometry.Polygon(hood.polygon)
        crimes_temp = []

        for crime in crimes_old:
            point = geometry.Point(crime.lat, crime.lng)

            if polygon.contains(point):
                crime.nhood = hood
                crimes_new.append(crime)
            else:
                crimes_temp.append(crime)
        crimes_old = crimes_temp
    print('Ended nhoods and crime grouping')

    if len(crimes_old) > 0:
        crimes_new = fix_missing_crime_hood(crimes_new, crimes_old)

    return crimes_new

"""

The method returns a list as long as the nr. of hoods
Each index contains a frequency dictionary with key
being the crime type and value, the number of happenings
There is also a 'total' key, which has the total nr. of crimes in that hood

"""
def hood_crime_frequency(crimes, nhoods):
    crime_nr = []

    for hood in nhoods:
        counter = 0
        dct = {}

        for crime in crimes:
            if crime.nhood.name == hood.name:
                counter = counter + 1

                if crime.type in list(dct.keys()):
                    dct[crime.type] = dct[crime.type] + 1
                else:
                    dct[crime.type] = 1

        dct['total'] = counter
        crime_nr.append(dct)

    return crime_nr
