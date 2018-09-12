from __future__ import print_function
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

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

def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = os.environ["GREETING_MSG"]
    reprompt_text = "To hear available stats, ask what stats are available"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = os.environ["EXIT_MSG"]
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def query_dynamodb_stat(table,stat):
    try:
        response = table.get_item(
            Key={'name':stat}
        )
    except KeyError:
        return -1
    except Exception:
        return -1
    return response['Item']['count']
        
def query_dynamodb_specific_tweet(table,stat):
    try:
        response = table.get_item(
        Key={'name':stat}
        )
    except KeyError:
        return -1
    except Exception:
        return -1
    return (response['Item']['count'],response['Item']['tweet_text'])

def get_total_tweets(table, intent, session):
    session_attributes = {}
    reprompt_text = "Sorry, I didn't understand. Please ask again"
    try:
        stat_value = query_dynamodb_stat(table, intent['slots'][os.environ["SLOT_NAME"]]['value'].upper())
        if stat_value:
            speech_output = "The number of " + intent['slots'][os.environ["SLOT_NAME"]]['value'] + " is " + str(stat_value)
            should_end_session = False
    except Exception:
        speech_output = os.environ["EXCEPTION_MSG"]
        should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def get_specific_tweet(table, intent, session):
    session_attributes = {}
    reprompt_text = "Sorry, I didn't understand. Please ask again"
    try:
        count,text = query_dynamodb_specific_tweet(table, intent['slots']['tweetType']['value'].upper())
        print("Stat value is: ", text)
        if count:
            speech_output = "With " + str(count) + " " + intent['slots']['tweetType']['value'].upper() + ", the tweet is " + str(text)
        else:
            speech_output = "The " + intent['slots']['tweetType']['value'].upper() + " tweet is " + str(text)
        should_end_session = False
    except Exception:
        speech_output = os.environ["EXCEPTION_MSG"]
        should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
        
def get_sentiment(table, intent, session):
    session_attributes = {}
    reprompt_text = "Sorry, I didn't understand. Please ask again"
    try:
        response = table.get_item(Key={'name':'SENTIMENT'})
    except Exception:
        speech_output = os.environ["EXCEPTION_MSG"]
        should_end_session = False    
    sentiment_categories = {'POSITIVE':response['Item']['POSITIVE'],'NEGATIVE':response['Item']['NEGATIVE'],'NEUTRAL':response['Item']['NEUTRAL'],'MIXED':response['Item']['MIXED']}
    sentiment = max(sentiment_categories, key=sentiment_categories.get)
    print (sentiment)
    if sentiment:
        speech_output = "People are feeling " + sentiment + " about your corporation.”
        should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(table, session_started_request, session):

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(table, launch_request, session):
    return get_welcome_response()

def on_intent(table, intent_request, session):

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name.upper() == "TOTALTWEETS":
        return get_total_tweets(table, intent, session)
    if intent_name.upper() == "SPECIFICTWEET":
        return get_specific_tweet(table,intent,session)
    if intent_name.upper() == "SENTIMENT":
        return get_sentiment(table,intent,session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        reprompt_text = "Sorry, I didn't understand. Please try again."
        should_end_session = False

def on_session_ended(table, session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])

# --------------- Main handler ------------------

def lambda_handler(event, context):
    print(event)
    
    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")
    
    indexEndRegion = context.invoked_function_arn[15:30].find(":")+15
    region = context.invoked_function_arn[15:indexEndRegion]
    dynamodb = boto3.resource('dynamodb', region_name=region, endpoint_url="https://dynamodb."+region+".amazonaws.com")
    stats_table = dynamodb.Table(os.environ["STATS_TABLE"])
    
    try:
        if event['session']['new']:
            on_session_started(stats_table, {'requestId': event['request']['requestId']}, event['session'])
    except KeyError:
        print("Message")
    if event['request']['type'] == "LaunchRequest":
        print ("launching")
        return on_launch(stats_table, event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        print ("calling an intent")
        return on_intent(stats_table, event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        print("Session End Requested")
        return on_session_ended(stats_table, event['request'], event['session'])
