from datetime import datetime

class Crime(object):

    def __init__(self, type, weekday_name, date_time, lat, lng, is_crime, nhood):
        self.type = type
        self.weekday_name = weekday_name
        self.date_time = date_time
        self.lat = lat
        self.lng = lng
        self.is_crime = is_crime
        self.nhood = nhood

    def __str__(self):
        return self.type

    def to_json(self):
        js = '{'
        js += '"type": "{}", "weekday_name": "{}", "date": "{}", "time": "{}", "lat": {}, "lng": {}, "is_crime": {}, "hood_name": "{}"'\
            .format(self.type, self.weekday_name, self.date_time.date(), self.date_time.time(), self.lat, self.lng,
                    int(self.is_crime), self.nhood.name)
        js += '}'
        return js
