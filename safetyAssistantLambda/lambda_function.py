import json
import requests
import datetime

def getDate(date_str):
    year, month, day = (int(x) for x in date_str.split('-'))
    ans = datetime.date(year, month, day)
    return ans

def lambda_handler(event, context):
    
    sessionAttributes = event['sessionAttributes']
    slots = event['currentIntent']['slots']

    try:
        day = slots['day']
    except:
        try:
            date = slots['date']
            dt = getDate(date)
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day = days[dt.weekday()]
        except:
            return { 
                "sessionAttributes": sessionAttributes,
                "dialogAction": {
                    "type": "Close",
                    "fulfillmentState": "Fulfilled",
                    "message": {
                        "contentType": "PlainText",
                        "content": "Sorry. Something went wrong."
                    }
                }
            }

    
    try:
    	address = slots['street_address']
    except:
    	try:
    		address = slots['zip']
    	except:
    		return { 
                "sessionAttributes": sessionAttributes,
                "dialogAction": {
                    "type": "Close",
                    "fulfillmentState": "Fulfilled",
                    "message": {
                        "contentType": "PlainText",
                        "content": "Sorry. Something went wrong."
                    }
                }
            }

    city = 'San Francisco'
    place = "{}, {}".format(address, city)
    
    url = 'http://safetyassistant.us-east-1.elasticbeanstalk.com/api'
    data = json.dumps({'day': day, 'place': place})
    r = requests.post(url, data)
    r_json = r.json()

    result = float(r_json['results'])

    if result == -1:
        result_str = "I could not find any relevant data about the location."
    elif result >= 0 and result < 0.15:
    	result_str = "It is safe."
    elif result >= 0.15 and result < 0.4:
    	result_str = "It is relatively OK, but be careful."
    else:
    	result_str = "It is NOT safe."
    
    # result = "Going on {} to {}".format(day, place)
    
    response = {
        "sessionAttributes": sessionAttributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": result_str
            }
        }
    }
    
    return response
