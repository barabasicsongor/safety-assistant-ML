import json
import requests

def lambda_handler(event, context):
    
    sessionAttributes = event['sessionAttributes']
    day = event['currentIntent']['slots']['day']
    street = event['currentIntent']['slots']['street_address']
    city = event['currentIntent']['slots']['city']
    place = "{}, {}".format(street, city)
    
    url = 'http://safetyassistant.eu-west-2.elasticbeanstalk.com/api'
    data = json.dumps({'day': day, 'place': place})
    r = requests.post(url, data)
    r_json = r.json()

    result = float(r_json['results'])

    if result >= 0 and result < 0.15:
    	result_str = "All I can say is have fun buddy, enjoy your time while you're there!"
    elif result >= 0.15 and result < 0.4:
    	result_str = "The area you are going to is not that dangerous, but still be careful!"
    elif result >= 0.4 and result < 0.7:
    	result_str = "The area you are going to is unsafe. Try not to be too adventurous!"
    else:
    	result_str = "The area you are going to is extremely dangerous. Be careful, and don't go there on your own!"
    
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
