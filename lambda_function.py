"""
This is a Python template for Alexa to get you building skills (conversations) quickly.
"""

from __future__ import print_function

import urllib.request
import requests
import json


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
def get_search_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    print("inside the function!!!");
    city = intent['slots']['city']['value'];
    city = city.split(' ');
    param = dict()
    param["country"] = "US"
    param["currency"] = "USD"
    param["locale"] = "en-US"
    param["originplace"] = "SFO-sky"
    param["destinationplace"] = "JFK-sky"
    param["outboundpartialdate"] = "2019-09-01"

    flight = Flight(param)

    print(flight.browsequotes())
    session_attributes = {}
    card_title = "Test"
    speech_output = "please name sourse and distination city to search for tickets"
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_average_response():
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    session_attributes = {}
    card_title = "Test"
    speech_output = "please name sourse and distination city to search for average price for tickets"
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "to search for the tickets name first sourse city then distination city!"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, welcome to your custom alexa application!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "search":
        return get_search_response(intent)
    if intent_name == "average":
        return get_average_response()
    if intent_name == "cheapest":
        return get_cheapest_response()
    if intent_name == "direct":
        return get_direct_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


class Flight:
    headers = {
        "X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        "X-RapidAPI-Key": "2c2e4d17b0mshcc471f8a7475016p16c892jsn034748cb94d5"
    }

    attr = ""

    type = ""

    # Class Attribute
    version = "v1.0"

    URI = ""

    BASE_URI = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices"

    # instance method
    def browsequotes(self, attr):
        self.attr = attr
        self.build_url("browsequotes")
        response = requests.get(self.URI, None, headers=self.headers)
        return response.json()

    def suggest_places(self, attr):
        self.attr = attr
        self.build_url("autosuggest")
        print(self.URI)
        response = requests.get(self.URI, None, headers=self.headers)
        # response = urllib.request.urlopen(request)
        return response.json()
        # response = urllib.request.urlopen(request)
        # return response.read().decode('utf-8')

    def build_url(self, type):
        separator = "/"
        self.URI = ""
        self.URI = self.BASE_URI + separator + type + separator + self.version
        for k, v in self.attr.items():
            print(k)
            print(v)
            if k == 'query':
                self.URI += "/?query=" + v
            if k != 'query':
                self.URI += separator + v


class Location:

    # Initializer / Instance Attributes
    def __init__(self, city):
        self.city = city

    headers = {
            "X-RapidAPI-Host": "devru-latitude-longitude-find-v1.p.rapidapi.com",
            "X-RapidAPI-Key": "2c2e4d17b0mshcc471f8a7475016p16c892jsn034748cb94d5"
    }

    URI = "https://devru-latitude-longitude-find-v1.p.rapidapi.com/latlon.php?location="

    city = ""

    def get(self):
        self.URI += self.city
        print(self.URI)
        request = urllib.request.Request(self.URI, None, self.headers)
        response = urllib.request.urlopen(request)
        return response.read().decode('utf-8')


print("inside the function!!!")
city = "Berlin Barcelona"

city = city.split(' ')


# location = Location(city[0])
# print(location.get())

flight = Flight()


places = dict()
places["country"] = "DE"
places["currency"] = "EUR"
places["locale"] = "en-DE"
places["query"] = "Berlin"


print(flight.suggest_places(places))


places["query"] = "Paris"
print(json.dumps(flight.suggest_places(places), indent=4, sort_keys=True))

quotes = dict()
quotes["country"] = "DE"
quotes["currency"] = "EUR"
quotes["locale"] = "en-DE"
quotes["originplace"] = "TXL-sky"
quotes["destinationplace"] = "CDG-sky"
quotes["outboundpartialdate"] = "2019-09-01"
print(json.dumps(flight.browsequotes(quotes), indent=4, sort_keys=True))