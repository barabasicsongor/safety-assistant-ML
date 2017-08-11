import json
import requests
import datetime

def getDate(date_str):
    year, month, day = (int(x) for x in date_str.split('-'))
    ans = datetime.date(year, month, day)
    return ans

def final_json(event, text, should_end):
    return {
		"response": {
			"outputSpeech": {
				"type": "PlainText",
				"text": text
			},
			"card": {
				"content": text,
				"title": "SafetyAssistant Answer",
				"type": "Simple"
			},
			"shouldEndSession": should_end
		}
	}

def launch_req(event):
    return final_json(event, "Hello. How can I help you?", False)

def end_req(event):
    return final_json(event, "Goodbye!", True)

def help_req(event):
    return final_json(event, "Say for example: Is it safe tomorrow on California street?", False)

def int_req(event):
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
            return final_json(event, "Sorry. Something went wrong. Please try again.", False)

    try:
        address = slots['street_address']['value']
    except:
        try:
            address = slots['zip']['value']
        except:
            return final_json(event, "Sorry. Something went wrong. Please try again.", False)

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

    return final_json(event, result_str, True)


def lambda_handler(event, context):

    if event['session']['application']['applicationId'] != 'amzn1.ask.skill.03e0f3ce-8a37-4e1c-bd2f-6a7053028a60':
        raise ValueError('Invalid Application ID')

    session = event['session']
    request = event['request']

    if request['type'] == 'LaunchRequest':
    	return launch_req(event)
    elif request['type'] == 'SessionEndedRequest':
    	return end_req(event)
    else:
        if request['intent']['name'] == 'AMAZON.CancelIntent' or request['intent']['name'] == 'AMAZON.StopIntent':
            return end_req(event)
        elif request['intent']['name'] == 'AMAZON.HelpIntent':
            return help_req(event)
        else:
    	    return int_req(event)
