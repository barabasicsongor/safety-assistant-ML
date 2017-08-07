import json
import requests
import datetime

def getDate(date_str):
    year, month, day = (int(x) for x in date_str.split('-'))
    ans = datetime.date(year, month, day)
    return ans

def lambda_handler(event, context):

    if event['session']['application']['applicationId'] != 'amzn1.ask.skill.03e0f3ce-8a37-4e1c-bd2f-6a7053028a60':
        raise ValueError('Invalid Application ID')

    session = event['session']
    slots = event['request']['intent']['slots']

    try:
        day = slots['day']['value']
    except:
        try:
            date = slots['date']['value']
            dt = getDate(date)
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day = days[dt.weekday()]
        except:
            return { 
                "sessionAttributes": {},
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": "Sorry. Something went wrong."
                    },
                    "card": {
                    	"content": "Sorry. Something went wrong.",
                    	"title": "Error",
                    	"type": "Simple"
                    },
                    "reprompt": {
                    	"outputSpeech": {
                    		"type": "PlainText",
                    		"text": ""
                    	}
                    }
                }
            }


    street = slots['street_address']['value']
    city = slots['city']['value']
    place = "{}, {}".format(street, city)

    url = 'http://safetyassistant.us-east-1.elasticbeanstalk.com/api'
    data = json.dumps({'day': day, 'place': place})
    r = requests.post(url, data)
    r_json = r.json()

    result = float(r_json['results'])

    if result == -1:
        result_str = "I could not find any relevant data about the location."
    elif result >= 0 and result < 0.15:
    	result_str = "All I can say is have fun buddy, enjoy your time while you're there!"
    elif result >= 0.15 and result < 0.4:
    	result_str = "The area you are going to is not that dangerous, but still be careful!"
    elif result >= 0.4 and result < 0.7:
    	result_str = "The area you are going to is unsafe. Try not to be too adventurous!"
    else:
    	result_str = "The area you are going to is extremely dangerous. Be careful, and don't go there on your own!"
    
    # result = "Going on {} to {}".format(day, place)

    response = { 
                "sessionAttributes": {},
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": result_str
                    },
                    "card": {
                    	"content": result_str,
                    	"title": "Response",
                    	"type": "Simple"
                    },
                    "reprompt": {
                    	"outputSpeech": {
                    		"type": "PlainText",
                    		"text": ""
                    	}
                    }
                }
            }
    
    return response
