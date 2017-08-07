from geopy.distance import vincenty
# from geopy.geocoders import Nominatim
from geopy import geocoders
from geopy.exc import GeocoderTimedOut
from colour import Color
import sys

"""

Returns the distance in meters between two coordinates
Params: (lat, lng) (lat, lng)

"""
def get_distance_in_meters(coord_1,coord_2):
    return vincenty(coord_1,coord_2).meters

"""

Returns the distance in miles between two coordinates
Params: (lat, lng) (lat, lng)

"""
def get_distance_in_miles(coord_1,coord_2):
    return vincenty(coord_1,coord_2).miles

"""

Returns the latitude and longitude of the address given
using reverse geocoding

"""
# geolocator = Nominatim(scheme='http')
geolocator = geocoders.GoogleV3(scheme="http")
def reverse_geocode(place):
    try:
        location = geolocator.geocode(place)
        return location.latitude, location.longitude
    except GeocoderTimedOut:
        return reverse_geocode(place)

"""

The method generates a list of colors, which are the gradient from
start_hex to end_hex. The number of colors between is determined
by grad_steps, which has start end end hex inclusive

"""
def generate_color_gradient(start_hex, end_hex, grad_steps):
    color = Color(start_hex)
    colors = list(color.range_to(Color(end_hex), grad_steps))
    return colors

"""

Sorting the nhoods according to crime_freq[x]['total']
which represents the total nr of crimes in that hood
Algorithm: Insertion sort, simultaneously for two lists

"""
def sim_sort(crime_freq, nhoods):
    old_crime_freq = crime_freq
    old_nhoods = nhoods
    new_crime_freq = []
    new_nhoods = []

    while len(old_crime_freq) > 0:

        # Find index of min element
        min = sys.maxsize
        index = -1
        for i in range(0, len(old_crime_freq)):
            if old_crime_freq[i]['total'] < min:
                min = old_crime_freq[i]['total']
                index = i

        new_crime_freq.append(old_crime_freq[index])
        new_nhoods.append(old_nhoods[index])
        del old_crime_freq[index]
        del old_nhoods[index]

    return new_crime_freq, new_nhoods

"""

Get the part of the day: Night (21 - 5), Morning (5 - 12), Afternoon (12 - 17), Evening (17 - 21)
Parameter is a datetime object

"""
def get_day_part(date_time):
    if date_time.hour >= 21 or date_time.hour < 5:
        return 'Night'
    elif date_time.hour >= 5 and date_time.hour < 12:
        return 'Morning'
    elif date_time.hour >= 12 and date_time.hour < 17:
        return 'Afternoon'
    elif date_time.hour >= 17 and date_time.hour < 21:
        return 'Evening'

def get_nhood(nhoods, point):

    h = ''

    for hood in nhoods:
        if hood.polygon.contains(point):
            h = hood.name
            break

    if h == '':
        pass

    return h